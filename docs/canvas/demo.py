"""Live, callback-free demo for the docs page. Rendered via `.. exec::docs.canvas.demo`."""
import dash_flows

nodes = [{'id': 'a', 'type': 'input', 'data': {'label': 'Source'}, 'position': {'x': 120, 'y': 40}},
 {'id': 'b', 'type': 'default', 'data': {'label': 'Transform'}, 'position': {'x': 120, 'y': 180}},
 {'id': 'c', 'type': 'output', 'data': {'label': 'Sink'}, 'position': {'x': 120, 'y': 320}}]

edges = [{'id': 'ab', 'source': 'a', 'target': 'b', 'animated': True},
 {'id': 'bc', 'source': 'b', 'target': 'c'}]

component = dash_flows.DashFlows(
    id="canvas-demo",
    nodes=nodes,
    edges=edges,
    style={'border': '1px solid var(--mantine-color-default-border)',
 'borderRadius': '8px',
 'height': '440px'},
    showControls=True,
    showMiniMap=True,
    showBackground=True,
    backgroundVariant='cross',
    fitView=True,
    colorMode='system',
)
