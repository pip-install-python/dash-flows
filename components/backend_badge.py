"""Backend indicator badge used in the header.

Reads from ``lib.backend.get_backend_info`` so the displayed backend stays
in sync with what ``run.py`` actually instantiated.
"""
from __future__ import annotations

import dash_mantine_components as dmc
from dash_iconify import DashIconify

from lib.backend import get_backend_info


def create_backend_badge(size: str = "md") -> dmc.Tooltip:
    """Return a small, themed badge advertising the active Dash backend.

    Renders without a Dash id so it can be placed in multiple slots
    (header, navbar, drawer) without colliding.
    """
    info = get_backend_info()

    label = info.label
    if info.is_async:
        label += " · async"

    badge = dmc.Badge(
        label,
        leftSection=DashIconify(icon=info.icon, width=14),
        variant="light",
        color=info.color,
        radius="sm",
        size=size,
        styles={"root": {"textTransform": "none", "fontWeight": 600}},
    )

    return dmc.Tooltip(
        label=f"Dash backend: {info.label}. {info.description}",
        position="bottom",
        withArrow=True,
        multiline=True,
        w=260,
        children=badge,
    )
