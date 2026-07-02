"""
Example 20: Context Menu with Liquid Glass Styling
===================================================
This example demonstrates:
- Right-click context menu on the canvas
- Submenus for adding nodes (Input, Process, Output, Resizable)
- Submenus for edge types (Bezier, Straight, Step, SmoothStep)
- Theme preset selection (Glass, Solid, Minimal)
- Color mode toggle (Light, Dark, System)
- Color scheme selection (Default, Ocean, Forest, Sunset, Midnight, Rose)
- Dynamic node/edge creation
- Liquid glass morphism styling for menus
"""

import dash
from dash import html, callback, Input, Output, State, ctx, dcc
from dash.exceptions import PreventUpdate
import dash_flows
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import uuid

app = dash.Dash(
    __name__,
    assets_folder="assets",
    suppress_callback_exceptions=True
)

# Initial empty state
initial_nodes = []
initial_edges = []


def create_node_submenu():
    """Create the nodes submenu with node type options."""
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
                    id="add-input-node",
                    leftSection=html.Div("+", className="node-type-icon node-input-icon"),
                    rightSection=dmc.Text("Source", size="xs", c="dimmed"),
                ),
                dmc.MenuItem(
                    "Process Node",
                    id="add-process-node",
                    leftSection=html.Div("⚙", className="node-type-icon node-process-icon"),
                    rightSection=dmc.Text("Transform", size="xs", c="dimmed"),
                ),
                dmc.MenuItem(
                    "Output Node",
                    id="add-output-node",
                    leftSection=html.Div("→", className="node-type-icon node-output-icon"),
                    rightSection=dmc.Text("Sink", size="xs", c="dimmed"),
                ),
                dmc.MenuDivider(),
                dmc.MenuItem(
                    "Resizable Node",
                    id="add-resizable-node",
                    leftSection=html.Div("⤢", className="node-type-icon node-resizable-icon"),
                    rightSection=dmc.Text("Custom", size="xs", c="dimmed"),
                ),
            ]
        ),
    ])


def create_edge_submenu():
    """Create the edges submenu with edge type options."""
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
                    id="edge-bezier",
                    leftSection=DashIconify(icon="tabler:vector-bezier-2", width=18),
                ),
                dmc.MenuItem(
                    "Straight",
                    id="edge-straight",
                    leftSection=DashIconify(icon="tabler:line", width=18),
                ),
                dmc.MenuItem(
                    "Step",
                    id="edge-step",
                    leftSection=DashIconify(icon="tabler:stairs", width=18),
                ),
                dmc.MenuItem(
                    "Smooth Step",
                    id="edge-smoothstep",
                    leftSection=DashIconify(icon="tabler:corner-down-right", width=18),
                ),
                dmc.MenuDivider(),
                dmc.MenuItem(
                    "Animated",
                    id="edge-animated",
                    leftSection=DashIconify(icon="tabler:bolt", width=18, color="orange"),
                ),
            ]
        ),
    ])


def create_theme_preset_submenu():
    """Create the theme preset submenu."""
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
                    id="preset-glass",
                    leftSection=html.Div(className="preset-indicator preset-glass"),
                    rightSection=dmc.Text("Blur effect", size="xs", c="dimmed"),
                ),
                dmc.MenuItem(
                    "Solid",
                    id="preset-solid",
                    leftSection=html.Div(className="preset-indicator preset-solid"),
                    rightSection=dmc.Text("Opaque", size="xs", c="dimmed"),
                ),
                dmc.MenuItem(
                    "Minimal",
                    id="preset-minimal",
                    leftSection=html.Div(className="preset-indicator preset-minimal"),
                    rightSection=dmc.Text("Clean", size="xs", c="dimmed"),
                ),
            ]
        ),
    ])


def create_color_mode_submenu():
    """Create the color mode submenu."""
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
                    id="mode-light",
                    leftSection=DashIconify(icon="tabler:sun", width=18, color="#f59e0b"),
                ),
                dmc.MenuItem(
                    "Dark",
                    id="mode-dark",
                    leftSection=DashIconify(icon="tabler:moon", width=18, color="#6366f1"),
                ),
                dmc.MenuItem(
                    "System",
                    id="mode-system",
                    leftSection=DashIconify(icon="tabler:device-desktop", width=18),
                ),
            ]
        ),
    ])


