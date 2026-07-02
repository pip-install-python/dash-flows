# React Flow API Quick Reference for dash-flows

## Core Imports Available (@xyflow/react 12.10.1)

```javascript
import {
    // Components
    ReactFlow, ReactFlowProvider,
    Controls, MiniMap, Background, Panel,
    Handle, Position,
    BaseEdge, EdgeLabelRenderer,
    NodeResizer, NodeResizeControl,
    NodeToolbar, EdgeToolbar,           // EdgeToolbar added in 12.9.0
    ViewportPortal,

    // Path helpers
    getBezierPath, getStraightPath, getSmoothStepPath, getSimpleBezierPath,

    // Hooks
    useReactFlow, useNodesState, useEdgesState, useOnSelectionChange,
    useNodeConnections,                  // Added in 12.4.0 — track connections per node
    useHandleConnections,                // Track connections per handle
    useConnection,                       // Connection state during drag
    useUpdateNodeInternals,              // Recalculate handle positions
    useNodesInitialized,                 // Wait for nodes to render
    useNodesData,                        // Efficient multi-node data access
    useViewport,                         // Real-time viewport state
    useKeyPress,                         // Keyboard detection
    useOnViewportChange,                 // Viewport change callbacks
    useStore, useStoreApi,               // Direct zustand store access
    useInternalNode,                     // Internal node data (dimensions)

    // Utilities
    getIncomers, getOutgoers,            // Graph traversal
    getConnectedEdges,                   // Edges for node set
    getNodesBounds,                      // Bounding box
    getViewportForBounds,                // Viewport for bounds

    // Enums
    MarkerType, ConnectionMode, SelectionMode, ConnectionLineType,
} from '@xyflow/react';
```

## New Props Available (12.4.0 → 12.10.1)

| Prop | Version | Description |
|------|---------|-------------|
| `connectionDragThreshold` | 12.8.0 | Drag distance before connection starts |
| `zIndexMode` | 12.10.0 | Z-index calculation strategy |
| `autoPanOnNodeFocus` | 12.7.0 | Auto-pan on keyboard focus |
| `ariaRole` | 12.7.0 | ARIA role for accessibility |
| `ariaLabelConfig` | 12.7.0 | Customize ARIA labels |

## Custom Node Pattern

```javascript
import React, { memo } from 'react';
import PropTypes from 'prop-types';
import { Handle, Position } from '@xyflow/react';

const MyNode = memo(({ data, selected, isConnectable }) => {
    return (
        <div className={`df-glass-node ${selected ? 'selected' : ''}`}>
            <Handle
                type="target"
                position={Position.Top}
                isConnectable={isConnectable}
                className="df-handle"
            />
            <div className="df-node-label">{data.label}</div>
            <Handle
                type="source"
                position={Position.Bottom}
                isConnectable={isConnectable}
                className="df-handle"
            />
        </div>
    );
});

MyNode.propTypes = {
    /** Node data including label and configuration */
    data: PropTypes.shape({
        label: PropTypes.string,
    }),
    /** Whether the node is currently selected */
    selected: PropTypes.bool,
    /** Whether the node can accept new connections */
    isConnectable: PropTypes.bool,
};

export default MyNode;
```

## Custom Edge Pattern

```javascript
import React from 'react';
import PropTypes from 'prop-types';
import { BaseEdge, EdgeLabelRenderer, getBezierPath } from '@xyflow/react';

const MyEdge = ({ id, sourceX, sourceY, targetX, targetY,
                  sourcePosition, targetPosition, label, style,
                  markerEnd, markerStart, data, selected }) => {
    const [edgePath, labelX, labelY] = getBezierPath({
        sourceX, sourceY, sourcePosition,
        targetX, targetY, targetPosition,
    });

    return (
        <>
            <BaseEdge id={id} path={edgePath} style={style}
                      markerEnd={markerEnd} markerStart={markerStart} />
            {label && (
                <EdgeLabelRenderer>
                    <div style={{
                        position: 'absolute',
                        transform: `translate(-50%, -50%) translate(${labelX}px, ${labelY}px)`,
                        pointerEvents: 'all',
                    }} className="nodrag nopan df-edge-label-container">
                        <span className="df-edge-label">{label}</span>
                    </div>
                </EdgeLabelRenderer>
            )}
        </>
    );
};

MyEdge.propTypes = {
    /** Unique identifier for the edge */
    id: PropTypes.string.isRequired,
    /** X position of the source */
    sourceX: PropTypes.number.isRequired,
    /** Y position of the source */
    sourceY: PropTypes.number.isRequired,
    /** X position of the target */
    targetX: PropTypes.number.isRequired,
    /** Y position of the target */
    targetY: PropTypes.number.isRequired,
    /** Position of source handle */
    sourcePosition: PropTypes.string,
    /** Position of target handle */
    targetPosition: PropTypes.string,
    /** Edge label text */
    label: PropTypes.string,
    /** Edge styling */
    style: PropTypes.object,
    /** Marker at the end of the edge */
    markerEnd: PropTypes.oneOfType([PropTypes.string, PropTypes.object]),
    /** Marker at the start of the edge */
    markerStart: PropTypes.oneOfType([PropTypes.string, PropTypes.object]),
    /** Additional data for the edge */
    data: PropTypes.object,
    /** Whether the edge is selected */
    selected: PropTypes.bool,
};

export default MyEdge;
```

## Handle Position Values

- `Position.Top` - Handle on top
- `Position.Bottom` - Handle on bottom
- `Position.Left` - Handle on left
- `Position.Right` - Handle on right

## Path Helpers

| Function | Returns |
|----------|---------|
| `getBezierPath({...})` | `[path, labelX, labelY, offsetX, offsetY]` |
| `getStraightPath({...})` | `[path, labelX, labelY]` |
| `getSmoothStepPath({...})` | `[path, labelX, labelY, offsetX, offsetY]` |
| `getSimpleBezierPath({...})` | `[path, labelX, labelY]` |

All accept: `{ sourceX, sourceY, sourcePosition, targetX, targetY, targetPosition }`

## useReactFlow Hook

```javascript
const { setNodes, setEdges, getNodes, getEdges,
        fitView, zoomIn, zoomOut, setViewport,
        screenToFlowPosition, flowToScreenPosition } = useReactFlow();
```

## MarkerType Values

```javascript
MarkerType.Arrow       // Simple arrow
MarkerType.ArrowClosed // Filled arrow
```