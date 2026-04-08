% Auto-generated: do not edit by hand
\name{dashFlows}

\alias{dashFlows}

\title{DashFlows component}

\description{
DashFlows - A React Flow-based node graph component for Dash applications. Provides interactive node-based workflow visualization with support for custom node types, edge types, glass morphism styling, and extensive callback integration for Python-based interactivity.
}

\usage{
dashFlows(id=NULL, addNodeOnEdgeDrop=NULL, animateLayout=NULL,
animateLayoutDuration=NULL, ariaLabelConfig=NULL,
autoPanOnConnect=NULL, autoPanOnNodeDrag=NULL,
autoPanOnNodeFocus=NULL, autoPanSpeed=NULL,
backgroundColor=NULL, backgroundGap=NULL,
backgroundSize=NULL, backgroundVariant=NULL, className=NULL,
clickedEdge=NULL, clickedNode=NULL, clipboard=NULL,
collapsedGroups=NULL, colorMode=NULL, colorScheme=NULL,
computeAction=NULL, computeResult=NULL, connectOnClick=NULL,
connectionDragThreshold=NULL, connectionLineStyle=NULL,
connectionLineType=NULL, connectionMode=NULL,
connectionRadius=NULL, connectionRules=NULL,
connectionStartHandle=NULL, contextMenuEdge=NULL,
contextMenuNode=NULL, controlsPosition=NULL,
controlsShowFitView=NULL, controlsShowInteractive=NULL,
controlsShowZoom=NULL, copyAction=NULL,
defaultEdgeOptions=NULL, defaultMarkerColor=NULL,
defaultViewport=NULL, deleteElementsAction=NULL,
deleteKeyCode=NULL, deletedEdges=NULL, deletedNodes=NULL,
disableKeyboardA11y=NULL, doubleClickedEdge=NULL,
doubleClickedNode=NULL, downloadImage=NULL,
draggedNode=NULL, droppedNode=NULL, edgeDroppedNode=NULL,
edges=NULL, edgesFocusable=NULL, edgesReconnectable=NULL,
elementsSelectable=NULL, elevateEdgesOnSelect=NULL,
elevateNodesOnSelect=NULL, enableUndoRedo=NULL,
exportFlowState=NULL, fitView=NULL, fitViewOptions=NULL,
flowState=NULL, helperLineThreshold=NULL, helperLines=NULL,
hoveredEdge=NULL, hoveredNode=NULL, imageDownloaded=NULL,
initialized=NULL, lastConnection=NULL, lastError=NULL,
layoutOptions=NULL, maxZoom=NULL, minZoom=NULL,
miniMapMaskColor=NULL, miniMapNodeBorderRadius=NULL,
miniMapNodeColor=NULL, miniMapNodeStrokeColor=NULL,
miniMapPannable=NULL, miniMapPosition=NULL,
miniMapZoomable=NULL, multiSelectionKeyCode=NULL,
noDragClassName=NULL, noPanClassName=NULL,
noWheelClassName=NULL, nodeConnections=NULL,
nodeExtent=NULL, nodes=NULL, nodesConnectable=NULL,
nodesDraggable=NULL, nodesFocusable=NULL,
onlyRenderVisibleElements=NULL, panActivationKeyCode=NULL,
panOnDrag=NULL, panOnScroll=NULL, panOnScrollMode=NULL,
panOnScrollSpeed=NULL, paneClickPosition=NULL,
paneContextMenu=NULL, panels=NULL, pasteAction=NULL,
pastedElements=NULL, preventDelete=NULL,
preventDeleteEdges=NULL, preventDeleteNodes=NULL,
preventScrolling=NULL, reconnectRadius=NULL,
restoreFlowState=NULL, selectNodesOnDrag=NULL,
selectedEdges=NULL, selectedNodes=NULL,
selectionKeyCode=NULL, selectionMode=NULL,
selectionOnDrag=NULL, showBackground=NULL,
showControls=NULL, showDevTools=NULL, showMiniMap=NULL,
smartHandles=NULL, snapGrid=NULL, snapToGrid=NULL,
style=NULL, theme=NULL, themePreset=NULL,
toggleCollapseNode=NULL, trackNodeDrag=NULL,
trackViewport=NULL, translateExtent=NULL,
undoRedoAction=NULL, undoRedoMaxHistory=NULL,
undoRedoState=NULL, viewport=NULL, viewportAction=NULL,
viewportMoving=NULL, viewportOverlays=NULL, zIndexMode=NULL,
zoomActivationKeyCode=NULL, zoomOnDoubleClick=NULL,
zoomOnPinch=NULL, zoomOnScroll=NULL)
}

