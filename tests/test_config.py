"""Configuration that is silently wrong when it's wrong: base URL, template
metadata, and the version numbers that live in more than one file."""

from __future__ import annotations

import json
import re

import pytest

from conftest import REPO_ROOT
from lib import constants

INDEX_HTML = (REPO_ROOT / "templates" / "index.html").read_text()

# The template is heavily commented, and several comments quote the very tags
# they are explaining. Scanning for live markup has to ignore them.
INDEX_HTML_LIVE = re.sub(r"<!--.*?-->", "", INDEX_HTML, flags=re.S)


# ---------------------------------------------------------------------------
# BASE_URL guard
# ---------------------------------------------------------------------------


def test_default_base_url_is_the_public_domain():
    assert constants.DEFAULT_BASE_URL == "https://flows.2plot.dev"
    assert not constants.DEFAULT_BASE_URL.endswith("/")


def test_guard_is_inert_outside_production(monkeypatch):
    monkeypatch.delenv("RENDER", raising=False)
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("APP_BASE_URL", raising=False)
    constants.require_owned_base_url()  # must not raise locally or in CI


def test_an_unset_base_url_in_production_is_fine_here(monkeypatch):
    """DELIBERATE DIVERGENCE from the template — read before "fixing" it.

    On the boilerplate an unset APP_BASE_URL is fatal, because the default
    it would inherit is the TEMPLATE's origin: a fork deploying that way
    serves boilerplate.2plot.dev canonicals on every page and asks to be
    deindexed. Here DEFAULT_BASE_URL is already this app's own public
    origin, so inheriting it is not merely safe, it is the correct
    production posture — and the failure that actually bites, a
    platform-generated hostname, is still caught by the test below.
    """
    monkeypatch.setenv("RENDER", "true")
    monkeypatch.delenv("APP_BASE_URL", raising=False)
    monkeypatch.delenv("DASH_FLOWS_BASE_URL", raising=False)
    constants.require_owned_base_url()  # must not raise


def test_guard_rejects_platform_hostnames(monkeypatch):
    monkeypatch.setenv("RENDER", "true")
    monkeypatch.setenv("APP_BASE_URL", "https://my-docs.onrender.com")
    with pytest.raises(RuntimeError, match="platform-generated"):
        constants.require_owned_base_url("https://my-docs.onrender.com")


def test_guard_accepts_a_real_domain(monkeypatch):
    monkeypatch.setenv("RENDER", "true")
    monkeypatch.setenv("APP_BASE_URL", "https://leaflet.2plot.dev")
    constants.require_owned_base_url("https://leaflet.2plot.dev")


# ---------------------------------------------------------------------------
# index.html
# ---------------------------------------------------------------------------


def test_template_has_no_hardcoded_canonical():
    """The package injects a per-page canonical. A second one in the template
    doesn't override it — both ship, and a conflicting pair is no signal."""
    live = re.findall(r'<link[^>]+rel="canonical"[^>]*>', INDEX_HTML_LIVE)
    assert live == [], f"remove the hard-coded canonical: {live}"


def test_template_has_no_placeholder_hosts():
    """Placeholder identities in the MARKUP, which is what ships to a reader.

    Comments are stripped first, on purpose and with one narrow exception
    below. The point of this test is a placeholder that reaches a crawler —
    a `content=` or an `href=` — not the word "onrender.com" appearing in a
    comment that EXPLAINS why hits on that hostname are consolidated onto
    the canonical. Two of the strings below are prose fragments that a
    comment may legitimately discuss.

    THE EXCEPTION, and it is not a general licence for comments: a comment
    is not always inert. `data-dimll-prerender` in a comment silently
    disabled this site's entire prerender for months, because the package
    probes for it as a substring of the whole document — see
    tests/test_prerender.py, which checks the raw bytes precisely because
    that string is NOT safe in a comment. Strip comments here; never there.
    """
    markup = re.sub(r"<!--.*?-->", "", INDEX_HTML, flags=re.S)
    for placeholder in ("yourdomain.com", "onrender.com", "Your Organization Name",
                        "Your Name or Organization", "plotly.pro"):
        assert placeholder not in markup, (
            f"{placeholder!r} left in the served markup of templates/index.html"
        )


