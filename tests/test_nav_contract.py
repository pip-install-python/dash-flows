"""The navigation contract (sync item 16) — uniform where it must be, free
where it may.

Owner's brief of 2026-08-30 (DESIGN-navigation-uniformity): the sidebar's
sections come from frontmatter against CATEGORY_ORDER; the network is ONE
registry rendered as the top bar's Other Apps menu; Resources is one
constant; Admin is owner-only and absent from the tree otherwise; every
icon-only control has a name; no `dcc.*` where DMC has the component. Each
pin here is one line of that brief.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
ALLOWED_DCC = {"Location", "Store", "Interval", "Upload", "Graph"}


def _calls(src: str, name: str):
    """Yield the source text of every `name(` call, parens balanced."""
    for m in re.finditer(re.escape(name) + r"\(", src):
        depth, i = 0, m.start()
        while i < len(src):
            if src[i] == "(":
                depth += 1
            elif src[i] == ")":
                depth -= 1
                if depth == 0:
                    yield src[m.start():i + 1]
                    break
            i += 1


# ------------------------------------------------------------- a11y --


@pytest.mark.parametrize("control", ["dmc.Burger", "dmc.ActionIcon"])
def test_every_icon_only_control_in_components_has_a_name(control):
    """Requirement 9: the audits named the unlabelled Burger and copy
    button. Every Burger/ActionIcon in components/ carries aria-label."""
    unlabelled = []
    for path in sorted((REPO / "components").glob("*.py")):
        for call in _calls(path.read_text(), control):
            if "aria-label" not in call:
                unlabelled.append(f"{path.name}: {call[:60]}…")
    assert unlabelled == [], unlabelled


def test_code_highlight_copy_button_has_a_name():
    src = (REPO / "lib" / "directives" / "source.py").read_text()
    assert "copyLabel=" in src and "copiedLabel=" in src


def test_no_dcc_where_dmc_has_the_component():
    """Requirement 10, fleet-wide: `dcc.` only for Location, Store,
    Interval, Upload, Graph (no DMC equivalent)."""
    offenders = []
    for folder in ("pages", "components"):
        for path in sorted((REPO / folder).glob("*.py")):
            code = "\n".join(line for line in path.read_text().splitlines()
                             if not line.lstrip().startswith("#"))
            for m in re.finditer(r"\bdcc\.([A-Za-z]+)", code):
                if m.group(1) not in ALLOWED_DCC:
                    offenders.append(f"{folder}/{path.name}: dcc.{m.group(1)}")
    assert offenders == [], offenders


def test_the_traffic_page_uses_a_date_picker_not_a_dropdown():
    src = (REPO / "pages" / "traffic.py").read_text()
    assert "dcc.Dropdown" not in src
    assert "dmc.DatePickerInput" in src and 'valueFormat="YYYY-MM-DD"' in src
    assert "presets=" in src and "minDate=" in src and "maxDate=" in src


# --------------------------------------------------------- registry --


def test_other_apps_menu_is_the_registrys_primary_set(app_module):
    """Requirement 4 + the owner's review (2026-08-30): the PRIMARY
    applications only — never the docs subdomains — from the registry,
    no duplicates, self omitted, short labels (the domain)."""
    from components.header import create_other_apps_menu
    from lib.constants import DOCS_BASE_URL
    from lib.network_directory import AFFILIATED, PEERS, PRIMARY, other_apps_for

    menu = create_other_apps_menu()
    items = menu.children[1].children
    hrefs = [i.href for i in items]
    expected = [e["url"] for e in other_apps_for(DOCS_BASE_URL)]
    assert hrefs == expected
    assert set(h.rstrip("/") for h in hrefs) == PRIMARY - {DOCS_BASE_URL.rstrip("/")}
    assert {"https://2plot.ai", "https://2plot.dev", "https://2plot.media",
            "https://piratesbargain.com", "https://ai-agent.buzz"} == set(PRIMARY)
    assert PRIMARY <= {e["url"].rstrip("/") for e in PEERS + AFFILIATED}, "PRIMARY names a URL the registry lacks"
    assert not any(".2plot.dev" in h for h in hrefs), "a docs subdomain leaked into the menu"
    assert len(set(hrefs)) == len(hrefs), "a host is listed twice"
    for item in items:
        label = item.children
        assert "." in label and " " not in label and "—" not in label, label
        assert item.target == "_blank"


def test_resources_are_third_party_only():
    """Owner's review (2026-08-30): the sidebar's Resources holds dmc and
    the upstream project only; the owner's own links are top bar + footer."""
    from lib import constants
    from lib.constants import DISCORD_URL, GITHUB_PROFILE_URL, GITHUB_URL, YOUTUBE_URL, resources

    items = resources()
    assert items[0]["label"] == "dmc" and items[0]["url"] == "https://www.dash-mantine-components.com/"
    urls = [r["url"] for r in items]
    # The OWNER's links are banned; an upstream project on GitHub is not.
    for banned in (GITHUB_URL, GITHUB_PROFILE_URL, DISCORD_URL, YOUTUBE_URL,
                   "pip-install-python", "discord.gg", "youtube.com",
                   "community.plotly.com", "https://2plot.dev"):
        assert not any(banned in u for u in urls), banned
    if constants.UPSTREAM:
        assert urls[-1] == constants.UPSTREAM["url"]


