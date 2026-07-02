"""
Example 30: Node Resize Constraints
====================================
Demonstrates resize constraints on ResizableNode and GroupNode:
- keepAspectRatio: Lock aspect ratio during resize
- maxWidth / maxHeight: Maximum size limits
"""

import dash
from dash import html
import dash_flows

app = dash.Dash(__name__)

nodes = [
    # Resizable node with aspect ratio lock
    {
        "id": "aspect-locked",
        "type": "resizable",
        "data": {
            "label": "Aspect Ratio Locked (2:1)",
            "handles": [
                {"id": "source-right", "type": "source", "position": "right"},
                {"id": "target-left", "type": "target", "position": "left"},
            ],
            "keepAspectRatio": True,
            "initialWidth": 300,
            "initialHeight": 150,
            "minWidth": 200,
            "minHeight": 100,
        },
        "position": {"x": 50, "y": 50},
        "style": {"width": 300, "height": 150},
    },
    # Resizable node with max dimensions
    {
        "id": "max-constrained",
        "type": "resizable",
        "data": {
            "label": "Max 400x200",
            "handles": [
                {"id": "source-right", "type": "source", "position": "right"},
                {"id": "target-left", "type": "target", "position": "left"},
            ],
            "maxWidth": 400,
            "maxHeight": 200,
            "minWidth": 150,
            "minHeight": 80,
        },
        "position": {"x": 50, "y": 280},
        "style": {"width": 250, "height": 120},
    },
    # Group node with resize constraints
    {
        "id": "constrained-group",
        "type": "group",
        "data": {
            "label": "Constrained Group (max 500x400)",
            "maxWidth": 500,
            "maxHeight": 400,
            "minWidth": 200,
            "minHeight": 150,
        },
        "position": {"x": 450, "y": 50},
        "style": {"width": 350, "height": 300},
    },
    # Child inside group
    {
        "id": "child-1",
        "type": "default",
        "data": {"label": "Child Node A"},
        "position": {"x": 30, "y": 50},
        "parentId": "constrained-group",
        "extent": "parent",
    },
    {
        "id": "child-2",
        "type": "default",
        "data": {"label": "Child Node B"},
        "position": {"x": 30, "y": 150},
        "parentId": "constrained-group",
        "extent": "parent",
    },
    # Group with aspect ratio lock
    {
        "id": "aspect-group",
        "type": "group",
        "data": {
            "label": "Aspect Locked Group",
            "keepAspectRatio": True,
            "minWidth": 150,
            "minHeight": 150,
        },
        "position": {"x": 450, "y": 380},
        "style": {"width": 250, "height": 250},
    },
]

edges = [
    {"id": "e1", "source": "aspect-locked", "target": "max-constrained"},
    {"id": "e2", "source": "child-1", "target": "child-2"},
]

app.layout = html.Div([
    html.H2("Node Resize Constraints"),

    # Constraint summary
    html.Div([
        html.Strong("How to resize: ", style={"fontSize": "13px"}),
        html.Span("Click a node to select it, then drag the blue corner / edge handles that appear.",
                  style={"fontSize": "13px", "color": "#555"}),
        html.Br(),
        html.Div([
            html.Span("■ Top-left ResizableNode",  style={"color": "#3b82f6", "fontWeight": "600", "fontSize": "12px"}),
            html.Span(" — aspect ratio locked 2:1, min 200×100",           style={"fontSize": "12px", "color": "#555", "marginRight": "18px"}),
            html.Span("■ Bottom-left ResizableNode", style={"color": "#8b5cf6", "fontWeight": "600", "fontSize": "12px"}),
            html.Span(" — max 400×200, min 150×80",                         style={"fontSize": "12px", "color": "#555"}),
        ], style={"marginTop": "4px"}),
        html.Div([
            html.Span("■ Right GroupNode",           style={"color": "#10b981", "fontWeight": "600", "fontSize": "12px"}),
            html.Span(" — max 500×400, min 200×150",                         style={"fontSize": "12px", "color": "#555", "marginRight": "18px"}),
            html.Span("■ Bottom-right GroupNode",    style={"color": "#f59e0b", "fontWeight": "600", "fontSize": "12px"}),
            html.Span(" — aspect ratio locked, min 150×150",                 style={"fontSize": "12px", "color": "#555"}),
        ], style={"marginTop": "2px"}),
    ], style={
        "background": "#f9fafb", "border": "1px solid #e5e7eb",
        "borderRadius": "8px", "padding": "10px 14px", "marginBottom": "12px",
    }),

    dash_flows.DashFlows(
        id="resize-flow",
        nodes=nodes,
        edges=edges,
        fitView=True,
        showControls=True,
        showMiniMap=True,
        showBackground=True,
        style={"height": "700px"},
    ),
], style={"padding": "20px"})

if __name__ == "__main__":
    app.run(debug=True, port=8030)
