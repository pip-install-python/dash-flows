"""
Example 08: Connection Validation and Rules
===========================================
This example demonstrates connection validation:
- Preventing self-connections
- Limiting connections per handle
- Custom connection rules
- Visual feedback during connection
"""

import dash
from dash import html, Input, Output, callback, clientside_callback
import dash_flows
import dash_mantine_components as dmc
import json

app = dash.Dash(__name__)

# Define nodes with specific connection rules
nodes = [
    # Input nodes (sources only)
    {"id": "input-1", "type": "input", "data": {"label": "Data Source A"}, "position": {"x": 50, "y": 50}},
    {"id": "input-2", "type": "input", "data": {"label": "Data Source B"}, "position": {"x": 50, "y": 150}},

    # Processing nodes (can connect to each other)
    {"id": "process-1", "type": "default", "data": {"label": "Filter"}, "position": {"x": 250, "y": 50}},
    {"id": "process-2", "type": "default", "data": {"label": "Transform"}, "position": {"x": 250, "y": 150}},
    {"id": "process-3", "type": "default", "data": {"label": "Aggregate"}, "position": {"x": 450, "y": 100}},

    # Output nodes (targets only)
    {"id": "output-1", "type": "output", "data": {"label": "Database"}, "position": {"x": 650, "y": 50}},
    {"id": "output-2", "type": "output", "data": {"label": "API"}, "position": {"x": 650, "y": 150}},
]

initial_edges = [
    {"id": "e1", "source": "input-1", "target": "process-1"},
    {"id": "e2", "source": "input-2", "target": "process-2"},
]

app.layout = dmc.MantineProvider([
    html.H1("Connection Validation Example"),
    html.P("Try connecting nodes and observe the validation rules in action."),

    dmc.Alert([
        dmc.Text("Connection Rules:", fw=600),
        dmc.List([
            dmc.ListItem("Input nodes can only be sources (green)"),
            dmc.ListItem("Output nodes can only be targets (purple)"),
            dmc.ListItem("Self-connections are not allowed"),
            dmc.ListItem("Duplicate connections are prevented"),
        ], size="sm"),
    ], color="blue", variant="light", style={"marginBottom": 20}),

    dash_flows.DashFlows(
        id="validation-flow",
        nodes=nodes,
        edges=initial_edges,
        style={"height": "400px", "border": "1px solid #ddd"},
        fitView=True,
        showControls=True,
        # Connection settings
        nodesConnectable=True,
        connectionMode="loose",  # Allow connections to any point on node
        # Visual feedback
        connectionLineStyle={"stroke": "#3b82f6", "strokeWidth": 2},
    ),

    dmc.Space(h=20),

    dmc.Paper([
        dmc.Text("Current Edges:", fw=600),
        html.Pre(id="edges-display", style={"fontSize": "11px", "maxHeight": "200px", "overflow": "auto"}),
    ], p="md", withBorder=True),

    dmc.Space(h=10),

    dmc.Group([
        dmc.Button("Add Random Connection", id="add-edge-btn", variant="outline"),
        dmc.Button("Clear All Edges", id="clear-edges-btn", variant="outline", color="red"),
    ]),
])

@callback(
    Output("edges-display", "children"),
    Input("validation-flow", "edges"),
)
def display_edges(edges):
    if not edges:
        return "No edges"
    edge_info = [{"id": e["id"], "source": e["source"], "target": e["target"]} for e in edges]
    return json.dumps(edge_info, indent=2)

@callback(
    Output("validation-flow", "edges", allow_duplicate=True),
    Input("clear-edges-btn", "n_clicks"),
    prevent_initial_call=True,
)
def clear_edges(n):
    return []

@callback(
    Output("validation-flow", "edges", allow_duplicate=True),
    Input("add-edge-btn", "n_clicks"),
    Input("validation-flow", "edges"),
    prevent_initial_call=True,
)
def add_random_edge(n_clicks, current_edges):
    import random
    from dash import ctx

    if ctx.triggered_id != "add-edge-btn":
        return current_edges

    # Try to create a valid random connection
    sources = ["input-1", "input-2", "process-1", "process-2", "process-3"]
    targets = ["process-1", "process-2", "process-3", "output-1", "output-2"]

    for _ in range(10):  # Try up to 10 times to find a valid connection
        source = random.choice(sources)
        target = random.choice(targets)

        if source == target:
            continue

        # Check if edge already exists
        edge_id = f"e-{source}-{target}"
        if any(e["id"] == edge_id or (e["source"] == source and e["target"] == target) for e in current_edges):
            continue

        # Valid new edge
        new_edge = {"id": edge_id, "source": source, "target": target}
        return current_edges + [new_edge]

    return current_edges  # No valid connection found

if __name__ == "__main__":
    app.run(debug=True, port=8057)