def test_github_icon_and_same_as_share_one_constant(app_module):
    from components.header import create_header
    from lib.constants import GITHUB_URL, SAME_AS

    assert GITHUB_URL in SAME_AS
    assert GITHUB_URL.startswith("https://github.com/pip-install-python/")
    assert GITHUB_URL.count("/") == 4, "the REPOSITORY, not the profile"
    assert GITHUB_URL in str(create_header([]))


# ---------------------------------------------------------- sidebar --


def test_sections_follow_category_order_and_never_hold_admin(app_module):
    import dash

    from components.navbar import sections_for
    from lib.constants import CATEGORY_ORDER

    data = list(dash.page_registry.values())
    sections = sections_for(data)
    titles = [t for t, _ in sections]
    known = [t for t in titles if t in CATEGORY_ORDER]
    assert known == [c for c in CATEGORY_ORDER if c in titles], titles
    for _, entries in sections:
        assert not any(e["path"].startswith("/admin/") for e in entries)
        assert not any(e["path"] in ("/", "/changelog", "/api") for e in entries)
    # this fork's own docs all declare a category
    assert "Documentation" not in titles, "a docs page lost its category: frontmatter"


def test_frontmatter_order_sorts_within_a_section(app_module):
    import dash

    from components.navbar import sections_for

    for title, entries in sections_for(dash.page_registry.values()):
        orders = [int(e.get("order") or 1000) for e in entries]
        assert orders == sorted(orders), (title, orders)


def test_anonymous_tree_has_no_admin_href(app_module, monkeypatch):
    """Requirement 7: hidden, not blocked. The startup tree carries only an
    empty Admin placeholder; the callback returns nothing to a non-admin."""
    import dash

    from components.navbar import create_content, render_admin_section

    tree = str(create_content(dash.page_registry.values()))
    assert "/admin/" not in tree
    assert "navbar-admin-desktop" in tree
    monkeypatch.delenv("ALLOW_UNGATED_ADMIN", raising=False)
    assert render_admin_section("navbar-admin-desktop") == (None, None)


def test_admin_tree_lists_every_admin_page(app_module, monkeypatch):
    from components.navbar import render_admin_section

    monkeypatch.setenv("ALLOW_UNGATED_ADMIN", "1")
    desktop, mobile = render_admin_section("navbar-admin-desktop")
    text = str(desktop)
    assert "/admin/control-board" in text and "/admin/traffic" in text
    assert str(mobile) == text


def test_search_lists_only_sidebar_pages(app_module):
    import dash

    from components.navbar import search_data

    values = [d["value"] for d in search_data(dash.page_registry.values())]
    assert values and not any(v.startswith("/admin/") for v in values)
    assert "/" not in values and "/changelog" not in values


