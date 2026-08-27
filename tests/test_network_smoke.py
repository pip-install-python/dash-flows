"""Run the network battery against the in-process app.

`scripts/network_smoke.py` only ever executes in two places a developer never
watches: against the container CI just booted, and against production after a
deploy. That is exactly the code that rots — a typo in a check turns it into a
silent pass and the battery keeps reporting green over a broken host.

So it runs here too, with its fetchers pointed at the test client. Three
distinct things get proven, and it is worth being explicit about which:

1. the battery's own logic still works (the checks fire, and they can fail);
2. this app satisfies every check the network standard makes of a satellite;
3. the per-site block at the top of the script — the expected H1, the sample
   page, the card URL — still matches the app it describes.

What it cannot prove is the deployed artifact, which is the whole reason the
container run and the post-deploy run exist as well.
"""

from __future__ import annotations

import importlib.util
import re
import sys

import pytest

from conftest import REPO_ROOT
from lib.constants import (
    BASE_URL,
    INTERNAL_UA_TOKEN,
    OG_IMAGE_HEIGHT,
    OG_IMAGE_URL,
    OG_IMAGE_WIDTH,
    SITE_BRAND,
)

BASE = BASE_URL


def _png_header(width: int, height: int) -> bytes:
    """The first 24 bytes of a PNG: signature, chunk length, IHDR, w, h.

    Enough for the battery's dimension check, which reads bytes 16..24. A real
    file is not needed and would only make this suite depend on Cloudflare.
    """
    return (b"\x89PNG\r\n\x1a\n"
            + (13).to_bytes(4, "big") + b"IHDR"
            + width.to_bytes(4, "big") + height.to_bytes(4, "big"))


