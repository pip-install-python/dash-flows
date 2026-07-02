"""
Embeddable twin of examples/20_context_menu.py for the docs page.
Rendered via `.. exec::docs.interactions.ex20`.

Trimmed for the docs canvas: the full example also syncs the page-level
Mantine color scheme to the "Color Mode" submenu and runs full-viewport
(100vh); here the canvas is a fixed height and the color-mode submenu only
affects the DashFlows canvas itself. See examples/20_context_menu.py for the
complete, page-level version.
"""
import uuid

from dash import html, callback, Input, Output, State, ctx, dcc
from dash.exceptions import PreventUpdate
import dash_flows
import dash_mantine_components as dmc
from dash_iconify import DashIconify

initial_nodes = []
initial_edges = []


def create_node_submenu():
    return dmc.SubMenu([
        dmc.SubMenuTarget(
            dmc.SubMenuItem(
                "Add Node",
                leftSection=DashIconify(icon="tabler:square-plus", width=18),
            )
        ),
        dmc.SubMenuDropdown(
            className="glass-morphism-menu",
            children=[
                dmc.MenuItem(
                    "Input Node",
                    id="ex20-add-input-node",
                    leftSection=html.Div("+", className="node-type-icon node-input-icon"),
                    rightSection=dmc.Text("Source", size="xs", c="dimmed"),
                ),
                dmc.MenuItem(
                    "Process Node",
                    id="ex20-add-process-node",
                    leftSection=html.Div("⚙", className="node-type-icon node-process-icon"),
                    rightSection=dmc.Text("Transform", size="xs", c="dimmed"),
                ),
                dmc.MenuItem(
                    "Output Node",
                    id="ex20-add-output-node",
                    leftSection=html.Div("→", className="node-type-icon node-output-icon"),
                    rightSection=dmc.Text("Sink", size="xs", c="dimmed"),
                ),
                dmc.MenuDivider(),
                dmc.MenuItem(
                    "Resizable Node",
                    id="ex20-add-resizable-node",
                    leftSection=html.Div("⤢", className="node-type-icon node-resizable-icon"),
                    rightSection=dmc.Text("Custom", size="xs", c="dimmed"),
                ),
            ]
        ),
    ])


def create_edge_submenu():
    return dmc.SubMenu([
        dmc.SubMenuTarget(
            dmc.SubMenuItem(
                "Edge Type",
                leftSection=DashIconify(icon="tabler:line", width=18),
            )
        ),
        dmc.SubMenuDropdown(
            className="glass-morphism-menu",
            children=[
                dmc.MenuItem(
                    "Bezier",
                    id="ex20-edge-bezier",
                    leftSection=DashIconify(icon="tabler:vector-bezier-2", width=18),
                ),
                dmc.MenuItem(
                    "Straight",
                    id="ex20-edge-straight",
                    leftSection=DashIconify(icon="tabler:line", width=18),
                ),
                dmc.MenuItem(
                    "Step",
                    id="ex20-edge-step",
                    leftSection=DashIconify(icon="tabler:stairs", width=18),
                ),
                dmc.MenuItem(
                    "Smooth Step",
                    id="ex20-edge-smoothstep",
                    leftSection=DashIconify(icon="tabler:corner-down-right", width=18),
                ),
                dmc.MenuDivider(),
                dmc.MenuItem(
                    "Animated",
                    id="ex20-edge-animated",
                    leftSection=DashIconify(icon="tabler:bolt", width=18, color="orange"),
                ),
            ]
        ),
    ])


def create_theme_preset_submenu():
    return dmc.SubMenu([
        dmc.SubMenuTarget(
            dmc.SubMenuItem(
                "Theme Preset",
                leftSection=DashIconify(icon="tabler:palette", width=18),
            )
        ),
        dmc.SubMenuDropdown(
            className="glass-morphism-menu",
            children=[
                dmc.MenuItem(
                    "Glass",
                    id="ex20-preset-glass",
                    leftSection=html.Div(className="preset-indicator preset-glass"),
                    rightSection=dmc.Text("Blur effect", size="xs", c="dimmed"),
                ),
                dmc.MenuItem(
                    "Solid",
                    id="ex20-preset-solid",
                    leftSection=html.Div(className="preset-indicator preset-solid"),
                    rightSection=dmc.Text("Opaque", size="xs", c="dimmed"),
                ),
                dmc.MenuItem(
                    "Minimal",
                    id="ex20-preset-minimal",
                    leftSection=html.Div(className="preset-indicator preset-minimal"),
                    rightSection=dmc.Text("Clean", size="xs", c="dimmed"),
                ),
            ]
        ),
    ])


