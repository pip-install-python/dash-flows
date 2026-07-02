---
name: Nodes
description: Built-in node types, handle configuration, and Dash components or icons inside nodes.
endpoint: /nodes
package: dash_flows
icon: carbon:assembly-cluster
---

.. llms_copy::Nodes

.. toc::

### Overview

dash-flows ships several node types: `input` (source only), `output` (target only), `default` (both), `group` (a container for child nodes via `parentId`), `resizable`, `circle`, and `toolbar`. You can also render arbitrary Dash components and DashIconify icons inside a node's `data`.

### Live demo

Drag the nodes, pan, and zoom — the canvas below is a real, running `DashFlows` component (no callbacks, just the rendered graph):

.. exec::docs.nodes.demo
    :code: false

.. source::docs/nodes/demo.py
    :defaultExpanded: false
    :withExpandedButton: true

### Examples

Each example below is a complete, runnable Dash app from the [`examples/`](https://github.com/pip-install-python/dash-flows/tree/main/examples) folder. Run any of them with `python examples/<file>`.

#### All Node Types

Every built-in node type side by side: input, output, default, group, resizable, circle, and toolbar. Use this as a visual reference when picking a `type` for a new node.

.. exec::docs.nodes.ex02
    :code: false

.. source::examples/02_all_node_types.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `type: "input"` / `"output"` — single-handle nodes with a green (source-only) or purple (target-only) accent, good for entry/exit points.
- `type: "toolbar"` — reveals an action toolbar above the node on selection via `data.toolbarPosition`.
- `type: "resizable"` with `data.handles` — a resizable node with a custom list of handles (each with `type`, `position`, and `id`), used here to expose a top target and bottom source handle.
- `type: "group"` plus `parentId` / `extent: "parent"` on child nodes — nests nodes inside a container that moves and resizes as a unit.
- `type: "circle"` — a compact animated circular node, handy for status dots or simple junctions.

#### Handle Configurations

Control where connection handles sit, how many a node has, and how they're styled — beyond the single default source/target pair.

.. exec::docs.nodes.ex06
    :code: false

.. source::examples/06_handle_configurations.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `data.handles` — a list of `{type, position, id, style}` dicts; each entry adds one handle to the node, so a node can mix any number of sources and targets on any side.
- `position` (`"top"` / `"bottom"` / `"left"` / `"right"`) picks which edge of the node the handle sits on.
- `style.left` (e.g. `"25%"`, `"75%"`) offsets multiple handles that share the same side so they don't overlap.
- `sourceHandle` / `targetHandle` on an edge reference a specific handle `id`, letting you route several distinct connections through one node.
- `style.background` colors each handle individually, which is useful for visually pairing a handle with the edges that use it.

#### Dash Components in Nodes

Render arbitrary Dash and Dash Mantine components — including live charts — as node content, and combine that with a "detail panel" pattern for content too heavy to keep inline.

.. exec::docs.nodes.ex14
    :code: false

.. source::examples/14_dash_components_in_nodes.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `data.label` accepts any Dash component tree (here, `html.Div` stat cards with CSS-drawn mini bar charts and a progress ring) instead of a plain string.
- `type: "resizable"` nodes size themselves to their content via `data.minWidth` / `data.minHeight`, so cards keep their layout as they're resized.
- `clickedNode` (an Input on the flow's id) fires with the clicked node's full dict, letting a callback branch on `node["id"]` to render node-specific detail — full `dcc.Graph` charts live in a side panel rather than inside the node itself.
- Multiple named handles (`revenue-in`, `status-out`, etc.) route several cards into a single "Pipeline Status" node without ambiguity.
- This mirrors the library's guidance: simple HTML/CSS content can live directly in a node, while `dcc.Graph` and other heavy/interactive components are better shown in a panel driven by node click events.

#### Custom Icons

Use DashIconify icons inside node `data`, and combine them with the `layout` ("stacked" vs "horizontal") and `showIcon` options to control node composition — then update everything live from Dash Mantine form controls.

.. exec::docs.nodes.ex22
    :code: false

.. source::examples/22_custom_icons.py
    :defaultExpanded: false
    :withExpandedButton: true

**How it works**

- `data.icon` — pass a `DashIconify(icon="mdi:...")` component directly; any name from [icon-sets.iconify.design](https://icon-sets.iconify.design/) works.
- `data.layout` — `"stacked"` renders the icon above the text, `"horizontal"` renders a two-column icon/text layout.
- `data.showIcon` — toggles whether the icon renders at all, letting the same node type serve icon-only, text-only, or full-content variants.
- `data.body` — optional secondary text rendered below the label, for a short description under the title.
- Editing a `dmc.TextInput` / `dmc.SegmentedControl` / `dmc.Switch` with a pattern-matching id (`{"type": ..., "node": node_id}`) triggers a callback that rebuilds the matching node's `data` and writes it back to the flow's `nodes` prop, showing that node content can be fully data-driven.

