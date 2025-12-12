"""
Example 19: Copy and Paste
==========================
This example demonstrates how to:
- Copy selected nodes and edges
- Paste with position offset
- Use keyboard shortcuts for copy/paste
"""

import dash
from dash import html, callback, Input, Output, State
import dash_flows

app = dash.Dash(__name__)

# Initial nodes
initial_nodes = [
    {
        "id": "node-1",
        "type": "input",
        "data": {"label": "Source A"},
        "position": {"x": 100, "y": 100},
    },
    {
        "id": "node-2",
        "type": "default",
        "data": {"label": "Process"},
        "position": {"x": 100, "y": 250},
    },
    {
        "id": "node-3",
        "type": "output",
        "data": {"label": "Output"},
        "position": {"x": 100, "y": 400},
    },
]

initial_edges = [
    {"id": "e1-2", "source": "node-1", "target": "node-2"},
    {"id": "e2-3", "source": "node-2", "target": "node-3"},
]

button_style = {
    "padding": "10px 20px",
    "marginRight": "10px",
    "borderRadius": "6px",
    "border": "none",
    "cursor": "pointer",
    "fontWeight": "500",
    "fontSize": "14px",
}

app.layout = html.Div([
    html.H1("Copy and Paste Example"),
    html.P([
        "Select nodes (click or shift+drag), then use the buttons or keyboard shortcuts to copy/paste.",
        html.Br(),
        "Tip: Hold Shift and drag to select multiple nodes."
    ]),

    # Control buttons
    html.Div([
        html.Button(
            "Copy Selected (Ctrl+C)",
            id="btn-copy",
            n_clicks=0,
            style={**button_style, "background": "#4CAF50", "color": "white"}
        ),
        html.Button(
            "Paste (Ctrl+V)",
            id="btn-paste",
            n_clicks=0,
            style={**button_style, "background": "#2196F3", "color": "white"}
        ),
        html.Button(
            "Copy All",
            id="btn-copy-all",
            n_clicks=0,
            style={**button_style, "background": "#FF9800", "color": "white"}
        ),
    ], style={"marginBottom": "15px"}),

    # Status display
    html.Div(id="status", style={
        "padding": "10px",
        "marginBottom": "10px",
        "background": "#f0f0f0",
        "borderRadius": "5px",
    }, children="Select nodes and use Copy/Paste"),

    # Flow component
    dash_flows.DashFlows(
        id="flow",
        nodes=initial_nodes,
        edges=initial_edges,
        style={"height": "500px", "border": "1px solid #ddd"},
        fitView=True,
        showControls=True,
        showMiniMap=True,
        showBackground=True,
        selectionOnDrag=True,  # Enable drag selection
    ),
])


# Copy button handler
@callback(
    Output("flow", "copyAction"),
    Input("btn-copy", "n_clicks"),
    prevent_initial_call=True,
)
def handle_copy(n_clicks):
    return True


# Copy all button handler
@callback(
    Output("flow", "copyAction", allow_duplicate=True),
    Input("btn-copy-all", "n_clicks"),
    State("flow", "nodes"),
    prevent_initial_call=True,
)
def handle_copy_all(n_clicks, nodes):
    # Deselect all first (to trigger copy all behavior)
    return True


# Paste button handler
@callback(
    Output("flow", "pasteAction"),
    Input("btn-paste", "n_clicks"),
    prevent_initial_call=True,
)
def handle_paste(n_clicks):
    return {"offset": {"x": 100, "y": 50}}


# Update status based on clipboard and paste events
@callback(
    Output("status", "children"),
    [Input("flow", "clipboard"),
     Input("flow", "pastedElements"),
     Input("flow", "selectedNodes")],
)
def update_status(clipboard, pasted, selected):
    status_parts = []

    if selected:
        status_parts.append(f"Selected: {len(selected)} node(s)")
    else:
        status_parts.append("No nodes selected")

    if clipboard and clipboard.get("nodes"):
        status_parts.append(f" | Clipboard: {len(clipboard['nodes'])} node(s)")

    if pasted and pasted.get("nodeIds"):
        status_parts.append(f" | Just pasted: {len(pasted['nodeIds'])} node(s)")

    return "".join(status_parts) if status_parts else "Select nodes and use Copy/Paste"


# Client-side callback for keyboard shortcuts
app.clientside_callback(
    """
    function(id) {
        document.addEventListener('keydown', function(e) {
            // Ctrl+C or Cmd+C
            if ((e.ctrlKey || e.metaKey) && e.key === 'c' && !e.shiftKey) {
                // Don't interfere with normal copy in text inputs
                if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

                e.preventDefault();
                document.getElementById('btn-copy').click();
            }
            // Ctrl+V or Cmd+V
            if ((e.ctrlKey || e.metaKey) && e.key === 'v' && !e.shiftKey) {
                if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

                e.preventDefault();
                document.getElementById('btn-paste').click();
            }
        });
        return window.dash_clientside.no_update;
    }
    """,
    Output("status", "data-keyboard"),
    Input("status", "id"),
)


if __name__ == "__main__":
    app.run(debug=True, port=8089)
