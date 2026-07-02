"""
Example 26: Floating Edges
===========================
Demonstrates the 'floating' edge type which connects to the nearest point
on each node's border instead of fixed handle positions. This creates more
natural-looking connections, especially when nodes are positioned at angles.
"""

import dash
from dash import html, callback, Input, Output
import dash_flows

app = dash.Dash(__name__)

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

app.layout = html.Div([
    html.H1("Floating Edges"),
    html.P(
        "Floating edges connect to the nearest point on each node's border. "
        "Drag nodes around and watch the edges dynamically reattach to the closest point."
    ),
    dash_flows.DashFlows(
        id="floating-flow",
        nodes=nodes,
        edges=edges,
        style={"height": "600px", "border": "1px solid #ddd"},
        fitView=True,
        fitViewOptions={"padding": 0.2},
        showControls=True,
        showMiniMap=True,
        showBackground=True,
        colorScheme="ocean",
    ),
    html.Div(id="floating-info", style={"marginTop": "12px", "fontSize": "14px", "color": "#666"}),
])


@callback(
    Output("floating-info", "children"),
    Input("floating-flow", "clickedNode"),
)
def show_clicked(node):
    if not node:
        return "Click a node to see its info. Drag nodes to see floating edges update."
    return f"Clicked: {node['id']} - {node['data'].get('label', '')}"


if __name__ == "__main__":
    app.run(debug=True, port=8026)
