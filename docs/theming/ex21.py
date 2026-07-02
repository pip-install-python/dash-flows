"""
Embeddable twin of examples/21_ui_components.py for the docs page.
Rendered via `.. exec::docs.theming.ex21`.

Demonstrates several UI-focused building blocks: node status ("initial" /
"loading" / "success" / "error"), DataEdge (values rendered on the edge
itself), AnimatedSvgEdge (shapes traveling along a path), and a simple search
panel that focuses nodes via `viewportAction`.
"""
import random

import dash
from dash import html, dcc, callback, Input, Output, State, ctx
from dash.exceptions import PreventUpdate
import dash_flows as df
import dash_mantine_components as dmc

# Initial nodes demonstrating various features
initial_nodes = [
    # Status indicator demo nodes
    {
        'id': 'status-initial',
        'type': 'default',
        'position': {'x': 50, 'y': 50},
        'data': {
            'label': 'Initial State',
            'status': 'initial',
            'value': 0
        },
    },
    {
        'id': 'status-loading',
        'type': 'default',
        'position': {'x': 250, 'y': 50},
        'data': {
            'label': 'Loading State',
            'status': 'loading',
            'value': 42
        },
    },
    {
        'id': 'status-success',
        'type': 'default',
        'position': {'x': 450, 'y': 50},
        'data': {
            'label': 'Success State',
            'status': 'success',
            'value': 100
        },
    },
    {
        'id': 'status-error',
        'type': 'default',
        'position': {'x': 650, 'y': 50},
        'data': {
            'label': 'Error State',
            'status': 'error',
            'value': -1
        },
    },
    # Data flow demo nodes
    {
        'id': 'data-source',
        'type': 'input',
        'position': {'x': 100, 'y': 250},
        'data': {
            'label': 'Data Source',
            'price': 1299.99,
            'count': 42,
            'status': 'active'
        },
    },
    {
        'id': 'data-processor',
        'type': 'default',
        'position': {'x': 350, 'y': 250},
        'data': {
            'label': 'Processor',
            'multiplier': 2,
            'output': 2599.98
        },
    },
    {
        'id': 'data-output',
        'type': 'output',
        'position': {'x': 600, 'y': 250},
        'data': {
            'label': 'Output',
            'result': 'Complete'
        },
    },
    # Animated edge demo nodes
    {
        'id': 'anim-start',
        'type': 'input',
        'position': {'x': 50, 'y': 450},
        'data': {'label': 'Start'},
    },
    {
        'id': 'anim-circle',
        'type': 'default',
        'position': {'x': 250, 'y': 400},
        'data': {'label': 'Circle Animation'},
    },
    {
        'id': 'anim-arrow',
        'type': 'default',
        'position': {'x': 250, 'y': 500},
        'data': {'label': 'Arrow Animation'},
    },
    {
        'id': 'anim-pulse',
        'type': 'default',
        'position': {'x': 450, 'y': 400},
        'data': {'label': 'Pulse Animation'},
    },
    {
        'id': 'anim-rect',
        'type': 'default',
        'position': {'x': 450, 'y': 500},
        'data': {'label': 'Rect Animation'},
    },
    {
        'id': 'anim-end',
        'type': 'output',
        'position': {'x': 650, 'y': 450},
        'data': {'label': 'End'},
    },
]

