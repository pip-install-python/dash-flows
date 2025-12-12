# DashFlows Examples

This directory contains comprehensive examples demonstrating all features of the DashFlows component.

## Running Examples

Each example can be run independently:

```bash
python examples/01_basic_nodes_and_edges.py
```

Most examples use `dash-mantine-components` for the UI controls. Install it with:

```bash
pip install dash-mantine-components
```

## Example Index

| # | Example | Description | Port |
|---|---------|-------------|------|
| 01 | [Basic Nodes and Edges](01_basic_nodes_and_edges.py) | Fundamental building blocks | 8050 |
| 02 | [All Node Types](02_all_node_types.py) | Default, Input, Output, Group, Toolbar, Resizable, Circle | 8051 |
| 03 | [All Edge Types](03_all_edge_types.py) | Straight, Step, SmoothStep, SimpleBezier, Button | 8052 |
| 04 | [Background Variants](04_background_variants.py) | Dots, Lines, Cross patterns | 8053 |
| 05 | [Controls and MiniMap](05_controls_and_minimap.py) | Zoom, fit view, navigation | 8054 |
| 06 | [Handle Configurations](06_handle_configurations.py) | Multiple handles, positions, styling | 8055 |
| 07 | [Node Interactions](07_node_interactions.py) | Click, drag, selection callbacks | 8056 |
| 08 | [Connection Validation](08_connection_validation.py) | Rules, validation, visual feedback | 8057 |
| 09 | [Viewport Controls](09_viewport_controls.py) | Zoom, pan, fit view, locks | 8058 |
| 10 | [Selection and Multi-Select](10_selection_multiselect.py) | Single, multi, box selection | 8059 |
| 11 | [Dark Mode with Mantine](11_dark_mode_mantine.py) | Theme integration, CSS variables | 8060 |
| 12 | [ELK Layouts](12_elk_layouts.py) | Automatic layout algorithms | 8061 |
| 13 | [Complete Showcase](13_complete_showcase.py) | All features combined | 8062 |

## Features Covered

### Node Types
- **default**: Standard node with source and target handles
- **input**: Entry node with only source handle (green accent)
- **output**: Exit node with only target handle (purple accent)
- **group**: Container node that holds child nodes
- **toolbar**: Node with action toolbar on selection
- **resizable**: Node with resize handles
- **circle**: Animated circular node

### Edge Types
- **default**: React Flow's built-in bezier curve
- **straight**: Direct line connection
- **step**: Right-angled path with sharp corners
- **smoothstep**: Right-angled with rounded corners
- **simplebezier**: Simple curved line
- **button**: Edge with interactive delete button
- **animated**: Edge with animation using Dash components

### Background Options
- **dots**: Grid of dots (default)
- **lines**: Horizontal and vertical lines
- **cross**: Crosshatch pattern
- Custom colors, gaps, and sizes

### Interactive Features
- Node drag and drop
- Edge creation by connecting handles
- Selection (single, multi, box)
- Zoom and pan
- Fit view
- MiniMap navigation

### Theming
- Apple-inspired glass morphism design
- Light and dark mode support
- Integration with dash-mantine-components
- CSS custom properties for customization

### Layout Algorithms (ELK)
- Layered (hierarchical) - all directions
- Force-directed
- Radial
- Stress

## Glass UI Styling

DashFlows uses a glass morphism design inspired by Apple's UI. The styling is implemented using CSS custom properties that automatically adapt to light and dark modes.

Key CSS variables:
- `--df-glass-blur`: Blur amount for glass effect
- `--df-node-bg`: Node background color
- `--df-edge-color`: Edge stroke color
- `--df-handle-bg`: Handle background color

See `src/lib/styles/glass-theme.css` for the complete list of variables.

## Integration with Dash Mantine Components

DashFlows automatically detects the Mantine color scheme via the `data-mantine-color-scheme` attribute. Simply wrap your app in `MantineProvider` and toggle the theme - DashFlows will update automatically.

```python
import dash_mantine_components as dmc

app.layout = dmc.MantineProvider(
    forceColorScheme="dark",  # or "light"
    children=[
        dash_flows.DashFlows(...)
    ]
)
```