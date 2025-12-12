# AUTO GENERATED FILE - DO NOT EDIT

export inputnode

"""
    inputnode(;kwargs...)

An InputNode component.
InputNode - Glass morphism styled node with only a source handle (no incoming connections)
Features a green accent bar at the top

Uses CSS classes from glass-theme.css for styling, supporting:
- Light/dark mode via colorMode prop or Mantine color scheme
- Theme presets (glass, solid, minimal)
- Custom CSS variable overrides via theme prop
- Custom icons via DashIconify or any Dash component
Keyword arguments:
- `data` (required): . data has the following type: lists containing elements 'label', 'title', 'sublabel', 'body', 'icon', 'iconColor', 'showIcon', 'layout', 'multiline', 'style', 'className', 'handleStyle', 'sourcePosition', 'status', 'loadingVariant'.
Those elements have the following types:
  - `label` (Bool | Real | String | Dict | Array; optional): Primary content to display in the node (string or Dash component)
  - `title` (Bool | Real | String | Dict | Array; optional): Alias for label - use for clarity when also using body text
  - `sublabel` (String; optional): Secondary text displayed below the main label
  - `body` (Bool | Real | String | Dict | Array; optional): Body text displayed below title/sublabel
  - `icon` (Bool | Real | String | Dict | Array; optional): Custom icon - DashIconify component or any Dash component
  - `iconColor` (String; optional): Background color for the icon container
  - `showIcon` (Bool; optional): Show/hide the input icon (default: true)
  - `layout` (a value equal to: 'stacked', 'horizontal'; optional): Layout mode: 'stacked' (vertical) or 'horizontal' (icon left, text right)
  - `multiline` (Bool; optional): Allow multiline text wrapping
  - `style` (Dict; optional): Custom CSS styles for the node container
  - `className` (String; optional): Additional CSS class name
  - `handleStyle` (Dict; optional): Custom CSS styles for connection handles
  - `sourcePosition` (String; optional): Position for the source (output) handle
  - `status` (a value equal to: 'initial', 'loading', 'success', 'error'; optional): Node status: 'initial', 'loading', 'success', 'error'
  - `loadingVariant` (a value equal to: 'border', 'overlay'; optional): Loading animation variant: 'border' or 'overlay'
- `isConnectable` (Bool; optional): Whether connections can be made from this node
- `selected` (Bool; optional): Whether the node is currently selected
"""
function inputnode(; kwargs...)
        available_props = Symbol[:data, :isConnectable, :selected]
        wild_props = Symbol[]
        return Component("inputnode", "InputNode", "dash_flows", available_props, wild_props; kwargs...)
end

