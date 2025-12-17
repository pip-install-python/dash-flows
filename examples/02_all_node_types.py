"""
Example 02: All Node Types
==========================
This example showcases all available node types in DashFlows:
- default: Standard node with both source and target handles
- input: Node with only source handle (start nodes)
- output: Node with only target handle (end nodes)
- group: Container node that can hold other nodes
- toolbar: Node with a configurable toolbar
- resizable: Node that can be resized by the user
- circle: Animated circular node
"""

import dash
from dash import html
import dash_flows

app = dash.Dash(__name__)

nodes = [
    # Input Node - Entry point (only source handle)
    {
        "id": "input-1",
        "type": "input",
        "data": {
            "label": "Input Node",
            "sublabel": "Entry point",
        },
        "position": {"x": 50, "y": 50},
    },

    # Default Node - Standard processing node
    {
        "id": "default-1",
        "type": "default",
        "data": {
            "label": "Default Node",
            "sublabel": "Both handles",
        },
        "position": {"x": 50, "y": 200},
    },

    # Output Node - Exit point (only target handle)
    {
        "id": "output-1",
        "type": "output",
        "data": {
            "label": "Output Node",
            "sublabel": "Exit point",
        },
        "position": {"x": 50, "y": 350},
    },

    # Toolbar Node - With action buttons
    {
        "id": "toolbar-1",
        "type": "toolbar",
        "data": {
            "label": "Toolbar Node",
            "sublabel": "Click to see toolbar",
            "toolbarPosition": "top",
        },
        "position": {"x": 300, "y": 50},
    },

    # Resizable Node - Can be resized
    {
        "id": "resizable-1",
        "type": "resizable",
        "data": {
            "label": html.Div([
                html.Strong("Resizable Node"),
                html.P("Drag corners to resize", style={"fontSize": "11px"}),
            ]),
            "handles": [
                {"type": "target", "position": "top", "id": "r-top"},
                {"type": "source", "position": "bottom", "id": "r-bottom"},
            ],
        },
        "position": {"x": 300, "y": 200},
        "style": {"width": 200, "height": 100},
    },

    # Circle Node - Animated circular node
    {
        "id": "circle-1",
        "type": "circle",
        "data": {"label": "A"},
        "position": {"x": 340, "y": 360},
    },

    # Group Node - Container for other nodes
    {
        "id": "group-1",
        "type": "group",
        "data": {
            "label": "Group Container",
        },
        "position": {"x": 550, "y": 50},
        "style": {"width": 250, "height": 300},
    },

    # Child nodes inside the group
    {
        "id": "child-1",
        "type": "default",
        "data": {"label": "Child A"},
        "position": {"x": 50, "y": 50},  # Position below the label badge
        "parentId": "group-1",
        "extent": "parent",  # Keep within parent bounds
    },
    {
        "id": "child-2",
        "type": "default",
        "data": {"label": "Child B"},
        "position": {"x": 50, "y": 160},
        "parentId": "group-1",
        "extent": "parent",
    },
]

edges = [
    {"id": "e1", "source": "input-1", "target": "default-1"},
    {"id": "e2", "source": "default-1", "target": "output-1"},
    {"id": "e3", "source": "toolbar-1", "target": "resizable-1", "sourceHandle": None, "targetHandle": "r-top"},
    {"id": "e4", "source": "resizable-1", "target": "circle-1", "sourceHandle": "r-bottom"},
    {"id": "e5", "source": "child-1", "target": "child-2"},
]

app.layout = html.Div([
    html.H1("All Node Types Example"),
    html.P("Demonstrates every available node type in DashFlows."),
    html.Ul([
        html.Li("Input Node: Green accent, only outgoing connections"),
        html.Li("Default Node: Standard node with both connection types"),
        html.Li("Output Node: Purple accent, only incoming connections"),
        html.Li("Toolbar Node: Click to reveal action toolbar"),
        html.Li("Resizable Node: Drag corners to resize"),
        html.Li("Circle Node: Animated circular indicator"),
        html.Li("Group Node: Container that holds child nodes"),
    ]),
    dash_flows.DashFlows(
        id="node-types-flow",
        nodes=nodes,
        edges=edges,
        style={"height": "600px", "border": "1px solid #ddd"},
        fitView=True,
        showControls=True,
        showMiniMap=True,
    ),
])

if __name__ == "__main__":
    app.run(debug=True, port=8071)