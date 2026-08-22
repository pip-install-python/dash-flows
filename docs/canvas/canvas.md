---
name: Canvas & Controls
description: Background variants, zoom/pan controls, the minimap, and viewport control.
endpoint: /canvas
package: dash_flows
icon: mdi:card-outline
lastmod: 2026-07-01
---

.. llms_copy::Canvas & Controls

.. toc::

### Overview

Toggle the on-canvas chrome with `showBackground`, `showControls`, and `showMiniMap`, and pick a `backgroundVariant` of `dots`, `lines`, or `cross`. The viewport can also be driven programmatically from callbacks via `viewportAction` and `fitView`.

### Live demo

Drag the nodes, pan, and zoom — the canvas below is a real, running `DashFlows` component (no callbacks, just the rendered graph):

.. exec::docs.canvas.demo
    :code: false

.. source::docs/canvas/demo.py
    :defaultExpanded: false
    :withExpandedButton: true

### Examples

Each example below is a complete, runnable Dash app from the [`examples/`](https://github.com/pip-install-python/dash-flows/tree/main/examples) folder. Run any of them with `python examples/<file>`.

#### Background Variants

Swap between the `dots`, `lines`, and `cross` background patterns and tweak their color, gap, and size — handy when picking a background that fits your theme.

.. exec::docs.canvas.ex04
    :code: false

.. source::examples/04_background_variants.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `backgroundVariant` — one of `"dots"`, `"lines"`, or `"cross"`; controlled here by a `dmc.Select`.
- `backgroundColor` — CSS color for the pattern, wired to a `dmc.ColorInput`.
- `backgroundGap` / `backgroundSize` — spacing and scale of the pattern, driven by `dmc.NumberInput`.
- The callback rebuilds the whole `DashFlows` component on every control change rather than patching individual props — simple and fine for background-only settings.

#### Controls and MiniMap

A larger 5x6 node grid shows off the zoom/pan control bar and the type-colored `MiniMap`, including position and pannable/zoomable toggles.

.. exec::docs.canvas.ex05
    :code: false

.. source::examples/05_controls_and_minimap.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `showControls` / `controlsPosition` — toggle and place the zoom-in/zoom-out/fit-view/lock control bar.
- `controlsShowZoom`, `controlsShowFitView`, `controlsShowInteractive` — enable individual buttons within the control bar.
- `showMiniMap` / `miniMapPosition` — toggle and place the minimap overlay.
- `miniMapPannable` / `miniMapZoomable` — let the minimap itself be dragged or scrolled to navigate large graphs.
- With dozens of nodes, the minimap becomes the fastest way to orient yourself after zooming in.

#### Viewport Controls

Drive the camera from Dash callbacks: fit view, zoom in/out, reset zoom, and pan to named positions, plus switches to lock zooming, panning, or node dragging.

.. exec::docs.canvas.ex09
    :code: false

.. source::examples/09_viewport_controls.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `viewportAction` — an input prop you set from a callback to imperatively move the camera, e.g. `{"action": "fitView", "options": {"padding": 0.2}}` or `{"action": "setCenter", "x": 450, "y": 300, "options": {"zoom": 1, "duration": 500}}`.
- The buttons here use a clientside callback (`clientside_callback`) so the viewport reacts instantly without a server round-trip.
- `zoomOnScroll`, `zoomOnPinch`, `zoomOnDoubleClick`, `panOnDrag`, `panOnScroll`, `nodesDraggable` — booleans for locking specific interactions, toggled by the switches above.
- `minZoom` / `maxZoom` — clamp how far in/out the viewport can go.
- `viewport` — a read-only output prop reporting the current `{x, y, zoom}`, rendered live below the canvas.

