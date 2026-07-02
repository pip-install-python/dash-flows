"""
Embeddable twin of examples/22_custom_icons.py for the docs page.
Rendered via `.. exec::docs.nodes.ex22`.
"""
import dash
from dash import html, callback, Input, Output, State, ALL, ctx
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash_flows

# Initial node configurations showcasing different layouts and content modes
initial_nodes = [
    # Full content node with icon, title, and body (stacked layout)
    {
        "id": "input-1",
        "type": "input",
        "data": {
            "icon": DashIconify(icon="mdi:database", width=20, color="white"),
            "label": "Data Source",
            "body": "PostgreSQL Database",
            "layout": "stacked",
        },
        "position": {"x": 100, "y": 50},
    },
    # Icon-only node (compact sizing)
    {
        "id": "icon-only",
        "type": "default",
        "data": {
            "icon": DashIconify(icon="mdi:lightning-bolt", width=24, color="white"),
            "showIcon": True,
            "iconColor": "#f59e0b",
        },
        "position": {"x": 300, "y": 50},
    },
    # Full content node with horizontal layout
    {
        "id": "process-1",
        "type": "default",
        "data": {
            "icon": DashIconify(icon="mdi:cog", width=20, color="white"),
            "label": "Transform",
            "body": "Clean and normalize",
            "layout": "horizontal",
            "showIcon": True,
        },
        "position": {"x": 100, "y": 200},
    },
    # Text-only node (centered, no icon space reserved)
    {
        "id": "text-only",
        "type": "default",
        "data": {
            "label": "Validate",
            "sublabel": "Quality check",
            "showIcon": False,
        },
        "position": {"x": 300, "y": 200},
    },
    # Output with horizontal layout
    {
        "id": "output-1",
        "type": "output",
        "data": {
            "icon": DashIconify(icon="mdi:chart-bar", width=20, color="white"),
            "label": "Dashboard",
            "body": "Visualization",
            "layout": "horizontal",
        },
        "position": {"x": 100, "y": 350},
    },
    # Icon-only output
    {
        "id": "output-icon",
        "type": "output",
        "data": {
            "icon": DashIconify(icon="mdi:file-export", width=24, color="white"),
            "showIcon": True,
        },
        "position": {"x": 300, "y": 350},
    },
]

initial_edges = [
    {"id": "e1-p1", "source": "input-1", "target": "process-1", "animated": True},
    {"id": "e1-icon", "source": "icon-only", "target": "text-only", "animated": True},
    {"id": "ep1-o1", "source": "process-1", "target": "output-1", "animated": True},
    {"id": "et-oicon", "source": "text-only", "target": "output-icon", "animated": True},
]

# Popular icon suggestions for each node type
icon_suggestions = {
    "input": [
        "mdi:database",
        "mdi:file-document",
        "mdi:api",
        "mdi:cloud-download",
        "mdi:folder",
        "mdi:web",
        "mdi:server",
        "mdi:import",
    ],
    "process": [
        "mdi:cog",
        "mdi:function",
        "mdi:filter",
        "mdi:merge",
        "mdi:swap-horizontal",
        "mdi:code-braces",
        "mdi:math-integral",
        "mdi:lightning-bolt",
    ],
    "output": [
        "mdi:chart-bar",
        "mdi:file-export",
        "mdi:monitor-dashboard",
        "mdi:email-send",
        "mdi:cloud-upload",
        "mdi:database-export",
        "mdi:printer",
        "mdi:share-variant",
    ],
}


