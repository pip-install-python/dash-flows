"""
Embeddable twin of examples/32_undo_redo.py for the docs page.
Rendered via `.. exec::docs.advanced.ex32`.
"""
import dash
from dash import html, dcc, callback, Input, Output, State, ctx
import dash_flows

initial_nodes = [
    {"id": "a", "type": "input",   "data": {"label": "Node A", "sublabel": "Source"},   "position": {"x": 50,  "y": 150}},
    {"id": "b", "type": "default", "data": {"label": "Node B", "sublabel": "Process 1"}, "position": {"x": 280, "y": 50}},
    {"id": "c", "type": "default", "data": {"label": "Node C", "sublabel": "Process 2"}, "position": {"x": 280, "y": 250}},
    {"id": "d", "type": "output",  "data": {"label": "Node D", "sublabel": "Output"},   "position": {"x": 510, "y": 150}},
]

initial_edges = [
    {"id": "e-ab", "source": "a", "target": "b"},
    {"id": "e-ac", "source": "a", "target": "c"},
    {"id": "e-bd", "source": "b", "target": "d"},
]

btn_style = {
    "padding": "8px 16px",
    "border": "1px solid var(--mantine-color-default-border)",
    "borderRadius": "6px",
    "cursor": "pointer",
    "fontSize": "13px",
    "fontWeight": "500",
    "minWidth": "80px",
}

component = html.Div([
    # Instruction panel
    html.Div([
        html.Div([
            html.Strong("Try these actions:"),
            html.Ul([
                html.Li("Drag a node to a new position → then Undo"),
                html.Li("Select a node (click) → press Delete or Backspace → then Undo"),
                html.Li("Draw a new edge by dragging from a handle → then Undo"),
                html.Li("Use the Delete Selected button below to remove selected nodes"),
            ], style={"margin": "6px 0 0 0", "paddingLeft": "18px", "fontSize": "13px", "color": "var(--mantine-color-dimmed)"}),
        ]),
    ], style={
        "background": "var(--mantine-color-default)",
        "border": "1px solid var(--mantine-color-default-border)",
        "borderRadius": "8px",
        "padding": "10px 14px",
        "marginBottom": "10px",
        "fontSize": "13px",
    }),

    # Controls row
    html.Div([
        html.Button(
            "⟲ Undo", id="ex32-btn-undo",
            style={**btn_style, "background": "var(--mantine-color-red-light)", "borderColor": "var(--mantine-color-red-light-color)"},
            disabled=True,
        ),
        html.Button(
            "⟳ Redo", id="ex32-btn-redo",
            style={**btn_style, "background": "var(--mantine-color-blue-light)", "borderColor": "var(--mantine-color-blue-light-color)"},
            disabled=True,
        ),
        html.Button(
            "🗑 Delete Selected", id="ex32-btn-delete",
            style={**btn_style, "background": "var(--mantine-color-yellow-light)", "borderColor": "var(--mantine-color-yellow-light-color)"},
        ),
        html.Span(id="ex32-history-info", style={
            "padding": "8px 14px",
            "background": "var(--mantine-color-default)",
            "borderRadius": "6px",
            "fontSize": "12px",
            "color": "var(--mantine-color-dimmed)",
            "marginLeft": "4px",
        }),
    ], style={"display": "flex", "gap": "8px", "alignItems": "center", "marginBottom": "10px"}),

    # Store to hold selected node IDs for delete action
    dcc.Store(id="ex32-selected-ids-store"),

    dash_flows.DashFlows(
        id="ex32-undo-redo-flow",
        nodes=initial_nodes,
        edges=initial_edges,
        fitView=True,
        enableUndoRedo=True,
        undoRedoMaxHistory=50,
        showControls=True,
        showMiniMap=True,
        showBackground=True,
        style={
            "height": "460px",
            "border": "1px solid var(--mantine-color-default-border)",
            "borderRadius": "8px",
        },
    ),

    html.Div(id="ex32-action-log", style={
        "marginTop": "10px",
        "padding": "8px 12px",
        "background": "var(--mantine-color-default)",
        "border": "1px solid var(--mantine-color-default-border)",
        "borderRadius": "6px",
        "fontSize": "12px",
        "color": "var(--mantine-color-dimmed)",
        "minHeight": "32px",
    }),
])


@callback(
    Output("ex32-undo-redo-flow", "undoRedoAction"),
    Input("ex32-btn-undo", "n_clicks"),
    Input("ex32-btn-redo", "n_clicks"),
    prevent_initial_call=True,
)
def handle_undo_redo(undo_clicks, redo_clicks):
    if ctx.triggered_id == "ex32-btn-undo":
        return {"action": "undo"}
    elif ctx.triggered_id == "ex32-btn-redo":
        return {"action": "redo"}
    return dash.no_update


@callback(
    Output("ex32-btn-undo", "disabled"),
    Output("ex32-btn-redo", "disabled"),
    Output("ex32-history-info", "children"),
    Input("ex32-undo-redo-flow", "undoRedoState"),
)
def update_buttons(state):
    if not state:
        return True, True, "History: 0 undo / 0 redo"
    undo_count = state.get("undoCount", 0)
    redo_count = state.get("redoCount", 0)
    label = f"History: {undo_count} undo / {redo_count} redo"
    return (
        not state.get("canUndo", False),
        not state.get("canRedo", False),
        label,
    )


@callback(
    Output("ex32-selected-ids-store", "data"),
    Input("ex32-undo-redo-flow", "selectedNodes"),
    Input("ex32-undo-redo-flow", "selectedEdges"),
)
def track_selected(sel_nodes, sel_edges):
    # selectedNodes / selectedEdges are already arrays of string IDs
    return {"nodes": sel_nodes or [], "edges": sel_edges or []}


@callback(
    Output("ex32-undo-redo-flow", "deleteElementsAction"),
    Output("ex32-action-log", "children"),
    Input("ex32-btn-delete", "n_clicks"),
    State("ex32-selected-ids-store", "data"),
    prevent_initial_call=True,
)
def delete_selected(n_clicks, selected):
    if not selected:
        return dash.no_update, "Nothing selected to delete."

    node_ids = selected.get("nodes", [])
    edge_ids = selected.get("edges", [])

    if not node_ids and not edge_ids:
        return dash.no_update, "Nothing selected to delete."

    parts = []
    if node_ids:
        parts.append(f"{len(node_ids)} node(s)")
    if edge_ids:
        parts.append(f"{len(edge_ids)} edge(s)")
    msg = f"Deleted {' and '.join(parts)}. Press ⟲ Undo to restore."

    # Route through deleteElementsAction so React Flow's normal deletion
    # flow fires — the undo/redo middleware can then capture the snapshot.
    return {"nodeIds": node_ids, "edgeIds": edge_ids}, msg
