"""
Example 06: Handle Configurations
=================================
This example demonstrates various handle configurations:
- Multiple handles per node
- Handle positions (top, bottom, left, right)
- Custom handle IDs for specific connections
- Handle styling
"""

import dash
from dash import html
import dash_flows

app = dash.Dash(__name__)

nodes = [
    # Node with multiple handles on different sides
    {
        "id": "multi-handle",
        "type": "resizable",
        "data": {
            "label": html.Div([
                html.Strong("Multi-Handle Node"),
                html.P("4 handles on each side", style={"fontSize": "11px", "margin": 0}),
            ]),
            "handles": [
                {"type": "target", "position": "top", "id": "top-in", "style": {"background": "#10b981"}},
                {"type": "target", "position": "left", "id": "left-in", "style": {"background": "#3b82f6"}},
                {"type": "source", "position": "bottom", "id": "bottom-out", "style": {"background": "#8b5cf6"}},
                {"type": "source", "position": "right", "id": "right-out", "style": {"background": "#f59e0b"}},
            ],
        },
        "position": {"x": 250, "y": 150},
        "style": {"width": 180, "height": 80},
    },

    # Source nodes feeding into the multi-handle node
    {
        "id": "top-source",
        "type": "input",
        "data": {"label": "Top Source"},
        "position": {"x": 270, "y": 20},
    },
    {
        "id": "left-source",
        "type": "input",
        "data": {"label": "Left Source"},
        "position": {"x": 50, "y": 160},
    },

    # Target nodes receiving from the multi-handle node
    {
        "id": "bottom-target",
        "type": "output",
        "data": {"label": "Bottom Target"},
        "position": {"x": 270, "y": 310},
    },
    {
        "id": "right-target",
        "type": "output",
        "data": {"label": "Right Target"},
        "position": {"x": 480, "y": 160},
    },

    # Node with offset handles
    {
        "id": "offset-handles",
        "type": "resizable",
        "data": {
            "label": html.Div([
                html.Strong("Offset Handles"),
                html.P("Handles at specific positions", style={"fontSize": "11px", "margin": 0}),
            ]),
            "handles": [
                {"type": "target", "position": "top", "id": "t1", "style": {"left": "25%", "background": "#ef4444"}},
                {"type": "target", "position": "top", "id": "t2", "style": {"left": "75%", "background": "#ef4444"}},
                {"type": "source", "position": "bottom", "id": "s1", "style": {"left": "25%", "background": "#22c55e"}},
                {"type": "source", "position": "bottom", "id": "s2", "style": {"left": "75%", "background": "#22c55e"}},
            ],
        },
        "position": {"x": 250, "y": 420},
        "style": {"width": 180, "height": 80},
    },

    # Nodes to connect to offset handles
    {
        "id": "offset-source-1",
        "type": "input",
        "data": {"label": "A"},
        "position": {"x": 220, "y": 350},
    },
    {
        "id": "offset-source-2",
        "type": "input",
        "data": {"label": "B"},
        "position": {"x": 380, "y": 350},
    },
    {
        "id": "offset-target-1",
        "type": "output",
        "data": {"label": "X"},
        "position": {"x": 220, "y": 560},
    },
    {
        "id": "offset-target-2",
        "type": "output",
        "data": {"label": "Y"},
        "position": {"x": 380, "y": 560},
    },
]

edges = [
    # Connections to multi-handle node
    {"id": "e1", "source": "top-source", "target": "multi-handle", "targetHandle": "top-in"},
    {"id": "e2", "source": "left-source", "target": "multi-handle", "targetHandle": "left-in"},
    {"id": "e3", "source": "multi-handle", "target": "bottom-target", "sourceHandle": "bottom-out"},
    {"id": "e4", "source": "multi-handle", "target": "right-target", "sourceHandle": "right-out"},

    # Connections to offset handles node
    {"id": "e5", "source": "offset-source-1", "target": "offset-handles", "targetHandle": "t1"},
    {"id": "e6", "source": "offset-source-2", "target": "offset-handles", "targetHandle": "t2"},
    {"id": "e7", "source": "offset-handles", "target": "offset-target-1", "sourceHandle": "s1"},
    {"id": "e8", "source": "offset-handles", "target": "offset-target-2", "sourceHandle": "s2"},
]

app.layout = html.Div([
    html.H1("Handle Configurations Example"),
    html.P("Demonstrates multiple handles, custom positions, and handle styling."),
    html.Ul([
        html.Li("Multi-Handle Node: 4 handles, one on each side with different colors"),
        html.Li("Offset Handles: Multiple handles on the same side at specific positions"),
        html.Li("Each handle has a unique ID for precise edge connections"),
    ]),
    dash_flows.DashFlows(
        id="handle-flow",
        nodes=nodes,
        edges=edges,
        style={"height": "700px", "border": "1px solid #ddd"},
        fitView=True,
        showControls=True,
    ),
])

if __name__ == "__main__":
    app.run(debug=True, port=8055)