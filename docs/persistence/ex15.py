"""
Embeddable twin of examples/15_save_restore.py for the docs page.
Rendered via `.. exec::docs.persistence.ex15`.
"""
import json

import dash
from dash import html, dcc, callback, Input, Output, State
import dash_flows
import dash_mantine_components as dmc

initial_nodes = [
    {"id": "node-1", "type": "input", "data": {"label": "Data Source"}, "position": {"x": 100, "y": 100}},
    {"id": "node-2", "type": "default", "data": {"label": "Transform"}, "position": {"x": 100, "y": 250}},
    {"id": "node-3", "type": "default", "data": {"label": "Process"}, "position": {"x": 300, "y": 250}},
    {"id": "node-4", "type": "output", "data": {"label": "Output"}, "position": {"x": 200, "y": 400}},
]

initial_edges = [
    {"id": "e1-2", "source": "node-1", "target": "node-2"},
    {"id": "e1-3", "source": "node-1", "target": "node-3"},
    {"id": "e2-4", "source": "node-2", "target": "node-4"},
    {"id": "e3-4", "source": "node-3", "target": "node-4"},
]

component = html.Div([
    dmc.Group([
        dmc.Button("Export State", id="ex15-export-btn", n_clicks=0, variant="light", size="sm"),
        dmc.Button("Download JSON", id="ex15-download-btn", n_clicks=0, variant="default", size="sm"),
        dmc.Button("Restore from Saved", id="ex15-restore-btn", n_clicks=0, variant="default", size="sm"),
        dmc.Button("Reset to Initial", id="ex15-reset-btn", n_clicks=0, variant="default", color="red", size="sm"),
    ], gap="sm", mb="xs"),

    dmc.Group([
        dmc.Button("Fit View", id="ex15-fit-view-btn", n_clicks=0, variant="default", size="sm"),
        dmc.Button("Zoom In", id="ex15-zoom-in-btn", n_clicks=0, variant="default", size="sm"),
        dmc.Button("Zoom Out", id="ex15-zoom-out-btn", n_clicks=0, variant="default", size="sm"),
        dmc.Button("Focus Node 1", id="ex15-focus-node-btn", n_clicks=0, variant="default", size="sm"),
    ], gap="sm", mb="md"),

    dcc.Download(id="ex15-download-json"),
    dcc.Store(id="ex15-saved-state-store"),

    html.Div(
        id="ex15-status-display",
        children="Drag nodes around, then click Export State to capture a snapshot.",
        style={
            "padding": "10px",
            "marginBottom": "10px",
            "borderRadius": "6px",
            "background": "var(--mantine-color-default-hover)",
        },
    ),

    dash_flows.DashFlows(
        id="ex15-flow",
        nodes=initial_nodes,
        edges=initial_edges,
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

    html.H4("Exported State Preview", style={"marginTop": "16px", "marginBottom": "8px"}),
    html.Pre(id="ex15-state-preview", style={
        "padding": "12px",
        "background": "#2d2d2d",
        "color": "#a6e22e",
        "borderRadius": "6px",
        "maxHeight": "220px",
        "overflow": "auto",
        "fontSize": "12px",
    }),
])


# Export state callback
@callback(
    Output("ex15-flow", "exportFlowState"),
    Input("ex15-export-btn", "n_clicks"),
    prevent_initial_call=True,
)
def trigger_export(n_clicks):
    return True


# Handle exported state
@callback(
    Output("ex15-saved-state-store", "data"),
    Output("ex15-state-preview", "children"),
    Output("ex15-status-display", "children"),
    Input("ex15-flow", "flowState"),
    prevent_initial_call=True,
)
def handle_export(flow_state):
    if flow_state:
        json_str = json.dumps(flow_state, indent=2)
        return (
            flow_state,
            json_str,
            f"State exported! {len(flow_state.get('nodes', []))} nodes, {len(flow_state.get('edges', []))} edges",
        )
    return dash.no_update, dash.no_update, dash.no_update


# Download JSON callback
@callback(
    Output("ex15-download-json", "data"),
    Input("ex15-download-btn", "n_clicks"),
    State("ex15-saved-state-store", "data"),
    prevent_initial_call=True,
)
def download_json(n_clicks, saved_state):
    if saved_state:
        return dict(content=json.dumps(saved_state, indent=2), filename="flow_state.json")
    return None


# Restore from saved state
@callback(
    Output("ex15-flow", "restoreFlowState"),
    Input("ex15-restore-btn", "n_clicks"),
    State("ex15-saved-state-store", "data"),
    prevent_initial_call=True,
)
def restore_state(n_clicks, saved_state):
    if saved_state:
        return saved_state
    return None


# Reset to initial state
@callback(
    Output("ex15-flow", "restoreFlowState", allow_duplicate=True),
    Input("ex15-reset-btn", "n_clicks"),
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
    Output("ex15-flow", "viewportAction"),
    Input("ex15-fit-view-btn", "n_clicks"),
    Input("ex15-zoom-in-btn", "n_clicks"),
    Input("ex15-zoom-out-btn", "n_clicks"),
    Input("ex15-focus-node-btn", "n_clicks"),
    prevent_initial_call=True,
)
def handle_viewport_action(fit_clicks, zoom_in_clicks, zoom_out_clicks, focus_clicks):
    triggered = dash.callback_context.triggered
    if not triggered:
        return None

    button_id = triggered[0]["prop_id"].split(".")[0]

    if button_id == "ex15-fit-view-btn":
        return {"action": "fitView", "options": {"padding": 0.2, "duration": 500}}
    elif button_id == "ex15-zoom-in-btn":
        return {"action": "zoomIn", "options": {"duration": 300}}
    elif button_id == "ex15-zoom-out-btn":
        return {"action": "zoomOut", "options": {"duration": 300}}
    elif button_id == "ex15-focus-node-btn":
        return {"action": "focusNode", "nodeId": "node-1", "zoom": 2, "duration": 800}

    return None
