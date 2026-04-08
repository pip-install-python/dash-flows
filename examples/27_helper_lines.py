"""
Example 27: Helper Lines (Alignment Guides)
=============================================
Demonstrates helper lines that appear as visual guides when dragging a node
near another node's edge. Helps users align nodes precisely.
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_flows

app = dash.Dash(__name__)

nodes = [
    {
        "id": "a",
        "type": "input",
        "data": {"label": "Start"},
        "position": {"x": 50, "y": 50},
    },
    {
        "id": "b",
        "type": "default",
        "data": {"label": "Process A"},
        "position": {"x": 300, "y": 50},
    },
    {
        "id": "c",
        "type": "default",
        "data": {"label": "Process B"},
        "position": {"x": 300, "y": 200},
    },
    {
        "id": "d",
        "type": "default",
        "data": {"label": "Process C"},
        "position": {"x": 550, "y": 125},
    },
    {
        "id": "e",
        "type": "output",
        "data": {"label": "End"},
        "position": {"x": 550, "y": 300},
    },
]

edges = [
    {"id": "e-ab", "source": "a", "target": "b", "type": "smoothstep"},
    {"id": "e-ac", "source": "a", "target": "c", "type": "smoothstep"},
    {"id": "e-bd", "source": "b", "target": "d", "type": "smoothstep"},
    {"id": "e-cd", "source": "c", "target": "d", "type": "smoothstep"},
    {"id": "e-de", "source": "d", "target": "e", "type": "smoothstep"},
]

app.layout = html.Div([
    html.H1("Helper Lines (Alignment Guides)"),
    html.P(
        "Drag any node and blue alignment guides will appear when it aligns "
        "with another node's edge. The node will snap to the alignment."
    ),
    html.Div([
        dcc.Checklist(
            id="helper-toggle",
            options=[{"label": " Enable helper lines", "value": "on"}],
            value=["on"],
            style={"fontSize": "14px", "marginBottom": "8px"},
        ),
        html.Label("Snap threshold (px): ", style={"fontSize": "14px"}),
        dcc.Slider(
            id="threshold-slider",
            min=1, max=20, step=1, value=5,
            marks={1: "1", 5: "5", 10: "10", 20: "20"},
        ),
    ], style={"marginBottom": "12px", "maxWidth": "400px"}),
    dash_flows.DashFlows(
        id="helper-flow",
        nodes=nodes,
        edges=edges,
        helperLines=True,
        helperLineThreshold=5,
        smartHandles=True,
        style={"height": "550px", "border": "1px solid #ddd"},
        fitView=True,
        fitViewOptions={"padding": 0.2},
        showControls=True,
        showBackground=True,
        backgroundVariant="dots",
    ),
])


@callback(
    Output("helper-flow", "helperLines"),
    Output("helper-flow", "helperLineThreshold"),
    Input("helper-toggle", "value"),
    Input("threshold-slider", "value"),
)
def update_helper_settings(toggle, threshold):
    enabled = "on" in (toggle or [])
    return enabled, threshold or 5


if __name__ == "__main__":
    app.run(debug=True, port=8027)
