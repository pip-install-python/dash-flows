"""
Example 01: Basic Nodes and Edges
=================================
This example demonstrates the fundamental building blocks of DashFlows:
- Creating nodes with different types
- Connecting nodes with edges
- Basic styling and positioning
"""

import dash
from dash import html
import dash_flows

app = dash.Dash(__name__)

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

app.layout = html.Div([
    html.H1("Basic Nodes and Edges Example"),
    html.P("This shows the fundamental elements of a flow diagram."),
    dash_flows.DashFlows(
        id="basic-flow",
        nodes=nodes,
        edges=edges,
        style={"height": "600px", "border": "1px solid #ddd"},
        fitView=True,
        showControls=True,
        showMiniMap=True,
    ),
])

if __name__ == "__main__":
    app.run(debug=True, port=8070)