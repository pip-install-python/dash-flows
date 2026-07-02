"""
Example 31: Animated Layout Transitions
========================================
Demonstrates smooth animated transitions when switching between
different ELK layout algorithms. Nodes interpolate from their current
positions to the new layout positions using an ease-out cubic curve.
"""

import json
import dash
from dash import html, dcc, callback, Input, Output, State
import dash_flows

app = dash.Dash(__name__)

# Create a pipeline-like graph
nodes = [
    {"id": "src-1",  "type": "input",   "data": {"label": "Source A"},   "position": {"x": 0,   "y": 0}},
    {"id": "src-2",  "type": "input",   "data": {"label": "Source B"},   "position": {"x": 0,   "y": 100}},
    {"id": "proc-1", "type": "default", "data": {"label": "Validate"},   "position": {"x": 200, "y": 0}},
    {"id": "proc-2", "type": "default", "data": {"label": "Transform"},  "position": {"x": 200, "y": 100}},
    {"id": "proc-3", "type": "default", "data": {"label": "Enrich"},     "position": {"x": 200, "y": 200}},
    {"id": "merge",  "type": "default", "data": {"label": "Merge"},      "position": {"x": 400, "y": 100}},
    {"id": "filter", "type": "default", "data": {"label": "Filter"},     "position": {"x": 600, "y": 50}},
    {"id": "agg",    "type": "default", "data": {"label": "Aggregate"},  "position": {"x": 600, "y": 150}},
    {"id": "out-1",  "type": "output",  "data": {"label": "Dashboard"},  "position": {"x": 800, "y": 50}},
    {"id": "out-2",  "type": "output",  "data": {"label": "Report"},     "position": {"x": 800, "y": 150}},
]

edges = [
    {"id": "e1",  "source": "src-1",  "target": "proc-1"},
    {"id": "e2",  "source": "src-1",  "target": "proc-2"},
    {"id": "e3",  "source": "src-2",  "target": "proc-2"},
    {"id": "e4",  "source": "src-2",  "target": "proc-3"},
    {"id": "e5",  "source": "proc-1", "target": "merge"},
    {"id": "e6",  "source": "proc-2", "target": "merge"},
    {"id": "e7",  "source": "proc-3", "target": "merge"},
    {"id": "e8",  "source": "merge",  "target": "filter"},
    {"id": "e9",  "source": "merge",  "target": "agg"},
    {"id": "e10", "source": "filter", "target": "out-1"},
    {"id": "e11", "source": "agg",    "target": "out-2"},
]

# Layout presets
layouts = {
    "layered-lr": {
        "label": "← → Layered (LR)",
        "options": json.dumps({
            "elk.algorithm": "layered",
            "elk.direction": "RIGHT",
            "elk.spacing.nodeNode": "50",
            "elk.layered.spacing.nodeNodeBetweenLayers": "80",
        }),
    },
    "layered-tb": {
        "label": "↓ Layered (TB)",
        "options": json.dumps({
            "elk.algorithm": "layered",
            "elk.direction": "DOWN",
            "elk.spacing.nodeNode": "50",
            "elk.layered.spacing.nodeNodeBetweenLayers": "80",
        }),
    },
    "force": {
        "label": "⚛ Force",
        "options": json.dumps({
            "elk.algorithm": "force",
            "elk.spacing.nodeNode": "80",
            "elk.force.iterations": "300",
        }),
    },
    "radial": {
        "label": "◎ Radial",
        "options": json.dumps({
            "elk.algorithm": "radial",
            "elk.spacing.nodeNode": "60",
        }),
    },
}

_btn_base = {
    "padding": "8px 16px", "border": "1px solid #ddd",
    "borderRadius": "6px", "cursor": "pointer",
    "fontSize": "13px", "fontWeight": "500", "transition": "all 0.15s",
}
_btn_active = {**_btn_base, "background": "#3b82f6", "color": "white", "borderColor": "#3b82f6"}
_btn_idle   = {**_btn_base, "background": "#fff", "color": "#374151"}

app.layout = html.Div([
    html.H2("Animated Layout Transitions"),
    html.P(
        "Click a layout to animate all nodes to their new positions. "
        "The viewport auto-fits after each transition.",
        style={"color": "#666"},
    ),

    html.Div([
        html.Button(info["label"], id=f"btn-{key}", style=_btn_idle)
        for key, info in layouts.items()
    ] + [
        html.Span(id="active-layout-label", style={
            "padding": "8px 14px", "background": "#f0f0f0",
            "borderRadius": "6px", "fontSize": "12px", "color": "#555",
        }),
    ], style={"display": "flex", "gap": "8px", "alignItems": "center", "marginBottom": "12px"}),

    dcc.Store(id="active-layout-store", data=""),

    dash_flows.DashFlows(
        id="animated-layout-flow",
        nodes=nodes,
        edges=edges,
        fitView=True,
        animateLayout=True,
        animateLayoutDuration=500,
        showControls=True,
        showMiniMap=True,
        showBackground=True,
        style={"height": "550px"},
    ),
], style={"padding": "20px"})


@callback(
    Output("animated-layout-flow", "layoutOptions"),
    Output("animated-layout-flow", "viewportAction"),
    Output("active-layout-store",  "data"),
    Output("active-layout-label",  "children"),
    [Input(f"btn-{key}", "n_clicks") for key in layouts],
    prevent_initial_call=True,
)
def apply_layout(*_clicks):
    from dash import ctx
    triggered = ctx.triggered_id
    if not triggered:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # e.g. "btn-layered-lr" → "layered-lr"
    key = triggered[len("btn-"):]
    if key not in layouts:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # Fit view after layout animation completes
    viewport_action = {"action": "fitView", "duration": 300, "delay": 550}

    return (
        layouts[key]["options"],
        viewport_action,
        key,
        f"Layout: {layouts[key]['label']}",
    )


# Highlight the active layout button
for key in layouts:
    @callback(
        Output(f"btn-{key}", "style"),
        Input("active-layout-store", "data"),
    )
    def update_btn_style(active, _key=key):
        return _btn_active if active == _key else _btn_idle


if __name__ == "__main__":
    app.run(debug=True, port=8031)