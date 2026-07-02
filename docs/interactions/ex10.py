"""
Embeddable twin of examples/10_selection_multiselect.py for the docs page.
Rendered via `.. exec::docs.interactions.ex10`.
"""
from dash import html, Input, Output, State, callback, ctx
import dash_flows
import dash_mantine_components as dmc


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

component = html.Div([
    dmc.Alert([
        dmc.Text("Selection Tips:", fw=600),
        dmc.List([
            dmc.ListItem("Click a node/edge to select it"),
            dmc.ListItem("Shift+click to add to selection"),
            dmc.ListItem("Drag on canvas to create selection box"),
            dmc.ListItem("Ctrl+A to select all"),
            dmc.ListItem("Escape to deselect all"),
        ], size="sm"),
    ], color="blue", variant="light", mb="md"),

    dmc.Grid([
        dmc.GridCol([
            dash_flows.DashFlows(
                id="ex10-flow",
                nodes=initial_nodes,
                edges=initial_edges,
                style={
                    "height": "440px",
                    "border": "1px solid var(--mantine-color-default-border)",
                    "borderRadius": "8px",
                },
                fitView=True,
                showControls=True,
                elementsSelectable=True,
                selectNodesOnDrag=False,
                selectionOnDrag=True,
                selectionMode="partial",
                multiSelectionKeyCode="Shift",
            ),
        ], span=8),

        dmc.GridCol([
            dmc.Stack([
                dmc.Paper([
                    dmc.Text("Selected Nodes:", fw=600),
                    html.Div(id="ex10-selected-nodes-display"),
                ], p="sm", withBorder=True),

                dmc.Paper([
                    dmc.Text("Selected Edges:", fw=600),
                    html.Div(id="ex10-selected-edges-display"),
                ], p="sm", withBorder=True),

                dmc.Paper([
                    dmc.Text("Selection Actions:", fw=600),
                    dmc.Stack([
                        dmc.Button("Select All Nodes", id="ex10-btn-select-all", fullWidth=True, size="sm"),
                        dmc.Button("Select Odd Nodes", id="ex10-btn-select-odd", fullWidth=True, size="sm", variant="outline"),
                        dmc.Button("Clear Selection", id="ex10-btn-clear-selection", fullWidth=True, size="sm", variant="outline", color="red"),
                        dmc.Button("Delete Selected", id="ex10-btn-delete-selected", fullWidth=True, size="sm", color="red"),
                    ], gap="xs"),
                ], p="sm", withBorder=True),
            ], gap="sm"),
        ], span=4),
    ]),
])


@callback(
    Output("ex10-selected-nodes-display", "children"),
    Input("ex10-flow", "selectedNodes"),
)
def display_selected_nodes(selected_nodes):
    if not selected_nodes:
        return dmc.Text("No nodes selected", c="dimmed", size="sm")
    node_ids = extract_ids(selected_nodes)
    return dmc.Group([
        dmc.Badge(nid, variant="filled", size="sm") for nid in node_ids
    ], gap="xs")


@callback(
    Output("ex10-selected-edges-display", "children"),
    Input("ex10-flow", "selectedEdges"),
)
def display_selected_edges(selected_edges):
    if not selected_edges:
        return dmc.Text("No edges selected", c="dimmed", size="sm")
    edge_ids = extract_ids(selected_edges)
    return dmc.Group([
        dmc.Badge(eid, variant="outline", size="sm") for eid in edge_ids
    ], gap="xs")


@callback(
    Output("ex10-flow", "nodes"),
    Output("ex10-flow", "edges"),
    Input("ex10-btn-select-all", "n_clicks"),
    Input("ex10-btn-select-odd", "n_clicks"),
    Input("ex10-btn-clear-selection", "n_clicks"),
    Input("ex10-btn-delete-selected", "n_clicks"),
    State("ex10-flow", "nodes"),
    State("ex10-flow", "edges"),
    State("ex10-flow", "selectedNodes"),
    State("ex10-flow", "selectedEdges"),
    prevent_initial_call=True,
)
def handle_selection_actions(all_clicks, odd_clicks, clear_clicks, delete_clicks,
                              nodes, edges, selected_nodes, selected_edges):
    if not nodes:
        return initial_nodes, initial_edges

    triggered = ctx.triggered_id

    if triggered == "ex10-btn-select-all":
        updated_nodes = [{**n, "selected": True} for n in nodes]
        return updated_nodes, edges

    elif triggered == "ex10-btn-select-odd":
        updated_nodes = []
        for i, n in enumerate(nodes):
            updated_nodes.append({**n, "selected": (i % 2 == 0)})
        return updated_nodes, edges

    elif triggered == "ex10-btn-clear-selection":
        updated_nodes = [{**n, "selected": False} for n in nodes]
        updated_edges = [{**e, "selected": False} for e in edges]
        return updated_nodes, updated_edges

    elif triggered == "ex10-btn-delete-selected":
        if not selected_nodes:
            return nodes, edges
        selected_ids = set(extract_ids(selected_nodes))
        remaining_nodes = [n for n in nodes if n["id"] not in selected_ids]
        remaining_edges = [e for e in edges if e["source"] not in selected_ids and e["target"] not in selected_ids]
        return remaining_nodes, remaining_edges

    return nodes, edges
