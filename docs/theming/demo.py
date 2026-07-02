"""Live, callback-free demo for the docs page. Rendered via `.. exec::docs.theming.demo`."""
import dash_flows

nodes = [{'id': 't1', 'type': 'input', 'data': {'label': 'Ocean'}, 'position': {'x': 120, 'y': 40}},
 {'id': 't2', 'type': 'default', 'data': {'label': 'Scheme'}, 'position': {'x': 120, 'y': 180}},
 {'id': 't3', 'type': 'output', 'data': {'label': 'Preset'}, 'position': {'x': 120, 'y': 320}}]

edges = [{'id': 't12', 'source': 't1', 'target': 't2', 'animated': True},
 {'id': 't23', 'source': 't2', 'target': 't3'}]

component = dash_flows.DashFlows(
    id="theming-demo",
    nodes=nodes,
    edges=edges,
    style={'border': '1px solid var(--mantine-color-default-border)',
 'borderRadius': '8px',
 'height': '440px'},
    showControls=True,
    showMiniMap=True,
    colorScheme='ocean',
    themePreset='glass',
    fitView=True,
    colorMode='dark',
)
