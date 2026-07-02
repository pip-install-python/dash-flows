"""
Embeddable twin of examples/11_dark_mode_mantine.py for the docs page.
Rendered via `.. exec::docs.theming.ex11`.

The standalone example toggles the *whole* Mantine theme (via
`forceColorScheme` on a page-level `MantineProvider`) using a clientside
callback. The docs app already owns the page-level `MantineProvider`, so this
twin does not mount its own and does not mutate the page theme. Instead it
scopes the demo to the DashFlows `colorMode` prop on this canvas only.
"""
from dash import html, Input, Output, callback
import dash_flows
import dash_mantine_components as dmc

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

header = dmc.Group(
    [
        dmc.Text("Canvas color mode:", fw=600, size="sm"),
        dmc.SegmentedControl(
            id="ex11-color-mode",
            value="light",
            data=[
                {"value": "light", "label": "Light"},
                {"value": "dark", "label": "Dark"},
                {"value": "system", "label": "System"},
            ],
            size="xs",
        ),
    ],
    justify="space-between",
    style={"marginBottom": "10px"},
)

flow_component = dash_flows.DashFlows(
    id="ex11-flow",
    nodes=nodes,
    edges=edges,
    style={
        "height": "480px",
        "border": "1px solid var(--mantine-color-default-border)",
        "borderRadius": "8px",
    },
    fitView=True,
    showControls=True,
    showMiniMap=True,
    backgroundVariant="dots",
    colorMode="light",
)

theme_info = dmc.Paper(
    [
        dmc.Text("Theme Integration Details:", fw=600, mb="xs"),
        dmc.Text(
            [
                "This canvas reacts to its own ",
                dmc.Code("colorMode"),
                " prop (",
                dmc.Code("light"),
                " / ",
                dmc.Code("dark"),
                " / ",
                dmc.Code("system"),
                "), independent of the rest of this page.",
            ],
            size="sm",
            mb="xs",
        ),
        dmc.List(
            [
                dmc.ListItem("Glass morphism backgrounds adapt to theme"),
                dmc.ListItem("Node colors and shadows change automatically"),
                dmc.ListItem("Edge and handle colors update"),
                dmc.ListItem("Controls and MiniMap match the theme"),
            ],
            size="sm",
        ),
    ],
    p="md",
    withBorder=True,
    mt="md",
)

component = html.Div([
    header,
    flow_component,
    theme_info,
])


@callback(
    Output("ex11-flow", "colorMode"),
    Input("ex11-color-mode", "value"),
    prevent_initial_call=True,
)
def set_color_mode(value):
    return value
