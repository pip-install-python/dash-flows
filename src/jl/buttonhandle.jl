# AUTO GENERATED FILE - DO NOT EDIT

export buttonhandle

"""
    buttonhandle(;kwargs...)
    buttonhandle(children::Any;kwargs...)
    buttonhandle(children_maker::Function;kwargs...)


A ButtonHandle component.
ButtonHandle - A handle that can also function as a button
Useful for triggering actions when clicking on a connection point
Keyword arguments:
- `children` (a list of or a singular dash component, string or number; optional): Child content for the button
- `id` (String; optional): Unique identifier for the handle
- `buttonClassName` (String; optional): CSS class for the button
- `buttonContent` (a list of or a singular dash component, string or number; optional): Content to display in the button
- `buttonStyle` (Dict; optional): Inline styles for the button
- `className` (String; optional): CSS class for the handle
- `isConnectable` (Bool; optional): Whether the handle can connect to other nodes
- `position` (a value equal to: 'top', 'bottom', 'left', 'right'; optional): Position of the handle on the node
- `showButton` (Bool; optional): Whether to show the button (default: false)
- `style` (Dict; optional): Inline styles for the handle
- `type` (a value equal to: 'source', 'target'; required): Type of handle - source or target
"""
function buttonhandle(; kwargs...)
        available_props = Symbol[:children, :id, :buttonClassName, :buttonContent, :buttonStyle, :className, :isConnectable, :position, :showButton, :style, :type]
        wild_props = Symbol[]
        return Component("buttonhandle", "ButtonHandle", "dash_flows", available_props, wild_props; kwargs...)
end

buttonhandle(children::Any; kwargs...) = buttonhandle(;kwargs..., children = children)
buttonhandle(children_maker::Function; kwargs...) = buttonhandle(children_maker(); kwargs...)

