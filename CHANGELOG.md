# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-12-10

### Added

#### Custom Icons with DashIconify
- **DashIconify Integration**: InputNode, DefaultNode, and OutputNode now support custom icons via DashIconify
- **Icon Props**: New `icon` prop accepts DashIconify components or any Dash component for custom node icons
- **Icon Color**: New `iconColor` prop allows customizing the icon container background color
- **Show/Hide Icon**: New `showIcon` prop to toggle icon visibility (useful for text-only nodes)

#### Node Layout System
- **Layout Prop**: New `layout` prop with two options:
  - `"stacked"` (default): Vertical arrangement with icon above text
  - `"horizontal"`: Two-column layout with icon on left, text on right
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

### Technical

- Added CSS classes for content detection: `.df-icon-only`, `.df-text-only`, `.df-full-content`
- Added CSS classes for layouts: `.df-layout-stacked`, `.df-layout-horizontal`
- Added horizontal layout structure with `.df-node-icon-column` and `.df-node-text-column`
- Added Iconify API fallback for rendering DashIconify icons when namespace unavailable
- Enhanced `renderDashComponent` function to handle serialized Dash component format from callbacks

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