# ---------------------------------------------------------- footer --


def test_footer_is_the_contract(app_module):
    from datetime import datetime

    from components.footer import create_footer
    from lib.constants import DISCORD_URL, GITHUB_PROFILE_URL, GITHUB_URL, YOUTUBE_SUBSCRIBE_URL

    text = str(create_footer())
    assert f"© {datetime.now().year} Pip Install Python LLC" in text
    for href in (GITHUB_PROFILE_URL, DISCORD_URL, YOUTUBE_SUBSCRIBE_URL):
        assert href in text
    assert GITHUB_URL not in text, "the repo link is the top bar's; the footer links the profile"
    assert "/changelog" not in text, "the sidebar's single Changelog link is the one"
    assert "/terms" not in text and "/privacy" not in text


# ------------------------------------------------------- changelog --


def test_changelog_page_is_the_file(app_module, client):
    from pages.changelog import parse_changelog

    versions = parse_changelog()
    newest = re.search(r"^## \[([^\]]+)\]", (REPO / "CHANGELOG.md").read_text(), re.M).group(1)
    assert versions and versions[0]["version"] == newest
    doc = client.get("/changelog/llms.txt", user_agent="Mozilla/5.0 (compatible; Googlebot/2.1)")
    assert doc.status == 200
    assert doc.text.startswith("# Changelog") and "\n# Changelog" not in doc.text, "the file's H1 was not deduplicated"
    assert f"## [{newest}]" in doc.text
    page = client.get("/changelog", user_agent="Mozilla/5.0 (compatible; Googlebot/2.1)")
    assert page.status == 200 and newest in page.text


# ------------------------------------------------------------- api --


def test_api_reference_reads_a_dash_package_metadata():
    from lib import api_reference

    comps = api_reference.load_package("tests.fixtures.fake_dash_pkg")
    names = [c["name"] for c in comps]
    assert names == ["FakeGauge", "FakeWidget"], "sorted, exported only"
    widget = comps[1]
    props = {p["name"]: p for p in widget["props"]}
    assert "setProps" not in props
    assert props["value"]["required"] and props["value"]["default"] == "0"
    assert props["variant"]["type"].startswith("one of ")
    assert widget["props"][0]["name"] == "id"
    md = api_reference.as_markdown(["tests.fixtures.fake_dash_pkg"])
    assert "| `value` * | number | 0 | Current value. |" in md


def test_api_page_renders_one_table_per_component():
    from pages.api import build_page

    text = str(build_page(["tests.fixtures.fake_dash_pkg"]))
    assert "api-table-FakeWidget" in text and "api-table-FakeGauge" in text
    assert "Current value." in text


def test_api_page_follows_api_packages(app_module):
    """A host that declares API_PACKAGES has /api registered, in the
    sidebar, with components read from the package's metadata."""
    import dash

    from components.navbar import _has_api_page
    from lib import api_reference
    from lib.constants import API_PACKAGES

    paths = [p["path"] for p in dash.page_registry.values()]
    assert API_PACKAGES == ["dash_flows"]
    assert "/api" in paths
    assert _has_api_page(dash.page_registry.values())
    for pkg in api_reference.load_packages(API_PACKAGES):
        assert not pkg.get("error"), pkg
        assert pkg["components"], f"{pkg['package']} exposes no components"


def test_missing_package_is_reported_not_raised():
    from lib import api_reference

    out = api_reference.load_packages(["no_such_dash_package_xyz"])
    assert out[0]["components"] == [] and "error" in out[0]