# Initial edges demonstrating DataEdge and AnimatedSvgEdge
initial_edges = [
    # Data edges showing values from source nodes
    {
        'id': 'e-data-1',
        'source': 'data-source',
        'target': 'data-processor',
        'type': 'data',
        'data': {
            'key': 'price',
            'prefix': '$',
        },
    },
    {
        'id': 'e-data-2',
        'source': 'data-processor',
        'target': 'data-output',
        'type': 'data',
        'data': {
            'key': 'output',
            'prefix': 'Total: $',
        },
    },
    # Animated SVG edges with different shapes
    {
        'id': 'e-anim-circle',
        'source': 'anim-start',
        'target': 'anim-circle',
        'type': 'animatedSvg',
        'data': {
            'shape': 'circle',
            'duration': 2,
            'size': 5,
            'color': '#3b82f6',
            'count': 2,
        },
    },
    {
        'id': 'e-anim-arrow',
        'source': 'anim-start',
        'target': 'anim-arrow',
        'type': 'animatedSvg',
        'data': {
            'shape': 'arrow',
            'duration': 1.5,
            'size': 6,
            'color': '#10b981',
            'count': 3,
        },
    },
    {
        'id': 'e-anim-pulse',
        'source': 'anim-circle',
        'target': 'anim-pulse',
        'type': 'animatedSvg',
        'data': {
            'shape': 'pulse',
            'duration': 2.5,
            'size': 4,
            'color': '#f59e0b',
            'count': 2,
        },
    },
    {
        'id': 'e-anim-rect',
        'source': 'anim-arrow',
        'target': 'anim-rect',
        'type': 'animatedSvg',
        'data': {
            'shape': 'rect',
            'duration': 2,
            'size': 4,
            'color': '#8b5cf6',
            'count': 2,
        },
    },
    {
        'id': 'e-anim-end-1',
        'source': 'anim-pulse',
        'target': 'anim-end',
        'type': 'animatedSvg',
        'data': {
            'shape': 'circle',
            'duration': 1.5,
            'size': 6,
            'color': '#ef4444',
            'count': 1,
            'reverse': False,
        },
    },
    {
        'id': 'e-anim-end-2',
        'source': 'anim-rect',
        'target': 'anim-end',
        'type': 'animatedSvg',
        'data': {
            'shape': 'arrow',
            'duration': 1.5,
            'size': 5,
            'color': '#ec4899',
            'count': 2,
        },
    },
    # Status indicator connections
    {
        'id': 'e-status-1',
        'source': 'status-initial',
        'target': 'status-loading',
        'type': 'animatedSvg',
        'data': {
            'shape': 'circle',
            'duration': 1,
            'size': 4,
            'color': '#64748b',
            'count': 1,
        },
    },
    {
        'id': 'e-status-2',
        'source': 'status-loading',
        'target': 'status-success',
        'type': 'animatedSvg',
        'data': {
            'shape': 'pulse',
            'duration': 1,
            'size': 4,
            'color': '#3b82f6',
            'count': 2,
        },
    },
    {
        'id': 'e-status-3',
        'source': 'status-loading',
        'target': 'status-error',
        'type': 'animatedSvg',
        'data': {
            'shape': 'arrow',
            'duration': 1,
            'size': 4,
            'color': '#ef4444',
            'count': 1,
        },
    },
]

