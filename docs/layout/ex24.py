"""
Embeddable twin of examples/24_smart_handles.py for the docs page.
Rendered via `.. exec::docs.layout.ex24`.
"""
from dash import html, dcc, callback, Input, Output
import dash_flows

# --- Nodes arranged in various positions to show smart routing ---
smart_nodes = [
    {
        "id": "source-1",
        "type": "input",
        "data": {"label": "Data Source", "sublabel": "API"},
        "position": {"x": 50, "y": 50},
    },
    {
        "id": "process-1",
        "type": "default",
        "data": {"label": "Validate", "sublabel": "Schema Check"},
        "position": {"x": 400, "y": 30},
    },
    {
        "id": "process-2",
        "type": "default",
        "data": {"label": "Transform", "sublabel": "Map & Filter"},
        "position": {"x": 250, "y": 200},
    },
    {
        "id": "process-3",
        "type": "default",
        "data": {"label": "Aggregate", "sublabel": "Group By"},
        "position": {"x": 50, "y": 350},
    },
    {
        "id": "process-4",
        "type": "default",
        "data": {"label": "Enrich", "sublabel": "Join External"},
        "position": {"x": 500, "y": 220},
    },
    {
        "id": "output-1",
        "type": "output",
        "data": {"label": "Dashboard", "sublabel": "Visualization"},
        "position": {"x": 400, "y": 400},
    },
    {
        "id": "output-2",
        "type": "output",
        "data": {"label": "Database", "sublabel": "PostgreSQL"},
        "position": {"x": 200, "y": 430},
    },
]

smart_edges = [
    {"id": "e1", "source": "source-1", "target": "process-1", "type": "smoothstep"},
    {"id": "e2", "source": "source-1", "target": "process-2", "type": "smoothstep"},
    {"id": "e3", "source": "process-1", "target": "process-4", "type": "smoothstep"},
    {"id": "e4", "source": "process-2", "target": "process-3", "type": "smoothstep"},
    {"id": "e5", "source": "process-2", "target": "process-4", "type": "smoothstep"},
    {"id": "e6", "source": "process-2", "target": "output-1", "type": "smoothstep"},
    {"id": "e7", "source": "process-4", "target": "output-1", "type": "smoothstep"},
    {"id": "e8", "source": "process-3", "target": "output-2", "type": "smoothstep"},
]


component = html.Div([
    dcc.Checklist(
        id="ex24-smart-toggle",
        options=[{"label": " Enable smartHandles", "value": "on"}],
        value=["on"],
        style={"fontSize": "14px", "marginBottom": "8px"},
    ),
    html.Div(id="ex24-smart-status", style={"fontSize": "12px", "color": "var(--mantine-color-dimmed)", "marginBottom": "8px"}),
    dash_flows.DashFlows(
        id="ex24-smart-flow",
        nodes=smart_nodes,
        edges=smart_edges,
        smartHandles=True,
        style={
            "height": "500px",
            "border": "1px solid var(--mantine-color-default-border)",
            "borderRadius": "8px",
        },
        fitView=True,
        fitViewOptions={"padding": 0.15},
        showControls=True,
        showMiniMap=True,
        colorScheme="ocean",
    ),
])


@callback(
    Output("ex24-smart-flow", "smartHandles"),
    Output("ex24-smart-status", "children"),
    Input("ex24-smart-toggle", "value"),
)
def toggle_smart_handles(value):
    enabled = "on" in (value or [])
    status = (
        "smartHandles=True (edges route to closest side)"
        if enabled
        else "smartHandles=False (default top/bottom handles)"
    )
    return enabled, status
