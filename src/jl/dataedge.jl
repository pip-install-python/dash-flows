# AUTO GENERATED FILE - DO NOT EDIT

export dataedge

"""
    dataedge(;kwargs...)

A DataEdge component.
DataEdge - An edge that displays data from the source node
Useful for showing data flow between nodes
Keyword arguments:
- `id` (String; required)
- `data` (optional): . data has the following type: lists containing elements 'key', 'prefix', 'suffix', 'labelStyle'.
Those elements have the following types:
  - `key` (String; required): Key to read from source node's data
  - `prefix` (String; optional): Prefix to display before the value
  - `suffix` (String; optional): Suffix to display after the value
  - `labelStyle` (Dict; optional): Custom label styles
- `markerEnd` (Bool | Real | String | Dict | Array; optional)
- `markerStart` (Bool | Real | String | Dict | Array; optional)
- `selected` (Bool; optional)
- `source` (String; required)
- `sourcePosition` (String; optional)
- `sourceX` (Real; required)
- `sourceY` (Real; required)
- `style` (Dict; optional)
- `targetPosition` (String; optional)
- `targetX` (Real; required)
- `targetY` (Real; required)
"""
function dataedge(; kwargs...)
        available_props = Symbol[:id, :data, :markerEnd, :markerStart, :selected, :source, :sourcePosition, :sourceX, :sourceY, :style, :targetPosition, :targetX, :targetY]
        wild_props = Symbol[]
        return Component("dataedge", "DataEdge", "dash_flows", available_props, wild_props; kwargs...)
end