component = html.Div([
    # Control Panel
    html.Div([
        # Node Search Toggle
        dmc.Button(
            "Toggle Search",
            id="ex21-toggle-search",
            variant="light",
            color="blue",
            size="sm",
        ),

        # Status simulation controls
        dmc.Button(
            "Simulate Loading",
            id="ex21-btn-simulate-loading",
            variant="light",
            color="orange",
            size="sm",
            style={'marginLeft': '10px'},
        ),

        # Data update controls
        dmc.Button(
            "Update Data Values",
            id="ex21-btn-update-data",
            variant="light",
            color="green",
            size="sm",
            style={'marginLeft': '10px'},
        ),

        # Fit view
        dmc.Button(
            "Fit View",
            id="ex21-btn-fit-view",
            variant="light",
            color="gray",
            size="sm",
            style={'marginLeft': '10px'},
        ),

        # Animation speed control
        html.Div([
            html.Label("Animation Speed:", style={'marginRight': '10px', 'fontSize': '14px'}),
            dmc.SegmentedControl(
                id="ex21-animation-speed",
                value="normal",
                data=[
                    {"value": "slow", "label": "Slow"},
                    {"value": "normal", "label": "Normal"},
                    {"value": "fast", "label": "Fast"},
                ],
                size="xs",
            ),
        ], style={'display': 'flex', 'alignItems': 'center', 'marginLeft': '20px'}),

    ], style={
        'padding': '10px 0',
        'display': 'flex',
        'alignItems': 'center',
        'flexWrap': 'wrap',
        'rowGap': '10px',
    }),

    # Node Search Panel (hidden by default)
    html.Div(
        id="ex21-search-panel",
        children=[
            dmc.TextInput(
                id="ex21-node-search-input",
                placeholder="Search nodes by label or ID...",
                style={'width': '300px'},
                leftSection=html.Span("\U0001F50D"),
            ),
            html.Div(id="ex21-search-results", style={'marginTop': '10px'}),
        ],
        style={
            'display': 'none',
            'position': 'absolute',
            'top': '70px',
            'left': '50%',
            'transform': 'translateX(-50%)',
            'zIndex': 1000,
            'padding': '15px',
            'backgroundColor': 'var(--mantine-color-body)',
            'backdropFilter': 'blur(10px)',
            'borderRadius': '12px',
            'boxShadow': '0 8px 32px rgba(0, 0, 0, 0.15)',
            'border': '1px solid var(--mantine-color-default-border)',
        },
    ),

    # Flow Container
    html.Div([
        df.DashFlows(
            id='ex21-flow',
            nodes=initial_nodes,
            edges=initial_edges,
            style={
                'height': '500px',
                'border': '1px solid var(--mantine-color-default-border)',
                'borderRadius': '8px',
            },
            fitView=True,
            showMiniMap=True,
            showControls=True,
            showBackground=True,
            colorMode='light',
            themePreset='glass',
        ),
    ], style={'position': 'relative'}),

    # Info Panel
    dmc.Grid([
        dmc.GridCol([
            html.Div([
                html.Strong("DataEdge"),
                html.P("Displays data from the source node on the edge itself. "
                       "See the 'price' and 'output' values on the middle row edges.",
                       style={'fontSize': '13px', 'margin': '5px 0 0 0', 'color': 'var(--mantine-color-dimmed)'}),
            ]),
        ], span=4),
        dmc.GridCol([
            html.Div([
                html.Strong("AnimatedSvgEdge"),
                html.P("Animated shapes traveling along edges: circle, arrow, pulse, rect. "
                       "Watch the bottom section for all animation types.",
                       style={'fontSize': '13px', 'margin': '5px 0 0 0', 'color': 'var(--mantine-color-dimmed)'}),
            ]),
        ], span=4),
        dmc.GridCol([
            html.Div([
                html.Strong("Node Status"),
                html.P("Top row shows different states. Click 'Simulate Loading' to see "
                       "the status transition through states.",
                       style={'fontSize': '13px', 'margin': '5px 0 0 0', 'color': 'var(--mantine-color-dimmed)'}),
            ]),
        ], span=4),
    ], mt="md"),

    # Store for search state
    dcc.Store(id='ex21-search-open', data=False),
])


# Toggle search panel
@callback(
    [Output('ex21-search-panel', 'style'),
     Output('ex21-search-open', 'data')],
    Input('ex21-toggle-search', 'n_clicks'),
    State('ex21-search-open', 'data'),
    State('ex21-search-panel', 'style'),
    prevent_initial_call=True,
)
def toggle_search(n_clicks, is_open, current_style):
    if not n_clicks:
        raise PreventUpdate

    new_style = {**current_style}
    new_style['display'] = 'none' if is_open else 'block'
    return new_style, not is_open


# Search nodes
@callback(
    [Output('ex21-search-results', 'children'),
     Output('ex21-flow', 'viewportAction', allow_duplicate=True)],
    Input('ex21-node-search-input', 'value'),
    State('ex21-flow', 'nodes'),
    prevent_initial_call=True,
)
def search_nodes(search_term, nodes):
    if not search_term or len(search_term) < 2:
        return [], dash.no_update

    term = search_term.lower()
    matches = []

    for node in nodes:
        node_id = node['id'].lower()
        label = node.get('data', {}).get('label', '').lower()

        if term in node_id or term in label:
            matches.append(node)

    if not matches:
        return html.Div("No nodes found", style={'color': 'var(--mantine-color-dimmed)', 'padding': '10px'}), dash.no_update

    results = []
    for node in matches[:5]:  # Limit to 5 results
        results.append(
            dmc.Button(
                f"{node['data'].get('label', node['id'])} ({node['id']})",
                id={'type': 'ex21-search-result', 'id': node['id']},
                variant="subtle",
                fullWidth=True,
                size="sm",
                style={'marginBottom': '5px', 'justifyContent': 'flex-start'},
            )
        )

    return results, dash.no_update


# Focus on searched node
@callback(
    Output('ex21-flow', 'viewportAction'),
    Input({'type': 'ex21-search-result', 'id': dash.ALL}, 'n_clicks'),
    prevent_initial_call=True,
)
def focus_search_result(n_clicks):
    if not any(n_clicks):
        raise PreventUpdate

    triggered = ctx.triggered_id
    if triggered and isinstance(triggered, dict):
        node_id = triggered['id']
        return {
            'action': 'focusNode',
            'nodeId': node_id,
            'zoom': 1.5,
            'duration': 500,
        }

    raise PreventUpdate