@pytest.fixture(scope="module")
def battery():
    spec = importlib.util.spec_from_file_location(
        "network_smoke", REPO_ROOT / "scripts" / "network_smoke.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["network_smoke"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def wired(battery, client, monkeypatch):
    """Point the battery's `fetch_raw` at the test client.

    `fetch` delegates to `fetch_raw`, so patching the one covers both. The
    signature is `fetch_raw(url, ua=..., method=..., body=..., headers=...)`
    returning `(status, lowercased_headers, bytes)`. Only GET is used by the
    satellite battery, so a non-GET here is a bug in the script rather than
    something to emulate.
    """
    seen_agents = []

    def fetch_raw(url, ua=battery.UA, method="GET", body=None, headers=None,
                  timeout=None, retries=1):
        assert method == "GET", f"the satellite battery issued a {method}"
        seen_agents.append(ua)

        # Off-host URLs — today just the CDN-hosted social card — resolve to a
        # synthetic PNG header of the declared size. Reaching the real CDN from
        # a unit test would make the suite depend on another service being up;
        # that the asset genuinely resolves, and is genuinely that shape, is
        # the DEPLOYED battery's job, which is where the check earns its keep.
        if not url.startswith(BASE) and "://" in url:
            return (200, {"content-type": "image/png"},
                    _png_header(OG_IMAGE_WIDTH, OG_IMAGE_HEIGHT))

        path = url[len(BASE):] if url.startswith(BASE) else url
        accept = (headers or {}).get("Accept")
        response = client.get(path or "/", user_agent=ua, accept=accept)
        return response.status, dict(response.headers), response.raw

    monkeypatch.setattr(battery, "fetch_raw", fetch_raw)
    monkeypatch.setattr(battery, "_RESULTS", [])
    # This seat's interpreter is the SUITE's, not a deploy artifact: /healthz
    # here reports whichever Python is running pytest, which on a developer
    # machine or the examples matrix' window legs is deliberately not the
    # fleet Python. python_matches_declared still proves the field EXISTS;
    # holding a served interpreter to the Dockerfile's minor is the container
    # and production seats' job, and both of those are armed.
    monkeypatch.setattr(battery, "declared_python_minor", lambda: None)
    battery.seen_agents = seen_agents
    return battery


def test_the_battery_passes_against_this_app(wired, capsys):
    wired.satellite_checks(BASE)
    output = capsys.readouterr().out

    failed = [(name, detail) for name, verdict, detail in wired._RESULTS
              if verdict == wired.FAIL]
    assert failed == [], f"battery failures against the in-process app:\n{output}"
    assert len(wired._RESULTS) >= 11, "checks silently stopped running"


def test_every_request_the_battery_makes_is_internal(wired):
    """A battery that pollutes the ledger it is auditing is worse than none."""
    wired.satellite_checks(BASE)
    untokened = [ua for ua in wired.seen_agents if INTERNAL_UA_TOKEN not in ua]
    assert untokened == [], f"battery sent untokened User-Agents: {untokened}"


def test_the_expected_h1_tracks_the_brand_constant(battery):
    """The per-site block is a copy of `SITE_BRAND`; copies drift."""
    assert battery.SITE_H1 == f"# {SITE_BRAND}"


def test_the_card_constants_track_lib_constants(battery):
    assert battery.OG_IMAGE_URL == OG_IMAGE_URL
    assert battery.OG_IMAGE_WIDTH == OG_IMAGE_WIDTH
    assert battery.OG_IMAGE_HEIGHT == OG_IMAGE_HEIGHT


def test_the_sample_page_is_a_page_this_app_actually_has(battery, page_paths):
    assert battery.SAMPLE_PAGE in page_paths, (
        f"the battery probes {battery.SAMPLE_PAGE}, which is not registered"
    )


def test_the_battery_reports_a_failure_rather_than_swallowing_it(wired):
    """The check that keeps every other assertion here honest.

    If `check()` ever caught too broadly, the battery would print `pass` for a
    host that is on fire. Break one expectation on purpose and require it to be
    reported.
    """
    wired.SITE_H1 = "# not this site"
    try:
        wired.satellite_checks(BASE)
    finally:
        wired.SITE_H1 = f"# {SITE_BRAND}"

    verdicts = {name: verdict for name, verdict, _ in wired._RESULTS}
    assert verdicts.get("llms_txt_identity") == wired.FAIL


def test_the_card_check_catches_a_resized_cdn_object(wired):
    """The failure no offline test can see, simulated.

    Someone re-exports the card at 1280x640 and uploads it. Every unit test
    stays green; the tags still say 1200x630; the platform reserves that box
    and crops into the new file. Only a battery that reads the real bytes
    notices.
    """
    original = wired.fetch_raw

    def resized(url, **kw):
        if not url.startswith(BASE) and "://" in url:
            return 200, {"content-type": "image/png"}, _png_header(1280, 640)
        return original(url, **kw)

    wired.fetch_raw = resized
    try:
        wired.satellite_checks(BASE)
    finally:
        wired.fetch_raw = original

    verdicts = {name: verdict for name, verdict, _ in wired._RESULTS}
    assert verdicts.get("social_card_real_pixels") == wired.FAIL


def test_the_default_base_url_matches_the_container_port(battery):
    """CI boots the image and runs the battery with no --base-url.

    ADAPTED FROM dash-email: that Dockerfile spells the fallback inline
    (`:${PORT:-8054}`); this one sets `ENV PORT=8560` and binds `:${PORT}`.
    Same contract — the battery's default port must be the port the container
    actually answers on — asserted against the shape this Dockerfile uses.
    """
    dockerfile = (REPO_ROOT / "Dockerfile").read_text()
    port = battery.DEFAULT_BASE_URL.rsplit(":", 1)[1]
    assert f"EXPOSE {port}" in dockerfile, (
        f"the battery defaults to port {port}; the image exposes something else"
    )
    assert f"PORT={port}" in dockerfile, (
        f"the battery defaults to port {port}; the image's ENV default differs"
    )
    assert ":${PORT}" in dockerfile, "the CMD binds a different port"


def test_battery_urlopens_pass_the_ssl_context():
    """Source pin: every urlopen in network_smoke.py carries an SSL context.

    Same class as the smoke_live pin (tests/test_smoke_live.py), and the same
    blind spot: `fetch_raw` raises after its retries, so a handshake this
    battery cannot complete surfaces as `FAIL healthz responds 200` — it
    reads a healthy host as DOWN. macOS Python has no OS trust-store
    integration, so that is every local run against production; CI is Linux
    and never sees it. No wired test can either — they monkeypatch
    `fetch_raw` — which leaves the source as the only place to hold the line.

    Added fleet-wide 2026-08-26. The template's own copy still lacked it at
    1.6.29 (5589318): reported upstream, applied here first.
    """
    source = (REPO_ROOT / "scripts" / "network_smoke.py").read_text(
        encoding="utf-8"
    )
    calls = re.findall(r"urlopen\((?:[^)]|\n)*?\)", source)
    assert calls, "no urlopen calls found in network_smoke.py — rewritten?"
    naked = [c for c in calls if "context=SSL_CONTEXT" not in c]
    assert not naked, (
        f"urlopen without context=SSL_CONTEXT in network_smoke.py: {naked} — "
        "from a Mac this reads every healthy host as down"
    )
