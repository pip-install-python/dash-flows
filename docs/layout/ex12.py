"""
Embeddable twin of examples/12_elk_layouts.py for the docs page.
Rendered via `.. exec::docs.layout.ex12`.
"""
import json

from dash import html, callback, Input, Output, State
import dash_flows
import dash_mantine_components as dmc

# A more complex graph to show layout differences
initial_nodes = [
    {"id": "1", "type": "input", "data": {"label": "Start"}, "position": {"x": 0, "y": 0}},
    {"id": "2", "type": "default", "data": {"label": "Step A"}, "position": {"x": 0, "y": 0}},
    {"id": "3", "type": "default", "data": {"label": "Step B"}, "position": {"x": 0, "y": 0}},
    {"id": "4", "type": "default", "data": {"label": "Step C"}, "position": {"x": 0, "y": 0}},
    {"id": "5", "type": "default", "data": {"label": "Step D"}, "position": {"x": 0, "y": 0}},
    {"id": "6", "type": "default", "data": {"label": "Step E"}, "position": {"x": 0, "y": 0}},
    {"id": "7", "type": "default", "data": {"label": "Step F"}, "position": {"x": 0, "y": 0}},
    {"id": "8", "type": "output", "data": {"label": "End"}, "position": {"x": 0, "y": 0}},
]

initial_edges = [
    {"id": "e1-2", "source": "1", "target": "2"},
    {"id": "e1-3", "source": "1", "target": "3"},
    {"id": "e2-4", "source": "2", "target": "4"},
    {"id": "e2-5", "source": "2", "target": "5"},
    {"id": "e3-5", "source": "3", "target": "5"},
    {"id": "e3-6", "source": "3", "target": "6"},
    {"id": "e4-7", "source": "4", "target": "7"},
    {"id": "e5-7", "source": "5", "target": "7"},
    {"id": "e6-7", "source": "6", "target": "7"},
    {"id": "e7-8", "source": "7", "target": "8"},
]

layout_presets = {
    "layered-down": {
        "elk.algorithm": "layered",
        "elk.direction": "DOWN",
        "elk.spacing.nodeNode": 50,
        "elk.layered.spacing.nodeNodeBetweenLayers": 80,
    },
    "layered-right": {
        "elk.algorithm": "layered",
        "elk.direction": "RIGHT",
        "elk.spacing.nodeNode": 50,
        "elk.layered.spacing.nodeNodeBetweenLayers": 120,
    },
    "layered-up": {
        "elk.algorithm": "layered",
        "elk.direction": "UP",
        "elk.spacing.nodeNode": 50,
    },
    "layered-left": {
        "elk.algorithm": "layered",
        "elk.direction": "LEFT",
        "elk.spacing.nodeNode": 50,
    },
    "force": {
        "elk.algorithm": "org.eclipse.elk.force",
        "elk.force.iterations": 300,
        "elk.spacing.nodeNode": 80,
    },
    "radial": {
        "elk.algorithm": "org.eclipse.elk.radial",
        "elk.radial.radius": 150,
    },
    "stress": {
        "elk.algorithm": "org.eclipse.elk.stress",
        "elk.spacing.nodeNode": 100,
    },
}

component = html.Div([
    dmc.Group([
        dmc.Select(
            id="ex12-layout-select",
            label="Select Layout Algorithm",
            data=[
                {"value": "layered-down", "label": "Layered (Top to Bottom)"},
                {"value": "layered-right", "label": "Layered (Left to Right)"},
                {"value": "layered-up", "label": "Layered (Bottom to Top)"},
                {"value": "layered-left", "label": "Layered (Right to Left)"},
                {"value": "force", "label": "Force-Directed"},
                {"value": "radial", "label": "Radial"},
                {"value": "stress", "label": "Stress"},
            ],
            value="layered-down",
            style={"width": 250},
        ),
        dmc.Button("Apply Layout", id="ex12-apply-layout-btn", variant="filled"),
        dmc.Button("Reset Positions", id="ex12-reset-btn", variant="outline"),
    ], style={"marginBottom": 16}),

    dash_flows.DashFlows(
        id="ex12-elk-flow",
        nodes=initial_nodes,
        edges=initial_edges,
        style={
            "height": "500px",
            "border": "1px solid var(--mantine-color-default-border)",
            "borderRadius": "8px",
        },
        fitView=True,
        showControls=True,
        showMiniMap=True,
        layoutOptions=json.dumps(layout_presets["layered-down"]),
    ),

    dmc.Space(h=16),

    dmc.Paper([
        dmc.Text("Current Layout Options:", fw=600, size="sm"),
        html.Pre(id="ex12-layout-options-display", style={"fontSize": "11px"}),
    ], p="md", withBorder=True),
])


@callback(
    Output("ex12-elk-flow", "layoutOptions"),
    Output("ex12-layout-options-display", "children"),
    Input("ex12-apply-layout-btn", "n_clicks"),
    State("ex12-layout-select", "value"),
    prevent_initial_call=True,
)
def apply_layout(n_clicks, layout_type):
    options = layout_presets.get(layout_type, layout_presets["layered-down"])
    return json.dumps(options), json.dumps(options, indent=2)


@callback(
    Output("ex12-elk-flow", "nodes"),
    Input("ex12-reset-btn", "n_clicks"),
    prevent_initial_call=True,
)
def reset_positions(n_clicks):
    # Reset to initial scattered positions (all at 0,0) so the next layout
    # run visibly animates from scratch.
    return initial_nodes
