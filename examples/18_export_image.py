"""
Example 18: Export Flow as Image
================================
This example demonstrates how to:
- Export the flow as PNG, SVG, or JPEG
- Configure export options (quality, background, resolution)
- Track when downloads complete
"""

import dash
from dash import html, callback, Input, Output, State
import dash_flows

app = dash.Dash(__name__)

# Sample nodes
nodes = [
    {
        "id": "node-1",
        "type": "input",
        "data": {"label": "Data Input"},
        "position": {"x": 100, "y": 50},
    },
    {
        "id": "node-2",
        "type": "default",
        "data": {"label": "Process"},
        "position": {"x": 100, "y": 200},
    },
    {
        "id": "node-3",
        "type": "default",
        "data": {"label": "Transform"},
        "position": {"x": 300, "y": 200},
    },
    {
        "id": "node-4",
        "type": "output",
        "data": {"label": "Output"},
        "position": {"x": 200, "y": 350},
    },
]

edges = [
    {"id": "e1-2", "source": "node-1", "target": "node-2", "animated": True},
    {"id": "e1-3", "source": "node-1", "target": "node-3"},
    {"id": "e2-4", "source": "node-2", "target": "node-4", "label": "Result"},
    {"id": "e3-4", "source": "node-3", "target": "node-4"},
]

button_style = {
    "padding": "10px 20px",
    "marginRight": "10px",
    "borderRadius": "6px",
    "border": "none",
    "cursor": "pointer",
    "fontWeight": "500",
}

app.layout = html.Div([
    html.H1("Export Flow as Image"),
    html.P("Click a button below to export the flow as an image file."),

    # Export buttons
    html.Div([
        html.Button(
            "Download PNG",
            id="btn-png",
            n_clicks=0,
            style={**button_style, "background": "#4CAF50", "color": "white"}
        ),
        html.Button(
            "Download SVG",
            id="btn-svg",
            n_clicks=0,
            style={**button_style, "background": "#2196F3", "color": "white"}
        ),
        html.Button(
            "Download JPEG",
            id="btn-jpeg",
            n_clicks=0,
            style={**button_style, "background": "#FF9800", "color": "white"}
        ),
        html.Button(
            "High-Res PNG (4x)",
            id="btn-hires",
            n_clicks=0,
            style={**button_style, "background": "#9C27B0", "color": "white"}
        ),
        html.Button(
            "Transparent PNG",
            id="btn-transparent",
            n_clicks=0,
            style={**button_style, "background": "#607D8B", "color": "white"}
        ),
    ], style={"marginBottom": "20px"}),

    # Status display
    html.Div(id="export-status", style={
        "padding": "10px",
        "marginBottom": "10px",
        "background": "#f0f0f0",
        "borderRadius": "5px",
    }, children="Click a button to export the flow"),

    # Flow component
    dash_flows.DashFlows(
        id="flow",
        nodes=nodes,
        edges=edges,
        style={"height": "500px", "border": "1px solid #ddd"},
        fitView=True,
        showControls=True,
        showMiniMap=True,
        showBackground=True,
        backgroundVariant="dots",
    ),
])


# Handle export button clicks
@callback(
    Output("flow", "downloadImage"),
    [Input("btn-png", "n_clicks"),
     Input("btn-svg", "n_clicks"),
     Input("btn-jpeg", "n_clicks"),
     Input("btn-hires", "n_clicks"),
     Input("btn-transparent", "n_clicks")],
    prevent_initial_call=True,
)
def handle_export(png_clicks, svg_clicks, jpeg_clicks, hires_clicks, transparent_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return None

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "btn-png":
        return {
            "format": "png",
            "filename": "flow_diagram",
            "backgroundColor": "#ffffff",
        }
    elif button_id == "btn-svg":
        return {
            "format": "svg",
            "filename": "flow_vector",
            "backgroundColor": "#ffffff",
        }
    elif button_id == "btn-jpeg":
        return {
            "format": "jpeg",
            "filename": "flow_compressed",
            "quality": 0.8,
            "backgroundColor": "#ffffff",
        }
    elif button_id == "btn-hires":
        return {
            "format": "png",
            "filename": "flow_highres",
            "pixelRatio": 4,
            "backgroundColor": "#ffffff",
        }
    elif button_id == "btn-transparent":
        return {
            "format": "png",
            "filename": "flow_transparent",
            "backgroundColor": "transparent",
        }

    return None


# Show status when download completes
@callback(
    Output("export-status", "children"),
    [Input("flow", "imageDownloaded"),
     Input("flow", "lastError")],
    prevent_initial_call=True,
)
def update_status(downloaded, error):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update

    trigger = ctx.triggered[0]["prop_id"]

    if "imageDownloaded" in trigger and downloaded:
        return f"Downloaded: {downloaded.get('filename', 'unknown')} ({downloaded.get('format', '').upper()})"
    elif "lastError" in trigger and error:
        if error.get("type") == "image-export":
            return f"Export failed: {error.get('message', 'Unknown error')}"

    return dash.no_update


if __name__ == "__main__":
    app.run(debug=True, port=8088)
