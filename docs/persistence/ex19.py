"""
Embeddable twin of examples/19_copy_paste.py for the docs page.
Rendered via `.. exec::docs.persistence.ex19`.
"""
from dash import html, callback, clientside_callback, Input, Output, State
import dash_flows
import dash_mantine_components as dmc

initial_nodes = [
    {"id": "node-1", "type": "input", "data": {"label": "Source A"}, "position": {"x": 100, "y": 100}},
    {"id": "node-2", "type": "default", "data": {"label": "Process"}, "position": {"x": 100, "y": 250}},
    {"id": "node-3", "type": "output", "data": {"label": "Output"}, "position": {"x": 100, "y": 400}},
]

initial_edges = [
    {"id": "e1-2", "source": "node-1", "target": "node-2"},
    {"id": "e2-3", "source": "node-2", "target": "node-3"},
]

component = html.Div([
    html.P([
        "Select nodes (click or shift+drag), then use the buttons or keyboard shortcuts to copy/paste.",
        html.Br(),
        "Tip: Hold Shift and drag to select multiple nodes.",
    ], style={"marginTop": 0}),

    dmc.Group([
        dmc.Button("Copy Selected (Ctrl+C)", id="ex19-btn-copy", n_clicks=0, color="green"),
        dmc.Button("Paste (Ctrl+V)", id="ex19-btn-paste", n_clicks=0, color="blue"),
        dmc.Button("Copy All", id="ex19-btn-copy-all", n_clicks=0, color="orange"),
    ], gap="sm", mb="sm"),

    html.Div(
        id="ex19-status",
        children="Select nodes and use Copy/Paste",
        style={
            "padding": "10px",
            "marginBottom": "10px",
            "borderRadius": "6px",
            "background": "var(--mantine-color-default-hover)",
        },
    ),

    dash_flows.DashFlows(
        id="ex19-flow",
        nodes=initial_nodes,
        edges=initial_edges,
        style={
            "height": "480px",
            "border": "1px solid var(--mantine-color-default-border)",
            "borderRadius": "8px",
        },
        fitView=True,
        showControls=True,
        showMiniMap=True,
        showBackground=True,
        selectionOnDrag=True,  # Enable drag selection
    ),
])


# Copy button handler
@callback(
    Output("ex19-flow", "copyAction"),
    Input("ex19-btn-copy", "n_clicks"),
    prevent_initial_call=True,
)
def handle_copy(n_clicks):
    return True


# Copy all button handler
@callback(
    Output("ex19-flow", "copyAction", allow_duplicate=True),
    Input("ex19-btn-copy-all", "n_clicks"),
    State("ex19-flow", "nodes"),
    prevent_initial_call=True,
)
def handle_copy_all(n_clicks, nodes):
    # Deselect all first (to trigger copy all behavior)
    return True


# Paste button handler
@callback(
    Output("ex19-flow", "pasteAction"),
    Input("ex19-btn-paste", "n_clicks"),
    prevent_initial_call=True,
)
def handle_paste(n_clicks):
    return {"offset": {"x": 100, "y": 50}}


# Update status based on clipboard and paste events
@callback(
    Output("ex19-status", "children"),
    Input("ex19-flow", "clipboard"),
    Input("ex19-flow", "pastedElements"),
    Input("ex19-flow", "selectedNodes"),
)
def update_status(clipboard, pasted, selected):
    status_parts = []

    if selected:
        status_parts.append(f"Selected: {len(selected)} node(s)")
    else:
        status_parts.append("No nodes selected")

    if clipboard and clipboard.get("nodes"):
        status_parts.append(f" | Clipboard: {len(clipboard['nodes'])} node(s)")

    if pasted and pasted.get("nodeIds"):
        status_parts.append(f" | Just pasted: {len(pasted['nodeIds'])} node(s)")

    return "".join(status_parts) if status_parts else "Select nodes and use Copy/Paste"


# Client-side callback for keyboard shortcuts
clientside_callback(
    """
    function(id) {
        document.addEventListener('keydown', function(e) {
            // Ctrl+C or Cmd+C
            if ((e.ctrlKey || e.metaKey) && e.key === 'c' && !e.shiftKey) {
                // Don't interfere with normal copy in text inputs
                if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

                e.preventDefault();
                document.getElementById('ex19-btn-copy').click();
            }
            // Ctrl+V or Cmd+V
            if ((e.ctrlKey || e.metaKey) && e.key === 'v' && !e.shiftKey) {
                if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

                e.preventDefault();
                document.getElementById('ex19-btn-paste').click();
            }
        });
        return window.dash_clientside.no_update;
    }
    """,
    Output("ex19-status", "data-keyboard"),
    Input("ex19-status", "id"),
)
