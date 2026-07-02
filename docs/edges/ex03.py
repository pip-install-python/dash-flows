"""
Embeddable twin of examples/03_all_edge_types.py for the docs page.
Rendered via `.. exec::docs.edges.ex03`.
"""
from dash import html, callback, Input, Output
import dash_flows

# Create a row of source nodes and a row of target nodes
nodes = [
    # Source nodes (top row)
    {"id": "s1", "type": "input", "data": {"label": "Default"}, "position": {"x": 50, "y": 50}},
    {"id": "s2", "type": "input", "data": {"label": "Straight"}, "position": {"x": 200, "y": 50}},
    {"id": "s3", "type": "input", "data": {"label": "Step"}, "position": {"x": 350, "y": 50}},
    {"id": "s4", "type": "input", "data": {"label": "SmoothStep"}, "position": {"x": 500, "y": 50}},
    {"id": "s5", "type": "input", "data": {"label": "SimpleBezier"}, "position": {"x": 650, "y": 50}},
    {"id": "s6", "type": "input", "data": {"label": "Button Edge"}, "position": {"x": 800, "y": 50}},

    # Target nodes (bottom row)
    {"id": "t1", "type": "output", "data": {"label": "Target 1"}, "position": {"x": 50, "y": 300}},
    {"id": "t2", "type": "output", "data": {"label": "Target 2"}, "position": {"x": 200, "y": 300}},
    {"id": "t3", "type": "output", "data": {"label": "Target 3"}, "position": {"x": 350, "y": 300}},
    {"id": "t4", "type": "output", "data": {"label": "Target 4"}, "position": {"x": 500, "y": 300}},
    {"id": "t5", "type": "output", "data": {"label": "Target 5"}, "position": {"x": 650, "y": 300}},
    {"id": "t6", "type": "output", "data": {"label": "Target 6"}, "position": {"x": 800, "y": 300}},
]

edges = [
    # Default edge (bezier curve) - React Flow's built-in
    {
        "id": "e1",
        "source": "s1",
        "target": "t1",
        "type": "default",
        "label": "Default",
        "animated": True,
    },

    # Straight edge - direct line
    {
        "id": "e2",
        "source": "s2",
        "target": "t2",
        "type": "straight",
        "label": "Straight",
    },

    # Step edge - sharp right angles
    {
        "id": "e3",
        "source": "s3",
        "target": "t3",
        "type": "step",
        "label": "Step",
    },

    # SmoothStep edge - rounded right angles
    {
        "id": "e4",
        "source": "s4",
        "target": "t4",
        "type": "smoothstep",
        "label": "SmoothStep",
        "data": {"borderRadius": 15},  # Custom corner radius
    },

    # SimpleBezier edge - simple curve
    {
        "id": "e5",
        "source": "s5",
        "target": "t5",
        "type": "simplebezier",
        "label": "SimpleBezier",
    },

    # Button edge - with delete button
    {
        "id": "e6",
        "source": "s6",
        "target": "t6",
        "type": "button",
        "data": {
            "label": "Click X to delete",
            "showButton": True,
            "buttonLabel": "x",
        },
    },
]

component = html.Div([
    dash_flows.DashFlows(
        id="ex03-edge-types-flow",
        nodes=nodes,
        edges=edges,
        style={
            "height": "480px",
            "border": "1px solid var(--mantine-color-default-border)",
            "borderRadius": "8px",
        },
        fitView=True,
        showControls=True,
        colorMode="system",
    ),
    html.Div(id="ex03-edge-deleted-info", style={"marginTop": "12px", "fontSize": "14px", "color": "var(--mantine-color-dimmed)"}),
])


# Track edge deletions
@callback(
    Output("ex03-edge-deleted-info", "children"),
    Input("ex03-edge-types-flow", "edges"),
    prevent_initial_call=True,
)
def track_edge_changes(current_edges):
    if current_edges is None:
        return ""
    edge_count = len(current_edges)
    return f"Current edge count: {edge_count}"
