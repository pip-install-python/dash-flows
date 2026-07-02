"""
Example 23: Callback Stress Test
================================
This example stress tests Dash callbacks when interacting with DashFlows:
- Large number of nodes and edges
- Multiple simultaneous callbacks monitoring different events
- Rapid node manipulation (add, remove, update)
- Stress testing drag, selection, and connection events
- Performance metrics tracking
- Batch operations on nodes/edges
"""

import dash
from dash import html, Input, Output, State, callback, ctx, dcc, ALL, MATCH
from dash.exceptions import PreventUpdate
import dash_flows
import dash_mantine_components as dmc
import json
import time
import random
import uuid

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Configuration
GRID_ROWS = 5
GRID_COLS = 10
NODE_SPACING_X = 180
NODE_SPACING_Y = 120

def generate_grid_nodes(rows, cols):
    """Generate a grid of nodes for stress testing."""
    nodes = []
    for row in range(rows):
        for col in range(cols):
            node_id = f"node-{row}-{col}"
            node_type = "default"
            if col == 0:
                node_type = "input"
            elif col == cols - 1:
                node_type = "output"

            nodes.append({
                "id": node_id,
                "type": node_type,
                "data": {
                    "label": f"N{row},{col}",
                    "sublabel": f"idx: {row * cols + col}"
                },
                "position": {
                    "x": 50 + col * NODE_SPACING_X,
                    "y": 50 + row * NODE_SPACING_Y
                },
            })
    return nodes

def generate_grid_edges(rows, cols):
    """Generate edges connecting adjacent nodes in the grid."""
    edges = []
    for row in range(rows):
        for col in range(cols - 1):
            source = f"node-{row}-{col}"
            target = f"node-{row}-{col + 1}"
            edges.append({
                "id": f"edge-{source}-{target}",
                "source": source,
                "target": target,
                "type": random.choice(["default", "smoothstep", "step"]),
            })
    return edges

initial_nodes = generate_grid_nodes(GRID_ROWS, GRID_COLS)
initial_edges = generate_grid_edges(GRID_ROWS, GRID_COLS)

# Stress test metrics store
metrics_store = {
    "callback_counts": {},
    "last_callback_times": {},
    "total_callbacks": 0,
}

