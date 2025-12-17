# Dash Flows

A powerful React Flow integration for Plotly Dash, providing interactive node-based flow diagrams with a comprehensive set of components for building visual workflows, data pipelines, and interactive diagrams.

![Dash Flows Example](assets/current_project.png)

## Features

- **React Flow 12+ Integration**: Built on the latest React Flow library with full Dash compatibility
- **Comprehensive Node Types**: Input, Output, Default, Group, Toolbar, and Resizable nodes
- **Multiple Edge Types**: Bezier, Smooth Step, Step, Straight, Animated SVG, Button, and Data edges
- **Custom Icons**: DashIconify integration for custom node icons with dynamic updates
- **Flexible Node Layouts**: Stacked (vertical) or horizontal layouts with content-aware sizing
- **Glass Morphism Theme**: Beautiful modern UI with glass effects, dark mode support, and multiple color schemes
- **Status Indicators**: Visual loading, success, and error states for nodes
- **ELK Layout Support**: Automatic graph layouts using the ELK algorithm
- **Interactive Features**: Drag-and-drop, copy/paste, context menus, and more
- **Mantine Integration**: Seamless dark/light mode with dash-mantine-components

## Installation

```bash
pip install dash-flows
```

## Quick Start

```python
import dash
from dash import html
from dash_flows import DashFlows

app = dash.Dash(__name__)

nodes = [
    {
        'id': '1',
        'type': 'input',
        'data': {'label': 'Start'},
        'position': {'x': 250, 'y': 0},
    },
    {
        'id': '2',
        'data': {'label': 'Process'},
        'position': {'x': 250, 'y': 100},
    },
    {
        'id': '3',
        'type': 'output',
        'data': {'label': 'End'},
        'position': {'x': 250, 'y': 200},
    },
]

edges = [
    {'id': 'e1-2', 'source': '1', 'target': '2'},
    {'id': 'e2-3', 'source': '2', 'target': '3'},
]

app.layout = html.Div([
    DashFlows(
        id='flow',
        nodes=nodes,
        edges=edges,
        fitView=True,
        style={'width': '100%', 'height': '600px'}
    )
])

if __name__ == '__main__':
    app.run(debug=True)
```

## Components

### Main Component

- **DashFlows**: The main flow canvas component with full React Flow functionality

### Node Types

| Component | Description |
|-----------|-------------|
| `DefaultNode` | Standard node with configurable handles |
| `InputNode` | Source node with green accent (output handles only) |
| `OutputNode` | Sink node with purple accent (input handles only) |
| `GroupNode` | Container node for grouping other nodes |
| `ToolbarNode` | Node with floating toolbar on selection |
| `ResizableNode` | Node that can be resized by the user |

### Edge Types

| Component | Description |
|-----------|-------------|
| `SimpleBezierEdge` | Smooth curved connection |
| `SmoothStepEdge` | Rounded right-angle connections |
| `StepEdge` | Sharp right-angle connections |
| `StraightEdge` | Direct line connection |
| `AnimatedSvgEdge` | Edge with animated flowing dots |
| `ButtonEdge` | Edge with delete button |
| `DataEdge` | Edge displaying data labels |

### UI Components

| Component | Description |
|-----------|-------------|
| `NodeStatusIndicator` | Loading/success/error states for nodes |
| `NodeTooltip` | Hover tooltips for nodes |
| `NodeSearch` | Search and filter nodes |
| `ButtonHandle` | Interactive handle with button styling |
| `DevTools` | Debug panel for development |

## Theming

Dash Flows includes a comprehensive theming system with CSS custom properties.

### Theme Presets

Apply theme classes to customize the appearance:

- `.df-theme-glass` (default) - Glass morphism with blur effects
- `.df-theme-solid` - Opaque cards with shadows
- `.df-theme-minimal` - Clean, border-focused design

### Color Schemes

- `.df-scheme-default` - Neutral blue/purple
- `.df-scheme-ocean` - Blues and teals
- `.df-scheme-forest` - Greens and browns
- `.df-scheme-sunset` - Oranges and reds
- `.df-scheme-midnight` - Deep blues and purples
- `.df-scheme-rose` - Pinks and reds

### Dark Mode

Dark mode is automatically supported via:
- React Flow's `colorMode="dark"` prop
- Mantine's `data-mantine-color-scheme="dark"` attribute
- Custom `.dark-mode` class

## Node Status Indicators

Wrap nodes with status indicators to show processing states:

```python
from dash_flows import NodeStatusIndicator

# In your node's data
node = {
    'id': '1',
    'data': {
        'label': 'Processing...',
        'status': 'loading',  # 'initial', 'loading', 'success', 'error'
    },
    'position': {'x': 100, 'y': 100},
}
```

Status types:
- `initial` - Default state, no indicator
- `loading` - Blue pulsing glow animation
- `success` - Green border with checkmark badge
- `error` - Red border with X badge and shake animation

## Custom Icons with DashIconify

Add custom icons to nodes using DashIconify:

```python
from dash_iconify import DashIconify

node = {
    'id': '1',
    'type': 'input',
    'data': {
        'label': 'Data Source',
        'icon': DashIconify(icon="mdi:database", width=20, color="white"),
        'iconColor': '#10b981',  # Optional: icon background color
        'body': 'PostgreSQL Database',  # Optional: description text
    },
    'position': {'x': 100, 'y': 100},
}
```