\arguments{
\item{id}{Character. The ID used to identify this component in Dash callbacks.}

\item{addNodeOnEdgeDrop}{Logical. When true, dragging a connection from a handle and dropping on empty canvas
creates a new default node at that position and connects it.}

\item{animateLayout}{Logical. Enable smooth animated transitions when applying ELK layout.
Nodes interpolate from current to target positions with an ease-out curve.}

\item{animateLayoutDuration}{Numeric. Duration of layout animation in milliseconds (default: 300)}

\item{ariaLabelConfig}{Named list. ARIA label configuration for accessibility. Customize labels for screen readers.
Keys: nodes, edges, controls, minimap. Values are label strings.}

\item{autoPanOnConnect}{Logical. Auto-pan viewport when making a new connection near edges}

\item{autoPanOnNodeDrag}{Logical. Auto-pan viewport when dragging a node near edges}

\item{autoPanOnNodeFocus}{Logical. Auto-pan the viewport when focusing a node via keyboard (Tab key).}

\item{autoPanSpeed}{Numeric. Speed of auto-panning (default: 15)}

\item{backgroundColor}{Character. Color of the background pattern}

\item{backgroundGap}{Numeric | list of numerics. Gap between background pattern elements}

\item{backgroundSize}{Numeric. Size of background pattern elements}

\item{backgroundVariant}{A value equal to: 'dots', 'lines', 'cross'. Background pattern type: 'dots', 'lines', 'cross'}

\item{className}{Character. CSS class name for the container div}

\item{clickedEdge}{Lists containing elements 'id', 'source', 'target'.
those elements have the following types:
  - id (character; optional)
  - source (character; optional)
  - target (character; optional). The edge that was clicked}

\item{clickedNode}{Lists containing elements 'id', 'data', 'position'.
those elements have the following types:
  - id (character; optional)
  - data (named list; optional)
  - position (named list; optional). The node that was clicked}

\item{clipboard}{Lists containing elements 'nodes', 'edges', 'timestamp'.
those elements have the following types:
  - nodes (unnamed list; optional)
  - edges (unnamed list; optional)
  - timestamp (numeric; optional). Internal clipboard containing copied nodes and edges.
Populated by copyAction, consumed by pasteAction.}

\item{collapsedGroups}{List of characters. List of currently collapsed group node IDs (read-only output).}

\item{colorMode}{A value equal to: 'light', 'dark', 'system'. Color mode: 'light', 'dark', or 'system'}

\item{colorScheme}{A value equal to: 'default', 'ocean', 'forest', 'sunset', 'midnight', 'rose'. Color scheme preset for node and edge colors.
Works in combination with themePreset for full customization.
Each scheme includes light and dark mode variants.
- default: Neutral blue/purple (default)
- ocean: Blues and teals
- forest: Greens and browns
- sunset: Oranges and reds
- midnight: Deep blues and purples
- rose: Pinks and reds}

\item{computeAction}{Lists containing elements 'action', 'nodeid', 'inputdata'.
those elements have the following types:
  - action (a value equal to: 'compute', 'computenode'; optional)
  - nodeid (character; optional)
  - inputdata (named list; optional). Trigger a graph computation. Set to { action: 'compute' } to perform
topological sort and emit traversal order with input mappings.
Will be reset to null after execution.}

\item{computeResult}{Lists containing elements 'traversalorder', 'nodeinputs', 'timestamp'.
those elements have the following types:
  - traversalorder (list of characters; optional)
  - nodeinputs (named list; optional)
  - timestamp (numeric; optional). Result of the last computation. Contains traversalOrder (array of node IDs
in topological order) and nodeInputs (map of nodeId to input details).}

\item{connectOnClick}{Logical. Enable click-based connection mode (click source then target)}

\item{connectionDragThreshold}{Numeric. Minimum drag distance in pixels before a connection line appears.
Useful to prevent accidental connections. Default is 0 (immediate).}

\item{connectionLineStyle}{Named list. Style for the connection line while dragging}

\item{connectionLineType}{A value equal to: 'bezier', 'straight', 'step', 'smoothstep', 'simplebezier'. Type of connection line: 'bezier', 'straight', 'step', 'smoothstep', 'simplebezier'}

\item{connectionMode}{A value equal to: 'strict', 'loose'. Connection mode: 'strict' (same handle type) or 'loose' (any handle)}

\item{connectionRadius}{Numeric. Radius for connection drop detection (default: 20)}

\item{connectionRules}{Lists containing elements 'allowselfconnection', 'allowduplicateconnections', 'validsourcetypes', 'validtargettypes'.
those elements have the following types:
  - allowselfconnection (logical; optional)
  - allowduplicateconnections (logical; optional)
  - validsourcetypes (list of characters; optional)
  - validtargettypes (list of characters; optional). Rules for validating connections}

\item{connectionStartHandle}{Lists containing elements 'nodeid', 'handleid', 'handletype'.
those elements have the following types:
  - nodeid (character; optional)
  - handleid (character; optional)
  - handletype (character; optional). Current connection being created}

\item{contextMenuEdge}{Lists containing elements 'id', 'source', 'target', 'clientx', 'clienty'.
those elements have the following types:
  - id (character; optional)
  - source (character; optional)
  - target (character; optional)
  - clientx (numeric; optional)
  - clienty (numeric; optional). Context menu info for an edge}

\item{contextMenuNode}{Lists containing elements 'id', 'data', 'position', 'clientx', 'clienty'.
those elements have the following types:
  - id (character; optional)
  - data (named list; optional)
  - position (named list; optional)
  - clientx (numeric; optional)
  - clienty (numeric; optional). Context menu info for a node}

\item{controlsPosition}{A value equal to: 'top-left', 'top-right', 'bottom-left', 'bottom-right', 'top-center', 'bottom-center'. Position of controls panel}

\item{controlsShowFitView}{Logical. Show fit-view button in controls}

\item{controlsShowInteractive}{Logical. Show interactive toggle in controls}

\item{controlsShowZoom}{Logical. Show zoom buttons in controls}

\item{copyAction}{Logical. Trigger to copy selected nodes and edges to clipboard.
Set to true to copy. Will be reset to false after copying.
If nothing is selected, copies all nodes and their connecting edges.}

\item{defaultEdgeOptions}{Lists containing elements 'type', 'style', 'animated', 'markerstart', 'markerend'.
those elements have the following types:
  - type (character; optional)
  - style (named list; optional)
  - animated (logical; optional)
  - markerstart (named list; optional)
  - markerend (named list; optional). Default options applied to all new edges}

\item{defaultMarkerColor}{Character. Default color for edge markers}

\item{defaultViewport}{Lists containing elements 'x', 'y', 'zoom'.
those elements have the following types:
  - x (numeric; optional)
  - y (numeric; optional)
  - zoom (numeric; optional). The initial viewport position and zoom level}

\item{deleteElementsAction}{Lists containing elements 'nodeids', 'edgeids'.
those elements have the following types:
  - nodeids (list of characters; optional): ids of nodes to delete (connected edges are also removed)
  - edgeids (list of characters; optional): ids of edges to delete. Delete specific nodes and/or edges by ID. Routes through
reactFlowInstance.deleteElements() so undo/redo middleware can capture
the change. Set to { nodeIds: [...], edgeIds: [...] }; auto-resets to null.}

\item{deleteKeyCode}{Character. Key code for deleting selected elements (default: 'Backspace', null to disable)}

\item{deletedEdges}{List of characters. IDs of recently deleted edges}

\item{deletedNodes}{List of characters. IDs of recently deleted nodes}

\item{disableKeyboardA11y}{Logical. Disable keyboard accessibility features}

\item{doubleClickedEdge}{Lists containing elements 'id', 'source', 'target'.
those elements have the following types:
  - id (character; optional)
  - source (character; optional)
  - target (character; optional). The edge that was double-clicked}

\item{doubleClickedNode}{Lists containing elements 'id', 'data', 'position'.
those elements have the following types:
  - id (character; optional)
  - data (named list; optional)
  - position (named list; optional). The node that was double-clicked}

\item{downloadImage}{Lists containing elements 'format', 'filename', 'quality', 'backgroundcolor', 'pixelratio'.
those elements have the following types:
  - format (a value equal to: 'png', 'svg', 'jpeg', 'jpg'; optional)
  - filename (character; optional)
  - quality (numeric; optional)
  - backgroundcolor (character; optional)
  - pixelratio (numeric; optional). Trigger to download the flow as an image.
Set to a config object to initiate download. Will be reset to null after download.

Config options:
- format: 'png' | 'svg' | 'jpeg' (default: 'png')
- filename: string (default: 'flow')
- quality: number 0-1 (default: 0.95, for jpeg only)
- backgroundColor: string (default: '#ffffff')
- pixelRatio: number (default: 2, for higher resolution)}

\item{draggedNode}{Lists containing elements 'id', 'isdragging', 'startposition', 'currentposition', 'endposition'.
those elements have the following types:
  - id (character; optional)
  - isdragging (logical; optional)
  - startposition (named list; optional)
  - currentposition (named list; optional)
  - endposition (named list; optional). The node being dragged}

\item{droppedNode}{Lists containing elements 'type', 'position', 'data', 'clientx', 'clienty', 'timestamp'.
those elements have the following types:
  - type (character; optional)
  - position (optional): . position has the following type: lists containing elements 'x', 'y'.
those elements have the following types:
  - x (numeric; optional)
  - y (numeric; optional)
  - data (named list; optional)
  - clientx (numeric; optional)
  - clienty (numeric; optional)
  - timestamp (numeric; optional). Node data from a drop event (drag and drop from external source).
Contains the type, position, and data of the dropped item.
Use this in a callback to create a new node at the drop position.}

\item{edgeDroppedNode}{Lists containing elements 'nodeid', 'position', 'sourcenodeid', 'sourcehandleid', 'handletype', 'timestamp'.
those elements have the following types:
  - nodeid (character; optional)
  - position (optional): . position has the following type: lists containing elements 'x', 'y'.
those elements have the following types:
  - x (numeric; optional)
  - y (numeric; optional)
  - sourcenodeid (character; optional)
  - sourcehandleid (character; optional)
  - handletype (character; optional)
  - timestamp (numeric; optional). Info about the node created by dropping an edge on empty canvas.
Contains nodeId, position, sourceNodeId, sourceHandleId, handleType, timestamp.}

\item{edges}{List of lists containing elements 'id', 'source', 'target', 'sourcehandle', 'targethandle', 'type', 'data', 'style', 'classname', 'hidden', 'selected', 'animated', 'deletable', 'selectable', 'focusable', 'zindex', 'arialabel', 'interactionwidth', 'label', 'labelstyle', 'labelshowbg', 'labelbgstyle', 'labelbgpadding', 'labelbgborderradius', 'markerstart', 'markerend'.
those elements have the following types:
  - id (character; required)
  - source (character; required)
  - target (character; required)
  - sourcehandle (character; optional)
  - targethandle (character; optional)
  - type (character; optional)
  - data (named list; optional)
  - style (named list; optional)
  - classname (character; optional)
  - hidden (logical; optional)
  - selected (logical; optional)
  - animated (logical; optional)
  - deletable (logical; optional)
  - selectable (logical; optional)
  - focusable (logical; optional)
  - zindex (numeric; optional)
  - arialabel (character; optional)
  - interactionwidth (numeric; optional)
  - label (character; optional)
  - labelstyle (named list; optional)
  - labelshowbg (logical; optional)
  - labelbgstyle (named list; optional)
  - labelbgpadding (list of numerics; optional)
  - labelbgborderradius (numeric; optional)
  - markerstart (optional): . markerstart has the following type: character | lists containing elements 'type', 'color', 'width', 'height', 'markerunits', 'orient', 'strokewidth'.
those elements have the following types:
  - type (character; required)
  - color (character; optional)
  - width (numeric; optional)
  - height (numeric; optional)
  - markerunits (character; optional)
  - orient (character; optional)
  - strokewidth (numeric; optional)
  - markerend (optional): . markerend has the following type: character | lists containing elements 'type', 'color', 'width', 'height', 'markerunits', 'orient', 'strokewidth'.
those elements have the following types:
  - type (character; required)
  - color (character; optional)
  - width (numeric; optional)
  - height (numeric; optional)
  - markerunits (character; optional)
  - orient (character; optional)
  - strokewidth (numeric; optional)s. Array of edges defining connections between nodes}

\item{edgesFocusable}{Logical. Enable/disable keyboard focus on edges}

\item{edgesReconnectable}{Logical. Allow edges to be reconnected after creation}

\item{elementsSelectable}{Logical. Enable/disable the ability to select elements}

\item{elevateEdgesOnSelect}{Logical. Raise z-index of selected edges}

\item{elevateNodesOnSelect}{Logical. Raise z-index of selected nodes}

\item{enableUndoRedo}{Logical. Enable the undo/redo history system. When enabled, node and edge changes
(add, remove, position drag-stop) are recorded to a history stack.}

\item{exportFlowState}{Logical. Trigger to export the current flow state. Set to true to export.
After export, this will be reset to false and flowState will be populated.}

\item{fitView}{Logical. Automatically fit all nodes in view on initialization}

\item{fitViewOptions}{Lists containing elements 'padding', 'includehiddennodes', 'minzoom', 'maxzoom', 'duration', 'nodes'.
those elements have the following types:
  - padding (numeric; optional)
  - includehiddennodes (logical; optional)
  - minzoom (numeric; optional)
  - maxzoom (numeric; optional)
  - duration (numeric; optional)
  - nodes (optional): . nodes has the following type: list of lists containing elements 'id'.
those elements have the following types:
  - id (character; optional)s. Options for fitView behavior}

\item{flowState}{Lists containing elements 'nodes', 'edges', 'viewport'.
those elements have the following types:
  - nodes (unnamed list; optional)
  - edges (unnamed list; optional)
  - viewport (optional): . viewport has the following type: lists containing elements 'x', 'y', 'zoom'.
those elements have the following types:
  - x (numeric; optional)
  - y (numeric; optional)
  - zoom (numeric; optional). The exported flow state as a serializable object containing nodes, edges, and viewport.
This is populated when exportFlowState is triggered.}

\item{helperLineThreshold}{Numeric. Distance in pixels within which helper lines snap and appear (default: 5)}

\item{helperLines}{Logical. Enable visual alignment guides (helper lines) when dragging nodes.
Lines appear when a node aligns with another node's top/center/bottom or left/center/right.}

\item{hoveredEdge}{Lists containing elements 'id', 'source', 'target'.
those elements have the following types:
  - id (character; optional)
  - source (character; optional)
  - target (character; optional). The edge being hovered}

\item{hoveredNode}{Lists containing elements 'id', 'data'.
those elements have the following types:
  - id (character; optional)
  - data (named list; optional). The node being hovered}

\item{imageDownloaded}{Lists containing elements 'filename', 'format', 'timestamp'.
those elements have the following types:
  - filename (character; optional)
  - format (character; optional)
  - timestamp (numeric; optional). Information about the last successful image download.
Populated after a successful downloadImage operation.}

\item{initialized}{Logical. Whether the flow has been initialized}

\item{lastConnection}{Lists containing elements 'source', 'sourcehandle', 'target', 'targethandle'.
those elements have the following types:
  - source (character; optional)
  - sourcehandle (character; optional)
  - target (character; optional)
  - targethandle (character; optional). The last connection that was made}

\item{lastError}{Lists containing elements 'id', 'message', 'type', 'timestamp'.
those elements have the following types:
  - id (character; optional)
  - message (character; optional)
  - type (character; optional)
  - timestamp (numeric; optional). Last error that occurred}

\item{layoutOptions}{Character. Layout options for arranging nodes using the ELK layout engine (JSON string)}

\item{maxZoom}{Numeric. Maximum zoom level (default: 2)}

\item{minZoom}{Numeric. Minimum zoom level (default: 0.5)}

\item{miniMapMaskColor}{Character. Color for the minimap mask (viewport indicator)}

\item{miniMapNodeBorderRadius}{Numeric. Border radius for minimap nodes}

\item{miniMapNodeColor}{Character. Color function or string for minimap nodes}

\item{miniMapNodeStrokeColor}{Character. Stroke color for minimap nodes}

\item{miniMapPannable}{Logical. Allow panning by dragging the minimap}

\item{miniMapPosition}{A value equal to: 'top-left', 'top-right', 'bottom-left', 'bottom-right'. Position of the minimap}

\item{miniMapZoomable}{Logical. Allow zooming via the minimap}

\item{multiSelectionKeyCode}{Character. Key code for adding to selection}

\item{noDragClassName}{Character. CSS class name that prevents dragging when applied to elements}

\item{noPanClassName}{Character. CSS class name that prevents panning when applied to elements}

\item{noWheelClassName}{Character. CSS class name that prevents wheel zoom when applied to elements}

\item{nodeConnections}{Named list. Map of nodeId to connection metadata. Each entry has 'incoming' and 'outgoing' arrays
with edge/node details. Updated automatically when edges change.}

\item{nodeExtent}{List of list of numericss. Limit where nodes can be placed [[minX, minY], [maxX, maxY]]}

\item{nodes}{List of lists containing elements 'id', 'type', 'data', 'position', 'style', 'classname', 'hidden', 'selected', 'draggable', 'selectable', 'connectable', 'deletable', 'draghandle', 'width', 'height', 'parentid', 'zindex', 'extent', 'expandparent', 'positionabsolute', 'arialabel', 'focusable', 'resizing'.
those elements have the following types:
  - id (character; required)
  - type (character; optional)
  - data (named list; required)
  - position (required): . position has the following type: lists containing elements 'x', 'y'.
those elements have the following types:
  - x (numeric; required)
  - y (numeric; required)
  - style (named list; optional)
  - classname (character; optional)
  - hidden (logical; optional)
  - selected (logical; optional)
  - draggable (logical; optional)
  - selectable (logical; optional)
  - connectable (logical; optional)
  - deletable (logical; optional)
  - draghandle (character; optional)
  - width (numeric; optional)
  - height (numeric; optional)
  - parentid (character; optional)
  - zindex (numeric; optional)
  - extent (character | list of list of numericss; optional)
  - expandparent (logical; optional)
  - positionabsolute (optional): . positionabsolute has the following type: lists containing elements 'x', 'y'.
those elements have the following types:
  - x (numeric; optional)
  - y (numeric; optional)
  - arialabel (character; optional)
  - focusable (logical; optional)
  - resizing (logical; optional)s. Array of nodes to display in the flow}

\item{nodesConnectable}{Logical. Enable/disable the ability to make new connections between nodes}

\item{nodesDraggable}{Logical. Enable/disable node dragging behavior}

\item{nodesFocusable}{Logical. Enable/disable keyboard focus on nodes}

\item{onlyRenderVisibleElements}{Logical. Only render nodes and edges that are visible in the viewport}

\item{panActivationKeyCode}{Character. Key code to activate pan mode (default: 'Space')}

\item{panOnDrag}{Logical | list of numerics. Enable/disable panning by dragging. Can be boolean or array of mouse buttons [0,1,2]}

\item{panOnScroll}{Logical. Enable panning by scrolling}

\item{panOnScrollMode}{A value equal to: 'free', 'vertical', 'horizontal'. Restrict scroll panning direction: 'free', 'vertical', 'horizontal'}

\item{panOnScrollSpeed}{Numeric. Speed of scroll-based panning (default: 0.5)}

\item{paneClickPosition}{Lists containing elements 'clientx', 'clienty'.
those elements have the following types:
  - clientx (numeric; optional)
  - clienty (numeric; optional). Position where the pane was clicked}

\item{paneContextMenu}{Lists containing elements 'clientx', 'clienty'.
those elements have the following types:
  - clientx (numeric; optional)
  - clienty (numeric; optional). Context menu info for the pane}

\item{panels}{List of lists containing elements 'position', 'children'.
those elements have the following types:
  - position (a value equal to: 'top-left', 'top-right', 'bottom-left', 'bottom-right', 'top-center', 'bottom-center'; optional)
  - children (logical | numeric | character | named list | unnamed list; optional)s. Array of panel configurations for custom UI overlays}

\item{pasteAction}{Lists containing elements 'offset'.
those elements have the following types:
  - offset (optional): . offset has the following type: lists containing elements 'x', 'y'.
those elements have the following types:
  - x (numeric; optional)
  - y (numeric; optional). Trigger to paste nodes and edges from clipboard.
Set to an object with optional offset: { offset: { x: 50, y: 50 } }
Will be reset to null after pasting.}

\item{pastedElements}{Lists containing elements 'nodeids', 'edgeids', 'timestamp'.
those elements have the following types:
  - nodeids (list of characters; optional)
  - edgeids (list of characters; optional)
  - timestamp (numeric; optional). Information about the last paste operation.
Contains the IDs of newly created nodes and edges.}

\item{preventDelete}{Logical. Enable delete prevention checks}

\item{preventDeleteEdges}{List of characters. List of edge IDs that cannot be deleted}

\item{preventDeleteNodes}{List of characters. List of node IDs that cannot be deleted}

\item{preventScrolling}{Logical. Prevent scrolling on the page when the mouse is over the flow}

\item{reconnectRadius}{Numeric. Radius for reconnection detection (default: 10)}

\item{restoreFlowState}{Lists containing elements 'nodes', 'edges', 'viewport'.
those elements have the following types:
  - nodes (unnamed list; optional)
  - edges (unnamed list; optional)
  - viewport (optional): . viewport has the following type: lists containing elements 'x', 'y', 'zoom'.
those elements have the following types:
  - x (numeric; optional)
  - y (numeric; optional)
  - zoom (numeric; optional). Import/restore a previously exported flow state.
Set this to a flowState object to restore the flow.}

\item{selectNodesOnDrag}{Logical. Select nodes when dragging over them}

\item{selectedEdges}{List of characters. IDs of currently selected edges}

\item{selectedNodes}{List of characters. IDs of currently selected nodes}

\item{selectionKeyCode}{Character. Key code for multi-selection box (default: 'Shift')}

\item{selectionMode}{A value equal to: 'full', 'partial'. Selection mode: 'full' (fully enclosed) or 'partial' (touching)}

\item{selectionOnDrag}{Logical. Enable selection box by dragging on the pane}

\item{showBackground}{Logical. Show/hide the background pattern}

\item{showControls}{Logical. Show/hide the control panel}

\item{showDevTools}{Logical. Show/hide the developer tools panel}

\item{showMiniMap}{Logical. Show/hide the minimap navigation component}

\item{smartHandles}{Logical. Enable smart handle positioning. When true, nodes render handles on all 4 sides
and edges automatically connect to the closest handle pair based on relative node
positions. This prevents edges from wrapping around nodes unnecessarily.}

\item{snapGrid}{List of numerics. The grid size for snapping [x, y] (default: [15, 15])}

\item{snapToGrid}{Logical. Whether to snap nodes to a grid when dragging}

\item{style}{Named list. Custom CSS styles for the container div}

\item{theme}{Lists containing elements 'glassblur', 'glasssaturate', 'nodebackground', 'nodeborder', 'nodetext', 'nodetextsecondary', 'inputnodebackground', 'inputnodeborder', 'inputnodeaccent', 'outputnodebackground', 'outputnodeborder', 'outputnodeaccent', 'edgestroke', 'edgestrokeselected', 'edgestrokeanimated', 'edgestrokewidth', 'handlebackground', 'handleborder', 'handleconnected', 'backgroundcolor', 'backgroundpattern', 'selectionbackground', 'selectionborder', 'borderradius'.
those elements have the following types:
  - glassblur (numeric; optional): glass blur intensity in pixels (default: 12)
  - glasssaturate (numeric; optional): glass saturation percentage (default: 180)
  - nodebackground (character; optional): node background color (e.g., 'rgba(255, 255, 255, 0.72)')
  - nodeborder (character; optional): node border color
  - nodetext (character; optional): node primary text color
  - nodetextsecondary (character; optional): node secondary/subtitle text color
  - inputnodebackground (character; optional): input node background color
  - inputnodeborder (character; optional): input node border color
  - inputnodeaccent (character; optional): input node accent color (top bar)
  - outputnodebackground (character; optional): output node background color
  - outputnodeborder (character; optional): output node border color
  - outputnodeaccent (character; optional): output node accent color (bottom bar)
  - edgestroke (character; optional): edge stroke color
  - edgestrokeselected (character; optional): selected edge stroke color
  - edgestrokeanimated (character; optional): animated edge stroke color
  - edgestrokewidth (numeric; optional): edge stroke width in pixels
  - handlebackground (character; optional): handle background color
  - handleborder (character; optional): handle border color
  - handleconnected (character; optional): connected handle color
  - backgroundcolor (character; optional): flow background color
  - backgroundpattern (character; optional): background pattern color
  - selectionbackground (character; optional): selection box background color
  - selectionborder (character; optional): selection box border color
  - borderradius (numeric; optional): node border radius in pixels. Custom theme configuration. Overrides CSS variables for fine-grained control.
All properties are optional - only specify what you want to customize.}

\item{themePreset}{A value equal to: 'glass', 'solid', 'minimal'. Theme preset: 'glass' (default), 'solid', or 'minimal'
- glass: Glassmorphism with blur and transparency
- solid: Opaque nodes with subtle shadows (better for complex backgrounds)
- minimal: Clean lines with minimal styling}

\item{toggleCollapseNode}{Character. Set to a group node ID to toggle its collapsed/expanded state.
When collapsed, child nodes are hidden and boundary edges remap to the group.
Will be reset to null after processing.}

\item{trackNodeDrag}{Logical. Track node position during drag (can be expensive)}

\item{trackViewport}{Logical. Track viewport changes during pan/zoom}

\item{translateExtent}{List of list of numericss. Limit the viewport panning extent [[minX, minY], [maxX, maxY]]}

\item{undoRedoAction}{Lists containing elements 'action'.
those elements have the following types:
  - action (a value equal to: 'undo', 'redo'; optional). Trigger an undo or redo action. Set to { action: 'undo' } or { action: 'redo' }.
Will be reset to null after execution.}

\item{undoRedoMaxHistory}{Numeric. Maximum number of history snapshots to keep (default: 50)}

\item{undoRedoState}{Lists containing elements 'canundo', 'canredo', 'undocount', 'redocount'.
those elements have the following types:
  - canundo (logical; optional)
  - canredo (logical; optional)
  - undocount (numeric; optional)
  - redocount (numeric; optional). Current undo/redo state. Contains canUndo, canRedo, undoCount, redoCount.
Updated automatically when history changes.}

\item{viewport}{Lists containing elements 'x', 'y', 'zoom'.
those elements have the following types:
  - x (numeric; optional)
  - y (numeric; optional)
  - zoom (numeric; optional). Current viewport state (read-only, updated by callbacks)}

\item{viewportAction}{Lists containing elements 'action', 'nodeid', 'x', 'y', 'zoom', 'duration', 'viewport', 'options'.
those elements have the following types:
  - action (a value equal to: 'fitview', 'zoomin', 'zoomout', 'setzoom', 'setcenter', 'setviewport', 'focusnode'; optional)
  - nodeid (character; optional)
  - x (numeric; optional)
  - y (numeric; optional)
  - zoom (numeric; optional)
  - duration (numeric; optional)
  - viewport (optional): . viewport has the following type: lists containing elements 'x', 'y', 'zoom'.
those elements have the following types:
  - x (numeric; optional)
  - y (numeric; optional)
  - zoom (numeric; optional)
  - options (named list; optional). Trigger viewport actions programmatically.
Set to an action object to execute. Will be reset to null after execution.

Supported actions:
- { action: 'fitView', options: {...} }
- { action: 'zoomIn', options: {...} }
- { action: 'zoomOut', options: {...} }
- { action: 'setZoom', zoom: 1.5, options: {...} }
- { action: 'setCenter', x: 100, y: 100, options: {...} }
- { action: 'setViewport', viewport: {x, y, zoom}, options: {...} }
- { action: 'focusNode', nodeId: 'node-1', zoom: 1.5, duration: 500 }}

\item{viewportMoving}{Logical. Whether viewport is currently moving (panning/zooming)}

\item{viewportOverlays}{List of lists containing elements 'x', 'y', 'content', 'style'.
those elements have the following types:
  - x (numeric; optional): x position in flow coordinates
  - y (numeric; optional): y position in flow coordinates
  - content (character; optional): text content to display
  - style (named list; optional): custom css styles for the overlay divs. Array of overlay elements rendered in flow coordinates via ViewportPortal.
Each overlay moves with the viewport (pan/zoom) and is positioned at (x, y) in flow space.}

\item{zIndexMode}{A value equal to: 'default', 'elevate'. Z-index calculation mode. 'default' uses standard stacking. 'elevate' raises
selected nodes and connected edges above all other elements.}

\item{zoomActivationKeyCode}{Character. Key code to activate zoom mode}

\item{zoomOnDoubleClick}{Logical. Enable zooming by double-clicking}

\item{zoomOnPinch}{Logical. Enable zooming by pinching on touch devices}

\item{zoomOnScroll}{Logical. Enable zooming by scrolling}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

