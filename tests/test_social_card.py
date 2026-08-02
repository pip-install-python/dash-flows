"""The social card — the surface that fails silently and fails OUTSIDE the app.

NETWORK FILE: adapted from dash-documentation-boilerplate 1.2.4 via
email.2plot.dev. It changes only where this site legitimately differs: this
repo ships NO installable-app surface — no `assets/favicon/site.webmanifest`,
no apple-touch-icon set, only `assets/favicon.ico` — so the boilerplate's
manifest section has no counterpart here. If that surface is ever added, port
the manifest tests back from dash-email alongside it.

What is tested fails silently, which is why it needs tests rather than a look
at the page — nobody sees their own unfurls.

The failure the boilerplate actually shipped, and this repo was one refactor
away from: **TWO empty og:image tags on every page.** No `register_page` call
passed `image_url=`, so Dash emitted `og:image=""` (dash/_pages.py) — and an
EMPTY tag unfurls worse than a missing one, because scrapers treat the empty
value as the declared image and render a blank card. It was doubled because
`templates/index.html` spelled the metas placeholder out inside an HTML
comment, and Dash substitutes placeholders by plain string replacement over
the whole template, comments included. The comment was invisible in a browser
and perfectly visible to anything reading the raw HTML.

Note where each tag comes from, because it decides which file to open when one
of these fails: `og:image`, `twitter:image` and the `twitter:*` set are DASH's
(per page, from `register_page`); `og:site_name`, `og:url` and the
`og:image:*` auxiliaries are `templates/index.html`'s.
dash-improve-my-llms adds a third set, but only on the prerender path, which
social scrapers do not take — its bot list has `facebookbot` (Meta's AI
training crawler), not `facebookexternalhit` (the link-preview fetcher). That
is why deleting the template would silently kill every unfurl.
"""

from __future__ import annotations

import re

from conftest import REPO_ROOT
from lib.constants import (
    OG_IMAGE_ALT,
    OG_IMAGE_HEIGHT,
    OG_IMAGE_TYPE,
    OG_IMAGE_URL,
    OG_IMAGE_WIDTH,
    SITE_BRAND,
)


def _visible(html: str) -> str:
    """The document with HTML comments removed.

    The template documents itself with commented-out example tags, and a regex
    cannot tell those from live ones.
    """
    return re.sub(r"<!--.*?-->", "", html, flags=re.S)


def _meta(html: str, value: str) -> list[str]:
    """Every `content` for a property/name — a list, so duplicates show up.

    Tags carrying `data-dimll-prerender` are excluded. dash-improve-my-llms
    injects its own description and OpenGraph block on the prerender path, and
    marks each one precisely so it can be told apart. Counting those here would
    make this test fail on a package behaviour nothing in this repo controls,
    and it would hide what the test is actually for: duplication between
    `templates/index.html` and the tags Dash generates from `register_page`.
    """
    pattern = (
        rf'<meta[^>]*(?:property|name)="{re.escape(value)}"[^>]*content="([^"]*)"'
        rf'|<meta[^>]*content="([^"]*)"[^>]*(?:property|name)="{re.escape(value)}"'
    )
    body = re.sub(r'<meta[^>]*data-dimll-prerender[^>]*>', "", _visible(html))
    return ["".join(m) for m in re.findall(pattern, body)]


# ------------------------------------------------------------- the og image --


def test_the_og_image_is_never_empty(client, page_paths):
    for path in page_paths[:8]:
        images = _meta(client.get(path).text, "og:image")
        assert images, f"{path} declares no og:image at all"
        assert all(src.strip() for src in images), (
            f"{path} serves an EMPTY og:image {images} — the card renders blank"
        )


def test_the_image_is_declared_exactly_once(client, page_paths):
    """The duplicate-tag regression, in both of the ways it happened upstream."""
    for path in page_paths[:8]:
        html = client.get(path).text
        assert len(_meta(html, "og:image")) == 1, (
            f"{path} has {_meta(html, 'og:image')} — a scraper picks one, and "
            "it will not be the one you meant"
        )
        assert len(_meta(html, "twitter:image")) == 1


