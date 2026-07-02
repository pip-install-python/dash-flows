"""
Embeddable twin of examples/07_node_interactions.py for the docs page.
Rendered via `.. exec::docs.interactions.ex07`.
"""
from dash import html, Input, Output, callback
import dash_flows
import dash_mantine_components as dmc
import json

initial_nodes = [
    {"id": "1", "type": "default", "data": {"label": "Click Me"}, "position": {"x": 100, "y": 50}},
    {"id": "2", "type": "default", "data": {"label": "Drag Me"}, "position": {"x": 300, "y": 50}},
    {"id": "3", "type": "default", "data": {"label": "Right-Click Me"}, "position": {"x": 500, "y": 50}},
    {"id": "4", "type": "default", "data": {"label": "Node 4"}, "position": {"x": 100, "y": 200}},
    {"id": "5", "type": "default", "data": {"label": "Node 5"}, "position": {"x": 300, "y": 200}},
    {"id": "6", "type": "default", "data": {"label": "Node 6"}, "position": {"x": 500, "y": 200}},
]

initial_edges = [
    {"id": "e1-4", "source": "1", "target": "4"},
    {"id": "e2-5", "source": "2", "target": "5"},
    {"id": "e3-6", "source": "3", "target": "6"},
]

component = html.Div([
    dmc.Grid([
        dmc.GridCol([
            dash_flows.DashFlows(
                id="ex07-flow",
                nodes=initial_nodes,
                edges=initial_edges,
                style={
                    "height": "460px",
                    "border": "1px solid var(--mantine-color-default-border)",
                    "borderRadius": "8px",
                },
                fitView=True,
                showControls=True,
                nodesDraggable=True,
                nodesConnectable=True,
                elementsSelectable=True,
                multiSelectionKeyCode="Shift",
            ),
        ], span=8),

        dmc.GridCol([
            dmc.Stack([
                dmc.Paper([
                    dmc.Text("Last Click Event:", fw=600),
                    html.Pre(id="ex07-click-event", children="Click a node...",
                             style={"fontSize": "11px", "maxHeight": "100px", "overflow": "auto"}),
                ], p="sm", withBorder=True),

                dmc.Paper([
                    dmc.Text("Node Positions:", fw=600),
                    html.Pre(id="ex07-position-info", children="Drag a node...",
                             style={"fontSize": "11px", "maxHeight": "120px", "overflow": "auto"}),
                ], p="sm", withBorder=True),

                dmc.Paper([
                    dmc.Text("Selection Info:", fw=600),
                    html.Pre(id="ex07-selection-info", children="Select nodes...",
                             style={"fontSize": "11px", "maxHeight": "100px", "overflow": "auto"}),
                ], p="sm", withBorder=True),

                dmc.Paper([
                    dmc.Text("Context Menu (Right-Click):", fw=600),
                    html.Pre(id="ex07-context-menu-info", children="Right-click a node...",
                             style={"fontSize": "11px", "maxHeight": "100px", "overflow": "auto"}),
                ], p="sm", withBorder=True),
            ], gap="sm"),
        ], span=4),
    ]),
])


@callback(
    Output("ex07-click-event", "children"),
    Input("ex07-flow", "selectedNodes"),
    prevent_initial_call=True,
)
def on_node_click(selected_nodes):
    if not selected_nodes:
        return "No nodes selected"
    return json.dumps(selected_nodes, indent=2)


@callback(
    Output("ex07-position-info", "children"),
    Input("ex07-flow", "nodes"),
    prevent_initial_call=True,
)
def on_node_drag(nodes):
    if not nodes:
        return "No nodes"
    positions = {n["id"]: n["position"] for n in nodes}
    return json.dumps(positions, indent=2)


def extract_ids(items):
    """Extract IDs from selection data, handling different formats."""
    if not items:
        return []
    result = []
    for item in items:
        if isinstance(item, dict) and "id" in item:
            result.append(item["id"])
        elif isinstance(item, str):
            result.append(item)
    return result


@callback(
    Output("ex07-selection-info", "children"),
    Input("ex07-flow", "selectedNodes"),
    Input("ex07-flow", "selectedEdges"),
)
def on_selection_change(selected_nodes, selected_edges):
    info = {
        "selectedNodes": extract_ids(selected_nodes),
        "selectedEdges": extract_ids(selected_edges),
    }
    return json.dumps(info, indent=2)


@callback(
    Output("ex07-context-menu-info", "children"),
    Input("ex07-flow", "contextMenuNode"),
    prevent_initial_call=True,
)
def on_context_menu(context_menu_node):
    if not context_menu_node:
        return "Right-click a node..."
    return json.dumps(context_menu_node, indent=2)
