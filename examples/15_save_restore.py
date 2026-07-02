"""
Example 15: Save and Restore Flow State
=======================================
This example demonstrates how to:
- Export the current flow state to JSON
- Save the state to localStorage or download as file
- Restore a previously saved flow state
- Use viewport actions for programmatic control
"""

import dash
from dash import html, dcc, callback, Input, Output, State
import dash_flows
import json

app = dash.Dash(__name__)

# Initial nodes
initial_nodes = [
    {
        "id": "node-1",
        "type": "input",
        "data": {"label": "Data Source"},
        "position": {"x": 100, "y": 100},
    },
    {
        "id": "node-2",
        "type": "default",
        "data": {"label": "Transform"},
        "position": {"x": 100, "y": 250},
    },
    {
        "id": "node-3",
        "type": "default",
        "data": {"label": "Process"},
        "position": {"x": 300, "y": 250},
    },
    {
        "id": "node-4",
        "type": "output",
        "data": {"label": "Output"},
        "position": {"x": 200, "y": 400},
    },
]

# Initial edges
initial_edges = [
    {"id": "e1-2", "source": "node-1", "target": "node-2"},
    {"id": "e1-3", "source": "node-1", "target": "node-3"},
    {"id": "e2-4", "source": "node-2", "target": "node-4"},
    {"id": "e3-4", "source": "node-3", "target": "node-4"},
]

app.layout = html.Div([
    html.H1("Save and Restore Flow State"),
    html.P("Drag nodes around, add connections, then save or restore the flow state."),

    # Control buttons
    html.Div([
        html.Button("Export State", id="export-btn", n_clicks=0,
                   style={"marginRight": "10px", "padding": "10px 20px"}),
        html.Button("Download JSON", id="download-btn", n_clicks=0,
                   style={"marginRight": "10px", "padding": "10px 20px"}),
        html.Button("Restore from Saved", id="restore-btn", n_clicks=0,
                   style={"marginRight": "10px", "padding": "10px 20px"}),
        html.Button("Reset to Initial", id="reset-btn", n_clicks=0,
                   style={"marginRight": "10px", "padding": "10px 20px"}),
    ], style={"marginBottom": "10px"}),

    # Viewport action buttons
    html.Div([
        html.Button("Fit View", id="fit-view-btn", n_clicks=0,
                   style={"marginRight": "10px", "padding": "8px 16px"}),
        html.Button("Zoom In", id="zoom-in-btn", n_clicks=0,
                   style={"marginRight": "10px", "padding": "8px 16px"}),
        html.Button("Zoom Out", id="zoom-out-btn", n_clicks=0,
                   style={"marginRight": "10px", "padding": "8px 16px"}),
        html.Button("Focus Node 1", id="focus-node-btn", n_clicks=0,
                   style={"marginRight": "10px", "padding": "8px 16px"}),
    ], style={"marginBottom": "20px"}),

    # Download component
    dcc.Download(id="download-json"),

    # Hidden store for saved state
    dcc.Store(id="saved-state-store"),

    # Status display
    html.Div(id="status-display", style={
        "padding": "10px",
        "marginBottom": "10px",
        "background": "#f0f0f0",
        "borderRadius": "5px",
    }),

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
    ),

    # JSON preview
    html.H3("Exported State Preview:"),
    html.Pre(id="state-preview", style={
        "padding": "15px",
        "background": "#2d2d2d",
        "color": "#a6e22e",
        "borderRadius": "5px",
        "maxHeight": "300px",
        "overflow": "auto",
        "fontSize": "12px",
    }),
])


# Export state callback
@callback(
    Output("flow", "exportFlowState"),
    Input("export-btn", "n_clicks"),
    prevent_initial_call=True,
)
def trigger_export(n_clicks):
    return True


# Handle exported state
@callback(
    [Output("saved-state-store", "data"),
     Output("state-preview", "children"),
     Output("status-display", "children")],
    Input("flow", "flowState"),
    prevent_initial_call=True,
)
def handle_export(flow_state):
    if flow_state:
        json_str = json.dumps(flow_state, indent=2)
        return (
            flow_state,
            json_str,
            f"State exported! {len(flow_state.get('nodes', []))} nodes, {len(flow_state.get('edges', []))} edges"
        )
    return dash.no_update, dash.no_update, dash.no_update


# Download JSON callback
@callback(
    Output("download-json", "data"),
    Input("download-btn", "n_clicks"),
    State("saved-state-store", "data"),
    prevent_initial_call=True,
)
def download_json(n_clicks, saved_state):
    if saved_state:
        return dict(
            content=json.dumps(saved_state, indent=2),
            filename="flow_state.json",
        )
    return None


# Restore from saved state
@callback(
    Output("flow", "restoreFlowState"),
    Input("restore-btn", "n_clicks"),
    State("saved-state-store", "data"),
    prevent_initial_call=True,
)
def restore_state(n_clicks, saved_state):
    if saved_state:
        return saved_state
    return None


# Reset to initial state
@callback(
    Output("flow", "restoreFlowState", allow_duplicate=True),
    Input("reset-btn", "n_clicks"),
    prevent_initial_call=True,
)
def reset_state(n_clicks):
    return {
        "nodes": initial_nodes,
        "edges": initial_edges,
        "viewport": {"x": 0, "y": 0, "zoom": 1},
    }


# Viewport action callbacks
@callback(
    Output("flow", "viewportAction"),
    [Input("fit-view-btn", "n_clicks"),
     Input("zoom-in-btn", "n_clicks"),
     Input("zoom-out-btn", "n_clicks"),
     Input("focus-node-btn", "n_clicks")],
    prevent_initial_call=True,
)
def handle_viewport_action(fit_clicks, zoom_in_clicks, zoom_out_clicks, focus_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return None

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "fit-view-btn":
        return {"action": "fitView", "options": {"padding": 0.2, "duration": 500}}
    elif button_id == "zoom-in-btn":
        return {"action": "zoomIn", "options": {"duration": 300}}
    elif button_id == "zoom-out-btn":
        return {"action": "zoomOut", "options": {"duration": 300}}
    elif button_id == "focus-node-btn":
        return {"action": "focusNode", "nodeId": "node-1", "zoom": 2, "duration": 800}

    return None


if __name__ == "__main__":
    app.run(debug=True, port=8085)
