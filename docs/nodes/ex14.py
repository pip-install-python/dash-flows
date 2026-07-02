"""
Embeddable twin of examples/14_dash_components_in_nodes.py for the docs page.
Rendered via `.. exec::docs.nodes.ex14`.
"""
from dash import html, dcc, Input, Output, callback
import dash_flows
import dash_mantine_components as dmc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Sample data for the detail panel charts
df = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Revenue": [12400, 15800, 14200, 18900, 21000, 19500],
    "Users": [1200, 1450, 1380, 1720, 1950, 1840],
})


# ============================================
# Node Definitions
# ============================================

nodes = [
    # Input Node - Data Source
    {
        "id": "data-source",
        "type": "input",
        "data": {"label": "Data Source", "sublabel": "API Feed"},
        "position": {"x": 50, "y": 150},
    },

    # Resizable Node - Revenue Metrics Card
    {
        "id": "revenue-card",
        "type": "resizable",
        "data": {
            "label": html.Div([
                # Header
                html.Div("Revenue", style={
                    "fontSize": "12px",
                    "color": "var(--mantine-color-dimmed)",
                    "marginBottom": "4px",
                }),
                # Main value
                html.Div("$19,500", style={
                    "fontSize": "28px",
                    "fontWeight": "bold",
                    "color": "var(--mantine-color-text)",
                }),
                # Trend indicator
                html.Div([
                    html.Span("+8.2%", style={
                        "color": "#10b981",
                        "fontWeight": "600",
                        "fontSize": "13px",
                    }),
                    html.Span(" vs last month", style={
                        "color": "var(--mantine-color-dimmed)",
                        "fontSize": "11px",
                    }),
                ], style={"marginTop": "4px"}),
                # Mini bar chart using CSS
                html.Div([
                    html.Div(style={"flex": "1", "height": "20px", "background": "#dbeafe", "borderRadius": "2px", "margin": "1px"}),
                    html.Div(style={"flex": "1", "height": "28px", "background": "#93c5fd", "borderRadius": "2px", "margin": "1px"}),
                    html.Div(style={"flex": "1", "height": "24px", "background": "#60a5fa", "borderRadius": "2px", "margin": "1px"}),
                    html.Div(style={"flex": "1", "height": "35px", "background": "#3b82f6", "borderRadius": "2px", "margin": "1px"}),
                    html.Div(style={"flex": "1", "height": "42px", "background": "#2563eb", "borderRadius": "2px", "margin": "1px"}),
                    html.Div(style={"flex": "1", "height": "38px", "background": "#1d4ed8", "borderRadius": "2px", "margin": "1px"}),
                ], style={
                    "display": "flex",
                    "alignItems": "flex-end",
                    "marginTop": "12px",
                    "height": "45px",
                }),
            ], style={
                "padding": "12px",
                "height": "100%",
                "boxSizing": "border-box",
            }),
            "handles": [
                {"type": "target", "position": "left", "id": "revenue-in"},
                {"type": "source", "position": "right", "id": "revenue-out"},
            ],
            "minWidth": 160,
            "minHeight": 140,
            "padding": 0,
        },
        "position": {"x": 250, "y": 50},
        "style": {"width": 180, "height": 160},
    },

    # Resizable Node - User Metrics Card
    {
        "id": "users-card",
        "type": "resizable",
        "data": {
            "label": html.Div([
                # Header
                html.Div("Active Users", style={
                    "fontSize": "12px",
                    "color": "var(--mantine-color-dimmed)",
                    "marginBottom": "4px",
                }),
                # Main value
                html.Div("1,840", style={
                    "fontSize": "28px",
                    "fontWeight": "bold",
                    "color": "var(--mantine-color-text)",
                }),
                # Trend indicator
                html.Div([
                    html.Span("-5.6%", style={
                        "color": "#ef4444",
                        "fontWeight": "600",
                        "fontSize": "13px",
                    }),
                    html.Span(" vs last month", style={
                        "color": "var(--mantine-color-dimmed)",
                        "fontSize": "11px",
                    }),
                ], style={"marginTop": "4px"}),
                # Progress ring simulation
                html.Div([
                    html.Div(style={
                        "width": "50px",
                        "height": "50px",
                        "borderRadius": "50%",
                        "border": "4px solid var(--mantine-color-default-border)",
                        "borderTopColor": "#8b5cf6",
                        "borderRightColor": "#8b5cf6",
                        "transform": "rotate(45deg)",
                    }),
                    html.Div("73%", style={
                        "position": "absolute",
                        "fontSize": "11px",
                        "fontWeight": "bold",
                        "color": "var(--mantine-color-dimmed)",
                    }),
                ], style={
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "marginTop": "8px",
                    "position": "relative",
                }),
            ], style={
                "padding": "12px",
                "height": "100%",
                "boxSizing": "border-box",
            }),
            "handles": [
                {"type": "target", "position": "left", "id": "users-in"},
                {"type": "source", "position": "right", "id": "users-out"},
            ],
            "minWidth": 160,
            "minHeight": 140,
            "padding": 0,
        },
        "position": {"x": 250, "y": 240},
        "style": {"width": 180, "height": 170},
    },

    # Resizable Node - Processing Status
    {
        "id": "status-card",
        "type": "resizable",
        "data": {
            "label": html.Div([
                html.Div("Pipeline Status", style={
                    "fontSize": "13px",
                    "fontWeight": "600",
                    "color": "var(--mantine-color-text)",
                    "marginBottom": "12px",
                }),
                # Stage 1 - Complete
                html.Div([
                    html.Div([
                        html.Span("Extract", style={"fontSize": "11px", "color": "var(--mantine-color-text)"}),
                        html.Span("Done", style={"fontSize": "10px", "color": "#10b981", "marginLeft": "auto"}),
                    ], style={"display": "flex", "marginBottom": "4px"}),
                    html.Div([
                        html.Div(style={
                            "width": "100%",
                            "height": "6px",
                            "background": "#10b981",
                            "borderRadius": "3px",
                        })
                    ], style={"background": "var(--mantine-color-default-border)", "borderRadius": "3px"}),
                ], style={"marginBottom": "10px"}),
                # Stage 2 - In Progress
                html.Div([
                    html.Div([
                        html.Span("Transform", style={"fontSize": "11px", "color": "var(--mantine-color-text)"}),
                        html.Span("75%", style={"fontSize": "10px", "color": "#3b82f6", "marginLeft": "auto"}),
                    ], style={"display": "flex", "marginBottom": "4px"}),
                    html.Div([
                        html.Div(style={
                            "width": "75%",
                            "height": "6px",
                            "background": "#3b82f6",
                            "borderRadius": "3px",
                        })
                    ], style={"background": "var(--mantine-color-default-border)", "borderRadius": "3px"}),
                ], style={"marginBottom": "10px"}),
                # Stage 3 - Pending
                html.Div([
                    html.Div([
                        html.Span("Load", style={"fontSize": "11px", "color": "var(--mantine-color-text)"}),
                        html.Span("Pending", style={"fontSize": "10px", "color": "var(--mantine-color-dimmed)", "marginLeft": "auto"}),
                    ], style={"display": "flex", "marginBottom": "4px"}),
                    html.Div([
                        html.Div(style={
                            "width": "0%",
                            "height": "6px",
                            "background": "#9ca3af",
                            "borderRadius": "3px",
                        })
                    ], style={"background": "var(--mantine-color-default-border)", "borderRadius": "3px"}),
                ]),
            ], style={
                "padding": "12px",
                "height": "100%",
                "boxSizing": "border-box",
            }),
            "handles": [
                {"type": "target", "position": "top", "id": "status-in-1"},
                {"type": "target", "position": "left", "id": "status-in-2"},
                {"type": "source", "position": "right", "id": "status-out"},
            ],
            "minWidth": 150,
            "minHeight": 150,
            "padding": 0,
        },
        "position": {"x": 500, "y": 130},
        "style": {"width": 170, "height": 175},
    },

    # Output Node - Dashboard
    {
        "id": "dashboard",
        "type": "output",
        "data": {"label": "Dashboard", "sublabel": "Final Output"},
        "position": {"x": 730, "y": 175},
    },
]

