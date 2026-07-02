---
name: Getting Started
description: "Build your first dash-flows graph: nodes, edges, and styling."
endpoint: /getting-started
package: dash_flows
icon: mdi:rocket-launch-outline
---

.. llms_copy::Getting Started

.. toc::

### Overview

**dash-flows** renders interactive node graphs in Plotly Dash using [React Flow 12](https://reactflow.dev). A flow needs three things: a list of `nodes`, a list of `edges`, and a `style` with a `height`. Node `type` picks the visual (`input`, `default`, `output`, …); edges connect nodes by `source` and `target` id. Set `animated=True` on an edge for a moving dashed line.

### Live demo

Drag the nodes, pan, and zoom — the canvas below is a real, running `DashFlows` component (no callbacks, just the rendered graph):

.. exec::docs.getting_started.demo
    :code: false

.. source::docs/getting_started/demo.py
    :defaultExpanded: false
    :withExpandedButton: true

### Examples

Each example below is a complete, runnable Dash app from the [`examples/`](https://github.com/pip-install-python/dash-flows/tree/main/examples) folder. Run any of them with `python examples/<file>`.

#### Basic Nodes and Edges

The fundamentals — creating typed nodes, connecting them with edges, and basic positioning and styling. Use this pattern as the starting point for any new flow.

.. exec::docs.getting_started.ex01
    :code: false

.. source::examples/01_basic_nodes_and_edges.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `nodes` — a plain list of dicts, each with an `id`, `type` (`"default"` here), `data.label`, and a `position` in canvas pixels.
- `edges` — connect nodes by `source`/`target` id; the `id` on each edge just needs to be unique.
- `animated=True` on an edge draws a moving dashed line, useful for highlighting active/primary paths.
- `label` on an edge renders text along the connector (see `"Step 1"` / `"Step 2"`).
- `style={"height": ...}` is required — React Flow needs an explicit container height to size the canvas.
- `fitView`, `showControls`, and `showMiniMap` are convenience toggles for the zoom/pan controls and minimap overlay.

