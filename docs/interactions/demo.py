"""Live, callback-free demo for the docs page. Rendered via `.. exec::docs.interactions.demo`."""
import dash_flows

nodes = [{'id': 'q', 'type': 'input', 'data': {'label': 'Request'}, 'position': {'x': 60, 'y': 40}},
 {'id': 'v', 'type': 'default', 'data': {'label': 'Validate'}, 'position': {'x': 60, 'y': 170}},
 {'id': 'p', 'type': 'default', 'data': {'label': 'Persist'}, 'position': {'x': 240, 'y': 170}},
 {'id': 'r', 'type': 'output', 'data': {'label': 'Respond'}, 'position': {'x': 150, 'y': 300}}]

edges = [{'id': 'qv', 'source': 'q', 'target': 'v'},
 {'id': 'vp', 'source': 'v', 'target': 'p'},
 {'id': 'pr', 'source': 'p', 'target': 'r'},
 {'id': 'vr', 'source': 'v', 'target': 'r'}]

component = dash_flows.DashFlows(
    id="interactions-demo",
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
