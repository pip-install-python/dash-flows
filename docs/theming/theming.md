---
name: Theming & UI
description: Color modes, glass/solid/minimal presets, color schemes, and UI building blocks.
endpoint: /theming
package: dash_flows
icon: mdi:palette-outline
---

.. llms_copy::Theming & UI

.. toc::

### Overview

Switch light/dark with `colorMode` (`light` / `dark` / `system`), choose a `themePreset` (`glass` / `solid` / `minimal`), and pick a `colorScheme` (`default`, `ocean`, `forest`, `sunset`, `midnight`, `rose`). dash-flows pairs naturally with Dash Mantine Components.

### Live demo

Drag the nodes, pan, and zoom — the canvas below is a real, running `DashFlows` component (no callbacks, just the rendered graph):

.. exec::docs.theming.demo
    :code: false

.. source::docs/theming/demo.py
    :defaultExpanded: false
    :withExpandedButton: true

### Examples

Each example below is a complete, runnable Dash app from the [`examples/`](https://github.com/pip-install-python/dash-flows/tree/main/examples) folder. Run any of them with `python examples/<file>`.

#### Dark Mode with Mantine

Sync dash-flows color mode with a Dash Mantine Components theme. Use the segmented control below to switch the canvas between `light`, `dark`, and `system` — the standalone example additionally flips the whole page's Mantine theme via `forceColorScheme`, which this embedded demo intentionally does not do since the docs page owns its own theme.

.. exec::docs.theming.ex11
    :code: false

.. source::examples/11_dark_mode_mantine.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `colorMode` — set to `"light"`, `"dark"`, or `"system"` on `DashFlows`; the canvas repaints its glass-morphism surfaces, node colors, and edge/handle styling to match.
- A Mantine `SegmentedControl` drives a callback that writes directly to the `colorMode` prop, so the flow can be tied to any Dash-driven theme toggle.
- In the standalone example, a clientside callback instead flips `forceColorScheme` on a page-level `dmc.MantineProvider`, and `DashFlows` picks up the change automatically via the `data-mantine-color-scheme` attribute — no `colorMode` prop needed when the whole page shares one theme.
- CSS variables in `glass-theme.css` provide both light and dark styling for nodes, edges, Controls, and the MiniMap.

#### UI Components

Compose toolbars, panels, and controls around the flow canvas: status-aware nodes, data-carrying edges, animated SVG edges, and a lightweight node search that focuses the viewport. The full app also wires this into a shared control bar; the embedded version below keeps the same nodes, edges, and callbacks with panel spacing trimmed to fit the page.

.. exec::docs.theming.ex21
    :code: false

.. source::examples/21_ui_components.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `data.status` — `"initial"` / `"loading"` / `"success"` / `"error"` on a node's `data` renders the built-in status indicator; a button callback cycles the top-row nodes through each state.
- `type: "data"` edges — read a `data.key` field (with an optional `prefix`) straight off the source node and render it as an edge label, so the label updates whenever the source node's data changes.
- `type: "animatedSvg"` edges — animate a `shape` (`circle`, `arrow`, `pulse`, `rect`) along the edge path; `duration`, `size`, `color`, and `count` control the animation, and a `SegmentedControl` rescales every edge's `duration` at once.
- `viewportAction: {'action': 'focusNode', ...}` — used by both the "Fit View" button and the search-result buttons to pan/zoom the canvas to a specific node.
- A pattern-matching `Input({'type': 'ex21-search-result', 'id': dash.ALL}, 'n_clicks')` callback reads `ctx.triggered_id` to know which search result was clicked.