def create_color_mode_submenu():
    return dmc.SubMenu([
        dmc.SubMenuTarget(
            dmc.SubMenuItem(
                "Color Mode",
                leftSection=DashIconify(icon="tabler:sun-moon", width=18),
            )
        ),
        dmc.SubMenuDropdown(
            className="glass-morphism-menu",
            children=[
                dmc.MenuItem(
                    "Light",
                    id="ex20-mode-light",
                    leftSection=DashIconify(icon="tabler:sun", width=18, color="#f59e0b"),
                ),
                dmc.MenuItem(
                    "Dark",
                    id="ex20-mode-dark",
                    leftSection=DashIconify(icon="tabler:moon", width=18, color="#6366f1"),
                ),
                dmc.MenuItem(
                    "System",
                    id="ex20-mode-system",
                    leftSection=DashIconify(icon="tabler:device-desktop", width=18),
                ),
            ]
        ),
    ])


def create_color_scheme_submenu():
    return dmc.SubMenu([
        dmc.SubMenuTarget(
            dmc.SubMenuItem(
                "Color Scheme",
                leftSection=DashIconify(icon="tabler:color-swatch", width=18),
            )
        ),
        dmc.SubMenuDropdown(
            className="glass-morphism-menu",
            children=[
                dmc.MenuItem(
                    "Default",
                    id="ex20-scheme-default",
                    leftSection=html.Div(className="color-scheme-swatch swatch-default"),
                ),
                dmc.MenuItem(
                    "Ocean",
                    id="ex20-scheme-ocean",
                    leftSection=html.Div(className="color-scheme-swatch swatch-ocean"),
                ),
                dmc.MenuItem(
                    "Forest",
                    id="ex20-scheme-forest",
                    leftSection=html.Div(className="color-scheme-swatch swatch-forest"),
                ),
                dmc.MenuItem(
                    "Sunset",
                    id="ex20-scheme-sunset",
                    leftSection=html.Div(className="color-scheme-swatch swatch-sunset"),
                ),
                dmc.MenuItem(
                    "Midnight",
                    id="ex20-scheme-midnight",
                    leftSection=html.Div(className="color-scheme-swatch swatch-midnight"),
                ),
                dmc.MenuItem(
                    "Rose",
                    id="ex20-scheme-rose",
                    leftSection=html.Div(className="color-scheme-swatch swatch-rose"),
                ),
            ]
        ),
    ])


def create_context_menu():
    return dmc.Menu(
        id="ex20-context-menu",
        opened=False,
        position="bottom-start",
        offset=0,
        withArrow=False,
        shadow="lg",
        width=220,
        zIndex=9999,
        closeOnClickOutside=True,
        closeOnEscape=True,
        children=[
            dmc.MenuTarget(
                html.Div(
                    id="ex20-context-menu-trigger",
                    className="context-menu-trigger",
                )
            ),
            dmc.MenuDropdown(
                className="glass-morphism-menu",
                children=[
                    dmc.MenuLabel("Nodes"),
                    create_node_submenu(),
                    dmc.MenuDivider(),
                    dmc.MenuLabel("Connections"),
                    create_edge_submenu(),
                    dmc.MenuDivider(),
                    dmc.MenuLabel("Appearance"),
                    create_theme_preset_submenu(),
                    create_color_mode_submenu(),
                    create_color_scheme_submenu(),
                    dmc.MenuDivider(),
                    dmc.MenuItem(
                        "Fit View",
                        id="ex20-action-fit-view",
                        leftSection=DashIconify(icon="tabler:arrows-maximize", width=18),
                    ),
                    dmc.MenuItem(
                        "Clear Canvas",
                        id="ex20-action-clear",
                        leftSection=DashIconify(icon="tabler:trash", width=18),
                        color="red",
                    ),
                ]
            ),
        ],
    )


