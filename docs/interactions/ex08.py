"""
Embeddable twin of examples/08_connection_validation.py for the docs page.
Rendered via `.. exec::docs.interactions.ex08`.
"""
from dash import html, Input, Output, callback, ctx
import dash_flows
import dash_mantine_components as dmc
import json
import random

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

component = html.Div([
    dmc.Alert([
        dmc.Text("Connection Rules:", fw=600),
        dmc.List([
            dmc.ListItem("Input nodes can only be sources (green)"),
            dmc.ListItem("Output nodes can only be targets (purple)"),
            dmc.ListItem("Self-connections are not allowed"),
            dmc.ListItem("Duplicate connections are prevented"),
        ], size="sm"),
    ], color="blue", variant="light", mb="md"),

    dash_flows.DashFlows(
        id="ex08-flow",
        nodes=nodes,
        edges=initial_edges,
        style={
            "height": "440px",
            "border": "1px solid var(--mantine-color-default-border)",
            "borderRadius": "8px",
        },
        fitView=True,
        showControls=True,
        nodesConnectable=True,
        connectionMode="loose",
        connectionLineStyle={"stroke": "#3b82f6", "strokeWidth": 2},
    ),

    dmc.Space(h=20),

    dmc.Paper([
        dmc.Text("Current Edges:", fw=600),
        html.Pre(id="ex08-edges-display", style={"fontSize": "11px", "maxHeight": "160px", "overflow": "auto"}),
    ], p="md", withBorder=True),

    dmc.Space(h=10),

    dmc.Group([
        dmc.Button("Add Random Connection", id="ex08-add-edge-btn", variant="outline"),
        dmc.Button("Clear All Edges", id="ex08-clear-edges-btn", variant="outline", color="red"),
    ]),
])


@callback(
    Output("ex08-edges-display", "children"),
    Input("ex08-flow", "edges"),
)
def display_edges(edges):
    if not edges:
        return "No edges"
    edge_info = [{"id": e["id"], "source": e["source"], "target": e["target"]} for e in edges]
    return json.dumps(edge_info, indent=2)


@callback(
    Output("ex08-flow", "edges", allow_duplicate=True),
    Input("ex08-clear-edges-btn", "n_clicks"),
    prevent_initial_call=True,
)
def clear_edges(n):
    return []


@callback(
    Output("ex08-flow", "edges", allow_duplicate=True),
    Input("ex08-add-edge-btn", "n_clicks"),
    Input("ex08-flow", "edges"),
    prevent_initial_call=True,
)
def add_random_edge(n_clicks, current_edges):
    if ctx.triggered_id != "ex08-add-edge-btn":
        return current_edges

    sources = ["input-1", "input-2", "process-1", "process-2", "process-3"]
    targets = ["process-1", "process-2", "process-3", "output-1", "output-2"]

    for _ in range(10):  # Try up to 10 times to find a valid connection
        source = random.choice(sources)
        target = random.choice(targets)

        if source == target:
            continue

        edge_id = f"e-{source}-{target}"
        if any(e["id"] == edge_id or (e["source"] == source and e["target"] == target) for e in current_edges):
            continue

        new_edge = {"id": edge_id, "source": source, "target": target}
        return current_edges + [new_edge]

    return current_edges  # No valid connection found
