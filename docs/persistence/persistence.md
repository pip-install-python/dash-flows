---
name: Save, Restore & Export
description: Persist and restore flow state, export to PNG, and copy/paste.
endpoint: /persistence
package: dash_flows
icon: mdi:content-save-outline
lastmod: 2026-07-01
category: Data & Export
order: 1
---

.. llms_copy::Save, Restore & Export

.. toc::

### Overview

Serialize the whole graph with `exportFlowState` / `flowState` and rebuild it with `restoreFlowState`. Export the canvas to an image via `downloadImage`, and duplicate elements with `copyAction` / `pasteAction`.

### Live demo

Drag the nodes, pan, and zoom — the canvas below is a real, running `DashFlows` component (no callbacks, just the rendered graph):

.. exec::docs.persistence.demo
    :code: false

.. source::docs/persistence/demo.py
    :defaultExpanded: false
    :withExpandedButton: true

### Examples

Each example below is a complete, runnable Dash app from the [`examples/`](https://github.com/pip-install-python/dash-flows/tree/main/examples) folder. Run any of them with `python examples/<file>`.

#### Save & Restore

Export the current flow to JSON and restore it later, plus drive the viewport (fit, zoom, focus) from callbacks. Use this pattern for a "save my diagram" button or a session-restore flow.

.. exec::docs.persistence.ex15
    :code: false

.. source::examples/15_save_restore.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `exportFlowState=True` — asks the flow to serialize its current nodes, edges, and viewport; the result comes back on `flowState`.
- `Input("ex15-flow", "flowState")` — fires once export completes, so you can stash it in a `dcc.Store` and preview it as JSON.
- `restoreFlowState={"nodes": ..., "edges": ..., "viewport": ...}` — rebuilds the flow from a previously saved (or hand-built) state object.
- `Output(..., allow_duplicate=True)` — required whenever a second callback also targets `restoreFlowState`, here used by the "Reset to Initial" button.
- `viewportAction={"action": "fitView" | "zoomIn" | "zoomOut" | "focusNode", "options": {...}}` — triggers programmatic viewport moves without touching nodes or edges.

#### Export Image

Download the flow as a PNG, SVG, or JPEG using html-to-image, with options for background color, quality, and resolution.

.. exec::docs.persistence.ex18
    :code: false

.. source::examples/18_export_image.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `downloadImage={"format": "png" | "svg" | "jpeg", "filename": ..., "backgroundColor": ...}` — triggers a browser download of the rendered canvas.
- `pixelRatio` — renders at a higher resolution (e.g. `4` for a 4x PNG) without changing the on-screen layout.
- `backgroundColor="transparent"` — exports a PNG with no background fill, useful for overlaying on other content.
- `Input("ex18-flow", "imageDownloaded")` — fires with the filename and format once the export succeeds.
- `Input("ex18-flow", "lastError")` — reports export failures (checked here for `type == "image-export"`).

#### Copy & Paste

Copy selected nodes and edges to an internal clipboard, then paste them with a position offset — wired to both buttons and Ctrl/Cmd+C / Ctrl/Cmd+V keyboard shortcuts.

.. exec::docs.persistence.ex19
    :code: false

.. source::examples/19_copy_paste.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `copyAction=True` — copies the currently selected nodes/edges (or everything, if nothing is selected) into the flow's internal `clipboard`.
- `pasteAction={"offset": {"x": 100, "y": 50}}` — pastes the clipboard contents, shifting the new copies so they don't sit exactly on top of the originals.
- `selectionOnDrag=True` — lets a shift+drag rectangle select multiple nodes at once, so Copy Selected has something to act on.
- `Input("ex19-flow", "clipboard")` / `Input("ex19-flow", "pastedElements")` — report clipboard contents and the ids of the most recently pasted elements.
- `clientside_callback(...)` — listens for Ctrl/Cmd+C and Ctrl/Cmd+V at the document level and clicks the copy/paste buttons, so keyboard shortcuts work without a server round trip.

