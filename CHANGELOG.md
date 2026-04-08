# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-04-03

### Added

#### React Flow 12.10.1 Pass-Through Props
- **connectionDragThreshold** (number): Minimum drag distance in pixels before a connection line appears, preventing accidental connections
- **zIndexMode** (`"default"` / `"elevate"`): Selected elements automatically elevate above others when set to `"elevate"`
- **autoPanOnNodeFocus** (boolean): Viewport auto-pans when focusing nodes via Tab key for improved keyboard navigation

#### Floating Edges
- **FloatingEdge component**: New `floating` edge type that connects to the nearest point on each node's border instead of fixed handle positions
- Uses `useInternalNode` hook for real-time border intersection calculation
- Natural-looking connections for arbitrary node layouts

#### Helper Lines (Alignment Guides)
- **helperLines** (boolean): Visual alignment guides appear when dragging nodes near other nodes
- **helperLineThreshold** (number, default 5): Snap distance in pixels for alignment detection
- Automatic snapping to horizontal and vertical alignment

#### Add Node on Edge Drop
- **addNodeOnEdgeDrop** (boolean): Drag a connection from a handle and drop on empty canvas to create a new node
- **edgeDroppedNode** (output): Callback data with `nodeId`, `position`, `source`, and `handleType` of the dropped connection

#### Node Connections Tracking
- **nodeConnections** (output): Real-time map of `nodeId` to `{incoming: [...], outgoing: [...]}` with edge/node details
- Automatically updated when edges change

#### Undo/Redo System
- **enableUndoRedo** (boolean): Enable history tracking for node/edge changes
- **undoRedoMaxHistory** (number, default 50): Maximum number of history snapshots
- **undoRedoAction** (`{action: 'undo' | 'redo'}`): Trigger undo or redo from callbacks
- **undoRedoState** (output): `{canUndo, canRedo, undoCount, redoCount}` for UI state
- Tracks node position changes, additions, deletions, and edge connections
- Uses React Flow's `experimental_useOnNodesChangeMiddleware` and `experimental_useOnEdgesChangeMiddleware`

#### Computing Flows (Graph Traversal)
- **computeAction** (`{action: 'compute' | 'computeNode', nodeId?, inputData?}`): Trigger topological sort computation
- **computeResult** (output): `{traversalOrder, nodeInputs, timestamp}` with Kahn's algorithm results
- JavaScript-side topological sort; Python handles all business logic and value propagation

#### Sub-flows (Collapsible Group Nodes)
- **toggleCollapseNode** (string): Set to a group node ID to toggle its collapse/expand state
- **collapsedGroups** (output): Array of currently collapsed group node IDs
- Double-click a group node to toggle collapse
- Child nodes and internal edges hidden when collapsed; group shrinks to compact view
- External edges remain connected at the group level
- GroupNode supports `data.collapsedWidth` and `data.collapsedHeight` for compact dimensions

#### ViewportPortal (Floating Annotations)
- **viewportOverlays** (array): Floating overlays anchored to flow coordinates that move with pan/zoom
- Each overlay: `{x, y, content, style}` — positioned in flow space, not screen space
- Add, remove, and edit annotations dynamically via callbacks

#### Animated Layout Transitions
- **animateLayout** (boolean): Smooth animated transitions when applying ELK layouts
- **animateLayoutDuration** (number, default 300): Animation duration in milliseconds
- Ease-out cubic interpolation from current to target positions

#### Accessibility (ARIA Support)
- **ariaLabelConfig** (object): Custom ARIA labels for `nodes`, `edges`, `controls`, `minimap` regions
- Per-node/edge `ariaLabel` in data for screen reader support
- **nodesFocusable** / **edgesFocusable** (boolean): Enable Tab key navigation through nodes and edges
- **disableKeyboardA11y** (boolean): Disable keyboard shortcuts when needed

