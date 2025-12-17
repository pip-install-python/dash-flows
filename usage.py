"""
Dash Flows - Usage Example with Theming

This example demonstrates:
- Theme presets (glass, solid, minimal)
- Dark/light mode toggle
- Custom theme colors via the theme prop
- Various node types (input, output, default, resizable, toolbar)
- Edge types and connections
"""
import dash
from dash import html, Input, Output, State, clientside_callback, dcc, callback
import dash_flows
import dash_mantine_components as dmc
import json

app = dash.Dash(__name__, assets_folder="assets")

# Example nodes showcasing different node types
initial_nodes = [
    # Input node (green accent, source handle only)
    {
        "id": "input-1",
        "type": "input",
        "data": {
            "label": "Data Source",
            "sublabel": "API Endpoint",
        },
        "position": {"x": 50, "y": 50},
    },
    # Default node (standard node with both handles)
    {
        "id": "default-1",
        "type": "default",
        "data": {
            "label": "Process Data",
            "sublabel": "Transform & Validate",
        },
        "position": {"x": 50, "y": 200},
    },
    # Another default node
    {
        "id": "default-2",
        "type": "default",
        "data": {
            "label": "Filter Records",
        },
        "position": {"x": 250, "y": 200},
    },
    # Output node (purple accent, target handle only)
    {
        "id": "output-1",
        "type": "output",
        "data": {
            "label": "Output",
            "sublabel": "Database",
        },
        "position": {"x": 150, "y": 350},
    },
    # Toolbar node example
    {
        "id": "toolbar-1",
        "type": "toolbar",
        "data": {
            "label": "Configurable Node",
            "sublabel": "Click for options",
            "toolbarButtons": [
                {"icon": "edit", "action": "edit"},
                {"icon": "copy", "action": "copy"},
                {"icon": "delete", "action": "delete"},
            ],
        },
        "position": {"x": 450, "y": 100},
    },
    # Resizable node with custom content
    {
        "id": "resizable-1",
        "type": "resizable",
        "data": {
            "label": html.Div(
                [
                    html.Img(
                        src="https://avatars.githubusercontent.com/u/120129682?v=4",
                        style={"width": "100%", "height": "100%", "objectFit": "cover", "borderRadius": "8px"},
                    ),
                ],
                style={
                    "width": "100%",
                    "height": "100%",
                    "padding": "8px",
                    "boxSizing": "border-box",
                },
            ),
            "handles": [
                {"type": "target", "position": "top", "id": "h1"},
                {"type": "source", "position": "bottom", "id": "h2"},
            ],
        },
        "position": {"x": 450, "y": 250},
        "style": {"width": 150, "height": 150},
    },
]

initial_edges = [
    {
        "id": "e-input-default",
        "source": "input-1",
        "target": "default-1",
        "type": "smoothstep",
        "animated": True,
    },
    {
        "id": "e-default1-default2",
        "source": "default-1",
        "target": "default-2",
        "type": "smoothstep",
    },
    {
        "id": "e-default1-output",
        "source": "default-1",
        "target": "output-1",
        "type": "smoothstep",
        "label": "validated",
    },
    {
        "id": "e-default2-output",
        "source": "default-2",
        "target": "output-1",
        "type": "smoothstep",
    },
    {
        "id": "e-toolbar-resizable",
        "source": "toolbar-1",
        "target": "resizable-1",
        "targetHandle": "h1",
        "type": "smoothstep",
    },
]

# Theme preset options
theme_presets = [
    {"value": "glass", "label": "Glass (Default)"},
    {"value": "solid", "label": "Solid"},
    {"value": "minimal", "label": "Minimal"},
]

# Color mode options
color_modes = [
    {"value": "light", "label": "Light"},
    {"value": "dark", "label": "Dark"},
    {"value": "system", "label": "System"},
]

# Color scheme options
color_schemes = [
    {"value": "default", "label": "Default"},
    {"value": "ocean", "label": "Ocean"},
    {"value": "forest", "label": "Forest"},
    {"value": "sunset", "label": "Sunset"},
    {"value": "midnight", "label": "Midnight"},
    {"value": "rose", "label": "Rose"},
]