app.layout = dmc.MantineProvider([
    dcc.Store(id="metrics-store", data={
        "callbacks_fired": 0,
        "nodes_added": 0,
        "nodes_removed": 0,
        "edges_added": 0,
        "edges_removed": 0,
        "drags_completed": 0,
        "selections_made": 0,
        "connections_made": 0,
        "start_time": time.time(),
    }),
    dcc.Interval(id="metrics-interval", interval=500, n_intervals=0),

    html.H1("DashFlows Callback Stress Test", style={"marginBottom": "10px"}),

    # Control Panel
    dmc.Paper([
        dmc.Group([
            dmc.Text("Stress Test Controls:", fw=700),
            dmc.Button("Add 10 Random Nodes", id="btn-add-nodes", color="green", size="xs"),
            dmc.Button("Remove 10 Random Nodes", id="btn-remove-nodes", color="red", size="xs"),
            dmc.Button("Shuffle All Positions", id="btn-shuffle", color="blue", size="xs"),
            dmc.Button("Connect Random Pairs", id="btn-connect", color="violet", size="xs"),
            dmc.Button("Select All", id="btn-select-all", color="cyan", size="xs"),
            dmc.Button("Clear Selection", id="btn-clear-selection", color="gray", size="xs"),
            dmc.Button("Reset Grid", id="btn-reset", color="orange", size="xs"),
        ], gap="xs"),
    ], p="sm", mb="sm", withBorder=True),

    # Batch Operations Panel
    dmc.Paper([
        dmc.Group([
            dmc.Text("Batch Operations:", fw=700),
            dmc.NumberInput(id="batch-size", value=50, min=10, max=500, step=10,
                          label="Batch Size", w=120, size="xs"),
            dmc.Button("Add Batch Nodes", id="btn-batch-add", color="teal", size="xs"),
            dmc.Button("Batch Update Labels", id="btn-batch-update", color="indigo", size="xs"),
            dmc.Button("Stress Connect All", id="btn-stress-connect", color="pink", size="xs"),
        ], gap="xs"),
    ], p="sm", mb="sm", withBorder=True),

    # Main Layout
    dmc.Grid([
        # Flow Canvas
        dmc.GridCol([
            dash_flows.DashFlows(
                id="stress-flow",
                nodes=initial_nodes,
                edges=initial_edges,
                style={"height": "500px", "border": "1px solid #ddd"},
                fitView=True,
                showControls=True,
                showMiniMap=True,
                miniMapPosition="bottom-left",
                nodesDraggable=True,
                nodesConnectable=True,
                elementsSelectable=True,
                selectNodesOnDrag=False,
                backgroundVariant="dots",
                connectionMode="loose",
            ),
        ], span=9),

        # Metrics Panel
        dmc.GridCol([
            dmc.Stack([
                dmc.Paper([
                    dmc.Text("Live Metrics", fw=700, size="lg", mb="xs"),
                    html.Div(id="live-metrics"),
                ], p="sm", withBorder=True),

                dmc.Paper([
                    dmc.Text("Callback Activity", fw=700, size="lg", mb="xs"),
                    html.Div(id="callback-activity"),
                ], p="sm", withBorder=True),

                dmc.Paper([
                    dmc.Text("Current State", fw=700, size="lg", mb="xs"),
                    html.Div(id="current-state"),
                ], p="sm", withBorder=True),

                dmc.Paper([
                    dmc.Text("Last Events", fw=700, size="lg", mb="xs"),
                    html.Div(id="last-events", style={"maxHeight": "150px", "overflow": "auto"}),
                ], p="sm", withBorder=True),
            ], gap="xs"),
        ], span=3),
    ]),

    # Event Log
    dmc.Paper([
        dmc.Group([
            dmc.Text("Event Log (last 20):", fw=700),
            dmc.Button("Clear Log", id="btn-clear-log", size="xs", variant="subtle"),
        ], justify="space-between", mb="xs"),
        html.Div(id="event-log", style={
            "maxHeight": "150px",
            "overflow": "auto",
            "fontFamily": "monospace",
            "fontSize": "11px",
        }),
    ], p="sm", mt="sm", withBorder=True),

    # Hidden stores for event tracking
    dcc.Store(id="event-log-store", data=[]),
    dcc.Store(id="callback-counter", data=0),
])


# ============================================================================
# STRESS TEST CALLBACKS - Node Manipulation
# ============================================================================

@callback(
    Output("stress-flow", "nodes", allow_duplicate=True),
    Output("event-log-store", "data", allow_duplicate=True),
    Output("metrics-store", "data", allow_duplicate=True),
    Input("btn-add-nodes", "n_clicks"),
    State("stress-flow", "nodes"),
    State("event-log-store", "data"),
    State("metrics-store", "data"),
    prevent_initial_call=True,
)
def add_random_nodes(n_clicks, nodes, log, metrics):
    """Add 10 random nodes to stress test node addition."""
    if not n_clicks:
        raise PreventUpdate

    nodes = nodes or []
    new_nodes = []

    for i in range(10):
        node_id = f"rand-{uuid.uuid4().hex[:8]}"
        new_nodes.append({
            "id": node_id,
            "type": random.choice(["default", "input", "output"]),
            "data": {
                "label": f"New-{i}",
                "sublabel": f"Added #{n_clicks}"
            },
            "position": {
                "x": random.randint(50, 1500),
                "y": random.randint(50, 500)
            },
        })

    log = log or []
    log.insert(0, f"[ADD] Added 10 nodes (total: {len(nodes) + 10})")
    log = log[:20]

    metrics["nodes_added"] = metrics.get("nodes_added", 0) + 10
    metrics["callbacks_fired"] = metrics.get("callbacks_fired", 0) + 1

    return nodes + new_nodes, log, metrics


