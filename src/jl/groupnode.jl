# AUTO GENERATED FILE - DO NOT EDIT

export groupnode

"""
    groupnode(;kwargs...)

A GroupNode component.
GroupNode - A simple labeled group container for child nodes

This follows the React Flow pattern for group nodes:
- The node's width/height is controlled via the style prop on the node definition
- Child nodes use parentId to reference this node
- Child nodes can use extent: 'parent' to stay within bounds

Unlike standard nodes, group nodes are rendered as simple containers
that React Flow manages for parent-child relationships.
Keyword arguments:
- `data` (optional): Node data object containing label, icon, and styling options. data has the following type: lists containing elements 'label', 'icon', 'labelStyle', 'resizable', 'minWidth', 'minHeight'.
Those elements have the following types:
  - `label` (Bool | Real | String | Dict | Array; optional): Label content for the group - displayed in top-left corner
  - `icon` (Bool | Real | String | Dict | Array; optional): Icon element to display next to the label
  - `labelStyle` (Dict; optional): Custom CSS styles for the label element
  - `resizable` (Bool; optional): Whether the group can be resized (default: true)
  - `minWidth` (Real; optional): Minimum width constraint for resizing
  - `minHeight` (Real; optional): Minimum height constraint for resizing
- `selected` (Bool; optional): Whether the group is currently selected
"""
function groupnode(; kwargs...)
        available_props = Symbol[:data, :selected]
        wild_props = Symbol[]
        return Component("groupnode", "GroupNode", "dash_flows", available_props, wild_props; kwargs...)
end

