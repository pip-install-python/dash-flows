"""Live, callback-free demo for the docs page. Rendered via `.. exec::docs.nodes.demo`."""
import dash_flows

nodes = [{'id': 'in', 'type': 'input', 'data': {'label': 'input'}, 'position': {'x': 40, 'y': 20}},
 {'id': 'def', 'type': 'default', 'data': {'label': 'default'}, 'position': {'x': 40, 'y': 140}},
 {'id': 'out', 'type': 'output', 'data': {'label': 'output'}, 'position': {'x': 40, 'y': 260}},
 {'id': 'res',
  'type': 'resizable',
  'data': {'label': 'resizable'},
  'position': {'x': 260, 'y': 40},
  'style': {'width': 170, 'height': 90}},
 {'id': 'circ', 'type': 'circle', 'data': {'label': 'circle'}, 'position': {'x': 300, 'y': 200}},
 {'id': 'grp',
  'type': 'group',
  'data': {'label': 'group'},
  'position': {'x': 480, 'y': 20},
  'style': {'width': 220, 'height': 180}},
 {'id': 'c1',
  'type': 'default',
  'data': {'label': 'child 1'},
  'position': {'x': 20, 'y': 40},
  'parentId': 'grp',
  'extent': 'parent'},
 {'id': 'c2',
  'type': 'default',
  'data': {'label': 'child 2'},
  'position': {'x': 20, 'y': 110},
  'parentId': 'grp',
  'extent': 'parent'}]

edges = [{'id': 'n1', 'source': 'in', 'target': 'def'},
 {'id': 'n2', 'source': 'def', 'target': 'out'},
 {'id': 'n3', 'source': 'res', 'target': 'circ'}]

component = dash_flows.DashFlows(
    id="nodes-demo",
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
