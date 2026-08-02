import dash_mantine_components as dmc
from dash import Output, Input, clientside_callback
from dash_iconify import DashIconify

from components.backend_badge import create_backend_badge
from lib.backend import get_backend_info


def create_link(icon, href):
    """Create an external link icon button"""
    return dmc.Anchor(
        dmc.ActionIcon(
            DashIconify(icon=icon, width=22),
            variant="subtle",
            size="lg",
            color="gray",
        ),
        href=href,
        target="_blank",
    )


def create_search(data):
    """Create searchable dropdown for component navigation"""
    return dmc.Select(
        id="select-component",
        placeholder="Search pages...",
        searchable=True,
        clearable=True,
        w=240,
        size="sm",
        nothingFoundMessage="No pages found",
        leftSection=DashIconify(icon="mingcute:search-3-line", width=18),
        data=[
            {"label": component["name"], "value": component["path"]}
            for component in data
            if component["name"] not in ["Home", "Not found 404"]
        ],
        visibleFrom="sm",
        comboboxProps={"zIndex": 2000},
        styles={
            "input": {
                "borderColor": "var(--mantine-color-gray-4)",
            }
        }
    )


def _create_openapi_link():
    """Show a Swagger UI link only when the FastAPI backend is active."""
    info = get_backend_info()
    if info.name != "fastapi":
        return None
    return dmc.Tooltip(
        label="OpenAPI docs (Swagger UI) — available on the FastAPI backend",
        position="bottom",
        withArrow=True,
        children=dmc.Anchor(
            dmc.Badge(
                "OpenAPI",
                leftSection=DashIconify(icon="logos:swagger", width=14),
                variant="light",
                color="cyan",
                radius="sm",
                styles={"root": {"textTransform": "none", "fontWeight": 600}},
            ),
            href="/docs",
            target="_blank",
            underline=False,
        ),
    )


def create_header(data):
    """Create application header with logo, search, and theme toggle"""
    return dmc.AppShellHeader(
        dmc.Group(
            [
                # Left section: Hamburger (mobile) + Burger (desktop collapse) + Logo
                dmc.Group(
                    [
                        dmc.ActionIcon(
                            DashIconify(icon="radix-icons:hamburger-menu", width=22),
                            id="drawer-hamburger-button",
                            variant="subtle",
                            size="lg",
                            color="gray",
                            hiddenFrom="md",
                        ),
                        # Desktop-only burger: collapses/expands the AppShell navbar
                        # on md-xl screens. Default opened=True so users see the X
                        # state on first load (navbar visible).
                        dmc.Burger(
                            id="desktop-navbar-toggle",
                            opened=True,
                            size="sm",
                            visibleFrom="md",
                        ),
                        dmc.Anchor(
                            dmc.Group(
                                [
                                    DashIconify(
                                        icon="carbon:flow",
                                        width=30,
                                        color="#3b82f6",
                                    ),
                                    dmc.Text(
                                        "dash-flows",
                                        size="lg",
                                        fw=700,
                                        c="#3b82f6",
                                        id="dash-docs-title",
                                    ),
                                ],
                                gap="sm",
                            ),
                            href="/",
                            underline=False,
                        ),
                    ],
                    gap="md",
                ),

                # Right section: Backend badge + OpenAPI (fastapi only) + Search + GitHub + Theme toggle
                dmc.Group(
                    [
                        dmc.Box(create_backend_badge(), visibleFrom="sm"),
                        dmc.Box(_create_openapi_link(), visibleFrom="md"),
                        create_search(data),
                        create_link(
                            "radix-icons:github-logo",
                            "https://github.com/pip-install-python/dash-flows",
                        ),
                        dmc.ActionIcon(
                            [
                                DashIconify(
                                    icon="radix-icons:sun",
                                    width=22,
                                    id="light-theme-icon",
                                ),
                                DashIconify(
                                    icon="radix-icons:moon",
                                    width=22,
                                    id="dark-theme-icon",
                                ),
                            ],
                            variant="subtle",
                            color="yellow",
                            id="color-scheme-toggle",
                            size="lg",
                        ),
                    ],
                    gap="sm",
                ),
            ],
            justify="space-between",
            h=70,
            px="xl",
        ),
    )


clientside_callback(
    """
    function(value) {
        if (value) {
            return value
        }
    }
    """,
    Output("url", "href"),
    Input("select-component", "value"),
)

clientside_callback(
    """function(n_clicks) { return true }""",
    Output("components-navbar-drawer", "opened"),
    Input("drawer-hamburger-button", "n_clicks"),
    prevent_initial_call=True,
)