def test_template_references_only_assets_that_exist():
    """A <link> or <meta> pointing at a missing asset is a 404 on every page
    load — invisible in a browser, noisy in the logs, and a broken preview
    card on every share."""
    referenced = set(
        re.findall(
            r'["\'(](?:https://boilerplate\.2plot\.dev)?/assets/([^"\')\s]+)',
            INDEX_HTML_LIVE,
        )
    )
    missing = {name for name in referenced if not (REPO_ROOT / "assets" / name).exists()}
    assert not missing, f"index.html references assets that do not exist: {sorted(missing)}"


def test_structured_data_parses():
    """Valid JSON-LD describing at least the software and the site.

    Shape differs from the template's deliberately: this site declares ONE
    script carrying an `@graph` of typed nodes rather than two sibling
    scripts. Both are valid JSON-LD and Google reads them identically, so
    the assertion is on the node COUNT after flattening the graph, not on
    how many script tags the author chose.
    """
    blocks = re.findall(
        r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', INDEX_HTML, re.S
    )
    assert blocks, "no JSON-LD at all in templates/index.html"

    nodes = []
    for block in blocks:
        parsed = json.loads(block)  # raises on malformed markup
        nodes.extend(parsed.get("@graph", [parsed]))

    types = {node.get("@type") for node in nodes}
    assert len(nodes) >= 2, f"expected the software and the site described; got {types}"
    assert "WebSite" in types, f"no WebSite node — types present: {types}"
    assert types & {"SoftwareSourceCode", "SoftwareApplication"}, (
        f"nothing describes the software itself — types present: {types}"
    )


def test_declared_software_version_matches_constants():
    """Two places hold the version; they drift the moment one is bumped alone."""
    blocks = re.findall(
        r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', INDEX_HTML, re.S
    )
    # `softwareVersion` on SoftwareApplication, `version` on
    # SoftwareSourceCode (which inherits it from CreativeWork) — the same
    # declaration under the name schema.org gives it for the type used.
    versions = []
    for block in blocks:
        for node in json.loads(block).get("@graph", [json.loads(block)]):
            for key in ("softwareVersion", "version"):
                if key in node:
                    versions.append(node[key])
    assert versions == [constants.APP_VERSION], (
        f"index.html declares softwareVersion {versions}, lib/constants.py says "
        f"{constants.APP_VERSION}"
    )


# ---------------------------------------------------------------------------
# The title element
#
# dash-improve-my-llms locates it with `re.compile(r"<title>.*?</title>",
# DOTALL | IGNORECASE)` and rewrites the first match. Two ways that goes
# wrong, both silent:
#
#   - No element at all: nothing to anchor on, so no page gets a title.
#   - The tag name written in angle brackets inside a nearby comment: the
#     match starts THERE and runs to the next closing tag, so every line in
#     between is replaced by the rewritten title and disappears from the
#     served page. With rewriting on it still looks correct.
# ---------------------------------------------------------------------------

TITLE_RE = re.compile(r"<title>.*?</title>", re.S | re.I)


def test_template_uses_the_dash_title_placeholder():
    """A hard-coded title discards the per-page titles pages/markdown.py
    registers, and makes every page depend on the package rewriting it."""
    assert "<title>{%title%}</title>" in INDEX_HTML


def test_only_one_title_match_and_it_is_the_element():
    """Guards the comment trap in both directions."""
    matches = TITLE_RE.findall(INDEX_HTML)
    assert matches == ["<title>{%title%}</title>"], (
        "the title regex matched something other than the element itself — "
        "check for the tag name written in angle brackets inside a comment"
    )


def test_no_title_tag_spelled_out_in_comments():
    for comment in re.findall(r"<!--.*?-->", INDEX_HTML, re.S):
        assert "<title" not in comment.lower(), (
            "a comment spells the title tag in angle brackets; the package's "
            "regex would start matching there and swallow the lines that follow"
        )


def test_app_title_is_set(app_module):
    """`{%title%}` resolves to app.title in the served HTML. Unset, Dash's
    default is the bare string "Dash" on every page."""
    assert app_module.app.title == constants.APP_TITLE
    assert constants.APP_TITLE != "Dash"