# ------------------------------------------------- the markdown api-half --
#
# docs/api_reference/api_reference.md is this fork's OWN, hand-curated API
# doc — a `.. kwargs::` directive per component, distinct from the generated
# /api page above. THE DEFECT (sync item 18 contract highlight 7-amended,
# muicharts' finding 2026-08-30): a markdown2dash directive renders Dash
# COMPONENTS, so its table exists only in the browser's React tree. The
# machine lane (/<page>/llms.txt, the crawler document) and the non-JS
# prerender are all built from the markdown SOURCE, where the directive
# line is stripped — so /api-reference served real tables to a browser and
# ZERO property rows anywhere else. pages/markdown.py now expands
# `.. kwargs::` the same fence-aware way it already expanded `.. source::`,
# through lib.directives.kwargs.props_markdown — ONE parse
# (lib.directives.kwargs.props_for) for both the directive's own table and
# the expansion, so the two lanes cannot drift apart again.


def test_the_api_reference_doc_has_real_prop_rows(app_module):
    """Rows, not just headings — a table with headers and no body is
    exactly what the defect looked like from the browser side."""
    import dash

    entry = next(p for p in dash.page_registry.values() if p["path"] == "/api-reference")
    layout = entry["layout"]
    tree = str(layout() if callable(layout) else layout)
    assert tree.count("m2d-block-kwargs") == 5, "one table per `.. kwargs::` directive"
    assert tree.count("TableTr") > 20, "the tables have no body rows"
    assert "The ID used to identify this component in Dash callbacks." in tree


def test_the_api_reference_props_reach_the_machine_lane_too(app_module, client):
    """THE DEFECT, pinned directly. Measured before this fix: /api-reference
    /llms.txt carried zero markdown table rows and the non-JS prerender
    carried zero `<table>`, while a real browser saw five populated tables."""
    import re

    from conftest import BROWSER_UA, CRAWLER_UA

    llms = client.get("/api-reference/llms.txt", user_agent=CRAWLER_UA)
    assert llms.status == 200
    rows = [ln for ln in llms.text.split("\n")
            if ln.startswith("| ") and set(ln) - set("| -")]
    assert len(rows) > 100, f"only {len(rows)} markdown table rows in /api-reference/llms.txt"
    assert "| Name | Type | Description |" in rows
    assert any("The ID used to identify this component in Dash callbacks." in r
               for r in rows)
    # the raw directive must not survive into the prose either
    assert ".. kwargs::" not in llms.text

    crawler = client.get("/api-reference", user_agent=CRAWLER_UA)
    assert crawler.text.count("<table") >= 5, "the crawler document has no tables"

    prerender = re.search(r'<div id="dimll-prerender".*?</div>\s*(?=<script|</body)',
                          client.get("/api-reference", user_agent=BROWSER_UA).text, re.S)
    assert prerender and prerender.group(0).count("<table") >= 5, (
        "the non-JS prerender has no tables — a text reader still gets nothing"
    )


def test_the_api_reference_two_lanes_report_the_same_number_of_rows(app_module, client):
    """One parse, two renderings. If these ever disagree, someone has grown
    a second props implementation — the state that produced the defect."""
    import dash

    from conftest import CRAWLER_UA

    entry = next(p for p in dash.page_registry.values() if p["path"] == "/api-reference")
    layout = entry["layout"]
    browser_rows = str(layout() if callable(layout) else layout).count("TableTr")

    llms = client.get("/api-reference/llms.txt", user_agent=CRAWLER_UA).text
    machine_rows = len([ln for ln in llms.split("\n")
                        if ln.startswith("| ") and set(ln) - set("| -")])

    assert browser_rows == machine_rows, (
        f"browser lane {browser_rows} rows, machine lane {machine_rows} — "
        "the lanes have drifted apart again"
    )


def test_every_kwargs_directive_in_the_docs_resolves():
    """A `.. kwargs::` naming a component that cannot be read renders as
    NOTHING in the browser (markdown2dash's render returns None on empty
    data) and as an HTML comment in the prose — silence either way, so the
    emptiness has to be caught here."""
    import re
    from pathlib import Path

    from lib.directives.kwargs import props_for

    repo = Path(__file__).resolve().parent.parent
    specs = []
    for md in sorted((repo / "docs").glob("**/*.md")):
        specs += re.findall(r"^\.\. kwargs::(.+?)$", md.read_text(), re.M)
    assert specs, "no .. kwargs:: directives found — this pin would be vacuous"
    empty = sorted({s.strip() for s in specs if not props_for(s.strip())})
    assert empty == [], f"kwargs directives that resolve to no props: {empty}"


