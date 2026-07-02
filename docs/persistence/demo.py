"""Live, callback-free demo for the docs page. Rendered via `.. exec::docs.persistence.demo`."""
import dash_flows

nodes = [{'id': 'load', 'type': 'input', 'data': {'label': 'Load'}, 'position': {'x': 120, 'y': 40}},
 {'id': 'edit', 'type': 'default', 'data': {'label': 'Edit'}, 'position': {'x': 120, 'y': 180}},
 {'id': 'save', 'type': 'output', 'data': {'label': 'Save'}, 'position': {'x': 120, 'y': 320}}]

edges = [{'id': 'le', 'source': 'load', 'target': 'edit', 'animated': True},
 {'id': 'es', 'source': 'edit', 'target': 'save'}]

component = dash_flows.DashFlows(
    id="persistence-demo",
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
