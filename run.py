"""
dash-flows documentation site — flows.2plot.dev.

A markdown-driven documentation app (2plot network standard, seeded from the
Dash Documentation Boilerplate). Documentation lives in ``docs/<topic>/<topic>.md``
and is auto-discovered by ``pages/markdown.py``. Each page renders prose plus
live component demos (``.. exec::``), syntax-highlighted source
(``.. source::``), and auto-generated prop tables (``.. kwargs::``).

Run:
    pip install -r requirements-docs.txt
    pip install --no-deps markdown2dash==0.1.2
    python run.py
Then open http://localhost:8560

Backend (Dash 4.1+): set DASH_BACKEND=flask|fastapi|quart (default flask).

ORDER MATTERS IN THIS FILE. The registration sequence below is the network
standard's, proven on the boilerplate/leaflet/email, and the two rules that
bite when broken are:

  1. the visitor-tracking hook (Flask/Quart) registers BEFORE
     add_llms_routes — the package's bot middleware short-circuits crawler
     requests, and a hook added after it never sees exactly the bot traffic
     a docs site most wants counted;
  2. native routes (/healthz, /api/pageview) register BEFORE add_llms_routes
     on FastAPI, or the package's catch-all /<page>/llms.txt matcher shadows
     them. FastAPI's tracking middleware is the mirror image and goes AFTER
     (Starlette runs the last-added middleware outermost).
"""
import os
import platform

import dash
from dash import Dash
from dotenv import load_dotenv

# MUST come before the first-party imports below, and this is not style.
# Several modules read os.environ at *import* time — lib/constants.py
# (APP_BASE_URL / DASH_FLOWS_BASE_URL), lib/ad_client.py (AD_SERVER_URL,
# AD_APP_ID) and lib/analytics_tracker.py (TRAFFIC_ANALYTICS_FILE). Loading
# the .env after importing them means every one of those silently falls back
# to its default no matter what the file says.
load_dotenv()

# THE FORK POINT — claim this app's network identity before any hub-facing
# module imports. Every module that names this app (satellite_reporter,
# ad_client, hub_client, bulletin) carries its own fallback default, and
# after a template sync those defaults DISAGREE: lib/satellite_reporter.py
# is kept BYTE-IDENTICAL to the boilerplate's (shasum is the acceptance
# check for the whole fleet), so its own fallback says "boilerplate" while
# this fork's other modules say "flows". An unset SATELLITE_APP_KEY would
# then file this site's traffic under the TEMPLATE's hub row — found live
# on pannellum 2026-08-21, and this repo has its own contamination in the
# hub's history from the same class.
#
# setdefault, not assignment: a real env value (Render dashboard, .env
# loaded immediately above) always wins; this line only closes the unset
# gap. FORKS CHANGE THIS ONE STRING — and repairing the reporter's
# fallback instead would break the byte-identity the fleet checks.
#
# Supersedes the retired SATELLITE_APP_ID mechanism: that name is dead
# network-wide, and any lingering SATELLITE_APP_ID in a service's env is
# read by nothing.
os.environ.setdefault("SATELLITE_APP_KEY", "flows")

from lib import bulletin, network_directory  # noqa: E402
from lib.analytics_tracker import tracker  # noqa: E402
from lib.backend import resolve_backend, get_backend_info  # noqa: E402
from lib.constants import (  # noqa: E402
    APP_VERSION,
    DOCS_BASE_URL,
    OG_IMAGE_ALT,
    OG_IMAGE_HEIGHT,
    OG_IMAGE_URL,
    OG_IMAGE_WIDTH,
    ORIGIN_PLACEHOLDER,
    PUBLISHER,
    SAME_AS,
    SITE_BRAND,
    SITE_DESCRIPTION,
    require_owned_base_url,
)
from lib.pageview_beacon import (  # noqa: E402
    register_pageview_beacon,
    register_pageview_route,
)

