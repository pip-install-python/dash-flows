"""
Embeddable twin of examples/09_viewport_controls.py for the docs page.
Rendered via `.. exec::docs.canvas.ex09`.
"""
import json

from dash import html, Input, Output, callback, clientside_callback
import dash_flows
import dash_mantine_components as dmc

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

component = html.Div([
    dmc.Group([
        dmc.Button("Fit View", id="ex09-btn-fit-view", variant="filled"),
        dmc.Button("Zoom In", id="ex09-btn-zoom-in", variant="outline"),
        dmc.Button("Zoom Out", id="ex09-btn-zoom-out", variant="outline"),
        dmc.Button("Reset Zoom", id="ex09-btn-reset-zoom", variant="outline"),
    ], style={"marginBottom": 10}),

    dmc.Group([
        dmc.Button("Pan to Top Left", id="ex09-btn-pan-tl", variant="light", size="sm"),
        dmc.Button("Pan to Center", id="ex09-btn-pan-center", variant="light", size="sm"),
        dmc.Button("Pan to Bottom Right", id="ex09-btn-pan-br", variant="light", size="sm"),
    ], style={"marginBottom": 10}),

    dmc.Group([
        dmc.Switch(id="ex09-lock-zoom", label="Lock Zoom", checked=False),
        dmc.Switch(id="ex09-lock-pan", label="Lock Pan", checked=False),
        dmc.Switch(id="ex09-lock-drag", label="Lock Node Drag", checked=False),
    ], style={"marginBottom": 20}),

    html.Div(id="ex09-flow-viewport-container"),

    dmc.Space(h=20),

    dmc.Paper([
        dmc.Text("Current Viewport State:", fw=600),
        html.Pre(id="ex09-viewport-state", style={"fontSize": "11px"}),
    ], p="md", withBorder=True),
])


@callback(
    Output("ex09-flow-viewport-container", "children"),
    Input("ex09-lock-zoom", "checked"),
    Input("ex09-lock-pan", "checked"),
    Input("ex09-lock-drag", "checked"),
)
def update_flow_locks(lock_zoom, lock_pan, lock_drag):
    return dash_flows.DashFlows(
        id="ex09-viewport-flow",
        nodes=nodes,
        edges=edges,
        style={
            "height": "440px",
            "border": "1px solid var(--mantine-color-default-border)",
            "borderRadius": "8px",
        },
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
clientside_callback(
    """
    function(fitClicks, zoomInClicks, zoomOutClicks, resetClicks, panTLClicks, panCenterClicks, panBRClicks) {
        const triggered = dash_clientside.callback_context.triggered;
        if (!triggered || triggered.length === 0) {
            return window.dash_clientside.no_update;
        }

        const btnId = triggered[0].prop_id.split('.')[0];

        switch(btnId) {
            case 'ex09-btn-fit-view':
                return {'action': 'fitView', 'options': {padding: 0.2}};
            case 'ex09-btn-zoom-in':
                return {'action': 'zoomIn', 'options': {}};
            case 'ex09-btn-zoom-out':
                return {'action': 'zoomOut', 'options': {}};
            case 'ex09-btn-reset-zoom':
                return {'action': 'setZoom', 'zoom': 1, 'options': {}};
            case 'ex09-btn-pan-tl':
                return {'action': 'setCenter', 'x': 0, 'y': 0, 'options': {zoom: 1, duration: 500}};
            case 'ex09-btn-pan-center':
                return {'action': 'setCenter', 'x': 450, 'y': 300, 'options': {zoom: 1, duration: 500}};
            case 'ex09-btn-pan-br':
                return {'action': 'setCenter', 'x': 900, 'y': 550, 'options': {zoom: 1, duration: 500}};
            default:
                return window.dash_clientside.no_update;
        }
    }
    """,
    Output("ex09-viewport-flow", "viewportAction", allow_duplicate=True),
    Input("ex09-btn-fit-view", "n_clicks"),
    Input("ex09-btn-zoom-in", "n_clicks"),
    Input("ex09-btn-zoom-out", "n_clicks"),
    Input("ex09-btn-reset-zoom", "n_clicks"),
    Input("ex09-btn-pan-tl", "n_clicks"),
    Input("ex09-btn-pan-center", "n_clicks"),
    Input("ex09-btn-pan-br", "n_clicks"),
    prevent_initial_call=True,
)


@callback(
    Output("ex09-viewport-state", "children"),
    Input("ex09-viewport-flow", "viewport"),
)
def display_viewport(viewport):
    if not viewport:
        return "Viewport not available"
    return json.dumps(viewport, indent=2)
