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

from lib import bulletin, network_directory  # noqa: E402
from lib.analytics_tracker import tracker  # noqa: E402
from lib.backend import resolve_backend, get_backend_info  # noqa: E402
from lib.constants import (  # noqa: E402
    APP_VERSION,
    DOCS_BASE_URL,
    ORIGIN_PLACEHOLDER,
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
    LLMSConfig,
    RobotsConfig,
    register_page_metadata,
)

# dash-improve-my-llms floor. 2.3.4 ships `resolve_site_title` (the /llms.txt
# H1 + viewer brand chip); 2.3.3 fixed the crawler taxonomy in robots.txt.
# Below the floor those surfaces silently publish the wrong identity, so the
# app refuses to boot rather than serve them — override with ALLOW_STALE_DEPS=1
# for local archaeology only.
LLMS_PKG_FLOOR = (2, 3, 4)
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
        "pip install -U 'dash-improve-my-llms[flask]>=2.3.4' "
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

# Expose backend info so UI components can render a badge without re-reading env.
app._backend_info = BACKEND_INFO
app._base_url = DOCS_BASE_URL

# Cross-host directory: <link rel="related"> tags, a `## Network` section in
# /llms.txt, and followed links in the prerendered body. Must run before
# add_llms_routes so the routes are built with it in place.
network_directory.apply(DOCS_BASE_URL)

# Training crawlers (GPTBot, ClaudeBot, CCBot, …) disallowed; user-triggered
# and search fetchers (Claude-User, Claude-SearchBot, ChatGPT-User,
# OAI-SearchBot, PerplexityBot) and traditional engines allowed. Correct as of
# dimll 2.3.3, which buckets per vendor rather than per company.
app._robots_config = RobotsConfig(
    block_ai_training=True,
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
# Native routes + visitor tracking — see the ORDER MATTERS note up top.
# ============================================================================


def _health_body() -> dict:
    from lib.satellite_reporter import app_key

    return {
        "ok": True,  # the network battery asserts this exact field
        "app": app_key(),
        "version": APP_VERSION,
        "dash": dash.__version__,
        "reporting": bool(os.environ.get("CROSS_APP_WEBHOOK_SECRET")),
    }


register_pageview_route(app, BACKEND)

if BACKEND == "fastapi":
    from starlette.responses import JSONResponse

    @app.server.get("/healthz", include_in_schema=False)
    async def healthz():  # pragma: no cover — flask is the deployed backend
        return JSONResponse(_health_body())

elif BACKEND == "quart":
    from quart import jsonify as _quart_jsonify
    from quart import request as _quart_request

    @app.server.get("/healthz")
    async def healthz():  # pragma: no cover — flask is the deployed backend
        return _quart_jsonify(_health_body())

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
        return _flask_jsonify(_health_body())

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


# Wires /llms.txt, /<page>/llms.txt, /robots.txt, /sitemap.xml and
# bot-detection middleware. Pages (home + every docs/*.md) were already
# registered by use_pages importing pages/ during Dash(); nothing may register
# in front of /<page>/llms.txt after this point.
add_llms_routes(app, LLMSConfig(warn_missing_llms_doc=True))

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
