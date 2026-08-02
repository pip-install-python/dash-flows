"""Site identity: one brand, every surface, verbatim.

The network standard says a site states what it is in the same words
everywhere an agent or a reader can reach. The failure this pins is silent,
which is why it needs tests rather than a code review: nothing errors when a
surface falls back to a default.

What was live on flows.2plot.dev until this pass: the page-title prefix was a
bare "dash-flows" with no stated tagline anywhere, and the README's H1 read
**"Dash Flows"** — a display name that names nothing a reader can act on.
There is no package called "Dash Flows" on PyPI and no repository by that
name on GitHub. The brand an agent publishes has to be the string that finds
the thing.

dash-improve-my-llms 2.3.4's `resolve_site_title` is what makes the fix
possible: it takes the home page's registered `name` first, `app.title`
second, and *skips* generic candidates ("Home", "Index", "Dash") rather than
publishing them. These tests assert both ends of that — the inputs this repo
controls, and the H1 it produces.
"""

from __future__ import annotations

import re

from conftest import REPO_ROOT
from lib.constants import (
    PAGE_TITLE_PREFIX,
    SITE_BRAND,
    SITE_DESCRIPTION,
    SITE_SHORT_NAME,
)

# Spelled out rather than imported, so that renaming the constant cannot
# silently rename the site. Changing the brand should require changing this
# line, deliberately.
EXPECTED_BRAND = "dash-flows — React Flow node graphs for Dash"


def test_brand_constant_is_the_agreed_identity():
    assert SITE_BRAND == EXPECTED_BRAND


def test_app_title_is_the_brand(app):
    """`Dash(title=...)` — the <title>, and `resolve_site_title`'s fallback."""
    assert app.title == EXPECTED_BRAND


def test_home_prose_opens_with_the_brand():
    """`pages/home.py`'s LLMS_DOC is what /llms.txt serves as the home body.

    dash-improve-my-llms discovers it by module attribute, so it is live
    despite nothing in this repo importing it. Unlike dash-email, the literal
    does not live in home.py — `LLMS_DOC` is loaded from `pages/home.md` via
    frontmatter — so the H1 to pin is that file's first line. Reading the file
    rather than importing the module keeps this test free of Dash's
    page-registry side effects.
    """
    source = (REPO_ROOT / "pages" / "home.md").read_text()
    first = source.strip().splitlines()[0]
    assert first == f"# {EXPECTED_BRAND}"


def test_llms_index_h1_is_the_brand(client):
    """The single most-read line of this site, and the one nobody looks at."""
    response = client.get("/llms.txt")
    assert response.ok
    assert response.text.splitlines()[0] == f"# {EXPECTED_BRAND}"


def test_llms_index_tagline_is_the_description(client):
    body = client.get("/llms.txt").text
    assert f"> {SITE_DESCRIPTION}" in body


def test_the_viewer_brand_chip_is_not_a_framework_default(client):
    """The chip that reads "Dash" on a pre-2.3.4 artifact.

    It is rendered from the same `resolve_site_title` call as the H1, so
    asserting the brand is present catches both a stale package and a
    regressed constant. The banner is templated markup, so the brand may
    arrive HTML-escaped — compare both spellings rather than failing for a
    reason that has nothing to do with identity.
    """
    import html as html_module

    from conftest import BROWSER_ACCEPT, SAMPLE_PAGE

    page = client.get(f"{SAMPLE_PAGE}/llms.txt", accept=BROWSER_ACCEPT).text
    assert html_module.escape(EXPECTED_BRAND) in page or EXPECTED_BRAND in page, (
        "the viewer banner does not name this site"
    )


def test_the_byline_is_in_the_description_not_the_brand():
    """Naming rules from the standard.

    The brand says what the site *is*; the byline says who made it. A brand of
    "Pip Install Python" would make every satellite in the network share one
    name.

    The PACKAGE name is deliberately allowed in the brand here, unlike the
    documentation boilerplate: for a component library the package IS what a
    reader came to find, which is why leaflet.2plot.dev ships
    "dash-leaflet2 — Leaflet 2 maps for Dash". Nobody installs a template; a
    lot of people install this.
    """
    assert "dash-flows" in SITE_DESCRIPTION
    assert "Pip Install Python" in SITE_DESCRIPTION
    assert "Pip Install Python" not in SITE_BRAND


