"""Live, callback-free demo for the docs page. Rendered via `.. exec::docs.getting_started.demo`."""
import dash_flows

nodes = [{'id': '1', 'type': 'input', 'data': {'label': 'Start'}, 'position': {'x': 120, 'y': 40}},
 {'id': '2', 'type': 'default', 'data': {'label': 'Process A'}, 'position': {'x': 40, 'y': 180}},
 {'id': '3', 'type': 'default', 'data': {'label': 'Process B'}, 'position': {'x': 220, 'y': 180}},
 {'id': '4', 'type': 'output', 'data': {'label': 'End'}, 'position': {'x': 120, 'y': 320}}]

edges = [{'id': 'e1-2', 'source': '1', 'target': '2', 'animated': True},
 {'id': 'e1-3', 'source': '1', 'target': '3'},
 {'id': 'e2-4', 'source': '2', 'target': '4'},
 {'id': 'e3-4', 'source': '3', 'target': '4', 'animated': True}]

component = dash_flows.DashFlows(
    id="getting_started-demo",
    nodes=nodes,
    edges=edges,
    style={'border': '1px solid var(--mantine-color-default-border)',
 'borderRadius': '8px',
 'height': '440px'},
    showControls=True,
    showMiniMap=True,
    fitView=True,
    colorMode='system',
)
