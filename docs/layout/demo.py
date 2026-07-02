"""Live, callback-free demo for the docs page. Rendered via `.. exec::docs.layout.demo`."""
import dash_flows

nodes = [{'id': 'root', 'type': 'input', 'data': {'label': 'Root'}, 'position': {'x': 200, 'y': 20}},
 {'id': 'l1', 'type': 'default', 'data': {'label': 'Branch 1'}, 'position': {'x': 60, 'y': 160}},
 {'id': 'l2', 'type': 'default', 'data': {'label': 'Branch 2'}, 'position': {'x': 340, 'y': 160}},
 {'id': 'l3', 'type': 'output', 'data': {'label': 'Leaf A'}, 'position': {'x': 20, 'y': 300}},
 {'id': 'l4', 'type': 'output', 'data': {'label': 'Leaf B'}, 'position': {'x': 160, 'y': 300}},
 {'id': 'l5', 'type': 'output', 'data': {'label': 'Leaf C'}, 'position': {'x': 340, 'y': 300}}]

edges = [{'id': 'r1', 'source': 'root', 'target': 'l1'},
 {'id': 'r2', 'source': 'root', 'target': 'l2'},
 {'id': '13', 'source': 'l1', 'target': 'l3'},
 {'id': '14', 'source': 'l1', 'target': 'l4'},
 {'id': '25', 'source': 'l2', 'target': 'l5'}]

component = dash_flows.DashFlows(
    id="layout-demo",
    nodes=nodes,
    edges=edges,
    style={'border': '1px solid var(--mantine-color-default-border)',
 'borderRadius': '8px',
 'height': '440px'},
    showControls=True,
    showMiniMap=True,
    smartHandles=True,
    fitView=True,
    colorMode='system',
)