#### Resize Constraints
- ResizableNode and GroupNode now support constraint props in `data`:
  - `keepAspectRatio` (boolean): Lock aspect ratio during resize
  - `minWidth` / `minHeight` (number): Minimum dimensions in pixels
  - `maxWidth` / `maxHeight` (number): Maximum dimensions in pixels

#### Glass Connection Line
- Custom glass morphism styled connection line preview while dragging new edges
- Blue dashed line with glow and drop shadow effect

#### Type-Colored MiniMap
- Custom MiniMap node rendering with colors based on node type (green=input, blue=default, purple=output, amber=toolbar)

#### EdgeToolbar on ButtonEdge
- ButtonEdge now supports `data.showToolbar` (boolean) to display an EdgeToolbar on selection
- Toolbar includes edit (inline label editing) and delete actions
- Custom styling via `data.toolbarStyle`

#### Smart Handle Positioning
- **smartHandles** (boolean): Automatically routes edges to the closest side of each node
- Renders handles on all 4 sides and selects optimal connection points
- Alternative manual control via `data.sourcePosition` / `data.targetPosition` per node

#### Delete Elements Action
- **deleteElementsAction** (`{nodeIds: [...], edgeIds: [...]}`): Programmatic deletion routed through `reactFlowInstance.deleteElements()` for undo/redo compatibility

#### New Examples
- **Example 24**: `24_smart_handles.py` — Smart handle auto-routing demo
- **Example 25**: `25_phase1_features.py` — Phase 1 feature showcase (drag threshold, zIndex, auto-pan, EdgeToolbar)
- **Example 26**: `26_floating_edges.py` — Floating edge border intersection demo
- **Example 27**: `27_helper_lines.py` — Alignment guide and snap demo
- **Example 28**: `28_add_node_on_drop.py` — Add node on edge drop with connection tracking
- **Example 29**: `29_accessibility.py` — ARIA labels and keyboard navigation
- **Example 30**: `30_resize_constraints.py` — Aspect ratio and min/max resize limits
- **Example 31**: `31_animated_layout.py` — Smooth layout transitions with ELK
- **Example 32**: `32_undo_redo.py` — Full undo/redo system demo
- **Example 33**: `33_computing_flows.py` — Topological sort and data flow computation
- **Example 34**: `34_viewport_portal.py` — Floating viewport annotations
- **Example 35**: `35_subflows.py` — Collapsible group nodes with boundary edge remapping

#### New Python Wrapper Components (auto-generated)
- `AnimatedSvgEdge`, `ButtonEdge`, `ButtonHandle`, `DataEdge`, `DefaultNode`
- `FloatingEdge`, `GroupNode`, `InputNode`, `NodeSearch`, `NodeStatusIndicator`
- `NodeTooltip`, `OutputNode`, `SimpleBezierEdge`, `SmoothStepEdge`
- `StepEdge`, `StraightEdge`, `ToolbarNode`

### Changed

- **@xyflow/react** upgraded from 12.3.5 to 12.10.1 (7 minor versions, 33 releases, no breaking changes)
- **elkjs** upgraded from 0.8.2 to 0.9.3
- **zustand** upgraded from 4.4.7 to 4.5.5 (stays on 4.x — React Flow requires ^4.4.0)
- **React 18+ Compatibility**: Converted `DashFlows.defaultProps` to JavaScript default parameters to eliminate deprecation warnings
- **GroupNode Refactoring**: Simplified to React Fragment; styling applied directly to `.react-flow__node-group`
- **Node Base Styling**: Changed from fixed `width` to `max-width` for better layout flexibility

### Fixed

- **React defaultProps Warning**: Eliminated React 18+ deprecation warning across all components
- **GroupNode Nested Container**: Fixed nested wrapper div rendering issue
- CSS `!important` rules added to ensure layout class overrides apply correctly

---

## [1.1.0] - 2025-12-15

### Added