from dash_improve_my_llms import (  # noqa: E402
    add_llms_routes,
    configure_seo,
    LLMSConfig,
    on_document_read,
    RobotsConfig,
    register_page_metadata,
)

# dash-improve-my-llms floor. Below it this site's published surfaces are
# wrong in ways nothing about the running app looks wrong, so it refuses to
# boot rather than serve them — override with ALLOW_STALE_DEPS=1 for local
# archaeology only.
#
#   2.3.4  resolve_site_title (the /llms.txt H1 + viewer brand chip);
#          2.3.3 had fixed the crawler taxonomy in robots.txt.
#   2.5.1  configure_seo: icons, social card, publisher/sameAs.
#   2.6.0  configure_access — the enforcement half lib/access.py wires, so
#          the prerender obeys a page's tier rather than publishing gated
#          prose to crawlers.
#   2.6.1  the prerender guarantee: the block is served VISIBLE (<= 2.6.0
#          shipped it `hidden`, so visibility-respecting extractors read
#          the whole site as "Loading..."), hidden again by a synchronous
#          script only JS browsers run.
#   2.7.0  dedup + hardening of that block: the injected prerender H1 no
#          longer doubles the doc body's own markdown H1 (every page was a
#          duplicate-H1 page to crawlers), the home footer stops doubling
#          its /llms.txt link, and the idempotency probe no longer trips on
#          a page that merely MENTIONS the marker — the trap that silently
#          disabled this host's prerender from an index.html comment. Also
#          ships the geo guardrail seam _health_body() reports.
#   2.7.1  the round-3 network floor: llms.txt v2 discovery relations
#          (rel=alternate/describedby on both lanes + Link headers), the
#          Accept: text/plain ramp, and the representation content digest.
#   2.8.0  the ledger floor (2026-08-29): ONE classifier — `classify()` is
#          the registry robots.txt is rendered from, and
#          lib/analytics_tracker delegates to it instead of carrying a
#          fourth UA list that filed ClaudeBot as search; the READ EVENT —
#          `on_document_read` hands the app one row per corpus document
#          served (tier, verdict, bytes, verified vendor), which the
#          tracker keeps as the ledger's `reads` table; and verified vendor
#          identity (`verified` is `n/a` where the operator publishes no
#          ranges — Anthropic does not). 2.8.1 will write the resolved
#          `policy` on every event; until then it is None and the rollup
#          groups it as "default". Nothing here waits on it.
#
# THIS NUMBER LIVES IN FIVE PLACES — requirements-docs.txt, here,
# ci.yml (the host check and the in-image check) and tests/test_config.py.
# Grep the number, not the file. The requirements-docs.txt line is also the
# Docker cache bust; a floor that moves only here rebuilds nothing.
LLMS_PKG_FLOOR = (2, 8, 0)
try:
    from importlib.metadata import version as _pkg_version

    _llms_version = tuple(
        int(p) for p in _pkg_version("dash-improve-my-llms").split(".")[:3]
    )
except Exception:  # pragma: no cover — metadata missing on editable installs
    _llms_version = LLMS_PKG_FLOOR
if _llms_version < LLMS_PKG_FLOOR and os.environ.get("ALLOW_STALE_DEPS") != "1":
    raise RuntimeError(
        f"dash-improve-my-llms {'.'.join(map(str, _llms_version))} is below "
        f"the network floor {'.'.join(map(str, LLMS_PKG_FLOOR))}. "
        "Below 2.8.0 there is no `classify()` and no `on_document_read`: the "
        "tracker cannot delegate bot classification and no read row is ever "
        "kept, so the ledger's `reads` table and rollup v4's vendors[] are "
        "empty (ImportError at boot, not a silent degrade). "
        "Below 2.7.1 the llms.txt v2 discovery relations (rel=alternate/"
        "describedby + Link headers), the text/plain Accept ramp and the "
        "representation digest are missing. Below 2.7.0 every page serves a "
        "DUPLICATE H1 to crawlers, the home footer doubles its /llms.txt "
        "link, and a page that merely mentions the prerender marker loses "
        "its prerender entirely. Below 2.6.1 the prerender ships `hidden`, "
        "so every visibility-respecting reader gets 'Loading...' instead of "
        "the page's prose. "
        "pip install -U 'dash-improve-my-llms[flask]>=2.8.0' "
        "(or set ALLOW_STALE_DEPS=1 to boot anyway)."
    )

