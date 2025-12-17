# AUTO GENERATED FILE - DO NOT EDIT

export dataedge

"""
    dataedge(;kwargs...)

A DataEdge component.
DataEdge - An edge that displays data from the source node
Useful for showing data flow between nodes
Keyword arguments:
- `id` (String; required): Unique identifier for the edge
- `data` (optional): Configuration data for the data edge. data has the following type: lists containing elements 'key', 'prefix', 'suffix', 'labelStyle'.
Those elements have the following types:
  - `key` (String; required): Key to read from source node's data
  - `prefix` (String; optional): Prefix to display before the value
  - `suffix` (String; optional): Suffix to display after the value
  - `labelStyle` (Dict; optional): Custom label styles
- `markerEnd` (Bool | Real | String | Dict | Array; optional): Marker configuration for the edge end
- `markerStart` (Bool | Real | String | Dict | Array; optional): Marker configuration for the edge start
- `selected` (Bool; optional): Whether the edge is currently selected
- `source` (String; required): ID of the source node to read data from
- `sourcePosition` (String; optional): Position of the source handle ('top', 'bottom', 'left', 'right')
- `sourceX` (Real; required): X coordinate of the edge source
- `sourceY` (Real; required): Y coordinate of the edge source
- `style` (Dict; optional): Custom CSS styles for the edge path
- `targetPosition` (String; optional): Position of the target handle ('top', 'bottom', 'left', 'right')
- `targetX` (Real; required): X coordinate of the edge target
- `targetY` (Real; required): Y coordinate of the edge target
"""
function dataedge(; kwargs...)
        available_props = Symbol[:id, :data, :markerEnd, :markerStart, :selected, :source, :sourcePosition, :sourceX, :sourceY, :style, :targetPosition, :targetX, :targetY]
        wild_props = Symbol[]
        return Component("dataedge", "DataEdge", "dash_flows", available_props, wild_props; kwargs...)
end

