"""
Embeddable twin of examples/18_export_image.py for the docs page.
Rendered via `.. exec::docs.persistence.ex18`.
"""
import dash
from dash import html, callback, Input, Output
import dash_flows
import dash_mantine_components as dmc

nodes = [
    {"id": "node-1", "type": "input", "data": {"label": "Data Input"}, "position": {"x": 100, "y": 50}},
    {"id": "node-2", "type": "default", "data": {"label": "Process"}, "position": {"x": 100, "y": 200}},
    {"id": "node-3", "type": "default", "data": {"label": "Transform"}, "position": {"x": 300, "y": 200}},
    {"id": "node-4", "type": "output", "data": {"label": "Output"}, "position": {"x": 200, "y": 350}},
]

edges = [
    {"id": "e1-2", "source": "node-1", "target": "node-2", "animated": True},
    {"id": "e1-3", "source": "node-1", "target": "node-3"},
    {"id": "e2-4", "source": "node-2", "target": "node-4", "label": "Result"},
    {"id": "e3-4", "source": "node-3", "target": "node-4"},
]

component = html.Div([
    dmc.Group([
        dmc.Button("Download PNG", id="ex18-btn-png", n_clicks=0, color="green"),
        dmc.Button("Download SVG", id="ex18-btn-svg", n_clicks=0, color="blue"),
        dmc.Button("Download JPEG", id="ex18-btn-jpeg", n_clicks=0, color="orange"),
        dmc.Button("High-Res PNG (4x)", id="ex18-btn-hires", n_clicks=0, color="grape"),
        dmc.Button("Transparent PNG", id="ex18-btn-transparent", n_clicks=0, color="gray"),
    ], gap="sm", mb="sm"),

    html.Div(
        id="ex18-export-status",
        children="Click a button to export the flow",
        style={
            "padding": "10px",
            "marginBottom": "10px",
            "borderRadius": "6px",
            "background": "var(--mantine-color-default-hover)",
        },
    ),

    dash_flows.DashFlows(
        id="ex18-flow",
        nodes=nodes,
        edges=edges,
        style={
            "height": "480px",
            "border": "1px solid var(--mantine-color-default-border)",
            "borderRadius": "8px",
        },
        fitView=True,
        showControls=True,
        showMiniMap=True,
        showBackground=True,
        backgroundVariant="dots",
    ),
])


# Handle export button clicks
@callback(
    Output("ex18-flow", "downloadImage"),
    Input("ex18-btn-png", "n_clicks"),
    Input("ex18-btn-svg", "n_clicks"),
    Input("ex18-btn-jpeg", "n_clicks"),
    Input("ex18-btn-hires", "n_clicks"),
    Input("ex18-btn-transparent", "n_clicks"),
    prevent_initial_call=True,
)
def handle_export(png_clicks, svg_clicks, jpeg_clicks, hires_clicks, transparent_clicks):
    triggered = dash.callback_context.triggered
    if not triggered:
        return None

    button_id = triggered[0]["prop_id"].split(".")[0]

    if button_id == "ex18-btn-png":
        return {"format": "png", "filename": "flow_diagram", "backgroundColor": "#ffffff"}
    elif button_id == "ex18-btn-svg":
        return {"format": "svg", "filename": "flow_vector", "backgroundColor": "#ffffff"}
    elif button_id == "ex18-btn-jpeg":
        return {"format": "jpeg", "filename": "flow_compressed", "quality": 0.8, "backgroundColor": "#ffffff"}
    elif button_id == "ex18-btn-hires":
        return {"format": "png", "filename": "flow_highres", "pixelRatio": 4, "backgroundColor": "#ffffff"}
    elif button_id == "ex18-btn-transparent":
        return {"format": "png", "filename": "flow_transparent", "backgroundColor": "transparent"}

    return None


# Show status when download completes
@callback(
    Output("ex18-export-status", "children"),
    Input("ex18-flow", "imageDownloaded"),
    Input("ex18-flow", "lastError"),
    prevent_initial_call=True,
)
def update_status(downloaded, error):
    triggered = dash.callback_context.triggered
    if not triggered:
        return dash.no_update

    trigger = triggered[0]["prop_id"]

    if "imageDownloaded" in trigger and downloaded:
        return f"Downloaded: {downloaded.get('filename', 'unknown')} ({downloaded.get('format', '').upper()})"
    elif "lastError" in trigger and error:
        if error.get("type") == "image-export":
            return f"Export failed: {error.get('message', 'Unknown error')}"

    return dash.no_update
