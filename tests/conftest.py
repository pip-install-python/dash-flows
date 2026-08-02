"""Shared fixtures — boot the real app once, then interrogate it.

The suite deliberately exercises `run.py` itself rather than a stripped-down
app assembled for testing. Nearly everything worth catching here lives in the
wiring: registration order (the visitor tracker has to be installed BEFORE
`add_llms_routes`, or bot traffic is never counted), which middleware runs
first, whether a page's prose survived to the response.  A test app that
re-implements that wiring tests the re-implementation.

Flask, forced. Unlike dash-email, this repo DOES have a `lib/backend.py` and
`run.py` accepts `DASH_BACKEND=flask|fastapi|quart` — but flask is the
deployed backend and the one the network's shared tests were written against,
so the env block below pins it. The `Client` wrapper is kept so the shared
network tests copied from the boilerplate and leaflet run unmodified.

SECRETLESS, AND ORDER MATTERS. The suite runs against the app exactly as CI's
zero-secret container does: no `CROSS_APP_WEBHOOK_SECRET` (the traffic reporter
never starts a thread), no `NETWORK_BULLETIN_URL` (the bulletin stays unwired),
and the analytics ledger in a temp dir.

The env block below has to run BEFORE anything imports `run.py`, because
`run.py` calls `load_dotenv()` at import time and a developer's local `.env`
would otherwise flip the app into a configured posture. `load_dotenv()` never
overrides an existing key, so pinning each secret to `""` here (falsy to every
`os.getenv(...) or None` reader in `lib/`) neutralises the file without
deleting it. In CI there is no `.env` at all and this is belt-and-braces. Same
pattern as 2plotai, pip-docs+, the boilerplate, leaflet and email.
"""

from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

# --- 1. Neutralise every secret (must precede any import of run.py) ---------
SECRET_ENV_KEYS = (
    "CROSS_APP_WEBHOOK_SECRET", "NETWORK_BULLETIN_URL",
    "SESSION_SECRET", "FLASK_SECRET_KEY",
    "DATABASE_URL",
)
for _key in SECRET_ENV_KEYS:
    os.environ[_key] = ""

# --- 2. Keep app state out of the repo --------------------------------------
# Without this the suite appends its own hits to the checked-out
# visitor_analytics.json / satellite_traffic.jsonl, which then show up in
# `git status` and, worse, in the next hourly rollup a developer's local run
# happens to send.
_TMP_STATE = tempfile.mkdtemp(prefix="dash-flows-tests-")
os.environ["TRAFFIC_ANALYTICS_FILE"] = os.path.join(_TMP_STATE, "visitor_analytics.json")
# Behind Cloudflare in production; in tests an outbound ip-api.com lookup per
# hit would make the suite depend on a third party being up.
os.environ["ANALYTICS_GEO_LOOKUP"] = "0"
# The reporter thread would otherwise start on import and wake up mid-suite.
os.environ["SATELLITE_REPORT_INTERVAL_S"] = "86400"
# `require_owned_base_url()` and the reporter both key off these; keep them
# inert. RENDER is popped rather than blanked because the check is truthiness.
os.environ["APP_ENV"] = "ci"
os.environ.pop("RENDER", None)
# This repo supports fastapi/quart via lib/backend.py; the suite runs the
# deployed backend only. The shared tests assume a WSGI test client.
os.environ["DASH_BACKEND"] = "flask"

BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
CRAWLER_UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

# What a real browser sends. `/<page>/llms.txt` negotiates on this header —
# not on the User-Agent — so it is what separates "a person opened the URL"
# from "an agent fetched it".
BROWSER_ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"

# The body dash-improve-my-llms serves when a page has no prose registered.
# Its presence on any page is the failure this whole network cares most about.
STUB_MARKER = "This page contains interactive content that requires JavaScript"

# A real documentation page, used wherever a test needs one that is not the
# home page. Mirrors scripts/network_smoke.SAMPLE_PAGE.
SAMPLE_PAGE = "/getting-started"


@pytest.fixture(scope="session")
def app_module():
    """Import run.py as a module, from the repo root.

    run.py opens 'templates/index.html' by relative path and pages/markdown.py
    globs 'docs/**/*.md', so the process CWD has to be the repo root regardless
    of where pytest was invoked from.
    """
    os.chdir(REPO_ROOT)
    spec = importlib.util.spec_from_file_location("runmod", REPO_ROOT / "run.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["runmod"] = module
    try:
        spec.loader.exec_module(module)
    except SystemExit:  # pragma: no cover - run.py doesn't call sys.exit today
        pass
    return module


@pytest.fixture(scope="session")
def app(app_module):
    return app_module.app


class Response:
    __slots__ = ("status", "text", "raw", "headers")

    def __init__(self, status: int, text: str, headers=None, raw: bytes = b"") -> None:
        self.status = status
        self.text = text
        # The undecoded body. Only one caller needs it — the social-card
        # checks read a PNG's IHDR chunk — but a lossy decode is one-way, so
        # it has to be kept here rather than reconstructed.
        self.raw = raw
        # Headers matter from 2.2.0 on: `/<page>/llms.txt` content-negotiates,
        # so the *type* of the response is part of the contract and `Vary` is
        # what stops a CDN serving cached HTML to the next agent. Keys are
        # lowercased so a caller never has to guess the casing a proxy chose.
        self.headers = {k.lower(): v for k, v in (headers or {}).items()}

    @property
    def ok(self) -> bool:
        return self.status == 200

    def header(self, name: str, default: str = "") -> str:
        return self.headers.get(name.lower(), default)

    @property
    def content_type(self) -> str:
        return self.header("Content-Type")

    def __repr__(self) -> str:  # pragma: no cover - assertion output only
        return f"<Response {self.status} {self.content_type} {len(self.text)}b>"


class Client:
    """One synchronous `.get()`, shaped like the network's shared tests expect."""

    def __init__(self, raw) -> None:
        self._raw = raw

    def get(self, path: str, user_agent: str = BROWSER_UA, accept: str = None) -> Response:
        headers = {"User-Agent": user_agent}
        if accept is not None:
            headers["Accept"] = accept

        r = self._raw.get(path, headers=headers)
        body = r.get_data()
        # errors="replace", not `as_text=True`: the latter decodes strictly and
        # raises UnicodeDecodeError on any binary response, so a test that
        # merely checks a favicon RESOLVES would blow up on the PNG's first
        # byte.
        return Response(r.status_code, body.decode("utf-8", "replace"),
                        dict(r.headers), body)


@pytest.fixture(scope="session")
def client(app):
    return Client(app.server.test_client())


@pytest.fixture(scope="session")
def tmp_state_dir():
    """Where the app's ledger and lease files live for this run."""
    return _TMP_STATE


@pytest.fixture(scope="session")
def pages(app_module):
    """Every registered page as (path, name, entry), sorted by path."""
    import dash

    return sorted(
        ((entry["path"], entry.get("name", ""), entry) for entry in dash.page_registry.values()),
        key=lambda item: item[0],
    )


@pytest.fixture(scope="session")
def page_paths(pages):
    return [path for path, _name, _entry in pages]


def main_body(html: str) -> str:
    """The prerendered <main> block, or '' when the document has none."""
    if "<main>" not in html:
        return ""
    return html.split("<main>", 1)[1].split("</main>", 1)[0]
