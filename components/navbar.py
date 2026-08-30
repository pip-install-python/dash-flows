"""The sidebar — one registry, the app's identity from frontmatter (1.6.38).

Nothing in this file is edited by a fork. The sections come from each
page's frontmatter (`category:` + `order:`) in the order of
`lib.constants.CATEGORY_ORDER`; Resources from `lib.constants.resources()`;
the Admin section from a callback that returns nothing unless the viewer is
an admin (the pip-docs+ pattern); the network lives in the top bar's Other
Apps menu (components/header.py), never here. The survey of 2026-08-30 found
the previous hand-written `page_order` / `excluded_links` copied and edited
twelve different ways across the fleet — this is the replacement.

Contract order: Home · Changelog → the app's sections → API (when
generated) → Resources → Admin (owner-only; absent otherwise).
"""
from __future__ import annotations

from collections import defaultdict

import dash_mantine_components as dmc
from dash import Input, Output, callback
from dash_iconify import DashIconify

from lib.constants import CATEGORY_ORDER, HEADER_HEIGHT, resources

ADMIN_PREFIX = "/admin/"
UNCATEGORISED = "Documentation"
DEFAULT_ICON = "fluent:document-24-regular"


def create_nav_link(icon, text, href, external=False):
    """Create a styled navigation link with icon"""
    return dmc.Anchor(
        dmc.Group(
            [
                DashIconify(icon=icon, width=18),
                dmc.Text(text, size="sm", fw=500),
            ],
            gap="sm",
        ),
        href=href,
        target="_blank" if external else None,
        className="navbar-link",
        underline=False,
    )


def create_nav_section(title, links):
    """Create a navigation section with a title and links"""
    return dmc.Stack(
        [
            dmc.Text(
                title,
                size="xs",
                fw=700,
                tt="uppercase",
                c="dimmed",
                mb="xs",
            ),
            dmc.Stack(links, gap="xs"),
        ],
        gap="sm",
    )


# ----------------------------------------------------------------- pages --


def is_admin_path(path: str) -> bool:
    return (path or "").startswith(ADMIN_PREFIX)


def is_nav_page(entry) -> bool:
    """A page the sidebar and search may list: not Home, not /admin/*, not
    the 404, not a hidden-tier page, and registered from a real path."""
    path = entry.get("path") or ""
    if not path.startswith("/") or path == "/" or is_admin_path(path):
        return False
    if entry.get("name") in ("Not found 404",) or path in ("/404", "/changelog", "/api"):
        return False
    try:
        from lib import page_tiers

        if page_tiers.local_tier(path) == "hidden":
            return False
    except Exception:  # pragma: no cover - tiers optional on a fork
        pass
    return True


def _sort_key(entry):
    order = entry.get("order")
    try:
        order = int(order) if order is not None else 1000
    except (TypeError, ValueError):
        order = 1000
    return (order, entry.get("name") or "")


def sections_for(data) -> list[tuple[str, list]]:
    """``[(section title, [registry entries]), ...]`` in contract order:
    CATEGORY_ORDER first, then any other category alphabetically; pages
    within a section by `order` then name. Uncategorised pages fall into
    one "Documentation" section, last of the app's own."""
    by_cat: dict[str, list] = defaultdict(list)
    for entry in data:
        if not is_nav_page(entry):
            continue
        by_cat[entry.get("category") or UNCATEGORISED].append(entry)
    known = [c for c in CATEGORY_ORDER if c in by_cat]
    extra = sorted(c for c in by_cat if c not in CATEGORY_ORDER and c != UNCATEGORISED)
    tail = [UNCATEGORISED] if UNCATEGORISED in by_cat else []
    return [(c, sorted(by_cat[c], key=_sort_key)) for c in known + extra + tail]


def admin_pages(data) -> list:
    return sorted((e for e in data if is_admin_path(e.get("path") or "")),
                  key=lambda e: e.get("name") or "")


def _page_link(entry):
    return create_nav_link(entry.get("icon") or DEFAULT_ICON, entry["name"], entry["path"])


def _has_api_page(data) -> bool:
    return any((e.get("path") or "") == "/api" for e in data)


def _has_changelog(data) -> bool:
    return any((e.get("path") or "") == "/changelog" for e in data)


# ----------------------------------------------------------------- tree --


def create_content(data, variant="desktop"):
    """The sidebar tree. `variant` names the Admin placeholder so the
    desktop navbar and the mobile drawer each get their own callback
    target (a duplicate id would be a Dash error)."""
    data = list(data)
    blocks = [create_nav_link("fluent:home-24-regular", "Home", "/")]
    if _has_changelog(data):
        blocks.append(create_nav_link("tabler:history", "Changelog", "/changelog"))

    for title, entries in sections_for(data):
        blocks.append(dmc.Divider(mt="xs", mb="xs"))
        blocks.append(create_nav_section(title, [_page_link(e) for e in entries]))

    if _has_api_page(data):
        blocks.append(dmc.Divider(mt="md", mb="sm"))
        blocks.append(create_nav_section(
            "API", [create_nav_link("mdi:api", "Component props", "/api")]))

    blocks.append(dmc.Divider(mt="md", mb="sm"))
    blocks.append(create_nav_section(
        "Resources",
        [create_nav_link(r["icon"], r["label"], r["url"], external=True)
         for r in resources()],
    ))

    # Admin: filled per request by the callback below; an empty div for
    # everyone else — the section does not exist for them, it is not hidden.
    blocks.append(dmc.Box(id=f"navbar-admin-{variant}"))

    return dmc.ScrollArea(
        offsetScrollbars=True,
        type="scroll",
        style={"height": "100%"},
        children=dmc.Stack(blocks, gap="xs", p="md"),
    )


