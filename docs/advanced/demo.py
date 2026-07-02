"""Live, callback-free demo for the docs page. Rendered via `.. exec::docs.advanced.demo`."""
import dash_flows

nodes = [{'id': 'src', 'type': 'input', 'data': {'label': 'Input'}, 'position': {'x': 60, 'y': 40}},
 {'id': 'm1', 'type': 'default', 'data': {'label': 'Step 1'}, 'position': {'x': 60, 'y': 170}},
 {'id': 'm2', 'type': 'default', 'data': {'label': 'Step 2'}, 'position': {'x': 260, 'y': 170}},
 {'id': 'agg', 'type': 'default', 'data': {'label': 'Aggregate'}, 'position': {'x': 160, 'y': 300}},
 {'id': 'snk', 'type': 'output', 'data': {'label': 'Output'}, 'position': {'x': 160, 'y': 430}}]

edges = [{'id': 'a1', 'source': 'src', 'target': 'm1'},
 {'id': 'a2', 'source': 'src', 'target': 'm2'},
 {'id': 'a3', 'source': 'm1', 'target': 'agg', 'animated': True},
 {'id': 'a4', 'source': 'm2', 'target': 'agg'},
 {'id': 'a5', 'source': 'agg', 'target': 'snk'}]

component = dash_flows.DashFlows(
    id="advanced-demo",
    nodes=nodes,
    edges=edges,
    style={'border': '1px solid var(--mantine-color-default-border)',
 'borderRadius': '8px',
 'height': '440px'},
    showControls=True,
    showMiniMap=True,
    enableUndoRedo=True,
    helperLines=True,
    fitView=True,
    colorMode='system',
)