def create_controls():
    """Create the control panel for theming options."""
    return dmc.Paper(
        [
            dmc.Text("Theme Controls", fw=600, size="lg", mb="md"),
            dmc.Stack(
                [
                    # Theme Preset
                    dmc.Select(
                        id="theme-preset-select",
                        label="Theme Preset",
                        data=theme_presets,
                        value="glass",
                        w=200,
                    ),
                    # Color Mode
                    dmc.Select(
                        id="color-mode-select",
                        label="Color Mode",
                        data=color_modes,
                        value="light",
                        w=200,
                    ),
                    # Color Scheme
                    dmc.Select(
                        id="color-scheme-select",
                        label="Color Scheme",
                        data=color_schemes,
                        value="default",
                        w=200,
                    ),
                    # Glass Blur
                    dmc.NumberInput(
                        id="glass-blur-input",
                        label="Glass Blur (px)",
                        value=12,
                        min=0,
                        max=30,
                        step=2,
                        w=200,
                    ),
                    # Border Radius
                    dmc.NumberInput(
                        id="border-radius-input",
                        label="Border Radius (px)",
                        value=14,
                        min=0,
                        max=30,
                        step=2,
                        w=200,
                    ),
                    # Edge Stroke Width
                    dmc.NumberInput(
                        id="edge-width-input",
                        label="Edge Width (px)",
                        value=2,
                        min=1,
                        max=5,
                        step=0.5,
                        w=200,
                    ),
                    dmc.Divider(my="md"),
                    # Layout buttons
                    dmc.Text("Auto Layout", fw=500, size="sm"),
                    dmc.Group(
                        [
                            dmc.Button("Vertical", id="btn-vertical", variant="outline", size="xs"),
                            dmc.Button("Horizontal", id="btn-horizontal", variant="outline", size="xs"),
                        ],
                        gap="xs",
                    ),
                    dmc.Group(
                        [
                            dmc.Button("Radial", id="btn-radial", variant="outline", size="xs"),
                            dmc.Button("Force", id="btn-force", variant="outline", size="xs"),
                        ],
                        gap="xs",
                    ),
                ],
                gap="sm",
            ),
        ],
        p="md",
        radius="md",
        withBorder=True,
        style={"position": "absolute", "top": 16, "right": 16, "zIndex": 100, "width": 250},
    )


app.layout = dmc.MantineProvider(
    id="mantine-provider",
    forceColorScheme="light",
    children=[
        html.Div(
            [
                # Controls panel
                create_controls(),
                # DashFlows component
                dash_flows.DashFlows(
                    id="flow-example",
                    nodes=initial_nodes,
                    edges=initial_edges,
                    # Theming props
                    colorMode="light",
                    themePreset="glass",
                    colorScheme="default",
                    theme={
                        "glassBlur": 12,
                        "borderRadius": 14,
                        "edgeStrokeWidth": 2,
                    },
                    # Display options
                    showMiniMap=True,
                    showControls=True,
                    showBackground=True,
                    showDevTools=False,
                    # Behavior
                    fitView=True,
                    fitViewOptions={"padding": 0.2},
                    # Style
                    style={"height": "100vh", "width": "100%"},
                ),
                # Store for layout options
                dcc.Store(id="nodes-store", data=initial_nodes),
            ],
            style={"position": "relative", "height": "100vh"},
        ),
    ],
)


@callback(
    Output("flow-example", "colorMode"),
    Output("mantine-provider", "forceColorScheme"),
    Input("color-mode-select", "value"),
)
def update_color_mode(color_mode):
    """Update both React Flow and Mantine color modes."""
    mantine_scheme = None if color_mode == "system" else color_mode
    return color_mode, mantine_scheme


@callback(
    Output("flow-example", "themePreset"),
    Input("theme-preset-select", "value"),
)
def update_theme_preset(preset):
    """Update the theme preset."""
    return preset


@callback(
    Output("flow-example", "colorScheme"),
    Input("color-scheme-select", "value"),
)
def update_color_scheme(scheme):
    """Update the color scheme."""
    return scheme


@callback(
    Output("flow-example", "theme"),
    Input("glass-blur-input", "value"),
    Input("border-radius-input", "value"),
    Input("edge-width-input", "value"),
)
def update_custom_theme(blur, radius, edge_width):
    """Update custom theme values."""
    return {
        "glassBlur": blur or 12,
        "borderRadius": radius or 14,
        "edgeStrokeWidth": edge_width or 2,
    }


# Layout clientside callback
app.clientside_callback(
    """
    function(n_vertical, n_horizontal, n_radial, n_force) {
        const triggered = dash_clientside.callback_context.triggered[0];
        if (!triggered) return window.dash_clientside.no_update;

        const btnId = triggered.prop_id.split('.')[0];
        let options = {};

        switch(btnId) {
            case 'btn-vertical':
                options = {
                    'elk.algorithm': 'layered',
                    'elk.direction': 'DOWN',
                    'elk.spacing.nodeNode': 80,
                    'elk.layered.spacing.nodeNodeBetweenLayers': 100
                };
                break;
            case 'btn-horizontal':
                options = {
                    'elk.algorithm': 'layered',
                    'elk.direction': 'RIGHT',
                    'elk.spacing.nodeNode': 80,
                    'elk.layered.spacing.nodeNodeBetweenLayers': 100
                };
                break;
            case 'btn-radial':
                options = {
                    'elk.algorithm': 'org.eclipse.elk.radial',
                    'elk.radial.radius': 200
                };
                break;
            case 'btn-force':
                options = {
                    'elk.algorithm': 'org.eclipse.elk.force',
                    'elk.force.iterations': 300,
                    'elk.spacing.nodeNode': 80
                };
                break;
            default:
                return window.dash_clientside.no_update;
        }
        return JSON.stringify(options);
    }
    """,
    Output("flow-example", "layoutOptions"),
    Input("btn-vertical", "n_clicks"),
    Input("btn-horizontal", "n_clicks"),
    Input("btn-radial", "n_clicks"),
    Input("btn-force", "n_clicks"),
    prevent_initial_call=True,
)

if __name__ == "__main__":
    app.run(debug=True, port=7777)