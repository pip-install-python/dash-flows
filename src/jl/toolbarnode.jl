# AUTO GENERATED FILE - DO NOT EDIT

export toolbarnode

"""
    toolbarnode(;kwargs...)

A ToolbarNode component.
ToolbarNode - Glass morphism styled node with a configurable toolbar
Keyword arguments:
- `data` (required): . data has the following type: lists containing elements 'label', 'sublabel', 'toolbar', 'toolbarVisible', 'toolbarPosition', 'toolbarAlign', 'toolbarOffset', 'toolbarStyle', 'style', 'handleStyle', 'targetPosition', 'sourcePosition', 'showTargetHandle', 'showSourceHandle'.
Those elements have the following types:
  - `label` (Bool | Real | String | Dict | Array; optional)
  - `sublabel` (String; optional)
  - `toolbar` (Bool | Real | String | Dict | Array; optional)
  - `toolbarVisible` (Bool; optional)
  - `toolbarPosition` (a value equal to: 'top', 'bottom', 'left', 'right'; optional)
  - `toolbarAlign` (a value equal to: 'start', 'center', 'end'; optional)
  - `toolbarOffset` (Real; optional)
  - `toolbarStyle` (Dict; optional)
  - `style` (Dict; optional)
  - `handleStyle` (Dict; optional)
  - `targetPosition` (String; optional)
  - `sourcePosition` (String; optional)
  - `showTargetHandle` (Bool; optional)
  - `showSourceHandle` (Bool; optional)
- `isConnectable` (Bool; optional)
- `selected` (Bool; optional)
"""
function toolbarnode(; kwargs...)
        available_props = Symbol[:data, :isConnectable, :selected]
        wild_props = Symbol[]
        return Component("toolbarnode", "ToolbarNode", "dash_flows", available_props, wild_props; kwargs...)
end

