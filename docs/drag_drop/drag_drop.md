---
name: Drag & Drop
description: Drag nodes from a palette onto the canvas, and create nodes by dropping an edge.
endpoint: /drag-drop
package: dash_flows
icon: mdi:drag-variant
---

.. llms_copy::Drag & Drop

.. toc::

### Overview

Build a node palette and drop new nodes onto the canvas (`droppedNode`), or drag a connection into empty space to spawn a connected node with `addNodeOnEdgeDrop` (`edgeDroppedNode`).

### Live demo

Drag the nodes, pan, and zoom — the canvas below is a real, running `DashFlows` component (no callbacks, just the rendered graph):

.. exec::docs.drag_drop.demo
    :code: false

.. source::docs/drag_drop/demo.py
    :defaultExpanded: false
    :withExpandedButton: true

### Examples

Each example below is a complete, runnable Dash app from the [`examples/`](https://github.com/pip-install-python/dash-flows/tree/main/examples) folder. Run any of them with `python examples/<file>`.

#### Drag and Drop

Drag node templates from a sidebar palette and drop them onto the flow canvas. Use this pattern when you want a component-library-style builder where users assemble a graph from pre-defined node kinds.

.. exec::docs.drag_drop.ex17
    :code: false

.. source::examples/17_drag_and_drop.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `draggable="true"` HTML divs in the sidebar carry `data-node-type` / `data-node-label` attributes describing what to create.
- A `clientside_callback` wires up `ondragstart` handlers that pack that data into `e.dataTransfer` as `application/reactflow` (and `text/plain`) JSON — this runs once on load via a dummy `Input("...", "id")` trigger.
- `droppedNode` (output prop) fires when the user releases the drag over the canvas, giving you the parsed `type`, `data`, and drop `position`.
- The `droppedNode` callback appends a new node dict to `nodes` — `type="resizable"` nodes additionally get custom `handles` and a `style` with width/height.
- The raw `droppedNode` payload is echoed as JSON below the canvas so you can see exactly what the drop event contains.

#### Add Node on Edge Drop

Drag a connection off a handle and release it on empty canvas to spawn a new, already-connected node — no palette required.

.. exec::docs.drag_drop.ex28
    :code: false

.. source::examples/28_add_node_on_drop.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `addNodeOnEdgeDrop=True` tells DashFlows to create a node automatically whenever a connection drag ends over empty canvas instead of over a handle.
- `edgeDroppedNode` (output prop) reports the new node/edge pair that was created, including the drop position and which node it was connected from.
- `nodeConnections` (output prop) is a live map of every node's incoming/outgoing edges, updated as connections are made — useful for building things like validation or dependency graphs.
- Both outputs are dumped as formatted JSON under the canvas so you can watch the events fire as you drag.
- `backgroundVariant="dots"` and `colorScheme="forest"` are purely cosmetic and can be swapped for any of the supported presets.