def test_disabling_the_kwargs_expansion_turns_the_machine_pin_red(monkeypatch):
    """MUTATION CHECK: the predecessor test asserted component NAMES, which
    are true even with zero rows (they come from the page's own headings) —
    that is exactly how the defect shipped unnoticed. Prove the new pin
    would have caught it: with props_markdown disabled (the shape the
    defect actually had — the directive line stripped, nothing put back),
    the row count collapses to zero."""
    from lib.directives import kwargs as kwargs_mod
    from pages.markdown import _expand_source_directives

    monkeypatch.setattr(kwargs_mod, "props_markdown", lambda spec, library=None: "")
    content = (Path(__file__).resolve().parent.parent / "docs" / "api_reference"
               / "api_reference.md").read_text().split("---", 2)[-1]
    expanded_disabled = _expand_source_directives(content)
    rows = [ln for ln in expanded_disabled.split("\n")
            if ln.startswith("| ") and set(ln) - set("| -")]
    assert rows == [], "the mutation should have produced zero table rows"


# ---------------------------------------------------------- visual pass --


def test_the_aside_collapses_on_pages_without_a_toc(app_module):
    """Owner's note 1: /changelog full width. Docs pages with `.. toc::`
    keep the column; everything else collapses it."""
    from lib.aside import ASIDE_PATHS, aside_config, has_aside

    # Derived from the registry, not named: any fork has SOME docs page
    # with a `.. toc::`, and its own paths.
    toc_pages = sorted(ASIDE_PATHS)
    assert toc_pages, "no docs page registered an aside — is `.. toc::` gone?"
    assert all(has_aside(p) for p in toc_pages)
    # Only pages the CONTRACT owns and that render no TOC are asserted
    # collapsed; a fork may serve / or /api as a docs page with its own
    # toc, so those are not named here.
    for path in ("/changelog", "/admin/traffic", "/admin/control-board"):
        assert not has_aside(path), path
        assert aside_config(path)["collapsed"]["desktop"] is True
    assert aside_config(toc_pages[0])["collapsed"]["desktop"] is False
    assert aside_config(None)["collapsed"]["mobile"] is True


def test_the_mobile_drawer_is_always_mounted(app_module):
    """Owner's note 2: the burger must not depend on a mount-on-open
    transition, and #navbar-admin-mobile must exist on every load."""
    from components.navbar import create_navbar_drawer

    drawer = create_navbar_drawer([])
    assert drawer.keepMounted is True
    assert "navbar-admin-mobile" in str(drawer)


def test_code_blocks_cannot_widen_the_page():
    """Owner's note 3: the overflow rule lives in the stylesheet, for every
    container a code block can sit in — never a per-page fix."""
    css = (REPO / "assets" / "main.css").read_text()
    for selector in (".mantine-List-itemWrapper", ".mantine-List-itemLabel",
                     ".mantine-Timeline-itemBody", ".mantine-CodeHighlight-root",
                     ".mantine-CodeHighlightTabs-root", ".mantine-AppShell-main pre",
                     "table.m2d-block-kwargs", "code.m2d-codespan"):
        assert selector in css, selector
    # and the changelog's rows let an unbreakable code token wrap
    src = (REPO / "pages" / "changelog.py").read_text()
    assert '"overflowWrap": "anywhere"' in src and '"minWidth": 0' in src
    wrappers = css[css.index(".mantine-List-itemWrapper"):]
    assert "min-width: 0" in wrappers[:400]
    pre_rule = css[css.index(".mantine-AppShell-main pre"):]
    assert "overflow-x: auto" in pre_rule[:200]
    assert "overflow-wrap: anywhere" in css[css.index("code.m2d-codespan"):][:200]


