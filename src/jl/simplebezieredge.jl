# AUTO GENERATED FILE - DO NOT EDIT

export simplebezieredge

"""
    simplebezieredge(;kwargs...)

A SimpleBezierEdge component.
SimpleBezierEdge - Glass morphism styled simple bezier curve edge
Keyword arguments:
- `id` (String; required)
- `data` (Dict; optional)
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
function simplebezieredge(; kwargs...)
        available_props = Symbol[:id, :data, :label, :labelStyle, :markerEnd, :markerStart, :selected, :sourcePosition, :sourceX, :sourceY, :style, :targetPosition, :targetX, :targetY]
        wild_props = Symbol[]
        return Component("simplebezieredge", "SimpleBezierEdge", "dash_flows", available_props, wild_props; kwargs...)
end

