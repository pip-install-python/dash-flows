"""
Embeddable twin of examples/01_basic_nodes_and_edges.py for the docs page.
Rendered via `.. exec::docs.getting_started.ex01`.
"""
from dash import html
import dash_flows

# Define basic nodes
nodes = [
    {
        "id": "node-1",
        "type": "default",
        "data": {"label": "Start Node"},
        "position": {"x": 100, "y": 100},
    },
    {
        "id": "node-2",
        "type": "default",
        "data": {"label": "Process A"},
        "position": {"x": 100, "y": 250},
    },
    {
        "id": "node-3",
        "type": "default",
        "data": {"label": "Process B"},
        "position": {"x": 300, "y": 250},
    },
    {
        "id": "node-4",
        "type": "default",
        "data": {"label": "End Node"},
        "position": {"x": 200, "y": 400},
    },
]

# Define edges connecting the nodes
edges = [
    {
        "id": "edge-1-2",
        "source": "node-1",
        "target": "node-2",
        "animated": True,  # Shows animated dashed line
    },
    {
        "id": "edge-1-3",
        "source": "node-1",
        "target": "node-3",
    },
    {
        "id": "edge-2-4",
        "source": "node-2",
        "target": "node-4",
        "label": "Step 1",  # Edge with label
    },
    {
        "id": "edge-3-4",
        "source": "node-3",
        "target": "node-4",
        "label": "Step 2",
    },
]

component = html.Div([
    dash_flows.DashFlows(
        id="ex01-basic-flow",
        nodes=nodes,
        edges=edges,
        style={
            "height": "480px",
            "border": "1px solid var(--mantine-color-default-border)",
            "borderRadius": "8px",
        },
        fitView=True,
        showControls=True,
        showMiniMap=True,
        colorMode="system",
    ),
])
