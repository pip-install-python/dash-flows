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
# distrust the rest of the list for. muicharts.2plot.dev and
# flexlayout.2plot.dev have no docs site yet — add them in the same change
# that ships them, not before.
#
# ---------------------------------------------------------------------------
# DIVERGENCE FROM boilerplate.2plot.dev — deliberate, not drift.
#
# Verified by request on 2026-07-31, not by reading a status table:
#
#     pannellum.2plot.dev   NXDOMAIN   <- listed in the boilerplate's copy
#     emojimart.2plot.dev   NXDOMAIN   <- listed in the boilerplate's copy
#     muischeduler.2plot.dev  200      (hub still says "shipping")
#     flows.2plot.dev         200      (hub still says "shipping")
#     leaflet.2plot.dev       200
#     boilerplate.2plot.dev   200
#     llms.2plot.dev          503 spin-up, live per the hub  <- ABSENT upstream
#
# So the two dead entries are dropped here and llms.2plot.dev is added. The
# real fix belongs in the boilerplate, because that copy propagates to every
# satellite; restore this file to a straight copy once it lands there.
# ---------------------------------------------------------------------------
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
        "name": "dash-flows",
        "url": "https://flows.2plot.dev",
        "description": "Node-graph editors built on React Flow.",
    },
    {
        "name": "dash-improve-my-llms",
        "url": "https://llms.2plot.dev",
        "description": "The AI/LLM and SEO package every site in this network is built on.",
    },
    {
        "name": "dash-email",
        "url": "https://email.2plot.dev",
        "description": "Email composition and delivery components.",
    },
    # dash-pannellum (pannellum.2plot.dev) and dash-emoji-mart
    # (emojimart.2plot.dev) belong here the day their DNS resolves. Both are
    # NXDOMAIN as of 2026-07-31 — see the note above.
]

AFFILIATED: List[Dict[str, str]] = [
    {
        "name": "Pip Install Python",
        "url": "https://pip-install-python.com",
        "description": "The original component documentation site.",
    },
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
]

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
