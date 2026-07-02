"""
Example 25: Phase 1 Feature Showcase
=====================================
Demonstrates new features from React Flow 12.10.1 upgrade:
- connectionDragThreshold: drag distance before connection starts
- zIndexMode: selected elements elevate above others
- autoPanOnNodeFocus: viewport pans when tabbing to nodes
- Glass connection line: styled preview during edge creation
- Type-colored MiniMap: node types shown as distinct colors
- EdgeToolbar on ButtonEdge: toolbar appears on selected edges
"""

import dash
from dash import html, dcc, callback, Input, Output, State
import dash_flows

app = dash.Dash(__name__)

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


app.layout = html.Div([
    html.H1("Phase 1 Feature Showcase"),

    html.Div([
        html.H3("New Features Demonstrated"),
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
                html.Strong("Glass Connection Line"),
                " — Drag from any handle to see the new blue dashed connection preview with glow effect",
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
    ], style={"padding": "0 16px", "fontSize": "14px"}),

    dash_flows.DashFlows(
        id="feature-flow",
        nodes=nodes,
        edges=edges,
        # New Phase 1 props
        connectionDragThreshold=10,
        zIndexMode="elevate",
        autoPanOnNodeFocus=True,
        # Standard display options
        style={"height": "600px", "border": "1px solid #ddd"},
        fitView=True,
        fitViewOptions={"padding": 0.15},
        showControls=True,
        showMiniMap=True,
        showBackground=True,
        colorScheme="default",
    ),
])


if __name__ == "__main__":
    app.run(debug=True, port=8025)
