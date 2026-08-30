"""Cross-host directory for the 2plot network — one definition, every satellite.

Why this file exists
--------------------
Search engines follow links between hosts weakly; agents don't follow them at
all. A model answering "what does this ecosystem provide?" fetches one or two
URLs and reasons from what came back. Landing on ``leaflet.2plot.dev`` it sees
one library, with nothing in the markup saying the other eleven hosts exist.
``sitemap.xml`` cannot fix that — a sitemap is scoped to its own origin by
design — so ``dash-improve-my-llms`` 2.1 emits an explicit machine-readable
directory instead: ``<link rel="related">`` tags in ``<head>``, a ``## Network``
section in ``/llms.txt``, and followed links in the prerendered body.

Keep the definition **here**, in the template, and import it. Twelve
hand-maintained copies of the same peer list will drift, and a directory that
disagrees with itself across hosts is worse than no directory at all.

Three tiers, and the distinction is load-bearing:

``PEERS``
    Same network, same operator. These build the cross-host graph you own.
``AFFILIATED``
    Yours, on unrelated domains. Findable when asked "what else did you
    build?" without being swept into "what is the 2plot network?".
``EXTERNAL``
    Third-party docs you reference but don't own. Emitted ``rel="nofollow"``
    — references, not endorsements.

Usage in a satellite's ``run.py``, before ``add_llms_routes(app)``::

    from lib.constants import BASE_URL
    from lib import network_directory

    app._base_url = BASE_URL
    network_directory.apply(BASE_URL)
"""

from __future__ import annotations

from typing import Any, Dict, List

# Only list hosts that are actually live. A directory entry pointing at a
# subdomain with no site is a dead link an agent will follow once and then
# distrust the rest of the list for. The full docs fleet went live on paid
# hosting 2026-08-19/20 — muicharts, flexlayout and llms joined in that
# window (the drift sweep of 2026-08-20 found seven different versions of
# this list across nine repos; this copy is the canonical one and the fleet
# syncs FROM here, verbatim). excalidraw.2plot.dev and modelviewer.2plot.dev
# were deliberately absent until they deployed; both went live in the gate
# wave (2026-08-21/22, verified via /healthz build identity) and joined in
# 1.6.5. The fleet re-copy carries them to every satellite's directory.
PEERS: List[Dict[str, str]] = [
    {
        "name": "2plot.ai",
        "url": "https://2plot.ai",
        "description": "Network hub and account origin.",
    },
    {
        "name": "2plot.dev",
        "url": "https://2plot.dev",
        "description": "Package index for every open-source component in the network.",
    },
    {
        "name": "Documentation boilerplate",
        "url": "https://boilerplate.2plot.dev",
        "description": "The markdown-driven documentation template every satellite site is built from.",
    },
    {
        "name": "dash-leaflet2",
        "url": "https://leaflet.2plot.dev",
        "description": "Leaflet 2 maps as Dash components.",
    },
    {
        "name": "dash-mui-scheduler",
        "url": "https://muischeduler.2plot.dev",
        "description": "MUI X Scheduler — calendars and event scheduling for Dash.",
    },
    {
        "name": "dash-mui-charts",
        "url": "https://muicharts.2plot.dev",
        "description": "MUI X charts, tree views and time pickers for Dash.",
    },
    {
        "name": "flexlayout-dash",
        "url": "https://flexlayout.2plot.dev",
        "description": "IDE-style dockable, resizable and floatable window panels.",
    },
    {
        "name": "dash-improve-my-llms",
        "url": "https://llms.2plot.dev",
        "description": "The AI/LLM and SEO package every site in this network is built on.",
    },
    {
        "name": "dash-flows",
        "url": "https://flows.2plot.dev",
        "description": "Node-graph editors built on React Flow.",
    },
    {
        "name": "dash-pannellum",
        "url": "https://pannellum.2plot.dev",
        "description": "360° panorama and virtual-tour viewer.",
    },
    {
        "name": "dash-emoji-mart",
        "url": "https://emojimart.2plot.dev",
        "description": "Emoji picker component.",
    },
    {
        "name": "dash-email",
        "url": "https://email.2plot.dev",
        "description": "Email composition and delivery components.",
    },
    {
        "name": "dash-model-viewer",
        "url": "https://modelviewer.2plot.dev",
        "description": "3D model viewer with AR support, built on Google's model-viewer.",
    },
    {
        "name": "dash-excalidraw",
        "url": "https://excalidraw.2plot.dev",
        "description": "Excalidraw virtual whiteboard and sketching canvas.",
    },
]

# pip-install-python.com is deliberately NOT here: the domain is retired
# network-wide (the fleet's retire-pip-install-python-domain sweep), and
# leaflet's test_social_card pins its absence. A directory that keeps
# pointing agents at a retired origin re-teaches them the identity the
# network spent a release unlearning.
AFFILIATED: List[Dict[str, str]] = [
    {
        "name": "Pirate's Bargain",
        "url": "https://piratesbargain.com",
        "description": "Deal aggregator built on the same Dash stack.",
    },
    {
        "name": "ai-agent.buzz",
        "url": "https://ai-agent.buzz",
        "description": "Agent tooling directory.",
    },
    {
        "name": "2plot.media",
        "url": "https://2plot.media",
        "description": "Media and streaming, on the same Dash stack.",
    },
]

# The top bar's *Other Apps* menu lists the PRIMARY applications only
# (owner, 2026-08-30): the hub, the catalogue and the affiliated sites —
# never the fleet's docs subdomains, which 2plot.dev's catalogue already
# lists. A set of URLs, not a hand-typed menu, so the registry stays the
# source and the menu==registry test asserts this filtered set.
PRIMARY = frozenset({
    "https://2plot.ai",
    "https://2plot.dev",
    "https://2plot.media",
    "https://piratesbargain.com",
    "https://ai-agent.buzz",
})

