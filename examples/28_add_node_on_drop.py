"""
Example 28: Add Node on Edge Drop
===================================
Demonstrates creating new nodes by dragging a connection from a handle
and dropping it on empty canvas. A new default node is created at the
drop position and automatically connected.
"""

import dash
from dash import html, callback, Input, Output, State
import dash_flows
import json

app = dash.Dash(__name__)

initial_nodes = [
    {
        "id": "start",
        "type": "input",
        "data": {"label": "Start Here", "sublabel": "Drag from a handle"},
        "position": {"x": 250, "y": 50},
    },
]

initial_edges = []

app.layout = html.Div([
    html.H1("Add Node on Edge Drop"),
    html.P(
        "Drag from any handle and release on empty canvas to create a new node. "
        "The new node is automatically connected to the source."
    ),
    dash_flows.DashFlows(
        id="drop-flow",
        nodes=initial_nodes,
        edges=initial_edges,
        addNodeOnEdgeDrop=True,
        style={"height": "600px", "border": "1px solid #ddd"},
        fitView=True,
        showControls=True,
        showBackground=True,
        showMiniMap=True,
        backgroundVariant="dots",
        colorScheme="forest",
    ),
    html.Div([
        html.H3("Edge Drop Events", style={"marginTop": "16px"}),
        html.Pre(
            id="drop-info",
            style={
                "background": "#f5f5f5",
                "padding": "12px",
                "borderRadius": "6px",
                "fontSize": "12px",
                "maxHeight": "200px",
                "overflow": "auto",
            },
        ),
    ]),
    html.Div([
        html.H3("Node Connections"),
        html.Pre(
            id="connections-info",
            style={
                "background": "#f5f5f5",
                "padding": "12px",
                "borderRadius": "6px",
                "fontSize": "12px",
                "maxHeight": "200px",
                "overflow": "auto",
            },
        ),
    ]),
])


@callback(
    Output("drop-info", "children"),
    Input("drop-flow", "edgeDroppedNode"),
)
def show_drop_event(dropped):
    if not dropped:
        return "Drag from a handle and drop on empty canvas..."
    return json.dumps(dropped, indent=2)


@callback(
    Output("connections-info", "children"),
    Input("drop-flow", "nodeConnections"),
)
def show_connections(connections):
    if not connections:
        return "No connections yet."
    return json.dumps(connections, indent=2)


if __name__ == "__main__":
    app.run(debug=True, port=8028)
