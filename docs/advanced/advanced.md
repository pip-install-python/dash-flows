---
name: Advanced Features
description: Undo/redo, computing flows, sub-flows, viewport portal, accessibility, and more.
endpoint: /advanced
package: dash_flows
icon: mdi:star-outline
---

.. llms_copy::Advanced Features

.. toc::

### Overview

The advanced feature set: history with `enableUndoRedo` / `undoRedoAction`, topological traversal with `computeAction` / `computeResult`, collapsible sub-flows (`toggleCollapseNode` / `collapsedGroups`), floating annotations via `viewportOverlays`, resize constraints, and full ARIA/keyboard accessibility.

### Live demo

Drag the nodes, pan, and zoom — the canvas below is a real, running `DashFlows` component (no callbacks, just the rendered graph):

.. exec::docs.advanced.demo
    :code: false

.. source::docs/advanced/demo.py
    :defaultExpanded: false
    :withExpandedButton: true

### Examples

Each example below is a complete, runnable Dash app from the [`examples/`](https://github.com/pip-install-python/dash-flows/tree/main/examples) folder. Run any of them with `python examples/<file>`.

#### Complete Showcase

A large example combining multiple node types, edge types, a group node, ELK layout switching, and live selection/count panels in one app. The full app (examples/13_complete_showcase.py) also includes a light/dark theme toggle; the embedded twin below drops that wrapper since the docs page already supplies a theme provider.

.. exec::docs.advanced.ex13
    :code: false

.. source::examples/13_complete_showcase.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `layoutOptions` — set from a `SegmentedControl` to switch between horizontal, vertical, and radial ELK layouts on the fly
- `showMiniMap` / `showControls` / `showDevTools` — toggled by switches, demonstrating that chrome can be turned on/off per render
- `selectedNodes` / `selectedEdges` — read in a callback to render badges for the current selection
- `nodes` / `edges` (as callback Inputs) — used purely to display live counts, showing that the props stay in sync with canvas state
- `type: "group"` with `parentId` / `extent: "parent"` children — nests the ML Pipeline nodes inside a group node
- `type: "toolbar"` and `type: "button"` edge — shows the ToolbarNode and ButtonEdge working alongside default/input/output nodes

#### Callback Stress Test

A performance harness that hammers the callback chain: a 5x10 node/edge grid, batch add/remove/shuffle/connect operations (up to hundreds of elements at once), and half a dozen simultaneous listeners on click/drag/selection/connection/deletion events, all while tracking a live metrics dashboard.

This example is intentionally **not embedded** as a live demo — running it inline would fire the same high-frequency callback storm against the whole docs page and degrade every other embedded example on it. Run it standalone with `python examples/23_callback_stress_test.py` instead.

.. source::examples/23_callback_stress_test.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `generate_grid_nodes` / `generate_grid_edges` — build a 50-node grid up front so the stress test starts with a non-trivial graph
- Batch buttons (`Add Batch Nodes`, `Stress Connect All`, etc.) — each dispatches one callback that mutates `nodes`/`edges` with `allow_duplicate=True` outputs so multiple buttons can target the same props
- `clickedNode`, `draggedNode`, `lastConnection`, `selectedNodes`, `deletedNodes` / `deletedEdges` — five independent listener callbacks log every interaction type into a shared event log store
- `dcc.Interval` — polls a metrics store every 500ms to compute a live callbacks-per-second rate, which is what the "stress test" is actually measuring

#### Phase 1 Features

A showcase of the React Flow 12.10.1 upgrade props: a drag threshold before a connection starts, z-index elevation for selected elements, auto-panning when tabbing between nodes, and an edge toolbar that appears on selection.

.. exec::docs.advanced.ex25
    :code: false

.. source::examples/25_phase1_features.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `connectionDragThreshold=10` — the connection line only appears after dragging 10px from a handle, preventing accidental connections on a light click
- `zIndexMode="elevate"` — selected nodes and their connected edges render above everything else
- `autoPanOnNodeFocus=True` — tabbing through nodes (after clicking into the canvas) pans the viewport to keep the focused node visible
- `data.showToolbar=True` on a `type="button"` edge — replaces the inline delete button with a floating `EdgeToolbar` that appears when the edge is selected
- MiniMap node coloring is automatic by node `type` (green=input, blue=default, purple=output, amber=toolbar) — no extra prop needed

#### Accessibility

Custom ARIA labels for the diagram, minimap, and controls, per-node/per-edge `ariaLabel` overrides, and keyboard-only navigation via focusable nodes and edges.

.. exec::docs.advanced.ex29
    :code: false

.. source::examples/29_accessibility.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `ariaLabelConfig` — supplies custom labels for the `rfDiagram`, `miniMap`, and `controls` regions, read by screen readers
- `ariaLabel` on individual node/edge dicts — gives each element its own accessible description, shown here in the info panel below the canvas
- `nodesFocusable` / `edgesFocusable` — makes every node and edge reachable via Tab / Shift+Tab
- `disableKeyboardA11y=False` — keeps arrow-key panning, Enter/Space selection, and Delete/Backspace shortcuts active
- `clickedNode` / `clickedEdge` — read in a callback to display which element was activated and its ARIA label

#### Resize Constraints

Min/max width and height bounds, plus locked aspect ratios, applied to both `ResizableNode` and `GroupNode`.

.. exec::docs.advanced.ex30
    :code: false

.. source::examples/30_resize_constraints.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `data.minWidth` / `data.maxWidth` / `data.minHeight` / `data.maxHeight` — clamp how far a `resizable` node or `group` node can be dragged in each dimension
- `data.keepAspectRatio=True` — locks the width:height ratio while resizing, regardless of which handle is dragged
- `data.handles` — customizes which side(s) of a `resizable` node expose source/target connection points
- Group resize constraints apply to the container only — child nodes with `parentId` / `extent: "parent"` stay clipped to whatever size the group currently is

#### Undo / Redo

History tracking for node moves, connections, and deletions, with dedicated Undo/Redo buttons and a live history counter.

.. exec::docs.advanced.ex32
    :code: false

.. source::examples/32_undo_redo.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `enableUndoRedo=True` and `undoRedoMaxHistory=50` — turns on history tracking and caps how many snapshots are kept
- `undoRedoAction` — set to `{"action": "undo"}` or `{"action": "redo"}` from the button callbacks to step through history
- `undoRedoState` — an output prop with `canUndo` / `canRedo` / `undoCount` / `redoCount`, used here to enable/disable the buttons and render the history badge
- `deleteElementsAction` — routes the "Delete Selected" button through React Flow's normal deletion pipeline (rather than mutating `nodes`/`edges` directly) so the undo/redo middleware can capture the change
- `selectedNodes` / `selectedEdges` — tracked in a store so the delete button knows what to remove

#### Computing Flows

Topological sort and value propagation across a small pipeline graph: input nodes hold values, operation nodes combine them, and an output node shows the final result.

.. exec::docs.advanced.ex33
    :code: false

.. source::examples/33_computing_flows.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `computeAction={"action": "compute"}` — triggers a client-side topological sort of the graph
- `computeResult` — an output prop with `traversalOrder` (node IDs in dependency order) and `nodeInputs` (each node's incoming values); JS only does the sort, Python does all the math
- The callback walks `traversalOrder`, applies each node's `data.operation` (`add` / `multiply`) to its inputs, and writes the running value back into `data.computedValue` / `data.sublabel`
- `smartHandles=True` — lets edges route to whichever side of a node is closest, useful once the pipeline fans out
- The "Reset" button restores `initial_nodes` via `copy.deepcopy` so a fresh compute run starts from the original seed values

#### Viewport Portal

Floating annotations rendered at specific flow coordinates that pan and zoom together with the canvas, with a small editor to add, edit, and remove them.

.. exec::docs.advanced.ex34
    :code: false

.. source::examples/34_viewport_portal.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `viewportOverlays` — a list of `{x, y, content, style}` dicts rendered via `ViewportPortal`, anchored to flow coordinates rather than screen pixels
- Adding an annotation appends a new overlay dict with randomized coordinates and re-renders the list
- Selecting an annotation from the `RadioItems` list populates an inline edit form (`x`, `y`, `content` inputs) sourced from a `dcc.Store` holding the current overlay list
- Hidden placeholder inputs mirror the edit-form IDs so the "Apply" callback's `State` references resolve even before an annotation has ever been selected
- Because overlays are plain data, they can be generated, persisted, or restored exactly like nodes and edges

#### Sub-flows

Collapsible group nodes: double-click a group (or use the toggle buttons) to collapse it to a compact box and hide its children, while edges to/from the group stay connected.

.. exec::docs.advanced.ex35
    :code: false

.. source::examples/35_subflows.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `toggleCollapseNode` — set to a group node's `id` to flip its collapsed/expanded state
- `collapsedGroups` — an output prop listing the IDs of currently-collapsed groups, shown in the status line
- `data.collapsedWidth` / `data.collapsedHeight` — the size a group shrinks to once collapsed
- Architecture pattern: edges that cross a group boundary connect to the **group node**, not to a child inside it; edges between two children of the same group connect child-to-child directly
- `doubleClickedNode` — lets users collapse/expand by double-clicking the group header, in addition to the toggle buttons

