# AUTO GENERATED FILE - DO NOT EDIT

export straightedge

"""
    straightedge(;kwargs...)

A StraightEdge component.
StraightEdge - Glass morphism styled straight line edge
Keyword arguments:
- `id` (String; required)
- `data` (Dict; optional)
- `label` (Bool | Real | String | Dict | Array; optional)
- `labelStyle` (Dict; optional)
- `markerEnd` (Bool | Real | String | Dict | Array; optional)
- `markerStart` (Bool | Real | String | Dict | Array; optional)
- `selected` (Bool; optional)
- `sourceX` (Real; required)
- `sourceY` (Real; required)
- `style` (Dict; optional)
- `targetX` (Real; required)
- `targetY` (Real; required)
"""
function straightedge(; kwargs...)
        available_props = Symbol[:id, :data, :label, :labelStyle, :markerEnd, :markerStart, :selected, :sourceX, :sourceY, :style, :targetX, :targetY]
        wild_props = Symbol[]
        return Component("straightedge", "StraightEdge", "dash_flows", available_props, wild_props; kwargs...)
end

