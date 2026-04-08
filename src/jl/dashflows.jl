# AUTO GENERATED FILE - DO NOT EDIT

export dashflows

"""
    dashflows(;kwargs...)

A DashFlows component.
DashFlows - A React Flow-based node graph component for Dash applications.
Provides interactive node-based workflow visualization with support for
custom node types, edge types, glass morphism styling, and extensive
callback integration for Python-based interactivity.
Keyword arguments:
- `id` (String; optional): The ID used to identify this component in Dash callbacks.
- `addNodeOnEdgeDrop` (Bool; optional): When true, dragging a connection from a handle and dropping on empty canvas
creates a new default node at that position and connects it.
- `animateLayout` (Bool; optional): Enable smooth animated transitions when applying ELK layout.
Nodes interpolate from current to target positions with an ease-out curve.
- `animateLayoutDuration` (Real; optional): Duration of layout animation in milliseconds (default: 300)
- `ariaLabelConfig` (Dict; optional): ARIA label configuration for accessibility. Customize labels for screen readers.
Keys: nodes, edges, controls, minimap. Values are label strings.
- `autoPanOnConnect` (Bool; optional): Auto-pan viewport when making a new connection near edges
- `autoPanOnNodeDrag` (Bool; optional): Auto-pan viewport when dragging a node near edges
- `autoPanOnNodeFocus` (Bool; optional): Auto-pan the viewport when focusing a node via keyboard (Tab key).
- `autoPanSpeed` (Real; optional): Speed of auto-panning (default: 15)
- `backgroundColor` (String; optional): Color of the background pattern
- `backgroundGap` (Real | Array of Reals; optional): Gap between background pattern elements
- `backgroundSize` (Real; optional): Size of background pattern elements
- `backgroundVariant` (a value equal to: 'dots', 'lines', 'cross'; optional): Background pattern type: 'dots', 'lines', 'cross'
- `className` (String; optional): CSS class name for the container div
- `clickedEdge` (optional): The edge that was clicked. clickedEdge has the following type: lists containing elements 'id', 'source', 'target'.
Those elements have the following types:
  - `id` (String; optional)
  - `source` (String; optional)
  - `target` (String; optional)
- `clickedNode` (optional): The node that was clicked. clickedNode has the following type: lists containing elements 'id', 'data', 'position'.
Those elements have the following types:
  - `id` (String; optional)
  - `data` (Dict; optional)
  - `position` (Dict; optional)
- `clipboard` (optional): Internal clipboard containing copied nodes and edges.
Populated by copyAction, consumed by pasteAction.. clipboard has the following type: lists containing elements 'nodes', 'edges', 'timestamp'.
Those elements have the following types:
  - `nodes` (Array; optional)
  - `edges` (Array; optional)
  - `timestamp` (Real; optional)
- `collapsedGroups` (Array of Strings; optional): List of currently collapsed group node IDs (read-only output).
- `colorMode` (a value equal to: 'light', 'dark', 'system'; optional): Color mode: 'light', 'dark', or 'system'
- `colorScheme` (a value equal to: 'default', 'ocean', 'forest', 'sunset', 'midnight', 'rose'; optional): Color scheme preset for node and edge colors.
Works in combination with themePreset for full customization.
Each scheme includes light and dark mode variants.
- default: Neutral blue/purple (default)
- ocean: Blues and teals
- forest: Greens and browns
- sunset: Oranges and reds
- midnight: Deep blues and purples
- rose: Pinks and reds
- `computeAction` (optional): Trigger a graph computation. Set to { action: 'compute' } to perform
topological sort and emit traversal order with input mappings.
Will be reset to null after execution.. computeAction has the following type: lists containing elements 'action', 'nodeId', 'inputData'.
Those elements have the following types:
  - `action` (a value equal to: 'compute', 'computeNode'; optional)
  - `nodeId` (String; optional)
  - `inputData` (Dict; optional)
- `computeResult` (optional): Result of the last computation. Contains traversalOrder (array of node IDs
in topological order) and nodeInputs (map of nodeId to input details).. computeResult has the following type: lists containing elements 'traversalOrder', 'nodeInputs', 'timestamp'.
Those elements have the following types:
  - `traversalOrder` (Array of Strings; optional)
  - `nodeInputs` (Dict; optional)
  - `timestamp` (Real; optional)
- `connectOnClick` (Bool; optional): Enable click-based connection mode (click source then target)
- `connectionDragThreshold` (Real; optional): Minimum drag distance in pixels before a connection line appears.
Useful to prevent accidental connections. Default is 0 (immediate).
- `connectionLineStyle` (Dict; optional): Style for the connection line while dragging
- `connectionLineType` (a value equal to: 'bezier', 'straight', 'step', 'smoothstep', 'simplebezier'; optional): Type of connection line: 'bezier', 'straight', 'step', 'smoothstep', 'simplebezier'
- `connectionMode` (a value equal to: 'strict', 'loose'; optional): Connection mode: 'strict' (same handle type) or 'loose' (any handle)
- `connectionRadius` (Real; optional): Radius for connection drop detection (default: 20)
- `connectionRules` (optional): Rules for validating connections. connectionRules has the following type: lists containing elements 'allowSelfConnection', 'allowDuplicateConnections', 'validSourceTypes', 'validTargetTypes'.
Those elements have the following types:
  - `allowSelfConnection` (Bool; optional)
  - `allowDuplicateConnections` (Bool; optional)
  - `validSourceTypes` (Array of Strings; optional)
  - `validTargetTypes` (Array of Strings; optional)
- `connectionStartHandle` (optional): Current connection being created. connectionStartHandle has the following type: lists containing elements 'nodeId', 'handleId', 'handleType'.
Those elements have the following types:
  - `nodeId` (String; optional)
  - `handleId` (String; optional)
  - `handleType` (String; optional)
- `contextMenuEdge` (optional): Context menu info for an edge. contextMenuEdge has the following type: lists containing elements 'id', 'source', 'target', 'clientX', 'clientY'.
Those elements have the following types:
  - `id` (String; optional)
  - `source` (String; optional)
  - `target` (String; optional)
  - `clientX` (Real; optional)
  - `clientY` (Real; optional)
- `contextMenuNode` (optional): Context menu info for a node. contextMenuNode has the following type: lists containing elements 'id', 'data', 'position', 'clientX', 'clientY'.
Those elements have the following types:
  - `id` (String; optional)
  - `data` (Dict; optional)
  - `position` (Dict; optional)
  - `clientX` (Real; optional)
  - `clientY` (Real; optional)
- `controlsPosition` (a value equal to: 'top-left', 'top-right', 'bottom-left', 'bottom-right', 'top-center', 'bottom-center'; optional): Position of controls panel
- `controlsShowFitView` (Bool; optional): Show fit-view button in controls
- `controlsShowInteractive` (Bool; optional): Show interactive toggle in controls
- `controlsShowZoom` (Bool; optional): Show zoom buttons in controls
- `copyAction` (Bool; optional): Trigger to copy selected nodes and edges to clipboard.
Set to true to copy. Will be reset to false after copying.
If nothing is selected, copies all nodes and their connecting edges.
- `defaultEdgeOptions` (optional): Default options applied to all new edges. defaultEdgeOptions has the following type: lists containing elements 'type', 'style', 'animated', 'markerStart', 'markerEnd'.
Those elements have the following types:
  - `type` (String; optional)
  - `style` (Dict; optional)
  - `animated` (Bool; optional)
  - `markerStart` (Dict; optional)
  - `markerEnd` (Dict; optional)
- `defaultMarkerColor` (String; optional): Default color for edge markers
- `defaultViewport` (optional): The initial viewport position and zoom level. defaultViewport has the following type: lists containing elements 'x', 'y', 'zoom'.
Those elements have the following types:
  - `x` (Real; optional)
  - `y` (Real; optional)
  - `zoom` (Real; optional)
- `deleteElementsAction` (optional): Delete specific nodes and/or edges by ID. Routes through
reactFlowInstance.deleteElements() so undo/redo middleware can capture
the change. Set to { nodeIds: [...], edgeIds: [...] }; auto-resets to null.. deleteElementsAction has the following type: lists containing elements 'nodeIds', 'edgeIds'.
Those elements have the following types:
  - `nodeIds` (Array of Strings; optional): IDs of nodes to delete (connected edges are also removed)
  - `edgeIds` (Array of Strings; optional): IDs of edges to delete
- `deleteKeyCode` (String; optional): Key code for deleting selected elements (default: 'Backspace', null to disable)
- `deletedEdges` (Array of Strings; optional): IDs of recently deleted edges
- `deletedNodes` (Array of Strings; optional): IDs of recently deleted nodes
- `disableKeyboardA11y` (Bool; optional): Disable keyboard accessibility features
- `doubleClickedEdge` (optional): The edge that was double-clicked. doubleClickedEdge has the following type: lists containing elements 'id', 'source', 'target'.
Those elements have the following types:
  - `id` (String; optional)
  - `source` (String; optional)
  - `target` (String; optional)
- `doubleClickedNode` (optional): The node that was double-clicked. doubleClickedNode has the following type: lists containing elements 'id', 'data', 'position'.
Those elements have the following types:
  - `id` (String; optional)
  - `data` (Dict; optional)
  - `position` (Dict; optional)
- `downloadImage` (optional): Trigger to download the flow as an image.
Set to a config object to initiate download. Will be reset to null after download.

Config options:
- format: 'png' | 'svg' | 'jpeg' (default: 'png')
- filename: string (default: 'flow')
- quality: number 0-1 (default: 0.95, for jpeg only)
- backgroundColor: string (default: '#ffffff')
- pixelRatio: number (default: 2, for higher resolution). downloadImage has the following type: lists containing elements 'format', 'filename', 'quality', 'backgroundColor', 'pixelRatio'.
Those elements have the following types:
  - `format` (a value equal to: 'png', 'svg', 'jpeg', 'jpg'; optional)
  - `filename` (String; optional)
  - `quality` (Real; optional)
  - `backgroundColor` (String; optional)
  - `pixelRatio` (Real; optional)
- `draggedNode` (optional): The node being dragged. draggedNode has the following type: lists containing elements 'id', 'isDragging', 'startPosition', 'currentPosition', 'endPosition'.
Those elements have the following types:
  - `id` (String; optional)
  - `isDragging` (Bool; optional)
  - `startPosition` (Dict; optional)
  - `currentPosition` (Dict; optional)
  - `endPosition` (Dict; optional)
- `droppedNode` (optional): Node data from a drop event (drag and drop from external source).
Contains the type, position, and data of the dropped item.
Use this in a callback to create a new node at the drop position.. droppedNode has the following type: lists containing elements 'type', 'position', 'data', 'clientX', 'clientY', 'timestamp'.
Those elements have the following types:
  - `type` (String; optional)
  - `position` (optional): . position has the following type: lists containing elements 'x', 'y'.
Those elements have the following types:
  - `x` (Real; optional)
  - `y` (Real; optional)
  - `data` (Dict; optional)
  - `clientX` (Real; optional)
  - `clientY` (Real; optional)
  - `timestamp` (Real; optional)
- `edgeDroppedNode` (optional): Info about the node created by dropping an edge on empty canvas.
Contains nodeId, position, sourceNodeId, sourceHandleId, handleType, timestamp.. edgeDroppedNode has the following type: lists containing elements 'nodeId', 'position', 'sourceNodeId', 'sourceHandleId', 'handleType', 'timestamp'.
Those elements have the following types:
  - `nodeId` (String; optional)
  - `position` (optional): . position has the following type: lists containing elements 'x', 'y'.
Those elements have the following types:
  - `x` (Real; optional)
  - `y` (Real; optional)
  - `sourceNodeId` (String; optional)
  - `sourceHandleId` (String; optional)
  - `handleType` (String; optional)
  - `timestamp` (Real; optional)
- `edges` (optional): Array of edges defining connections between nodes. edges has the following type: Array of lists containing elements 'id', 'source', 'target', 'sourceHandle', 'targetHandle', 'type', 'data', 'style', 'className', 'hidden', 'selected', 'animated', 'deletable', 'selectable', 'focusable', 'zIndex', 'ariaLabel', 'interactionWidth', 'label', 'labelStyle', 'labelShowBg', 'labelBgStyle', 'labelBgPadding', 'labelBgBorderRadius', 'markerStart', 'markerEnd'.
Those elements have the following types:
  - `id` (String; required)
  - `source` (String; required)
  - `target` (String; required)
  - `sourceHandle` (String; optional)
  - `targetHandle` (String; optional)
  - `type` (String; optional)
  - `data` (Dict; optional)
  - `style` (Dict; optional)
  - `className` (String; optional)
  - `hidden` (Bool; optional)
  - `selected` (Bool; optional)
  - `animated` (Bool; optional)
  - `deletable` (Bool; optional)
  - `selectable` (Bool; optional)
  - `focusable` (Bool; optional)
  - `zIndex` (Real; optional)
  - `ariaLabel` (String; optional)
  - `interactionWidth` (Real; optional)
  - `label` (String; optional)
  - `labelStyle` (Dict; optional)
  - `labelShowBg` (Bool; optional)
  - `labelBgStyle` (Dict; optional)
  - `labelBgPadding` (Array of Reals; optional)
  - `labelBgBorderRadius` (Real; optional)
  - `markerStart` (optional): . markerStart has the following type: String | lists containing elements 'type', 'color', 'width', 'height', 'markerUnits', 'orient', 'strokeWidth'.
Those elements have the following types:
  - `type` (String; required)
  - `color` (String; optional)
  - `width` (Real; optional)
  - `height` (Real; optional)
  - `markerUnits` (String; optional)
  - `orient` (String; optional)
  - `strokeWidth` (Real; optional)
  - `markerEnd` (optional): . markerEnd has the following type: String | lists containing elements 'type', 'color', 'width', 'height', 'markerUnits', 'orient', 'strokeWidth'.
Those elements have the following types:
  - `type` (String; required)
  - `color` (String; optional)
  - `width` (Real; optional)
  - `height` (Real; optional)
  - `markerUnits` (String; optional)
  - `orient` (String; optional)
  - `strokeWidth` (Real; optional)s
- `edgesFocusable` (Bool; optional): Enable/disable keyboard focus on edges
- `edgesReconnectable` (Bool; optional): Allow edges to be reconnected after creation
- `elementsSelectable` (Bool; optional): Enable/disable the ability to select elements
- `elevateEdgesOnSelect` (Bool; optional): Raise z-index of selected edges
- `elevateNodesOnSelect` (Bool; optional): Raise z-index of selected nodes
- `enableUndoRedo` (Bool; optional): Enable the undo/redo history system. When enabled, node and edge changes
(add, remove, position drag-stop) are recorded to a history stack.
- `exportFlowState` (Bool; optional): Trigger to export the current flow state. Set to true to export.
After export, this will be reset to false and flowState will be populated.
- `fitView` (Bool; optional): Automatically fit all nodes in view on initialization
- `fitViewOptions` (optional): Options for fitView behavior. fitViewOptions has the following type: lists containing elements 'padding', 'includeHiddenNodes', 'minZoom', 'maxZoom', 'duration', 'nodes'.
Those elements have the following types:
  - `padding` (Real; optional)
  - `includeHiddenNodes` (Bool; optional)
  - `minZoom` (Real; optional)
  - `maxZoom` (Real; optional)
  - `duration` (Real; optional)
  - `nodes` (optional): . nodes has the following type: Array of lists containing elements 'id'.
Those elements have the following types:
  - `id` (String; optional)s
- `flowState` (optional): The exported flow state as a serializable object containing nodes, edges, and viewport.
This is populated when exportFlowState is triggered.. flowState has the following type: lists containing elements 'nodes', 'edges', 'viewport'.
Those elements have the following types:
  - `nodes` (Array; optional)
  - `edges` (Array; optional)
  - `viewport` (optional): . viewport has the following type: lists containing elements 'x', 'y', 'zoom'.
Those elements have the following types:
  - `x` (Real; optional)
  - `y` (Real; optional)
  - `zoom` (Real; optional)
- `helperLineThreshold` (Real; optional): Distance in pixels within which helper lines snap and appear (default: 5)
- `helperLines` (Bool; optional): Enable visual alignment guides (helper lines) when dragging nodes.
Lines appear when a node aligns with another node's top/center/bottom or left/center/right.
- `hoveredEdge` (optional): The edge being hovered. hoveredEdge has the following type: lists containing elements 'id', 'source', 'target'.
Those elements have the following types:
  - `id` (String; optional)
  - `source` (String; optional)
  - `target` (String; optional)
- `hoveredNode` (optional): The node being hovered. hoveredNode has the following type: lists containing elements 'id', 'data'.
Those elements have the following types:
  - `id` (String; optional)
  - `data` (Dict; optional)
- `imageDownloaded` (optional): Information about the last successful image download.
Populated after a successful downloadImage operation.. imageDownloaded has the following type: lists containing elements 'filename', 'format', 'timestamp'.
Those elements have the following types:
  - `filename` (String; optional)
  - `format` (String; optional)
  - `timestamp` (Real; optional)
- `initialized` (Bool; optional): Whether the flow has been initialized
- `lastConnection` (optional): The last connection that was made. lastConnection has the following type: lists containing elements 'source', 'sourceHandle', 'target', 'targetHandle'.
Those elements have the following types:
  - `source` (String; optional)
  - `sourceHandle` (String; optional)
  - `target` (String; optional)
  - `targetHandle` (String; optional)
- `lastError` (optional): Last error that occurred. lastError has the following type: lists containing elements 'id', 'message', 'type', 'timestamp'.
Those elements have the following types:
  - `id` (String; optional)
  - `message` (String; optional)
  - `type` (String; optional)
  - `timestamp` (Real; optional)
- `layoutOptions` (String; optional): Layout options for arranging nodes using the ELK layout engine (JSON string)
- `maxZoom` (Real; optional): Maximum zoom level (default: 2)
- `minZoom` (Real; optional): Minimum zoom level (default: 0.5)
- `miniMapMaskColor` (String; optional): Color for the minimap mask (viewport indicator)
- `miniMapNodeBorderRadius` (Real; optional): Border radius for minimap nodes
- `miniMapNodeColor` (String; optional): Color function or string for minimap nodes
- `miniMapNodeStrokeColor` (String; optional): Stroke color for minimap nodes
- `miniMapPannable` (Bool; optional): Allow panning by dragging the minimap
- `miniMapPosition` (a value equal to: 'top-left', 'top-right', 'bottom-left', 'bottom-right'; optional): Position of the minimap
- `miniMapZoomable` (Bool; optional): Allow zooming via the minimap
- `multiSelectionKeyCode` (String; optional): Key code for adding to selection
- `noDragClassName` (String; optional): CSS class name that prevents dragging when applied to elements
- `noPanClassName` (String; optional): CSS class name that prevents panning when applied to elements
- `noWheelClassName` (String; optional): CSS class name that prevents wheel zoom when applied to elements
- `nodeConnections` (Dict; optional): Map of nodeId to connection metadata. Each entry has 'incoming' and 'outgoing' arrays
with edge/node details. Updated automatically when edges change.
- `nodeExtent` (Array of Array of Realss; optional): Limit where nodes can be placed [[minX, minY], [maxX, maxY]]
- `nodes` (optional): Array of nodes to display in the flow. nodes has the following type: Array of lists containing elements 'id', 'type', 'data', 'position', 'style', 'className', 'hidden', 'selected', 'draggable', 'selectable', 'connectable', 'deletable', 'dragHandle', 'width', 'height', 'parentId', 'zIndex', 'extent', 'expandParent', 'positionAbsolute', 'ariaLabel', 'focusable', 'resizing'.
Those elements have the following types:
  - `id` (String; required)
  - `type` (String; optional)
  - `data` (Dict; required)
  - `position` (required): . position has the following type: lists containing elements 'x', 'y'.
Those elements have the following types:
  - `x` (Real; required)
  - `y` (Real; required)
  - `style` (Dict; optional)
  - `className` (String; optional)
  - `hidden` (Bool; optional)
  - `selected` (Bool; optional)
  - `draggable` (Bool; optional)
  - `selectable` (Bool; optional)
  - `connectable` (Bool; optional)
  - `deletable` (Bool; optional)
  - `dragHandle` (String; optional)
  - `width` (Real; optional)
  - `height` (Real; optional)
  - `parentId` (String; optional)
  - `zIndex` (Real; optional)
  - `extent` (String | Array of Array of Realss; optional)
  - `expandParent` (Bool; optional)
  - `positionAbsolute` (optional): . positionAbsolute has the following type: lists containing elements 'x', 'y'.
Those elements have the following types:
  - `x` (Real; optional)
  - `y` (Real; optional)
  - `ariaLabel` (String; optional)
  - `focusable` (Bool; optional)
  - `resizing` (Bool; optional)s
- `nodesConnectable` (Bool; optional): Enable/disable the ability to make new connections between nodes
- `nodesDraggable` (Bool; optional): Enable/disable node dragging behavior
- `nodesFocusable` (Bool; optional): Enable/disable keyboard focus on nodes
- `onlyRenderVisibleElements` (Bool; optional): Only render nodes and edges that are visible in the viewport
- `panActivationKeyCode` (String; optional): Key code to activate pan mode (default: 'Space')
- `panOnDrag` (Bool | Array of Reals; optional): Enable/disable panning by dragging. Can be boolean or array of mouse buttons [0,1,2]
- `panOnScroll` (Bool; optional): Enable panning by scrolling
- `panOnScrollMode` (a value equal to: 'free', 'vertical', 'horizontal'; optional): Restrict scroll panning direction: 'free', 'vertical', 'horizontal'
- `panOnScrollSpeed` (Real; optional): Speed of scroll-based panning (default: 0.5)
- `paneClickPosition` (optional): Position where the pane was clicked. paneClickPosition has the following type: lists containing elements 'clientX', 'clientY'.
Those elements have the following types:
  - `clientX` (Real; optional)
  - `clientY` (Real; optional)
- `paneContextMenu` (optional): Context menu info for the pane. paneContextMenu has the following type: lists containing elements 'clientX', 'clientY'.
Those elements have the following types:
  - `clientX` (Real; optional)
  - `clientY` (Real; optional)
- `panels` (optional): Array of panel configurations for custom UI overlays. panels has the following type: Array of lists containing elements 'position', 'children'.
Those elements have the following types:
  - `position` (a value equal to: 'top-left', 'top-right', 'bottom-left', 'bottom-right', 'top-center', 'bottom-center'; optional)
  - `children` (Bool | Real | String | Dict | Array; optional)s
- `pasteAction` (optional): Trigger to paste nodes and edges from clipboard.
Set to an object with optional offset: { offset: { x: 50, y: 50 } }
Will be reset to null after pasting.. pasteAction has the following type: lists containing elements 'offset'.
Those elements have the following types:
  - `offset` (optional): . offset has the following type: lists containing elements 'x', 'y'.
Those elements have the following types:
  - `x` (Real; optional)
  - `y` (Real; optional)
- `pastedElements` (optional): Information about the last paste operation.
Contains the IDs of newly created nodes and edges.. pastedElements has the following type: lists containing elements 'nodeIds', 'edgeIds', 'timestamp'.
Those elements have the following types:
  - `nodeIds` (Array of Strings; optional)
  - `edgeIds` (Array of Strings; optional)
  - `timestamp` (Real; optional)
- `preventDelete` (Bool; optional): Enable delete prevention checks
- `preventDeleteEdges` (Array of Strings; optional): List of edge IDs that cannot be deleted
- `preventDeleteNodes` (Array of Strings; optional): List of node IDs that cannot be deleted
- `preventScrolling` (Bool; optional): Prevent scrolling on the page when the mouse is over the flow
- `reconnectRadius` (Real; optional): Radius for reconnection detection (default: 10)
- `restoreFlowState` (optional): Import/restore a previously exported flow state.
Set this to a flowState object to restore the flow.. restoreFlowState has the following type: lists containing elements 'nodes', 'edges', 'viewport'.
Those elements have the following types:
  - `nodes` (Array; optional)
  - `edges` (Array; optional)
  - `viewport` (optional): . viewport has the following type: lists containing elements 'x', 'y', 'zoom'.
Those elements have the following types:
  - `x` (Real; optional)
  - `y` (Real; optional)
  - `zoom` (Real; optional)
- `selectNodesOnDrag` (Bool; optional): Select nodes when dragging over them
- `selectedEdges` (Array of Strings; optional): IDs of currently selected edges
- `selectedNodes` (Array of Strings; optional): IDs of currently selected nodes
- `selectionKeyCode` (String; optional): Key code for multi-selection box (default: 'Shift')
- `selectionMode` (a value equal to: 'full', 'partial'; optional): Selection mode: 'full' (fully enclosed) or 'partial' (touching)
- `selectionOnDrag` (Bool; optional): Enable selection box by dragging on the pane
- `showBackground` (Bool; optional): Show/hide the background pattern
- `showControls` (Bool; optional): Show/hide the control panel
- `showDevTools` (Bool; optional): Show/hide the developer tools panel
- `showMiniMap` (Bool; optional): Show/hide the minimap navigation component
- `smartHandles` (Bool; optional): Enable smart handle positioning. When true, nodes render handles on all 4 sides
and edges automatically connect to the closest handle pair based on relative node
positions. This prevents edges from wrapping around nodes unnecessarily.
- `snapGrid` (Array of Reals; optional): The grid size for snapping [x, y] (default: [15, 15])
- `snapToGrid` (Bool; optional): Whether to snap nodes to a grid when dragging
- `style` (Dict; optional): Custom CSS styles for the container div
- `theme` (optional): Custom theme configuration. Overrides CSS variables for fine-grained control.
All properties are optional - only specify what you want to customize.. theme has the following type: lists containing elements 'glassBlur', 'glassSaturate', 'nodeBackground', 'nodeBorder', 'nodeText', 'nodeTextSecondary', 'inputNodeBackground', 'inputNodeBorder', 'inputNodeAccent', 'outputNodeBackground', 'outputNodeBorder', 'outputNodeAccent', 'edgeStroke', 'edgeStrokeSelected', 'edgeStrokeAnimated', 'edgeStrokeWidth', 'handleBackground', 'handleBorder', 'handleConnected', 'backgroundColor', 'backgroundPattern', 'selectionBackground', 'selectionBorder', 'borderRadius'.
Those elements have the following types:
  - `glassBlur` (Real; optional): Glass blur intensity in pixels (default: 12)
  - `glassSaturate` (Real; optional): Glass saturation percentage (default: 180)
  - `nodeBackground` (String; optional): Node background color (e.g., 'rgba(255, 255, 255, 0.72)')
  - `nodeBorder` (String; optional): Node border color
  - `nodeText` (String; optional): Node primary text color
  - `nodeTextSecondary` (String; optional): Node secondary/subtitle text color
  - `inputNodeBackground` (String; optional): Input node background color
  - `inputNodeBorder` (String; optional): Input node border color
  - `inputNodeAccent` (String; optional): Input node accent color (top bar)
  - `outputNodeBackground` (String; optional): Output node background color
  - `outputNodeBorder` (String; optional): Output node border color
  - `outputNodeAccent` (String; optional): Output node accent color (bottom bar)
  - `edgeStroke` (String; optional): Edge stroke color
  - `edgeStrokeSelected` (String; optional): Selected edge stroke color
  - `edgeStrokeAnimated` (String; optional): Animated edge stroke color
  - `edgeStrokeWidth` (Real; optional): Edge stroke width in pixels
  - `handleBackground` (String; optional): Handle background color
  - `handleBorder` (String; optional): Handle border color
  - `handleConnected` (String; optional): Connected handle color
  - `backgroundColor` (String; optional): Flow background color
  - `backgroundPattern` (String; optional): Background pattern color
  - `selectionBackground` (String; optional): Selection box background color
  - `selectionBorder` (String; optional): Selection box border color
  - `borderRadius` (Real; optional): Node border radius in pixels
- `themePreset` (a value equal to: 'glass', 'solid', 'minimal'; optional): Theme preset: 'glass' (default), 'solid', or 'minimal'
- glass: Glassmorphism with blur and transparency
- solid: Opaque nodes with subtle shadows (better for complex backgrounds)
- minimal: Clean lines with minimal styling
- `toggleCollapseNode` (String; optional): Set to a group node ID to toggle its collapsed/expanded state.
When collapsed, child nodes are hidden and boundary edges remap to the group.
Will be reset to null after processing.
- `trackNodeDrag` (Bool; optional): Track node position during drag (can be expensive)
- `trackViewport` (Bool; optional): Track viewport changes during pan/zoom
- `translateExtent` (Array of Array of Realss; optional): Limit the viewport panning extent [[minX, minY], [maxX, maxY]]
- `undoRedoAction` (optional): Trigger an undo or redo action. Set to { action: 'undo' } or { action: 'redo' }.
Will be reset to null after execution.. undoRedoAction has the following type: lists containing elements 'action'.
Those elements have the following types:
  - `action` (a value equal to: 'undo', 'redo'; optional)
- `undoRedoMaxHistory` (Real; optional): Maximum number of history snapshots to keep (default: 50)
- `undoRedoState` (optional): Current undo/redo state. Contains canUndo, canRedo, undoCount, redoCount.
Updated automatically when history changes.. undoRedoState has the following type: lists containing elements 'canUndo', 'canRedo', 'undoCount', 'redoCount'.
Those elements have the following types:
  - `canUndo` (Bool; optional)
  - `canRedo` (Bool; optional)
  - `undoCount` (Real; optional)
  - `redoCount` (Real; optional)
- `viewport` (optional): Current viewport state (read-only, updated by callbacks). viewport has the following type: lists containing elements 'x', 'y', 'zoom'.
Those elements have the following types:
  - `x` (Real; optional)
  - `y` (Real; optional)
  - `zoom` (Real; optional)
- `viewportAction` (optional): Trigger viewport actions programmatically.
Set to an action object to execute. Will be reset to null after execution.

Supported actions:
- { action: 'fitView', options: {...} }
- { action: 'zoomIn', options: {...} }
- { action: 'zoomOut', options: {...} }
- { action: 'setZoom', zoom: 1.5, options: {...} }
- { action: 'setCenter', x: 100, y: 100, options: {...} }
- { action: 'setViewport', viewport: {x, y, zoom}, options: {...} }
- { action: 'focusNode', nodeId: 'node-1', zoom: 1.5, duration: 500 }. viewportAction has the following type: lists containing elements 'action', 'nodeId', 'x', 'y', 'zoom', 'duration', 'viewport', 'options'.
Those elements have the following types:
  - `action` (a value equal to: 'fitView', 'zoomIn', 'zoomOut', 'setZoom', 'setCenter', 'setViewport', 'focusNode'; optional)
  - `nodeId` (String; optional)
  - `x` (Real; optional)
  - `y` (Real; optional)
  - `zoom` (Real; optional)
  - `duration` (Real; optional)
  - `viewport` (optional): . viewport has the following type: lists containing elements 'x', 'y', 'zoom'.
Those elements have the following types:
  - `x` (Real; optional)
  - `y` (Real; optional)
  - `zoom` (Real; optional)
  - `options` (Dict; optional)
- `viewportMoving` (Bool; optional): Whether viewport is currently moving (panning/zooming)
- `viewportOverlays` (optional): Array of overlay elements rendered in flow coordinates via ViewportPortal.
Each overlay moves with the viewport (pan/zoom) and is positioned at (x, y) in flow space.. viewportOverlays has the following type: Array of lists containing elements 'x', 'y', 'content', 'style'.
Those elements have the following types:
  - `x` (Real; optional): X position in flow coordinates
  - `y` (Real; optional): Y position in flow coordinates
  - `content` (String; optional): Text content to display
  - `style` (Dict; optional): Custom CSS styles for the overlay divs
- `zIndexMode` (a value equal to: 'default', 'elevate'; optional): Z-index calculation mode. 'default' uses standard stacking. 'elevate' raises
selected nodes and connected edges above all other elements.
- `zoomActivationKeyCode` (String; optional): Key code to activate zoom mode
- `zoomOnDoubleClick` (Bool; optional): Enable zooming by double-clicking
- `zoomOnPinch` (Bool; optional): Enable zooming by pinching on touch devices
- `zoomOnScroll` (Bool; optional): Enable zooming by scrolling
"""
function dashflows(; kwargs...)
        available_props = Symbol[:id, :addNodeOnEdgeDrop, :animateLayout, :animateLayoutDuration, :ariaLabelConfig, :autoPanOnConnect, :autoPanOnNodeDrag, :autoPanOnNodeFocus, :autoPanSpeed, :backgroundColor, :backgroundGap, :backgroundSize, :backgroundVariant, :className, :clickedEdge, :clickedNode, :clipboard, :collapsedGroups, :colorMode, :colorScheme, :computeAction, :computeResult, :connectOnClick, :connectionDragThreshold, :connectionLineStyle, :connectionLineType, :connectionMode, :connectionRadius, :connectionRules, :connectionStartHandle, :contextMenuEdge, :contextMenuNode, :controlsPosition, :controlsShowFitView, :controlsShowInteractive, :controlsShowZoom, :copyAction, :defaultEdgeOptions, :defaultMarkerColor, :defaultViewport, :deleteElementsAction, :deleteKeyCode, :deletedEdges, :deletedNodes, :disableKeyboardA11y, :doubleClickedEdge, :doubleClickedNode, :downloadImage, :draggedNode, :droppedNode, :edgeDroppedNode, :edges, :edgesFocusable, :edgesReconnectable, :elementsSelectable, :elevateEdgesOnSelect, :elevateNodesOnSelect, :enableUndoRedo, :exportFlowState, :fitView, :fitViewOptions, :flowState, :helperLineThreshold, :helperLines, :hoveredEdge, :hoveredNode, :imageDownloaded, :initialized, :lastConnection, :lastError, :layoutOptions, :maxZoom, :minZoom, :miniMapMaskColor, :miniMapNodeBorderRadius, :miniMapNodeColor, :miniMapNodeStrokeColor, :miniMapPannable, :miniMapPosition, :miniMapZoomable, :multiSelectionKeyCode, :noDragClassName, :noPanClassName, :noWheelClassName, :nodeConnections, :nodeExtent, :nodes, :nodesConnectable, :nodesDraggable, :nodesFocusable, :onlyRenderVisibleElements, :panActivationKeyCode, :panOnDrag, :panOnScroll, :panOnScrollMode, :panOnScrollSpeed, :paneClickPosition, :paneContextMenu, :panels, :pasteAction, :pastedElements, :preventDelete, :preventDeleteEdges, :preventDeleteNodes, :preventScrolling, :reconnectRadius, :restoreFlowState, :selectNodesOnDrag, :selectedEdges, :selectedNodes, :selectionKeyCode, :selectionMode, :selectionOnDrag, :showBackground, :showControls, :showDevTools, :showMiniMap, :smartHandles, :snapGrid, :snapToGrid, :style, :theme, :themePreset, :toggleCollapseNode, :trackNodeDrag, :trackViewport, :translateExtent, :undoRedoAction, :undoRedoMaxHistory, :undoRedoState, :viewport, :viewportAction, :viewportMoving, :viewportOverlays, :zIndexMode, :zoomActivationKeyCode, :zoomOnDoubleClick, :zoomOnPinch, :zoomOnScroll]
        wild_props = Symbol[]
        return Component("dashflows", "DashFlows", "dash_flows", available_props, wild_props; kwargs...)
end

