"""
Example 04: Background Variants
===============================
This example demonstrates the different background patterns available:
- dots: Grid of dots (default)
- lines: Horizontal and vertical lines
- cross: Crosshatch pattern
- Custom colors and sizes
"""

import dash
from dash import html, Input, Output, callback
import dash_flows
import dash_mantine_components as dmc

app = dash.Dash(__name__)

nodes = [
    {"id": "1", "type": "default", "data": {"label": "Node A"}, "position": {"x": 100, "y": 100}},
    {"id": "2", "type": "default", "data": {"label": "Node B"}, "position": {"x": 300, "y": 100}},
    {"id": "3", "type": "default", "data": {"label": "Node C"}, "position": {"x": 200, "y": 250}},
]

edges = [
    {"id": "e1", "source": "1", "target": "3"},
    {"id": "e2", "source": "2", "target": "3"},
]

app.layout = dmc.MantineProvider([
    html.H1("Background Variants Example"),
    html.P("Use the controls below to change the background pattern."),

    dmc.Group([
        dmc.Select(
            id="bg-variant",
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
            id="bg-color",
            label="Pattern Color",
            value="#e5e7eb",
            style={"width": 150},
        ),
        dmc.NumberInput(
            id="bg-gap",
            label="Gap Size",
            value=20,
            min=5,
            max=50,
            style={"width": 100},
        ),
        dmc.NumberInput(
            id="bg-size",
            label="Pattern Size",
            value=1,
            min=0.5,
            max=5,
            step=0.5,
            style={"width": 100},
        ),
    ], style={"marginBottom": 20}),

    html.Div(id="flow-container"),
])

@callback(
    Output("flow-container", "children"),
    Input("bg-variant", "value"),
    Input("bg-color", "value"),
    Input("bg-gap", "value"),
    Input("bg-size", "value"),
)
def update_background(variant, color, gap, size):
    return dash_flows.DashFlows(
        id="background-flow",
        nodes=nodes,
        edges=edges,
        style={"height": "500px", "border": "1px solid #ddd"},
        fitView=True,
        showControls=True,
        # Background configuration
        backgroundVariant=variant,
        backgroundGap=gap,
        backgroundSize=size,
        backgroundColor=color,
    )

if __name__ == "__main__":
    app.run(debug=True, port=8053)