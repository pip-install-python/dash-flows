# AUTO GENERATED FILE - DO NOT EDIT

export nodetooltip

"""
    nodetooltip(;kwargs...)
    nodetooltip(children::Any;kwargs...)
    nodetooltip(children_maker::Function;kwargs...)


A NodeTooltip component.
NodeTooltip - A wrapper that displays a tooltip when hovered
Built on top of React Flow's NodeToolbar component
Keyword arguments:
- `children` (a list of or a singular dash component, string or number; optional): The node content
- `className` (String; optional): CSS class for the container
- `offset` (Real; optional): Offset from the node in pixels
- `position` (a value equal to: 'top', 'bottom', 'left', 'right'; optional): Position of the tooltip relative to the node
- `showOnHover` (Bool; optional): Show tooltip only on hover (default: true)
- `style` (Dict; optional): Inline styles for the container
- `tooltipClassName` (String; optional): CSS class for the tooltip
- `tooltipContent` (a list of or a singular dash component, string or number; optional): Content to display in the tooltip
- `tooltipStyle` (Dict; optional): Inline styles for the tooltip
"""
function nodetooltip(; kwargs...)
        available_props = Symbol[:children, :className, :offset, :position, :showOnHover, :style, :tooltipClassName, :tooltipContent, :tooltipStyle]
        wild_props = Symbol[]
        return Component("nodetooltip", "NodeTooltip", "dash_flows", available_props, wild_props; kwargs...)
end

nodetooltip(children::Any; kwargs...) = nodetooltip(;kwargs..., children = children)
nodetooltip(children_maker::Function; kwargs...) = nodetooltip(children_maker(); kwargs...)

