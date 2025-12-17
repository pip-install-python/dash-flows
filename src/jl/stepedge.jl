# AUTO GENERATED FILE - DO NOT EDIT

export stepedge

"""
    stepedge(;kwargs...)

A StepEdge component.
StepEdge - Glass morphism styled stepped edge with sharp corners
Keyword arguments:
- `id` (String; required): Unique identifier for the edge
- `data` (Dict; optional): Additional data passed to the edge
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
function stepedge(; kwargs...)
        available_props = Symbol[:id, :data, :label, :labelStyle, :markerEnd, :markerStart, :selected, :sourcePosition, :sourceX, :sourceY, :style, :targetPosition, :targetX, :targetY]
        wild_props = Symbol[]
        return Component("stepedge", "StepEdge", "dash_flows", available_props, wild_props; kwargs...)
end