@callback(
    Output("stress-flow", "nodes", allow_duplicate=True),
    Output("stress-flow", "edges", allow_duplicate=True),
    Output("event-log-store", "data", allow_duplicate=True),
    Output("metrics-store", "data", allow_duplicate=True),
    Input("btn-remove-nodes", "n_clicks"),
    State("stress-flow", "nodes"),
    State("stress-flow", "edges"),
    State("event-log-store", "data"),
    State("metrics-store", "data"),
    prevent_initial_call=True,
)
def remove_random_nodes(n_clicks, nodes, edges, log, metrics):
    """Remove 10 random nodes to stress test node removal."""
    if not n_clicks or not nodes or len(nodes) <= 10:
        raise PreventUpdate

    nodes_to_remove = set(random.sample([n["id"] for n in nodes], min(10, len(nodes))))

    remaining_nodes = [n for n in nodes if n["id"] not in nodes_to_remove]
    remaining_edges = [e for e in (edges or [])
                       if e["source"] not in nodes_to_remove
                       and e["target"] not in nodes_to_remove]

    log = log or []
    log.insert(0, f"[REMOVE] Removed 10 nodes (remaining: {len(remaining_nodes)})")
    log = log[:20]

    metrics["nodes_removed"] = metrics.get("nodes_removed", 0) + 10
    metrics["callbacks_fired"] = metrics.get("callbacks_fired", 0) + 1

    return remaining_nodes, remaining_edges, log, metrics


@callback(
    Output("stress-flow", "nodes", allow_duplicate=True),
    Output("event-log-store", "data", allow_duplicate=True),
    Output("metrics-store", "data", allow_duplicate=True),
    Input("btn-shuffle", "n_clicks"),
    State("stress-flow", "nodes"),
    State("event-log-store", "data"),
    State("metrics-store", "data"),
    prevent_initial_call=True,
)
def shuffle_positions(n_clicks, nodes, log, metrics):
    """Shuffle all node positions to stress test batch position updates."""
    if not n_clicks or not nodes:
        raise PreventUpdate

    updated_nodes = []
    for node in nodes:
        updated_node = {**node}
        updated_node["position"] = {
            "x": random.randint(50, 1500),
            "y": random.randint(50, 500)
        }
        updated_nodes.append(updated_node)

    log = log or []
    log.insert(0, f"[SHUFFLE] Shuffled {len(nodes)} node positions")
    log = log[:20]

    metrics["callbacks_fired"] = metrics.get("callbacks_fired", 0) + 1

    return updated_nodes, log, metrics


@callback(
    Output("stress-flow", "edges", allow_duplicate=True),
    Output("event-log-store", "data", allow_duplicate=True),
    Output("metrics-store", "data", allow_duplicate=True),
    Input("btn-connect", "n_clicks"),
    State("stress-flow", "nodes"),
    State("stress-flow", "edges"),
    State("event-log-store", "data"),
    State("metrics-store", "data"),
    prevent_initial_call=True,
)
def connect_random_pairs(n_clicks, nodes, edges, log, metrics):
    """Create 10 random connections to stress test edge creation."""
    if not n_clicks or not nodes or len(nodes) < 2:
        raise PreventUpdate

    edges = edges or []
    existing_connections = {(e["source"], e["target"]) for e in edges}
    node_ids = [n["id"] for n in nodes]

    new_edges = []
    attempts = 0
    while len(new_edges) < 10 and attempts < 50:
        source = random.choice(node_ids)
        target = random.choice(node_ids)
        if source != target and (source, target) not in existing_connections:
            new_edges.append({
                "id": f"edge-{uuid.uuid4().hex[:8]}",
                "source": source,
                "target": target,
                "type": random.choice(["default", "smoothstep", "step"]),
                "animated": random.choice([True, False]),
            })
            existing_connections.add((source, target))
        attempts += 1

    log = log or []
    log.insert(0, f"[CONNECT] Created {len(new_edges)} new edges (total: {len(edges) + len(new_edges)})")
    log = log[:20]

    metrics["edges_added"] = metrics.get("edges_added", 0) + len(new_edges)
    metrics["callbacks_fired"] = metrics.get("callbacks_fired", 0) + 1

    return edges + new_edges, log, metrics


# ============================================================================
# BATCH OPERATIONS
# ============================================================================

