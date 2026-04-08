# AUTO GENERATED FILE - DO NOT EDIT

export buttonedge

"""
    buttonedge(;kwargs...)

A ButtonEdge component.
ButtonEdge - Glass morphism styled edge with an interactive button and optional toolbar
Keyword arguments:
- `id` (String; required): Unique identifier for the edge
- `data` (optional): Configuration data for the button edge. data has the following type: lists containing elements 'label', 'showButton', 'buttonLabel', 'buttonStyle', 'buttonTitle', 'onButtonClick', 'showToolbar', 'toolbarStyle'.
Those elements have the following types:
  - `label` (Bool | Real | String | Dict | Array; optional): Label text to display next to the button
  - `showButton` (Bool; optional): Whether to show the button (default: true)
  - `buttonLabel` (String; optional): Text/symbol to display on the button (default: '×')
  - `buttonStyle` (Dict; optional): Custom CSS styles for the button
  - `buttonTitle` (String; optional): Tooltip title for the button
  - `onButtonClick` (optional): Callback function when button is clicked
  - `showToolbar` (Bool; optional): Show glass morphism toolbar when edge is selected
  - `toolbarStyle` (Dict; optional): Custom CSS styles for the toolbar container
- `label` (Bool | Real | String | Dict | Array; optional): Label text to display on the edge
- `labelStyle` (Dict; optional): Custom CSS styles for the label
- `markerEnd` (Bool | Real | String | Dict | Array; optional): Marker configuration for the edge end
- `markerStart` (Bool | Real | String | Dict | Array; optional): Marker configuration for the edge start
- `selected` (Bool; optional): Whether the edge is currently selected
- `sourcePosition` (String; optional): Position of the source handle ('top', 'bottom', 'left', 'right')
- `sourceX` (Real; required): X coordinate of the edge source
- `sourceY` (Real; required): Y coordinate of the edge source
- `style` (Dict; optional): Custom CSS styles for the edge path
- `targetPosition` (String; optional): Position of the target handle ('top', 'bottom', 'left', 'right')
- `targetX` (Real; required): X coordinate of the edge target
- `targetY` (Real; required): Y coordinate of the edge target
"""
function buttonedge(; kwargs...)
        available_props = Symbol[:id, :data, :label, :labelStyle, :markerEnd, :markerStart, :selected, :sourcePosition, :sourceX, :sourceY, :style, :targetPosition, :targetX, :targetY]
        wild_props = Symbol[]
        return Component("buttonedge", "ButtonEdge", "dash_flows", available_props, wild_props; kwargs...)
end