BACKEND = resolve_backend()
BACKEND_INFO = get_backend_info(BACKEND)

print(f"[dash-flows docs] Dash {dash.__version__} · backend='{BACKEND}'")

# Refuses to boot in production if the canonical origin is a platform-generated
# hostname. `*.onrender.com` keeps resolving after the custom domain is
# attached, so a base URL pointing there splits link equity across two hosts
# and nothing about the running site looks wrong.
require_owned_base_url()

# The template's __CANONICAL_ORIGIN__ tokens become DOCS_BASE_URL here, so the
# canonical origin and the client-side og:url resync (components/appshell.py)
# both come from lib/constants.py. A static file cannot import that module,
# and two hand-maintained copies of an origin is exactly how half a site ends
# up pointing at one hostname and half at another.
_index_string = open(os.path.join("templates", "index.html")).read().replace(
    ORIGIN_PLACEHOLDER, DOCS_BASE_URL
)

# ----------------------------------------------------------------------------
# Clerk satellite auth, HALF ONE OF TWO. MUST run BEFORE Dash(...) —
# register_clerk_auth installs @dash.hooks callbacks that fire during app
# construction, so calling it afterwards silently does nothing. Fully
# optional: a no-op with no CLERK_* keys, which is the default and the
# posture this site ships in.
#
# The other half is `_auth.configure_app(app)` immediately after Dash(...).
# SHIPPING ONE WITHOUT THE OTHER MAKES THE SITE LIE: the components render
# and ClerkJS reports signed-in while every server render reads signed-out,
# so a gated page serves its owner a sign-in card forever, /api/auth/*
# answers 405 through Dash's GET-only page catch-all, and sign-out never
# revokes. Invisible to every local suite, because Clerk is off in test
# environments and configure_app no-ops without keys — which is why
# tests/test_auth_wiring.py pins BOTH calls by AST instead.
# ----------------------------------------------------------------------------
from lib import auth as _auth  # noqa: E402

CLERK_ENABLED = _auth.register()

_dash_kwargs = dict(
    use_pages=True,
    suppress_callback_exceptions=True,
    update_title=None,
    index_string=_index_string,
    # `resolve_site_title`'s second candidate (dimll 2.3.4), and the fallback
    # <title> for paths outside the page registry — so it carries SITE_BRAND
    # verbatim rather than a prose sentence: one string, every surface.
    # tests/test_site_identity.py pins it.
    title=SITE_BRAND,
)

# Dash 4.1+ accepts backend=; older Dash does not — degrade gracefully.
try:
    app = Dash(__name__, backend=BACKEND, **_dash_kwargs)
except TypeError:
    app = Dash(__name__, **_dash_kwargs)

# Clerk satellite auth, HALF TWO OF TWO — see the block above Dash(...) for
# why shipping only the first half makes the site lie. dash-clerk-auth splits
# its setup either side of the constructor: sessions, the /api/auth/* routes
# and per-request identity are wired here. No-op when Clerk is off.
_auth.configure_app(app)

# ----------------------------------------------------------------------------
# Trust the proxy's forwarded scheme. Immediately after the server object
# exists and before anything can serve a request.
#
# Dash builds `twitter:url` from `request.url` for every page, and behind
# Cloudflare -> Render the last hop is plain HTTP, so production advertised
# `http://flows.2plot.dev/` to every social scraper while `og:url` (which
# templates/index.html hard-codes) looked correct — measured live on this
# host 2026-08-22, before this pass. Scrapers do not run JavaScript, so the
# client-side canonical sync in the template cannot reach this. See
# lib/proxy.py for why gunicorn's own forwarded-header handling does not
# cover it, and for the trust boundary.
# ----------------------------------------------------------------------------
from lib import proxy as _proxy  # noqa: E402

