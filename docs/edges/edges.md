---
name: Edges
description: Every edge type, including floating edges that attach to the nearest border.
endpoint: /edges
package: dash_flows
icon: tabler:line-dashed
lastmod: 2026-07-01
category: Building Graphs
order: 2
---

.. llms_copy::Edges

.. toc::

### Overview

Set an edge's `type` to choose its path: `straight`, `step`, `smoothstep`, `simplebezier`, `button`, `data`, `animated`, or `floating`. Floating edges connect to the nearest point on each node's border instead of a fixed handle.

### Live demo

Drag the nodes, pan, and zoom — the canvas below is a real, running `DashFlows` component (no callbacks, just the rendered graph):

.. exec::docs.edges.demo
    :code: false

.. source::docs/edges/demo.py
    :defaultExpanded: false
    :withExpandedButton: true

### Examples

Each example below is a complete, runnable Dash app from the [`examples/`](https://github.com/pip-install-python/dash-flows/tree/main/examples) folder. Run any of them with `python examples/<file>`.

#### All Edge Types

A gallery of every edge type — default, straight, step, smoothstep, simplebezier, and button — laid out as a row of sources connecting to a row of targets, plus a callback that tracks edge deletions.

.. exec::docs.edges.ex03
    :code: false

.. source::examples/03_all_edge_types.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `type` on each edge — picks the renderer (`"default"`, `"straight"`, `"step"`, `"smoothstep"`, `"simplebezier"`, `"button"`); omit it to fall back to React Flow's default bezier curve.
- `animated=True` — draws a moving dashed line on the default edge.
- `data={"borderRadius": 15}` — the smoothstep edge reads this to control corner rounding.
- `data={"showButton": True, "buttonLabel": "x"}` — the button edge renders a small button (here used for deletion) on top of the path.
- `Input("ex03-edge-types-flow", "edges")` — fires whenever the edge list changes (e.g. after clicking a button edge's delete control), letting you track the current edge count.

#### Floating Edges

Edges that dynamically attach to the closest border point of each node, instead of a fixed handle position — useful when nodes sit at irregular angles relative to each other.

.. exec::docs.edges.ex26
    :code: false

.. source::examples/26_floating_edges.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `type: "floating"` on every edge — connects to whichever point on the node's border is closest to the other node, and re-computes it live as nodes move.
- `fitViewOptions={"padding": 0.2}` — adds breathing room around the graph when `fitView` runs.
- `colorScheme="ocean"` — swaps the default glass theme palette for the built-in ocean color scheme.
- `showMiniMap` / `showBackground` — enables the minimap overlay and canvas background grid alongside the controls.
- `Input("ex26-floating-flow", "clickedNode")` — reports the clicked node's `id` and `data.label`; try dragging nodes to see the floating edges re-attach in real time.

