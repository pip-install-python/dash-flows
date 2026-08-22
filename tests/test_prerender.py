"""The universal prerender, from the app's side.

Split out from the boilerplate's tests/test_pages.py because this repo's
page-shape tests already live in test_site_identity.py — what is missing
here is the GENERIC lane, and it is missing for a reason this repo paid
for (see below).
"""

import re

from conftest import SAMPLE_PAGE


def test_prerender_rides_the_generic_lane_not_a_ua_gate(client):
    """The universal prerender must be in the initial HTML for a PLAIN
    client — no crawler user-agent. An outside SEO audit (2026-08-22) read
    five hosts as serving "Loading... and nothing else" to browsers; the
    prose was there all along, but every test in this repo fetched either
    with CRAWLER_UA (the separate bot-document path) or not at all, so a
    regression that disabled the universal lane was invisible to the suite.

    THIS HOST'S REGRESSION, and the reason the test is not merely a copy:
    dash-improve-my-llms decides whether it has already injected by testing
    whether the marker string appears ANYWHERE in the served document — a
    substring probe, not a node lookup. templates/index.html carried the
    marker inside an explanatory HTML comment, so every response read as
    already-injected and the entire prerender was silently off in
    production from the day that comment was written. Never spell the
    marker in any served template or asset; not even in a comment warning
    about this, which is why the one in index.html now describes the block
    without naming its attribute.

    Since the 2.6.1 floor the block must also be VISIBLE: dimll <= 2.6.0
    shipped the div with a literal `hidden` attribute, so every
    visibility-respecting text extractor saw only "Loading..." — present
    and invisible, the worst of both. 2.6.1 serves it visible and hides it
    via a synchronous inline script that only JS browsers execute.
    """
    for path in ("/", SAMPLE_PAGE):
        html = client.get(path).text  # non-crawler UA — the point of the test
        div = re.search(r'<div id="dimll-prerender"[^>]*>', html)
        assert div, (
            f"{path}: no prerender block for a generic client — the "
            "universal lane is gated, off, or suppressed by a stray marker "
            "string in a served template"
        )
        assert "hidden" not in div.group(0), (
            f"{path}: the prerender div carries `hidden` again — "
            "visibility-respecting consumers are back to reading "
            "'Loading...'; the dimll floor is >=2.6.1 for exactly this"
        )
        assert 'data-dimll-prerender="1">document.getElementById' in html, (
            f"{path}: the marked synchronous hide script is missing — "
            "JS browsers would flash the prose before React mounts"
        )
        assert "<main>" in html, f"{path}: prerender block carries no <main> prose"


def test_no_stray_prerender_marker_in_served_templates():
    """The substring-probe trap, pinned at the source.

    The test above catches the symptom on two routes. This catches the
    cause on every byte the app can serve, so a marker reintroduced into a
    comment, an asset, or a page that neither route above renders still
    fails the build. Kept separate because its failure message names the
    file, which the symptom test cannot.
    """
    import pathlib

    repo = pathlib.Path(__file__).resolve().parent.parent
    marker = "data-dimll" + "-prerender"  # split so THIS file is not a match
    offenders = []
    for directory in ("templates", "assets", "pages", "components", "lib"):
        for candidate in (repo / directory).rglob("*"):
            if not candidate.is_file():
                continue
            if candidate.suffix.lower() not in {".html", ".js", ".css", ".py", ".md"}:
                continue
            try:
                text = candidate.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):  # pragma: no cover - binary
                continue
            if marker in text:
                offenders.append(str(candidate.relative_to(repo)))

    assert not offenders, (
        "the prerender marker appears in served text, which trips "
        "dash-improve-my-llms' substring idempotency probe and disables "
        f"the universal prerender site-wide: {offenders}"
    )