PROXY_FIX_APPLIED = _proxy.apply(app, BACKEND)
print(
    "[dash-flows docs] forwarded-scheme trust: "
    + ("on" if PROXY_FIX_APPLIED else "OFF — request.url will report the "
       "scheme of the last proxy hop, and social cards will advertise it")
)

# Expose backend info so UI components can render a badge without re-reading env.
app._backend_info = BACKEND_INFO
app._base_url = DOCS_BASE_URL

# Cross-host directory: <link rel="related"> tags, a `## Network` section in
# /llms.txt, and followed links in the prerendered body. Must run before
# add_llms_routes so the routes are built with it in place.
network_directory.apply(DOCS_BASE_URL)

# DEFAULT ALLOW (sync item 15, owner decision 2026-08-29): the wall used to
# decide by vendor CLASS what nobody could account for. Since sync item 12
# every corpus read is a ledger row this app keeps and the hub can
# reconcile against the wire, so a training-crawler read is now recorded
# and priceable rather than blocked outright — the tool becomes per-vendor
# policy (`vendor_policy={"<key>": "block" | "meter"}`) for one vendor
# whose rows justify it, never the whole class. `allow_ai_search` /
# `allow_traditional` are unchanged; robots.txt now carries no Disallow
# stanza for GPTBot/ClaudeBot/CCBot/… at all (they fall under
# `User-agent: *` / Allow), and the package's bot middleware stops 403ing
# the browser document and /healthz for them. See DIVERGENCES.md's
# `ai_bots` posture for the measured wire numbers.
app._robots_config = RobotsConfig(
    block_ai_training=False,
    allow_ai_search=True,
    allow_traditional=True,
    crawl_delay=10,
    disallowed_paths=[],
)

# `name` here is NOT a nav label — dash.register_page in pages/home.py owns
# that, and it says "Home". This is what dimll 2.3.4's `resolve_site_title`
# reads first, so it is the /llms.txt H1 and the llms viewer's brand chip: the
# two surfaces an agent uses to learn what this site is. `resolve_site_title`
# SKIPS generic candidates ("Home", "Index", "Dash"), so passing the page's
# display name here would silently fall through to `app.title`.
register_page_metadata(
    path="/",
    name=SITE_BRAND,
    description=SITE_DESCRIPTION,
)

# ============================================================================
# Site identity for the CRAWLER document (dash-improve-my-llms >= 2.5.0).
#
# The crawler document carried this site's content signals and NONE of its
# identity: measured here 2026-08-22, browsers got seven icon links, an
# og:image and a Twitter card from templates/index.html while Googlebot got
# publisher: no, sameAs: no, logo: no. One declaration covers every crawler
# surface, and it also claims /favicon.ico (Google's fallback), which was
# answering 404 on this host. Content may differ between the crawler
# document and the browser document; identity may not.
#
# The icons list is SET-EQUAL to what 2.6's autodiscovery already finds in
# assets/favicon/ — verified against the crawler head, and pinned by
# tests/test_seo_icons.py. That agreement is the point: the explicit list is
# authoritative today, and stays correct rather than fighting discovery.
#
# NO root assets/favicon.ico is added, deliberately. dimll answers
# /favicon.ico with a 302 to the real file (verified), so the fallback is
# covered — while a second, unreferenced copy at the root is precisely the
# root-icon trap: two byte-identical files that stay identical until one is
# regenerated and the other silently is not.
# ============================================================================
configure_seo(
    icons=[
        # Same paths templates/index.html links, so the two heads agree.
        "/assets/favicon/favicon.ico",
        {"href": "/assets/favicon/favicon-32x32.png", "sizes": "32x32"},
        {"href": "/assets/favicon/favicon-16x16.png", "sizes": "16x16"},
        {"href": "/assets/favicon/favicon-96x96.png", "sizes": "96x96"},
        {"href": "/assets/favicon/android-chrome-192x192.png", "sizes": "192x192"},
        {"href": "/assets/favicon/android-chrome-512x512.png", "sizes": "512x512"},
        {"href": "/assets/favicon/apple-touch-icon.png",
         "rel": "apple-touch-icon", "sizes": "180x180"},
    ],
    social_image=OG_IMAGE_URL,
    social_image_alt=OG_IMAGE_ALT,
    social_image_width=OG_IMAGE_WIDTH,
    social_image_height=OG_IMAGE_HEIGHT,
    publisher=PUBLISHER,
    same_as=SAME_AS,
)

