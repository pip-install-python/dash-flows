"""
Example 24: Smart Handle Positioning
=====================================
Demonstrates the smartHandles feature which automatically positions edge
connection points to the closest side of each node, preventing edges from
wrapping around nodes unnecessarily.

Also shows manual handle positioning via sourcePosition/targetPosition in node data.
"""

import dash
from dash import html, dcc, callback, Input, Output, State
import dash_flows

app = dash.Dash(__name__)


# --- Nodes arranged in various positions to show smart routing ---
smart_nodes = [
    # Top-left cluster
    {
        "id": "source-1",
        "type": "input",
        "data": {"label": "Data Source", "sublabel": "API"},
        "position": {"x": 50, "y": 50},
    },
    # Top-right
    {
        "id": "process-1",
        "type": "default",
        "data": {"label": "Validate", "sublabel": "Schema Check"},
        "position": {"x": 400, "y": 30},
    },
    # Center
    {
        "id": "process-2",
        "type": "default",
        "data": {"label": "Transform", "sublabel": "Map & Filter"},
        "position": {"x": 250, "y": 200},
    },
    # Bottom-left
    {
        "id": "process-3",
        "type": "default",
        "data": {"label": "Aggregate", "sublabel": "Group By"},
        "position": {"x": 50, "y": 350},
    },
    # Far right - mid
    {
        "id": "process-4",
        "type": "default",
        "data": {"label": "Enrich", "sublabel": "Join External"},
        "position": {"x": 500, "y": 220},
    },
    # Bottom-right
    {
        "id": "output-1",
        "type": "output",
        "data": {"label": "Dashboard", "sublabel": "Visualization"},
        "position": {"x": 400, "y": 400},
    },
    # Bottom center
    {
        "id": "output-2",
        "type": "output",
        "data": {"label": "Database", "sublabel": "PostgreSQL"},
        "position": {"x": 200, "y": 430},
    },
]

smart_edges = [
    # Horizontal: left -> right (should use right/left handles)
    {"id": "e1", "source": "source-1", "target": "process-1", "type": "smoothstep"},
    # Diagonal: top-left -> center (should pick best side)
    {"id": "e2", "source": "source-1", "target": "process-2", "type": "smoothstep"},
    # Right -> far right (horizontal, should use right/left)
    {"id": "e3", "source": "process-1", "target": "process-4", "type": "smoothstep"},
    # Center -> bottom-left (should use left/bottom or bottom/top)
    {"id": "e4", "source": "process-2", "target": "process-3", "type": "smoothstep"},
    # Center -> far right (horizontal)
    {"id": "e5", "source": "process-2", "target": "process-4", "type": "smoothstep"},
    # Center -> bottom-right output
    {"id": "e6", "source": "process-2", "target": "output-1", "type": "smoothstep"},
    # Far right -> bottom-right output
    {"id": "e7", "source": "process-4", "target": "output-1", "type": "smoothstep"},
    # Bottom-left -> bottom-center output
    {"id": "e8", "source": "process-3", "target": "output-2", "type": "smoothstep"},
]


# --- Manual handle positioning example ---
manual_nodes = [
    # Horizontal flow: left to right
    {
        "id": "h-start",
        "type": "input",
        "data": {
            "label": "Start",
            "sourcePosition": "right",  # Manual: source handle on right side
        },
        "position": {"x": 0, "y": 100},
    },
    {
        "id": "h-middle",
        "type": "default",
        "data": {
            "label": "Process",
            "sourcePosition": "right",
            "targetPosition": "left",  # Manual: target handle on left side
        },
        "position": {"x": 250, "y": 100},
    },
    {
        "id": "h-end",
        "type": "output",
        "data": {
            "label": "End",
            "targetPosition": "left",
        },
        "position": {"x": 500, "y": 100},
    },
]

manual_edges = [
    {"id": "he1", "source": "h-start", "target": "h-middle", "type": "smoothstep"},
    {"id": "he2", "source": "h-middle", "target": "h-end", "type": "smoothstep"},
]


app.layout = html.Div([
    html.H1("Smart Handle Positioning"),
    html.P(
        "The smartHandles prop automatically routes edges to the closest side of each node, "
        "eliminating unnecessary wrapping and overlapping."
    ),

    # Toggle
    html.Div([
        html.H3("Automatic Smart Handles"),
        html.P(
            "Toggle smartHandles to see the difference. Without it, all edges connect "
            "from bottom (source) to top (target), causing messy routing on non-vertical layouts."
        ),
        dcc.Checklist(
            id="smart-toggle",
            options=[{"label": "Enable smartHandles", "value": "on"}],
            value=["on"],
            style={"fontSize": "14px", "marginBottom": "12px"},
        ),
        html.Div(id="smart-status", style={"fontSize": "12px", "color": "#666", "marginBottom": "8px"}),
        dash_flows.DashFlows(
            id="smart-flow",
            nodes=smart_nodes,
            edges=smart_edges,
            smartHandles=True,
            style={"height": "550px", "border": "1px solid #ddd"},
            fitView=True,
            fitViewOptions={"padding": 0.15},
            showControls=True,
            showMiniMap=True,
            colorScheme="ocean",
        ),
    ], style={"marginBottom": "40px"}),

    html.Hr(),

    # Manual positioning example
    html.Div([
        html.H3("Manual Handle Positioning"),
        html.P(
            "You can also manually set sourcePosition and targetPosition in node data "
            "for precise control. This example creates a left-to-right horizontal flow."
        ),
        html.Pre(
            '{"label": "Process", "sourcePosition": "right", "targetPosition": "left"}',
            style={
                "background": "#f5f5f5",
                "padding": "8px 12px",
                "borderRadius": "4px",
                "fontSize": "12px",
            },
        ),
        dash_flows.DashFlows(
            id="manual-flow",
            nodes=manual_nodes,
            edges=manual_edges,
            style={"height": "250px", "border": "1px solid #ddd"},
            fitView=True,
            fitViewOptions={"padding": 0.3},
            showControls=True,
            showBackground=True,
        ),
    ]),
])


@callback(
    Output("smart-flow", "smartHandles"),
    Output("smart-status", "children"),
    Input("smart-toggle", "value"),
)
def toggle_smart_handles(value):
    enabled = "on" in (value or [])
    status = "smartHandles=True (edges route to closest side)" if enabled else "smartHandles=False (default top/bottom handles)"
    return enabled, status


if __name__ == "__main__":
    app.run(debug=True, port=8024)
