# AUTO GENERATED FILE - DO NOT EDIT

export buttonedge

"""
    buttonedge(;kwargs...)

A ButtonEdge component.
ButtonEdge - Glass morphism styled edge with an interactive button
Keyword arguments:
- `id` (String; required)
- `data` (optional): . data has the following type: lists containing elements 'label', 'showButton', 'buttonLabel', 'buttonStyle', 'buttonTitle', 'onButtonClick'.
Those elements have the following types:
  - `label` (Bool | Real | String | Dict | Array; optional)
  - `showButton` (Bool; optional)
  - `buttonLabel` (String; optional)
  - `buttonStyle` (Dict; optional)
  - `buttonTitle` (String; optional)
  - `onButtonClick` (optional)
- `label` (Bool | Real | String | Dict | Array; optional)
- `labelStyle` (Dict; optional)
- `markerEnd` (Bool | Real | String | Dict | Array; optional)
- `markerStart` (Bool | Real | String | Dict | Array; optional)
- `selected` (Bool; optional)
- `sourcePosition` (String; optional)
- `sourceX` (Real; required)
- `sourceY` (Real; required)
- `style` (Dict; optional)
- `targetPosition` (String; optional)
- `targetX` (Real; required)
- `targetY` (Real; required)
"""
function buttonedge(; kwargs...)
        available_props = Symbol[:id, :data, :label, :labelStyle, :markerEnd, :markerStart, :selected, :sourcePosition, :sourceX, :sourceY, :style, :targetPosition, :targetX, :targetY]
        wild_props = Symbol[]
        return Component("buttonedge", "ButtonEdge", "dash_flows", available_props, wild_props; kwargs...)
end

