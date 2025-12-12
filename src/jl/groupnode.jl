# AUTO GENERATED FILE - DO NOT EDIT

export groupnode

"""
    groupnode(;kwargs...)

A GroupNode component.
GroupNode - Glass morphism styled container node that can hold other nodes
Child nodes should have parentId set to this node's ID

IMPORTANT: Group nodes should have zIndex set lower than child nodes
in the node definition to ensure proper layering.
Keyword arguments:
- `data` (optional): Node data object containing label, icon, and styling options. data has the following type: lists containing elements 'label', 'icon', 'style', 'labelStyle', 'resizable', 'minWidth', 'minHeight'.
Those elements have the following types:
  - `label` (Bool | Real | String | Dict | Array; optional): Label content for the group - displayed above the group container
  - `icon` (Bool | Real | String | Dict | Array; optional): Icon element to display next to the label
  - `style` (Dict; optional): Custom CSS styles for the group container
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