# Fit view button
@callback(
    Output('ex21-flow', 'viewportAction', allow_duplicate=True),
    Input('ex21-btn-fit-view', 'n_clicks'),
    prevent_initial_call=True,
)
def fit_view(n_clicks):
    if not n_clicks:
        raise PreventUpdate
    return {'action': 'fitView', 'options': {'padding': 0.2, 'duration': 500}}


# Simulate loading states
@callback(
    Output('ex21-flow', 'nodes', allow_duplicate=True),
    Input('ex21-btn-simulate-loading', 'n_clicks'),
    State('ex21-flow', 'nodes'),
    prevent_initial_call=True,
)
def simulate_loading(n_clicks, nodes):
    if not n_clicks:
        raise PreventUpdate

    # Cycle through states
    states = ['initial', 'loading', 'success', 'error']

    updated_nodes = []
    for node in nodes:
        if node['id'].startswith('status-'):
            current_status = node['data'].get('status', 'initial')
            current_idx = states.index(current_status) if current_status in states else 0
            next_idx = (current_idx + 1) % len(states)

            updated_node = {
                **node,
                'data': {
                    **node['data'],
                    'status': states[next_idx],
                }
            }
            updated_nodes.append(updated_node)
        else:
            updated_nodes.append(node)

    return updated_nodes


# Update data values (to show DataEdge updates)
@callback(
    Output('ex21-flow', 'nodes', allow_duplicate=True),
    Input('ex21-btn-update-data', 'n_clicks'),
    State('ex21-flow', 'nodes'),
    prevent_initial_call=True,
)
def update_data_values(n_clicks, nodes):
    if not n_clicks:
        raise PreventUpdate

    updated_nodes = []
    for node in nodes:
        if node['id'] == 'data-source':
            new_price = round(random.uniform(500, 2000), 2)
            updated_node = {
                **node,
                'data': {
                    **node['data'],
                    'price': new_price,
                    'count': random.randint(10, 100),
                }
            }
            updated_nodes.append(updated_node)
        elif node['id'] == 'data-processor':
            # Find source price
            source_price = 1299.99
            for n in nodes:
                if n['id'] == 'data-source':
                    source_price = n['data'].get('price', 1299.99)
                    break

            multiplier = random.choice([1.5, 2, 2.5, 3])
            updated_node = {
                **node,
                'data': {
                    **node['data'],
                    'multiplier': multiplier,
                    'output': round(source_price * multiplier, 2),
                }
            }
            updated_nodes.append(updated_node)
        else:
            updated_nodes.append(node)

    return updated_nodes


# Update animation speed
@callback(
    Output('ex21-flow', 'edges'),
    Input('ex21-animation-speed', 'value'),
    State('ex21-flow', 'edges'),
    prevent_initial_call=True,
)
def update_animation_speed(speed, edges):
    if not speed:
        raise PreventUpdate

    speed_multipliers = {
        'slow': 2.0,
        'normal': 1.0,
        'fast': 0.5,
    }

    multiplier = speed_multipliers.get(speed, 1.0)
    base_durations = {
        'e-anim-circle': 2,
        'e-anim-arrow': 1.5,
        'e-anim-pulse': 2.5,
        'e-anim-rect': 2,
        'e-anim-end-1': 1.5,
        'e-anim-end-2': 1.5,
        'e-status-1': 1,
        'e-status-2': 1,
        'e-status-3': 1,
    }

    updated_edges = []
    for edge in edges:
        if edge['type'] == 'animatedSvg' and edge['id'] in base_durations:
            updated_edge = {
                **edge,
                'data': {
                    **edge.get('data', {}),
                    'duration': base_durations[edge['id']] * multiplier,
                }
            }
            updated_edges.append(updated_edge)
        else:
            updated_edges.append(edge)

    return updated_edges


# Follow the docs page's light/dark preference on this canvas. The app stores the
# active scheme in `color-scheme-storage` (which also drives the page-level
# MantineProvider), so mirroring it keeps the flow in sync with the page.
@callback(
    Output('ex21-flow', 'colorMode'),
    Input('color-scheme-storage', 'data'),
)
def ex21_sync_color_mode(scheme):
    return scheme or 'light'
