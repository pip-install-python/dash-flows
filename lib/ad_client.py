"""2plot.dev ad-network client for satellite documentation apps.

Drop-in module shared verbatim across every dash-documentation-boilerplate
app (dash-email, dash-mui-scheduler, dash-flows, dash-mui-charts, ...).
On each docs page view the ad slot fetches a campaign from the central
2plot.dev ad server (server-to-server, so ad blockers and CORS never see
it); clicks are beaconed from the browser straight back to 2plot.dev with
app + page attribution, feeding the /admin/ad-board performance tables.

Wiring (boilerplate apps):
    # pages/markdown.py — after `layout = parse(content)`:
    from lib.ad_client import inject_ad_into_aside
    inject_ad_into_aside(layout, metadata.endpoint)

Wiring (custom apps without the markdown TOC aside):
    from lib.ad_client import create_ad_component, register_location_refresh
    ...place create_ad_component("__navbar__") in a static shell...
    register_location_refresh("url")   # re-serve the ad on SPA navigation

Env:
    AD_SERVER_URL  — ad server origin (default https://2plot.dev)
    AD_APP_ID      — this app's identity in the network (default "flows",
                     this app's 2plot network-directory key; override per
                     deployment)

Failure behaviour: if the ad server is unreachable the slot simply stays
hidden, and a 60s circuit breaker stops retrying so an outage never adds
the HTTP timeout to every page view.
"""
from __future__ import annotations

import logging
import os
import threading
import time

import requests
import dash_mantine_components as dmc
from dash import MATCH, Input, Output, callback, clientside_callback, dcc, html, no_update
from dash_iconify import DashIconify

logger = logging.getLogger(__name__)

AD_SERVER_URL = os.environ.get("AD_SERVER_URL", "https://2plot.dev").rstrip("/")
# "flows" is this app's key in the 2plot network directory — the ONE short id
# used on every hub surface (ads, traffic, bulletin). The hub folds the legacy
# "dash-flows" spelling at ingest (`canonical_app_id`), so rows already logged
# under the package name are not orphaned — but a new deployment must
# converge, and render.yaml sets it explicitly rather than leaning on this
# default.
APP_ID = os.environ.get("AD_APP_ID", "flows")

_TIMEOUT = 2          # seconds per fetch — never stall a page view longer
_COOLDOWN = 60        # seconds to skip fetches after a failure
_session = requests.Session()
_breaker_lock = threading.Lock()
_last_failure = 0.0


def fetch_ad(page: str) -> dict | None:
    """GET one campaign from the ad server; None on any failure.

    Deliberately no caching of last-good ads: every served ad is logged as
    an impression server-side, and a cached ad would corrupt CTR. Failures
    trip a cooldown so an ad-server outage costs at most one timeout per
    process per minute.
    """
    global _last_failure
    with _breaker_lock:
        if time.time() - _last_failure < _COOLDOWN:
            return None

    from lib.constants import internal_ua

    try:
        resp = _session.get(
            f"{AD_SERVER_URL}/api/ad-network/serve",
            params={"app": APP_ID, "page": page},
            timeout=_TIMEOUT,
            # The highest-volume outbound call this app makes — one per docs
            # page view, server-to-server. Without the internal-traffic token
            # every one of them reaches 2plot.dev as `python-requests/2.x`,
            # which its tracker classifies as a bot: this satellite's readers
            # would be counted as crawler traffic on the hub. See
            # lib/constants.INTERNAL_UA.
            headers={"User-Agent": internal_ua("ad-client")},
        )
        if resp.status_code == 200 and resp.content:
            return resp.json()
        return None  # 204 = nothing to serve; not a failure
    except Exception as e:
        with _breaker_lock:
            _last_failure = time.time()
        logger.debug("Ad fetch failed (%s) — cooling down %ss", e, _COOLDOWN)
        return None