@callback(
    Output("stress-flow", "nodes", allow_duplicate=True),
    Output("event-log-store", "data", allow_duplicate=True),
    Output("metrics-store", "data", allow_duplicate=True),
    Input("btn-batch-add", "n_clicks"),
    State("batch-size", "value"),
    State("stress-flow", "nodes"),
    State("event-log-store", "data"),
    State("metrics-store", "data"),
    prevent_initial_call=True,
)
def batch_add_nodes(n_clicks, batch_size, nodes, log, metrics):
    """Add a large batch of nodes at once."""
    if not n_clicks:
        raise PreventUpdate

    batch_size = batch_size or 50
    nodes = nodes or []
    new_nodes = []

    for i in range(batch_size):
        node_id = f"batch-{uuid.uuid4().hex[:8]}"
        new_nodes.append({
            "id": node_id,
            "type": random.choice(["default", "input", "output"]),
            "data": {
                "label": f"B{i}",
                "sublabel": f"Batch #{n_clicks}"
            },
            "position": {
                "x": random.randint(50, 2000),
                "y": random.randint(50, 800)
            },
        })

    log = log or []
    log.insert(0, f"[BATCH ADD] Added {batch_size} nodes (total: {len(nodes) + batch_size})")
    log = log[:20]

    metrics["nodes_added"] = metrics.get("nodes_added", 0) + batch_size
    metrics["callbacks_fired"] = metrics.get("callbacks_fired", 0) + 1

    return nodes + new_nodes, log, metrics


@callback(
    Output("stress-flow", "nodes", allow_duplicate=True),
    Output("event-log-store", "data", allow_duplicate=True),
    Output("metrics-store", "data", allow_duplicate=True),
    Input("btn-batch-update", "n_clicks"),
    State("stress-flow", "nodes"),
    State("event-log-store", "data"),
    State("metrics-store", "data"),
    prevent_initial_call=True,
)
def batch_update_labels(n_clicks, nodes, log, metrics):
    """Update all node labels to stress test batch updates."""
    if not n_clicks or not nodes:
        raise PreventUpdate

    updated_nodes = []
    for i, node in enumerate(nodes):
        updated_node = {**node}
        updated_node["data"] = {
            **node.get("data", {}),
            "label": f"U{i}-{n_clicks}",
            "sublabel": f"Updated #{n_clicks}"
        }
        updated_nodes.append(updated_node)

    log = log or []
    log.insert(0, f"[BATCH UPDATE] Updated {len(nodes)} node labels")
    log = log[:20]

    metrics["callbacks_fired"] = metrics.get("callbacks_fired", 0) + 1

    return updated_nodes, log, metrics


@callback(
    Output("stress-flow", "edges", allow_duplicate=True),
    Output("event-log-store", "data", allow_duplicate=True),
    Output("metrics-store", "data", allow_duplicate=True),
    Input("btn-stress-connect", "n_clicks"),
    State("stress-flow", "nodes"),
    State("stress-flow", "edges"),
    State("event-log-store", "data"),
    State("metrics-store", "data"),
    prevent_initial_call=True,
)
def stress_connect_all(n_clicks, nodes, edges, log, metrics):
    """Create many random connections to stress test edge handling."""
    if not n_clicks or not nodes or len(nodes) < 2:
        raise PreventUpdate

    edges = edges or []
    existing_connections = {(e["source"], e["target"]) for e in edges}
    node_ids = [n["id"] for n in nodes]

    # Create up to 100 new edges or 2x current nodes, whichever is smaller
    target_new_edges = min(100, len(nodes) * 2)
    new_edges = []
    attempts = 0

    while len(new_edges) < target_new_edges and attempts < target_new_edges * 5:
        source = random.choice(node_ids)
        target = random.choice(node_ids)
        if source != target and (source, target) not in existing_connections:
            new_edges.append({
                "id": f"stress-{uuid.uuid4().hex[:8]}",
                "source": source,
                "target": target,
                "type": random.choice(["default", "smoothstep", "step", "straight"]),
                "animated": random.choice([True, False, False, False]),
            })
            existing_connections.add((source, target))
        attempts += 1

    log = log or []
    log.insert(0, f"[STRESS CONNECT] Created {len(new_edges)} edges (total: {len(edges) + len(new_edges)})")
    log = log[:20]

    metrics["edges_added"] = metrics.get("edges_added", 0) + len(new_edges)
    metrics["callbacks_fired"] = metrics.get("callbacks_fired", 0) + 1

    return edges + new_edges, log, metrics