def admin_section(data):
    """The Admin section for a viewer who may see it, or None."""
    pages = admin_pages(data)
    if not pages:
        return None
    return dmc.Stack(
        [dmc.Divider(mt="md", mb="sm"),
         create_nav_section("Admin", [_page_link(e) for e in pages])],
        gap="xs",
    )


@callback(
    Output("navbar-admin-desktop", "children"),
    Output("navbar-admin-mobile", "children"),
    Input("navbar-admin-desktop", "id"),
)
def render_admin_section(_):
    """Fill the Admin section per page load.

    The navbar tree is built once at startup with no request context, so
    the per-user check runs here, inside a request. Non-admins get empty
    divs. Without Clerk (local work) the section shows only when
    ALLOW_UNGATED_ADMIN=1 — the same gate the admin pages themselves use.
    """
    import dash

    from lib.auth import admin_access_open, clerk_enabled, is_admin_user

    if clerk_enabled():
        if not is_admin_user():
            return None, None
    elif not admin_access_open():
        return None, None
    data = list(dash.page_registry.values())
    return admin_section(data), admin_section(data)


# --------------------------------------------------------------- search --


def search_data(data) -> list:
    """Search entries: the pages the sidebar lists, and nothing else —
    never /admin/*, never a hidden-tier page (an anonymous visitor could
    otherwise enumerate them from the dropdown)."""
    return [{"label": e["name"], "value": e["path"]}
            for e in sorted((e for e in data if is_nav_page(e)), key=_sort_key)]


def create_mobile_content(data):
    """Drawer body: a sticky search field above the scrolling nav sections.

    The header's search Select is `visibleFrom="sm"`, so phones otherwise have
    no way to jump straight to a page. This is that missing entry point.
    """
    return dmc.Stack(
        [
            dmc.Box(
                dmc.Select(
                    id="mobile-select-component",
                    placeholder="Search pages...",
                    searchable=True,
                    clearable=True,
                    size="md",
                    nothingFoundMessage="No pages found",
                    leftSection=DashIconify(icon="mingcute:search-3-line", width=18),
                    data=search_data(data),
                    comboboxProps={"zIndex": 2000},
                    **{"aria-label": "Search pages"},
                ),
                p="md",
                pb="xs",
            ),
            dmc.Divider(),
            # flex/minHeight give the ScrollArea a definite box to scroll inside.
            dmc.Box(create_content(data, variant="mobile"), style={"flex": 1, "minHeight": 0}),
        ],
        gap=0,
        className="mobile-nav",
        style={"height": "100%"},
    )


def create_navbar(data):
    """Create the main application navbar"""
    return dmc.AppShellNavbar(
        children=create_content(data, variant="desktop"),
        style={"borderRight": "1px solid var(--mantine-color-gray-3)"}
    )


def create_navbar_drawer(data):
    """Mobile navigation: a solid, full-height side panel.

    Runs from the bottom of the fixed header to the bottom of the viewport —
    no floating card, no close-button header row. The hamburger toggles it and
    the header stays visible (and tappable) above the overlay.
    """
    return dmc.Drawer(
        id="components-navbar-drawer",
        overlayProps={"opacity": 0.55, "blur": 3},
        zIndex=1500,
        withCloseButton=False,  # removes the whole Drawer header row
        # Always in the DOM (1.6.39): the mobile nav must not depend on a
        # mount-on-open transition — measured on the wire, `opened` flipped
        # true while the content never mounted in an unfocused window — and
        # the Admin callback's mobile target (#navbar-admin-mobile) has to
        # exist on every page load, not only after the first open.
        keepMounted=True,
        size="300px",
        padding=0,
        children=create_mobile_content(data),
        trapFocus=False,
        position="left",
        styles={
            # Dock below the fixed header. dvh (not vh) so a collapsing mobile
            # URL bar doesn't leave a dead gap at the bottom.
            "inner": {
                "top": HEADER_HEIGHT,
                "height": f"calc(100dvh - {HEADER_HEIGHT}px)",
            },
            # Overlay starts below the header too, keeping the hamburger tappable.
            "overlay": {"top": HEADER_HEIGHT},
            # Solid panel: fill the inner, square corners.
            "content": {
                "height": "100%",
                "maxHeight": "100%",
                "borderRadius": 0,
                "display": "flex",
                "flexDirection": "column",
            },
            # Definite height so create_content's ScrollArea can actually scroll.
            "body": {"flex": 1, "minHeight": 0, "height": "100%", "padding": 0},
        },
    )
