"""
Example 34: ViewportPortal — Floating Annotations
===================================================
Demonstrates floating annotations rendered at specific flow coordinates
via ViewportPortal. Overlays move with pan/zoom.

Features:
- Add / remove annotations
- Select an annotation from the list and edit its x, y position and content
- Changes update immediately in the flow
"""

import dash
from dash import html, dcc, callback, Input, Output, State
import dash_flows

app = dash.Dash(__name__)

nodes = [
    {"id": "server", "type": "default", "data": {"label": "API Server",  "sublabel": "Port 8080"},  "position": {"x": 100, "y": 100}},
    {"id": "db",     "type": "default", "data": {"label": "Database",    "sublabel": "PostgreSQL"}, "position": {"x": 400, "y": 100}},
    {"id": "cache",  "type": "default", "data": {"label": "Cache",       "sublabel": "Redis"},      "position": {"x": 400, "y": 280}},
    {"id": "client", "type": "input",   "data": {"label": "Client App"},                            "position": {"x": -150, "y": 100}},
    {"id": "cdn",    "type": "output",  "data": {"label": "CDN"},                                   "position": {"x": 700, "y": 100}},
]

edges = [
    {"id": "e1", "source": "client", "target": "server"},
    {"id": "e2", "source": "server", "target": "db"},
    {"id": "e3", "source": "server", "target": "cache"},
    {"id": "e4", "source": "db",     "target": "cdn"},
]

initial_overlays = [
    {
        "x": -150, "y": 58,
        "content": "🌐 External Traffic",
        "style": {
            "background": "rgba(59,130,246,0.1)", "border": "1px dashed rgba(59,130,246,0.4)",
            "padding": "4px 10px", "borderRadius": "6px",
            "fontSize": "11px", "color": "#3b82f6", "fontWeight": "600", "whiteSpace": "nowrap",
        },
    },
    {
        "x": 200, "y": 68,
        "content": "← REST API →",
        "style": {
            "fontSize": "10px", "color": "#888", "fontStyle": "italic", "whiteSpace": "nowrap",
        },
    },
    {
        "x": 380, "y": 200,
        "content": "⚡ Hot path",
        "style": {
            "background": "rgba(245,158,11,0.15)", "border": "1px solid rgba(245,158,11,0.3)",
            "padding": "3px 8px", "borderRadius": "4px",
            "fontSize": "10px", "color": "#d97706", "fontWeight": "500", "whiteSpace": "nowrap",
        },
    },
    {
        "x": 100, "y": -2,
        "content": "── Internal Network ──────────────────────",
        "style": {
            "fontSize": "10px", "color": "#aaa", "letterSpacing": "1px", "whiteSpace": "nowrap",
        },
    },
]

def _build_options(overlays):
    return [
        {"label": f"[{i}] {o['content'][:28]}{'…' if len(o['content']) > 28 else ''}",
         "value": i}
        for i, o in enumerate(overlays)
    ]


# Shared button style
_btn = {
    "padding": "7px 14px", "border": "1px solid #ddd",
    "borderRadius": "6px", "background": "#fff", "cursor": "pointer", "fontSize": "13px",
}

app.layout = html.Div([
    html.H2("ViewportPortal — Floating Annotations"),
    html.P(
        "Annotations are anchored to flow coordinates and move with pan/zoom. "
        "Select one from the list below to edit its position or content.",
        style={"color": "#666"},
    ),

    # Top controls
    html.Div([
        html.Button("＋ Add Annotation", id="btn-add-overlay",   style=_btn),
        html.Button("✕ Clear All",        id="btn-clear-overlays", style=_btn),
    ], style={"display": "flex", "gap": "8px", "marginBottom": "10px"}),

    # Flow
    dash_flows.DashFlows(
        id="portal-flow",
        nodes=nodes,
        edges=edges,
        viewportOverlays=initial_overlays,
        fitView=True,
        showControls=True,
        showMiniMap=True,
        showBackground=True,
        smartHandles=True,
        style={"height": "460px"},
    ),

    # Editor panel
    html.Div([
        html.H4("Edit Annotations", style={"margin": "0 0 10px 0", "fontSize": "14px"}),
        html.Div(style={"display": "flex", "gap": "16px", "alignItems": "flex-start"}, children=[

            # Annotation list (left side)
            html.Div([
                html.Div("Select:", style={"fontSize": "12px", "color": "#888", "marginBottom": "4px"}),
                dcc.RadioItems(
                    id="annotation-selector",
                    options=_build_options(initial_overlays),
                    value=None,
                    labelStyle={"display": "block", "fontSize": "13px", "padding": "3px 0", "cursor": "pointer"},
                ),
            ], style={"minWidth": "220px"}),

            # Edit form (right side)
            html.Div(id="edit-form", style={"flex": "1"}, children=[
                html.P("Select an annotation to edit it.", style={"color": "#aaa", "fontSize": "13px"}),
            ]),
        ]),
    ], style={
        "marginTop": "14px", "padding": "14px",
        "border": "1px solid #e5e7eb", "borderRadius": "8px",
        "background": "#fafafa",
    }),

    # Hidden stores
    dcc.Store(id="overlays-store", data=initial_overlays),
], style={"padding": "20px"})


