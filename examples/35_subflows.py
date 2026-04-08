"""
Example 35: Sub-flows (Collapsible Groups)
===========================================
Demonstrates expandable/collapsible group nodes.

Architecture pattern for React Flow sub-flows:
- Edges that cross group boundaries connect to the GROUP node, not to children.
- Edges inside a group connect child-to-child (these are intra-group and safe).
- When a group collapses: children + their internal edges are hidden; the group
  shrinks to a compact box; external edges remain connected at the group level.

Double-click a group or use the buttons to toggle collapse/expand.
"""

import dash
from dash import html, callback, Input, Output, State
import dash_flows

app = dash.Dash(__name__)

# ── Initial graph ─────────────────────────────────────────────────────────────
#
#   source ──► [group-ingest: parse ──► validate] ──► [group-process: transform ──► enrich] ──► sink
#
# External edges connect to GROUP nodes (not directly to children).
# Internal edges connect children within the same group (safe pattern).

initial_nodes = [
    # External nodes
    {
        "id": "source",
        "type": "input",
        "data": {"label": "Data Source"},
        "position": {"x": 50, "y": 190},
    },

    # ── Ingestion group ────────────────────────────────────────────────────────
    {
        "id": "group-ingest",
        "type": "group",
        "data": {
            "label": "Ingestion Pipeline",
            "collapsedWidth": 200,
            "collapsedHeight": 52,
        },
        "position": {"x": 260, "y": 60},
        "style": {"width": 280, "height": 270},
    },
    {
        "id": "parse",
        "type": "default",
        "data": {"label": "Parse", "sublabel": "Deserialize"},
        "position": {"x": 50, "y": 55},
        "parentId": "group-ingest",
        "extent": "parent",
    },
    {
        "id": "validate",
        "type": "default",
        "data": {"label": "Validate", "sublabel": "Schema check"},
        "position": {"x": 50, "y": 170},
        "parentId": "group-ingest",
        "extent": "parent",
    },

    # ── Processing group ───────────────────────────────────────────────────────
    {
        "id": "group-process",
        "type": "group",
        "data": {
            "label": "Processing",
            "collapsedWidth": 200,
            "collapsedHeight": 52,
        },
        "position": {"x": 680, "y": 60},
        "style": {"width": 280, "height": 270},
    },
    {
        "id": "transform",
        "type": "default",
        "data": {"label": "Transform", "sublabel": "Normalize"},
        "position": {"x": 50, "y": 55},
        "parentId": "group-process",
        "extent": "parent",
    },
    {
        "id": "enrich",
        "type": "default",
        "data": {"label": "Enrich", "sublabel": "Add metadata"},
        "position": {"x": 50, "y": 170},
        "parentId": "group-process",
        "extent": "parent",
    },

    # External nodes
    {
        "id": "sink",
        "type": "output",
        "data": {"label": "Data Sink"},
        "position": {"x": 1100, "y": 190},
    },
]

initial_edges = [
    # External → Group  (NOT external → child inside group — avoids handle timing issues)
    {"id": "e-src-ingest",    "source": "source",        "target": "group-ingest",  "animated": True},

    # Intra-group edges (child → child within the SAME group — always safe)
    {"id": "e-parse-validate",    "source": "parse",     "target": "validate"},
    {"id": "e-transform-enrich",  "source": "transform", "target": "enrich"},

    # Group → Group  (cross-group at group level — safe)
    {"id": "e-ingest-process", "source": "group-ingest", "target": "group-process", "animated": True},

    # Group → External
    {"id": "e-process-sink",   "source": "group-process", "target": "sink",         "animated": True},
]

# ── Layout ────────────────────────────────────────────────────────────────────
btn_style = {
    "padding": "8px 16px",
    "border": "1px solid #ddd",
    "borderRadius": "6px",
    "background": "#fff",
    "cursor": "pointer",
    "fontSize": "13px",
}

app.layout = html.Div([
    html.H2("Sub-flows — Collapsible Groups"),

    html.Div([
        html.Strong("Pattern: ", style={"fontSize": "13px"}),
        html.Span(
            "External edges connect to the group container. "
            "Internal edges connect children within the same group. "
            "Collapsing hides children and shrinks the group; external connections stay intact.",
            style={"fontSize": "13px", "color": "#555"},
        ),
    ], style={
        "background": "#f0f7ff", "border": "1px solid #bfdbfe",
        "borderRadius": "8px", "padding": "10px 14px", "marginBottom": "10px",
    }),

    html.Div([
        html.Button("Toggle Ingestion",  id="btn-toggle-ingest",  style=btn_style),
        html.Button("Toggle Processing", id="btn-toggle-process", style=btn_style),
        html.Button("Expand All",        id="btn-expand-all",     style=btn_style),
        html.Span(id="collapse-info", style={
            "padding": "8px 16px", "background": "#f0f0f0",
            "borderRadius": "6px", "fontSize": "12px", "color": "#666",
        }),
    ], style={"display": "flex", "gap": "8px", "alignItems": "center", "marginBottom": "10px"}),

    dash_flows.DashFlows(
        id="subflow",
        nodes=initial_nodes,
        edges=initial_edges,
        fitView=True,
        showControls=True,
        showMiniMap=True,
        showBackground=True,
        style={"height": "520px"},
    ),
], style={"padding": "20px"})


# ── Callbacks ─────────────────────────────────────────────────────────────────

@callback(
    Output("subflow", "toggleCollapseNode"),
    Input("btn-toggle-ingest",  "n_clicks"),
    Input("btn-toggle-process", "n_clicks"),
    Input("subflow",            "doubleClickedNode"),
    prevent_initial_call=True,
)
def toggle_group(ingest, process, dbl_clicked):
    from dash import ctx
    if ctx.triggered_id == "btn-toggle-ingest":
        return "group-ingest"
    if ctx.triggered_id == "btn-toggle-process":
        return "group-process"
    if ctx.triggered_id == "subflow" and dbl_clicked:
        node_id = dbl_clicked.get("id", "")
        if node_id.startswith("group-"):
            return node_id
    return dash.no_update


@callback(
    Output("subflow", "nodes"),
    Input("btn-expand-all", "n_clicks"),
    State("subflow", "nodes"),
    prevent_initial_call=True,
)
def expand_all(n_clicks, nodes):
    """Force-expand all groups by clearing collapsed state."""
    if not nodes:
        return dash.no_update
    updated = []
    for n in nodes:
        if n.get("type") == "group" and n.get("data", {}).get("collapsed"):
            n = dict(n)
            n["data"] = {**n["data"], "collapsed": False}
            # Restore original size from initial_nodes
            orig = next((x for x in initial_nodes if x["id"] == n["id"]), None)
            if orig and orig.get("style"):
                n["style"] = orig["style"]
            n["hidden"] = False
        elif n.get("hidden"):
            n = dict(n)
            n["hidden"] = False
        updated.append(n)
    return updated


@callback(
    Output("collapse-info", "children"),
    Input("subflow", "collapsedGroups"),
)
def show_collapsed(groups):
    if not groups:
        return "All groups expanded"
    return f"Collapsed: {', '.join(groups)}"


if __name__ == "__main__":
    app.run(debug=True, port=8035)