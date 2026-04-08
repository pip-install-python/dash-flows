# AUTO GENERATED FILE - DO NOT EDIT

export resizablenode

"""
    resizablenode(;kwargs...)

A ResizableNode component.
ResizableNode - A node that can be resized by the user

This node supports embedding Dash components that will resize
along with the node container. The node receives width/height
from React Flow when resized.
Keyword arguments:
- `data` (required): Node data object containing label, handles, and styling options. data has the following type: lists containing elements 'label', 'handles', 'style', 'initialWidth', 'initialHeight', 'minWidth', 'minHeight', 'maxWidth', 'maxHeight', 'keepAspectRatio', 'padding', 'alignItems', 'justifyContent', 'flexDirection'.
Those elements have the following types:
  - `label` (Bool | Real | String | Dict | Array; optional): Content to render inside the node - can be string, React element, or Dash component
  - `handles` (required): Array of connection handles for this node. handles has the following type: Array of lists containing elements 'id', 'type', 'position', 'style', 'isConnectable', 'isConnectableStart', 'isConnectableEnd', 'onConnect', 'isValidConnection'.
Those elements have the following types:
  - `id` (String; required): Unique identifier for the handle
  - `type` (String; required): Handle type: 'source' or 'target'
  - `position` (String; required): Handle position: 'top', 'bottom', 'left', or 'right'
  - `style` (Dict; optional): Custom CSS styles for the handle
  - `isConnectable` (Bool; optional): Whether the handle can be connected
  - `isConnectableStart` (Bool; optional): Whether connections can start from this handle
  - `isConnectableEnd` (Bool; optional): Whether connections can end at this handle
  - `onConnect` (optional): Callback when a connection is made
  - `isValidConnection` (optional): Validation function for connectionss
  - `style` (Dict; optional): Custom CSS styles for the node container
  - `initialWidth` (Real; optional): Initial width of the node before resize
  - `initialHeight` (Real; optional): Initial height of the node before resize
  - `minWidth` (Real; optional): Minimum width constraint for resizing
  - `minHeight` (Real; optional): Minimum height constraint for resizing
  - `maxWidth` (Real; optional): Maximum width constraint for resizing
  - `maxHeight` (Real; optional): Maximum height constraint for resizing
  - `keepAspectRatio` (Bool; optional): Maintain aspect ratio when resizing
  - `padding` (Real; optional): Padding inside the node content area
  - `alignItems` (String; optional): Flexbox align-items value for content
  - `justifyContent` (String; optional): Flexbox justify-content value for content
  - `flexDirection` (String; optional): Flexbox flex-direction value for content
- `height` (Real; optional): Current height of the node (set by React Flow during resize)
- `selected` (Bool; optional): Whether the node is currently selected
- `width` (Real; optional): Current width of the node (set by React Flow during resize)
"""
function resizablenode(; kwargs...)
        available_props = Symbol[:data, :height, :selected, :width]
        wild_props = Symbol[]
        return Component("resizablenode", "ResizableNode", "dash_flows", available_props, wild_props; kwargs...)
end