# ============================================================================
# Native routes + visitor tracking — see the ORDER MATTERS note up top.
# ============================================================================


def _resolved_country(headers=None) -> str:
    """``geo.explain_resolution`` over THIS request's headers, or a reason.

    Reads the request headers directly rather than anything the package
    threads through, so it answers "did the country header reach this app at
    all?" independently of how the enforcement seam is wired.

    Each backend below hands its OWN framework's headers in. The template's
    first cut read Flask's request context unconditionally, which made the
    FastAPI and Quart lanes answer "no request context" forever — pannellum's
    production /healthz is where that showed (2026-08-23). This site deploys
    flask, so it would never have been bitten; the explicit hand-through is
    ported anyway because DASH_BACKEND is a supported env var here and a
    diagnostic that only works on the default backend is the kind of thing
    nobody discovers until they need it. ``normalize_headers`` accepts
    Flask/Starlette/Quart/dict and never raises; the Flask-context fallback
    stays for callers that pass nothing.
    """
    try:
        from dash_improve_my_llms import geo
        from dash_improve_my_llms._headers import normalize_headers
    except Exception:
        return "unavailable (pre-2.7.0 package)"

    try:
        if headers is not None:
            return geo.explain_resolution(normalize_headers(headers))

        from flask import has_request_context, request

        if not has_request_context():
            return "no request context"
        return geo.explain_resolution(normalize_headers(request.headers))
    except Exception:
        return "unavailable"