def create_status_bar():
    return dmc.Group(
        className="status-bar",
        p="xs",
        gap="md",
        style={
            "position": "absolute",
            "bottom": 16,
            "left": 16,
            "zIndex": 100,
        },
        children=[
            dmc.Group(gap="xs", children=[
                DashIconify(icon="tabler:box", width=14),
                dmc.Text(id="ex20-node-count", size="sm", children="Nodes: 0"),
            ]),
            dmc.Divider(orientation="vertical", size="sm"),
            dmc.Group(gap="xs", children=[
                DashIconify(icon="tabler:line", width=14),
                dmc.Text(id="ex20-edge-count", size="sm", children="Edges: 0"),
            ]),
            dmc.Divider(orientation="vertical", size="sm"),
            dmc.Group(gap="xs", children=[
                DashIconify(icon="tabler:palette", width=14),
                dmc.Text(id="ex20-current-preset", size="sm", children="glass"),
            ]),
            dmc.Divider(orientation="vertical", size="sm"),
            dmc.Group(gap="xs", children=[
                DashIconify(icon="tabler:color-swatch", width=14),
                dmc.Text(id="ex20-current-scheme", size="sm", children="default"),
            ]),
        ]
    )


def create_help_tooltip():
    return dmc.Paper(
        className="status-bar",
        p="sm",
        style={
            "position": "absolute",
            "top": 16,
            "left": 16,
            "zIndex": 100,
            "maxWidth": 280,
        },
        children=[
            dmc.Group(gap="xs", mb="xs", children=[
                DashIconify(icon="tabler:info-circle", width=18, color="blue"),
                dmc.Text("Right-Click Context Menu", fw=600, size="sm"),
            ]),
            dmc.Text(
                "Right-click anywhere on the canvas to open the context menu. "
                "Add nodes, change themes, and customize your flow.",
                size="xs",
                c="dimmed",
            ),
        ]
    )


component = html.Div([
    # Stores for state management
    dcc.Store(id="ex20-menu-position", data={"x": 0, "y": 0}),
    dcc.Store(id="ex20-current-edge-type", data="smoothstep"),
    dcc.Store(id="ex20-edge-animated-state", data=False),
    dcc.Store(id="ex20-last-node-clicks", data={"input": 0, "process": 0, "output": 0, "resizable": 0}),

    html.Div(
        style={"position": "relative", "height": "480px", "width": "100%"},
        children=[
            # Context menu (positioned via callback)
            html.Div(
                id="ex20-context-menu-container",
                className="context-menu-container",
                style={"position": "fixed", "left": 0, "top": 0},
                children=[create_context_menu()],
            ),

            create_help_tooltip(),
            create_status_bar(),

            dash_flows.DashFlows(
                id="ex20-flow",
                nodes=initial_nodes,
                edges=initial_edges,
                colorMode="light",
                themePreset="glass",
                colorScheme="default",
                theme={
                    "glassBlur": 12,
                    "borderRadius": 14,
                    "edgeStrokeWidth": 2,
                },
                showMiniMap=True,
                showControls=True,
                showBackground=True,
                fitView=True,
                fitViewOptions={"padding": 0.2},
                defaultEdgeOptions={
                    "type": "smoothstep",
                    "animated": False,
                },
                style={
                    "height": "480px",
                    "width": "100%",
                    "border": "1px solid var(--mantine-color-default-border)",
                    "borderRadius": "8px",
                },
            ),
        ],
    ),

    dmc.Space(h=10),

    dmc.Paper([
        dmc.Text("Last pane context-menu event:", fw=600, size="sm"),
        html.Pre(id="ex20-context-menu-log", children="Right-click the canvas...",
                  style={"fontSize": "11px", "maxHeight": "100px", "overflow": "auto"}),
    ], p="sm", withBorder=True),
])


# Callback to handle right-click and show context menu
@callback(
    [Output("ex20-context-menu", "opened"),
     Output("ex20-context-menu-container", "style"),
     Output("ex20-menu-position", "data"),
     Output("ex20-context-menu-log", "children")],
    [Input("ex20-flow", "paneContextMenu")],
    prevent_initial_call=True,
)
def show_context_menu(context_menu):
    """Show context menu at right-click position."""
    if not context_menu:
        raise PreventUpdate

    x = context_menu.get("clientX", 0)
    y = context_menu.get("clientY", 0)

    import json
    return (
        True,
        {"position": "fixed", "left": x, "top": y, "zIndex": 9999},
        {"x": x, "y": y},
        json.dumps(context_menu, indent=2),
    )


# Callback to close menu on pane click
@callback(
    Output("ex20-context-menu", "opened", allow_duplicate=True),
    Input("ex20-flow", "paneClickPosition"),
    prevent_initial_call=True,
)
def close_menu_on_click(pane_click):
    """Close context menu when clicking on the pane."""
    return False


