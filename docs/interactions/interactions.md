---
name: Interactions & Selection
description: Clicks, context menus, connection validation and limits, and multi-select.
endpoint: /interactions
package: dash_flows
icon: mdi:cursor-default-click-outline
lastmod: 2026-07-01
---

.. llms_copy::Interactions & Selection

.. toc::

### Overview

dash-flows surfaces user interaction as callback props: `clickedNode`, `doubleClickedNode`, `hoveredNode`, `contextMenuNode`, `selectedNodes`, `selectedEdges`, and `lastConnection`. You can validate or cap connections before they are committed.

### Live demo

Drag the nodes, pan, and zoom — the canvas below is a real, running `DashFlows` component (no callbacks, just the rendered graph):

.. exec::docs.interactions.demo
    :code: false

.. source::docs/interactions/demo.py
    :defaultExpanded: false
    :withExpandedButton: true

### Examples

Each example below is a complete, runnable Dash app from the [`examples/`](https://github.com/pip-install-python/dash-flows/tree/main/examples) folder. Run any of them with `python examples/<file>`.

#### Node Interactions

Read click, drag, selection, and right-click (context-menu) events on nodes in real time — useful whenever the rest of your UI needs to react to what the user is doing on the canvas.

.. exec::docs.interactions.ex07
    :code: false

.. source::examples/07_node_interactions.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `Input("ex07-flow", "selectedNodes")` — fires whenever the node selection changes; the payload is the list of currently-selected node objects.
- `Input("ex07-flow", "nodes")` — fires on every node change, including drags, so you can read live `position` data.
- `Input("ex07-flow", "selectedEdges")` — pairs with `selectedNodes` to report the full current selection (nodes and edges together).
- `Input("ex07-flow", "contextMenuNode")` — fires when a node is right-clicked, with the node's `id` and `data` in the payload.
- `multiSelectionKeyCode="Shift"` — lets Shift+click add nodes to the current selection instead of replacing it.

#### Connection Validation

Reject invalid connections before they are created — self-connections and duplicate edges are blocked automatically, and source/target-only node types (`input` / `output`) restrict which end of a connection they can be.

.. exec::docs.interactions.ex08
    :code: false

.. source::examples/08_connection_validation.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `type="input"` / `type="output"` on nodes — input nodes expose only a source handle, output nodes only a target handle, so invalid directions are impossible to draw.
- `connectionMode="loose"` — allows dragging a connection from or to any point on a node, not just a designated handle.
- `connectionLineStyle` — customizes the dashed preview line shown while a connection is being dragged.
- The "Add Random Connection" button retries up to 10 random source/target pairs and skips any that would be a self-connection or a duplicate of an existing edge id.
- `Input("ex08-flow", "edges")` — reads back the current edge list after every add/remove so the JSON panel always reflects the live graph.

#### Selection and Multi-select

Select nodes and edges by click, Shift+click, or drag-box, and drive selection programmatically from buttons — handy for bulk actions like "select all" or "delete selected".

.. exec::docs.interactions.ex10
    :code: false

.. source::examples/10_selection_multiselect.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `selectionOnDrag=True` with `selectNodesOnDrag=False` — dragging on empty canvas draws a selection box instead of moving nodes; `selectionMode="partial"` selects any node the box merely touches.
- `Input("ex10-flow", "selectedNodes")` / `Input("ex10-flow", "selectedEdges")` — read the live selection to render badges for each selected id.
- Setting `"selected": True` on node/edge dicts and writing them back to `Output("ex10-flow", "nodes")` / `"edges"` — the supported way to drive selection programmatically (e.g. "Select All", "Select Odd Nodes").
- "Delete Selected" filters `selectedNodes` out of the node list, then also drops any edge whose `source` or `target` pointed at a deleted node.
- `multiSelectionKeyCode="Shift"` — Shift+click adds to the selection rather than replacing it.

#### Connection Limits

Cap how many edges a node will accept, either per-direction or in total, so a flow can enforce structural rules like "this input only takes one wire".

.. exec::docs.interactions.ex16
    :code: false

.. source::examples/16_connection_limits.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `data.maxSourceConnections` — caps how many outgoing edges a node's source handle(s) will allow.
- `data.maxTargetConnections` — caps how many incoming edges a node's target handle(s) will allow.
- `data.maxConnections` — caps the combined total of incoming and outgoing edges on a node.
- `connectionRules={"allowSelfConnection": False, "allowDuplicateConnections": False}` — global rules applied on top of the per-node limits above.
- `Input("ex16-flow", "lastConnection")` — reports the most recently completed connection so the status bar can show `source -> target` as connections are made.

#### Context Menu

A fully custom right-click context menu built with `dmc.Menu` and `paneContextMenu`, with submenus for adding nodes, switching edge types, and changing the theme preset, color mode, and color scheme live.

.. exec::docs.interactions.ex20
    :code: false

.. source::examples/20_context_menu.py
    :defaultExpanded: false
    :withExpandedButton: true

The embedded demo above is trimmed to a fixed-height canvas that only themes itself (the full app in `examples/20_context_menu.py` runs at `100vh` and also syncs the page's overall Mantine color scheme from the same menu).

**How it works**

- `Input("ex20-flow", "paneContextMenu")` — fires on right-click over the canvas with `clientX` / `clientY`, which the callback uses to position the `dmc.Menu` and open it.
- `Input("ex20-flow", "paneClickPosition")` — fires on a plain left-click on the pane, used here to close the menu.
- `State("ex20-flow", "viewport")` — converts the screen-space menu position back into flow coordinates (accounting for pan/zoom) when placing a newly added node.
- `Output("ex20-flow", "themePreset")` / `"colorScheme"` / `"colorMode"` — the Appearance submenus write directly to these props to re-theme the canvas without a page reload.
- `Output("ex20-flow", "viewportAction")` with `{"action": "fitView", ...}` — the "Fit View" menu item triggers a programmatic viewport action.
- `assets/context_menu.css` (loaded automatically from the project's `assets/` folder) supplies the `glass-morphism-menu` and `status-bar` glassmorphism styling used by the menu, submenus, and overlays.

