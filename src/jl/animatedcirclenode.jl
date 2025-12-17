# AUTO GENERATED FILE - DO NOT EDIT

export animatedcirclenode

"""
    animatedcirclenode(;kwargs...)

An AnimatedCircleNode component.
AnimatedCircleNode - A circular node designed for use with animated edges.
Features a distinctive pink circular design that works well with AnimatedNodeEdge
to create animated dot effects along connections.
Keyword arguments:
- `data` (required): Node data object containing the label content. data has the following type: lists containing elements 'label'.
Those elements have the following types:
  - `label` (Bool | Real | String | Dict | Array; optional): Content to display inside the circular node - can be string or React element
"""
function animatedcirclenode(; kwargs...)
        available_props = Symbol[:data]
        wild_props = Symbol[]
        return Component("animatedcirclenode", "AnimatedCircleNode", "dash_flows", available_props, wild_props; kwargs...)
end

