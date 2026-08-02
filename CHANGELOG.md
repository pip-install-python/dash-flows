# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2026-08-01

### Changed — flows.2plot.dev joins the 2plot network standard

The docs site now matches the pattern proven on 2plot.ai, 2plot.dev,
boilerplate.2plot.dev, leaflet.2plot.dev and email.2plot.dev. What that means
in practice:

- **One identity, every surface.** `lib/constants.py` defines
  `SITE_BRAND = "dash-flows — React Flow node graphs for Dash"` (package name
  leads — the library rule; "Pip Install Python" is the byline, never the
  name), and it now reaches the `<title>`, the `/llms.txt` H1, the llms
  viewer's brand chip, the home prose, the README and every share-card
  headline. `tests/test_site_identity.py` pins all of them, because every one
  of these falls back to a framework default silently.
- **`dash-improve-my-llms>=2.3.4` is now required** (run.py refuses to boot
  below the floor) and replaces `lib/seo.py` entirely: `/robots.txt`,
  `/sitemap.xml`, `/llms.txt`, `/<page>/llms.txt`, the crawler prerender,
  canonical/og:url and the cross-host `## Network` directory
  (`lib/network_directory.py`) all come from the package. The one thing
  `lib/seo.py` did that the package does not — re-pointing canonical/og:url on
  client-side navigation — moved into `templates/index.html` as the
  network-standard History-API script.
- **The analytics stack is the network's.** `lib/satellite_analytics.py` split
  into the standard `lib/analytics_tracker.py` (which drops internal-network
  and `/healthz` traffic at WRITE time — the internal-traffic contract's
  inbound half), `lib/traffic_rollup.py`, `lib/satellite_reporter.py` (flock
  lease so one worker reports per interval) and `lib/bulletin.py`. This app's
  own SPA page-view beacon — the reason its session numbers are honest when
  every other Dash site reports single-page visits — survives the split as
  `lib/pageview_beacon.py`. The outbound half of the contract is new here:
  `ad_client` and the traffic reporter now send the `2plot-internal` UA, so
  this site's readers stop being counted as bot traffic on the hub.
- **The app id is `flows` everywhere** — the network-directory key, never the
  package name — across `AD_APP_ID`, `SATELLITE_APP_ID`/`SATELLITE_APP_KEY`
  and the bulletin.
- **Every page ships a real social card.** No `register_page()` call passed
  `image_url=` before, so Dash emitted `og:image=""` on every page — an empty
  tag that unfurls worse than none, because scrapers treat it as the declared
  image and render a blank card. All pages now point at
  `cdn.2plot.ai/github_assets/flows.2plot.dev.png` (1200x630, rendered by
  `scripts/make_social_card.py`), the template declares only the auxiliary
  tags Dash omits, and `scripts/smoke_live.py` reads the CDN object's IHDR
  bytes after every deploy.
- **gunicorn floored at 23** (CVE-2024-6827, CVE-2024-1135 — request
  smuggling). markdown2dash 0.1.2 pins `gunicorn<22`, so it now installs with
  `--no-deps` everywhere (Dockerfile, CI, requirements-docs.txt lists its real
  dependencies) and CI asserts the gunicorn version *inside* the built image.

### Added — CI/CD, from nothing

