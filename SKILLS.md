# Dash Flows - Complete Developer Guide

A comprehensive guide to building interactive node-based flow diagrams with **dash-flows**, a React Flow 12+ integration for Plotly Dash.

## Table of Contents

1. [Installation & Setup](#installation--setup)
2. [Quick Start](#quick-start)
3. [Core Concepts](#core-concepts)
4. [Node Types](#node-types)
5. [Edge Types](#edge-types)
6. [Handle Configuration](#handle-configuration)
7. [Styling & Theming](#styling--theming)
8. [Callbacks & Interactivity](#callbacks--interactivity)
9. [Advanced Features](#advanced-features)
10. [Complete Examples](#complete-examples)
11. [API Reference](#api-reference)

---

## Installation & Setup

### Install from PyPI

```bash
pip install dash-flows
```

### Requirements

- Python 3.8+
- Dash >= 3.0.0

### Verify Installation

```python
import dash_flows
print(dash_flows.__version__)
```

---

## Quick Start

Create your first flow diagram in under 20 lines:

```python
import dash
from dash import html
import dash_flows

app = dash.Dash(__name__)

# Define nodes
nodes = [
    {"id": "1", "type": "input", "data": {"label": "Start"}, "position": {"x": 0, "y": 0}},
    {"id": "2", "type": "default", "data": {"label": "Process"}, "position": {"x": 200, "y": 0}},
    {"id": "3", "type": "output", "data": {"label": "End"}, "position": {"x": 400, "y": 0}},
]

# Define edges (connections)
edges = [
    {"id": "e1-2", "source": "1", "target": "2"},
    {"id": "e2-3", "source": "2", "target": "3"},
]

app.layout = html.Div([
    dash_flows.DashFlows(
        id="my-flow",
        nodes=nodes,
        edges=edges,
        style={"height": "400px"},
        fitView=True,
    )
])

if __name__ == "__main__":
    app.run(debug=True)
```

---

## Core Concepts

### Node Structure

Every node requires these properties:

```python
{
    "id": "unique-id",           # Required: unique identifier
    "type": "default",           # Optional: node type (default, input, output, group, toolbar, resizable, circle)
    "data": {                    # Required: node data object
        "label": "Node Label",   # Primary text/content
        "sublabel": "Subtitle",  # Optional secondary text
    },
    "position": {"x": 0, "y": 0}, # Required: position in pixels
}
```

### Edge Structure

Every edge requires these properties:

```python
{
    "id": "unique-id",           # Required: unique identifier
    "source": "source-node-id",  # Required: source node ID
    "target": "target-node-id",  # Required: target node ID
}
```

### Position System

- Positions are in **pixels** relative to the flow canvas origin (top-left)
- Child nodes in groups use positions **relative to their parent**
- Use `fitView=True` to automatically adjust viewport to show all nodes

---

## Node Types

### Input Node

Source nodes with only outgoing connections. Features a green accent bar.

```python
{
    "id": "data-source",
    "type": "input",
    "data": {
        "label": "Data Source",
        "sublabel": "API",  # Optional
    },
    "position": {"x": 50, "y": 50},
}
```

### Output Node

Sink nodes with only incoming connections. Features a purple accent bar.

```python
{
    "id": "result",
    "type": "output",
    "data": {
        "label": "Results",
        "sublabel": "Database",
    },
    "position": {"x": 400, "y": 50},
}
```

### Default Node

Standard nodes with both incoming and outgoing handles.

```python
{
    "id": "process",
    "type": "default",
    "data": {
        "label": "Process Data",
        "sublabel": "Transform & Validate",
        "status": "loading",  # Optional: initial, loading, success, error
    },
    "position": {"x": 200, "y": 50},
}
```

**Status Options:**
- `"initial"` - Default state, no indicator
- `"loading"` - Blue pulsing glow animation
- `"success"` - Green border with checkmark
- `"error"` - Red border with X badge and shake animation

### Group Node

Container that holds child nodes. Child positions are relative to the group.

```python
# Parent group
{
    "id": "group-1",
    "type": "group",
    "data": {"label": "Processing Pipeline"},
    "position": {"x": 100, "y": 100},
    "style": {"width": 300, "height": 250},  # Required dimensions
}

# Child nodes (parentId links to group)
{
    "id": "child-1",
    "type": "default",
    "data": {"label": "Step 1"},
    "position": {"x": 30, "y": 50},    # Relative to parent!
    "parentId": "group-1",
    "extent": "parent",                 # Optional: constrain to parent bounds
}
```

### Toolbar Node

Node with a floating toolbar that appears on selection.

```python
{
    "id": "configurable",
    "type": "toolbar",
    "data": {
        "label": "Configurable Node",
        "sublabel": "Click for actions",
        "toolbarPosition": "top",  # or "bottom"
    },
    "position": {"x": 200, "y": 100},
}
```

### Resizable Node

Node that can be resized by dragging edges/corners. Supports custom HTML content.

```python
from dash import html

{
    "id": "resizable-1",
    "type": "resizable",
    "data": {
        "label": html.Div([
            html.H4("Custom Content"),
            html.P("Any HTML works here"),
        ], style={"padding": "10px"}),
        "handles": [  # Custom handle configuration
            {"type": "target", "position": "top", "id": "in"},
            {"type": "source", "position": "bottom", "id": "out"},
        ],
        "minWidth": 100,
        "minHeight": 80,
    },
    "position": {"x": 200, "y": 200},
    "style": {"width": 180, "height": 150},
}
```

### Circle Node (AnimatedCircleNode)

Small circular node (60px) for visual indicators.

```python
{
    "id": "indicator",
    "type": "circle",
    "data": {"label": "A"},
    "position": {"x": 300, "y": 100},
}
```

---

## Edge Types

### Default (Bezier)

Smooth curved connection using Bezier curves.

```python
{"id": "e1", "source": "a", "target": "b"}  # type defaults to bezier
```

### Straight

Direct line connection.

```python
{"id": "e1", "source": "a", "target": "b", "type": "straight"}
```

### Step

Right-angled connections with sharp corners.

```python
{"id": "e1", "source": "a", "target": "b", "type": "step"}
```

### SmoothStep

Right-angled connections with rounded corners.

```python
{
    "id": "e1",
    "source": "a",
    "target": "b",
    "type": "smoothstep",
    "data": {"borderRadius": 15},  # Optional: corner radius
}
```

### SimpleBezier

Simple curved connection (alternative to default).

```python
{"id": "e1", "source": "a", "target": "b", "type": "simplebezier"}
```

### Button Edge

Edge with an interactive delete button.

```python
{
    "id": "e1",
    "source": "a",
    "target": "b",
    "type": "button",
    "data": {
        "label": "Connection",
        "showButton": True,
        "buttonLabel": "x",
    },
}
```

### Animated SVG Edge

Edge with animated flowing effect.

```python
{"id": "e1", "source": "a", "target": "b", "type": "animatedSvg", "animated": True}
```

### Data Edge

Edge that displays data labels along the path.

```python
{"id": "e1", "source": "a", "target": "b", "type": "data", "label": "100 KB/s"}
```

### Edge Styling

All edges support these style properties:

```python
{
    "id": "e1",
    "source": "a",
    "target": "b",
    "animated": True,                    # Add animation
    "label": "Edge Label",               # Text label
    "style": {
        "stroke": "#ff0000",             # Line color
        "strokeWidth": 2,                # Line thickness
    },
    "markerEnd": {                       # Arrow at end
        "type": "ArrowClosed",
        "color": "#555",
        "width": 20,
        "height": 20,
    },
}
```

---

## Handle Configuration

Handles are connection points on nodes. Configure custom handles for complex flows.

### Default Handle Behavior

| Node Type | Target (Input) | Source (Output) |
|-----------|----------------|-----------------|
| input     | None           | Bottom          |
| output    | Top            | None            |
| default   | Top            | Bottom          |

### Custom Handles

Use the `handles` array in node data to define custom connection points:

```python
{
    "id": "multi-handle",
    "type": "resizable",
    "data": {
        "label": "Multi-Handle Node",
        "handles": [
            # Target handles (inputs)
            {"type": "target", "position": "top", "id": "in-1", "style": {"background": "#10b981"}},
            {"type": "target", "position": "left", "id": "in-2", "style": {"background": "#3b82f6"}},

            # Source handles (outputs)
            {"type": "source", "position": "bottom", "id": "out-1", "style": {"background": "#8b5cf6"}},
            {"type": "source", "position": "right", "id": "out-2", "style": {"background": "#f59e0b"}},
        ],
    },
    "position": {"x": 200, "y": 100},
    "style": {"width": 180, "height": 100},
}
```

### Multiple Handles on Same Side

Position multiple handles using CSS percentages:

```python
"handles": [
    {"type": "target", "position": "top", "id": "t1", "style": {"left": "25%"}},
    {"type": "target", "position": "top", "id": "t2", "style": {"left": "75%"}},
    {"type": "source", "position": "bottom", "id": "s1", "style": {"left": "25%"}},
    {"type": "source", "position": "bottom", "id": "s2", "style": {"left": "75%"}},
]
```

### Connecting to Specific Handles

When nodes have multiple handles, specify which handle to connect:

```python
{
    "id": "e1",
    "source": "node-a",
    "target": "node-b",
    "sourceHandle": "out-1",   # Specific source handle ID
    "targetHandle": "in-2",    # Specific target handle ID
}
```

---

## Styling & Theming

### Theme Presets

```python
dash_flows.DashFlows(
    ...,
    themePreset="glass",  # Options: "glass" (default), "solid", "minimal"
)
```

| Preset | Description |
|--------|-------------|
| `glass` | Glass morphism with blur and transparency |
| `solid` | Opaque nodes with shadows |
| `minimal` | Clean lines, border-focused design |

### Color Schemes

```python
dash_flows.DashFlows(
    ...,
    colorScheme="ocean",  # Options: "default", "ocean", "forest", "sunset", "midnight", "rose"
)
```

### Dark Mode

```python
dash_flows.DashFlows(
    ...,
    colorMode="dark",  # Options: "light" (default), "dark", "system"
)
```

With Mantine integration:

```python
import dash_mantine_components as dmc

app.layout = dmc.MantineProvider(
    forceColorScheme="dark",
    children=[
        dash_flows.DashFlows(
            ...,
            colorMode="dark",
        )
    ]
)
```

### Custom Theme

Override specific theme properties:

```python
dash_flows.DashFlows(
    ...,
    theme={
        "glassBlur": 15,                              # Blur intensity (px)
        "glassSaturate": 200,                         # Saturation (%)
        "nodeBackground": "rgba(255, 255, 255, 0.8)", # Node fill
        "nodeBorder": "#e5e7eb",                      # Node border
        "nodeText": "#1f2937",                        # Text color
        "inputNodeAccent": "#10b981",                 # Input node accent (green)
        "outputNodeAccent": "#8b5cf6",                # Output node accent (purple)
        "edgeStroke": "#64748b",                      # Edge color
        "edgeStrokeSelected": "#3b82f6",              # Selected edge color
        "handleBackground": "#ffffff",                # Handle color
        "borderRadius": 12,                           # Node corner radius (px)
    },
)
```

### Background Variants

```python
dash_flows.DashFlows(
    ...,
    showBackground=True,
    backgroundVariant="dots",  # Options: "dots" (default), "lines", "cross"
    backgroundGap=16,          # Gap between pattern elements
    backgroundSize=1,          # Size of pattern elements
)
```

---

## Callbacks & Interactivity

### Track Node/Edge Changes

```python
from dash import Input, Output, callback

@callback(
    Output("display", "children"),
    Input("flow", "nodes"),
    Input("flow", "edges"),
)
def on_flow_change(nodes, edges):
    return f"Nodes: {len(nodes)}, Edges: {len(edges)}"
```

### Handle Node Clicks

```python
@callback(
    Output("node-info", "children"),
    Input("flow", "clickedNode"),
    prevent_initial_call=True,
)
def on_node_click(clicked_node):
    if not clicked_node:
        return "No node selected"
    return f"Clicked: {clicked_node['id']}, Data: {clicked_node['data']}"
```

### Handle Double Clicks

```python
@callback(
    Output("modal", "opened"),
    Input("flow", "doubleClickedNode"),
    prevent_initial_call=True,
)
def on_double_click(node):
    return bool(node)
```

### Track Hover

```python
@callback(
    Output("hover-info", "children"),
    Input("flow", "hoveredNode"),
)
def on_hover(node):
    if node:
        return f"Hovering: {node['id']}"
    return "Hover over a node"
```

### Handle New Connections

```python
@callback(
    Output("connection-info", "children"),
    Input("flow", "lastConnection"),
    prevent_initial_call=True,
)
def on_connection(connection):
    if connection:
        return f"Connected: {connection['source']} → {connection['target']}"
    return ""
```

### Track Selection

```python
@callback(
    Output("selection-info", "children"),
    Input("flow", "selectedNodes"),
    Input("flow", "selectedEdges"),
)
def on_selection(nodes, edges):
    node_count = len(nodes) if nodes else 0
    edge_count = len(edges) if edges else 0
    return f"Selected: {node_count} nodes, {edge_count} edges"
```

### Handle Deletions

```python
@callback(
    Output("deleted-info", "children"),
    Input("flow", "deletedNodes"),
    Input("flow", "deletedEdges"),
    prevent_initial_call=True,
)
def on_delete(deleted_nodes, deleted_edges):
    return f"Deleted {len(deleted_nodes or [])} nodes, {len(deleted_edges or [])} edges"
```

### Update Node Status

```python
@callback(
    Output("flow", "nodes"),
    Input("process-btn", "n_clicks"),
    State("flow", "nodes"),
    prevent_initial_call=True,
)
def update_status(n_clicks, nodes):
    # Update a specific node's status
    return [
        {**node, "data": {**node["data"], "status": "loading"}}
        if node["id"] == "process-node" else node
        for node in nodes
    ]
```

### Add Nodes Dynamically

```python
@callback(
    Output("flow", "nodes"),
    Input("add-btn", "n_clicks"),
    State("flow", "nodes"),
    prevent_initial_call=True,
)
def add_node(n_clicks, nodes):
    new_node = {
        "id": f"node-{len(nodes)}",
        "type": "default",
        "data": {"label": f"Node {len(nodes)}"},
        "position": {"x": len(nodes) * 50, "y": len(nodes) * 50},
    }
    return nodes + [new_node]
```

---

## Advanced Features

### Automatic Layout (ELK)

Use ELK algorithms for automatic node arrangement:

```python
import json

# Horizontal layered layout
layout_horizontal = json.dumps({
    "elk.algorithm": "layered",
    "elk.direction": "RIGHT",
    "elk.spacing.nodeNode": 60,
    "elk.layered.spacing.nodeNodeBetweenLayers": 100,
})

# Vertical layered layout
layout_vertical = json.dumps({
    "elk.algorithm": "layered",
    "elk.direction": "DOWN",
    "elk.spacing.nodeNode": 60,
})

# Radial layout
layout_radial = json.dumps({
    "elk.algorithm": "org.eclipse.elk.radial",
    "elk.radial.radius": 180,
})

dash_flows.DashFlows(
    ...,
    layoutOptions=layout_horizontal,
)
```

### Trigger Layout via Callback

```python
@callback(
    Output("flow", "layoutOptions"),
    Input("layout-btn", "n_clicks"),
    prevent_initial_call=True,
)
def apply_layout(n_clicks):
    return json.dumps({
        "elk.algorithm": "layered",
        "elk.direction": "DOWN",
    })
```

### Connection Validation

Restrict which connections are allowed:

```python
dash_flows.DashFlows(
    ...,
    connectionRules={
        "allowSelfConnection": False,         # Prevent self-loops
        "allowDuplicateConnections": False,   # Prevent duplicate edges
        "validSourceTypes": ["input", "default"],
        "validTargetTypes": ["output", "default"],
    },
)
```

### Connection Limits per Node

```python
{
    "id": "limited-node",
    "type": "default",
    "data": {
        "label": "Limited Connections",
        "maxConnections": 3,          # Total max
        "maxSourceConnections": 2,    # Max outgoing
        "maxTargetConnections": 1,    # Max incoming
    },
    "position": {"x": 100, "y": 100},
}
```

### Export as Image

```python
@callback(
    Output("flow", "downloadImage"),
    Input("export-btn", "n_clicks"),
    prevent_initial_call=True,
)
def export_image(n_clicks):
    return {
        "format": "png",           # png, svg, jpeg
        "filename": "my-flow",
        "quality": 0.95,           # For jpeg
        "backgroundColor": "#ffffff",
        "pixelRatio": 2,           # Higher = more resolution
    }
```

### Save & Restore Flow State

```python
from dash import dcc

# Save state
@callback(
    Output("state-store", "data"),
    Input("save-btn", "n_clicks"),
    State("flow", "nodes"),
    State("flow", "edges"),
    prevent_initial_call=True,
)
def save_state(n_clicks, nodes, edges):
    return {"nodes": nodes, "edges": edges}

# Restore state
@callback(
    Output("flow", "nodes"),
    Output("flow", "edges"),
    Input("load-btn", "n_clicks"),
    State("state-store", "data"),
    prevent_initial_call=True,
)
def load_state(n_clicks, saved):
    if saved:
        return saved["nodes"], saved["edges"]
    return dash.no_update, dash.no_update
```

### Copy & Paste

```python
# Copy selected elements
@callback(
    Output("flow", "copyAction"),
    Input("copy-btn", "n_clicks"),
    prevent_initial_call=True,
)
def copy_selection(n_clicks):
    return True

# Paste with offset
@callback(
    Output("flow", "pasteAction"),
    Input("paste-btn", "n_clicks"),
    prevent_initial_call=True,
)
def paste_selection(n_clicks):
    return {"offset": {"x": 50, "y": 50}}
```

### Drag and Drop External Elements

```python
@callback(
    Output("flow", "nodes"),
    Input("flow", "droppedNode"),
    State("flow", "nodes"),
    prevent_initial_call=True,
)
def handle_drop(dropped, nodes):
    if not dropped:
        return nodes

    new_node = {
        "id": f"dropped-{len(nodes)}",
        "type": dropped.get("type", "default"),
        "data": dropped.get("data", {"label": "Dropped"}),
        "position": dropped["position"],
    }
    return nodes + [new_node]
```

### Viewport Control

```python
dash_flows.DashFlows(
    ...,
    fitView=True,
    fitViewOptions={"padding": 0.2, "duration": 500},
    minZoom=0.1,
    maxZoom=4,
    defaultViewport={"x": 0, "y": 0, "zoom": 1},
)
```

### Snap to Grid

```python
dash_flows.DashFlows(
    ...,
    snapToGrid=True,
    snapGrid=[20, 20],  # 20px grid
)
```

### Prevent Deletion

```python
dash_flows.DashFlows(
    ...,
    preventDelete=True,
    preventDeleteNodes=["critical-node-1", "critical-node-2"],
    preventDeleteEdges=["main-edge"],
)
```

### DevTools Panel

Enable debug panel showing viewport and node information:

```python
dash_flows.DashFlows(
    ...,
    showDevTools=True,
)
```

---

## Complete Examples

### Data Pipeline Flow

```python
import dash
from dash import html, Input, Output, State, callback
import dash_flows

app = dash.Dash(__name__)

nodes = [
    # Sources
    {"id": "api", "type": "input", "data": {"label": "REST API", "sublabel": "External"}, "position": {"x": 0, "y": 0}},
    {"id": "db", "type": "input", "data": {"label": "Database", "sublabel": "PostgreSQL"}, "position": {"x": 0, "y": 120}},

    # Processing
    {"id": "validate", "type": "default", "data": {"label": "Validate", "status": "initial"}, "position": {"x": 200, "y": 0}},
    {"id": "transform", "type": "default", "data": {"label": "Transform", "status": "initial"}, "position": {"x": 200, "y": 120}},
    {"id": "merge", "type": "default", "data": {"label": "Merge", "status": "initial"}, "position": {"x": 400, "y": 60}},

    # Output
    {"id": "output", "type": "output", "data": {"label": "Dashboard"}, "position": {"x": 600, "y": 60}},
]

edges = [
    {"id": "e1", "source": "api", "target": "validate"},
    {"id": "e2", "source": "db", "target": "transform"},
    {"id": "e3", "source": "validate", "target": "merge"},
    {"id": "e4", "source": "transform", "target": "merge"},
    {"id": "e5", "source": "merge", "target": "output", "animated": True},
]

app.layout = html.Div([
    html.Button("Run Pipeline", id="run-btn"),
    dash_flows.DashFlows(
        id="pipeline",
        nodes=nodes,
        edges=edges,
        style={"height": "400px"},
        fitView=True,
    ),
])

@callback(
    Output("pipeline", "nodes"),
    Input("run-btn", "n_clicks"),
    State("pipeline", "nodes"),
    prevent_initial_call=True,
)
def run_pipeline(n_clicks, nodes):
    # Simulate processing by updating statuses
    status_sequence = ["loading", "success"]
    return [
        {**node, "data": {**node["data"], "status": "loading"}}
        if node["type"] == "default" else node
        for node in nodes
    ]

if __name__ == "__main__":
    app.run(debug=True)
```

### Interactive Dashboard with Detail Panel

```python
import dash
from dash import html, dcc, Input, Output, callback
import dash_flows
import dash_mantine_components as dmc
import plotly.express as px

app = dash.Dash(__name__)

nodes = [
    {
        "id": "revenue",
        "type": "resizable",
        "data": {
            "label": html.Div([
                html.Div("Revenue", style={"fontSize": "12px", "color": "#6b7280"}),
                html.Div("$19,500", style={"fontSize": "24px", "fontWeight": "bold"}),
                html.Div("+8.2%", style={"color": "#10b981", "fontSize": "12px"}),
            ], style={"padding": "10px"}),
            "handles": [
                {"type": "target", "position": "left", "id": "in"},
                {"type": "source", "position": "right", "id": "out"},
            ],
        },
        "position": {"x": 100, "y": 100},
        "style": {"width": 150, "height": 100},
    },
    # Add more metric nodes...
]

edges = []

app.layout = dmc.MantineProvider([
    dmc.Grid([
        dmc.GridCol([
            dash_flows.DashFlows(
                id="metrics-flow",
                nodes=nodes,
                edges=edges,
                style={"height": "500px"},
                fitView=True,
            ),
        ], span=8),
        dmc.GridCol([
            dmc.Paper([
                html.Div(id="detail-panel"),
            ], p="md", withBorder=True),
        ], span=4),
    ]),
])

@callback(
    Output("detail-panel", "children"),
    Input("metrics-flow", "clickedNode"),
)
def show_details(node):
    if not node:
        return dmc.Text("Click a node for details")

    # Show detailed chart for the clicked node
    if node["id"] == "revenue":
        fig = px.line(x=["Jan", "Feb", "Mar"], y=[12000, 15000, 19500])
        return dcc.Graph(figure=fig)

    return dmc.Text(f"Selected: {node['id']}")

if __name__ == "__main__":
    app.run(debug=True)
```

---

## API Reference

### DashFlows Component Props

#### Core Data Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `id` | string | - | Component identifier |
| `nodes` | list | `[]` | Array of node objects |
| `edges` | list | `[]` | Array of edge objects |

#### Viewport Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `fitView` | bool | `False` | Auto-fit nodes on init |
| `fitViewOptions` | dict | - | Options: `padding`, `duration` |
| `minZoom` | number | `0.5` | Minimum zoom level |
| `maxZoom` | number | `2` | Maximum zoom level |
| `defaultViewport` | dict | - | Initial `{x, y, zoom}` |
| `snapToGrid` | bool | `False` | Enable grid snapping |
| `snapGrid` | list | `[15, 15]` | Grid size `[x, y]` |

#### Interaction Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `nodesDraggable` | bool | `True` | Enable node dragging |
| `nodesConnectable` | bool | `True` | Enable creating connections |
| `elementsSelectable` | bool | `True` | Enable selection |
| `panOnDrag` | bool/list | `True` | Pan by dragging |
| `zoomOnScroll` | bool | `True` | Zoom by scrolling |
| `zoomOnPinch` | bool | `True` | Zoom by pinching |
| `zoomOnDoubleClick` | bool | `True` | Zoom on double-click |
| `selectNodesOnDrag` | bool | `True` | Box selection |
| `connectionMode` | string | `"strict"` | `"strict"` or `"loose"` |

#### Display Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `showMiniMap` | bool | `True` | Show minimap |
| `showControls` | bool | `True` | Show zoom controls |
| `showBackground` | bool | `True` | Show background pattern |
| `showDevTools` | bool | `False` | Show debug panel |
| `backgroundVariant` | string | `"dots"` | `"dots"`, `"lines"`, `"cross"` |
| `backgroundGap` | number | `16` | Pattern gap |
| `miniMapPosition` | string | `"bottom-right"` | Minimap position |
| `controlsPosition` | string | `"bottom-left"` | Controls position |

#### Theme Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `colorMode` | string | `"light"` | `"light"`, `"dark"`, `"system"` |
| `themePreset` | string | `"glass"` | `"glass"`, `"solid"`, `"minimal"` |
| `colorScheme` | string | `"default"` | Color scheme name |
| `theme` | dict | - | Custom theme overrides |

#### Advanced Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `layoutOptions` | string | - | ELK layout JSON string |
| `connectionRules` | dict | - | Connection validation rules |
| `deleteKeyCode` | string | `"Backspace"` | Delete key |
| `selectionKeyCode` | string | `"Shift"` | Multi-select key |
| `preventDelete` | bool | `False` | Prevent all deletion |
| `preventDeleteNodes` | list | `[]` | Protected node IDs |
| `preventDeleteEdges` | list | `[]` | Protected edge IDs |

#### Output Props (Callback Outputs)

| Prop | Type | Description |
|------|------|-------------|
| `selectedNodes` | list | Currently selected node IDs |
| `selectedEdges` | list | Currently selected edge IDs |
| `clickedNode` | dict | Last clicked node |
| `doubleClickedNode` | dict | Last double-clicked node |
| `hoveredNode` | dict | Currently hovered node |
| `clickedEdge` | dict | Last clicked edge |
| `lastConnection` | dict | Last created connection |
| `deletedNodes` | list | Recently deleted node IDs |
| `deletedEdges` | list | Recently deleted edge IDs |
| `viewport` | dict | Current viewport `{x, y, zoom}` |
| `droppedNode` | dict | Externally dropped node |

#### Action Props (Triggers)

| Prop | Type | Description |
|------|------|-------------|
| `downloadImage` | dict | Trigger image export |
| `copyAction` | bool | Trigger copy |
| `pasteAction` | dict | Trigger paste with offset |
| `restoreFlowState` | dict | Import saved state |

---

## Best Practices

1. **Always use unique IDs** for nodes and edges
2. **Use `fitView=True`** for better initial user experience
3. **Specify handle IDs** when nodes have multiple handles
4. **Use connection rules** to prevent invalid connections
5. **Group related nodes** with GroupNode for organization
6. **Provide status feedback** during long operations
7. **Use responsive sizing** with percentage-based dimensions
8. **Limit minimap** for flows with >100 nodes
9. **Test theme combinations** for accessibility
10. **Use callbacks efficiently** - avoid unnecessary re-renders

---

## Troubleshooting

### Common Issues

**Nodes not appearing:**
- Ensure nodes have `id`, `data`, and `position` properties
- Check that the container has a defined height

**Edges not connecting:**
- Verify source and target IDs match existing node IDs
- For multi-handle nodes, specify `sourceHandle` and `targetHandle`

**Layout not applying:**
- Ensure `layoutOptions` is a valid JSON string
- Check ELK algorithm name spelling

**Callbacks not firing:**
- Add `prevent_initial_call=True` for event callbacks
- Check that component ID matches

---

## Resources

- [GitHub Repository](https://github.com/pip-install-python/dash-flows)
- [Dash Documentation](https://dash.plotly.com/)
- [React Flow Documentation](https://reactflow.dev/)
- [ELK Layout Algorithms](https://www.eclipse.org/elk/reference/algorithms.html)