def create_ad_component(page_path: str) -> html.Div:
    """Hidden ad shell; the mount callback below fills it per page view."""
    return html.Div(
        id={"type": "net-ad-container", "page": page_path},
        style={"display": "none"},
        children=[
            dcc.Store(id={"type": "net-ad-data", "page": page_path}, data=None),
            dmc.Divider(
                label="Advertisement",
                labelPosition="center",
                mb="md",
                mt="xl",
                styles={
                    "label": {
                        "fontSize": "0.75rem",
                        "fontWeight": 600,
                        "textTransform": "uppercase",
                        "letterSpacing": "0.5px",
                        "color": "var(--mantine-color-gray-6)",
                    }
                },
            ),
            html.A(
                href="#",
                target="_blank",
                rel="noopener noreferrer sponsored",
                id={"type": "net-ad-link", "page": page_path},
                style={"textDecoration": "none"},
                children=dmc.Paper(
                    [
                        html.Img(
                            id={"type": "net-ad-img", "page": page_path},
                            src="",
                            alt="Advertisement",
                            style={
                                "width": "100%",
                                "height": "auto",
                                "display": "block",
                                "borderRadius": "8px",
                            },
                        ),
                        dmc.Text(
                            [
                                DashIconify(icon="tabler:info-circle", width=12,
                                            style={"marginRight": "4px"}),
                                "Sponsored Content",
                            ],
                            size="xs",
                            c="gray",
                            ta="center",
                            mt="xs",
                            style={"display": "flex", "alignItems": "center",
                                   "justifyContent": "center"},
                        ),
                    ],
                    p="sm",
                    withBorder=True,
                    radius="md",
                    style={"cursor": "pointer"},
                ),
            ),
        ],
    )


def inject_ad_into_aside(layout_list, page_path: str) -> bool:
    """Append the ad slot below the TOC links inside the page's aside.

    The `.. toc::` directive emits
    ``AppShellAside(children=ScrollArea(Stack([...])))`` — the ad joins the
    Stack so it scrolls with the TOC. Pages without a TOC get no ad.
    Fail-silent: an unexpected layout shape must never break page
    registration.
    """
    try:
        for el in layout_list:
            if isinstance(el, dmc.AppShellAside):
                stack = el.children.children  # ScrollArea -> Stack
                kids = stack.children
                if not isinstance(kids, list):
                    kids = [kids]
                kids.append(create_ad_component(page_path))
                stack.children = kids
                return True
    except Exception as e:
        logger.warning("Ad slot injection failed for %s: %s", page_path, e)
    return False


_AD_OUTPUTS = lambda match: (  # noqa: E731 — shared output signature
    Output({"type": "net-ad-img", "page": match}, "src"),
    Output({"type": "net-ad-img", "page": match}, "alt"),
    Output({"type": "net-ad-link", "page": match}, "href"),
    Output({"type": "net-ad-data", "page": match}, "data"),
    Output({"type": "net-ad-container", "page": match}, "style"),
)


def _serve(page: str):
    ad = fetch_ad(page)
    if not ad:
        return no_update, no_update, no_update, no_update, {"display": "none"}
    return (
        ad.get("image", ""),
        ad.get("name", "Advertisement"),
        ad.get("url", "#"),
        {
            "campaign_id": ad.get("campaign_id"),
            "app": APP_ID,
            "page": page,
            "click_url": f"{AD_SERVER_URL}/api/ad-network/click",
        },
        {},
    )


@callback(
    *_AD_OUTPUTS(MATCH),
    Input({"type": "net-ad-container", "page": MATCH}, "id"),
    # Explicit: boilerplate apps may set prevent_initial_callbacks=True
    # app-wide; the mount-fire is exactly what serves the ad per page view.
    prevent_initial_call=False,
)
def serve_network_ad(container_id):
    """Fetch + show an ad every time the slot mounts (each page view)."""
    return _serve((container_id or {}).get("page", "unknown"))


# Click beacon: browser → 2plot.dev directly. text/plain keeps it a CORS
# "simple request" (no preflight), which also keeps keepalive reliable.
clientside_callback(
    """
    function(n_clicks, adData) {
        if (n_clicks && adData && adData.click_url) {
            try {
                fetch(adData.click_url, {
                    method: 'POST',
                    keepalive: true,
                    headers: {'Content-Type': 'text/plain'},
                    body: JSON.stringify({
                        campaign_id: adData.campaign_id,
                        app: adData.app,
                        page: adData.page
                    })
                }).catch(function(){});
            } catch (e) {}
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output({"type": "net-ad-link", "page": MATCH}, "title"),
    Input({"type": "net-ad-link", "page": MATCH}, "n_clicks"),
    Input({"type": "net-ad-data", "page": MATCH}, "data"),
    prevent_initial_call=True,
)


def register_location_refresh(location_id: str = "url",
                              page_key: str = "__navbar__") -> None:
    """For ad slots living in the static app shell (not per-page layouts).

    Static shells mount once per hard load, so the mount callback above
    only fires once. Apps like dash-mui-charts call this to re-serve the
    slot on every SPA navigation, attributing the real pathname.
    """

    @callback(
        *[Output(o.component_id, o.component_property, allow_duplicate=True)
          for o in _AD_OUTPUTS(page_key)],
        Input(location_id, "pathname"),
        prevent_initial_call="initial_duplicate",
    )
    def refresh_shell_ad(pathname):
        return _serve(pathname or page_key)
