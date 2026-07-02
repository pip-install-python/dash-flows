"""
Example 17: Drag and Drop from Sidebar
======================================
This example demonstrates how to:
- Create a sidebar with draggable node templates
- Drop nodes onto the flow canvas
- Create new nodes at the drop position
"""

import dash
from dash import html, callback, Input, Output, State
import dash_flows
import uuid

app = dash.Dash(__name__)

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
    "background": "rgba(255, 255, 255, 0.9)",
    "borderRadius": "8px",
    "cursor": "grab",
    "textAlign": "center",
    "fontWeight": "500",
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

app.layout = html.Div([
    html.H1("Drag and Drop Example"),
    html.P("Drag node types from the sidebar and drop them onto the canvas."),

    html.Div([
        # Sidebar with draggable items
        html.Div([
            html.H4("Node Palette", style={"color": "white", "marginBottom": "15px"}),

            # Input node
            html.Div(
                "Input Node",
                id="drag-input",
                draggable="true",
                style=draggable_item_style,
                **{"data-node-type": "input", "data-node-label": "Input"}
            ),

            # Default node
            html.Div(
                "Process Node",
                id="drag-default",
                draggable="true",
                style=draggable_item_style,
                **{"data-node-type": "default", "data-node-label": "Process"}
            ),

            # Output node
            html.Div(
                "Output Node",
                id="drag-output",
                draggable="true",
                style=draggable_item_style,
                **{"data-node-type": "output", "data-node-label": "Output"}
            ),

            # Resizable node
            html.Div(
                "Resizable Node",
                id="drag-resizable",
                draggable="true",
                style=draggable_item_style,
                **{"data-node-type": "resizable", "data-node-label": "Resizable"}
            ),
        ], style=sidebar_style),

        # Flow canvas
        html.Div([
            dash_flows.DashFlows(
                id="flow",
                nodes=initial_nodes,
                edges=[],
                style={"height": "500px", "border": "2px dashed #ccc", "borderRadius": "8px"},
                fitView=True,
                showControls=True,
                showMiniMap=True,
                showBackground=True,
            ),
        ], style={"flex": "1"}),
    ], style={"display": "flex", "gap": "15px"}),

    # Status display
    html.Div(id="drop-status", style={
        "marginTop": "15px",
        "padding": "10px",
        "background": "#f0f0f0",
        "borderRadius": "5px",
    }),

    # Hidden client-side callback script
    html.Script('''
        document.addEventListener('DOMContentLoaded', function() {
            const draggables = document.querySelectorAll('[draggable="true"]');
            draggables.forEach(item => {
                item.addEventListener('dragstart', function(e) {
                    const nodeType = this.getAttribute('data-node-type');
                    const nodeLabel = this.getAttribute('data-node-label');
                    e.dataTransfer.setData('application/reactflow', JSON.stringify({
                        type: nodeType,
                        data: { label: nodeLabel }
                    }));
                    e.dataTransfer.effectAllowed = 'move';
                });
            });
        });
    '''),
])


# Client-side callback to handle drag start
app.clientside_callback(
    """
    function(n) {
        // Set up drag events for all draggable items
        const draggables = document.querySelectorAll('[draggable="true"]');
        draggables.forEach(item => {
            item.ondragstart = function(e) {
                const nodeType = this.getAttribute('data-node-type');
                const nodeLabel = this.getAttribute('data-node-label');
                e.dataTransfer.setData('application/reactflow', JSON.stringify({
                    type: nodeType,
                    data: { label: nodeLabel }
                }));
                e.dataTransfer.setData('text/plain', JSON.stringify({
                    type: nodeType,
                    data: { label: nodeLabel }
                }));
                e.dataTransfer.effectAllowed = 'move';
            };
        });
        return window.dash_clientside.no_update;
    }
    """,
    Output("drop-status", "data-init"),
    Input("drop-status", "id"),
)


# Handle dropped node - create new node
@callback(
    [Output("flow", "nodes"),
     Output("drop-status", "children")],
    Input("flow", "droppedNode"),
    State("flow", "nodes"),
    prevent_initial_call=True,
)
def handle_drop(dropped_node, current_nodes):
    if not dropped_node:
        return dash.no_update, dash.no_update

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

    status = f"Created new {new_node['type']} node '{new_node['data'].get('label', 'Node')}' at ({dropped_node['position']['x']:.0f}, {dropped_node['position']['y']:.0f})"

    return updated_nodes, status


if __name__ == "__main__":
    app.run(debug=True, port=8087)