# ── Build / update the annotation list & sync overlay store ──────────────────

@callback(
    Output("portal-flow", "viewportOverlays"),
    Output("overlays-store", "data"),
    Output("annotation-selector", "options"),
    Input("btn-add-overlay",   "n_clicks"),
    Input("btn-clear-overlays","n_clicks"),
    State("overlays-store", "data"),
    prevent_initial_call=True,
)
def add_or_clear(add_clicks, clear_clicks, current):
    from dash import ctx
    import random

    if ctx.triggered_id == "btn-clear-overlays":
        return [], [], []

    current = current or []
    idx = len(current) + 1
    new_overlay = {
        "x": random.randint(-100, 500),
        "y": random.randint(-50, 320),
        "content": f"📌 Note #{idx}",
        "style": {
            "background": "rgba(139,92,246,0.1)", "border": "1px solid rgba(139,92,246,0.3)",
            "padding": "4px 10px", "borderRadius": "6px",
            "fontSize": "11px", "color": "#7c3aed", "fontWeight": "500", "whiteSpace": "nowrap",
        },
    }
    updated = current + [new_overlay]
    opts = _build_options(updated)
    return updated, updated, opts


# ── Populate the edit form when an annotation is selected ────────────────────

@callback(
    Output("edit-form", "children"),
    Input("annotation-selector", "value"),
    State("overlays-store", "data"),
)
def show_edit_form(selected_idx, overlays):
    if selected_idx is None or not overlays:
        return html.P("Select an annotation to edit it.", style={"color": "#aaa", "fontSize": "13px"})

    o = overlays[selected_idx]
    field = {"width": "80px", "padding": "5px 8px", "border": "1px solid #ddd",
             "borderRadius": "5px", "fontSize": "13px"}
    content_field = {**field, "width": "260px"}

    return html.Div([
        html.Div([
            html.Label("X position:", style={"fontSize": "12px", "color": "#666", "marginRight": "6px"}),
            dcc.Input(id="edit-x",       type="number", value=o["x"],       style=field, debounce=True),
            html.Label("Y position:", style={"fontSize": "12px", "color": "#666", "margin": "0 6px 0 14px"}),
            dcc.Input(id="edit-y",       type="number", value=o["y"],       style=field, debounce=True),
        ], style={"display": "flex", "alignItems": "center", "marginBottom": "8px"}),
        html.Div([
            html.Label("Content:", style={"fontSize": "12px", "color": "#666", "marginRight": "6px"}),
            dcc.Input(id="edit-content", type="text",   value=o["content"], style=content_field, debounce=True),
        ], style={"display": "flex", "alignItems": "center", "marginBottom": "8px"}),
        html.Button("💾 Apply", id="btn-apply-edit", style={
            "padding": "7px 18px", "border": "none", "borderRadius": "6px",
            "background": "#3b82f6", "color": "white", "cursor": "pointer", "fontSize": "13px",
        }),
        html.Div(id="edit-feedback", style={"marginTop": "6px", "fontSize": "12px", "color": "#16a34a"}),
    ])


# Placeholder outputs so Dash doesn't complain about missing IDs on initial load
app.layout.children.append(html.Div([
    dcc.Input(id="edit-x",       style={"display": "none"}),
    dcc.Input(id="edit-y",       style={"display": "none"}),
    dcc.Input(id="edit-content", style={"display": "none"}),
    html.Button(id="btn-apply-edit", style={"display": "none"}),
    html.Div(id="edit-feedback"),
], id="_hidden-edit-ids", style={"display": "none"}))


# ── Apply edits ───────────────────────────────────────────────────────────────

@callback(
    Output("portal-flow",          "viewportOverlays", allow_duplicate=True),
    Output("overlays-store",       "data",             allow_duplicate=True),
    Output("annotation-selector",  "options",          allow_duplicate=True),
    Output("edit-feedback",        "children"),
    Input("btn-apply-edit",        "n_clicks"),
    State("annotation-selector",   "value"),
    State("edit-x",                "value"),
    State("edit-y",                "value"),
    State("edit-content",          "value"),
    State("overlays-store",        "data"),
    prevent_initial_call=True,
)
def apply_edit(n, selected_idx, x, y, content, overlays):
    if selected_idx is None or not overlays:
        return dash.no_update, dash.no_update, dash.no_update, "Nothing to update."

    updated = [dict(o) for o in overlays]
    updated[selected_idx] = {
        **updated[selected_idx],
        "x": x if x is not None else updated[selected_idx]["x"],
        "y": y if y is not None else updated[selected_idx]["y"],
        "content": content if content is not None else updated[selected_idx]["content"],
    }
    opts = _build_options(updated)
    return updated, updated, opts, f"✓ Annotation [{selected_idx}] updated."


# ── Sync selector options when store resets to initial overlays ──────────────

@callback(
    Output("annotation-selector", "options", allow_duplicate=True),
    Input("overlays-store", "data"),
    prevent_initial_call=True,
)
def sync_options(overlays):
    return _build_options(overlays or [])


if __name__ == "__main__":
    app.run(debug=True, port=8034)