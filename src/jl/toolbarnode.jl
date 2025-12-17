# AUTO GENERATED FILE - DO NOT EDIT

export toolbarnode

"""
    toolbarnode(;kwargs...)

A ToolbarNode component.
ToolbarNode - Glass morphism styled node with a configurable toolbar
Keyword arguments:
- `data` (required): Node data configuration object. data has the following type: lists containing elements 'label', 'sublabel', 'toolbar', 'toolbarVisible', 'toolbarPosition', 'toolbarAlign', 'toolbarOffset', 'toolbarStyle', 'style', 'handleStyle', 'targetPosition', 'sourcePosition', 'showTargetHandle', 'showSourceHandle'.
Those elements have the following types:
  - `label` (Bool | Real | String | Dict | Array; optional): Primary content to display in the node
  - `sublabel` (String; optional): Secondary text displayed below the main label
  - `toolbar` (Bool | Real | String | Dict | Array; optional): Custom toolbar content - DashIconify or other components
  - `toolbarVisible` (Bool; optional): Whether the toolbar is visible (default: shows when selected)
  - `toolbarPosition` (a value equal to: 'top', 'bottom', 'left', 'right'; optional): Position of the toolbar relative to the node
  - `toolbarAlign` (a value equal to: 'start', 'center', 'end'; optional): Alignment of the toolbar ('start', 'center', 'end')
  - `toolbarOffset` (Real; optional): Offset distance of the toolbar from the node
  - `toolbarStyle` (Dict; optional): Custom CSS styles for the toolbar
  - `style` (Dict; optional): Custom CSS styles for the node container
  - `handleStyle` (Dict; optional): Custom CSS styles for connection handles
  - `targetPosition` (String; optional): Position for the target (input) handle
  - `sourcePosition` (String; optional): Position for the source (output) handle
  - `showTargetHandle` (Bool; optional): Whether to show the target handle (default: true)
  - `showSourceHandle` (Bool; optional): Whether to show the source handle (default: true)
- `isConnectable` (Bool; optional): Whether connections can be made to/from this node
- `selected` (Bool; optional): Whether the node is currently selected
"""
function toolbarnode(; kwargs...)
        available_props = Symbol[:data, :isConnectable, :selected]
        wild_props = Symbol[]
        return Component("toolbarnode", "ToolbarNode", "dash_flows", available_props, wild_props; kwargs...)
end