def test_no_dash_placeholder_is_named_inside_a_comment():
    """The bug behind the doubled tags, pinned at its source.

    Dash resolves `{%…%}` by plain string replacement over the whole template.
    A placeholder named in a comment is therefore not documentation — it is a
    second, hidden copy of whatever that placeholder emits. The metas one is
    what put two empty og:image tags on every page of the boilerplate.
    """
    template = (REPO_ROOT / "templates" / "index.html").read_text()
    for comment in re.findall(r"<!--.*?-->", template, flags=re.S):
        found = re.findall(r"\{%\s*\w+\s*%\}", comment)
        assert not found, (
            f"a comment in templates/index.html names {found} — Dash will "
            "substitute it there and emit the block twice"
        )


def test_the_image_is_not_an_svg(client):
    """SVG is rejected by Facebook, Twitter/X, LinkedIn and Slack alike.

    Dash's asset inference reaches `logo.<ext>`, so this is one missing
    `image_url=` and one added `assets/logo.svg` away from happening.
    """
    for prop in ("og:image", "twitter:image"):
        for src in _meta(client.get("/").text, prop):
            assert not src.lower().endswith(".svg"), f"{prop} is an SVG: {src}"


def test_the_image_is_absolute_and_matches_the_constant(client):
    for prop in ("og:image", "twitter:image"):
        values = _meta(client.get("/").text, prop)
        assert values, f"no {prop} on the home page"
        for src in values:
            assert src.startswith("http"), f"{prop}={src!r} is not absolute"
            assert src == OG_IMAGE_URL


def test_the_image_is_hosted_off_the_app():
    """The card must be on the CDN, not served by this app.

    Not a style rule. A card the app serves is fetched by the scraper at unfurl
    time; on a cold free-tier container that request lands mid-wake and times
    out, the preview renders blank ONCE, and the platform caches the miss — so
    the first person to share the link poisons it for everyone.

    That the URL RESOLVES is deliberately not checked here. It is off-host now,
    and reaching a third party would make this suite depend on Cloudflare being
    up (the same reason conftest disables the geo lookup).
    `scripts/network_smoke.py` and `scripts/smoke_live.py` fetch the real file
    after every deploy and read its IHDR chunk — which also catches the CDN
    object being replaced with something a different shape, something no
    offline test can see.
    """
    assert OG_IMAGE_URL.startswith("https://cdn.2plot.ai/github_assets/"), (
        f"{OG_IMAGE_URL} is not on the network CDN"
    )
    assert "/assets/" not in OG_IMAGE_URL, "the app is serving its own card again"


def test_the_card_url_names_this_domain():
    """One card per host. A satellite pointing at another's card is a real
    mistake and an easy one — the CDN path is a hand-typed filename."""
    assert OG_IMAGE_URL.endswith("/flows.2plot.dev.png")


def test_the_auxiliary_image_tags_match_the_constants(client):
    """index.html hard-codes the dimensions; lib/constants.py is the source.

    A declared width/height that disagrees with the file is worse than
    declaring none — the platform reserves the wrong box and crops.
    """
    html = client.get("/").text
    assert _meta(html, "og:image:width") == [str(OG_IMAGE_WIDTH)]
    assert _meta(html, "og:image:height") == [str(OG_IMAGE_HEIGHT)]
    assert _meta(html, "og:image:alt") == [OG_IMAGE_ALT]
    assert _meta(html, "og:image:type") == [OG_IMAGE_TYPE]
    assert _meta(html, "og:image:secure_url") == [OG_IMAGE_URL], (
        "secure_url must be the same file as og:image, not a stale copy"
    )


def test_the_declared_ratio_suits_a_large_image_card():
    """`summary_large_image` wants roughly 1.91:1."""
    ratio = OG_IMAGE_WIDTH / OG_IMAGE_HEIGHT
    assert 1.7 <= ratio <= 2.05, f"{OG_IMAGE_WIDTH}x{OG_IMAGE_HEIGHT} is {ratio:.2f}:1"