def test_no_dead_llm_endpoints_advertised():
    """/page.json and /architecture.txt were removed in dash-improve-my-llms
    2.0. Advertising them points agents at two 404s."""
    for dead in ("/page.json", "/architecture.txt", "/llms.toon"):
        assert dead not in INDEX_HTML_LIVE, (
            f"{dead} is no longer served but is still advertised"
        )


# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------


def test_the_installed_package_meets_the_floor(app_module):
    """Fail with the reason, not with thirty downstream symptoms.

    An IDE run configuration pointing at another project's virtualenv starts
    this app quite happily against whatever versions that environment holds.
    On dash-improve-my-llms 2.0.0 there is no `llms_viewer.py` at all, so
    `/<page>/llms.txt` serves plain Markdown to everyone and the negotiation
    tests below fail in a way that reads like a bug in the app. It isn't; it's
    the interpreter.
    """
    import sys

    import dash_improve_my_llms as pkg

    installed = tuple(int(p) for p in pkg.__version__.split(".")[:3] if p.isdigit())
    assert installed >= app_module.LLMS_PKG_FLOOR, (
        f"dash-improve-my-llms {pkg.__version__} is below the "
        f"{app_module.LLMS_PKG_FLOOR} floor. Running from {sys.executable} — "
        "if that is not this project's .venv, that is the whole problem."
    )


# ---------------------------------------------------------------------------
# Constructor arguments
# ---------------------------------------------------------------------------


def test_mcp_kwargs_are_omitted_when_mcp_is_off(app_module):
    """Dash raises TypeError on unknown constructor keywords.

    `enable_mcp` landed in Dash 4.3, so naming it unconditionally made the app
    refuse to boot on 4.2 with `Dash() got an unexpected keyword argument
    'enable_mcp'` — an error that says nothing about MCP, over a feature that
    is off by default.
    """
    # This fork never wired MCP, so there is no MCP_KWARGS to inspect — the
    # equivalent assertion is that no MCP keyword reaches the constructor
    # through the kwargs dict run.py actually builds. Same defect guarded:
    # Dash raises TypeError on unknown constructor keywords, so an
    # `enable_mcp` leaking in here would make the app refuse to boot on 4.2
    # with an error that says nothing about MCP.
    kwargs = app_module._dash_kwargs
    leaked = [k for k in kwargs if "mcp" in k.lower()]
    assert not leaked, (
        f"MCP is not wired on this site, so no MCP keyword should reach the "
        f"Dash constructor at all; found {leaked}"
    )


# ---------------------------------------------------------------------------
# Repo hygiene
# ---------------------------------------------------------------------------


# Live links to domains that have been retired. Matching the URL rather than
# the bare hostname on purpose: the changelog has to name plotly.pro in the
# entry that records its removal, and that mention is not a broken link.
# plotly.pro retired in favour of 2plot.ai; pip-install-python.com retired
# network-wide by the fleet's retire-pip-install-python-domain sweep, with
# 2plot.dev as its successor as the package index (lib/network_directory.py
# documents its deliberate absence from the directory).
#
# README.md is EXCLUDED below, not overlooked: it is the GitHub repo page,
# not a surface this site serves, and rewriting a package README's prose is
# the named fleet sweep's business rather than this pass's. Everything the
# app actually serves is in scope.
RETIRED_LINKS = re.compile(
    r"https?://(?:www\.)?(plotly\.pro|pip-install-python\.com)"
)

SKIP_DIRS = {".venv", "node_modules", ".git", "__pycache__", ".claude", "vendor",
             ".idea", "build", "dist", "src", "examples", "venv",
             "dash_flows.egg-info", "dash_flows"}
SKIP_FILES = {"README.md", "CHANGELOG.md", "CONTRIBUTING.md",
              "X402-SYNC-REPORT.md"}


def test_no_links_to_retired_domains():
    """plotly.pro was retired in favour of 2plot.ai."""
    offenders = []
    for path in REPO_ROOT.glob("**/*"):
        if not path.is_file() or path.suffix not in {".py", ".md", ".html", ".css", ".yml"}:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_FILES:
            continue
        for match in RETIRED_LINKS.finditer(path.read_text(errors="ignore")):
            offenders.append(f"{path.relative_to(REPO_ROOT)} -> {match.group(1)}")
    assert offenders == [], f"links to retired domains: {offenders}"