EXTERNAL: List[Dict[str, Any]] = [
    {
        "name": "Dash Mantine Components",
        "url": "https://www.dash-mantine-components.com",
        "description": "The UI component layer these docs are built with.",
        "llms_txt": "https://www.dash-mantine-components.com/llms.txt",
    },
    {
        "name": "Plotly Dash documentation",
        "url": "https://dash.plotly.com",
        "description": "Upstream framework documentation.",
    },
]

NETWORK_NAME = "The 2plot network"
NETWORK_DESCRIPTION = (
    "Open-source Dash component libraries by Pip Install Python. Each component "
    "has its own documentation site and its own llms.txt; 2plot.dev indexes all "
    "of them, and 2plot.ai is the hub."
)
HUB_URL = "https://2plot.dev"

# The mark drawn in the header of the rendered llms.txt view: "2" + morse
# encoding of "plot" + "ai", as columns of dots and dashes.
#
# No period glyph between the halves — the morse block already separates them,
# and a literal "." next to it reads as punctuation dropped into a graphic.
# The renderer turns a suffix ending in "i" into an upward flourish, so "ai"
# draws as "a" plus that mark; `label` carries the real domain for screen
# readers and the SVG <title>, which is the only place the dot belongs.
#
# Defined here rather than per-app because this module is copied verbatim into
# every satellite — that is what keeps one mark across the network instead of
# twelve slightly different ones.
WORDMARK = {
    "morse": "plot",
    "prefix": "2",
    "suffix": "ai",
    "label": "2plot.ai",
}


def peers_for(app_url: str) -> List[Dict[str, str]]:
    """`PEERS` with this app removed.

    A site listing itself as its own peer reads as generated rather than
    curated, and it wastes a slot in a list an agent may only skim.
    """
    own = app_url.rstrip("/")
    return [p for p in PEERS if p["url"].rstrip("/") != own]


# Menu icons, keyed by URL and kept OUT of the entries above: the package's
# `register_network` forwards every entry key to `register_network_site`
# verbatim, and an unknown key is a TypeError at boot (measured 1.6.38).
ICONS: Dict[str, str] = {
    "https://2plot.ai": "simple-icons:plotly",
    "https://2plot.dev": "solar:box-bold-duotone",
    "https://boilerplate.2plot.dev": "streamline-pixel:content-files-favorite-book",
    "https://leaflet.2plot.dev": "mdi:map-outline",
    "https://muischeduler.2plot.dev": "mdi:calendar-clock",
    "https://muicharts.2plot.dev": "mdi:chart-areaspline",
    "https://flexlayout.2plot.dev": "mdi:view-dashboard-outline",
    "https://llms.2plot.dev": "mdi:robot-outline",
    "https://flows.2plot.dev": "mdi:graph-outline",
    "https://pannellum.2plot.dev": "mdi:panorama-variant-outline",
    "https://emojimart.2plot.dev": "mdi:emoticon-outline",
    "https://email.2plot.dev": "mdi:email-outline",
    "https://modelviewer.2plot.dev": "mdi:cube-outline",
    "https://excalidraw.2plot.dev": "mdi:draw",
    "https://piratesbargain.com": "mdi:pirate",
    "https://ai-agent.buzz": "game-icons:beehive",
    "https://2plot.media": "mdi:movie-open-play-outline",
    "https://www.dash-mantine-components.com": "mdi:web",
    "https://dash.plotly.com": "mdi:web",
}


def other_apps_for(app_url: str) -> List[Dict[str, str]]:
    """The top bar's *Other Apps* menu (1.6.38): the PRIMARY entries of
    PEERS + AFFILIATED, in registry order, this app removed, each labelled
    by its DOMAIN — short enough for a menu, and the one name every host
    agrees on. Never hand-typed twice again: the survey found 2plot.dev
    listed twice on four hosts and a retired domain on one. `icon` comes
    from ICONS below (default `mdi:web`)."""
    own = app_url.rstrip("/")
    out = []
    for entry in PEERS + AFFILIATED:
        url = entry["url"].rstrip("/")
        if url == own or url not in PRIMARY:
            continue
        domain = url.split("://", 1)[-1].split("/", 1)[0]
        out.append({"label": domain, "url": entry["url"],
                    "icon": ICONS.get(url, "mdi:web"), "name": entry["name"]})
    return out


def apply(app_url: str) -> None:
    """Publish the directory for the app served at ``app_url``.

    Degrades rather than fails on older releases of the package. A satellite
    pinned behind this file should still boot: losing the directory, or losing
    the wordmark, is a degradation — refusing to start is not.

    That matters during a staged rollout, when this module reaches satellites
    before the new package does. ``register_network`` arrived in 2.1 and its
    ``wordmark`` argument in 2.2, and Python raises ``TypeError`` on an unknown
    keyword, so the argument is only passed when the installed signature
    actually accepts it.
    """
    try:
        from dash_improve_my_llms import register_network
    except ImportError:  # pragma: no cover - only on <2.1
        import warnings

        warnings.warn(
            "dash-improve-my-llms is older than 2.1, so the cross-host network "
            "directory will not be published. Upgrade to publish it.",
            RuntimeWarning,
            stacklevel=2,
        )
        return

    import inspect

    extra: Dict[str, Any] = {}
    if "wordmark" in inspect.signature(register_network).parameters:
        extra["wordmark"] = WORDMARK

    register_network(
        name=NETWORK_NAME,
        description=NETWORK_DESCRIPTION,
        hub_url=HUB_URL,
        peers=peers_for(app_url),
        affiliated=AFFILIATED,
        external=EXTERNAL,
        **extra,
    )
