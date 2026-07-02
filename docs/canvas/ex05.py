"""
Embeddable twin of examples/05_controls_and_minimap.py for the docs page.
Rendered via `.. exec::docs.canvas.ex05`.
"""
from dash import html, Input, Output, callback
import dash_flows
import dash_mantine_components as dmc

# Create a larger flow to demonstrate MiniMap utility
nodes = []
edges = []

for row in range(5):
    for col in range(6):
        node_id = f"ex05-node-{row}-{col}"
        nodes.append({
            "id": node_id,
            "type": "default",
            "data": {"label": f"({row},{col})"},
            "position": {"x": col * 200, "y": row * 150},
        })
        if col > 0:
            edges.append({
                "id": f"ex05-h-{row}-{col}",
                "source": f"ex05-node-{row}-{col-1}",
                "target": node_id,
            })
        if row > 0:
            edges.append({
                "id": f"ex05-v-{row}-{col}",
                "source": f"ex05-node-{row-1}-{col}",
                "target": node_id,
            })

component = html.Div([
    dmc.Group([
        dmc.Switch(id="ex05-show-controls", label="Show Controls", checked=True),
        dmc.Switch(id="ex05-show-minimap", label="Show MiniMap", checked=True),
        dmc.Switch(id="ex05-pannable-minimap", label="Pannable MiniMap", checked=True),
        dmc.Switch(id="ex05-zoomable-minimap", label="Zoomable MiniMap", checked=True),
    ], style={"marginBottom": 20}),

    dmc.Group([
        dmc.Select(
            id="ex05-controls-position",
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
            id="ex05-minimap-position",
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

    html.Div(id="ex05-controls-flow-container"),
])


@callback(
    Output("ex05-controls-flow-container", "children"),
    Input("ex05-show-controls", "checked"),
    Input("ex05-show-minimap", "checked"),
    Input("ex05-pannable-minimap", "checked"),
    Input("ex05-zoomable-minimap", "checked"),
    Input("ex05-controls-position", "value"),
    Input("ex05-minimap-position", "value"),
)
def update_flow(show_controls, show_minimap, pannable, zoomable, ctrl_pos, mm_pos):
    return dash_flows.DashFlows(
        id="ex05-controls-flow",
        nodes=nodes,
        edges=edges,
        style={
            "height": "500px",
            "border": "1px solid var(--mantine-color-default-border)",
            "borderRadius": "8px",
        },
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