# ============================================================================
# SELECTION CALLBACKS
# ============================================================================

@callback(
    Output("stress-flow", "nodes", allow_duplicate=True),
    Output("event-log-store", "data", allow_duplicate=True),
    Output("metrics-store", "data", allow_duplicate=True),
    Input("btn-select-all", "n_clicks"),
    State("stress-flow", "nodes"),
    State("event-log-store", "data"),
    State("metrics-store", "data"),
    prevent_initial_call=True,
)
def select_all_nodes(n_clicks, nodes, log, metrics):
    """Select all nodes to stress test selection handling."""
    if not n_clicks or not nodes:
        raise PreventUpdate

    selected_nodes = [{**n, "selected": True} for n in nodes]

    log = log or []
    log.insert(0, f"[SELECT ALL] Selected {len(nodes)} nodes")
    log = log[:20]

    metrics["selections_made"] = metrics.get("selections_made", 0) + 1
    metrics["callbacks_fired"] = metrics.get("callbacks_fired", 0) + 1

    return selected_nodes, log, metrics


@callback(
    Output("stress-flow", "nodes", allow_duplicate=True),
    Output("event-log-store", "data", allow_duplicate=True),
    Output("metrics-store", "data", allow_duplicate=True),
    Input("btn-clear-selection", "n_clicks"),
    State("stress-flow", "nodes"),
    State("event-log-store", "data"),
    State("metrics-store", "data"),
    prevent_initial_call=True,
)
def clear_selection(n_clicks, nodes, log, metrics):
    """Clear selection on all nodes."""
    if not n_clicks or not nodes:
        raise PreventUpdate

    cleared_nodes = [{**n, "selected": False} for n in nodes]

    log = log or []
    log.insert(0, f"[CLEAR] Cleared selection on {len(nodes)} nodes")
    log = log[:20]

    metrics["callbacks_fired"] = metrics.get("callbacks_fired", 0) + 1

    return cleared_nodes, log, metrics


@callback(
    Output("stress-flow", "nodes", allow_duplicate=True),
    Output("stress-flow", "edges", allow_duplicate=True),
    Output("event-log-store", "data", allow_duplicate=True),
    Output("metrics-store", "data", allow_duplicate=True),
    Input("btn-reset", "n_clicks"),
    State("event-log-store", "data"),
    State("metrics-store", "data"),
    prevent_initial_call=True,
)
def reset_grid(n_clicks, log, metrics):
    """Reset to initial grid configuration."""
    if not n_clicks:
        raise PreventUpdate

    log = log or []
    log.insert(0, f"[RESET] Reset to initial {GRID_ROWS}x{GRID_COLS} grid")
    log = log[:20]

    metrics["callbacks_fired"] = metrics.get("callbacks_fired", 0) + 1

    return (
        generate_grid_nodes(GRID_ROWS, GRID_COLS),
        generate_grid_edges(GRID_ROWS, GRID_COLS),
        log,
        metrics
    )


# ============================================================================
# EVENT MONITORING CALLBACKS
# ============================================================================

@callback(
    Output("event-log-store", "data", allow_duplicate=True),
    Output("metrics-store", "data", allow_duplicate=True),
    Input("stress-flow", "clickedNode"),
    State("event-log-store", "data"),
    State("metrics-store", "data"),
    prevent_initial_call=True,
)
def on_node_click(clicked_node, log, metrics):
    """Monitor node click events."""
    if not clicked_node:
        raise PreventUpdate

    node_id = clicked_node.get("id", "unknown") if isinstance(clicked_node, dict) else clicked_node

    log = log or []
    log.insert(0, f"[CLICK] Node: {node_id}")
    log = log[:20]

    metrics["callbacks_fired"] = metrics.get("callbacks_fired", 0) + 1

    return log, metrics