def test_no_surface_falls_back_to_a_generic_title():
    """The values `resolve_site_title` is designed to skip.

    If the brand were ever set to one of these, the package would silently fall
    through to the next candidate and this repo would have no idea which string
    it was publishing.
    """
    from dash_improve_my_llms.handlers import _GENERIC_SITE_TITLES

    assert SITE_BRAND.strip().lower() not in _GENERIC_SITE_TITLES


def test_the_home_page_display_name_really_is_generic(app_module):
    """Why `register_page_metadata(path="/", name=SITE_BRAND)` is load-bearing.

    `pages/home.py` registers the page as "Home" — the nav label, which is
    correct there and is on `resolve_site_title`'s skip list. Without the
    separate metadata registration in run.py the identity would fall through to
    `app.title`, which happens to be right today and would silently stop being
    right the moment somebody set a marketing title on the Dash constructor.
    """
    import dash

    from dash_improve_my_llms.handlers import _GENERIC_SITE_TITLES

    home = next(e for e in dash.page_registry.values() if e["path"] == "/")
    assert home["name"].strip().lower() in _GENERIC_SITE_TITLES


def test_readme_agrees_with_the_brand():
    """A README that names the site differently is the next drift."""
    readme = (REPO_ROOT / "README.md").read_text()
    assert EXPECTED_BRAND in readme, "README.md does not state the site brand"


def test_llms_package_floor_is_the_network_standard():
    """Identity resolution lives in the package; the floor is what delivers it."""
    import dash_improve_my_llms as pkg

    parts = tuple(int(p) for p in pkg.__version__.split(".")[:3] if p.isdigit())
    assert parts >= (2, 3, 4), (
        f"dash-improve-my-llms {pkg.__version__} predates resolve_site_title; "
        "the viewer chip and the /llms.txt H1 would fall back to app.title"
    )


# ---------------------------------------------------------------------------
# The per-page title — a share-card surface, not just a browser tab
#
# Dash passes each page's `title` straight into `og:title` and `twitter:title`
# (dash/_pages.py `_page_meta_tags`). PAGE_TITLE_PREFIX therefore sets the
# headline of every unfurl this site produces. Nobody sees their own share
# cards, so only a test catches it.
# ---------------------------------------------------------------------------


def test_the_page_title_prefix_is_derived_from_the_short_name():
    assert PAGE_TITLE_PREFIX == f"{SITE_SHORT_NAME} | "


def test_the_short_name_cannot_drift_from_the_brand():
    """Two constants, one identity. Derived, so this should be automatic."""
    assert SITE_BRAND.startswith(SITE_SHORT_NAME)


def test_the_share_card_headline_names_this_site(client):
    """og:title and twitter:title, as a scraper reads them."""
    html = client.get("/").text
    for tag in ("og:title", "twitter:title"):
        found = re.findall(
            rf'<meta[^>]*property="{tag}"[^>]*content="([^"]*)"', html
        )
        assert found, f"no {tag} on the home page"
        for value in found:
            assert SITE_SHORT_NAME in value, f"{tag}={value!r} does not name this site"


def test_no_surface_still_carries_the_old_display_name():
    """A sweep, because a "Dash Flows" display name is one paste away.

    This site never published a "Dash Flows"-style name from its constants —
    the drift risk here is the README's old H1 leaking back into the files
    that PUBLISH an identity. Comments and docstrings are stripped first:
    a file below may legitimately document the old value while explaining
    the fix.

    Scope is the files that PUBLISH an identity. `setup.py` and the package
    metadata are out, because the library's PyPI description is a different
    thing from the site's name. `README.md` is out too: it is the surface the
    identity pass rewrites, and the one string it must carry — the brand —
    has a test of its own above. `pages/home.md`'s H1 likewise has its own
    test.
    """
    offenders = []
    for path in ("lib/constants.py", "templates/index.html",
                 "scripts/network_smoke.py"):
        text = (REPO_ROOT / path).read_text()
        if path.endswith(".py"):
            text = re.sub(r'"""(?:.|\n)*?"""', "", text)
            text = re.sub(r"#.*", "", text)
        text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
        if "Dash Flows" in text:
            offenders.append(path)
    assert offenders == [], f"the old display name survives in {offenders}"