def _health_body(headers=None) -> dict:
    """Built PER REQUEST, never snapshotted at registration.

    Every field here used to be static for a running process, which made a
    snapshot look harmless — and `geo` is the field that stops being static:
    this route is registered well before the access/geo configuration below
    runs, so a value captured at registration would report the guardrail
    unconfigured on a host where it IS configured. That is the diagnostic
    lying in exactly the situation it exists for.
    """
    from lib.satellite_reporter import app_key

    body = {
        "ok": True,  # the network battery asserts this exact field
        "app": app_key(),
        "version": APP_VERSION,
        # BOTH spellings, deliberately (sync item 10). The fleet key set is
        # {app, backend, build, dash_version, geo, ok, python} and every
        # reader — the hub's hourly sweep, the F4 battery, cd.yml's
        # build-match wait, scripts/network_smoke.py — reads it BY KEY NAME.
        # This host shipped `dash` alone for months and read as MISSING
        # `dash_version` to all of them, which is the failure mode the item
        # exists for: a renamed key is invisible to every check that reads
        # the value rather than the key. The remedy is ADDITIVE — an extra
        # costs the fleet nothing, a substitute costs it a red cell — so
        # `dash` stays for anything of this fork's own that reads it.
        "dash": dash.__version__,
        "dash_version": dash.__version__,
        # Which of the three lib/backend.py lanes is actually serving.
        # Declared in render.yaml and the Dockerfile as `flask`; this is the
        # surface that can contradict either if a deploy ever disagrees.
        "backend": BACKEND,
        "reporting": bool(os.environ.get("CROSS_APP_WEBHOOK_SECRET")),
        # WHICH interpreter is actually serving. Three declared Pythons can
        # coexist for months without a single surface able to contradict any
        # of them — the template carried a patch-pinned 3.11.8 image, a 3.12
        # CI matrix and a 3.12.0 render.yaml simultaneously (ops-seat finding,
        # 2026-08-25). Here the Dockerfile's FROM tag is the ONE declaration
        # (this service is `runtime: docker`, so no PYTHON_VERSION lane
        # exists — see DIVERGENCES.md), and scripts/network_smoke.py's
        # python_matches_declared holds this field against it.
        "python": platform.python_version(),
    }
    # Which commit the RUNNING instance was built from — what lets CD verify
    # the artifact it just shipped rather than whichever build happens to be
    # answering. A disk-backed Render service restarts with a blip instead of
    # overlapping instances, so a bare 200 proves nothing about WHICH build
    # replied: the old build always passed the old battery, and the bug only
    # surfaced when a run added a new surface (the muicharts finding,
    # 2026-08-21 — its battery had been verifying the previous release on
    # every run, invisibly). ADDITIVE and optional: omitted where the platform
    # variable does not exist, so the fleet's probe contract is unchanged and
    # the battery's existing field assertions keep passing.
    build = os.environ.get("RENDER_GIT_COMMIT")
    if build:
        body["build"] = build

    # The geo guardrail's LIVE state (dash-improve-my-llms >= 2.7.0). Added
    # after a production verification elsewhere on the network could not
    # answer "is the denylist actually in force?" from outside: the only
    # surfaces that could settle it (the boot log, the operator panel) need
    # credentials a verification pass does not have.
    #
    # COUNTS AND FLAGS ONLY — never the denylist's country codes. A health
    # endpoint is not where anyone should learn policy. `resolved` reveals
    # only the caller's own country back to them, which Cloudflare's
    # /cdn-cgi/trace already does, and it is the one check that localises a
    # failure: geo can be fully configured and still never match if the
    # country header is not reaching the app. "configured: true, denied: 7,
    # resolved: unknown" says that in one line.
    try:
        from dash_improve_my_llms import geo
    except ImportError:
        # Pre-2.7 package: the key is OMITTED, not error-flagged. A host on
        # an older floor is not broken, it predates the diagnostic — and its
        # absence in production is precisely how this site can tell that a
        # floor bump did NOT reach the image (the Docker cache trap).
        pass
    else:
        try:
            body["geo"] = {
                "configured": bool(geo.is_configured()),
                "denied": len(geo.effective_policy().get("deny_countries") or []),
                "resolved": _resolved_country(headers),
            }
        except Exception:  # never let a diagnostic break the health probe
            body["geo"] = {"configured": False, "denied": 0, "error": True}

    return body


register_pageview_route(app, BACKEND)

if BACKEND == "fastapi":
    from starlette.requests import Request as _StarletteRequest
    from starlette.responses import JSONResponse

    @app.server.get("/healthz", include_in_schema=False)
    async def healthz(request: _StarletteRequest):  # pragma: no cover — flask deploys
        # The request's headers go WITH the payload: geo's `resolved` reads
        # the country header from THIS request, and _health_body's
        # Flask-context fallback can never see a Starlette one.
        return JSONResponse(_health_body(headers=request.headers))

elif BACKEND == "quart":
    from quart import jsonify as _quart_jsonify
    from quart import request as _quart_request

    @app.server.get("/healthz")
    async def healthz():  # pragma: no cover — flask is the deployed backend
        return _quart_jsonify(_health_body(headers=_quart_request.headers))

    @app.server.before_request
    async def track_visitor():  # pragma: no cover
        try:
            tracker.track_visit(
                _quart_request.path,
                _quart_request.headers.get("User-Agent", ""),
                _quart_request.remote_addr,
                headers=dict(_quart_request.headers),
            )
        except Exception:  # noqa: BLE001 — analytics must never break a page view
            pass

