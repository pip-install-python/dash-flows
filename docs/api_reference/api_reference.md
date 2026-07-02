---
name: API Reference
description: The full DashFlows prop table plus node and edge component props.
endpoint: /api-reference
package: dash_flows
icon: mdi:api
---

.. llms_copy::API Reference

.. toc::

### Overview

Auto-generated prop tables for the dash-flows components. `DashFlows` is the main component; the node and edge components below are the custom types it can render.

### DashFlows component

The main component. Set `nodes`, `edges`, and a `style` with a `height`; everything else is optional. Interaction outputs (e.g. `clickedNode`, `selectedNodes`, `lastConnection`) are read in callbacks.

.. kwargs::dash_flows.DashFlows

### Node components

Custom node types you can register and render inside a flow.

.. kwargs::dash_flows.DefaultNode

.. kwargs::dash_flows.GroupNode

### Edge components

.. kwargs::dash_flows.ButtonEdge

.. kwargs::dash_flows.FloatingEdge