## Node Layouts

Control node appearance with the `layout` prop:

```python
# Stacked layout (default) - icon above text
{'id': '1', 'data': {'label': 'Stacked', 'icon': icon, 'layout': 'stacked'}, ...}

# Horizontal layout - icon left, text right
{'id': '2', 'data': {'label': 'Horizontal', 'icon': icon, 'layout': 'horizontal'}, ...}

# Icon-only (compact) - just set icon without label
{'id': '3', 'data': {'icon': icon, 'showIcon': True}, ...}

# Text-only (centered) - hide icon
{'id': '4', 'data': {'label': 'Centered Text', 'showIcon': False}, ...}
```

## Handle Configuration

Configure handles for custom node connection points:

```python
node = {
    'id': '1',
    'data': {
        'label': 'Custom Handles',
        'handles': [
            {'type': 'target', 'position': 'top', 'id': 'input-1'},
            {'type': 'target', 'position': 'left', 'id': 'input-2'},
            {'type': 'source', 'position': 'bottom', 'id': 'output-1'},
            {'type': 'source', 'position': 'right', 'id': 'output-2'},
        ]
    },
    'position': {'x': 100, 'y': 100},
}
```

## Examples

The `examples/` directory contains comprehensive examples:

| Example | Description |
|---------|-------------|
| `01_basic_nodes_and_edges.py` | Getting started with nodes and edges |
| `02_all_node_types.py` | Showcase of all node types |
| `03_all_edge_types.py` | Showcase of all edge types |
| `04_background_variants.py` | Background patterns (dots, lines, cross) |
| `05_controls_and_minimap.py` | Navigation controls and minimap |
| `06_handle_configurations.py` | Custom handle positions |
| `07_node_interactions.py` | Click, drag, and selection events |
| `08_connection_validation.py` | Validate connections before creation |
| `09_viewport_controls.py` | Zoom and pan controls |
| `10_selection_multiselect.py` | Multi-node selection |
| `11_dark_mode_mantine.py` | Dark mode with Mantine |
| `12_elk_layouts.py` | Automatic ELK layouts |
| `13_complete_showcase.py` | Full feature demonstration |
| `14_dash_components_in_nodes.py` | Embed Dash components in nodes |
| `15_save_restore.py` | Save and restore flow state |
| `16_connection_limits.py` | Limit connections per handle |
| `17_drag_and_drop.py` | Drag nodes from palette |
| `18_export_image.py` | Export flow as image |
| `19_copy_paste.py` | Copy and paste nodes |
| `20_context_menu.py` | Right-click context menus |
| `21_ui_components.py` | UI components showcase |
| `22_custom_icons.py` | Custom icons with DashIconify & layouts |

## API Reference

### DashFlows Props

| Prop | Type | Description |
|------|------|-------------|
| `id` | string | Component ID for callbacks |
| `nodes` | list | Array of node objects |
| `edges` | list | Array of edge objects |
| `fitView` | bool | Auto-fit view to content |
| `colorMode` | string | 'light' or 'dark' |
| `style` | dict | Container style |
| `nodeTypes` | dict | Custom node type mappings |
| `edgeTypes` | dict | Custom edge type mappings |
| `onNodesChange` | callback | Node change handler |
| `onEdgesChange` | callback | Edge change handler |
| `onConnect` | callback | Connection handler |

### Node Object

```python
{
    'id': 'unique-id',
    'type': 'default',  # 'input', 'output', 'group', etc.
    'data': {
        'label': 'Node Label',        # Primary text
        'title': 'Title',             # Alias for label
        'sublabel': 'Secondary text', # Below label
        'body': 'Description',        # Below sublabel
        'icon': DashIconify(...),     # Custom icon
        'iconColor': '#3b82f6',       # Icon background
        'showIcon': True,             # Toggle icon visibility
        'layout': 'stacked',          # 'stacked' or 'horizontal'
        'handles': [...],             # Optional handle config
        'status': 'initial',          # 'initial', 'loading', 'success', 'error'
    },
    'position': {'x': 0, 'y': 0},
    'style': {},  # Optional CSS styles
    'className': '',  # Optional CSS class
}
```

### Edge Object

```python
{
    'id': 'unique-id',
    'source': 'source-node-id',
    'target': 'target-node-id',
    'sourceHandle': 'handle-id',  # Optional
    'targetHandle': 'handle-id',  # Optional
    'type': 'default',  # Edge type
    'animated': False,
    'style': {},
    'label': 'Edge Label',  # Optional
}
```

## Development

### Setup

```bash
# Install dependencies
npm install
pip install -r requirements.txt

# Build components
npm run build

# Run development server
python usage.py
```

### Building

```bash
# Production build
npm run build

# Create distribution
python setup.py sdist bdist_wheel
```

## Requirements

- Python >= 3.8
- Dash >= 3.0.0
- Node.js >= 8.11.0 (for development)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [GitHub Repository](https://github.com/pip-install-python/dash-flows)
- [Issue Tracker](https://github.com/pip-install-python/dash-flows/issues)
- [Dash Documentation](https://dash.plotly.com/)
- [React Flow Documentation](https://reactflow.dev/)