def test_other_apps_dropdown_is_solid_and_every_primary_app_has_an_icon(app_module):
    """Seat's note 4."""
    from components.header import create_other_apps_menu
    from lib.network_directory import ICONS, PRIMARY

    dropdown = create_other_apps_menu().children[1]
    assert dropdown.styles["dropdown"]["backgroundColor"]
    for url in PRIMARY:
        assert ICONS.get(url) not in (None, "mdi:web"), f"{url} has no icon"


def test_the_skip_link_is_the_first_tab_stop(app_module):
    """Adopted from muischeduler: "Skip to content" → #main-content, first
    in the tree, visible only on focus (.skip-link in main.css)."""
    from components.appshell import create_appshell

    shell = create_appshell([])
    first = shell.children[0]
    assert getattr(first, "href", None) == "#main-content" and first.className == "skip-link"
    assert 'id="main-content"' in str(shell).replace("'", '"') or "main-content" in str(shell)
    css = (REPO / "assets" / "main.css").read_text()
    assert ".skip-link:focus" in css and "left: -9999px" in css


def test_an_upstream_on_github_is_allowed_in_resources(monkeypatch):
    from lib import constants

    monkeypatch.setattr(constants, "UPSTREAM", {"name": "React Flow", "url": "https://github.com/xyflow/xyflow"})
    urls = [r["url"] for r in constants.resources()]
    assert urls[-1] == "https://github.com/xyflow/xyflow"
    assert not any("pip-install-python" in u for u in urls)


def test_changelog_headings_accept_every_dash(tmp_path):
    from pages.changelog import newest_date, parse_changelog

    p = tmp_path / "CHANGELOG.md"
    p.write_text("# Changelog\n\n## [2.0.0] — 2026-08-30\n\n### Added\n- em dash\n\n"
                 "## [1.9.0] – 2026-08-29\n\n### Fixed\n- en dash\n\n## [1.8.0] - 2026-08-28\n\n### Added\n- hyphen\n")
    versions = parse_changelog(p)
    assert [v["date"] for v in versions] == ["2026-08-30", "2026-08-29", "2026-08-28"]
    assert newest_date(p) == "2026-08-30"


def test_locked_pages_are_marked_in_the_sidebar(app_module, monkeypatch):
    """excalidraw's finding: an auth-tier page shows a lock and a Tooltip
    ("Sign in required") — never `title=`, which DMC 2.8 rejects."""
    import dash_mantine_components as dmc

    from components import navbar
    from lib import page_tiers

    monkeypatch.setattr(navbar, "page_tier", lambda p: "auth" if p == "/locked" else "public")
    locked = navbar._page_link({"path": "/locked", "name": "Locked", "icon": None})
    assert isinstance(locked, dmc.Tooltip) and locked.label == "Sign in required"
    assert "fluent:lock-closed-16-regular" in str(locked)
    public = navbar._page_link({"path": "/open", "name": "Open", "icon": None})
    assert isinstance(public, dmc.Anchor)
    assert page_tiers.local_tier("/getting-started") in ("public", "auth", "admin", "hidden")


def test_api_reference_falls_back_to_the_committed_extract_then_docstrings(tmp_path, monkeypatch):
    """metadata.json → api_metadata.json (committed, stamped) →
    docstrings (hook-based packages ship no metadata at all)."""
    import sys

    from lib import api_reference

    # docstring-only package (modelviewer's shape)
    comps = api_reference.load_package("tests.fixtures.docstring_dash_pkg")
    assert [c["name"] for c in comps] == ["DocWidget"]
    props = {p["name"]: p for p in comps[0]["props"]}
    assert props["value"]["required"] and props["size"]["default"] == "'md'"
    assert props["id"]["description"].startswith("The ID")
    assert "setProps" not in props
    # slim extract wins over docstrings and carries the generated stamp
    pkg_dir = tmp_path / "slim_pkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("class Only:\n    pass\n")
    (pkg_dir / api_reference.SLIM_METADATA).write_text(json.dumps({"generated": "2026-08-30", "components": [
        {"name": "Only", "description": "d", "props": [{"name": "id", "type": "string", "required": False, "default": "", "description": "x"}]}]}))
    monkeypatch.syspath_prepend(str(tmp_path))
    sys.modules.pop("slim_pkg", None)
    assert api_reference.load_package("slim_pkg")[0]["name"] == "Only"
    assert api_reference.slim_generated_on("slim_pkg") == "2026-08-30"
    assert api_reference.slim_generated_on("tests.fixtures.fake_dash_pkg") is None


