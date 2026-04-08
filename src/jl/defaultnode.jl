# AUTO GENERATED FILE - DO NOT EDIT

export defaultnode

"""
    defaultnode(;kwargs...)

A DefaultNode component.
DefaultNode - Glass morphism styled node with source and target handles
Equivalent to React Flow's built-in 'default' node type

Uses CSS classes from glass-theme.css for styling, supporting:
- Light/dark mode via colorMode prop or Mantine color scheme
- Theme presets (glass, solid, minimal)
- Custom CSS variable overrides via theme prop
- Status indicators (initial, loading, success, error)
- Custom icons via DashIconify or any Dash component
Keyword arguments:
- `data` (required): Node data object containing label, styling, and handle configuration. data has the following type: lists containing elements 'label', 'title', 'sublabel', 'body', 'icon', 'iconColor', 'showIcon', 'layout', 'multiline', 'style', 'className', 'handleStyle', 'targetPosition', 'sourcePosition', 'status', 'loadingVariant', 'smartHandles'.
Those elements have the following types:
  - `label` (Bool | Real | String | Dict | Array; optional): Primary content to display in the node - string or Dash component
  - `title` (Bool | Real | String | Dict | Array; optional): Alias for label - use for clarity when also using body text
  - `sublabel` (String; optional): Secondary text displayed below the main label
  - `body` (Bool | Real | String | Dict | Array; optional): Body text displayed below title/sublabel
  - `icon` (Bool | Real | String | Dict | Array; optional): Custom icon - DashIconify component or any Dash component
  - `iconColor` (String; optional): Background color for the icon container
  - `showIcon` (Bool; optional): Show/hide icon (default: true if icon prop provided, false otherwise)
  - `layout` (a value equal to: 'stacked', 'horizontal'; optional): Layout mode: 'stacked' (vertical) or 'horizontal' (icon left, text right)
  - `multiline` (Bool; optional): Allow multiline text wrapping
  - `style` (Dict; optional): Custom CSS styles for the node container
  - `className` (String; optional): Additional CSS class name
  - `handleStyle` (Dict; optional): Custom CSS styles for connection handles
  - `targetPosition` (String; optional): Position for the target (input) handle: 'top', 'bottom', 'left', 'right'
  - `sourcePosition` (String; optional): Position for the source (output) handle: 'top', 'bottom', 'left', 'right'
  - `status` (a value equal to: 'initial', 'loading', 'success', 'error'; optional): Node status: 'initial', 'loading', 'success', 'error'
  - `loadingVariant` (a value equal to: 'border', 'overlay'; optional): Loading animation variant: 'border' or 'overlay'
  - `smartHandles` (Bool; optional): Enable smart handles mode - renders handles on all 4 sides for optimal edge routing
- `isConnectable` (Bool; optional): Whether connections can be made to/from this node
- `selected` (Bool; optional): Whether the node is currently selected
"""
function defaultnode(; kwargs...)
        available_props = Symbol[:data, :isConnectable, :selected]
        wild_props = Symbol[]
        return Component("defaultnode", "DefaultNode", "dash_flows", available_props, wild_props; kwargs...)
end

