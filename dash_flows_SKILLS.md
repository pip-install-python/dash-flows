# Dash Flows - Complete Developer Guide

A comprehensive guide to building interactive node-based flow diagrams with **dash-flows**, a React Flow 12+ integration for Plotly Dash.

**Version 1.1.0** - Now with DashIconify integration, flexible node layouts, and enhanced React 18+ compatibility!

## Table of Contents

1. [Installation & Setup](#installation--setup)
2. [Quick Start](#quick-start)
3. [Core Concepts](#core-concepts)
4. [Node Types](#node-types)
5. [Custom Icons & Layouts](#custom-icons--layouts) *(New in 1.1.0)*
6. [Edge Types](#edge-types)
7. [Handle Configuration](#handle-configuration)
8. [Styling & Theming](#styling--theming)
9. [Callbacks & Interactivity](#callbacks--interactivity)
10. [Advanced Features](#advanced-features)
11. [Complete Examples](#complete-examples)
12. [API Reference](#api-reference)
13. [Troubleshooting](#troubleshooting)

---

## Installation & Setup

### Install from PyPI

```bash
pip install dash-flows
```

### Requirements

- Python 3.8+
- Dash >= 3.0.0

### Optional Dependencies

```bash
# For custom icons
pip install dash-iconify

# For UI components (theming, dark mode)
pip install dash-mantine-components
```

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

**Note:** Group nodes in v1.1.0 have been simplified to work correctly with React Flow's native group behavior. The styling is applied directly to `.react-flow__node-group` and the component renders only a NodeResizer and optional label badge.

### Toolbar Node

Node with a floating toolbar that appears on selection.

```python
{
    "id": "configurable",
    "type": "toolbar",
    "data": {
        "label": "Configurable Node",
        "sublabel": "Click for actions",
        "toolbarPosition": "top",  # or "bottom", "left", "right"
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

## Custom Icons & Layouts

*New in version 1.1.0*

### Custom Icons with DashIconify

Add custom icons to InputNode, DefaultNode, and OutputNode using DashIconify:

```bash
pip install dash-iconify
```

```python
from dash_iconify import DashIconify

# Node with custom icon
{
    "id": "data-source",
    "type": "input",
    "data": {
        "label": "Data Source",
        "icon": DashIconify(icon="mdi:database", width=20, color="white"),
        "iconColor": "#10b981",  # Icon container background
        "body": "PostgreSQL Database",  # Description text
    },
    "position": {"x": 100, "y": 50},
}
```

**Icon Props:**
| Prop | Type | Description |
|------|------|-------------|
| `icon` | DashIconify | Custom icon component |
| `iconColor` | string | Icon container background color (CSS color) |
| `showIcon` | bool | Toggle icon visibility (default: true if icon provided) |

### Node Layout Options

Control how node content is arranged with the `layout` prop:

#### Stacked Layout (Default)

Vertical arrangement - icon above text:

```python
{
    "id": "stacked-node",
    "type": "default",
    "data": {
        "label": "Process Data",
        "icon": DashIconify(icon="mdi:cog", width=20, color="white"),
        "body": "Transform and validate",
        "layout": "stacked",  # Icon on top, text below
    },
    "position": {"x": 100, "y": 100},
}
```

#### Horizontal Layout

Two-column arrangement - icon on left, text on right:

```python
{
    "id": "horizontal-node",
    "type": "default",
    "data": {
        "label": "Process Data",
        "icon": DashIconify(icon="mdi:cog", width=20, color="white"),
        "body": "Transform and validate",
        "layout": "horizontal",  # Icon left, text right
    },
    "position": {"x": 100, "y": 100},
}
```

### Content-Aware Node Sizing

Nodes automatically adjust their size based on content:

#### Icon-Only Nodes (Compact)

Just an icon, no text - node shrinks to fit:

```python
{
    "id": "icon-only",
    "type": "default",
    "data": {
        "icon": DashIconify(icon="mdi:lightning-bolt", width=24, color="white"),
        "iconColor": "#f59e0b",
        "showIcon": True,
        # No label, body, or sublabel = compact icon-only node
    },
    "position": {"x": 100, "y": 100},
}
```

#### Text-Only Nodes (Centered)

No icon - text is centered without reserved icon space:

```python
{
    "id": "text-only",
    "type": "default",
    "data": {
        "label": "Validate Data",
        "sublabel": "Quality check",
        "showIcon": False,  # Explicitly hide icon
    },
    "position": {"x": 100, "y": 100},
}
```

#### Full Content Nodes

Both icon and text - standard sized node:

```python
{
    "id": "full-content",
    "type": "input",
    "data": {
        "label": "Data Source",
        "sublabel": "External API",
        "body": "REST endpoint",
        "icon": DashIconify(icon="mdi:api", width=20, color="white"),
    },
    "position": {"x": 100, "y": 100},
}
```

### Enhanced Text Props

Additional text properties for richer node content:

```python
{
    "id": "rich-content",
    "type": "default",
    "data": {
        "title": "Primary Title",    # Alias for label
        "label": "Also works",       # Primary text (title takes precedence)
        "sublabel": "Secondary",     # Below title, smaller text
        "body": "Description text",  # Below sublabel, dimmed
        "multiline": True,           # Allow text wrapping
    },
    "position": {"x": 100, "y": 100},
}
```

### Dynamic Icon Updates via Callbacks

Icons update dynamically when node data changes:

```python
from dash import callback, Input, Output, State
from dash_iconify import DashIconify

@callback(
    Output("flow", "nodes"),
    Input("icon-selector", "value"),
    State("flow", "nodes"),
    prevent_initial_call=True,
)
def update_node_icon(icon_name, nodes):
    return [
        {
            **node,
            "data": {
                **node["data"],
                "icon": DashIconify(icon=icon_name, width=20, color="white"),
            }
        }
        if node["id"] == "target-node" else node
        for node in nodes
    ]
```

### Complete Example: Custom Icons Demo

See `examples/22_custom_icons.py` for a full interactive demo with:
- Custom icons for each node type
- Layout toggle (stacked/horizontal)
- Show/hide icon toggle
- Dynamic icon, title, and body updates
- DMC form controls for real-time editing

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
{
    "id": "e1",
    "source": "a",
    "target": "b",
    "type": "animatedSvg",
    "data": {
        "shape": "circle",      # circle, rect, arrow, pulse
        "size": 5,              # Size of the animated shape
        "color": "#3b82f6",     # Color of the shape
        "duration": 2,          # Animation duration in seconds
        "count": 1,             # Number of shapes
        "reverse": False,       # Reverse direction
    },
}
```

### Data Edge

Edge that displays data labels along the path.

```python
{
    "id": "e1",
    "source": "a",
    "target": "b",
    "type": "data",
    "data": {
        "key": "value",         # Key to read from source node's data
        "prefix": "$",          # Prefix before value
        "suffix": "/s",         # Suffix after value
    },
}
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

With Mantine integration (v2.4.0+ pattern):

```python
import dash_mantine_components as dmc
from dash import clientside_callback, Input, Output

# Theme toggle using ActionIcon with darkHidden/lightHidden
theme_toggle = dmc.ActionIcon(
    [
        dmc.Paper(DashIconify(icon="radix-icons:sun", width=25), darkHidden=True),
        dmc.Paper(DashIconify(icon="radix-icons:moon", width=25), lightHidden=True),
    ],
    variant="transparent",
    id="theme-toggle",
    size="lg",
)

app.layout = dmc.MantineProvider(
    id="mantine-provider",
    children=[
        theme_toggle,
        dash_flows.DashFlows(
            id="flow",
            colorMode="light",
            ...
        )
    ]
)

# Modern DMC v2.4.0 dark mode toggle
clientside_callback(
    """
    (n) => {
        if (!n) return window.dash_clientside.no_update;
        const currentScheme = document.documentElement.getAttribute('data-mantine-color-scheme') || 'light';
        const newScheme = currentScheme === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-mantine-color-scheme', newScheme);
        return newScheme;
    }
    """,
    Output("mantine-provider", "forceColorScheme"),
    Input("theme-toggle", "n_clicks"),
    prevent_initial_call=True,
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

### Handle Right-Click Context Menu

```python
@callback(
    Output("context-menu", "children"),
    Input("flow", "contextMenuNode"),
    prevent_initial_call=True,
)
def on_context_menu(context_menu_node):
    if not context_menu_node:
        return "Right-click a node..."
    return json.dumps(context_menu_node, indent=2)
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

### Multi-Selection with Shift Key

Enable multi-selection by holding Shift:

```python
dash_flows.DashFlows(
    ...,
    multiSelectionKeyCode="Shift",  # Hold Shift to add to selection
    selectionKeyCode="Shift",        # Shift+drag for box selection
)
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

### Viewport Control Actions

Control viewport programmatically:

```python
# Using clientside callback for viewport actions
clientside_callback(
    """
    function(n, btnId) {
        if (!n) return window.dash_clientside.no_update;

        switch(btnId) {
            case 'btn-fit-view':
                return {'action': 'fitView', 'options': {padding: 0.2}};
            case 'btn-zoom-in':
                return {'action': 'zoomIn', 'options': {}};
            case 'btn-zoom-out':
                return {'action': 'zoomOut', 'options': {}};
            case 'btn-reset-zoom':
                return {'action': 'setZoom', 'zoom': 1, 'options': {}};
            case 'btn-pan-center':
                return {'action': 'setCenter', 'x': 450, 'y': 300, 'options': {zoom: 1, duration: 500}};
            case 'btn-focus-node':
                return {'action': 'focusNode', 'nodeId': 'node-1', 'zoom': 1.5, 'duration': 500};
            default:
                return window.dash_clientside.no_update;
        }
    }
    """,
    Output("flow", "viewportAction"),
    Input({"type": "viewport-btn", "action": ALL}, "n_clicks"),
    State({"type": "viewport-btn", "action": ALL}, "id"),
)
```

**Important:** For `setCenter`, `x` and `y` must be at the top level of the action object, not inside `options`.

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

The `examples/` directory contains 23 comprehensive examples:

| Example | File | Description |
|---------|------|-------------|
| 01 | `01_basic_nodes_and_edges.py` | Basic flow setup |
| 02 | `02_all_node_types.py` | All node types showcase |
| 03 | `03_all_edge_types.py` | All edge types demo |
| 04 | `04_background_variants.py` | Background patterns |
| 05 | `05_controls_and_minimap.py` | UI controls |
| 06 | `06_handle_configurations.py` | Custom handles |
| 07 | `07_node_interactions.py` | Click, hover, context menu |
| 08 | `08_connection_validation.py` | Connection rules |
| 09 | `09_viewport_controls.py` | Pan, zoom, fit view |
| 10 | `10_selection_multiselect.py` | Selection features |
| 11 | `11_dark_mode_mantine.py` | Dark mode with DMC |
| 12 | `12_elk_layouts.py` | Auto-layout with ELK |
| 13 | `13_complete_showcase.py` | Full feature demo |
| 14 | `14_dash_components_in_nodes.py` | Embed Dash components |
| 15 | `15_save_restore.py` | Save/load state |
| 16 | `16_connection_limits.py` | Connection limits |
| 17 | `17_drag_and_drop.py` | External drag & drop |
| 18 | `18_export_image.py` | Export as image |
| 19 | `19_copy_paste.py` | Copy/paste nodes |
| 20 | `20_context_menu.py` | Custom context menus |
| 21 | `21_ui_components.py` | UI component showcase |
| 22 | `22_custom_icons.py` | DashIconify icons |
| 23 | `23_callback_stress_test.py` | Callback performance test |

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
| `multiSelectionKeyCode` | string | - | Key for multi-select (e.g., "Shift") |
| `selectionKeyCode` | string | `"Shift"` | Key for box selection |

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
| `contextMenuNode` | dict | Right-clicked node with position |
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
| `viewportAction` | dict | Trigger viewport actions (fitView, zoomIn, setCenter, etc.) |
| `downloadImage` | dict | Trigger image export |
| `copyAction` | bool | Trigger copy |
| `pasteAction` | dict | Trigger paste with offset |
| `restoreFlowState` | dict | Import saved state |

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

**Multi-select not working:**
- Add `multiSelectionKeyCode="Shift"` to enable Shift+click selection

**Context menu not showing:**
- Ensure you have a callback listening to `contextMenuNode`
- The component captures right-clicks but you must handle the display

**GroupNode appears with nested container:**
- This was fixed in v1.1.0 - update to latest version
- GroupNode now renders just NodeResizer and label, styling applied to `.react-flow__node-group`

**Viewport control buttons not working:**
- For `setCenter`, ensure `x` and `y` are at top level: `{'action': 'setCenter', 'x': 100, 'y': 100, 'options': {...}}`
- For `setZoom`, ensure `zoom` is at top level: `{'action': 'setZoom', 'zoom': 1.5, 'options': {...}}`

**Dark mode toggle not working (DMC):**
- Use the modern `data-mantine-color-scheme` attribute pattern (DMC v2.4.0+)
- Use `darkHidden`/`lightHidden` props on icon containers for auto-toggle visibility

**React defaultProps warning:**
- Fixed in v1.1.0 - update to latest version
- Component now uses JavaScript default parameters instead of `defaultProps`

---

## Resources

- [GitHub Repository](https://github.com/pip-install-python/dash-flows)
- [Dash Documentation](https://dash.plotly.com/)
- [React Flow Documentation](https://reactflow.dev/)
- [ELK Layout Algorithms](https://www.eclipse.org/elk/reference/algorithms.html)
- [DashIconify Icons](https://icon-sets.iconify.design/)
- [Dash Mantine Components](https://www.dash-mantine-components.com/)
