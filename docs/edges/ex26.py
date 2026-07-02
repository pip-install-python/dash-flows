"""
Embeddable twin of examples/26_floating_edges.py for the docs page.
Rendered via `.. exec::docs.edges.ex26`.
"""
from dash import html, callback, Input, Output
import dash_flows

nodes = [
    {
        "id": "1",
        "type": "input",
        "data": {"label": "Data Source", "sublabel": "REST API"},
        "position": {"x": 0, "y": 0},
    },
    {
        "id": "2",
        "type": "default",
        "data": {"label": "Validate"},
        "position": {"x": 300, "y": -50},
    },
    {
        "id": "3",
        "type": "default",
        "data": {"label": "Transform"},
        "position": {"x": 150, "y": 200},
    },
    {
        "id": "4",
        "type": "default",
        "data": {"label": "Enrich"},
        "position": {"x": 450, "y": 150},
    },
    {
        "id": "5",
        "type": "output",
        "data": {"label": "Database", "sublabel": "PostgreSQL"},
        "position": {"x": 350, "y": 350},
    },
    {
        "id": "6",
        "type": "output",
        "data": {"label": "Dashboard", "sublabel": "Visualization"},
        "position": {"x": 50, "y": 400},
    },
]

# All edges use the 'floating' type - they connect to the nearest border point
edges = [
    {"id": "e1-2", "source": "1", "target": "2", "type": "floating", "label": "raw"},
    {"id": "e1-3", "source": "1", "target": "3", "type": "floating"},
    {"id": "e2-4", "source": "2", "target": "4", "type": "floating", "label": "valid"},
    {"id": "e3-4", "source": "3", "target": "4", "type": "floating"},
    {"id": "e3-6", "source": "3", "target": "6", "type": "floating"},
    {"id": "e4-5", "source": "4", "target": "5", "type": "floating", "label": "enriched"},
]

component = html.Div([
    dash_flows.DashFlows(
        id="ex26-floating-flow",
        nodes=nodes,
        edges=edges,
        style={
            "height": "500px",
            "border": "1px solid var(--mantine-color-default-border)",
            "borderRadius": "8px",
        },
        fitView=True,
        fitViewOptions={"padding": 0.2},
        showControls=True,
        showMiniMap=True,
        showBackground=True,
        colorScheme="ocean",
    ),
    html.Div(id="ex26-floating-info", style={"marginTop": "12px", "fontSize": "14px", "color": "var(--mantine-color-dimmed)"}),
])


@callback(
    Output("ex26-floating-info", "children"),
    Input("ex26-floating-flow", "clickedNode"),
)
def show_clicked(node):
    if not node:
        return "Click a node to see its info. Drag nodes to see floating edges update."
    return f"Clicked: {node['id']} - {node['data'].get('label', '')}"