def create_color_scheme_submenu():
    """Create the color scheme submenu."""
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
                    id="scheme-default",
                    leftSection=html.Div(className="color-scheme-swatch swatch-default"),
                ),
                dmc.MenuItem(
                    "Ocean",
                    id="scheme-ocean",
                    leftSection=html.Div(className="color-scheme-swatch swatch-ocean"),
                ),
                dmc.MenuItem(
                    "Forest",
                    id="scheme-forest",
                    leftSection=html.Div(className="color-scheme-swatch swatch-forest"),
                ),
                dmc.MenuItem(
                    "Sunset",
                    id="scheme-sunset",
                    leftSection=html.Div(className="color-scheme-swatch swatch-sunset"),
                ),
                dmc.MenuItem(
                    "Midnight",
                    id="scheme-midnight",
                    leftSection=html.Div(className="color-scheme-swatch swatch-midnight"),
                ),
                dmc.MenuItem(
                    "Rose",
                    id="scheme-rose",
                    leftSection=html.Div(className="color-scheme-swatch swatch-rose"),
                ),
            ]
        ),
    ])


def create_context_menu():
    """Create the full context menu structure."""
    return dmc.Menu(
        id="context-menu",
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
                    id="context-menu-trigger",
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
                        id="action-fit-view",
                        leftSection=DashIconify(icon="tabler:arrows-maximize", width=18),
                    ),
                    dmc.MenuItem(
                        "Clear Canvas",
                        id="action-clear",
                        leftSection=DashIconify(icon="tabler:trash", width=18),
                        color="red",
                    ),
                ]
            ),
        ],
    )


def create_status_bar():
    """Create a status bar showing current settings."""
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
                dmc.Text(id="node-count", size="sm", children="Nodes: 0"),
            ]),
            dmc.Divider(orientation="vertical", size="sm"),
            dmc.Group(gap="xs", children=[
                DashIconify(icon="tabler:line", width=14),
                dmc.Text(id="edge-count", size="sm", children="Edges: 0"),
            ]),
            dmc.Divider(orientation="vertical", size="sm"),
            dmc.Group(gap="xs", children=[
                DashIconify(icon="tabler:palette", width=14),
                dmc.Text(id="current-preset", size="sm", children="glass"),
            ]),
            dmc.Divider(orientation="vertical", size="sm"),
            dmc.Group(gap="xs", children=[
                DashIconify(icon="tabler:color-swatch", width=14),
                dmc.Text(id="current-scheme", size="sm", children="default"),
            ]),
        ]
    )


def create_help_tooltip():
    """Create a help tooltip."""
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


app.layout = dmc.MantineProvider(
    id="mantine-provider",
    forceColorScheme="light",
    children=[
        # Stores for state management
        dcc.Store(id="menu-position", data={"x": 0, "y": 0}),
        dcc.Store(id="current-edge-type", data="smoothstep"),
        dcc.Store(id="edge-animated-state", data=False),
        dcc.Store(id="last-node-clicks", data={"input": 0, "process": 0, "output": 0, "resizable": 0}),

        html.Div(
            style={"position": "relative", "height": "100vh", "width": "100%"},
            children=[
                # Context menu (positioned via callback)
                html.Div(
                    id="context-menu-container",
                    className="context-menu-container",
                    style={"position": "fixed", "left": 0, "top": 0},
                    children=[create_context_menu()],
                ),

                # Help tooltip
                create_help_tooltip(),

                # Status bar
                create_status_bar(),

                # DashFlows component
                dash_flows.DashFlows(
                    id="flow",
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
                    style={"height": "100vh", "width": "100%"},
                ),
            ],
        ),
    ],
)


# Callback to handle right-click and show context menu
@callback(
    [Output("context-menu", "opened"),
     Output("context-menu-container", "style"),
     Output("menu-position", "data")],
    [Input("flow", "paneContextMenu")],
    prevent_initial_call=True,
)
def show_context_menu(context_menu):
    """Show context menu at right-click position."""
    if not context_menu:
        raise PreventUpdate

    x = context_menu.get("clientX", 0)
    y = context_menu.get("clientY", 0)

    return (
        True,
        {"position": "fixed", "left": x, "top": y, "zIndex": 9999},
        {"x": x, "y": y}
    )