# Callback to add nodes
@callback(
    [Output("ex20-flow", "nodes"),
     Output("ex20-context-menu", "opened", allow_duplicate=True),
     Output("ex20-last-node-clicks", "data")],
    [Input("ex20-add-input-node", "n_clicks"),
     Input("ex20-add-process-node", "n_clicks"),
     Input("ex20-add-output-node", "n_clicks"),
     Input("ex20-add-resizable-node", "n_clicks")],
    [State("ex20-flow", "nodes"),
     State("ex20-menu-position", "data"),
     State("ex20-flow", "viewport"),
     State("ex20-last-node-clicks", "data")],
    prevent_initial_call=True,
)
def add_node(n1, n2, n3, n4, current_nodes, menu_pos, viewport, last_clicks):
    """Add a new node at the context menu position."""
    if not ctx.triggered:
        raise PreventUpdate

    triggered_prop = ctx.triggered[0]["prop_id"]
    triggered_value = ctx.triggered[0]["value"]

    if not triggered_value:
        raise PreventUpdate

    triggered = triggered_prop.split(".")[0]

    node_types = {
        "ex20-add-input-node": ("input", "Input", "input"),
        "ex20-add-process-node": ("default", "Process", "process"),
        "ex20-add-output-node": ("output", "Output", "output"),
        "ex20-add-resizable-node": ("resizable", "Resizable", "resizable"),
    }

    if triggered not in node_types:
        raise PreventUpdate

    node_type, label, click_key = node_types[triggered]

    current_click = triggered_value or 0
    last_click = last_clicks.get(click_key, 0) if last_clicks else 0

    if current_click <= last_click:
        raise PreventUpdate

    new_last_clicks = last_clicks.copy() if last_clicks else {"input": 0, "process": 0, "output": 0, "resizable": 0}
    new_last_clicks[click_key] = current_click

    zoom = viewport.get("zoom", 1) if viewport else 1
    vp_x = viewport.get("x", 0) if viewport else 0
    vp_y = viewport.get("y", 0) if viewport else 0

    x = (menu_pos["x"] - vp_x) / zoom
    y = (menu_pos["y"] - vp_y) / zoom

    node_id = f"{node_type}-{str(uuid.uuid4())[:8]}"

    new_node = {
        "id": node_id,
        "type": node_type,
        "data": {
            "label": f"{label} {len(current_nodes) + 1 if current_nodes else 1}",
            "sublabel": f"Created at ({int(x)}, {int(y)})",
        },
        "position": {"x": x, "y": y},
    }

    if node_type == "resizable":
        new_node["data"]["handles"] = [
            {"id": "top", "type": "target", "position": "top"},
            {"id": "bottom", "type": "source", "position": "bottom"},
        ]
        new_node["style"] = {"width": 180, "height": 100}

    updated_nodes = (current_nodes or []) + [new_node]

    return updated_nodes, False, new_last_clicks


# Callback to handle edge type selection
@callback(
    [Output("ex20-current-edge-type", "data"),
     Output("ex20-edge-animated-state", "data"),
     Output("ex20-flow", "defaultEdgeOptions"),
     Output("ex20-context-menu", "opened", allow_duplicate=True)],
    [Input("ex20-edge-bezier", "n_clicks"),
     Input("ex20-edge-straight", "n_clicks"),
     Input("ex20-edge-step", "n_clicks"),
     Input("ex20-edge-smoothstep", "n_clicks"),
     Input("ex20-edge-animated", "n_clicks")],
    [State("ex20-current-edge-type", "data"),
     State("ex20-edge-animated-state", "data")],
    prevent_initial_call=True,
)
def set_edge_type(n1, n2, n3, n4, n5, current_type, is_animated):
    """Set the default edge type for new connections."""
    if not ctx.triggered_id:
        raise PreventUpdate

    triggered = ctx.triggered_id

    edge_types = {
        "ex20-edge-bezier": "default",
        "ex20-edge-straight": "straight",
        "ex20-edge-step": "step",
        "ex20-edge-smoothstep": "smoothstep",
    }

    new_type = current_type
    new_animated = is_animated

    if triggered == "ex20-edge-animated":
        new_animated = not is_animated
    elif triggered in edge_types:
        new_type = edge_types[triggered]

    default_options = {
        "type": new_type,
        "animated": new_animated,
    }

    return new_type, new_animated, default_options, False