def create_node_editor(
    node_id: str,
    node_type: str,
    default_icon: str,
    default_title: str,
    default_body: str,
    default_layout: str = "stacked",
    show_icon: bool = True,
):
    """Create a form section for editing a node's icon, title, body, and layout."""
    suggestions = icon_suggestions.get(node_type, icon_suggestions["process"])

    # Color based on node type
    accent_color = {
        "input": "#10b981",
        "process": "#3b82f6",
        "output": "#8b5cf6",
    }.get(node_type, "#3b82f6")

    return dmc.Paper(
        [
            dmc.Group(
                [
                    DashIconify(
                        icon=default_icon,
                        width=24,
                        color=accent_color,
                    ),
                    dmc.Text(
                        f"{node_type.title()} Node",
                        size="lg",
                        fw=600,
                    ),
                ],
                gap="sm",
                mb="md",
            ),
            # Layout toggle
            dmc.Group(
                [
                    dmc.Text("Layout:", size="sm", fw=500),
                    dmc.SegmentedControl(
                        id={"type": "ex22-layout-toggle", "node": node_id},
                        data=[
                            {"value": "stacked", "label": "Stacked"},
                            {"value": "horizontal", "label": "Horizontal"},
                        ],
                        value=default_layout,
                        size="xs",
                    ),
                ],
                gap="sm",
                mb="sm",
            ),
            # Show icon toggle
            dmc.Switch(
                id={"type": "ex22-show-icon-toggle", "node": node_id},
                label="Show Icon",
                checked=show_icon,
                size="sm",
                mb="sm",
            ),
            dmc.TextInput(
                id={"type": "ex22-icon-input", "node": node_id},
                label="Icon",
                description="Enter an icon name from iconify.design",
                placeholder="mdi:database",
                value=default_icon,
                leftSection=DashIconify(icon="mdi:emoticon", width=16),
                mb="sm",
                disabled=not show_icon,
            ),
            dmc.Group(
                [
                    dmc.Text("Suggestions:", size="xs", c="dimmed"),
                    *[
                        dmc.Badge(
                            icon,
                            size="sm",
                            variant="light",
                            color="gray",
                            style={"cursor": "pointer"},
                            id={"type": "ex22-icon-suggestion", "node": node_id, "icon": icon},
                        )
                        for icon in suggestions[:4]
                    ],
                ],
                gap="xs",
                mb="md",
            ),
            dmc.TextInput(
                id={"type": "ex22-title-input", "node": node_id},
                label="Title",
                placeholder="Node title",
                value=default_title,
                leftSection=DashIconify(icon="mdi:format-title", width=16),
                mb="sm",
            ),
            dmc.Textarea(
                id={"type": "ex22-body-input", "node": node_id},
                label="Body Text",
                placeholder="Description text",
                value=default_body,
                autosize=True,
                minRows=2,
                maxRows=4,
            ),
        ],
        p="md",
        radius="md",
        withBorder=True,
        style={"borderLeft": f"4px solid {accent_color}"},
    )


component = dmc.Container(
    [
        dmc.Group(
            [
                dmc.Anchor(
                    dmc.Group(
                        [
                            DashIconify(icon="mdi:magnify", width=16),
                            "Search icons at iconify.design",
                        ],
                        gap="xs",
                    ),
                    href="https://icon-sets.iconify.design/",
                    target="_blank",
                ),
                dmc.Badge("Stacked = Vertical layout", color="blue", variant="light"),
                dmc.Badge("Horizontal = Two-column layout", color="green", variant="light"),
            ],
            gap="md",
            mb="lg",
        ),
        # Layout preview section
        dmc.Paper(
            [
                dmc.Text("Content Mode Examples", size="sm", fw=500, mb="xs"),
                dmc.Group(
                    [
                        dmc.Badge("Icon + Text = Full Content", color="violet", variant="outline"),
                        dmc.Badge("Icon Only = Compact", color="orange", variant="outline"),
                        dmc.Badge("Text Only = Centered", color="cyan", variant="outline"),
                    ],
                    gap="xs",
                ),
            ],
            p="sm",
            radius="md",
            bg="var(--mantine-color-default)",
            mb="md",
        ),
        dmc.Grid(
            [
                # Left panel - Node editors
                dmc.GridCol(
                    dmc.Stack(
                        [
                            create_node_editor(
                                "input-1",
                                "input",
                                "mdi:database",
                                "Data Source",
                                "PostgreSQL Database",
                                default_layout="stacked",
                                show_icon=True,
                            ),
                            create_node_editor(
                                "process-1",
                                "process",
                                "mdi:cog",
                                "Transform",
                                "Clean and normalize",
                                default_layout="horizontal",
                                show_icon=True,
                            ),
                            create_node_editor(
                                "output-1",
                                "output",
                                "mdi:chart-bar",
                                "Dashboard",
                                "Visualization",
                                default_layout="horizontal",
                                show_icon=True,
                            ),
                        ],
                        gap="md",
                    ),
                    span=4,
                ),
                # Right panel - Flow canvas
                dmc.GridCol(
                    dmc.Paper(
                        dash_flows.DashFlows(
                            id="ex22-icon-flow",
                            nodes=initial_nodes,
                            edges=initial_edges,
                            fitView=True,
                            style={"height": "480px"},
                            showControls=True,
                            showMiniMap=True,
                        ),
                        radius="md",
                        withBorder=True,
                        style={"overflow": "hidden"},
                    ),
                    span=8,
                ),
            ],
            gutter="lg",
        ),
    ],
    size="xl",
    py="md",
    px=0,
)


