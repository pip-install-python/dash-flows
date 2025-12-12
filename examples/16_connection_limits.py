"""
Example 16: Connection Limits
=============================
This example demonstrates how to limit the number of connections:
- maxConnections: Total connections (source + target) for a node
- maxSourceConnections: Max outgoing connections from a node
- maxTargetConnections: Max incoming connections to a node
"""

import dash
from dash import html, callback, Input, Output
import dash_flows

app = dash.Dash(__name__)

# Nodes with connection limits
nodes = [
    # This node can only have 1 outgoing connection
    {
        "id": "single-out",
        "type": "input",
        "data": {
            "label": "Single Output (max 1)",
            "maxSourceConnections": 1,
        },
        "position": {"x": 50, "y": 50},
    },
    # This node can have unlimited outgoing connections
    {
        "id": "multi-out",
        "type": "input",
        "data": {
            "label": "Multi Output (unlimited)",
        },
        "position": {"x": 300, "y": 50},
    },
    # This node can only receive 1 incoming connection
    {
        "id": "single-in",
        "type": "default",
        "data": {
            "label": "Single Input (max 1)",
            "maxTargetConnections": 1,
        },
        "position": {"x": 100, "y": 200},
    },
    # This node can receive 2 incoming connections
    {
        "id": "dual-in",
        "type": "default",
        "data": {
            "label": "Dual Input (max 2)",
            "maxTargetConnections": 2,
        },
        "position": {"x": 350, "y": 200},
    },
    # This node has a total connection limit (in + out)
    {
        "id": "limited-total",
        "type": "default",
        "data": {
            "label": "Total Limit (max 2 total)",
            "maxConnections": 2,
        },
        "position": {"x": 225, "y": 350},
    },
    # Output nodes with no limits
    {
        "id": "output-1",
        "type": "output",
        "data": {"label": "Output 1"},
        "position": {"x": 100, "y": 500},
    },
    {
        "id": "output-2",
        "type": "output",
        "data": {"label": "Output 2"},
        "position": {"x": 350, "y": 500},
    },
]

# Initial edges showing some connections already made
edges = [
    # Single-out already has its one allowed connection
    {"id": "e1", "source": "single-out", "target": "single-in"},
]

app.layout = html.Div([
    html.H1("Connection Limits Example"),
    html.P([
        "Try to create connections between nodes. Notice that:",
        html.Ul([
            html.Li("'Single Output' can only connect to one target (already connected)"),
            html.Li("'Single Input' can only receive one connection (already has one)"),
            html.Li("'Dual Input' can receive up to 2 connections"),
            html.Li("'Total Limit' can have max 2 connections total (in + out combined)"),
            html.Li("'Multi Output' has no limits"),
        ]),
    ]),

    # Status display
    html.Div(id="connection-status", style={
        "padding": "10px",
        "marginBottom": "10px",
        "background": "#e8f4e8",
        "borderRadius": "5px",
    }),

    dash_flows.DashFlows(
        id="flow",
        nodes=nodes,
        edges=edges,
        style={"height": "600px", "border": "1px solid #ddd"},
        fitView=True,
        showControls=True,
        showMiniMap=True,
        showBackground=True,
        connectionRules={
            "allowSelfConnection": False,
            "allowDuplicateConnections": False,
        },
    ),
])


@callback(
    Output("connection-status", "children"),
    [Input("flow", "edges"),
     Input("flow", "lastConnection")],
)
def update_status(current_edges, last_connection):
    edge_count = len(current_edges) if current_edges else 0

    if last_connection:
        return f"Total connections: {edge_count} | Last connection: {last_connection.get('source', '')} -> {last_connection.get('target', '')}"

    return f"Total connections: {edge_count} | Drag from a handle to create a connection"


if __name__ == "__main__":
    app.run(debug=True, port=8086)
