"""
Example 09: Viewport Controls and Fit View
==========================================
This example demonstrates viewport manipulation:
- Zoom in/out programmatically
- Pan to specific positions
- Fit view to content
- Lock/unlock viewport
- Get/set viewport state
"""

import dash
from dash import html, Input, Output, State, callback, ctx
import dash_flows
import dash_mantine_components as dmc
import json

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Create nodes spread across the canvas
nodes = [
    {"id": "1", "type": "default", "data": {"label": "Top Left"}, "position": {"x": 0, "y": 0}},
    {"id": "2", "type": "default", "data": {"label": "Top Right"}, "position": {"x": 800, "y": 0}},
    {"id": "3", "type": "default", "data": {"label": "Center"}, "position": {"x": 400, "y": 250}},
    {"id": "4", "type": "default", "data": {"label": "Bottom Left"}, "position": {"x": 0, "y": 500}},
    {"id": "5", "type": "default", "data": {"label": "Bottom Right"}, "position": {"x": 800, "y": 500}},
]

edges = [
    {"id": "e1-3", "source": "1", "target": "3"},
    {"id": "e2-3", "source": "2", "target": "3"},
    {"id": "e3-4", "source": "3", "target": "4"},
    {"id": "e3-5", "source": "3", "target": "5"},
]

app.layout = dmc.MantineProvider([
    html.H1("Viewport Controls Example"),
    html.P("Control the viewport programmatically."),

    dmc.Group([
        dmc.Button("Fit View", id="btn-fit-view", variant="filled"),
        dmc.Button("Zoom In", id="btn-zoom-in", variant="outline"),
        dmc.Button("Zoom Out", id="btn-zoom-out", variant="outline"),
        dmc.Button("Reset Zoom", id="btn-reset-zoom", variant="outline"),
    ], style={"marginBottom": 10}),

    dmc.Group([
        dmc.Button("Pan to Top Left", id="btn-pan-tl", variant="light", size="sm"),
        dmc.Button("Pan to Center", id="btn-pan-center", variant="light", size="sm"),
        dmc.Button("Pan to Bottom Right", id="btn-pan-br", variant="light", size="sm"),
    ], style={"marginBottom": 10}),

    dmc.Group([
        dmc.Switch(id="lock-zoom", label="Lock Zoom", checked=False),
        dmc.Switch(id="lock-pan", label="Lock Pan", checked=False),
        dmc.Switch(id="lock-drag", label="Lock Node Drag", checked=False),
    ], style={"marginBottom": 20}),

    html.Div(id="flow-viewport-container"),

    dmc.Space(h=20),

    dmc.Paper([
        dmc.Text("Current Viewport State:", fw=600),
        html.Pre(id="viewport-state", style={"fontSize": "11px"}),
    ], p="md", withBorder=True),
])

@callback(
    Output("flow-viewport-container", "children"),
    Input("lock-zoom", "checked"),
    Input("lock-pan", "checked"),
    Input("lock-drag", "checked"),
)
def update_flow_locks(lock_zoom, lock_pan, lock_drag):
    return dash_flows.DashFlows(
        id="viewport-flow",
        nodes=nodes,
        edges=edges,
        style={"height": "400px", "border": "1px solid #ddd"},
        fitView=True,
        showControls=True,
        # Viewport lock settings
        zoomOnScroll=not lock_zoom,
        zoomOnPinch=not lock_zoom,
        zoomOnDoubleClick=not lock_zoom,
        panOnDrag=not lock_pan,
        panOnScroll=not lock_pan,
        nodesDraggable=not lock_drag,
        # Zoom limits
        minZoom=0.1,
        maxZoom=4,
    )

# Clientside callback for viewport manipulation
app.clientside_callback(
    """
    function(fitClicks, zoomInClicks, zoomOutClicks, resetClicks, panTLClicks, panCenterClicks, panBRClicks) {
        const triggered = dash_clientside.callback_context.triggered;
        if (!triggered || triggered.length === 0) {
            return window.dash_clientside.no_update;
        }

        const btnId = triggered[0].prop_id.split('.')[0];

        // These would need to be handled by the component itself
        // This is a placeholder to show the concept
        switch(btnId) {
            case 'btn-fit-view':
                return {'action': 'fitView', 'options': {padding: 0.2}};
            case 'btn-zoom-in':
                return {'action': 'zoomIn', 'options': {}};
            case 'btn-zoom-out':
                return {'action': 'zoomOut', 'options': {}};
            case 'btn-reset-zoom':
                return {'action': 'setZoom', 'options': {zoom: 1}};
            case 'btn-pan-tl':
                return {'action': 'setCenter', 'options': {x: 0, y: 0, zoom: 1}};
            case 'btn-pan-center':
                return {'action': 'setCenter', 'options': {x: 450, y: 300, zoom: 1}};
            case 'btn-pan-br':
                return {'action': 'setCenter', 'options': {x: 900, y: 550, zoom: 1}};
            default:
                return window.dash_clientside.no_update;
        }
    }
    """,
    Output("viewport-flow", "viewportAction", allow_duplicate=True),
    Input("btn-fit-view", "n_clicks"),
    Input("btn-zoom-in", "n_clicks"),
    Input("btn-zoom-out", "n_clicks"),
    Input("btn-reset-zoom", "n_clicks"),
    Input("btn-pan-tl", "n_clicks"),
    Input("btn-pan-center", "n_clicks"),
    Input("btn-pan-br", "n_clicks"),
    prevent_initial_call=True,
)

@callback(
    Output("viewport-state", "children"),
    Input("viewport-flow", "viewport"),
)
def display_viewport(viewport):
    if not viewport:
        return "Viewport not available"
    return json.dumps(viewport, indent=2)

if __name__ == "__main__":
    app.run(debug=True, port=8068)