@callback(
    Output("event-log-store", "data", allow_duplicate=True),
    Output("metrics-store", "data", allow_duplicate=True),
    Input("stress-flow", "draggedNode"),
    State("event-log-store", "data"),
    State("metrics-store", "data"),
    prevent_initial_call=True,
)
def on_node_drag(dragged_node, log, metrics):
    """Monitor node drag events."""
    if not dragged_node:
        raise PreventUpdate

    node_id = dragged_node.get("id", "unknown")
    is_dragging = dragged_node.get("isDragging", False)

    if not is_dragging:  # Only log when drag completes
        log = log or []
        end_pos = dragged_node.get("endPosition", {})
        log.insert(0, f"[DRAG] Node {node_id} to ({end_pos.get('x', 0):.0f}, {end_pos.get('y', 0):.0f})")
        log = log[:20]

        metrics["drags_completed"] = metrics.get("drags_completed", 0) + 1
        metrics["callbacks_fired"] = metrics.get("callbacks_fired", 0) + 1

        return log, metrics

    raise PreventUpdate


@callback(
    Output("event-log-store", "data", allow_duplicate=True),
    Output("metrics-store", "data", allow_duplicate=True),
    Input("stress-flow", "lastConnection"),
    State("event-log-store", "data"),
    State("metrics-store", "data"),
    prevent_initial_call=True,
)
def on_connection(last_connection, log, metrics):
    """Monitor new connection events."""
    if not last_connection:
        raise PreventUpdate

    source = last_connection.get("source", "?")
    target = last_connection.get("target", "?")

    log = log or []
    log.insert(0, f"[CONNECTION] {source} -> {target}")
    log = log[:20]

    metrics["connections_made"] = metrics.get("connections_made", 0) + 1
    metrics["callbacks_fired"] = metrics.get("callbacks_fired", 0) + 1

    return log, metrics


@callback(
    Output("event-log-store", "data", allow_duplicate=True),
    Output("metrics-store", "data", allow_duplicate=True),
    Input("stress-flow", "selectedNodes"),
    State("event-log-store", "data"),
    State("metrics-store", "data"),
    prevent_initial_call=True,
)
def on_selection_change(selected_nodes, log, metrics):
    """Monitor selection changes."""
    count = len(selected_nodes) if selected_nodes else 0

    log = log or []
    log.insert(0, f"[SELECTION] {count} node(s) selected")
    log = log[:20]

    metrics["selections_made"] = metrics.get("selections_made", 0) + 1
    metrics["callbacks_fired"] = metrics.get("callbacks_fired", 0) + 1

    return log, metrics


@callback(
    Output("event-log-store", "data", allow_duplicate=True),
    Output("metrics-store", "data", allow_duplicate=True),
    Input("stress-flow", "deletedNodes"),
    Input("stress-flow", "deletedEdges"),
    State("event-log-store", "data"),
    State("metrics-store", "data"),
    prevent_initial_call=True,
)
def on_delete(deleted_nodes, deleted_edges, log, metrics):
    """Monitor deletion events."""
    log = log or []

    if deleted_nodes:
        count = len(deleted_nodes)
        log.insert(0, f"[DELETE] {count} node(s) deleted")
        metrics["nodes_removed"] = metrics.get("nodes_removed", 0) + count

    if deleted_edges:
        count = len(deleted_edges)
        log.insert(0, f"[DELETE] {count} edge(s) deleted")
        metrics["edges_removed"] = metrics.get("edges_removed", 0) + count

    if not deleted_nodes and not deleted_edges:
        raise PreventUpdate

    log = log[:20]
    metrics["callbacks_fired"] = metrics.get("callbacks_fired", 0) + 1

    return log, metrics


# ============================================================================
# DISPLAY CALLBACKS
# ============================================================================

@callback(
    Output("live-metrics", "children"),
    Input("metrics-interval", "n_intervals"),
    State("metrics-store", "data"),
)
def update_live_metrics(n_intervals, metrics):
    """Update live metrics display."""
    elapsed = time.time() - metrics.get("start_time", time.time())
    callbacks_fired = metrics.get("callbacks_fired", 0)
    rate = callbacks_fired / elapsed if elapsed > 0 else 0

    return dmc.Stack([
        dmc.Group([
            dmc.Text("Elapsed:", size="sm"),
            dmc.Text(f"{elapsed:.1f}s", fw=600, size="sm"),
        ], justify="space-between"),
        dmc.Group([
            dmc.Text("Callbacks:", size="sm"),
            dmc.Text(f"{callbacks_fired}", fw=600, size="sm"),
        ], justify="space-between"),
        dmc.Group([
            dmc.Text("Rate:", size="sm"),
            dmc.Text(f"{rate:.2f}/s", fw=600, size="sm"),
        ], justify="space-between"),
    ], gap=4)