else:
    from flask import jsonify as _flask_jsonify
    from flask import request as _flask_request

    @app.server.get("/healthz")
    def healthz():
        """Liveness probe: Render's health check, the hub's hourly sweep, CD's
        sustained-health loop and scripts/network_smoke.py all read this.

        Never counted as a visit: lib/analytics_tracker drops /healthz at
        write time, because Render probes it far more often than anyone reads
        the docs.
        """
        return _flask_jsonify(_health_body(headers=_flask_request.headers))

    # Headers are passed so the tracker can read the real client IP and
    # country from the proxy: behind Render or Cloudflare, `remote_addr` is
    # the proxy and every visitor would otherwise look like the same one.
    @app.server.before_request
    def track_visitor():
        try:
            tracker.track_visit(
                _flask_request.path,
                _flask_request.headers.get("User-Agent", ""),
                _flask_request.remote_addr,
                headers=dict(_flask_request.headers),
            )
        except Exception:  # noqa: BLE001 — analytics must never break a page view
            pass


# ============================================================================
# Access control (dash-improve-my-llms >= 2.6.0). Reads the tiers the pages
# just declared, so it must run after they are registered and before the
# routes are attached. The policy and the reasoning live in lib/access.py.
#
# This block is the enforcement half. Until this pass the registration above
# was DECLARATION ONLY — the instrument-never-meter posture of the 30-day
# data window. The window's rule still holds where it matters: no metering,
# no 402, no day scope. What arrives here is the interactive sign-in gate,
# shipped DARK (PAGE_DEFAULT_TIER=public), with the flip left to env.
# ============================================================================

from lib import access as _access  # noqa: E402
from lib import page_tiers as _page_tiers  # noqa: E402
from lib import page_visibility as _page_visibility  # noqa: E402

# Tiered corpus documents (dash-improve-my-llms >= 2.4.0). Pseudo-paths:
# they never enter dash.page_registry, so they cannot leak into listings —
# registering them here lets this satellite tier its compact briefing and
# full corpus via env (LLMS_SMALL_TIER / LLMS_FULL_TIER), and the hub can
# tighten either network-wide through its page-tier ceilings with no
# redeploy here. The explicit `or "public"` matters: these used to register
# under the PAGE_DEFAULT_TIER fallback, which meant flipping that env to
# gate the *interactive* site would silently gate the corpus documents too.
# Machine surfaces stay public through the window, by decision — so their
# tier is now always a deliberate setting, never an ambient default.
_page_tiers.register("/llms-small.txt",
                     os.environ.get("LLMS_SMALL_TIER") or "public")
_page_tiers.register("/llms-full.txt",
                     os.environ.get("LLMS_FULL_TIER") or "public")

# The home page registers via pages/home.py, not pages/markdown.py, so no
# frontmatter ever declares its tier — under PAGE_DEFAULT_TIER=auth it would
# silently inherit the gate. The funnel's front door stays public, always.
_page_tiers.register("/", "public")

# force= when either gate env is present: with every tier still public the
# auto-detect would skip the wiring, but a host that flips by env needs the
# verdict plumbing (and the prerender's use of it) live during the dark
# launch, not on the flip. A host that flips without it wired would
# prerender gated prose to crawlers — the ordering rule from the plan.
ACCESS_ENABLED = _access.configure(
    force=bool(os.environ.get("PAGE_DEFAULT_TIER")
               or os.environ.get("LLMS_PUBLIC_DEFAULT"))
)

# Wires /llms.txt, /<page>/llms.txt, /robots.txt, /sitemap.xml and
# bot-detection middleware. Pages (home + every docs/*.md) were already
# registered by use_pages importing pages/ during Dash(); nothing may register
# in front of /<page>/llms.txt after this point.
add_llms_routes(app, LLMSConfig(warn_missing_llms_doc=True))