def test_api_markdown_escapes_pipes_in_every_cell():
    from lib import api_reference

    rows = [{"package": "x", "components": [{"name": "C", "description": "", "props": [
        {"name": "a|b", "type": "a | b", "required": False, "default": "x|y", "description": "d|e\nf"}]}]}]
    import unittest.mock as um
    with um.patch.object(api_reference, "load_packages", return_value=rows):
        md = api_reference.as_markdown(["x"])
    assert "| `a\\|b` | a \\| b | x\\|y | d\\|e f |" in md


def test_generated_pages_carry_the_full_machine_record(app_module, client):
    """/changelog (and /api when declared) register the full record —
    visibility, tier, lastmod — not just a module LLMS_DOC."""
    import re as _re

    from lib import page_tiers, page_visibility
    from pages.changelog import newest_date

    assert page_tiers.local_tier("/changelog") == "public"
    assert "/changelog" in page_visibility.controllable_pages()
    sitemap = client.get("/sitemap.xml").text
    m = _re.search(r"<url>\s*<loc>[^<]*/changelog</loc>\s*<lastmod>([^<]+)</lastmod>", sitemap)
    assert m and m.group(1).startswith(newest_date()), sitemap[:400]


def test_nav_short_label_is_used_in_sidebar_and_search():
    """emojimart, muicharts: frontmatter `nav:` is the sidebar and search
    label; `name:` stays the <title> / og:title / llms.txt heading."""
    from components.navbar import _page_link, search_data

    entry = {"path": "/very-long", "name": "A Very Long Page Name Indeed", "nav": "Long page", "icon": None}
    assert "Long page" in str(_page_link(entry)) and "Indeed" not in str(_page_link(entry))
    assert search_data([entry]) == [{"label": "Long page", "value": "/very-long"}]
    plain = {"path": "/p", "name": "Plain", "icon": None}
    assert search_data([plain]) == [{"label": "Plain", "value": "/p"}]


def test_changelog_parser_takes_prose_first_and_bare_versions(tmp_path):
    """pannellum's finding: `## 2.0.0 — date` with paragraphs and no ###
    sections rendered eight empty headings. Bare or bracketed version,
    any dash, prose as `para` items."""
    from pages.changelog import parse_changelog

    p = tmp_path / "CHANGELOG.md"
    p.write_text("# Changelog\n\n## 2.0.0 — 2026-08-02\n\nFirst paragraph of prose\nthat wraps.\n\nSecond paragraph.\n\n"
                 "## [1.0.0] - 2026-01-01\n\n### Added\n- a bullet\n")
    v = parse_changelog(p)
    assert [x["version"] for x in v] == ["2.0.0", "1.0.0"]
    assert v[0]["date"] == "2026-08-02"
    paras = [i["text"] for i in v[0]["sections"]["Notes"] if i["type"] == "para"]
    assert paras == ["First paragraph of prose that wraps.", "Second paragraph."]
    assert v[1]["sections"]["Added"][0] == {"type": "item", "text": "a bullet"}


def test_generated_api_yields_to_a_docs_page_that_owns_the_path(tmp_path, monkeypatch):
    from pages import api as api_page

    docs = tmp_path / "docs" / "x"
    docs.mkdir(parents=True)
    (docs / "api.md").write_text("---\nname: API\nendpoint: /api\n---\n\nprose\n")
    monkeypatch.chdir(tmp_path)
    assert api_page._docs_page_owns("/api") is True
    assert api_page._docs_page_owns("/nope") is False


