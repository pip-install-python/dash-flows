"""
Example 11: Dark Mode with Mantine Theme Integration
====================================================
This example demonstrates:
- Light/dark mode toggle using Mantine
- CSS variable integration with dash-mantine-components
- Dynamic theme switching
- Persisting theme preference
"""

import dash
from dash import html, Input, Output, callback, clientside_callback
import dash_flows
import dash_mantine_components as dmc
from dash_iconify import DashIconify

app = dash.Dash(__name__)

nodes = [
    {"id": "input-1", "type": "input", "data": {"label": "Data Source", "sublabel": "API"}, "position": {"x": 100, "y": 50}},
    {"id": "default-1", "type": "default", "data": {"label": "Transform", "sublabel": "ETL Process"}, "position": {"x": 100, "y": 180}},
    {"id": "default-2", "type": "default", "data": {"label": "Validate", "sublabel": "Schema Check"}, "position": {"x": 300, "y": 180}},
    {"id": "toolbar-1", "type": "toolbar", "data": {"label": "Review", "sublabel": "Manual Check"}, "position": {"x": 200, "y": 310}},
    {"id": "output-1", "type": "output", "data": {"label": "Database", "sublabel": "PostgreSQL"}, "position": {"x": 200, "y": 440}},
]

edges = [
    {"id": "e1", "source": "input-1", "target": "default-1", "animated": True},
    {"id": "e2", "source": "default-1", "target": "default-2", "type": "smoothstep"},
    {"id": "e3", "source": "default-2", "target": "toolbar-1"},
    {"id": "e4", "source": "toolbar-1", "target": "output-1"},
]

# Theme toggle button in header
header = dmc.Group([
    dmc.Title("DashFlows Dark Mode Demo", order=3),
    dmc.ActionIcon(
        id="theme-toggle",
        variant="outline",
        size="lg",
        radius="md",
        color='yellow',
        children=[
        dmc.Paper(DashIconify(icon="radix-icons:sun", width=25), darkHidden=True),
        dmc.Paper(DashIconify(icon="radix-icons:moon", width=25), lightHidden=True),
    ],
    ),
], justify="space-between", style={"padding": "10px 20px", "borderBottom": "1px solid var(--mantine-color-gray-3)"})

flow_component = dash_flows.DashFlows(
    id="themed-flow",
    nodes=nodes,
    edges=edges,
    style={"height": "500px"},
    fitView=True,
    showControls=True,
    showMiniMap=True,
    backgroundVariant="dots",
)

theme_info = dmc.Paper([
    dmc.Text("Theme Integration Details:", fw=600, mb="xs"),
    dmc.Text([
        "The DashFlows component automatically responds to the ",
        dmc.Code("data-mantine-color-scheme"),
        " attribute set by MantineProvider."
    ], size="sm", mb="xs"),
    dmc.Text([
        "CSS variables defined in ",
        dmc.Code("glass-theme.css"),
        " provide both light and dark mode styling."
    ], size="sm", mb="xs"),
    dmc.List([
        dmc.ListItem("Glass morphism backgrounds adapt to theme"),
        dmc.ListItem("Node colors and shadows change automatically"),
        dmc.ListItem("Edge and handle colors update"),
        dmc.ListItem("Controls and MiniMap match the theme"),
    ], size="sm"),
], p="md", withBorder=True, mt="md")

# Main layout with MantineProvider for theming
app.layout = dmc.MantineProvider(
    id="mantine-provider",
    forceColorScheme="light",
    children=[
        header,
        html.Div([
            flow_component,
            theme_info,
        ], style={"padding": "20px"}),
    ]
)

# Clientside callback for theme toggle using the modern Mantine pattern
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

if __name__ == "__main__":
    app.run(debug=True, port=8030)