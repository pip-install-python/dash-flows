---
name: Layout & Handles
description: Automatic ELK layouts, smart handles, helper lines, and animated layout transitions.
endpoint: /layout
package: dash_flows
icon: mdi:sitemap-outline
---

.. llms_copy::Layout & Handles

.. toc::

### Overview

Arrange graphs automatically with ELK by passing `layoutOptions`, and animate the transition with `animateLayout`. `smartHandles` auto-routes edges to the closest node side, while `helperLines` shows alignment guides as you drag.

### Live demo

Drag the nodes, pan, and zoom — the canvas below is a real, running `DashFlows` component (no callbacks, just the rendered graph):

.. exec::docs.layout.demo
    :code: false

.. source::docs/layout/demo.py
    :defaultExpanded: false
    :withExpandedButton: true

### Examples

Each example below is a complete, runnable Dash app from the [`examples/`](https://github.com/pip-install-python/dash-flows/tree/main/examples) folder. Run any of them with `python examples/<file>`.

#### ELK Layouts

Automatic graph layout with the ELK engine (layered, tree, radial, force, and stress). Pick an algorithm, click Apply, and watch the whole graph rearrange — useful whenever nodes are added dynamically and you don't want to hand-place positions.

.. exec::docs.layout.ex12
    :code: false

.. source::examples/12_elk_layouts.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `layoutOptions` — a JSON string of ELK options (`elk.algorithm`, `elk.direction`, spacing keys); setting it from a callback re-runs the layout engine and repositions every node.
- `elk.algorithm` values shown here: `layered` (with `elk.direction` of `DOWN`/`RIGHT`/`UP`/`LEFT`), `org.eclipse.elk.force`, `org.eclipse.elk.radial`, and `org.eclipse.elk.stress`.
- All nodes start at `{"x": 0, "y": 0}` — ELK computes real positions on first render since `layoutOptions` is set in the initial component props.
- `Output("ex12-elk-flow", "nodes")` on the Reset button — pushes the nodes back to their original (unlaid-out) positions so you can re-apply a layout and see the change.
- The full example additionally renders the active `layoutOptions` JSON in a `Pre` block for inspection, alongside a short reference on when to use each algorithm.

#### Smart Handles

Auto-route edges to the nearest node side by rendering handles on all four sides, instead of forcing every connection through fixed top/bottom handles. Toggle it off to see the difference on a graph laid out in a loose, non-linear grid.

.. exec::docs.layout.ex24
    :code: false

.. source::examples/24_smart_handles.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `smartHandles=True` — renders connection handles on all four sides of every node and picks whichever pair is closest for each edge, avoiding backtracking loops.
- With `smartHandles` off, all edges fall back to the default single top (target) / bottom (source) handle pair, which looks messy on diagonally arranged nodes.
- `Output("ex24-smart-flow", "smartHandles")` — flips the prop live from a `dcc.Checklist`, so you can compare routing with and without it on the same graph.
- `data.sourcePosition` / `data.targetPosition` — the full example also shows *manual* handle placement (e.g. `"right"` / `"left"`) for a strict left-to-right flow when you want precise control instead of automatic routing.
- `colorScheme="ocean"` — swaps in the built-in ocean palette for this demo.

#### Helper Lines

Alignment guides that appear as you drag a node near another node's edge, snapping it into place — the same kind of guide you'd get in a design tool like Figma.

.. exec::docs.layout.ex27
    :code: false

.. source::examples/27_helper_lines.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `helperLines=True` — enables the alignment-guide overlay; drag any node near another node's top/bottom/left/right edge or center line to see a blue guide and snap.
- `helperLineThreshold` — the snap distance in pixels; wired here to a `dcc.Slider` (1–20px) so you can feel the difference between a tight and loose snap radius live.
- `smartHandles=True` — combined with helper lines so edges keep routing cleanly even as you nudge nodes into alignment.
- `Output("ex27-helper-flow", "helperLines")` / `Output("ex27-helper-flow", "helperLineThreshold")` — both driven by the same callback, so the checkbox and slider update the running flow instantly.

#### Animated Layout

Smoothly interpolate node positions when a new ELK layout is applied, instead of nodes jumping straight to their new spot. Click between the layout buttons to see the pipeline graph animate.

.. exec::docs.layout.ex31
    :code: false

.. source::examples/31_animated_layout.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `animateLayout=True` — turns on eased position transitions whenever `layoutOptions` changes, instead of an instant re-layout.
- `animateLayoutDuration=500` — the transition length in milliseconds; nodes interpolate along an ease-out cubic curve.
- `layoutOptions` — swapped between four ELK presets (`layered` RIGHT, `layered` DOWN, `force`, `radial`) by the layout buttons.
- `viewportAction={"action": "fitView", "duration": 300, "delay": 550}` — re-fits the viewport just after the layout animation finishes, so the newly arranged graph stays centered.
- `dcc.Store` + `ctx.triggered_id` — tracks which layout button was last clicked so its style can be highlighted as "active" via a second callback.

