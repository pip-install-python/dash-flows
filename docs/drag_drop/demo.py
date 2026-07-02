"""Live, callback-free demo for the docs page. Rendered via `.. exec::docs.drag_drop.demo`."""
import dash_flows

nodes = [{'id': 'palette', 'type': 'input', 'data': {'label': 'Drag me'}, 'position': {'x': 60, 'y': 60}},
 {'id': 'canvas',
  'type': 'default',
  'data': {'label': 'Drop target'},
  'position': {'x': 240, 'y': 200}}]

edges = [{'id': 'pc', 'source': 'palette', 'target': 'canvas'}]

component = dash_flows.DashFlows(
    id="drag_drop-demo",
    nodes=nodes,
    edges=edges,
    style={'border': '1px solid var(--mantine-color-default-border)',
 'borderRadius': '8px',
 'height': '440px'},
    showControls=True,
    fitView=True,
    colorMode='system',
)