def test_the_rendered_card_on_disk_is_the_declared_shape():
    """If `scripts/make_social_card.py` has been run, its output must agree.

    The build directory is gitignored, so this skips on a fresh checkout — it
    is here for the machine that generated the card and is about to upload it,
    which is the moment the dimensions can still be fixed cheaply.
    """
    import pytest

    card = REPO_ROOT / "build" / "social-cards" / "flows.2plot.dev.png"
    if not card.exists():
        pytest.skip("no rendered card in build/social-cards (gitignored)")

    raw = card.read_bytes()
    assert raw[1:4] == b"PNG"
    assert int.from_bytes(raw[16:20], "big") == OG_IMAGE_WIDTH
    assert int.from_bytes(raw[20:24], "big") == OG_IMAGE_HEIGHT


def test_the_twitter_card_is_a_large_image(client):
    assert _meta(client.get("/").text, "twitter:card") == ["summary_large_image"]


def test_no_meta_tag_dash_emits_is_also_declared_statically(client):
    """The rule the OG and Twitter blocks in index.html are built on.

    Dash emits all of these per page. A static copy in the template makes two
    of each, and the static one describes the SITE where Dash's describes the
    PAGE — so the duplicate is both redundant and the less accurate of the two.
    """
    html = client.get("/").text
    for tag in ("description", "og:type", "og:title", "og:description",
                "og:image", "twitter:card", "twitter:url", "twitter:title",
                "twitter:description", "twitter:image"):
        found = _meta(html, tag)
        assert len(found) <= 1, f"{tag} is declared {len(found)} times: {found}"


def test_the_tags_dash_omits_are_declared_here(client):
    """The other half of the rule — do not delete these thinking Dash covers them."""
    html = client.get("/").text
    for tag in ("og:site_name", "og:url", "og:image:alt", "twitter:image:alt",
                "og:image:secure_url", "og:image:type",
                "og:image:width", "og:image:height"):
        assert _meta(html, tag), f"{tag} is missing and Dash does not emit it"


def test_og_site_name_is_the_brand(client):
    assert _meta(client.get("/").text, "og:site_name") == [SITE_BRAND]


# ------------------------------------------------------------- the template --


def test_every_asset_the_template_references_resolves(client):
    """The half-landed-commit guard.

    The boilerplate shipped a template pointing at `/assets/favicon/…` while
    the icon set sat UNTRACKED in git. The deploy builds from git, so
    production 404'd the manifest, the apple-touch-icon and every PNG icon —
    the whole installable-app surface — while every local boot looked perfect
    because the files were on disk. `git status` was the only place it showed.

    This repo has fewer icon assets, but the failure mode is identical for
    every `/assets/` URL the rendered document carries.
    """
    html = _visible(client.get("/").text)
    referenced = sorted(set(re.findall(r'(?:href|content|src)="(/assets/[^"]+)"', html)))
    assert referenced, "no /assets/ references found — did the template change?"

    missing = [ref for ref in referenced if not client.get(ref).ok]
    assert missing == [], (
        f"templates/index.html references assets that do not resolve: {missing}. "
        "If they exist on disk, they are untracked — the deploy builds from git."
    )


def test_the_index_template_is_still_wired_in(app_module):
    """`templates/index.html` looks removable and is not.

    dash-improve-my-llms appears to cover OG, but its injection runs only on
    the prerender path, which social scrapers do not take. Deleting the
    template kills every unfurl at once.
    """
    index = (REPO_ROOT / "templates" / "index.html").read_text()
    for placeholder in ("{%metas%}", "{%favicon%}", "{%css%}", "{%app_entry%}",
                        "{%config%}", "{%scripts%}", "{%renderer%}"):
        assert placeholder in index, f"{placeholder} missing from the template"
    assert app_module.app.index_string.startswith("<!DOCTYPE html>")


def test_the_template_takes_its_origin_from_the_constants(app_module):
    """No second copy of the canonical origin.

    The template is a static file and cannot import lib/constants, so run.py
    substitutes the token at startup. If a hand-typed origin ever appears in
    the template, half the site can end up advertising one hostname and half
    another — and nothing looks broken.
    """
    from lib.constants import DOCS_BASE_URL, ORIGIN_PLACEHOLDER

    raw = (REPO_ROOT / "templates" / "index.html").read_text()
    assert ORIGIN_PLACEHOLDER in raw, "the template no longer uses the token"
    assert ORIGIN_PLACEHOLDER not in app_module.app.index_string, (
        "run.py did not substitute the origin token"
    )
    assert DOCS_BASE_URL in app_module.app.index_string
