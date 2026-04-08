# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args

ComponentType = typing.Union[
    str,
    int,
    float,
    Component,
    None,
    typing.Sequence[typing.Union[str, int, float, Component, None]],
]

NumberType = typing.Union[
    typing.SupportsFloat, typing.SupportsInt, typing.SupportsComplex
]


class DashFlows(Component):
    """A DashFlows component.
DashFlows - A React Flow-based node graph component for Dash applications.
Provides interactive node-based workflow visualization with support for
custom node types, edge types, glass morphism styling, and extensive
callback integration for Python-based interactivity.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- addNodeOnEdgeDrop (boolean; optional):
    When True, dragging a connection from a handle and dropping on
    empty canvas creates a new default node at that position and
    connects it.

- animateLayout (boolean; default False):
    Enable smooth animated transitions when applying ELK layout. Nodes
    interpolate from current to target positions with an ease-out
    curve.

- animateLayoutDuration (number; default 300):
    Duration of layout animation in milliseconds (default: 300).

- ariaLabelConfig (dict; optional):
    ARIA label configuration for accessibility. Customize labels for
    screen readers. Keys: nodes, edges, controls, minimap. Values are
    label strings.

- autoPanOnConnect (boolean; default True):
    Auto-pan viewport when making a new connection near edges.

- autoPanOnNodeDrag (boolean; default True):
    Auto-pan viewport when dragging a node near edges.

- autoPanOnNodeFocus (boolean; default True):
    Auto-pan the viewport when focusing a node via keyboard (Tab key).

- autoPanSpeed (number; default 15):
    Speed of auto-panning (default: 15).

- backgroundColor (string; optional):
    Color of the background pattern.

- backgroundGap (number | list of numbers; default 16):
    Gap between background pattern elements.

- backgroundSize (number; default 1):
    Size of background pattern elements.

- backgroundVariant (a value equal to: 'dots', 'lines', 'cross'; default 'dots'):
    Background pattern type: 'dots', 'lines', 'cross'.

- className (string; default ''):
    CSS class name for the container div.

- clickedEdge (dict; optional):
    The edge that was clicked.

    `clickedEdge` is a dict with keys:

    - id (string; optional)

    - source (string; optional)

    - target (string; optional)

- clickedNode (dict; optional):
    The node that was clicked.

    `clickedNode` is a dict with keys:

    - id (string; optional)

    - data (dict; optional)

    - position (dict; optional)

- clipboard (dict; optional):
    Internal clipboard containing copied nodes and edges. Populated by
    copyAction, consumed by pasteAction.

    `clipboard` is a dict with keys:

    - nodes (list; optional)

    - edges (list; optional)

    - timestamp (number; optional)

- collapsedGroups (list of strings; optional):
    List of currently collapsed group node IDs (read-only output).

- colorMode (a value equal to: 'light', 'dark', 'system'; default 'light'):
    Color mode: 'light', 'dark', or 'system'.

- colorScheme (a value equal to: 'default', 'ocean', 'forest', 'sunset', 'midnight', 'rose'; optional):
    Color scheme preset for node and edge colors. Works in combination
    with themePreset for full customization. Each scheme includes
    light and dark mode variants. - default: Neutral blue/purple
    (default) - ocean: Blues and teals - forest: Greens and browns -
    sunset: Oranges and reds - midnight: Deep blues and purples -
    rose: Pinks and reds.

- computeAction (dict; optional):
    Trigger a graph computation. Set to { action: 'compute' } to
    perform topological sort and emit traversal order with input
    mappings. Will be reset to None after execution.

    `computeAction` is a dict with keys:

    - action (a value equal to: 'compute', 'computeNode'; optional)

    - nodeId (string; optional)

    - inputData (dict; optional)

- computeResult (dict; optional):
    Result of the last computation. Contains traversalOrder (array of
    node IDs in topological order) and nodeInputs (map of nodeId to
    input details).

    `computeResult` is a dict with keys:

    - traversalOrder (list of strings; optional)

    - nodeInputs (dict; optional)

    - timestamp (number; optional)

- connectOnClick (boolean; default True):
    Enable click-based connection mode (click source then target).

- connectionDragThreshold (number; default 0):
    Minimum drag distance in pixels before a connection line appears.
    Useful to prevent accidental connections. Default is 0
    (immediate).

- connectionLineStyle (dict; optional):
    Style for the connection line while dragging.

- connectionLineType (a value equal to: 'bezier', 'straight', 'step', 'smoothstep', 'simplebezier'; default 'bezier'):
    Type of connection line: 'bezier', 'straight', 'step',
    'smoothstep', 'simplebezier'.

- connectionMode (a value equal to: 'strict', 'loose'; default 'strict'):
    Connection mode: 'strict' (same handle type) or 'loose' (any
    handle).

- connectionRadius (number; default 20):
    Radius for connection drop detection (default: 20).

- connectionRules (dict; optional):
    Rules for validating connections.

    `connectionRules` is a dict with keys:

    - allowSelfConnection (boolean; optional)

    - allowDuplicateConnections (boolean; optional)

    - validSourceTypes (list of strings; optional)

    - validTargetTypes (list of strings; optional)

- connectionStartHandle (dict; optional):
    Current connection being created.

    `connectionStartHandle` is a dict with keys:

    - nodeId (string; optional)

    - handleId (string; optional)

    - handleType (string; optional)

- contextMenuEdge (dict; optional):
    Context menu info for an edge.

    `contextMenuEdge` is a dict with keys:

    - id (string; optional)

    - source (string; optional)

    - target (string; optional)

    - clientX (number; optional)

    - clientY (number; optional)

- contextMenuNode (dict; optional):
    Context menu info for a node.

    `contextMenuNode` is a dict with keys:

    - id (string; optional)

    - data (dict; optional)

    - position (dict; optional)

    - clientX (number; optional)

    - clientY (number; optional)

- controlsPosition (a value equal to: 'top-left', 'top-right', 'bottom-left', 'bottom-right', 'top-center', 'bottom-center'; default 'bottom-left'):
    Position of controls panel.

- controlsShowFitView (boolean; default True):
    Show fit-view button in controls.

- controlsShowInteractive (boolean; default True):
    Show interactive toggle in controls.

- controlsShowZoom (boolean; default True):
    Show zoom buttons in controls.

- copyAction (boolean; optional):
    Trigger to copy selected nodes and edges to clipboard. Set to True
    to copy. Will be reset to False after copying. If nothing is
    selected, copies all nodes and their connecting edges.

- defaultEdgeOptions (dict; optional):
    Default options applied to all new edges.

    `defaultEdgeOptions` is a dict with keys:

    - type (string; optional)

    - style (dict; optional)

    - animated (boolean; optional)

    - markerStart (dict; optional)

    - markerEnd (dict; optional)

- defaultMarkerColor (string; default '#555'):
    Default color for edge markers.

- defaultViewport (dict; optional):
    The initial viewport position and zoom level.

    `defaultViewport` is a dict with keys:

    - x (number; optional)

    - y (number; optional)

    - zoom (number; optional)

- deleteElementsAction (dict; optional):
    Delete specific nodes and/or edges by ID. Routes through
    reactFlowInstance.deleteElements() so undo/redo middleware can
    capture the change. Set to { nodeIds: [...], edgeIds: [...] };
    auto-resets to None.

    `deleteElementsAction` is a dict with keys:

    - nodeIds (list of strings; optional):
        IDs of nodes to delete (connected edges are also removed).

    - edgeIds (list of strings; optional):
        IDs of edges to delete.

- deleteKeyCode (string; default 'Backspace'):
    Key code for deleting selected elements (default: 'Backspace',
    None to disable).

- deletedEdges (list of strings; optional):
    IDs of recently deleted edges.

- deletedNodes (list of strings; optional):
    IDs of recently deleted nodes.

- disableKeyboardA11y (boolean; default False):
    Disable keyboard accessibility features.

- doubleClickedEdge (dict; optional):
    The edge that was double-clicked.

    `doubleClickedEdge` is a dict with keys:

    - id (string; optional)

    - source (string; optional)

    - target (string; optional)

- doubleClickedNode (dict; optional):
    The node that was double-clicked.

    `doubleClickedNode` is a dict with keys:

    - id (string; optional)

    - data (dict; optional)

    - position (dict; optional)

- downloadImage (dict; optional):
    Trigger to download the flow as an image. Set to a config object
    to initiate download. Will be reset to None after download.
    Config options: - format: 'png' | 'svg' | 'jpeg' (default: 'png')
    - filename: string (default: 'flow') - quality: number 0-1
    (default: 0.95, for jpeg only) - backgroundColor: string (default:
    '#ffffff') - pixelRatio: number (default: 2, for higher
    resolution).

    `downloadImage` is a dict with keys:

    - format (a value equal to: 'png', 'svg', 'jpeg', 'jpg'; optional)

    - filename (string; optional)

    - quality (number; optional)

    - backgroundColor (string; optional)

    - pixelRatio (number; optional)

- draggedNode (dict; optional):
    The node being dragged.

    `draggedNode` is a dict with keys:

    - id (string; optional)

    - isDragging (boolean; optional)

    - startPosition (dict; optional)

    - currentPosition (dict; optional)

    - endPosition (dict; optional)

- droppedNode (dict; optional):
    Node data from a drop event (drag and drop from external source).
    Contains the type, position, and data of the dropped item. Use
    this in a callback to create a new node at the drop position.

    `droppedNode` is a dict with keys:

    - type (string; optional)

    - position (dict; optional)

        `position` is a dict with keys:

        - x (number; optional)

        - y (number; optional)

    - data (dict; optional)

    - clientX (number; optional)

    - clientY (number; optional)

    - timestamp (number; optional)

- edgeDroppedNode (dict; optional):
    Info about the node created by dropping an edge on empty canvas.
    Contains nodeId, position, sourceNodeId, sourceHandleId,
    handleType, timestamp.

    `edgeDroppedNode` is a dict with keys:

    - nodeId (string; optional)

    - position (dict; optional)

        `position` is a dict with keys:

        - x (number; optional)

        - y (number; optional)

    - sourceNodeId (string; optional)

    - sourceHandleId (string; optional)

    - handleType (string; optional)

    - timestamp (number; optional)

- edges (list of dicts; optional):
    Array of edges defining connections between nodes.

    `edges` is a list of dicts with keys:

    - id (string; required)

    - source (string; required)

    - target (string; required)

    - sourceHandle (string; optional)

    - targetHandle (string; optional)

    - type (string; optional)

    - data (dict; optional)

    - style (dict; optional)

    - className (string; optional)

    - hidden (boolean; optional)

    - selected (boolean; optional)

    - animated (boolean; optional)

    - deletable (boolean; optional)

    - selectable (boolean; optional)

    - focusable (boolean; optional)

    - zIndex (number; optional)

    - ariaLabel (string; optional)

    - interactionWidth (number; optional)

    - label (string; optional)

    - labelStyle (dict; optional)

    - labelShowBg (boolean; optional)

    - labelBgStyle (dict; optional)

    - labelBgPadding (list of numbers; optional)

    - labelBgBorderRadius (number; optional)

    - markerStart (dict; optional)

        `markerStart` is a string

      Or dict with keys:

        - type (string; required)

        - color (string; optional)

        - width (number; optional)

        - height (number; optional)

        - markerUnits (string; optional)

        - orient (string; optional)

        - strokeWidth (number; optional)

    - markerEnd (dict; optional)

        `markerEnd` is a string | dict with keys:

        - type (string; required)

        - color (string; optional)

        - width (number; optional)

        - height (number; optional)

        - markerUnits (string; optional)

        - orient (string; optional)

        - strokeWidth (number; optional)

- edgesFocusable (boolean; default True):
    Enable/disable keyboard focus on edges.

- edgesReconnectable (boolean; default True):
    Allow edges to be reconnected after creation.

- elementsSelectable (boolean; default True):
    Enable/disable the ability to select elements.

- elevateEdgesOnSelect (boolean; default False):
    Raise z-index of selected edges.

- elevateNodesOnSelect (boolean; default True):
    Raise z-index of selected nodes.

- enableUndoRedo (boolean; default False):
    Enable the undo/redo history system. When enabled, node and edge
    changes (add, remove, position drag-stop) are recorded to a
    history stack.

- exportFlowState (boolean; optional):
    Trigger to export the current flow state. Set to True to export.
    After export, this will be reset to False and flowState will be
    populated.

- fitView (boolean; default False):
    Automatically fit all nodes in view on initialization.

- fitViewOptions (dict; optional):
    Options for fitView behavior.

    `fitViewOptions` is a dict with keys:

    - padding (number; optional)

    - includeHiddenNodes (boolean; optional)

    - minZoom (number; optional)

    - maxZoom (number; optional)

    - duration (number; optional)

    - nodes (list of dicts; optional)

        `nodes` is a list of dicts with keys:

        - id (string; optional)

- flowState (dict; optional):
    The exported flow state as a serializable object containing nodes,
    edges, and viewport. This is populated when exportFlowState is
    triggered.

    `flowState` is a dict with keys:

    - nodes (list; optional)

    - edges (list; optional)

    - viewport (dict; optional)

        `viewport` is a dict with keys:

        - x (number; optional)

        - y (number; optional)

        - zoom (number; optional)

- helperLineThreshold (number; optional):
    Distance in pixels within which helper lines snap and appear
    (default: 5).

- helperLines (boolean; optional):
    Enable visual alignment guides (helper lines) when dragging nodes.
    Lines appear when a node aligns with another node's
    top/center/bottom or left/center/right.

- hoveredEdge (dict; optional):
    The edge being hovered.

    `hoveredEdge` is a dict with keys:

    - id (string; optional)

    - source (string; optional)

    - target (string; optional)

- hoveredNode (dict; optional):
    The node being hovered.

    `hoveredNode` is a dict with keys:

    - id (string; optional)

    - data (dict; optional)

- imageDownloaded (dict; optional):
    Information about the last successful image download. Populated
    after a successful downloadImage operation.

    `imageDownloaded` is a dict with keys:

    - filename (string; optional)

    - format (string; optional)

    - timestamp (number; optional)

- initialized (boolean; optional):
    Whether the flow has been initialized.

- lastConnection (dict; optional):
    The last connection that was made.

    `lastConnection` is a dict with keys:

    - source (string; optional)

    - sourceHandle (string; optional)

    - target (string; optional)

    - targetHandle (string; optional)

- lastError (dict; optional):
    Last error that occurred.

    `lastError` is a dict with keys:

    - id (string; optional)

    - message (string; optional)

    - type (string; optional)

    - timestamp (number; optional)

- layoutOptions (string; optional):
    Layout options for arranging nodes using the ELK layout engine
    (JSON string).

- maxZoom (number; default 2):
    Maximum zoom level (default: 2).

- minZoom (number; default 0.5):
    Minimum zoom level (default: 0.5).

- miniMapMaskColor (string; optional):
    Color for the minimap mask (viewport indicator).

- miniMapNodeBorderRadius (number; optional):
    Border radius for minimap nodes.

- miniMapNodeColor (string; optional):
    Color function or string for minimap nodes.

- miniMapNodeStrokeColor (string; optional):
    Stroke color for minimap nodes.

- miniMapPannable (boolean; default False):
    Allow panning by dragging the minimap.

- miniMapPosition (a value equal to: 'top-left', 'top-right', 'bottom-left', 'bottom-right'; default 'bottom-right'):
    Position of the minimap.

- miniMapZoomable (boolean; default False):
    Allow zooming via the minimap.

- multiSelectionKeyCode (string; optional):
    Key code for adding to selection.

- noDragClassName (string; default 'nodrag'):
    CSS class name that prevents dragging when applied to elements.

- noPanClassName (string; default 'nopan'):
    CSS class name that prevents panning when applied to elements.

- noWheelClassName (string; default 'nowheel'):
    CSS class name that prevents wheel zoom when applied to elements.

- nodeConnections (dict; optional):
    Map of nodeId to connection metadata. Each entry has 'incoming'
    and 'outgoing' arrays with edge/node details. Updated
    automatically when edges change.

- nodeExtent (list of list of numberss; optional):
    Limit where nodes can be placed [[minX, minY], [maxX, maxY]].

- nodes (list of dicts; optional):
    Array of nodes to display in the flow.

    `nodes` is a list of dicts with keys:

    - id (string; required)

    - type (string; optional)

    - data (dict; required)

    - position (dict; required)

        `position` is a dict with keys:

        - x (number; required)

        - y (number; required)

    - style (dict; optional)

    - className (string; optional)

    - hidden (boolean; optional)

    - selected (boolean; optional)

    - draggable (boolean; optional)

    - selectable (boolean; optional)

    - connectable (boolean; optional)

    - deletable (boolean; optional)

    - dragHandle (string; optional)

    - width (number; optional)

    - height (number; optional)

    - parentId (string; optional)

    - zIndex (number; optional)

    - extent (string | list of list of numberss; optional)

    - expandParent (boolean; optional)

    - positionAbsolute (dict; optional)

        `positionAbsolute` is a dict with keys:

        - x (number; optional)

        - y (number; optional)

    - ariaLabel (string; optional)

    - focusable (boolean; optional)

    - resizing (boolean; optional)

- nodesConnectable (boolean; default True):
    Enable/disable the ability to make new connections between nodes.

- nodesDraggable (boolean; default True):
    Enable/disable node dragging behavior.

- nodesFocusable (boolean; default True):
    Enable/disable keyboard focus on nodes.

- onlyRenderVisibleElements (boolean; default False):
    Only render nodes and edges that are visible in the viewport.

- panActivationKeyCode (string; default 'Space'):
    Key code to activate pan mode (default: 'Space').

- panOnDrag (boolean | list of numbers; default True):
    Enable/disable panning by dragging. Can be boolean or array of
    mouse buttons [0,1,2].

- panOnScroll (boolean; default False):
    Enable panning by scrolling.

- panOnScrollMode (a value equal to: 'free', 'vertical', 'horizontal'; default 'free'):
    Restrict scroll panning direction: 'free', 'vertical',
    'horizontal'.

- panOnScrollSpeed (number; default 0.5):
    Speed of scroll-based panning (default: 0.5).

- paneClickPosition (dict; optional):
    Position where the pane was clicked.

    `paneClickPosition` is a dict with keys:

    - clientX (number; optional)

    - clientY (number; optional)

- paneContextMenu (dict; optional):
    Context menu info for the pane.

    `paneContextMenu` is a dict with keys:

    - clientX (number; optional)

    - clientY (number; optional)

- panels (list of dicts; optional):
    Array of panel configurations for custom UI overlays.

    `panels` is a list of dicts with keys:

    - position (a value equal to: 'top-left', 'top-right', 'bottom-left', 'bottom-right', 'top-center', 'bottom-center'; optional)

    - children (boolean | number | string | dict | list; optional)

- pasteAction (dict; optional):
    Trigger to paste nodes and edges from clipboard. Set to an object
    with optional offset: { offset: { x: 50, y: 50 } } Will be reset
    to None after pasting.

    `pasteAction` is a dict with keys:

    - offset (dict; optional)

        `offset` is a dict with keys:

        - x (number; optional)

        - y (number; optional)

- pastedElements (dict; optional):
    Information about the last paste operation. Contains the IDs of
    newly created nodes and edges.

    `pastedElements` is a dict with keys:

    - nodeIds (list of strings; optional)

    - edgeIds (list of strings; optional)

    - timestamp (number; optional)

- preventDelete (boolean; default False):
    Enable delete prevention checks.

- preventDeleteEdges (list of strings; optional):
    List of edge IDs that cannot be deleted.

- preventDeleteNodes (list of strings; optional):
    List of node IDs that cannot be deleted.

- preventScrolling (boolean; default True):
    Prevent scrolling on the page when the mouse is over the flow.

- reconnectRadius (number; default 10):
    Radius for reconnection detection (default: 10).

- restoreFlowState (dict; optional):
    Import/restore a previously exported flow state. Set this to a
    flowState object to restore the flow.

    `restoreFlowState` is a dict with keys:

    - nodes (list; optional)

    - edges (list; optional)

    - viewport (dict; optional)

        `viewport` is a dict with keys:

        - x (number; optional)

        - y (number; optional)

        - zoom (number; optional)

- selectNodesOnDrag (boolean; default True):
    Select nodes when dragging over them.

- selectedEdges (list of strings; optional):
    IDs of currently selected edges.

- selectedNodes (list of strings; optional):
    IDs of currently selected nodes.

- selectionKeyCode (string; default 'Shift'):
    Key code for multi-selection box (default: 'Shift').

- selectionMode (a value equal to: 'full', 'partial'; default 'full'):
    Selection mode: 'full' (fully enclosed) or 'partial' (touching).

- selectionOnDrag (boolean; default False):
    Enable selection box by dragging on the pane.

- showBackground (boolean; default True):
    Show/hide the background pattern.

- showControls (boolean; default True):
    Show/hide the control panel.

- showDevTools (boolean; default False):
    Show/hide the developer tools panel.

- showMiniMap (boolean; default True):
    Show/hide the minimap navigation component.

- smartHandles (boolean; optional):
    Enable smart handle positioning. When True, nodes render handles
    on all 4 sides and edges automatically connect to the closest
    handle pair based on relative node positions. This prevents edges
    from wrapping around nodes unnecessarily.

- snapGrid (list of numbers; default [15, 15]):
    The grid size for snapping [x, y] (default: [15, 15]).

- snapToGrid (boolean; default False):
    Whether to snap nodes to a grid when dragging.

- theme (dict; optional):
    Custom theme configuration. Overrides CSS variables for
    fine-grained control. All properties are optional - only specify
    what you want to customize.

    `theme` is a dict with keys:

    - glassBlur (number; optional):
        Glass blur intensity in pixels (default: 12).

    - glassSaturate (number; optional):
        Glass saturation percentage (default: 180).

    - nodeBackground (string; optional):
        Node background color (e.g., 'rgba(255, 255, 255, 0.72)').

    - nodeBorder (string; optional):
        Node border color.

    - nodeText (string; optional):
        Node primary text color.

    - nodeTextSecondary (string; optional):
        Node secondary/subtitle text color.

    - inputNodeBackground (string; optional):
        Input node background color.

    - inputNodeBorder (string; optional):
        Input node border color.

    - inputNodeAccent (string; optional):
        Input node accent color (top bar).

    - outputNodeBackground (string; optional):
        Output node background color.

    - outputNodeBorder (string; optional):
        Output node border color.

    - outputNodeAccent (string; optional):
        Output node accent color (bottom bar).

    - edgeStroke (string; optional):
        Edge stroke color.

    - edgeStrokeSelected (string; optional):
        Selected edge stroke color.

    - edgeStrokeAnimated (string; optional):
        Animated edge stroke color.

    - edgeStrokeWidth (number; optional):
        Edge stroke width in pixels.

    - handleBackground (string; optional):
        Handle background color.

    - handleBorder (string; optional):
        Handle border color.

    - handleConnected (string; optional):
        Connected handle color.

    - backgroundColor (string; optional):
        Flow background color.

    - backgroundPattern (string; optional):
        Background pattern color.

    - selectionBackground (string; optional):
        Selection box background color.

    - selectionBorder (string; optional):
        Selection box border color.

    - borderRadius (number; optional):
        Node border radius in pixels.

- themePreset (a value equal to: 'glass', 'solid', 'minimal'; optional):
    Theme preset: 'glass' (default), 'solid', or 'minimal' - glass:
    Glassmorphism with blur and transparency - solid: Opaque nodes
    with subtle shadows (better for complex backgrounds) - minimal:
    Clean lines with minimal styling.

- toggleCollapseNode (string; optional):
    Set to a group node ID to toggle its collapsed/expanded state.
    When collapsed, child nodes are hidden and boundary edges remap to
    the group. Will be reset to None after processing.

- trackNodeDrag (boolean; default False):
    Track node position during drag (can be expensive).

- trackViewport (boolean; default False):
    Track viewport changes during pan/zoom.

- translateExtent (list of list of numberss; optional):
    Limit the viewport panning extent [[minX, minY], [maxX, maxY]].

- undoRedoAction (dict; optional):
    Trigger an undo or redo action. Set to { action: 'undo' } or {
    action: 'redo' }. Will be reset to None after execution.

    `undoRedoAction` is a dict with keys:

    - action (a value equal to: 'undo', 'redo'; optional)

- undoRedoMaxHistory (number; default 50):
    Maximum number of history snapshots to keep (default: 50).

- undoRedoState (dict; optional):
    Current undo/redo state. Contains canUndo, canRedo, undoCount,
    redoCount. Updated automatically when history changes.

    `undoRedoState` is a dict with keys:

    - canUndo (boolean; optional)

    - canRedo (boolean; optional)

    - undoCount (number; optional)

    - redoCount (number; optional)

- viewport (dict; optional):
    Current viewport state (read-only, updated by callbacks).

    `viewport` is a dict with keys:

    - x (number; optional)

    - y (number; optional)

    - zoom (number; optional)

- viewportAction (dict; optional):
    Trigger viewport actions programmatically. Set to an action object
    to execute. Will be reset to None after execution.  Supported
    actions: - { action: 'fitView', options: {...} } - { action:
    'zoomIn', options: {...} } - { action: 'zoomOut', options: {...} }
    - { action: 'setZoom', zoom: 1.5, options: {...} } - { action:
    'setCenter', x: 100, y: 100, options: {...} } - { action:
    'setViewport', viewport: {x, y, zoom}, options: {...} } - {
    action: 'focusNode', nodeId: 'node-1', zoom: 1.5, duration: 500 }.

    `viewportAction` is a dict with keys:

    - action (a value equal to: 'fitView', 'zoomIn', 'zoomOut', 'setZoom', 'setCenter', 'setViewport', 'focusNode'; optional)

    - nodeId (string; optional)

    - x (number; optional)

    - y (number; optional)

    - zoom (number; optional)

    - duration (number; optional)

    - viewport (dict; optional)

        `viewport` is a dict with keys:

        - x (number; optional)

        - y (number; optional)

        - zoom (number; optional)

    - options (dict; optional)

- viewportMoving (boolean; optional):
    Whether viewport is currently moving (panning/zooming).

- viewportOverlays (list of dicts; optional):
    Array of overlay elements rendered in flow coordinates via
    ViewportPortal. Each overlay moves with the viewport (pan/zoom)
    and is positioned at (x, y) in flow space.

    `viewportOverlays` is a list of dicts with keys:

    - x (number; optional):
        X position in flow coordinates.

    - y (number; optional):
        Y position in flow coordinates.

    - content (string; optional):
        Text content to display.

    - style (dict; optional):
        Custom CSS styles for the overlay div.

- zIndexMode (a value equal to: 'default', 'elevate'; optional):
    Z-index calculation mode. 'default' uses standard stacking.
    'elevate' raises selected nodes and connected edges above all
    other elements.

- zoomActivationKeyCode (string; optional):
    Key code to activate zoom mode.

- zoomOnDoubleClick (boolean; default True):
    Enable zooming by double-clicking.

- zoomOnPinch (boolean; default True):
    Enable zooming by pinching on touch devices.

- zoomOnScroll (boolean; default True):
    Enable zooming by scrolling."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_flows'
    _type = 'DashFlows'
    NodesPosition = TypedDict(
        "NodesPosition",
            {
            "x": NumberType,
            "y": NumberType
        }
    )

    NodesPositionAbsolute = TypedDict(
        "NodesPositionAbsolute",
            {
            "x": NotRequired[NumberType],
            "y": NotRequired[NumberType]
        }
    )

    Nodes = TypedDict(
        "Nodes",
            {
            "id": str,
            "type": NotRequired[str],
            "data": dict,
            "position": "NodesPosition",
            "style": NotRequired[dict],
            "className": NotRequired[str],
            "hidden": NotRequired[bool],
            "selected": NotRequired[bool],
            "draggable": NotRequired[bool],
            "selectable": NotRequired[bool],
            "connectable": NotRequired[bool],
            "deletable": NotRequired[bool],
            "dragHandle": NotRequired[str],
            "width": NotRequired[NumberType],
            "height": NotRequired[NumberType],
            "parentId": NotRequired[str],
            "zIndex": NotRequired[NumberType],
            "extent": NotRequired[typing.Union[str, typing.Sequence[typing.Sequence[NumberType]]]],
            "expandParent": NotRequired[bool],
            "positionAbsolute": NotRequired["NodesPositionAbsolute"],
            "ariaLabel": NotRequired[str],
            "focusable": NotRequired[bool],
            "resizing": NotRequired[bool]
        }
    )

    EdgesMarkerStart = TypedDict(
        "EdgesMarkerStart",
            {
            "type": str,
            "color": NotRequired[str],
            "width": NotRequired[NumberType],
            "height": NotRequired[NumberType],
            "markerUnits": NotRequired[str],
            "orient": NotRequired[str],
            "strokeWidth": NotRequired[NumberType]
        }
    )

    EdgesMarkerEnd = TypedDict(
        "EdgesMarkerEnd",
            {
            "type": str,
            "color": NotRequired[str],
            "width": NotRequired[NumberType],
            "height": NotRequired[NumberType],
            "markerUnits": NotRequired[str],
            "orient": NotRequired[str],
            "strokeWidth": NotRequired[NumberType]
        }
    )

    Edges = TypedDict(
        "Edges",
            {
            "id": str,
            "source": str,
            "target": str,
            "sourceHandle": NotRequired[str],
            "targetHandle": NotRequired[str],
            "type": NotRequired[str],
            "data": NotRequired[dict],
            "style": NotRequired[dict],
            "className": NotRequired[str],
            "hidden": NotRequired[bool],
            "selected": NotRequired[bool],
            "animated": NotRequired[bool],
            "deletable": NotRequired[bool],
            "selectable": NotRequired[bool],
            "focusable": NotRequired[bool],
            "zIndex": NotRequired[NumberType],
            "ariaLabel": NotRequired[str],
            "interactionWidth": NotRequired[NumberType],
            "label": NotRequired[str],
            "labelStyle": NotRequired[dict],
            "labelShowBg": NotRequired[bool],
            "labelBgStyle": NotRequired[dict],
            "labelBgPadding": NotRequired[typing.Sequence[NumberType]],
            "labelBgBorderRadius": NotRequired[NumberType],
            "markerStart": NotRequired[typing.Union[str, "EdgesMarkerStart"]],
            "markerEnd": NotRequired[typing.Union[str, "EdgesMarkerEnd"]]
        }
    )

    DefaultViewport = TypedDict(
        "DefaultViewport",
            {
            "x": NotRequired[NumberType],
            "y": NotRequired[NumberType],
            "zoom": NotRequired[NumberType]
        }
    )

    Viewport = TypedDict(
        "Viewport",
            {
            "x": NotRequired[NumberType],
            "y": NotRequired[NumberType],
            "zoom": NotRequired[NumberType]
        }
    )

    FitViewOptionsNodes = TypedDict(
        "FitViewOptionsNodes",
            {
            "id": NotRequired[str]
        }
    )

    FitViewOptions = TypedDict(
        "FitViewOptions",
            {
            "padding": NotRequired[NumberType],
            "includeHiddenNodes": NotRequired[bool],
            "minZoom": NotRequired[NumberType],
            "maxZoom": NotRequired[NumberType],
            "duration": NotRequired[NumberType],
            "nodes": NotRequired[typing.Sequence["FitViewOptionsNodes"]]
        }
    )

    DefaultEdgeOptions = TypedDict(
        "DefaultEdgeOptions",
            {
            "type": NotRequired[str],
            "style": NotRequired[dict],
            "animated": NotRequired[bool],
            "markerStart": NotRequired[dict],
            "markerEnd": NotRequired[dict]
        }
    )

    ConnectionRules = TypedDict(
        "ConnectionRules",
            {
            "allowSelfConnection": NotRequired[bool],
            "allowDuplicateConnections": NotRequired[bool],
            "validSourceTypes": NotRequired[typing.Sequence[str]],
            "validTargetTypes": NotRequired[typing.Sequence[str]]
        }
    )

    Theme = TypedDict(
        "Theme",
            {
            "glassBlur": NotRequired[NumberType],
            "glassSaturate": NotRequired[NumberType],
            "nodeBackground": NotRequired[str],
            "nodeBorder": NotRequired[str],
            "nodeText": NotRequired[str],
            "nodeTextSecondary": NotRequired[str],
            "inputNodeBackground": NotRequired[str],
            "inputNodeBorder": NotRequired[str],
            "inputNodeAccent": NotRequired[str],
            "outputNodeBackground": NotRequired[str],
            "outputNodeBorder": NotRequired[str],
            "outputNodeAccent": NotRequired[str],
            "edgeStroke": NotRequired[str],
            "edgeStrokeSelected": NotRequired[str],
            "edgeStrokeAnimated": NotRequired[str],
            "edgeStrokeWidth": NotRequired[NumberType],
            "handleBackground": NotRequired[str],
            "handleBorder": NotRequired[str],
            "handleConnected": NotRequired[str],
            "backgroundColor": NotRequired[str],
            "backgroundPattern": NotRequired[str],
            "selectionBackground": NotRequired[str],
            "selectionBorder": NotRequired[str],
            "borderRadius": NotRequired[NumberType]
        }
    )

    Panels = TypedDict(
        "Panels",
            {
            "position": NotRequired[Literal["top-left", "top-right", "bottom-left", "bottom-right", "top-center", "bottom-center"]],
            "children": NotRequired[typing.Any]
        }
    )

    FlowStateViewport = TypedDict(
        "FlowStateViewport",
            {
            "x": NotRequired[NumberType],
            "y": NotRequired[NumberType],
            "zoom": NotRequired[NumberType]
        }
    )

    FlowState = TypedDict(
        "FlowState",
            {
            "nodes": NotRequired[typing.Sequence],
            "edges": NotRequired[typing.Sequence],
            "viewport": NotRequired["FlowStateViewport"]
        }
    )

    RestoreFlowStateViewport = TypedDict(
        "RestoreFlowStateViewport",
            {
            "x": NotRequired[NumberType],
            "y": NotRequired[NumberType],
            "zoom": NotRequired[NumberType]
        }
    )

    RestoreFlowState = TypedDict(
        "RestoreFlowState",
            {
            "nodes": NotRequired[typing.Sequence],
            "edges": NotRequired[typing.Sequence],
            "viewport": NotRequired["RestoreFlowStateViewport"]
        }
    )

    ViewportActionViewport = TypedDict(
        "ViewportActionViewport",
            {
            "x": NotRequired[NumberType],
            "y": NotRequired[NumberType],
            "zoom": NotRequired[NumberType]
        }
    )

    ViewportAction = TypedDict(
        "ViewportAction",
            {
            "action": NotRequired[Literal["fitView", "zoomIn", "zoomOut", "setZoom", "setCenter", "setViewport", "focusNode"]],
            "nodeId": NotRequired[str],
            "x": NotRequired[NumberType],
            "y": NotRequired[NumberType],
            "zoom": NotRequired[NumberType],
            "duration": NotRequired[NumberType],
            "viewport": NotRequired["ViewportActionViewport"],
            "options": NotRequired[dict]
        }
    )

    DownloadImage = TypedDict(
        "DownloadImage",
            {
            "format": NotRequired[Literal["png", "svg", "jpeg", "jpg"]],
            "filename": NotRequired[str],
            "quality": NotRequired[NumberType],
            "backgroundColor": NotRequired[str],
            "pixelRatio": NotRequired[NumberType]
        }
    )

    ImageDownloaded = TypedDict(
        "ImageDownloaded",
            {
            "filename": NotRequired[str],
            "format": NotRequired[str],
            "timestamp": NotRequired[NumberType]
        }
    )

    PasteActionOffset = TypedDict(
        "PasteActionOffset",
            {
            "x": NotRequired[NumberType],
            "y": NotRequired[NumberType]
        }
    )

    PasteAction = TypedDict(
        "PasteAction",
            {
            "offset": NotRequired["PasteActionOffset"]
        }
    )

    Clipboard = TypedDict(
        "Clipboard",
            {
            "nodes": NotRequired[typing.Sequence],
            "edges": NotRequired[typing.Sequence],
            "timestamp": NotRequired[NumberType]
        }
    )

    PastedElements = TypedDict(
        "PastedElements",
            {
            "nodeIds": NotRequired[typing.Sequence[str]],
            "edgeIds": NotRequired[typing.Sequence[str]],
            "timestamp": NotRequired[NumberType]
        }
    )

    LastError = TypedDict(
        "LastError",
            {
            "id": NotRequired[str],
            "message": NotRequired[str],
            "type": NotRequired[str],
            "timestamp": NotRequired[NumberType]
        }
    )

    LastConnection = TypedDict(
        "LastConnection",
            {
            "source": NotRequired[str],
            "sourceHandle": NotRequired[str],
            "target": NotRequired[str],
            "targetHandle": NotRequired[str]
        }
    )

    ConnectionStartHandle = TypedDict(
        "ConnectionStartHandle",
            {
            "nodeId": NotRequired[str],
            "handleId": NotRequired[str],
            "handleType": NotRequired[str]
        }
    )

    ClickedNode = TypedDict(
        "ClickedNode",
            {
            "id": NotRequired[str],
            "data": NotRequired[dict],
            "position": NotRequired[dict]
        }
    )

    DoubleClickedNode = TypedDict(
        "DoubleClickedNode",
            {
            "id": NotRequired[str],
            "data": NotRequired[dict],
            "position": NotRequired[dict]
        }
    )

    ContextMenuNode = TypedDict(
        "ContextMenuNode",
            {
            "id": NotRequired[str],
            "data": NotRequired[dict],
            "position": NotRequired[dict],
            "clientX": NotRequired[NumberType],
            "clientY": NotRequired[NumberType]
        }
    )

    DroppedNodePosition = TypedDict(
        "DroppedNodePosition",
            {
            "x": NotRequired[NumberType],
            "y": NotRequired[NumberType]
        }
    )

    DroppedNode = TypedDict(
        "DroppedNode",
            {
            "type": NotRequired[str],
            "position": NotRequired["DroppedNodePosition"],
            "data": NotRequired[dict],
            "clientX": NotRequired[NumberType],
            "clientY": NotRequired[NumberType],
            "timestamp": NotRequired[NumberType]
        }
    )

    DraggedNode = TypedDict(
        "DraggedNode",
            {
            "id": NotRequired[str],
            "isDragging": NotRequired[bool],
            "startPosition": NotRequired[dict],
            "currentPosition": NotRequired[dict],
            "endPosition": NotRequired[dict]
        }
    )

    HoveredNode = TypedDict(
        "HoveredNode",
            {
            "id": NotRequired[str],
            "data": NotRequired[dict]
        }
    )

    ClickedEdge = TypedDict(
        "ClickedEdge",
            {
            "id": NotRequired[str],
            "source": NotRequired[str],
            "target": NotRequired[str]
        }
    )

    DoubleClickedEdge = TypedDict(
        "DoubleClickedEdge",
            {
            "id": NotRequired[str],
            "source": NotRequired[str],
            "target": NotRequired[str]
        }
    )

    ContextMenuEdge = TypedDict(
        "ContextMenuEdge",
            {
            "id": NotRequired[str],
            "source": NotRequired[str],
            "target": NotRequired[str],
            "clientX": NotRequired[NumberType],
            "clientY": NotRequired[NumberType]
        }
    )

    HoveredEdge = TypedDict(
        "HoveredEdge",
            {
            "id": NotRequired[str],
            "source": NotRequired[str],
            "target": NotRequired[str]
        }
    )

    PaneClickPosition = TypedDict(
        "PaneClickPosition",
            {
            "clientX": NotRequired[NumberType],
            "clientY": NotRequired[NumberType]
        }
    )

    PaneContextMenu = TypedDict(
        "PaneContextMenu",
            {
            "clientX": NotRequired[NumberType],
            "clientY": NotRequired[NumberType]
        }
    )

    EdgeDroppedNodePosition = TypedDict(
        "EdgeDroppedNodePosition",
            {
            "x": NotRequired[NumberType],
            "y": NotRequired[NumberType]
        }
    )

    EdgeDroppedNode = TypedDict(
        "EdgeDroppedNode",
            {
            "nodeId": NotRequired[str],
            "position": NotRequired["EdgeDroppedNodePosition"],
            "sourceNodeId": NotRequired[str],
            "sourceHandleId": NotRequired[str],
            "handleType": NotRequired[str],
            "timestamp": NotRequired[NumberType]
        }
    )

    UndoRedoAction = TypedDict(
        "UndoRedoAction",
            {
            "action": NotRequired[Literal["undo", "redo"]]
        }
    )

    UndoRedoState = TypedDict(
        "UndoRedoState",
            {
            "canUndo": NotRequired[bool],
            "canRedo": NotRequired[bool],
            "undoCount": NotRequired[NumberType],
            "redoCount": NotRequired[NumberType]
        }
    )

    ComputeAction = TypedDict(
        "ComputeAction",
            {
            "action": NotRequired[Literal["compute", "computeNode"]],
            "nodeId": NotRequired[str],
            "inputData": NotRequired[dict]
        }
    )

    ComputeResult = TypedDict(
        "ComputeResult",
            {
            "traversalOrder": NotRequired[typing.Sequence[str]],
            "nodeInputs": NotRequired[dict],
            "timestamp": NotRequired[NumberType]
        }
    )

    ViewportOverlays = TypedDict(
        "ViewportOverlays",
            {
            "x": NotRequired[NumberType],
            "y": NotRequired[NumberType],
            "content": NotRequired[str],
            "style": NotRequired[dict]
        }
    )

    DeleteElementsAction = TypedDict(
        "DeleteElementsAction",
            {
            "nodeIds": NotRequired[typing.Sequence[str]],
            "edgeIds": NotRequired[typing.Sequence[str]]
        }
    )


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        nodes: typing.Optional[typing.Sequence["Nodes"]] = None,
        edges: typing.Optional[typing.Sequence["Edges"]] = None,
        defaultViewport: typing.Optional["DefaultViewport"] = None,
        viewport: typing.Optional["Viewport"] = None,
        viewportMoving: typing.Optional[bool] = None,
        minZoom: typing.Optional[NumberType] = None,
        maxZoom: typing.Optional[NumberType] = None,
        snapToGrid: typing.Optional[bool] = None,
        snapGrid: typing.Optional[typing.Sequence[NumberType]] = None,
        translateExtent: typing.Optional[typing.Sequence[typing.Sequence[NumberType]]] = None,
        nodeExtent: typing.Optional[typing.Sequence[typing.Sequence[NumberType]]] = None,
        onlyRenderVisibleElements: typing.Optional[bool] = None,
        preventScrolling: typing.Optional[bool] = None,
        fitView: typing.Optional[bool] = None,
        fitViewOptions: typing.Optional["FitViewOptions"] = None,
        nodesDraggable: typing.Optional[bool] = None,
        nodesConnectable: typing.Optional[bool] = None,
        nodesFocusable: typing.Optional[bool] = None,
        edgesFocusable: typing.Optional[bool] = None,
        elementsSelectable: typing.Optional[bool] = None,
        autoPanOnConnect: typing.Optional[bool] = None,
        autoPanOnNodeDrag: typing.Optional[bool] = None,
        autoPanSpeed: typing.Optional[NumberType] = None,
        panOnDrag: typing.Optional[typing.Union[bool, typing.Sequence[NumberType]]] = None,
        panOnScroll: typing.Optional[bool] = None,
        panOnScrollSpeed: typing.Optional[NumberType] = None,
        panOnScrollMode: typing.Optional[Literal["free", "vertical", "horizontal"]] = None,
        zoomOnScroll: typing.Optional[bool] = None,
        zoomOnPinch: typing.Optional[bool] = None,
        zoomOnDoubleClick: typing.Optional[bool] = None,
        selectNodesOnDrag: typing.Optional[bool] = None,
        selectionOnDrag: typing.Optional[bool] = None,
        selectionMode: typing.Optional[Literal["full", "partial"]] = None,
        connectOnClick: typing.Optional[bool] = None,
        connectionMode: typing.Optional[Literal["strict", "loose"]] = None,
        elevateNodesOnSelect: typing.Optional[bool] = None,
        elevateEdgesOnSelect: typing.Optional[bool] = None,
        zIndexMode: typing.Optional[Literal["default", "elevate"]] = None,
        autoPanOnNodeFocus: typing.Optional[bool] = None,
        defaultEdgeOptions: typing.Optional["DefaultEdgeOptions"] = None,
        defaultMarkerColor: typing.Optional[str] = None,
        edgesReconnectable: typing.Optional[bool] = None,
        reconnectRadius: typing.Optional[NumberType] = None,
        connectionLineStyle: typing.Optional[dict] = None,
        connectionLineType: typing.Optional[Literal["bezier", "straight", "step", "smoothstep", "simplebezier"]] = None,
        connectionRadius: typing.Optional[NumberType] = None,
        connectionDragThreshold: typing.Optional[NumberType] = None,
        connectionRules: typing.Optional["ConnectionRules"] = None,
        smartHandles: typing.Optional[bool] = None,
        deleteKeyCode: typing.Optional[str] = None,
        selectionKeyCode: typing.Optional[str] = None,
        multiSelectionKeyCode: typing.Optional[str] = None,
        zoomActivationKeyCode: typing.Optional[str] = None,
        panActivationKeyCode: typing.Optional[str] = None,
        disableKeyboardA11y: typing.Optional[bool] = None,
        noPanClassName: typing.Optional[str] = None,
        noDragClassName: typing.Optional[str] = None,
        noWheelClassName: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        className: typing.Optional[str] = None,
        colorMode: typing.Optional[Literal["light", "dark", "system"]] = None,
        themePreset: typing.Optional[Literal["glass", "solid", "minimal"]] = None,
        colorScheme: typing.Optional[Literal["default", "ocean", "forest", "sunset", "midnight", "rose"]] = None,
        theme: typing.Optional["Theme"] = None,
        showMiniMap: typing.Optional[bool] = None,
        showControls: typing.Optional[bool] = None,
        showBackground: typing.Optional[bool] = None,
        showDevTools: typing.Optional[bool] = None,
        controlsShowZoom: typing.Optional[bool] = None,
        controlsShowFitView: typing.Optional[bool] = None,
        controlsShowInteractive: typing.Optional[bool] = None,
        controlsPosition: typing.Optional[Literal["top-left", "top-right", "bottom-left", "bottom-right", "top-center", "bottom-center"]] = None,
        miniMapNodeColor: typing.Optional[str] = None,
        miniMapNodeStrokeColor: typing.Optional[str] = None,
        miniMapNodeBorderRadius: typing.Optional[NumberType] = None,
        miniMapMaskColor: typing.Optional[str] = None,
        miniMapPosition: typing.Optional[Literal["top-left", "top-right", "bottom-left", "bottom-right"]] = None,
        miniMapPannable: typing.Optional[bool] = None,
        miniMapZoomable: typing.Optional[bool] = None,
        backgroundVariant: typing.Optional[Literal["dots", "lines", "cross"]] = None,
        backgroundGap: typing.Optional[typing.Union[NumberType, typing.Sequence[NumberType]]] = None,
        backgroundSize: typing.Optional[NumberType] = None,
        backgroundColor: typing.Optional[str] = None,
        panels: typing.Optional[typing.Sequence["Panels"]] = None,
        layoutOptions: typing.Optional[str] = None,
        trackNodeDrag: typing.Optional[bool] = None,
        trackViewport: typing.Optional[bool] = None,
        preventDelete: typing.Optional[bool] = None,
        preventDeleteNodes: typing.Optional[typing.Sequence[str]] = None,
        preventDeleteEdges: typing.Optional[typing.Sequence[str]] = None,
        exportFlowState: typing.Optional[bool] = None,
        flowState: typing.Optional["FlowState"] = None,
        restoreFlowState: typing.Optional["RestoreFlowState"] = None,
        viewportAction: typing.Optional["ViewportAction"] = None,
        downloadImage: typing.Optional["DownloadImage"] = None,
        imageDownloaded: typing.Optional["ImageDownloaded"] = None,
        copyAction: typing.Optional[bool] = None,
        pasteAction: typing.Optional["PasteAction"] = None,
        clipboard: typing.Optional["Clipboard"] = None,
        pastedElements: typing.Optional["PastedElements"] = None,
        initialized: typing.Optional[bool] = None,
        lastError: typing.Optional["LastError"] = None,
        selectedNodes: typing.Optional[typing.Sequence[str]] = None,
        selectedEdges: typing.Optional[typing.Sequence[str]] = None,
        lastConnection: typing.Optional["LastConnection"] = None,
        connectionStartHandle: typing.Optional["ConnectionStartHandle"] = None,
        clickedNode: typing.Optional["ClickedNode"] = None,
        doubleClickedNode: typing.Optional["DoubleClickedNode"] = None,
        contextMenuNode: typing.Optional["ContextMenuNode"] = None,
        droppedNode: typing.Optional["DroppedNode"] = None,
        draggedNode: typing.Optional["DraggedNode"] = None,
        hoveredNode: typing.Optional["HoveredNode"] = None,
        clickedEdge: typing.Optional["ClickedEdge"] = None,
        doubleClickedEdge: typing.Optional["DoubleClickedEdge"] = None,
        contextMenuEdge: typing.Optional["ContextMenuEdge"] = None,
        hoveredEdge: typing.Optional["HoveredEdge"] = None,
        paneClickPosition: typing.Optional["PaneClickPosition"] = None,
        paneContextMenu: typing.Optional["PaneContextMenu"] = None,
        deletedNodes: typing.Optional[typing.Sequence[str]] = None,
        deletedEdges: typing.Optional[typing.Sequence[str]] = None,
        helperLines: typing.Optional[bool] = None,
        helperLineThreshold: typing.Optional[NumberType] = None,
        addNodeOnEdgeDrop: typing.Optional[bool] = None,
        edgeDroppedNode: typing.Optional["EdgeDroppedNode"] = None,
        nodeConnections: typing.Optional[dict] = None,
        ariaLabelConfig: typing.Optional[dict] = None,
        animateLayout: typing.Optional[bool] = None,
        animateLayoutDuration: typing.Optional[NumberType] = None,
        enableUndoRedo: typing.Optional[bool] = None,
        undoRedoMaxHistory: typing.Optional[NumberType] = None,
        undoRedoAction: typing.Optional["UndoRedoAction"] = None,
        undoRedoState: typing.Optional["UndoRedoState"] = None,
        computeAction: typing.Optional["ComputeAction"] = None,
        computeResult: typing.Optional["ComputeResult"] = None,
        viewportOverlays: typing.Optional[typing.Sequence["ViewportOverlays"]] = None,
        toggleCollapseNode: typing.Optional[str] = None,
        collapsedGroups: typing.Optional[typing.Sequence[str]] = None,
        deleteElementsAction: typing.Optional["DeleteElementsAction"] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'addNodeOnEdgeDrop', 'animateLayout', 'animateLayoutDuration', 'ariaLabelConfig', 'autoPanOnConnect', 'autoPanOnNodeDrag', 'autoPanOnNodeFocus', 'autoPanSpeed', 'backgroundColor', 'backgroundGap', 'backgroundSize', 'backgroundVariant', 'className', 'clickedEdge', 'clickedNode', 'clipboard', 'collapsedGroups', 'colorMode', 'colorScheme', 'computeAction', 'computeResult', 'connectOnClick', 'connectionDragThreshold', 'connectionLineStyle', 'connectionLineType', 'connectionMode', 'connectionRadius', 'connectionRules', 'connectionStartHandle', 'contextMenuEdge', 'contextMenuNode', 'controlsPosition', 'controlsShowFitView', 'controlsShowInteractive', 'controlsShowZoom', 'copyAction', 'defaultEdgeOptions', 'defaultMarkerColor', 'defaultViewport', 'deleteElementsAction', 'deleteKeyCode', 'deletedEdges', 'deletedNodes', 'disableKeyboardA11y', 'doubleClickedEdge', 'doubleClickedNode', 'downloadImage', 'draggedNode', 'droppedNode', 'edgeDroppedNode', 'edges', 'edgesFocusable', 'edgesReconnectable', 'elementsSelectable', 'elevateEdgesOnSelect', 'elevateNodesOnSelect', 'enableUndoRedo', 'exportFlowState', 'fitView', 'fitViewOptions', 'flowState', 'helperLineThreshold', 'helperLines', 'hoveredEdge', 'hoveredNode', 'imageDownloaded', 'initialized', 'lastConnection', 'lastError', 'layoutOptions', 'maxZoom', 'minZoom', 'miniMapMaskColor', 'miniMapNodeBorderRadius', 'miniMapNodeColor', 'miniMapNodeStrokeColor', 'miniMapPannable', 'miniMapPosition', 'miniMapZoomable', 'multiSelectionKeyCode', 'noDragClassName', 'noPanClassName', 'noWheelClassName', 'nodeConnections', 'nodeExtent', 'nodes', 'nodesConnectable', 'nodesDraggable', 'nodesFocusable', 'onlyRenderVisibleElements', 'panActivationKeyCode', 'panOnDrag', 'panOnScroll', 'panOnScrollMode', 'panOnScrollSpeed', 'paneClickPosition', 'paneContextMenu', 'panels', 'pasteAction', 'pastedElements', 'preventDelete', 'preventDeleteEdges', 'preventDeleteNodes', 'preventScrolling', 'reconnectRadius', 'restoreFlowState', 'selectNodesOnDrag', 'selectedEdges', 'selectedNodes', 'selectionKeyCode', 'selectionMode', 'selectionOnDrag', 'showBackground', 'showControls', 'showDevTools', 'showMiniMap', 'smartHandles', 'snapGrid', 'snapToGrid', 'style', 'theme', 'themePreset', 'toggleCollapseNode', 'trackNodeDrag', 'trackViewport', 'translateExtent', 'undoRedoAction', 'undoRedoMaxHistory', 'undoRedoState', 'viewport', 'viewportAction', 'viewportMoving', 'viewportOverlays', 'zIndexMode', 'zoomActivationKeyCode', 'zoomOnDoubleClick', 'zoomOnPinch', 'zoomOnScroll']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'addNodeOnEdgeDrop', 'animateLayout', 'animateLayoutDuration', 'ariaLabelConfig', 'autoPanOnConnect', 'autoPanOnNodeDrag', 'autoPanOnNodeFocus', 'autoPanSpeed', 'backgroundColor', 'backgroundGap', 'backgroundSize', 'backgroundVariant', 'className', 'clickedEdge', 'clickedNode', 'clipboard', 'collapsedGroups', 'colorMode', 'colorScheme', 'computeAction', 'computeResult', 'connectOnClick', 'connectionDragThreshold', 'connectionLineStyle', 'connectionLineType', 'connectionMode', 'connectionRadius', 'connectionRules', 'connectionStartHandle', 'contextMenuEdge', 'contextMenuNode', 'controlsPosition', 'controlsShowFitView', 'controlsShowInteractive', 'controlsShowZoom', 'copyAction', 'defaultEdgeOptions', 'defaultMarkerColor', 'defaultViewport', 'deleteElementsAction', 'deleteKeyCode', 'deletedEdges', 'deletedNodes', 'disableKeyboardA11y', 'doubleClickedEdge', 'doubleClickedNode', 'downloadImage', 'draggedNode', 'droppedNode', 'edgeDroppedNode', 'edges', 'edgesFocusable', 'edgesReconnectable', 'elementsSelectable', 'elevateEdgesOnSelect', 'elevateNodesOnSelect', 'enableUndoRedo', 'exportFlowState', 'fitView', 'fitViewOptions', 'flowState', 'helperLineThreshold', 'helperLines', 'hoveredEdge', 'hoveredNode', 'imageDownloaded', 'initialized', 'lastConnection', 'lastError', 'layoutOptions', 'maxZoom', 'minZoom', 'miniMapMaskColor', 'miniMapNodeBorderRadius', 'miniMapNodeColor', 'miniMapNodeStrokeColor', 'miniMapPannable', 'miniMapPosition', 'miniMapZoomable', 'multiSelectionKeyCode', 'noDragClassName', 'noPanClassName', 'noWheelClassName', 'nodeConnections', 'nodeExtent', 'nodes', 'nodesConnectable', 'nodesDraggable', 'nodesFocusable', 'onlyRenderVisibleElements', 'panActivationKeyCode', 'panOnDrag', 'panOnScroll', 'panOnScrollMode', 'panOnScrollSpeed', 'paneClickPosition', 'paneContextMenu', 'panels', 'pasteAction', 'pastedElements', 'preventDelete', 'preventDeleteEdges', 'preventDeleteNodes', 'preventScrolling', 'reconnectRadius', 'restoreFlowState', 'selectNodesOnDrag', 'selectedEdges', 'selectedNodes', 'selectionKeyCode', 'selectionMode', 'selectionOnDrag', 'showBackground', 'showControls', 'showDevTools', 'showMiniMap', 'smartHandles', 'snapGrid', 'snapToGrid', 'style', 'theme', 'themePreset', 'toggleCollapseNode', 'trackNodeDrag', 'trackViewport', 'translateExtent', 'undoRedoAction', 'undoRedoMaxHistory', 'undoRedoState', 'viewport', 'viewportAction', 'viewportMoving', 'viewportOverlays', 'zIndexMode', 'zoomActivationKeyCode', 'zoomOnDoubleClick', 'zoomOnPinch', 'zoomOnScroll']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(DashFlows, self).__init__(**args)

setattr(DashFlows, "__init__", _explicitize_args(DashFlows.__init__))
