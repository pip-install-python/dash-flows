"""Live, callback-free demo for the docs page. Rendered via `.. exec::docs.edges.demo`."""
import dash_flows

nodes = [{'id': '0', 'type': 'default', 'data': {'label': 'straight'}, 'position': {'x': 60, 'y': 40}},
 {'id': '1', 'type': 'default', 'data': {'label': 'step'}, 'position': {'x': 320, 'y': 40}},
 {'id': '2', 'type': 'default', 'data': {'label': 'smoothstep'}, 'position': {'x': 60, 'y': 160}},
 {'id': '3',
  'type': 'default',
  'data': {'label': 'simplebezier'},
  'position': {'x': 320, 'y': 160}},
 {'id': '4', 'type': 'default', 'data': {'label': 'button'}, 'position': {'x': 60, 'y': 280}},
 {'id': '5', 'type': 'default', 'data': {'label': 'animated'}, 'position': {'x': 320, 'y': 280}}]

edges = [{'id': 's', 'source': '0', 'target': '1', 'type': 'straight'},
 {'id': 'st', 'source': '1', 'target': '2', 'type': 'step'},
 {'id': 'sm', 'source': '2', 'target': '3', 'type': 'smoothstep'},
 {'id': 'sb', 'source': '3', 'target': '4', 'type': 'simplebezier'},
 {'id': 'bt', 'source': '4', 'target': '5', 'type': 'button'},
 {'id': 'an', 'source': '5', 'target': '0', 'type': 'animated'}]

component = dash_flows.DashFlows(
    id="edges-demo",
    nodes=nodes,
    edges=edges,
    style={'border': '1px solid var(--mantine-color-default-border)',
 'borderRadius': '8px',
 'height': '440px'},
    showControls=True,
    fitView=True,
    colorMode='system',
)
