# AUTO GENERATED FILE - DO NOT EDIT

export animatedsvgedge

"""
    animatedsvgedge(;kwargs...)

An AnimatedSvgEdge component.
AnimatedSvgEdge - An edge that animates a custom SVG element along the path
Useful for showing data flow direction or active connections
Keyword arguments:
- `id` (String; required)
- `data` (optional): . data has the following type: lists containing elements 'duration', 'shape', 'size', 'color', 'count', 'reverse'.
Those elements have the following types:
  - `duration` (Real; optional): Animation duration in seconds
  - `shape` (a value equal to: 'circle', 'rect', 'arrow', 'pulse'; optional): Shape to animate: 'circle', 'rect', 'arrow', 'pulse'
  - `size` (Real; optional): Size of the animated shape
  - `color` (String; optional): Color of the animated shape
  - `count` (Real; optional): Number of shapes to animate along the path
  - `reverse` (Bool; optional): Reverse the animation direction
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
function animatedsvgedge(; kwargs...)
        available_props = Symbol[:id, :data, :markerEnd, :markerStart, :selected, :sourcePosition, :sourceX, :sourceY, :style, :targetPosition, :targetX, :targetY]
        wild_props = Symbol[]
        return Component("animatedsvgedge", "AnimatedSvgEdge", "dash_flows", available_props, wild_props; kwargs...)
end