@callback(
    Output("callback-activity", "children"),
    Input("metrics-store", "data"),
)
def update_callback_activity(metrics):
    """Update callback activity display."""
    return dmc.Stack([
        dmc.Group([
            dmc.Text("Nodes Added:", size="sm"),
            dmc.Badge(str(metrics.get("nodes_added", 0)), color="green", size="sm"),
        ], justify="space-between"),
        dmc.Group([
            dmc.Text("Nodes Removed:", size="sm"),
            dmc.Badge(str(metrics.get("nodes_removed", 0)), color="red", size="sm"),
        ], justify="space-between"),
        dmc.Group([
            dmc.Text("Edges Added:", size="sm"),
            dmc.Badge(str(metrics.get("edges_added", 0)), color="blue", size="sm"),
        ], justify="space-between"),
        dmc.Group([
            dmc.Text("Edges Removed:", size="sm"),
            dmc.Badge(str(metrics.get("edges_removed", 0)), color="orange", size="sm"),
        ], justify="space-between"),
        dmc.Group([
            dmc.Text("Drags:", size="sm"),
            dmc.Badge(str(metrics.get("drags_completed", 0)), color="violet", size="sm"),
        ], justify="space-between"),
        dmc.Group([
            dmc.Text("Connections:", size="sm"),
            dmc.Badge(str(metrics.get("connections_made", 0)), color="cyan", size="sm"),
        ], justify="space-between"),
    ], gap=4)


@callback(
    Output("current-state", "children"),
    Input("stress-flow", "nodes"),
    Input("stress-flow", "edges"),
)
def update_current_state(nodes, edges):
    """Display current node and edge counts."""
    node_count = len(nodes) if nodes else 0
    edge_count = len(edges) if edges else 0

    return dmc.Stack([
        dmc.Group([
            dmc.Text("Total Nodes:", size="sm"),
            dmc.Text(f"{node_count}", fw=700, size="lg", c="blue"),
        ], justify="space-between"),
        dmc.Group([
            dmc.Text("Total Edges:", size="sm"),
            dmc.Text(f"{edge_count}", fw=700, size="lg", c="grape"),
        ], justify="space-between"),
    ], gap=4)


@callback(
    Output("last-events", "children"),
    Input("stress-flow", "clickedNode"),
    Input("stress-flow", "hoveredNode"),
    Input("stress-flow", "draggedNode"),
)
def update_last_events(clicked, hovered, dragged):
    """Display last event information."""
    events = []

    if clicked:
        node_id = clicked.get("id", clicked) if isinstance(clicked, dict) else clicked
        events.append(dmc.Text(f"Clicked: {node_id}", size="xs"))

    if hovered:
        node_id = hovered.get("id", hovered) if isinstance(hovered, dict) else hovered
        events.append(dmc.Text(f"Hovered: {node_id}", size="xs", c="dimmed"))

    if dragged:
        node_id = dragged.get("id", "?")
        is_dragging = dragged.get("isDragging", False)
        status = "dragging..." if is_dragging else "dropped"
        events.append(dmc.Text(f"Drag: {node_id} ({status})", size="xs"))

    if not events:
        events.append(dmc.Text("No recent events", size="xs", c="dimmed"))

    return dmc.Stack(events, gap=2)


@callback(
    Output("event-log", "children"),
    Input("event-log-store", "data"),
)
def update_event_log(log):
    """Display the event log."""
    if not log:
        return dmc.Text("No events yet...", c="dimmed", size="sm")

    return html.Div([
        html.Div(entry, style={"padding": "2px 0"}) for entry in log
    ])


@callback(
    Output("event-log-store", "data", allow_duplicate=True),
    Input("btn-clear-log", "n_clicks"),
    prevent_initial_call=True,
)
def clear_log(n_clicks):
    """Clear the event log."""
    return []


if __name__ == "__main__":
    app.run(debug=True, port=8093)