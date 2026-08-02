import os

# ---------------------------------------------------------------------------
# Site identity — one string, every surface
# ---------------------------------------------------------------------------
# The network standard (2plot.ai, 2plot.dev, boilerplate.2plot.dev,
# leaflet.2plot.dev, email.2plot.dev): a site states what it is, in the same
# words, on every surface an agent or a reader can reach. The surfaces this
# brand has to reach, and what serves each:
#
#   Dash(title=SITE_BRAND)              -> <title>, and the fallback identity
#   register_page_metadata(path="/",    -> the /llms.txt H1 and the llms
#       name=SITE_BRAND)                   viewer's brand chip, both via
#                                          dash-improve-my-llms 2.3.4's
#                                          `resolve_site_title`
#   pages/home.py's LLMS_DOC H1         -> the home page's own prose
#
# tests/test_site_identity.py pins all of them to this constant, because the
# failure is silent: `resolve_site_title` SKIPS generic candidates ("Home",
# "Index", Dash's default "Dash") rather than publishing them, so a site that
# never states its identity falls through to whatever is left and nothing
# looks broken.
#
# Naming rules, from the network standard:
#   - "Pip Install Python" is the byline (who made it), never the site name;
#   - the package name leads, because for a component library the package IS
#     what a reader came to find. Same shape as leaflet.2plot.dev
#     ("dash-leaflet2 — Leaflet 2 maps for Dash") and email.2plot.dev
#     ("dash-email — email components for Dash").
SITE_BRAND = "dash-flows — React Flow node graphs for Dash"

SITE_DESCRIPTION = (
    "dash-flows — React Flow (@xyflow/react 12) node-graph components for "
    "Plotly Dash: interactive flow diagrams with a glass-morphism theme, ELK "
    "layouts, custom node/edge types, undo/redo, sub-flows and full Dash "
    "callback integration. By Pip Install Python."
)

# The brand without its tagline. SITE_BRAND is right for a page that has room
# for it; this is for the places that prefix something else and would
# otherwise run past every platform's truncation point.
SITE_SHORT_NAME = "dash-flows"

# Prefixed to every per-page title (`pages/markdown.py`, `pages/home.py`), and
# therefore NOT only a browser-tab string: Dash passes the page title straight
# into `og:title` and `twitter:title` (dash/_pages.py `_page_meta_tags`), so
# this is the headline on every share card the site produces. Derived rather
# than retyped so the two cannot drift apart.
PAGE_TITLE_PREFIX = f"{SITE_SHORT_NAME} | "

PRIMARY_COLOR = "blue"

# Keep in step with package.json and dash_flows/package-info.json when cutting
# a release.
APP_VERSION = "1.3.0"

GITHUB_URL = "https://github.com/pip-install-python/dash-flows"

# ---------------------------------------------------------------------------
# Public origin
# ---------------------------------------------------------------------------
# The single source of truth for every absolute URL this app emits:
# sitemap.xml, robots.txt, the llms.txt links, and the per-page
# <link rel="canonical">. templates/index.html does NOT restate it — run.py
# substitutes it into the template's __CANONICAL_ORIGIN__ token at startup, so
# there is nothing to drift.
#
# TWO env names, on purpose. `APP_BASE_URL` is the network-wide name every
# other satellite reads (the boilerplate, leaflet, email, the hub), and it
# wins; `DASH_FLOWS_BASE_URL` is this repo's original name and is still
# honoured because render.yaml has been offering it since the first deploy.
# Renaming it in one place and not the other is how a host quietly starts
# advertising the wrong canonical origin.
#
# Leaving both unset in production is correct: the default is the canonical
# public origin, which is what consolidates link equity onto one hostname
# instead of splitting it with *.onrender.com.
DEFAULT_BASE_URL = "https://flows.2plot.dev"
DOCS_BASE_URL = (
    os.environ.get("APP_BASE_URL")
    or os.environ.get("DASH_FLOWS_BASE_URL")
    or DEFAULT_BASE_URL
).rstrip("/")

# Kept as an alias because the network's shared files (scripts/, tests/)
# import `BASE_URL` by that name on every host. One value, two spellings, no
# second source of truth.
BASE_URL = DOCS_BASE_URL

# Token in templates/index.html that run.py swaps for DOCS_BASE_URL at
# startup. The template is a static file, so it cannot read this module; the
# substitution is what keeps one origin rather than two that can disagree.
ORIGIN_PLACEHOLDER = "__CANONICAL_ORIGIN__"