#### Custom Icons with DashIconify
- **DashIconify Integration**: InputNode, DefaultNode, and OutputNode now support custom icons via DashIconify
- **Icon Props**: New `icon` prop accepts DashIconify components or any Dash component for custom node icons
- **Icon Color**: New `iconColor` prop allows customizing the icon container background color
- **Show/Hide Icon**: New `showIcon` prop to toggle icon visibility (useful for text-only nodes)

#### Node Layout System
- **Layout Prop**: New `layout` prop with two options:
  - `"stacked"` (default): Vertical arrangement with icon above text
  - `"horizontal"`: Two[CHANGELOG.md](CHANGELOG.md)-column layout with icon on left, text on right
- **Content-Aware Sizing**: Nodes automatically adjust size based on content configuration:
  - **Icon-only nodes**: Compact sizing that fits the icon (no wasted space)
  - **Text-only nodes**: Centered text without reserved icon space
  - **Full content nodes**: Standard layout with icon and text

#### Enhanced Node Data Props
- **Title Prop**: New `title` prop as alias for `label` (for clarity when using body text)
- **Body Prop**: New `body` prop for description text below the title/sublabel
- **Sublabel Prop**: Secondary text displayed below the main label

#### New Example
- **Example 22**: `22_custom_icons.py` - Interactive demo showcasing:
  - Custom icons with DashIconify
  - Layout toggle (stacked/horizontal)
  - Show/hide icon toggle
  - Dynamic icon, title, and body text updates via DMC forms

### Changed

- **Node Base Styling**: Changed from fixed `width` to `max-width` for better layout flexibility
- **CSS Layout Classes**: Added `!important` flags to ensure layout overrides work correctly

### Fixed

- **Horizontal Layout**: Fixed horizontal layout not being applied correctly due to CSS specificity issues
- **Icon-Only Node Width**: Fixed icon-only nodes being too wide by using `inline-flex` display

#### New Examples
- **Example 23**: `23_callback_stress_test.py` - Stress test for Dash callbacks with DashFlows
  - 50 initial nodes in 5x10 grid
  - Multiple simultaneous callbacks monitoring events
  - Batch operations and live metrics
  - Event logging for debugging

### Changed

- **Node Base Styling**: Changed from fixed `width` to `max-width` for better layout flexibility
- **CSS Layout Classes**: Added `!important` flags to ensure layout overrides work correctly
- **React 18+ Compatibility**: Converted `DashFlows.defaultProps` to JavaScript default parameters to eliminate React deprecation warnings
- **GroupNode Simplification**: Refactored GroupNode to use React Fragment instead of wrapper divs, styling applied directly to `.react-flow__node-group`

### Fixed

- **Multi-select Not Working**: Added `multiSelectionKeyCode="Shift"` support in example 07
- **Right-click Context Menu**: Fixed context menu callback in example 07 to display node data
- **React defaultProps Warning**: Fixed React 18+ deprecation warning by using default parameters instead of `Component.defaultProps`
- **GroupNode Nested Container**: Fixed GroupNode appearing with nested container by simplifying component to render only NodeResizer and label badge
- **Viewport Control Buttons**: Fixed Pan to Top Left/Center/Bottom Right buttons in example 09 by correcting the `viewportAction` object structure
- **Dark Mode Toggle (DMC)**: Fixed Mantine dark mode toggle in example 11 using modern `data-mantine-color-scheme` attribute pattern

### Technical

- Added CSS classes for content detection: `.df-icon-only`, `.df-text-only`, `.df-full-content`
- Added CSS classes for layouts: `.df-layout-stacked`, `.df-layout-horizontal`
- Added horizontal layout structure with `.df-node-icon-column` and `.df-node-text-column`
- Added Iconify API fallback for rendering DashIconify icons when namespace unavailable
- Enhanced `renderDashComponent` function to handle serialized Dash component format from callbacks
- Added comprehensive JSDoc descriptions to all component propTypes for better IDE support
- GroupNode now styles `.react-flow__node-group` directly with `!important` rules for proper React Flow integration

---

## [1.0.0] - 2024-12-10

### Added