This repo had no `.github/workflows` at all. It now has the boilerplate's
proven shape: `ci.yml` (actionlint first — an invalid workflow file is the one
defect CI structurally cannot report; flake8; the secretless pytest suite —
zero secrets in CI on purpose, so fail-closed postures are provable; the real
Docker image built, version-fingerprinted inside, booted and probed by
`scripts/network_smoke.py` — the same battery CD runs against production; an
examples matrix across Dash 4.2.0/4.4.1 and Python 3.10–3.13; a wheel build
proving the `dash>=4.1.0` floor in a clean venv with nothing but Dash) and
`cd.yml` (owns `main`, requires CI, then 120s settle + five *consecutive*
healthy probes — Render swaps instances, so a single 200 can come from the
dying instance — then the battery plus `scripts/smoke_live.py` against
https://flows.2plot.dev, where peer checks warn and own-host checks fail).

### Changed — the wheel states its real floor

`setup.py` now declares `install_requires=['dash>=4.1.0']` (the first release
with the multi-backend constructor this component targets). CI installs the
wheel with exactly `dash==4.1.0` and nothing else, and asserts
`top_level.txt == ["dash_flows"]` so no docs-site directory can ever leak into
the package.

### Changed
- **Dash 4.2+ support**: minimum `dash>=4.0.0` (dev pin `dash[dev]>=4.2.0`). Dash 4 keeps
  React 18, so no component-side React migration was required. Multi-backend
  (Flask/FastAPI/Quart) and websocket callbacks are available to consuming apps.
- **dash-mantine-components** pinned to `>=2.8.0` for examples and the docs app.
- **@xyflow/react** bumped to `^12.11.1` (latest 12.x). `zustand` remains pinned to `4.x`
  (React Flow requires `^4.4.0`).

### Added
- **Markdown-driven documentation app** at the repo root (`run.py`, `pages/`, `docs/`,
  `components/`, `lib/`) seeded from the Dash Documentation Boilerplate. Each component
  is documented in `docs/<topic>/<topic>.md` with live `.. exec::` demos, `.. source::`
  code, and `.. kwargs::` prop tables generated from the existing `examples/`.
- **Every example runnable inline in the docs**: 34 of the 35 `examples/` apps now have
  an embeddable twin (`docs/<topic>/exNN.py`, ids namespaced `exNN-`) rendered live via
  `.. exec::`, plus the full source and a "How it works" breakdown on its category page.
  `23_callback_stress_test` is intentionally source-only (performance harness).
- **Validation harnesses** committed under `scripts/`: `smoke_examples.py` (import gate),
  `smoke_runtime.py` (WSGI runtime gate: `/`, `/_dash-layout`, `/_dash-dependencies`),
  and `validate_docs.py` (docs render gate). Results matrix in `SMOKE_RESULTS.md`
  (35/35 import + runtime). Browser-fidelity test in `tests/test_examples_render.py`.

### Removed
- **R and Julia language bindings** dropped — the project targets Python/Dash only.
  Removed `R/`, `man/`, `src/jl/`, `src/DashFlows.jl`, `NAMESPACE`, `DESCRIPTION`,
  `Project.toml`, `.Rbuildignore`, and the duplicate JS bundle copies under `deps/` and
  `inst/`. `build:backends` no longer generates R/Julia (`--r-prefix`/`--jl-prefix` removed).
- Repo clutter removed from version control: `SKILLS.md`, `dash_flows_SKILLS.md`,
  `review_checklist.md`, `REACT_FLOW_COMPARISON.md`, and the tracked `.idea/` IDE config.
- **Pre-migration remnants** removed: `usage.py` (superseded by the docs app — use
  `python run.py`), the old JS dev demo (`src/demo/`, root `index.html`,
  `webpack.serve.config.js`, the `npm start` script, `webpack-dev-server`), the stale
  boilerplate tests `tests/test_usage.py`/`tests/test_handle.py` (replaced by
  `tests/test_examples_render.py`), unreferenced `assets/logo.svg`/`assets/group-node.png`,
  the unused `webpack` require in `webpack.config.js`, and the deprecated `babel-eslint`
  parser (now `@babel/eslint-parser`; run `npm install` once to refresh the lockfile).

### Fixed
- Populated the previously empty `LICENSE` file with the MIT license text.
- **"Maximum update depth exceeded" render loop**: the outbound `nodes`/`edges`
  `setProps` effects in `DashFlows.react.js` now guard on a serialized diff
  (mirroring the `nodeConnections` effect), so React Flow's asynchronous node
  re-measurement can no longer drive a `setProps`↔`setNodes` loop.
- **React Flow error 008 ("null source/target handle") on resizable nodes**:
  `ResizableNode` now renders a default target (top) + source (bottom) handle
  pair when `data.handles` is omitted or empty (matching `DefaultNode`), so edges
  bind to it instead of failing. The `data.handles` prop is now optional.
- **MiniMap ignored the light/dark preference**: removed the inline
  `colorMode`-based background override so the MiniMap follows the `--df-minimap-*`
  CSS variables, which track both React Flow's `.dark` class and Mantine's
  `data-mantine-color-scheme` (correct even for `colorMode="system"`).
- **Dark-mode fidelity across the docs example twins**: replaced hardcoded light
  colors on cards/panels/buttons with Mantine CSS variables; converted native
  `html.Button`s to `dmc.Button` (`ex15`/`ex18`/`ex19`); synced the `ex20`/`ex21`
  canvases' `colorMode` to the page theme via `color-scheme-storage`; and themed
  the `ex14` metric-card node text so it stays legible on dark canvases.

### Roadmap (carried over from REACT_FLOW_COMPARISON.md)
- Refactor `DashFlows.react.js` (~2500 lines) into focused hooks
  (`useSmartHandles`, `useFlowState`, `useConnectionValidation`, `useViewportActions`,
  `useImageExport`, `useCopyPaste`, `useElkLayout`).
- Lazy-load `elkjs` (~1.45 MB, ~77% of the bundle) via dynamic import on first
  `layoutOptions` use.
- Remove the `ramda` dependency in favor of native JS.
- Memoize smart-handle edge computation; document `onlyRenderVisibleElements` for large flows.

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