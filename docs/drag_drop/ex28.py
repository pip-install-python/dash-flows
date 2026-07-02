"""
Embeddable twin of examples/28_add_node_on_drop.py for the docs page.
Rendered via `.. exec::docs.drag_drop.ex28`.
"""
import json

from dash import html, callback, Input, Output
import dash_flows

initial_nodes = [
    {
        "id": "start",
        "type": "input",
        "data": {"label": "Start Here", "sublabel": "Drag from a handle"},
        "position": {"x": 250, "y": 50},
    },
]

initial_edges = []

component = html.Div([
    html.P(
        "Drag from any handle and release on empty canvas to create a new node. "
        "The new node is automatically connected to the source."
    ),
    dash_flows.DashFlows(
        id="ex28-drop-flow",
        nodes=initial_nodes,
        edges=initial_edges,
        addNodeOnEdgeDrop=True,
        style={
            "height": "480px",
            "border": "1px solid var(--mantine-color-default-border)",
            "borderRadius": "8px",
        },
        fitView=True,
        showControls=True,
        showBackground=True,
        showMiniMap=True,
        backgroundVariant="dots",
        colorScheme="forest",
    ),
    html.Div([
        html.H4("Edge Drop Events", style={"marginTop": "16px"}),
        html.Pre(
            id="ex28-drop-info",
            children="Drag from a handle and drop on empty canvas...",
            style={
                "background": "var(--mantine-color-default)",
                "color": "var(--mantine-color-text)",
                "padding": "12px",
                "borderRadius": "6px",
                "fontSize": "12px",
                "maxHeight": "200px",
                "overflow": "auto",
            },
        ),
    ]),
    html.Div([
        html.H4("Node Connections"),
        html.Pre(
            id="ex28-connections-info",
            children="No connections yet.",
            style={
                "background": "var(--mantine-color-default)",
                "color": "var(--mantine-color-text)",
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
    Output("ex28-drop-info", "children"),
    Input("ex28-drop-flow", "edgeDroppedNode"),
)
def show_drop_event(dropped):
    if not dropped:
        return "Drag from a handle and drop on empty canvas..."
    return json.dumps(dropped, indent=2)


@callback(
    Output("ex28-connections-info", "children"),
    Input("ex28-drop-flow", "nodeConnections"),
)
def show_connections(connections):
    if not connections:
        return "No connections yet."
    return json.dumps(connections, indent=2)
