"""
Example 32: Undo/Redo System
=============================
Demonstrates the undo/redo history system. Move nodes, create connections,
delete elements — then undo and redo your changes.

Features demonstrated:
- Node movement undo/redo (drag a node, then undo)
- Node/edge deletion undo/redo (select + Delete key, or use button)
- Connection creation undo (draw an edge between nodes)
- History counter shows pending undo/redo steps

Uses experimental_useOnNodesChangeMiddleware and
experimental_useOnEdgesChangeMiddleware from React Flow 12.10.1.
"""

import dash
from dash import html, dcc, callback, Input, Output, State
import dash_flows

app = dash.Dash(__name__)

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
    "border": "1px solid #ddd",
    "borderRadius": "6px",
    "cursor": "pointer",
    "fontSize": "13px",
    "fontWeight": "500",
    "minWidth": "80px",
}

app.layout = html.Div([
    html.H2("Undo/Redo System"),

    # Instruction panel
    html.Div([
        html.Div([
            html.Strong("Try these actions:"),
            html.Ul([
                html.Li("Drag a node to a new position → then Undo"),
                html.Li("Select a node (click) → press Delete or Backspace → then Undo"),
                html.Li("Draw a new edge by dragging from a handle → then Undo"),
                html.Li("Use the Delete Selected button below to remove selected nodes"),
            ], style={"margin": "6px 0 0 0", "paddingLeft": "18px", "fontSize": "13px", "color": "#555"}),
        ]),
    ], style={
        "background": "#f0f7ff",
        "border": "1px solid #bfdbfe",
        "borderRadius": "8px",
        "padding": "10px 14px",
        "marginBottom": "10px",
        "fontSize": "13px",
    }),

    # Controls row
    html.Div([
        html.Button(
            "⟲ Undo", id="btn-undo",
            style={**btn_style, "background": "#fee2e2", "borderColor": "#fca5a5"},
            disabled=True,
        ),
        html.Button(
            "⟳ Redo", id="btn-redo",
            style={**btn_style, "background": "#dbeafe", "borderColor": "#93c5fd"},
            disabled=True,
        ),
        html.Button(
            "🗑 Delete Selected", id="btn-delete",
            style={**btn_style, "background": "#fef9c3", "borderColor": "#fde047"},
        ),
        html.Span(id="history-info", style={
            "padding": "8px 14px",
            "background": "#f0f0f0",
            "borderRadius": "6px",
            "fontSize": "12px",
            "color": "#555",
            "marginLeft": "4px",
        }),
    ], style={"display": "flex", "gap": "8px", "alignItems": "center", "marginBottom": "10px"}),

    # Store to hold selected node IDs for delete action
    dcc.Store(id="selected-ids-store"),

    dash_flows.DashFlows(
        id="undo-redo-flow",
        nodes=initial_nodes,
        edges=initial_edges,
        fitView=True,
        enableUndoRedo=True,
        undoRedoMaxHistory=50,
        showControls=True,
        showMiniMap=True,
        showBackground=True,
        style={"height": "500px"},
    ),

    html.Div(id="action-log", style={
        "marginTop": "10px",
        "padding": "8px 12px",
        "background": "#fafafa",
        "border": "1px solid #e5e7eb",
        "borderRadius": "6px",
        "fontSize": "12px",
        "color": "#6b7280",
        "minHeight": "32px",
    }),
], style={"padding": "20px"})


@callback(
    Output("undo-redo-flow", "undoRedoAction"),
    Input("btn-undo", "n_clicks"),
    Input("btn-redo", "n_clicks"),
    prevent_initial_call=True,
)
def handle_undo_redo(undo_clicks, redo_clicks):
    from dash import ctx
    if ctx.triggered_id == "btn-undo":
        return {"action": "undo"}
    elif ctx.triggered_id == "btn-redo":
        return {"action": "redo"}
    return dash.no_update


@callback(
    Output("btn-undo", "disabled"),
    Output("btn-redo", "disabled"),
    Output("history-info", "children"),
    Input("undo-redo-flow", "undoRedoState"),
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
    Output("selected-ids-store", "data"),
    Input("undo-redo-flow", "selectedNodes"),
    Input("undo-redo-flow", "selectedEdges"),
)
def track_selected(sel_nodes, sel_edges):
    # selectedNodes / selectedEdges are already arrays of string IDs
    return {"nodes": sel_nodes or [], "edges": sel_edges or []}


@callback(
    Output("undo-redo-flow", "deleteElementsAction"),
    Output("action-log", "children"),
    Input("btn-delete", "n_clicks"),
    State("selected-ids-store", "data"),
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


if __name__ == "__main__":
    app.run(debug=True, port=8032)