# Callback to close menu on pane click
@callback(
    Output("context-menu", "opened", allow_duplicate=True),
    Input("flow", "paneClickPosition"),
    prevent_initial_call=True,
)
def close_menu_on_click(pane_click):
    """Close context menu when clicking on the pane."""
    return False


# Callback to add nodes
@callback(
    [Output("flow", "nodes"),
     Output("context-menu", "opened", allow_duplicate=True),
     Output("last-node-clicks", "data")],
    [Input("add-input-node", "n_clicks"),
     Input("add-process-node", "n_clicks"),
     Input("add-output-node", "n_clicks"),
     Input("add-resizable-node", "n_clicks")],
    [State("flow", "nodes"),
     State("menu-position", "data"),
     State("flow", "viewport"),
     State("last-node-clicks", "data")],
    prevent_initial_call=True,
)
def add_node(n1, n2, n3, n4, current_nodes, menu_pos, viewport, last_clicks):
    """Add a new node at the context menu position."""
    # Check which input actually triggered the callback
    if not ctx.triggered:
        raise PreventUpdate

    # Get the prop_id that triggered this callback
    triggered_prop = ctx.triggered[0]["prop_id"]
    triggered_value = ctx.triggered[0]["value"]

    # Only proceed if there was an actual click (value > 0)
    if not triggered_value:
        raise PreventUpdate

    # Extract the component id from prop_id (format: "component-id.property")
    triggered = triggered_prop.split(".")[0]

    # Map trigger to node type and last_clicks key
    node_types = {
        "add-input-node": ("input", "Input", "input"),
        "add-process-node": ("default", "Process", "process"),
        "add-output-node": ("output", "Output", "output"),
        "add-resizable-node": ("resizable", "Resizable", "resizable"),
    }

    if triggered not in node_types:
        raise PreventUpdate

    node_type, label, click_key = node_types[triggered]

    # Check if this is a new click by comparing with last stored value
    current_click = triggered_value or 0
    last_click = last_clicks.get(click_key, 0) if last_clicks else 0

    if current_click <= last_click:
        raise PreventUpdate

    # Update the last clicks store
    new_last_clicks = last_clicks.copy() if last_clicks else {"input": 0, "process": 0, "output": 0, "resizable": 0}
    new_last_clicks[click_key] = current_click

    # Calculate position in flow coordinates
    # Account for viewport transform
    zoom = viewport.get("zoom", 1) if viewport else 1
    vp_x = viewport.get("x", 0) if viewport else 0
    vp_y = viewport.get("y", 0) if viewport else 0

    x = (menu_pos["x"] - vp_x) / zoom
    y = (menu_pos["y"] - vp_y) / zoom

    # Generate unique ID
    node_id = f"{node_type}-{str(uuid.uuid4())[:8]}"

    # Create new node
    new_node = {
        "id": node_id,
        "type": node_type,
        "data": {
            "label": f"{label} {len(current_nodes) + 1 if current_nodes else 1}",
            "sublabel": f"Created at ({int(x)}, {int(y)})",
        },
        "position": {"x": x, "y": y},
    }

    # Add resizable-specific properties
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
    [Output("current-edge-type", "data"),
     Output("edge-animated-state", "data"),
     Output("flow", "defaultEdgeOptions"),
     Output("context-menu", "opened", allow_duplicate=True)],
    [Input("edge-bezier", "n_clicks"),
     Input("edge-straight", "n_clicks"),
     Input("edge-step", "n_clicks"),
     Input("edge-smoothstep", "n_clicks"),
     Input("edge-animated", "n_clicks")],
    [State("current-edge-type", "data"),
     State("edge-animated-state", "data")],
    prevent_initial_call=True,
)
def set_edge_type(n1, n2, n3, n4, n5, current_type, is_animated):
    """Set the default edge type for new connections."""
    if not ctx.triggered_id:
        raise PreventUpdate

    triggered = ctx.triggered_id

    edge_types = {
        "edge-bezier": "default",
        "edge-straight": "straight",
        "edge-step": "step",
        "edge-smoothstep": "smoothstep",
    }

    new_type = current_type
    new_animated = is_animated

    if triggered == "edge-animated":
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
    [Output("flow", "themePreset"),
     Output("current-preset", "children"),
     Output("context-menu", "opened", allow_duplicate=True)],
    [Input("preset-glass", "n_clicks"),
     Input("preset-solid", "n_clicks"),
     Input("preset-minimal", "n_clicks")],
    prevent_initial_call=True,
)
def set_theme_preset(n1, n2, n3):
    """Set the theme preset."""
    if not ctx.triggered_id:
        raise PreventUpdate

    presets = {
        "preset-glass": "glass",
        "preset-solid": "solid",
        "preset-minimal": "minimal",
    }

    preset = presets.get(ctx.triggered_id, "glass")
    return preset, preset, False