# ---------------------------------------------------------------------------
# The social card
# ---------------------------------------------------------------------------
# Dash builds `og:image` and `twitter:image` for every page from
# `register_page(image_url=...)`, and emits `content=""` when it finds neither
# an explicit URL nor an inferable asset (dash/_pages.py). An empty og:image
# unfurls WORSE than having no tag at all, because scrapers treat the empty
# value as the declared image and render a blank card.
#
# THE CARD LIVES ON THE CDN, NOT IN assets/. Network rule, about cold starts:
# a card served by the app is fetched by the scraper at unfurl time, and on a
# cold free-tier container that request lands mid-wake and times out. The
# preview renders blank ONCE and the platform caches the miss. The CDN has no
# cold start.
#
# Rendered by `scripts/make_social_card.py` (1200x630 = 1.91:1, the Open
# Graph ideal) and uploaded BY HAND to the Cloudflare bucket — there is no
# automated path to that bucket, and og:image must not point here until the
# upload is verified (200 + IHDR 1200x630, read as bytes).
#
# The width and height MUST match the file. `tests/test_social_card.py` pins
# these against templates/index.html, and `scripts/smoke_live.py` fetches the
# real file after every deploy and reads its IHDR chunk.
OG_IMAGE_URL = "https://cdn.2plot.ai/github_assets/flows.2plot.dev.png"
OG_IMAGE_WIDTH = 1200
OG_IMAGE_HEIGHT = 630
OG_IMAGE_TYPE = "image/png"
OG_IMAGE_ALT = SITE_BRAND

# ---------------------------------------------------------------------------
# The network's internal-traffic contract
# ---------------------------------------------------------------------------
# The analytics point of truth is https://2plot.ai/docs/satellite-analytics
# ("Internal traffic"): any request whose User-Agent contains
# INTERNAL_UA_TOKEN is 2plot network machinery talking to itself — the hub's
# hourly health sweep, CI smoke batteries, this app's own server-to-server
# calls to the hub. It is counted NOWHERE.
#
# Two halves, and both are required for the contract to hold:
#
#   inbound  — every tracker drops a token-carrying request at WRITE time,
#              before device detection and before bot classification, so it
#              never reaches the ledger the hourly rollup is built from;
#   outbound — every call this host makes to another network host sends
#              INTERNAL_UA, so the far side can apply the same rule.
#
# The token string must stay byte-identical across the network; it mirrors
# 2plotai/lib/constants.py, pip-docs+/lib/constants.py, the boilerplate's,
# leaflet's and email's.
INTERNAL_UA_TOKEN = "2plot-internal"
INTERNAL_UA = "2plot-internal/1.0 (+https://2plot.ai/docs/satellite-analytics)"


def internal_ua(caller: str = "") -> str:
    """``INTERNAL_UA`` with a caller suffix, e.g. ``"ad-client"``.

    The suffix is for reading logs on the far side; only the token matters to
    the contract, and it stays intact whatever the suffix says.
    """
    caller = (caller or "").strip()
    return f"{INTERNAL_UA} {caller}" if caller else INTERNAL_UA


def require_owned_base_url(base_url: str = DOCS_BASE_URL) -> None:
    """Fail fast in production when the base URL isn't this app's real origin.

    Only enforced when a hosting platform is detected (Render sets ``RENDER``;
    ``APP_ENV=production`` works anywhere else), so local development and the
    test suite are unaffected.

    ``DEFAULT_BASE_URL`` here is this app's own origin, so inheriting it is
    correct. What is still caught is the failure that actually bites — a
    platform-generated hostname. ``*.onrender.com`` keeps resolving after a
    custom domain is attached, so canonicals pointing there split link equity
    across two hosts for as long as nobody notices.
    """
    in_production = bool(
        os.environ.get("RENDER") or os.environ.get("APP_ENV") == "production"
    )
    if not in_production:
        return

    for platform_host in ("onrender.com", "herokuapp.com", "railway.app", "fly.dev"):
        if platform_host in base_url:
            raise RuntimeError(
                f"base URL {base_url!r} is a platform-generated hostname. "
                "Canonical tags, sitemap.xml and llms.txt would all point at "
                "it instead of the custom domain, splitting link equity "
                "across two hosts. Set APP_BASE_URL to the public domain."
            )


# Populated by pages/markdown.py when loading documentation files.
# Maps page name -> raw markdown content (used by the llms_copy directive).
NAME_CONTENT_MAP = {}

# Mantine style-prop shorthands excluded from the `.. kwargs::` prop tables.
PROPS_TO_EXCLUDE = [
    "unstyled",
    "m",
    "my",
    "mx",
    "mt",
    "mb",
    "ms",
    "me",
    "ml",
    "mr",
    "p",
    "py",
    "px",
    "pt",
    "pb",
    "ps",
    "pe",
    "pl",
    "pr",
    "bg",
    "c",
    "opacity",
    "ff",
    "fz",
    "fw",
    "lts",
    "ta",
    "lh",
    "fs",
    "tt",
    "td",
    "w",
    "miw",
    "maw",
    "h",
    "mih",
    "mah",
    "bgsz",
    "bgp",
    "bgr",
    "bga",
    "pos",
    "top",
    "left",
    "bottom",
    "right",
    "inset",
    "display",
    "flex",
]