def test_header_reads_header_height_and_props_tables_scroll(app_module):
    from components.header import create_header
    from lib.constants import HEADER_HEIGHT

    src = (REPO / "components" / "header.py").read_text()
    assert "h=HEADER_HEIGHT" in src and "h=70" not in src
    assert f"h={HEADER_HEIGHT}" in str(create_header([]))
    css = (REPO / "assets" / "main.css").read_text()
    assert ".m2d-block-props table" in css


FLEET_HEADINGS = [
    ("## [1.4.0] - 2026-08-03", "1.4.0", "v1.4.0", "2026-08-03", ""),
    ("## [1.0.0] — 2026-08-21", "1.0.0", "v1.0.0", "2026-08-21", ""),
    ("## [0.9.0] – 2026-08-20", "0.9.0", "v0.9.0", "2026-08-20", ""),
    ("## 2.0.0 — 2026-08-02", "2.0.0", "v2.0.0", "2026-08-02", ""),
    ("## [0.2.0] — 2026-07-31 (never published)", "0.2.0", "v0.2.0", "2026-07-31", "never published"),
    ("## [0.1.0] — unreleased", "0.1.0", "v0.1.0", "", "unreleased"),
    ("## [2026-08-30] — the round in one line", "2026-08-30", "2026-08-30", "2026-08-30", "the round in one line"),
    ("## [Unreleased]", "Unreleased", "Unreleased", "", ""),
]


def test_every_fleet_heading_shape_parses(tmp_path):
    """The seven heading shapes measured on the fleet's main branches, plus
    Unreleased — label, badge, date and note each land."""
    import re as _re

    from pages.changelog import _is_version, parse_changelog

    body = "# Changelog\n\n" + "\n\n".join(h + "\n\n- a bullet" for h, *_ in FLEET_HEADINGS)
    p = tmp_path / "CHANGELOG.md"
    p.write_text(body)
    versions = parse_changelog(p)
    assert len(versions) == len(FLEET_HEADINGS)
    for got, (_, label, badge, date, note) in zip(versions, FLEET_HEADINGS):
        assert got["version"] == label, got
        assert got["date"] == date, got
        assert got["note"] == note, got
        rendered_badge = f"v{got['version']}" if _is_version(got["version"]) else got["version"]
        assert rendered_badge == badge, got
        assert not _re.match(r"^v(Unreleased|\d{4}-)", rendered_badge), "VUNRELEASED / v<date>"


def test_bold_spans_containing_inline_code_render(tmp_path):
    r"""`**A \`/changelog\` page.** rest` rendered raw asterisks when code
    split before bold."""
    from dash import html

    from pages.changelog import _inline

    parts = _inline("**A `/changelog` page.** This file is the source.")
    strong = parts[0]
    assert isinstance(strong, html.Strong)
    inner = str(strong.children)
    assert "/changelog" in inner and "**" not in str(parts)
    assert any("This file is the source." in str(x) for x in parts[1:])


def test_battery_hidden_paths_match_the_registry(app_module):
    """The battery's literal tuple is pinned against the registry, so a
    page added, renamed or deleted moves it in the same change."""
    import dash

    from scripts.network_smoke import HIDDEN_DOC_PATHS

    admin = {p["path"] for p in dash.page_registry.values() if p["path"].startswith("/admin/")}
    assert set(HIDDEN_DOC_PATHS) == {f"{p}/llms.txt" for p in admin}, (
        "network_smoke.HIDDEN_DOC_PATHS drifted from the registered admin pages"
    )


def test_every_test_client_user_names_headers():
    """A bare test client sends `Werkzeug/x.y` — crawler lane at dimll ≥
    2.8 — so a mark_hidden page 404s and an every-page-200 loop goes red
    at the floor bump. Any file that drives `.test_client()` must pass
    headers (a named UA)."""
    offenders = []
    for folder in ("tests", "scripts"):
        for path in sorted((REPO / folder).glob("*.py")):
            src = path.read_text()
            names_ua = "headers=" in src or "HTTP_USER_AGENT" in src
            if ".test_client()" in src and not names_ua:
                offenders.append(f"{folder}/{path.name}")
    assert offenders == [], offenders