# The ledger row (1.6.34, dimll 2.8.0): the package emits one event per
# corpus document it serves and does no I/O with it; the tracker keeps it
# as the `reads` table next to `visits`. Registered ONCE — the test suite
# imports run.py more than once per process and `on_document_read`
# appends, so a marker on the callback's owner guards the second import
# (the package also dedups an identical callable; belt and braces).
if not getattr(tracker, "_read_hook_registered", False):
    on_document_read(tracker.record_read)
    tracker._read_hook_registered = True

if BACKEND == "fastapi":  # pragma: no cover — flask is the deployed backend
    # Mirror image of the Flask hook above: Starlette runs the LAST-added
    # middleware outermost, so adding ours after add_llms_routes is what lets
    # it see crawler requests before the bot middleware answers them.
    @app.server.middleware("http")
    async def track_visitor_mw(request, call_next):
        try:
            client = request.client
            tracker.track_visit(
                request.url.path,
                dict(request.headers).get("user-agent", ""),
                client.host if client else None,
                headers=dict(request.headers),
            )
        except Exception:  # noqa: BLE001
            pass
        return await call_next(request)


# The hub's announcement feed, rendered in the header of this site's llms.txt
# viewer. Opt-in: with NETWORK_BULLETIN_URL unset it wires nothing and the
# viewer still renders on the package's built-in tips. The boot line says
# which of the two states this process is in — an announcement that never
# appears is not a symptom anyone notices.
print(
    f"[dash-flows docs] network bulletin: "
    f"{'wired -> ' + (bulletin.url() or '') if bulletin.configure() else 'off (NETWORK_BULLETIN_URL unset)'}"
)

# ============================================================================

# Build the shell after pages are registered so the navbar can list them.
from components.appshell import create_appshell  # noqa: E402

app.layout = create_appshell(dash.page_registry.values())

# SPA route changes never reach the server — beacon them to /api/pageview so
# sessions read as multi-page (see lib/pageview_beacon.py).
register_pageview_beacon()

server = app.server

# ============================================================================
# The person -> agent handoff: /api/agent-key turns the browser's Clerk
# session into a portable ?key= for copied llms.txt URLs (lib/agent_key.py).
# 204 for everyone until Clerk and the hub are configured, so it is safe to
# mount unconditionally — and mounting it always is what keeps the route off
# Dash's GET-only page catch-all, which would otherwise answer it with the
# app shell at 200 and look like a working endpoint.
# ============================================================================

from lib.agent_key import register_agent_key_route  # noqa: E402

register_agent_key_route(app, BACKEND)

# The three-absences-and-one-presence acceptance check for this host's
# deploy: THIS line present and naming the dimll floor, no [visibility]
# warning from lib/page_visibility, and no [auth] warning from lib/auth.
_non_public = sum(1 for t in _page_tiers.registered().values() if t != "public")
print(
    f"[flows] interactive gate: default tier "
    f"'{os.environ.get('PAGE_DEFAULT_TIER') or 'public'}', "
    f"{_non_public} non-public page(s), machine surfaces "
    f"{'GATED' if not _page_tiers.get_llms_public('/__probe__') else 'open'} "
    f"by default (LLMS_PUBLIC_DEFAULT), access wiring "
    f"{'ON' if ACCESS_ENABLED else 'off'}, clerk "
    f"{'ON' if CLERK_ENABLED else 'off'}, dimll "
    f"{'.'.join(map(str, _llms_version))}, control board at "
    f"/admin/control-board ({_page_visibility.override_count()} live "
    f"override(s))."
)

# Hourly signed rollup POSTed to 2plot.ai so the hub's owner-only /traffic
# dashboard can chart this app alongside the network. No-op unless
# CROSS_APP_WEBHOOK_SECRET is set. A flock lease means exactly one worker
# reports per interval rather than N racing duplicates.
from lib.satellite_reporter import start_reporter  # noqa: E402

start_reporter()


if __name__ == "__main__":
    app.run(
        debug=os.environ.get("DASH_DEBUG", "0") == "1",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8560)),
    )