#### New Node Types
- **DefaultNode**: Standard node with fully configurable handles
- **InputNode**: Source node with green accent styling and output handles
- **OutputNode**: Sink node with purple accent styling and input handles
- **GroupNode**: Container node for visually grouping related nodes
- **ToolbarNode**: Node with floating toolbar that appears on selection
- **ResizableNode**: Node that users can resize with drag handles

#### New Edge Types
- **SimpleBezierEdge**: Smooth curved Bezier connections
- **SmoothStepEdge**: Rounded right-angle step connections
- **StepEdge**: Sharp right-angle step connections
- **StraightEdge**: Direct straight-line connections
- **AnimatedSvgEdge**: Edge with animated flowing dot effect
- **ButtonEdge**: Edge with interactive delete button
- **DataEdge**: Edge that displays data labels inline

#### New UI Components
- **NodeStatusIndicator**: Visual status wrapper for nodes with loading, success, and error states
- **NodeTooltip**: Hover tooltip component for nodes
- **NodeSearch**: Search and filter nodes in the flow
- **ButtonHandle**: Interactive button-styled handle component
- **DevTools**: Development debugging panel

#### Theming System
- **Glass Morphism Theme**: Default theme with blur effects and transparency
- **Solid Theme**: Opaque cards with traditional shadows
- **Minimal Theme**: Clean, border-focused minimal design
- **Color Schemes**: 6 color schemes (default, ocean, forest, sunset, midnight, rose)
- **Dark Mode Support**: Automatic dark mode via React Flow, Mantine, or custom classes
- **CSS Custom Properties**: Full theming via CSS variables for customization

#### Status Indicators
- Loading state with blue pulsing glow animation
- Success state with green border and checkmark badge
- Error state with red border, X badge, and shake animation
- Initial state (no visual indicator)

#### Handle Configuration
- Configurable handle positions (top, right, bottom, left)
- Multiple handles per position
- Custom handle IDs for precise edge connections
- Handle styling customization

#### Examples
- 21 comprehensive example files covering all features
- Basic usage to advanced implementations
- Context menus, drag-and-drop, copy/paste demonstrations
- ELK layout integration examples
- Dash component embedding examples

### Changed

- Upgraded to React Flow 12.3.5 (@xyflow/react)
- Complete rewrite of theming system with CSS custom properties
- Improved handle hover states with smooth transitions
- Enhanced node selection styling
- Better dark mode color contrast

### Fixed

- Node status indicator loading animation now works properly with rounded corners
- Fixed CSS class name mismatch between JavaScript components and stylesheets
- Improved glass effect rendering across browsers
- Fixed handle positioning for custom node types

### Technical

- Built on React 18.2
- Uses Zustand for state management
- ELK.js integration for automatic layouts
- html-to-image for flow export functionality
- Full TypeScript prop-types definitions

## [0.0.4] - 2024-11-XX

### Added
- Configurable handles feature
- Callback to view nodes for debugging
- DevTools component

### Changed
- Updated version number

## [0.0.3] - 2024-XX-XX

### Added
- Initial public release
- Basic DashFlows component
- React Flow integration
- AnimatedCircleNode
- AnimatedNodeEdge

---

## Migration Guide

### From 0.0.x to 1.0.0

1. **Update import statements**: Component names remain the same, but ensure you're importing from `dash_flows`:
   ```python
   from dash_flows import DashFlows, DefaultNode, InputNode, OutputNode
   ```

2. **Node status indicators**: The status indicator CSS classes have been updated. If you were using custom CSS targeting the old classes, update to:
   - `.df-node-status-loading-border` for loading state
   - `.df-node-status-success` for success state
   - `.df-node-status-error` for error state

3. **Theming**: The new theming system uses CSS custom properties. Apply theme classes to your container:
   ```python
   DashFlows(
       id='flow',
       className='df-theme-glass df-scheme-ocean',
       ...
   )
   ```

4. **Handle configuration**: Handles are now configured via the node's `data.handles` array instead of separate props.