# Edge connections
edges = [
    {"id": "e1", "source": "data-source", "target": "revenue-card", "targetHandle": "revenue-in"},
    {"id": "e2", "source": "data-source", "target": "users-card", "targetHandle": "users-in"},
    {"id": "e3", "source": "revenue-card", "target": "status-card", "sourceHandle": "revenue-out", "targetHandle": "status-in-1"},
    {"id": "e4", "source": "users-card", "target": "status-card", "sourceHandle": "users-out", "targetHandle": "status-in-2"},
    {"id": "e5", "source": "status-card", "target": "dashboard", "sourceHandle": "status-out"},
]


# ============================================
# Chart Functions for Detail Panel
# ============================================

def create_revenue_chart():
    """Full Plotly chart shown in detail panel."""
    fig = px.bar(
        df, x="Month", y="Revenue",
        color_discrete_sequence=["#3b82f6"]
    )
    fig.update_layout(
        margin=dict(l=40, r=20, t=40, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title=dict(text="Monthly Revenue", font=dict(size=14)),
        height=280,
    )
    return fig


def create_users_chart():
    """Full Plotly chart shown in detail panel."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Month"],
        y=df["Users"],
        mode="lines+markers",
        line=dict(color="#8b5cf6", width=3),
        marker=dict(size=8),
        fill="tozeroy",
        fillcolor="rgba(139, 92, 246, 0.1)",
    ))
    fig.update_layout(
        margin=dict(l=40, r=20, t=40, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title=dict(text="User Growth", font=dict(size=14)),
        height=280,
    )
    return fig


# ============================================
# Component Layout
# ============================================

component = dmc.Grid([
    # Flow canvas
    dmc.GridCol([
        dash_flows.DashFlows(
            id="ex14-metrics-flow",
            nodes=nodes,
            edges=edges,
            style={
                "height": "480px",
                "border": "1px solid var(--mantine-color-default-border)",
                "borderRadius": "8px",
            },
            fitView=True,
            showControls=True,
            showMiniMap=False,
            nodesDraggable=True,
            elementsSelectable=True,
        ),
    ], span=8),

    # Detail panel
    dmc.GridCol([
        dmc.Paper([
            dmc.Text("Node Details", fw=600, size="sm", mb="sm"),
            html.Div(id="ex14-node-info", children=[
                dmc.Text("Click a node to see details", c="dimmed", size="sm"),
            ]),
        ], p="md", withBorder=True, mb="md"),

        dmc.Paper([
            dmc.Text("Chart Preview", fw=600, size="sm", mb="sm"),
            html.Div(id="ex14-chart-panel", children=[
                dmc.Text("Select a metric card to see the full chart", c="dimmed", size="sm"),
            ]),
        ], p="md", withBorder=True, style={"minHeight": "320px"}),
    ], span=4),
])


# ============================================
# Callbacks
# ============================================

@callback(
    Output("ex14-node-info", "children"),
    Output("ex14-chart-panel", "children"),
    Input("ex14-metrics-flow", "clickedNode"),
    prevent_initial_call=True,
)
def show_node_details(clicked_node):
    """Show node info and corresponding chart when a node is clicked."""
    if not clicked_node:
        return (
            dmc.Text("No node selected", c="dimmed", size="sm"),
            dmc.Text("Click a metric card", c="dimmed", size="sm"),
        )

    node_id = clicked_node.get("id", "Unknown")
    node_type = clicked_node.get("type", "unknown")
    position = clicked_node.get("position", {})

    # Node info display
    info = dmc.Stack([
        dmc.Group([
            dmc.Text("ID:", size="sm", fw=500),
            dmc.Badge(node_id, variant="light", color="blue"),
        ], gap="xs"),
        dmc.Group([
            dmc.Text("Type:", size="sm", fw=500),
            dmc.Badge(node_type, variant="light", color="gray"),
        ], gap="xs"),
        dmc.Group([
            dmc.Text("Position:", size="sm", fw=500),
            dmc.Code(f"({position.get('x', 0):.0f}, {position.get('y', 0):.0f})"),
        ], gap="xs"),
    ], gap="xs")

    # Chart based on selected node
    if node_id == "revenue-card":
        chart = dcc.Graph(
            figure=create_revenue_chart(),
            config={"displayModeBar": False},
        )
    elif node_id == "users-card":
        chart = dcc.Graph(
            figure=create_users_chart(),
            config={"displayModeBar": False},
        )
    elif node_id == "status-card":
        chart = dmc.Stack([
            dmc.Text("ETL Pipeline Status", fw=600, size="sm"),
            dmc.Progress(value=100, color="green", size="lg", mb="xs"),
            dmc.Text("Extract: Complete", size="xs", c="dimmed"),
            dmc.Progress(value=75, color="blue", size="lg", mb="xs"),
            dmc.Text("Transform: 75%", size="xs", c="dimmed"),
            dmc.Progress(value=0, color="gray", size="lg", mb="xs"),
            dmc.Text("Load: Pending", size="xs", c="dimmed"),
        ], gap="sm")
    else:
        chart = dmc.Text(f"No chart for: {node_id}", c="dimmed", size="sm")

    return info, chart
