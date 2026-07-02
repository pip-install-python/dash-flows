"""
Example 13: Complete Feature Showcase
=====================================
A comprehensive example combining multiple DashFlows features:
- Multiple node types with custom styling
- Various edge types
- Interactive toolbar
- Dark mode toggle
- Layout controls
- DevTools panel
"""

import dash
from dash import html, Input, Output, State, callback, clientside_callback, dcc
import dash_flows
import dash_mantine_components as dmc
import json

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Comprehensive node configuration
initial_nodes = [
    # Input nodes
    {
        "id": "input-api",
        "type": "input",
        "data": {"label": "REST API", "sublabel": "External Data"},
        "position": {"x": 50, "y": 50},
    },
    {
        "id": "input-db",
        "type": "input",
        "data": {"label": "Database", "sublabel": "PostgreSQL"},
        "position": {"x": 50, "y": 180},
    },

    # Processing nodes
    {
        "id": "process-validate",
        "type": "default",
        "data": {"label": "Validate", "sublabel": "Schema Check"},
        "position": {"x": 250, "y": 50},
    },
    {
        "id": "process-transform",
        "type": "default",
        "data": {"label": "Transform", "sublabel": "ETL Pipeline"},
        "position": {"x": 250, "y": 180},
    },
    {
        "id": "process-merge",
        "type": "toolbar",
        "data": {
            "label": "Merge Data",
            "sublabel": "Click for actions",
            "toolbarPosition": "top",
        },
        "position": {"x": 450, "y": 115},
    },

    # Group node with children
    {
        "id": "group-ml",
        "type": "group",
        "data": {"label": "ML Pipeline"},
        "position": {"x": 650, "y": 30},
        "style": {"width": 280, "height": 220},
    },
    {
        "id": "ml-train",
        "type": "default",
        "data": {"label": "Train Model"},
        "position": {"x": 30, "y": 50},
        "parentId": "group-ml",
        "extent": "parent",
    },
    {
        "id": "ml-evaluate",
        "type": "default",
        "data": {"label": "Evaluate"},
        "position": {"x": 30, "y": 130},
        "parentId": "group-ml",
        "extent": "parent",
    },

    # Output nodes
    {
        "id": "output-dashboard",
        "type": "output",
        "data": {"label": "Dashboard", "sublabel": "Visualization"},
        "position": {"x": 450, "y": 300},
    },
    {
        "id": "output-export",
        "type": "output",
        "data": {"label": "Export", "sublabel": "CSV/JSON"},
        "position": {"x": 650, "y": 300},
    },
]

initial_edges = [
    {"id": "e1", "source": "input-api", "target": "process-validate", "animated": True},
    {"id": "e2", "source": "input-db", "target": "process-transform", "type": "smoothstep"},
    {"id": "e3", "source": "process-validate", "target": "process-merge"},
    {"id": "e4", "source": "process-transform", "target": "process-merge", "type": "step"},
    {"id": "e5", "source": "process-merge", "target": "ml-train", "type": "simplebezier"},
    {"id": "e6", "source": "ml-train", "target": "ml-evaluate"},
    {"id": "e7", "source": "process-merge", "target": "output-dashboard", "type": "button", "data": {"label": "Live", "showButton": True}},
    {"id": "e8", "source": "ml-evaluate", "target": "output-export"},
]

# Layout presets
layouts = {
    "horizontal": json.dumps({
        "elk.algorithm": "layered",
        "elk.direction": "RIGHT",
        "elk.spacing.nodeNode": 60,
        "elk.layered.spacing.nodeNodeBetweenLayers": 100,
    }),
    "vertical": json.dumps({
        "elk.algorithm": "layered",
        "elk.direction": "DOWN",
        "elk.spacing.nodeNode": 60,
    }),
    "radial": json.dumps({
        "elk.algorithm": "org.eclipse.elk.radial",
        "elk.radial.radius": 180,
    }),
}

