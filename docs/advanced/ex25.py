"""
Embeddable twin of examples/25_phase1_features.py for the docs page.
Rendered via `.. exec::docs.advanced.ex25`.
"""
from dash import html
import dash_flows

nodes = [
    # Input nodes (green in minimap)
    {
        "id": "source-1",
        "type": "input",
        "data": {"label": "API Source", "sublabel": "REST Endpoint"},
        "position": {"x": 50, "y": 50},
    },
    {
        "id": "source-2",
        "type": "input",
        "data": {"label": "DB Source", "sublabel": "PostgreSQL"},
        "position": {"x": 50, "y": 200},
    },

    # Default nodes (blue in minimap)
    {
        "id": "validate",
        "type": "default",
        "data": {"label": "Validate", "sublabel": "Schema Check"},
        "position": {"x": 300, "y": 50},
    },
    {
        "id": "transform",
        "type": "default",
        "data": {"label": "Transform", "sublabel": "Map & Filter"},
        "position": {"x": 300, "y": 200},
    },
    {
        "id": "merge",
        "type": "default",
        "data": {"label": "Merge", "sublabel": "Join Data"},
        "position": {"x": 550, "y": 125},
    },

    # Output nodes (purple in minimap)
    {
        "id": "output-1",
        "type": "output",
        "data": {"label": "Dashboard", "sublabel": "Visualization"},
        "position": {"x": 800, "y": 50},
    },
    {
        "id": "output-2",
        "type": "output",
        "data": {"label": "Export", "sublabel": "CSV File"},
        "position": {"x": 800, "y": 200},
    },

    # Toolbar node (amber in minimap)
    {
        "id": "config",
        "type": "toolbar",
        "data": {"label": "Config", "sublabel": "Settings"},
        "position": {"x": 550, "y": 300},
    },
]

edges = [
    # Standard edges
    {"id": "e1", "source": "source-1", "target": "validate", "type": "smoothstep", "animated": True},
    {"id": "e2", "source": "source-2", "target": "transform", "type": "smoothstep", "animated": True},
    {"id": "e3", "source": "validate", "target": "merge", "type": "smoothstep"},
    {"id": "e4", "source": "transform", "target": "merge", "type": "smoothstep"},

    # ButtonEdge with toolbar — select this edge to see the EdgeToolbar
    {
        "id": "e5",
        "source": "merge",
        "target": "output-1",
        "type": "button",
        "data": {
            "label": "Primary",
            "showButton": False,   # Hide inline delete button
            "showToolbar": True,   # EdgeToolbar appears when selected instead
        },
    },
    {
        "id": "e6",
        "source": "merge",
        "target": "output-2",
        "type": "button",
        "data": {
            "label": "Secondary",
            "showButton": False,
            "showToolbar": True,
        },
    },

    # Edge to config
    {"id": "e7", "source": "merge", "target": "config", "type": "smoothstep", "style": {"strokeDasharray": "5 5"}},
]


component = html.Div([
    html.Div([
        html.Ul([
            html.Li([
                html.Strong("connectionDragThreshold=10"),
                " — Drag 10px from a handle before the connection line appears (prevents accidental connections)",
            ]),
            html.Li([
                html.Strong("zIndexMode='elevate'"),
                " — Selected nodes and their connected edges elevate above all other elements",
            ]),
            html.Li([
                html.Strong("autoPanOnNodeFocus=True"),
                " — Click inside the flow canvas first, then press Tab to cycle through nodes; viewport auto-pans to keep the focused node visible",
            ]),
            html.Li([
                html.Strong("Type-Colored MiniMap"),
                " — Check the minimap (bottom-right): green=input, blue=default, purple=output, amber=toolbar",
            ]),
            html.Li([
                html.Strong("EdgeToolbar"),
                " — Click the 'Primary' or 'Secondary' edge line (not a node) to select it — a glass toolbar with edit/delete buttons appears above the edge",
            ]),
        ]),
    ], style={"padding": "0 0 10px 0", "fontSize": "13px"}),

    dash_flows.DashFlows(
        id="ex25-feature-flow",
        nodes=nodes,
        edges=edges,
        # Phase 1 props
        connectionDragThreshold=10,
        zIndexMode="elevate",
        autoPanOnNodeFocus=True,
        # Standard display options
        style={
            "height": "480px",
            "border": "1px solid var(--mantine-color-default-border)",
            "borderRadius": "8px",
        },
        fitView=True,
        fitViewOptions={"padding": 0.15},
        showControls=True,
        showMiniMap=True,
        showBackground=True,
        colorScheme="default",
    ),
])
