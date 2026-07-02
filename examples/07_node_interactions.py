"""
Example 07: Node Interactions
=============================
This example demonstrates node interaction callbacks:
- Node click events
- Node drag events
- Node hover events (via CSS)
- Context menu (right-click) events
- Selection change events
"""

import dash
from dash import html, Input, Output, State, callback
import dash_flows
import dash_mantine_components as dmc
import json

app = dash.Dash(__name__, suppress_callback_exceptions=True)

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

app.layout = dmc.MantineProvider([
    html.H1("Node Interactions Example"),
    html.P("Interact with nodes and observe the callbacks."),

    dmc.Grid([
        dmc.GridCol([
            dash_flows.DashFlows(
                id="interaction-flow",
                nodes=initial_nodes,
                edges=initial_edges,
                style={"height": "400px", "border": "1px solid #ddd"},
                fitView=True,
                showControls=True,
                # Enable interactions
                nodesDraggable=True,
                nodesConnectable=True,
                elementsSelectable=True,
                # Enable multi-select with Shift key
                multiSelectionKeyCode="Shift",
            ),
        ], span=8),

        dmc.GridCol([
            dmc.Stack([
                dmc.Paper([
                    dmc.Text("Last Click Event:", fw=600),
                    html.Pre(id="click-event", children="Click a node...",
                             style={"fontSize": "11px", "maxHeight": "100px", "overflow": "auto"}),
                ], p="sm", withBorder=True),

                dmc.Paper([
                    dmc.Text("Node Positions:", fw=600),
                    html.Pre(id="position-info", children="Drag a node...",
                             style={"fontSize": "11px", "maxHeight": "150px", "overflow": "auto"}),
                ], p="sm", withBorder=True),

                dmc.Paper([
                    dmc.Text("Selection Info:", fw=600),
                    html.Pre(id="selection-info", children="Select nodes...",
                             style={"fontSize": "11px", "maxHeight": "100px", "overflow": "auto"}),
                ], p="sm", withBorder=True),

                dmc.Paper([
                    dmc.Text("Context Menu (Right-Click):", fw=600),
                    html.Pre(id="context-menu-info", children="Right-click a node...",
                             style={"fontSize": "11px", "maxHeight": "100px", "overflow": "auto"}),
                ], p="sm", withBorder=True),
            ], gap="sm"),
        ], span=4),
    ]),

    dmc.Space(h=20),
    dmc.Text("Tips:", fw=600),
    dmc.List([
        dmc.ListItem("Click on any node to see click event data"),
        dmc.ListItem("Drag nodes to see position updates"),
        dmc.ListItem("Hold Shift and click to multi-select nodes"),
        dmc.ListItem("Use the selection box (drag on canvas) to select multiple nodes"),
        dmc.ListItem("Right-click a node to see context menu event data"),
    ]),
])

@callback(
    Output("click-event", "children"),
    Input("interaction-flow", "selectedNodes"),
    prevent_initial_call=True,
)
def on_node_click(selected_nodes):
    if not selected_nodes:
        return "No nodes selected"
    # Show the last selected node
    return json.dumps(selected_nodes, indent=2)

@callback(
    Output("position-info", "children"),
    Input("interaction-flow", "nodes"),
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
    Output("selection-info", "children"),
    Input("interaction-flow", "selectedNodes"),
    Input("interaction-flow", "selectedEdges"),
)
def on_selection_change(selected_nodes, selected_edges):
    info = {
        "selectedNodes": extract_ids(selected_nodes),
        "selectedEdges": extract_ids(selected_edges),
    }
    return json.dumps(info, indent=2)


@callback(
    Output("context-menu-info", "children"),
    Input("interaction-flow", "contextMenuNode"),
    prevent_initial_call=True,
)
def on_context_menu(context_menu_node):
    if not context_menu_node:
        return "Right-click a node..."
    # Show context menu event data
    return json.dumps(context_menu_node, indent=2)


if __name__ == "__main__":
    app.run(debug=True, port=8066)