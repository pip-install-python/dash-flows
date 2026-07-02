"""
Embeddable twin of examples/04_background_variants.py for the docs page.
Rendered via `.. exec::docs.canvas.ex04`.
"""
from dash import html, Input, Output, callback
import dash_flows
import dash_mantine_components as dmc

nodes = [
    {"id": "1", "type": "default", "data": {"label": "Node A"}, "position": {"x": 100, "y": 100}},
    {"id": "2", "type": "default", "data": {"label": "Node B"}, "position": {"x": 300, "y": 100}},
    {"id": "3", "type": "default", "data": {"label": "Node C"}, "position": {"x": 200, "y": 250}},
]

edges = [
    {"id": "e1", "source": "1", "target": "3"},
    {"id": "e2", "source": "2", "target": "3"},
]

component = html.Div([
    dmc.Group([
        dmc.Select(
            id="ex04-bg-variant",
            label="Background Variant",
            data=[
                {"value": "dots", "label": "Dots"},
                {"value": "lines", "label": "Lines"},
                {"value": "cross", "label": "Cross"},
            ],
            value="dots",
            style={"width": 150},
        ),
        dmc.ColorInput(
            id="ex04-bg-color",
            label="Pattern Color",
            value="#e5e7eb",
            style={"width": 150},
        ),
        dmc.NumberInput(
            id="ex04-bg-gap",
            label="Gap Size",
            value=20,
            min=5,
            max=50,
            style={"width": 100},
        ),
        dmc.NumberInput(
            id="ex04-bg-size",
            label="Pattern Size",
            value=1,
            min=0.5,
            max=5,
            step=0.5,
            style={"width": 100},
        ),
    ], style={"marginBottom": 20}),

    html.Div(id="ex04-flow-container"),
])


@callback(
    Output("ex04-flow-container", "children"),
    Input("ex04-bg-variant", "value"),
    Input("ex04-bg-color", "value"),
    Input("ex04-bg-gap", "value"),
    Input("ex04-bg-size", "value"),
)
def update_background(variant, color, gap, size):
    return dash_flows.DashFlows(
        id="ex04-background-flow",
        nodes=nodes,
        edges=edges,
        style={
            "height": "460px",
            "border": "1px solid var(--mantine-color-default-border)",
            "borderRadius": "8px",
        },
        fitView=True,
        showControls=True,
        # Background configuration
        backgroundVariant=variant,
        backgroundGap=gap,
        backgroundSize=size,
        backgroundColor=color,
    )