@callback(
    Output("ex22-icon-flow", "nodes"),
    Input({"type": "ex22-icon-input", "node": ALL}, "value"),
    Input({"type": "ex22-title-input", "node": ALL}, "value"),
    Input({"type": "ex22-body-input", "node": ALL}, "value"),
    Input({"type": "ex22-layout-toggle", "node": ALL}, "value"),
    Input({"type": "ex22-show-icon-toggle", "node": ALL}, "checked"),
    State("ex22-icon-flow", "nodes"),
    prevent_initial_call=True,
)
def update_nodes(icons, titles, bodies, layouts, show_icons, current_nodes):
    """Update nodes when form values change."""
    if not current_nodes:
        return dash.no_update

    # Map node IDs to their indices in the callback inputs
    node_mapping = {
        "input-1": 0,
        "process-1": 1,
        "output-1": 2,
    }

    # Update each node
    updated_nodes = []
    for node in current_nodes:
        node_id = node["id"]
        if node_id in node_mapping:
            idx = node_mapping[node_id]

            # Determine icon color based on node type
            icon_color = {
                "input": "white",
                "default": "white",
                "output": "white",
            }.get(node.get("type", "default"), "white")

            # Create updated node data
            updated_data = {
                **node.get("data", {}),
                "label": titles[idx] if titles[idx] else node.get("data", {}).get("label", ""),
                "body": bodies[idx] if bodies[idx] else "",
                "layout": layouts[idx] if layouts[idx] else "stacked",
                "showIcon": show_icons[idx],
            }

            # Add icon if provided and showIcon is enabled
            if icons[idx] and show_icons[idx]:
                updated_data["icon"] = DashIconify(
                    icon=icons[idx],
                    width=20,
                    color=icon_color,
                )

            updated_nodes.append({
                **node,
                "data": updated_data,
            })
        else:
            updated_nodes.append(node)

    return updated_nodes


@callback(
    Output({"type": "ex22-icon-input", "node": ALL}, "value"),
    Input({"type": "ex22-icon-suggestion", "node": ALL, "icon": ALL}, "n_clicks"),
    State({"type": "ex22-icon-input", "node": ALL}, "value"),
    prevent_initial_call=True,
)
def handle_icon_suggestion(clicks, current_values):
    """Handle clicking on icon suggestions."""
    if not ctx.triggered_id or not any(clicks):
        return dash.no_update

    # Get the clicked suggestion
    triggered = ctx.triggered_id
    clicked_node = triggered["node"]
    clicked_icon = triggered["icon"]

    # Update the corresponding input
    node_mapping = {"input-1": 0, "process-1": 1, "output-1": 2}

    result = list(current_values)
    if clicked_node in node_mapping:
        result[node_mapping[clicked_node]] = clicked_icon

    return result


@callback(
    Output({"type": "ex22-icon-input", "node": ALL}, "disabled"),
    Input({"type": "ex22-show-icon-toggle", "node": ALL}, "checked"),
)
def toggle_icon_input_disabled(show_icons):
    """Disable icon input when showIcon is toggled off."""
    return [not checked for checked in show_icons]