# Callback to handle color mode selection
@callback(
    [Output("flow", "colorMode"),
     Output("mantine-provider", "forceColorScheme"),
     Output("context-menu", "opened", allow_duplicate=True)],
    [Input("mode-light", "n_clicks"),
     Input("mode-dark", "n_clicks"),
     Input("mode-system", "n_clicks")],
    prevent_initial_call=True,
)
def set_color_mode(n1, n2, n3):
    """Set the color mode."""
    if not ctx.triggered_id:
        raise PreventUpdate

    modes = {
        "mode-light": "light",
        "mode-dark": "dark",
        "mode-system": "system",
    }

    mode = modes.get(ctx.triggered_id, "light")
    mantine_scheme = None if mode == "system" else mode

    return mode, mantine_scheme, False


# Callback to handle color scheme selection
@callback(
    [Output("flow", "colorScheme"),
     Output("current-scheme", "children"),
     Output("context-menu", "opened", allow_duplicate=True)],
    [Input("scheme-default", "n_clicks"),
     Input("scheme-ocean", "n_clicks"),
     Input("scheme-forest", "n_clicks"),
     Input("scheme-sunset", "n_clicks"),
     Input("scheme-midnight", "n_clicks"),
     Input("scheme-rose", "n_clicks")],
    prevent_initial_call=True,
)
def set_color_scheme(n1, n2, n3, n4, n5, n6):
    """Set the color scheme."""
    if not ctx.triggered_id:
        raise PreventUpdate

    schemes = {
        "scheme-default": "default",
        "scheme-ocean": "ocean",
        "scheme-forest": "forest",
        "scheme-sunset": "sunset",
        "scheme-midnight": "midnight",
        "scheme-rose": "rose",
    }

    scheme = schemes.get(ctx.triggered_id, "default")
    return scheme, scheme, False


# Callback to handle fit view action
@callback(
    [Output("flow", "viewportAction"),
     Output("context-menu", "opened", allow_duplicate=True)],
    Input("action-fit-view", "n_clicks"),
    prevent_initial_call=True,
)
def fit_view(n_clicks):
    """Trigger fit view action."""
    if not n_clicks:
        raise PreventUpdate

    # Use viewportAction to trigger fitView
    return {"action": "fitView", "options": {"padding": 0.2, "duration": 500}}, False


# Callback to clear all nodes and edges
@callback(
    [Output("flow", "nodes", allow_duplicate=True),
     Output("flow", "edges"),
     Output("context-menu", "opened", allow_duplicate=True)],
    Input("action-clear", "n_clicks"),
    prevent_initial_call=True,
)
def clear_canvas(n_clicks):
    """Clear all nodes and edges from the canvas."""
    if not n_clicks:
        raise PreventUpdate

    return [], [], False


# Callback to update status bar counts
@callback(
    [Output("node-count", "children"),
     Output("edge-count", "children")],
    [Input("flow", "nodes"),
     Input("flow", "edges")],
)
def update_counts(nodes, edges):
    """Update the node and edge counts in the status bar."""
    node_count = len(nodes) if nodes else 0
    edge_count = len(edges) if edges else 0

    return f"Nodes: {node_count}", f"Edges: {edge_count}"


if __name__ == "__main__":
    app.run(debug=True, port=8020)