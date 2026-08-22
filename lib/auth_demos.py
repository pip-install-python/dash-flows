"""Teaser demos for the authentication gate cards.

Each auth-gated docs page can register ONE live example that renders inside
the sign-in card (lib.gate_layouts.sign_in_layout) — an interactive taste of
what's behind the gate, with no code and no surrounding docs.

The modules referenced here are the same ``.. exec::`` example modules the
docs pages use (they expose a module-level ``component``), so they're already
imported — and their callbacks already registered — when pages/markdown.py
parses the docs at startup. Only one layout (gate card OR full docs) renders
per request, so sharing the component instances never duplicates IDs.

The table ships EMPTY in the template: entries are site-specific dotted
paths, so each satellite fills in its own hero example (one entry is plenty —
this is a funnel, not a gallery).

Entries:
    endpoint -> {
        "module":     dotted path of the example module,
        "caption":    short label shown next to the "Live demo" badge,
        "max_height": px cap for the demo viewport inside the card,
        "height":     optional explicit px height — needed by components that
                      size to their container,
    }
"""
from __future__ import annotations

import importlib
import logging

logger = logging.getLogger(__name__)

DEMOS: dict[str, dict] = {
    # THIS SITE'S HERO. Gate /nodes (control board, or `tier: auth` in
    # docs/nodes/nodes.md frontmatter) and its sign-in card renders a live,
    # draggable graph carrying every node type this library ships — input,
    # default, output, resizable, circle and a group with children — above
    # the "Authentication required" copy.
    #
    # docs.nodes.demo is the right choice for the funnel specifically
    # because it is CALLBACK-FREE: the teaser is fully interactive (drag,
    # pan, zoom, resize) without a single server round trip, so an
    # anonymous visitor gets the real thing rather than a screenshot of it.
    # It is also already imported at startup by pages/markdown.py parsing
    # the same `.. exec::docs.nodes.demo` directive, so nothing extra is
    # loaded to render the card.
    #
    # `height` is set, not just `max_height`: DashFlows sizes to its
    # container, and a flow canvas in a box with no definite height
    # collapses to nothing. 440 matches the demo module's own style.
    "/nodes": {
        "module": "docs.nodes.demo",
        "caption": "Live graph — drag, zoom, resize",
        "max_height": 460,
        "height": 440,
    },
}


def build_demo(path: str):
    """Return the teaser demo block for ``path``, or None.

    Import/attribute failures degrade to the plain (demo-less) card — a broken
    example must never take down the sign-in funnel.
    """
    spec = DEMOS.get(path)
    if spec is None:
        return None
    try:
        module = importlib.import_module(spec["module"])
        component = getattr(module, "component")
    except Exception as e:
        logger.warning("Auth-gate demo %s failed to load (%s) — card renders "
                       "without it", spec.get("module"), e)
        return None

    import dash_mantine_components as dmc
    from dash_iconify import DashIconify

    return dmc.Box(
        [
            dmc.Group(
                [
                    dmc.Badge(
                        "Live demo — try it",
                        variant="light",
                        color="teal",
                        leftSection=DashIconify(icon="tabler:hand-click", width=13),
                    ),
                    dmc.Text(spec.get("caption", ""), size="sm", c="dimmed"),
                ],
                justify="space-between",
                px="md",
                pt="md",
            ),
            dmc.Box(
                component,
                p="md",
                className="auth-gate-demo",
                style={
                    "maxHeight": f"{spec.get('max_height', 420)}px",
                    "overflowY": "auto",
                    "overflowX": "hidden",
                    **({"height": f"{spec['height']}px"} if "height" in spec else {}),
                },
            ),
        ]
    )
