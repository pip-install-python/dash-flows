"""
Example 29: Accessibility / ARIA Pass-through
==============================================
Demonstrates ARIA label customization, keyboard navigation, and focus
management for screen-reader and keyboard-only users.

Key features:
- ariaLabelConfig: custom labels for the diagram, minimap, and controls
- Per-node / per-edge ariaLabel: individual element descriptions
- nodesFocusable / edgesFocusable: Tab key navigates between elements
- disableKeyboardA11y=False: arrow-key panning and keyboard shortcuts active
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_flows

app = dash.Dash(__name__)

nodes = [
    {
        "id": "start",
        "type": "input",
        "data": {"label": "Start", "sublabel": "Entry point"},
        "position": {"x": 50, "y": 120},
        "ariaLabel": "Start process node — entry point of the workflow",
    },
    {
        "id": "validate",
        "type": "default",
        "data": {"label": "Validate", "sublabel": "Check data"},
        "position": {"x": 280, "y": 50},
        "ariaLabel": "Validation node — checks input data for correctness",
    },
    {
        "id": "process",
        "type": "default",
        "data": {"label": "Process", "sublabel": "Transform"},
        "position": {"x": 280, "y": 200},
        "ariaLabel": "Processing node — transforms validated data",
    },
    {
        "id": "end",
        "type": "output",
        "data": {"label": "Complete", "sublabel": "Output"},
        "position": {"x": 510, "y": 120},
        "ariaLabel": "Completion node — final output of the workflow",
    },
]

edges = [
    {"id": "e1", "source": "start",    "target": "validate", "ariaLabel": "Flow from start to validation"},
    {"id": "e2", "source": "start",    "target": "process",  "ariaLabel": "Flow from start to processing"},
    {"id": "e3", "source": "validate", "target": "end",      "ariaLabel": "Flow from validation to completion"},
    {"id": "e4", "source": "process",  "target": "end",      "ariaLabel": "Flow from processing to completion"},
]

aria_config = {
    "rfDiagram": "Interactive workflow diagram with 4 nodes and 4 connections",
    "miniMap":   "Minimap navigation — overview of the workflow diagram",
    "controls":  "Zoom and pan controls for the workflow diagram",
}

# Keyboard shortcut reference table
shortcuts = [
    ("Tab / Shift+Tab",  "Move focus between nodes and edges"),
    ("Enter / Space",    "Select the focused element"),
    ("Escape",           "Clear selection / close any overlay"),
    ("Arrow keys",       "Pan the viewport (when focus is on the canvas)"),
    ("+ / −",            "Zoom in / zoom out"),
    ("Delete / Backspace","Delete selected node or edge"),
]

app.layout = html.Div([
    html.H2("Accessibility / ARIA Labels"),
    html.P(
        "Tab through nodes and edges using the keyboard. "
        "Each element has an ARIA label that screen readers will announce. "
        "Inspect the DOM to see all applied aria-* attributes.",
        style={"color": "#666", "marginBottom": "12px"},
    ),

    # Keyboard shortcut reference
    html.Details([
        html.Summary("⌨  Keyboard shortcuts (click to expand)",
                     style={"cursor": "pointer", "fontWeight": "500", "fontSize": "13px", "color": "#374151"}),
        html.Table([
            html.Tbody([
                html.Tr([
                    html.Td(k, style={"padding": "3px 10px 3px 0", "fontFamily": "monospace",
                                      "fontSize": "12px", "whiteSpace": "nowrap", "color": "#1d4ed8"}),
                    html.Td(v, style={"padding": "3px 0", "fontSize": "12px", "color": "#374151"}),
                ])
                for k, v in shortcuts
            ]),
        ], style={"borderCollapse": "collapse", "marginTop": "6px"}),
    ], style={
        "background": "#f0f7ff", "border": "1px solid #bfdbfe",
        "borderRadius": "8px", "padding": "10px 14px", "marginBottom": "12px",
    }),

    dash_flows.DashFlows(
        id="accessible-flow",
        nodes=nodes,
        edges=edges,
        ariaLabelConfig=aria_config,
        fitView=True,
        showControls=True,
        showMiniMap=True,
        showBackground=True,
        disableKeyboardA11y=False,
        nodesFocusable=True,
        edgesFocusable=True,
        style={"height": "420px"},
    ),

    # Live info panel
    html.Div(id="a11y-info", style={
        "marginTop": "12px", "padding": "12px 14px",
        "background": "#f9fafb", "border": "1px solid #e5e7eb",
        "borderRadius": "8px", "minHeight": "56px",
    }),
], style={"padding": "20px"})


@callback(
    Output("a11y-info", "children"),
    Input("accessible-flow", "clickedNode"),
    Input("accessible-flow", "clickedEdge"),
    prevent_initial_call=True,
)
def show_element_info(clicked_node, clicked_edge):
    from dash import ctx
    if ctx.triggered_id == "accessible-flow" and clicked_node:
        nid = clicked_node["id"]
        label = clicked_node["data"].get("label", nid)
        # Find the matching ariaLabel
        aria = next((n["ariaLabel"] for n in nodes if n["id"] == nid), "No ARIA label set")
        return html.Div([
            html.Strong(f"Node clicked: {label}"),
            html.Br(),
            html.Span(f"ARIA label: \"{aria}\"",
                      style={"fontSize": "12px", "color": "#6b7280", "fontStyle": "italic"}),
            html.Br(),
            html.Span("Tip: Tab to next node, Delete/Backspace to remove selection",
                      style={"fontSize": "11px", "color": "#9ca3af"}),
        ])
    if ctx.triggered_id == "accessible-flow" and clicked_edge:
        eid = clicked_edge["id"]
        aria = next((e["ariaLabel"] for e in edges if e["id"] == eid), "No ARIA label set")
        return html.Div([
            html.Strong(f"Edge clicked: {eid}"),
            html.Br(),
            html.Span(f"ARIA label: \"{aria}\"",
                      style={"fontSize": "12px", "color": "#6b7280", "fontStyle": "italic"}),
        ])
    return html.Span("Click a node or edge to see its ARIA label.",
                     style={"color": "#9ca3af", "fontSize": "13px"})


if __name__ == "__main__":
    app.run(debug=True, port=8029)