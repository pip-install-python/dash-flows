"""
Embeddable twin of examples/17_drag_and_drop.py for the docs page.
Rendered via `.. exec::docs.drag_drop.ex17`.
"""
import json
import uuid

import dash
from dash import html, callback, clientside_callback, Input, Output, State
import dash_flows

# Sidebar styles
sidebar_style = {
    "width": "200px",
    "padding": "15px",
    "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "borderRadius": "12px",
    "marginRight": "15px",
}

draggable_item_style = {
    "padding": "12px",
    "marginBottom": "10px",
    "background": "var(--mantine-color-body)",
    "borderRadius": "8px",
    "cursor": "grab",
    "textAlign": "center",
    "fontWeight": "500",
    "color": "var(--mantine-color-text)",
    "boxShadow": "0 2px 8px rgba(0,0,0,0.15)",
    "transition": "transform 0.2s, box-shadow 0.2s",
}

# Initial nodes
initial_nodes = [
    {
        "id": "start",
        "type": "input",
        "data": {"label": "Start Here"},
        "position": {"x": 250, "y": 50},
    },
]

component = html.Div(
    id="ex17-palette",
    children=[
        html.Div([
            # Sidebar with draggable items
            html.Div([
                html.H4("Node Palette", style={"color": "white", "marginBottom": "15px"}),

                html.Div(
                    "Input Node",
                    id="ex17-drag-input",
                    draggable="true",
                    style=draggable_item_style,
                    **{"data-node-type": "input", "data-node-label": "Input"}
                ),
                html.Div(
                    "Process Node",
                    id="ex17-drag-default",
                    draggable="true",
                    style=draggable_item_style,
                    **{"data-node-type": "default", "data-node-label": "Process"}
                ),
                html.Div(
                    "Output Node",
                    id="ex17-drag-output",
                    draggable="true",
                    style=draggable_item_style,
                    **{"data-node-type": "output", "data-node-label": "Output"}
                ),
                html.Div(
                    "Resizable Node",
                    id="ex17-drag-resizable",
                    draggable="true",
                    style=draggable_item_style,
                    **{"data-node-type": "resizable", "data-node-label": "Resizable"}
                ),
            ], style=sidebar_style),

            # Flow canvas
            html.Div([
                dash_flows.DashFlows(
                    id="ex17-flow",
                    nodes=initial_nodes,
                    edges=[],
                    style={
                        "height": "480px",
                        "border": "1px solid var(--mantine-color-default-border)",
                        "borderRadius": "8px",
                    },
                    fitView=True,
                    showControls=True,
                    showMiniMap=True,
                    showBackground=True,
                ),
            ], style={"flex": "1"}),
        ], style={"display": "flex", "gap": "15px"}),

        # Status display
        html.Div(id="ex17-drop-status", style={
            "marginTop": "15px",
            "padding": "10px",
            "background": "var(--mantine-color-default)",
            "color": "var(--mantine-color-text)",
            "borderRadius": "5px",
        }),

        html.H4("droppedNode payload", style={"marginTop": "15px"}),
        html.Pre(
            id="ex17-dropped-node-json",
            children="Drag a node from the palette and drop it onto the canvas...",
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
    ],
)


# Client-side callback wires up native HTML5 drag events on the palette items,
# scoped to this example's container so it doesn't affect other demos on the page.
clientside_callback(
    """
    function(n) {
        const container = document.getElementById('ex17-palette');
        if (!container) {
            return window.dash_clientside.no_update;
        }
        const draggables = container.querySelectorAll('[draggable="true"]');
        draggables.forEach(item => {
            item.ondragstart = function(e) {
                const nodeType = this.getAttribute('data-node-type');
                const nodeLabel = this.getAttribute('data-node-label');
                const payload = JSON.stringify({
                    type: nodeType,
                    data: { label: nodeLabel }
                });
                e.dataTransfer.setData('application/reactflow', payload);
                e.dataTransfer.setData('text/plain', payload);
                e.dataTransfer.effectAllowed = 'move';
            };
        });
        return window.dash_clientside.no_update;
    }
    """,
    Output("ex17-drop-status", "data-init"),
    Input("ex17-drop-status", "id"),
)


# Handle dropped node - create new node
@callback(
    [Output("ex17-flow", "nodes"),
     Output("ex17-drop-status", "children"),
     Output("ex17-dropped-node-json", "children")],
    Input("ex17-flow", "droppedNode"),
    State("ex17-flow", "nodes"),
    prevent_initial_call=True,
)
def handle_drop(dropped_node, current_nodes):
    if not dropped_node:
        return dash.no_update, dash.no_update, dash.no_update

    # Generate unique ID for new node
    new_id = f"node-{str(uuid.uuid4())[:8]}"

    # Create new node
    new_node = {
        "id": new_id,
        "type": dropped_node.get("type", "default"),
        "data": dropped_node.get("data", {"label": "New Node"}),
        "position": dropped_node.get("position", {"x": 100, "y": 100}),
    }

    # Add resizable node specific properties
    if new_node["type"] == "resizable":
        new_node["data"]["handles"] = [
            {"id": "top", "type": "target", "position": "top"},
            {"id": "bottom", "type": "source", "position": "bottom"},
        ]
        new_node["style"] = {"width": 200, "height": 100}

    # Append to existing nodes
    updated_nodes = current_nodes + [new_node] if current_nodes else [new_node]

    status = (
        f"Created new {new_node['type']} node '{new_node['data'].get('label', 'Node')}' "
        f"at ({dropped_node['position']['x']:.0f}, {dropped_node['position']['y']:.0f})"
    )

    return updated_nodes, status, json.dumps(dropped_node, indent=2)
