"""
Embeddable twin of examples/33_computing_flows.py for the docs page.
Rendered via `.. exec::docs.advanced.ex33`.
"""
import copy

import dash
from dash import html, callback, Input, Output, State
import dash_flows

initial_nodes = [
    {
        "id": "input-a",
        "type": "input",
        "data": {"label": "Input A", "sublabel": "Value: 10", "computedValue": 10},
        "position": {"x": 50, "y": 50},
    },
    {
        "id": "input-b",
        "type": "input",
        "data": {"label": "Input B", "sublabel": "Value: 5", "computedValue": 5},
        "position": {"x": 50, "y": 200},
    },
    {
        "id": "input-c",
        "type": "input",
        "data": {"label": "Input C", "sublabel": "Value: 3", "computedValue": 3},
        "position": {"x": 50, "y": 350},
    },
    {
        "id": "add",
        "type": "default",
        "data": {"label": "Add (+)", "sublabel": "A + B", "operation": "add", "computedValue": None},
        "position": {"x": 300, "y": 100},
    },
    {
        "id": "multiply",
        "type": "default",
        "data": {"label": "Multiply (×)", "sublabel": "result × C", "operation": "multiply", "computedValue": None},
        "position": {"x": 550, "y": 200},
    },
    {
        "id": "output",
        "type": "output",
        "data": {"label": "Result", "sublabel": "Waiting...", "computedValue": None},
        "position": {"x": 800, "y": 200},
    },
]

initial_edges = [
    {"id": "e1", "source": "input-a", "target": "add"},
    {"id": "e2", "source": "input-b", "target": "add"},
    {"id": "e3", "source": "add", "target": "multiply"},
    {"id": "e4", "source": "input-c", "target": "multiply"},
    {"id": "e5", "source": "multiply", "target": "output"},
]

btn_style = {
    "padding": "10px 24px",
    "border": "none",
    "borderRadius": "8px",
    "background": "linear-gradient(135deg, #3b82f6, #8b5cf6)",
    "color": "white",
    "cursor": "pointer",
    "fontSize": "14px",
    "fontWeight": "600",
}

reset_btn_style = {
    "padding": "10px 18px",
    "border": "1px solid var(--mantine-color-default-border)",
    "borderRadius": "8px",
    "background": "var(--mantine-color-default)",
    "color": "var(--mantine-color-text)",
    "cursor": "pointer",
    "fontSize": "14px",
}

component = html.Div([
    html.P(
        "Pipeline: (A + B) × C → Result.  Click ⚡ Compute to propagate values through the graph.",
        style={"color": "var(--mantine-color-dimmed)", "fontSize": "13px"},
    ),

    html.Div([
        html.Button("⚡ Compute", id="ex33-btn-compute", style=btn_style),
        html.Button("↺ Reset", id="ex33-btn-reset", style=reset_btn_style),
        html.Span(id="ex33-compute-status", style={
            "padding": "8px 16px", "background": "var(--mantine-color-default)",
            "borderRadius": "6px", "fontSize": "13px",
        }),
    ], style={"display": "flex", "gap": "10px", "alignItems": "center", "marginBottom": "10px"}),

    dash_flows.DashFlows(
        id="ex33-compute-flow",
        nodes=initial_nodes,
        edges=initial_edges,
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
])


@callback(
    Output("ex33-compute-flow", "computeAction"),
    Input("ex33-btn-compute", "n_clicks"),
    prevent_initial_call=True,
)
def trigger_compute(n):
    return {"action": "compute"}


@callback(
    Output("ex33-compute-flow", "nodes"),
    Output("ex33-compute-status", "children"),
    Input("ex33-compute-flow", "computeResult"),
    State("ex33-compute-flow", "nodes"),
    prevent_initial_call=True,
)
def process_computation(result, nodes):
    if not result:
        return dash.no_update, dash.no_update

    traversal = result.get("traversalOrder", [])
    node_inputs_meta = result.get("nodeInputs", {})

    node_map = {n["id"]: n for n in nodes}

    # Seed computed_values from nodes that already have a value (source nodes).
    # We maintain our own dict so intermediate results propagate correctly
    # through the topological order — the JS snapshot only knows values that
    # existed BEFORE this compute call.
    computed_values = {}
    for n in nodes:
        val = n["data"].get("computedValue")
        if val is not None:
            computed_values[n["id"]] = val

    steps = []

    for node_id in traversal:
        node = node_map.get(node_id)
        if not node:
            continue

        meta = node_inputs_meta.get(node_id, {})
        incoming = meta.get("inputs", [])  # [{nodeId, value, data}, ...]
        operation = node["data"].get("operation")

        if not incoming:
            # Source node — keep its seed value, nothing to compute
            continue

        # Use our locally propagated computed_values for inputs, not the
        # stale JS snapshot values (which are None for intermediate nodes).
        input_values = [
            computed_values[inp["nodeId"]]
            for inp in incoming
            if inp["nodeId"] in computed_values
        ]

        if not input_values:
            continue

        if operation == "add":
            computed = sum(input_values)
            steps.append(f"{node_id}: {' + '.join(str(v) for v in input_values)} = {computed}")
        elif operation == "multiply":
            computed = 1
            for v in input_values:
                computed *= v
            steps.append(f"{node_id}: {' × '.join(str(v) for v in input_values)} = {computed}")
        else:
            # Output node or unknown: pass through
            computed = sum(input_values)
            steps.append(f"{node_id}: result = {computed}")

        computed_values[node_id] = computed
        node["data"] = dict(node["data"])
        node["data"]["computedValue"] = computed
        node["data"]["sublabel"] = f"= {computed}"

    updated_nodes = list(node_map.values())
    final_value = computed_values.get("output", "?")
    status = f"✓ Result = {final_value}   ({' → '.join(steps)})"

    return updated_nodes, status


@callback(
    Output("ex33-compute-flow", "nodes", allow_duplicate=True),
    Output("ex33-compute-status", "children", allow_duplicate=True),
    Input("ex33-btn-reset", "n_clicks"),
    prevent_initial_call=True,
)
def reset_flow(n):
    return copy.deepcopy(initial_nodes), "Reset — click ⚡ Compute to run again."
