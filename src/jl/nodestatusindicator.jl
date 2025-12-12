# AUTO GENERATED FILE - DO NOT EDIT

export nodestatusindicator

"""
    nodestatusindicator(;kwargs...)
    nodestatusindicator(children::Any;kwargs...)
    nodestatusindicator(children_maker::Function;kwargs...)


A NodeStatusIndicator component.
NodeStatusIndicator - A wrapper component that shows status indicators around nodes
Status can be: "initial", "loading", "success", "error"
Loading variants: "border" (spinning border) or "overlay" (full overlay with spinner)
Keyword arguments:
- `children` (a list of or a singular dash component, string or number; optional): The node content to wrap
- `className` (String; optional): Additional CSS class name
- `loadingVariant` (a value equal to: 'border', 'overlay'; optional): Loading animation variant - "border" shows spinning border, "overlay" shows full overlay
- `status` (a value equal to: 'initial', 'loading', 'success', 'error'; optional): The current status of the node
- `style` (Dict; optional): Custom inline styles
"""
function nodestatusindicator(; kwargs...)
        available_props = Symbol[:children, :className, :loadingVariant, :status, :style]
        wild_props = Symbol[]
        return Component("nodestatusindicator", "NodeStatusIndicator", "dash_flows", available_props, wild_props; kwargs...)
end

nodestatusindicator(children::Any; kwargs...) = nodestatusindicator(;kwargs..., children = children)
nodestatusindicator(children_maker::Function; kwargs...) = nodestatusindicator(children_maker(); kwargs...)