# Callback to handle theme preset selection
@callback(
    [Output("ex20-flow", "themePreset"),
     Output("ex20-current-preset", "children"),
     Output("ex20-context-menu", "opened", allow_duplicate=True)],
    [Input("ex20-preset-glass", "n_clicks"),
     Input("ex20-preset-solid", "n_clicks"),
     Input("ex20-preset-minimal", "n_clicks")],
    prevent_initial_call=True,
)
def set_theme_preset(n1, n2, n3):
    """Set the theme preset."""
    if not ctx.triggered_id:
        raise PreventUpdate

    presets = {
        "ex20-preset-glass": "glass",
        "ex20-preset-solid": "solid",
        "ex20-preset-minimal": "minimal",
    }

    preset = presets.get(ctx.triggered_id, "glass")
    return preset, preset, False


# Callback to handle color mode selection (scoped to the canvas only in this demo)
@callback(
    [Output("ex20-flow", "colorMode"),
     Output("ex20-context-menu", "opened", allow_duplicate=True)],
    [Input("ex20-mode-light", "n_clicks"),
     Input("ex20-mode-dark", "n_clicks"),
     Input("ex20-mode-system", "n_clicks")],
    prevent_initial_call=True,
)
def set_color_mode(n1, n2, n3):
    """Set the color mode."""
    if not ctx.triggered_id:
        raise PreventUpdate

    modes = {
        "ex20-mode-light": "light",
        "ex20-mode-dark": "dark",
        "ex20-mode-system": "system",
    }

    mode = modes.get(ctx.triggered_id, "light")
    return mode, False


# Callback to handle color scheme selection
@callback(
    [Output("ex20-flow", "colorScheme"),
     Output("ex20-current-scheme", "children"),
     Output("ex20-context-menu", "opened", allow_duplicate=True)],
    [Input("ex20-scheme-default", "n_clicks"),
     Input("ex20-scheme-ocean", "n_clicks"),
     Input("ex20-scheme-forest", "n_clicks"),
     Input("ex20-scheme-sunset", "n_clicks"),
     Input("ex20-scheme-midnight", "n_clicks"),
     Input("ex20-scheme-rose", "n_clicks")],
    prevent_initial_call=True,
)
def set_color_scheme(n1, n2, n3, n4, n5, n6):
    """Set the color scheme."""
    if not ctx.triggered_id:
        raise PreventUpdate

    schemes = {
        "ex20-scheme-default": "default",
        "ex20-scheme-ocean": "ocean",
        "ex20-scheme-forest": "forest",
        "ex20-scheme-sunset": "sunset",
        "ex20-scheme-midnight": "midnight",
        "ex20-scheme-rose": "rose",
    }

    scheme = schemes.get(ctx.triggered_id, "default")
    return scheme, scheme, False


# Callback to handle fit view action
@callback(
    [Output("ex20-flow", "viewportAction"),
     Output("ex20-context-menu", "opened", allow_duplicate=True)],
    Input("ex20-action-fit-view", "n_clicks"),
    prevent_initial_call=True,
)
def fit_view(n_clicks):
    """Trigger fit view action."""
    if not n_clicks:
        raise PreventUpdate

    return {"action": "fitView", "options": {"padding": 0.2, "duration": 500}}, False


# Callback to clear all nodes and edges
@callback(
    [Output("ex20-flow", "nodes", allow_duplicate=True),
     Output("ex20-flow", "edges"),
     Output("ex20-context-menu", "opened", allow_duplicate=True)],
    Input("ex20-action-clear", "n_clicks"),
    prevent_initial_call=True,
)
def clear_canvas(n_clicks):
    """Clear all nodes and edges from the canvas."""
    if not n_clicks:
        raise PreventUpdate

    return [], [], False


# Callback to update status bar counts
@callback(
    [Output("ex20-node-count", "children"),
     Output("ex20-edge-count", "children")],
    [Input("ex20-flow", "nodes"),
     Input("ex20-flow", "edges")],
)
def update_counts(nodes, edges):
    """Update the node and edge counts in the status bar."""
    node_count = len(nodes) if nodes else 0
    edge_count = len(edges) if edges else 0

    return f"Nodes: {node_count}", f"Edges: {edge_count}"


# Default the canvas color mode to the docs page's light/dark preference (and
# follow it when the page theme is toggled). The "Color Mode" context-menu
# submenu above still overrides this on the canvas — allow_duplicate lets both
# callbacks drive `colorMode`. The app stores the active scheme in
# `color-scheme-storage`, which also drives the page-level MantineProvider.
@callback(
    Output("ex20-flow", "colorMode", allow_duplicate=True),
    Input("color-scheme-storage", "data"),
    prevent_initial_call="initial_duplicate",
)
def sync_color_mode_to_page(scheme):
    return scheme or "light"
