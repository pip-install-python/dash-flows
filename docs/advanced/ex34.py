"""
Embeddable twin of examples/34_viewport_portal.py for the docs page.
Rendered via `.. exec::docs.advanced.ex34`.
"""
import random

import dash
from dash import html, dcc, callback, Input, Output, State, ctx
import dash_flows

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
    "padding": "7px 14px", "border": "1px solid var(--mantine-color-default-border)",
    "borderRadius": "6px", "background": "var(--mantine-color-default)", "cursor": "pointer", "fontSize": "13px",
}

component = html.Div([
    html.P(
        "Annotations are anchored to flow coordinates and move with pan/zoom. "
        "Select one from the list below to edit its position or content.",
        style={"color": "var(--mantine-color-dimmed)", "fontSize": "13px"},
    ),

    # Top controls
    html.Div([
        html.Button("＋ Add Annotation", id="ex34-btn-add-overlay",   style=_btn),
        html.Button("✕ Clear All",        id="ex34-btn-clear-overlays", style=_btn),
    ], style={"display": "flex", "gap": "8px", "marginBottom": "10px"}),

    # Flow
    dash_flows.DashFlows(
        id="ex34-portal-flow",
        nodes=nodes,
        edges=edges,
        viewportOverlays=initial_overlays,
        fitView=True,
        showControls=True,
        showMiniMap=True,
        showBackground=True,
        smartHandles=True,
        style={
            "height": "460px",
            "border": "1px solid var(--mantine-color-default-border)",
            "borderRadius": "8px",
        },
    ),

    # Editor panel
    html.Div([
        html.H4("Edit Annotations", style={"margin": "0 0 10px 0", "fontSize": "14px"}),
        html.Div(style={"display": "flex", "gap": "16px", "alignItems": "flex-start"}, children=[

            # Annotation list (left side)
            html.Div([
                html.Div("Select:", style={"fontSize": "12px", "color": "var(--mantine-color-dimmed)", "marginBottom": "4px"}),
                dcc.RadioItems(
                    id="ex34-annotation-selector",
                    options=_build_options(initial_overlays),
                    value=None,
                    labelStyle={"display": "block", "fontSize": "13px", "padding": "3px 0", "cursor": "pointer"},
                ),
            ], style={"minWidth": "220px"}),

            # Edit form (right side)
            html.Div(id="ex34-edit-form", style={"flex": "1"}, children=[
                html.P("Select an annotation to edit it.", style={"color": "var(--mantine-color-dimmed)", "fontSize": "13px"}),
            ]),
        ]),
    ], style={
        "marginTop": "14px", "padding": "14px",
        "border": "1px solid var(--mantine-color-default-border)", "borderRadius": "8px",
        "background": "var(--mantine-color-default)",
    }),

    # Hidden stores
    dcc.Store(id="ex34-overlays-store", data=initial_overlays),

    # Placeholder inputs so Dash doesn't complain about missing IDs before
    # the edit form has been populated for the first time.
    html.Div([
        dcc.Input(id="ex34-edit-x",       style={"display": "none"}),
        dcc.Input(id="ex34-edit-y",       style={"display": "none"}),
        dcc.Input(id="ex34-edit-content", style={"display": "none"}),
        html.Button(id="ex34-btn-apply-edit", style={"display": "none"}),
        html.Div(id="ex34-edit-feedback"),
    ], id="ex34-hidden-edit-ids", style={"display": "none"}),
])


# ── Build / update the annotation list & sync overlay store ──────────────────

@callback(
    Output("ex34-portal-flow", "viewportOverlays"),
    Output("ex34-overlays-store", "data"),
    Output("ex34-annotation-selector", "options"),
    Input("ex34-btn-add-overlay",    "n_clicks"),
    Input("ex34-btn-clear-overlays", "n_clicks"),
    State("ex34-overlays-store", "data"),
    prevent_initial_call=True,
)
def add_or_clear(add_clicks, clear_clicks, current):
    if ctx.triggered_id == "ex34-btn-clear-overlays":
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
    Output("ex34-edit-form", "children"),
    Input("ex34-annotation-selector", "value"),
    State("ex34-overlays-store", "data"),
)
def show_edit_form(selected_idx, overlays):
    if selected_idx is None or not overlays:
        return html.P("Select an annotation to edit it.", style={"color": "var(--mantine-color-dimmed)", "fontSize": "13px"})

    o = overlays[selected_idx]
    field = {"width": "80px", "padding": "5px 8px", "border": "1px solid var(--mantine-color-default-border)",
             "borderRadius": "5px", "fontSize": "13px"}
    content_field = {**field, "width": "260px"}

    return html.Div([
        html.Div([
            html.Label("X position:", style={"fontSize": "12px", "color": "var(--mantine-color-dimmed)", "marginRight": "6px"}),
            dcc.Input(id="ex34-edit-x",       type="number", value=o["x"],       style=field, debounce=True),
            html.Label("Y position:", style={"fontSize": "12px", "color": "var(--mantine-color-dimmed)", "margin": "0 6px 0 14px"}),
            dcc.Input(id="ex34-edit-y",       type="number", value=o["y"],       style=field, debounce=True),
        ], style={"display": "flex", "alignItems": "center", "marginBottom": "8px"}),
        html.Div([
            html.Label("Content:", style={"fontSize": "12px", "color": "var(--mantine-color-dimmed)", "marginRight": "6px"}),
            dcc.Input(id="ex34-edit-content", type="text",   value=o["content"], style=content_field, debounce=True),
        ], style={"display": "flex", "alignItems": "center", "marginBottom": "8px"}),
        html.Button("💾 Apply", id="ex34-btn-apply-edit", style={
            "padding": "7px 18px", "border": "none", "borderRadius": "6px",
            "background": "#3b82f6", "color": "white", "cursor": "pointer", "fontSize": "13px",
        }),
        html.Div(id="ex34-edit-feedback", style={"marginTop": "6px", "fontSize": "12px", "color": "#16a34a"}),
    ])


# ── Apply edits ───────────────────────────────────────────────────────────────

@callback(
    Output("ex34-portal-flow",         "viewportOverlays", allow_duplicate=True),
    Output("ex34-overlays-store",      "data",             allow_duplicate=True),
    Output("ex34-annotation-selector", "options",          allow_duplicate=True),
    Output("ex34-edit-feedback",       "children"),
    Input("ex34-btn-apply-edit",       "n_clicks"),
    State("ex34-annotation-selector",  "value"),
    State("ex34-edit-x",               "value"),
    State("ex34-edit-y",               "value"),
    State("ex34-edit-content",         "value"),
    State("ex34-overlays-store",       "data"),
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
    Output("ex34-annotation-selector", "options", allow_duplicate=True),
    Input("ex34-overlays-store", "data"),
    prevent_initial_call=True,
)
def sync_options(overlays):
    return _build_options(overlays or [])