# App layout
app.layout = dmc.MantineProvider(
    id="theme-provider",
    forceColorScheme="light",
    children=[
        # Header
        dmc.Paper([
            dmc.Group([
                dmc.Title("DashFlows Complete Showcase", order=2),
                dmc.Group([
                    dmc.ActionIcon(
                        id="theme-toggle",
                        variant="subtle",
                        size="lg",
                        children=dmc.Text(id="theme-icon", size="lg"),
                    ),
                ]),
            ], justify="space-between"),
        ], p="md", mb="md", withBorder=True),

        # Controls
        dmc.Paper([
            dmc.Group([
                dmc.SegmentedControl(
                    id="layout-control",
                    data=[
                        {"value": "none", "label": "Manual"},
                        {"value": "horizontal", "label": "Horizontal"},
                        {"value": "vertical", "label": "Vertical"},
                        {"value": "radial", "label": "Radial"},
                    ],
                    value="none",
                ),
                dmc.Switch(id="show-minimap", label="MiniMap", checked=True),
                dmc.Switch(id="show-controls", label="Controls", checked=True),
                dmc.Switch(id="show-devtools", label="DevTools", checked=False),
            ], gap="lg"),
        ], p="sm", mb="md", withBorder=True),

        # Main flow area
        dmc.Grid([
            dmc.GridCol([
                html.Div(id="flow-container"),
            ], span=12 if True else 9),
        ]),

        # Info panels
        dmc.Grid([
            dmc.GridCol([
                dmc.Paper([
                    dmc.Text("Selected Items", fw=600, mb="xs"),
                    html.Div(id="selection-display"),
                ], p="md", withBorder=True),
            ], span=4),
            dmc.GridCol([
                dmc.Paper([
                    dmc.Text("Node Count", fw=600, mb="xs"),
                    html.Div(id="node-count"),
                ], p="md", withBorder=True),
            ], span=4),
            dmc.GridCol([
                dmc.Paper([
                    dmc.Text("Edge Count", fw=600, mb="xs"),
                    html.Div(id="edge-count"),
                ], p="md", withBorder=True),
            ], span=4),
        ], mt="md"),
    ],
)

# Theme toggle
clientside_callback(
    """
    function(n, scheme) {
        if (!n) return [scheme, scheme === 'dark' ? 'O' : '*'];
        const newScheme = scheme === 'light' ? 'dark' : 'light';
        return [newScheme, newScheme === 'dark' ? 'O' : '*'];
    }
    """,
    Output("theme-provider", "forceColorScheme"),
    Output("theme-icon", "children"),
    Input("theme-toggle", "n_clicks"),
    State("theme-provider", "forceColorScheme"),
    prevent_initial_call=False,
)

# Render flow with settings
@callback(
    Output("flow-container", "children"),
    Input("layout-control", "value"),
    Input("show-minimap", "checked"),
    Input("show-controls", "checked"),
    Input("show-devtools", "checked"),
)
def render_flow(layout, show_mm, show_ctrl, show_dev):
    layout_opts = layouts.get(layout) if layout != "none" else None

    return dash_flows.DashFlows(
        id="showcase-flow",
        nodes=initial_nodes,
        edges=initial_edges,
        style={"height": "500px", "borderRadius": "8px"},
        fitView=True,
        showControls=show_ctrl,
        showMiniMap=show_mm,
        showDevTools=show_dev,
        layoutOptions=layout_opts,
        backgroundVariant="dots",
        elementsSelectable=True,
        nodesConnectable=True,
        nodesDraggable=True,
    )

# Selection display
@callback(
    Output("selection-display", "children"),
    Input("showcase-flow", "selectedNodes"),
    Input("showcase-flow", "selectedEdges"),
    prevent_initial_call=True,
)
def show_selection(nodes, edges):
    # Handle various data formats
    node_ids = []
    edge_ids = []

    if nodes:
        if isinstance(nodes, list):
            for n in nodes:
                if isinstance(n, dict) and "id" in n:
                    node_ids.append(n["id"])
                elif isinstance(n, str):
                    node_ids.append(n)

    if edges:
        if isinstance(edges, list):
            for e in edges:
                if isinstance(e, dict) and "id" in e:
                    edge_ids.append(e["id"])
                elif isinstance(e, str):
                    edge_ids.append(e)

    if not node_ids and not edge_ids:
        return dmc.Text("Nothing selected", c="dimmed", size="sm")

    items = []
    if node_ids:
        items.append(dmc.Group([dmc.Badge(nid, color="blue", size="sm") for nid in node_ids], gap="xs"))
    if edge_ids:
        items.append(dmc.Group([dmc.Badge(eid, color="grape", size="sm") for eid in edge_ids], gap="xs"))

    return dmc.Stack(items, gap="xs")

# Node count
@callback(
    Output("node-count", "children"),
    Input("showcase-flow", "nodes"),
)
def show_node_count(nodes):
    count = len(nodes) if nodes else 0
    return dmc.Text(f"{count} nodes", size="xl", fw=700)

# Edge count
@callback(
    Output("edge-count", "children"),
    Input("showcase-flow", "edges"),
)
def show_edge_count(edges):
    count = len(edges) if edges else 0
    return dmc.Text(f"{count} edges", size="xl", fw=700)

if __name__ == "__main__":
    app.run(debug=True, port=8062)