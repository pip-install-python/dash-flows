"""
Example 05: Controls and MiniMap
================================
This example demonstrates:
- Zoom controls (zoom in, zoom out, fit view, lock interactivity)
- MiniMap with custom styling
- Control positioning options
"""

import dash
from dash import html, Input, Output, State
import dash_flows
import dash_mantine_components as dmc

app = dash.Dash(__name__)

# Create a larger flow to demonstrate MiniMap utility
nodes = []
edges = []

# Create a grid of nodes
for row in range(5):
    for col in range(6):
        node_id = f"node-{row}-{col}"
        nodes.append({
            "id": node_id,
            "type": "default",
            "data": {"label": f"({row},{col})"},
            "position": {"x": col * 200, "y": row * 150},
        })
        # Connect horizontally
        if col > 0:
            edges.append({
                "id": f"h-{row}-{col}",
                "source": f"node-{row}-{col-1}",
                "target": node_id,
            })
        # Connect vertically
        if row > 0:
            edges.append({
                "id": f"v-{row}-{col}",
                "source": f"node-{row-1}-{col}",
                "target": node_id,
            })

app.layout = dmc.MantineProvider([
    html.H1("Controls and MiniMap Example"),
    html.P("A large flow with zoom controls and minimap navigation."),

    dmc.Group([
        dmc.Switch(id="show-controls", label="Show Controls", checked=True),
        dmc.Switch(id="show-minimap", label="Show MiniMap", checked=True),
        dmc.Switch(id="pannable-minimap", label="Pannable MiniMap", checked=True),
        dmc.Switch(id="zoomable-minimap", label="Zoomable MiniMap", checked=True),
    ], style={"marginBottom": 20}),

    dmc.Group([
        dmc.Select(
            id="controls-position",
            label="Controls Position",
            data=[
                {"value": "top-left", "label": "Top Left"},
                {"value": "top-right", "label": "Top Right"},
                {"value": "bottom-left", "label": "Bottom Left"},
                {"value": "bottom-right", "label": "Bottom Right"},
            ],
            value="bottom-left",
            style={"width": 150},
        ),
        dmc.Select(
            id="minimap-position",
            label="MiniMap Position",
            data=[
                {"value": "top-left", "label": "Top Left"},
                {"value": "top-right", "label": "Top Right"},
                {"value": "bottom-left", "label": "Bottom Left"},
                {"value": "bottom-right", "label": "Bottom Right"},
            ],
            value="bottom-right",
            style={"width": 150},
        ),
    ], style={"marginBottom": 20}),

    html.Div(id="controls-flow-container"),
])

@app.callback(
    Output("controls-flow-container", "children"),
    Input("show-controls", "checked"),
    Input("show-minimap", "checked"),
    Input("pannable-minimap", "checked"),
    Input("zoomable-minimap", "checked"),
    Input("controls-position", "value"),
    Input("minimap-position", "value"),
)
def update_flow(show_controls, show_minimap, pannable, zoomable, ctrl_pos, mm_pos):
    return dash_flows.DashFlows(
        id="controls-flow",
        nodes=nodes,
        edges=edges,
        style={"height": "600px", "border": "1px solid #ddd"},
        fitView=True,
        # Controls configuration
        showControls=show_controls,
        controlsPosition=ctrl_pos,
        controlsShowZoom=True,
        controlsShowFitView=True,
        controlsShowInteractive=True,
        # MiniMap configuration
        showMiniMap=show_minimap,
        miniMapPosition=mm_pos,
        miniMapPannable=pannable,
        miniMapZoomable=zoomable,
    )

if __name__ == "__main__":
    app.run(debug=True, port=8054)