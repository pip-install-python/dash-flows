"""
Example 10: Selection and Multi-Select
======================================
This example demonstrates selection features:
- Single node selection
- Multi-node selection (Shift+click or drag selection)
- Edge selection
- Selection callbacks
- Programmatic selection
"""

import dash
from dash import html, Input, Output, State, callback, ctx
import dash_flows
import dash_mantine_components as dmc
import json

app = dash.Dash(__name__, suppress_callback_exceptions=True)


def extract_id(item):
    """Extract ID from an item, handling different formats."""
    if isinstance(item, dict) and "id" in item:
        return item["id"]
    elif isinstance(item, str):
        return item
    return None


def extract_ids(items):
    """Extract IDs from selection data, handling different formats."""
    if not items:
        return []
    return [id for id in (extract_id(item) for item in items) if id is not None]

initial_nodes = [
    {"id": "a", "type": "default", "data": {"label": "Node A"}, "position": {"x": 100, "y": 50}},
    {"id": "b", "type": "default", "data": {"label": "Node B"}, "position": {"x": 300, "y": 50}},
    {"id": "c", "type": "default", "data": {"label": "Node C"}, "position": {"x": 500, "y": 50}},
    {"id": "d", "type": "default", "data": {"label": "Node D"}, "position": {"x": 100, "y": 200}},
    {"id": "e", "type": "default", "data": {"label": "Node E"}, "position": {"x": 300, "y": 200}},
    {"id": "f", "type": "default", "data": {"label": "Node F"}, "position": {"x": 500, "y": 200}},
]

initial_edges = [
    {"id": "e-ab", "source": "a", "target": "b"},
    {"id": "e-bc", "source": "b", "target": "c"},
    {"id": "e-ad", "source": "a", "target": "d"},
    {"id": "e-be", "source": "b", "target": "e"},
    {"id": "e-cf", "source": "c", "target": "f"},
    {"id": "e-de", "source": "d", "target": "e"},
    {"id": "e-ef", "source": "e", "target": "f"},
]

app.layout = dmc.MantineProvider([
    html.H1("Selection and Multi-Select Example"),
    html.P("Select nodes and edges using various methods."),

    dmc.Alert([
        dmc.Text("Selection Tips:", fw=600),
        dmc.List([
            dmc.ListItem("Click a node/edge to select it"),
            dmc.ListItem("Shift+click to add to selection"),
            dmc.ListItem("Drag on canvas to create selection box"),
            dmc.ListItem("Ctrl+A to select all"),
            dmc.ListItem("Escape to deselect all"),
        ], size="sm"),
    ], color="blue", variant="light", style={"marginBottom": 20}),

    dmc.Grid([
        dmc.GridCol([
            dash_flows.DashFlows(
                id="selection-flow",
                nodes=initial_nodes,
                edges=initial_edges,
                style={"height": "400px", "border": "1px solid #ddd"},
                fitView=True,
                showControls=True,
                # Selection settings
                elementsSelectable=True,
                selectNodesOnDrag=False,  # Only select on click, not drag
                selectionOnDrag=True,  # Allow box selection
                selectionMode="partial",  # Select nodes partially in box
                multiSelectionKeyCode="Shift",
            ),
        ], span=8),

        dmc.GridCol([
            dmc.Stack([
                dmc.Paper([
                    dmc.Text("Selected Nodes:", fw=600),
                    html.Div(id="selected-nodes-display"),
                ], p="sm", withBorder=True),

                dmc.Paper([
                    dmc.Text("Selected Edges:", fw=600),
                    html.Div(id="selected-edges-display"),
                ], p="sm", withBorder=True),

                dmc.Paper([
                    dmc.Text("Selection Actions:", fw=600),
                    dmc.Stack([
                        dmc.Button("Select All Nodes", id="btn-select-all", fullWidth=True, size="sm"),
                        dmc.Button("Select Odd Nodes", id="btn-select-odd", fullWidth=True, size="sm", variant="outline"),
                        dmc.Button("Clear Selection", id="btn-clear-selection", fullWidth=True, size="sm", variant="outline", color="red"),
                        dmc.Button("Delete Selected", id="btn-delete-selected", fullWidth=True, size="sm", color="red"),
                    ], gap="xs"),
                ], p="sm", withBorder=True),
            ], gap="sm"),
        ], span=4),
    ]),
])

@callback(
    Output("selected-nodes-display", "children"),
    Input("selection-flow", "selectedNodes"),
)
def display_selected_nodes(selected_nodes):
    if not selected_nodes:
        return dmc.Text("No nodes selected", c="dimmed", size="sm")
    node_ids = extract_ids(selected_nodes)
    return dmc.Group([
        dmc.Badge(nid, variant="filled", size="sm") for nid in node_ids
    ], gap="xs")

@callback(
    Output("selected-edges-display", "children"),
    Input("selection-flow", "selectedEdges"),
)
def display_selected_edges(selected_edges):
    if not selected_edges:
        return dmc.Text("No edges selected", c="dimmed", size="sm")
    edge_ids = extract_ids(selected_edges)
    return dmc.Group([
        dmc.Badge(eid, variant="outline", size="sm") for eid in edge_ids
    ], gap="xs")

@callback(
    Output("selection-flow", "nodes"),
    Output("selection-flow", "edges"),
    Input("btn-select-all", "n_clicks"),
    Input("btn-select-odd", "n_clicks"),
    Input("btn-clear-selection", "n_clicks"),
    Input("btn-delete-selected", "n_clicks"),
    State("selection-flow", "nodes"),
    State("selection-flow", "edges"),
    State("selection-flow", "selectedNodes"),
    State("selection-flow", "selectedEdges"),
    prevent_initial_call=True,
)
def handle_selection_actions(all_clicks, odd_clicks, clear_clicks, delete_clicks,
                             nodes, edges, selected_nodes, selected_edges):
    if not nodes:
        return initial_nodes, initial_edges

    triggered = ctx.triggered_id

    if triggered == "btn-select-all":
        # Mark all nodes as selected
        updated_nodes = [{**n, "selected": True} for n in nodes]
        return updated_nodes, edges

    elif triggered == "btn-select-odd":
        # Select nodes with odd indices
        updated_nodes = []
        for i, n in enumerate(nodes):
            updated_nodes.append({**n, "selected": (i % 2 == 0)})
        return updated_nodes, edges

    elif triggered == "btn-clear-selection":
        # Clear all selections
        updated_nodes = [{**n, "selected": False} for n in nodes]
        updated_edges = [{**e, "selected": False} for e in edges]
        return updated_nodes, updated_edges

    elif triggered == "btn-delete-selected":
        # Remove selected nodes and their connected edges
        if not selected_nodes:
            return nodes, edges
        selected_ids = set(extract_ids(selected_nodes))
        remaining_nodes = [n for n in nodes if n["id"] not in selected_ids]
        remaining_edges = [e for e in edges if e["source"] not in selected_ids and e["target"] not in selected_ids]
        return remaining_nodes, remaining_edges

    return nodes, edges

if __name__ == "__main__":
    app.run(debug=True, port=8059)