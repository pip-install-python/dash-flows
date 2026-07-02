// src/lib/components/edges/FloatingEdge.js
import React from 'react';
import PropTypes from 'prop-types';
import { BaseEdge, EdgeLabelRenderer, useInternalNode } from '@xyflow/react';

/**
 * Computes the intersection point of a line from the center of a rectangle
 * to an external target point with the rectangle's border.
 */
function getNodeIntersection(node, targetPoint) {
    const w = node.measured?.width || node.width || 150;
    const h = node.measured?.height || node.height || 50;
    const x = node.internals?.positionAbsolute?.x ?? node.position.x;
    const y = node.internals?.positionAbsolute?.y ?? node.position.y;

    const cx = x + w / 2;
    const cy = y + h / 2;

    const dx = targetPoint.x - cx;
    const dy = targetPoint.y - cy;

    // Avoid division by zero
    if (dx === 0 && dy === 0) {
        return { x: cx, y: cy };
    }

    const slope = Math.abs(dy / (dx || 0.001));
    const aspectSlope = h / w;

    let ix, iy;

    if (slope > aspectSlope) {
        // Intersects top or bottom
        iy = dy > 0 ? y + h : y;
        ix = cx + (dx / Math.abs(dy)) * (h / 2);
    } else {
        // Intersects left or right
        ix = dx > 0 ? x + w : x;
        iy = cy + (dy / Math.abs(dx)) * (w / 2);
    }

    return { x: ix, y: iy };
}

/**
 * Returns the position (for edge path computation) of the intersection point.
 */
function getEdgePosition(node, intersectionPoint) {
    const w = node.measured?.width || node.width || 150;
    const h = node.measured?.height || node.height || 50;
    const x = node.internals?.positionAbsolute?.x ?? node.position.x;
    const y = node.internals?.positionAbsolute?.y ?? node.position.y;

    const cx = x + w / 2;
    const cy = y + h / 2;

    const dx = Math.abs(intersectionPoint.x - cx);
    const dy = Math.abs(intersectionPoint.y - cy);
    const halfW = w / 2;
    const halfH = h / 2;

    // Determine which side the intersection is on
    if (Math.abs(dx - halfW) < 1) {
        // Left or right side
        return intersectionPoint.x > cx ? 'right' : 'left';
    }
    return intersectionPoint.y > cy ? 'bottom' : 'top';
}

/**
 * FloatingEdge - Edge that connects to the nearest point on each node's border
 * instead of fixed handle positions. Creates more natural-looking connections.
 */
const FloatingEdge = ({
    id,
    source,
    target,
    label,
    labelStyle,
    style,
    markerEnd,
    markerStart,
    data,
    selected,
}) => {
    const sourceNode = useInternalNode(source);
    const targetNode = useInternalNode(target);

    if (!sourceNode || !targetNode) {
        return null;
    }

    const sw = sourceNode.measured?.width || sourceNode.width || 150;
    const sh = sourceNode.measured?.height || sourceNode.height || 50;
    const sx = sourceNode.internals?.positionAbsolute?.x ?? sourceNode.position.x;
    const sy = sourceNode.internals?.positionAbsolute?.y ?? sourceNode.position.y;

    const tw = targetNode.measured?.width || targetNode.width || 150;
    const th = targetNode.measured?.height || targetNode.height || 50;
    const tx = targetNode.internals?.positionAbsolute?.x ?? targetNode.position.x;
    const ty = targetNode.internals?.positionAbsolute?.y ?? targetNode.position.y;

    const sourceCenter = { x: sx + sw / 2, y: sy + sh / 2 };
    const targetCenter = { x: tx + tw / 2, y: ty + th / 2 };

    const sourceIntersection = getNodeIntersection(sourceNode, targetCenter);
    const targetIntersection = getNodeIntersection(targetNode, sourceCenter);

    // Calculate midpoint for label
    const labelX = (sourceIntersection.x + targetIntersection.x) / 2;
    const labelY = (sourceIntersection.y + targetIntersection.y) / 2;

    // Compute control points for a smooth bezier curve
    const dx = targetIntersection.x - sourceIntersection.x;
    const dy = targetIntersection.y - sourceIntersection.y;
    const controlOffset = Math.min(Math.sqrt(dx * dx + dy * dy) * 0.25, 80);

    const sourcePos = getEdgePosition(sourceNode, sourceIntersection);
    const targetPos = getEdgePosition(targetNode, targetIntersection);

    // Calculate control points based on the side the edge exits/enters
    let sx1 = sourceIntersection.x, sy1 = sourceIntersection.y;
    let tx1 = targetIntersection.x, ty1 = targetIntersection.y;

    switch (sourcePos) {
        case 'left': sx1 -= controlOffset; break;
        case 'right': sx1 += controlOffset; break;
        case 'top': sy1 -= controlOffset; break;
        case 'bottom': sy1 += controlOffset; break;
    }

    switch (targetPos) {
        case 'left': tx1 -= controlOffset; break;
        case 'right': tx1 += controlOffset; break;
        case 'top': ty1 -= controlOffset; break;
        case 'bottom': ty1 += controlOffset; break;
    }

    const edgePath = `M ${sourceIntersection.x} ${sourceIntersection.y} C ${sx1} ${sy1}, ${tx1} ${ty1}, ${targetIntersection.x} ${targetIntersection.y}`;

    const edgeLabel = label || data?.label;

    const glassLabelStyle = {
        backdropFilter: 'blur(8px) saturate(150%)',
        WebkitBackdropFilter: 'blur(8px) saturate(150%)',
        background: 'var(--df-edge-label-bg, rgba(255, 255, 255, 0.85))',
        padding: '4px 10px',
        borderRadius: 'var(--df-radius-sm, 6px)',
        fontSize: '11px',
        fontWeight: 500,
        color: 'var(--df-node-text, #1a1b1e)',
        border: '1px solid var(--df-edge-label-border, rgba(255, 255, 255, 0.6))',
        boxShadow: 'var(--df-edge-label-shadow, 0 2px 8px rgba(0, 0, 0, 0.08))',
        ...labelStyle,
    };

    const edgeStyle = {
        stroke: selected
            ? 'var(--df-edge-selected, #3b82f6)'
            : 'var(--df-edge-stroke, #64748b)',
        strokeWidth: selected ? 2 : 1.5,
        ...style,
    };

    return (
        <>
            <BaseEdge
                id={id}
                path={edgePath}
                style={edgeStyle}
                markerEnd={markerEnd}
                markerStart={markerStart}
            />
            {edgeLabel && (
                <EdgeLabelRenderer>
                    <div
                        style={{
                            position: 'absolute',
                            transform: `translate(-50%, -50%) translate(${labelX}px, ${labelY}px)`,
                            pointerEvents: 'all',
                        }}
                        className="nodrag nopan df-edge-label-container"
                    >
                        <span className="df-edge-label" style={glassLabelStyle}>
                            {edgeLabel}
                        </span>
                    </div>
                </EdgeLabelRenderer>
            )}
        </>
    );
};

FloatingEdge.propTypes = {
    /** Unique identifier for the edge */
    id: PropTypes.string.isRequired,
    /** Source node ID */
    source: PropTypes.string.isRequired,
    /** Target node ID */
    target: PropTypes.string.isRequired,
    /** X coordinate of the edge source */
    sourceX: PropTypes.number,
    /** Y coordinate of the edge source */
    sourceY: PropTypes.number,
    /** X coordinate of the edge target */
    targetX: PropTypes.number,
    /** Y coordinate of the edge target */
    targetY: PropTypes.number,
    /** Label text to display on the edge */
    label: PropTypes.any,
    /** Custom CSS styles for the label */
    labelStyle: PropTypes.object,
    /** Custom CSS styles for the edge path */
    style: PropTypes.object,
    /** Marker configuration for the edge end */
    markerEnd: PropTypes.any,
    /** Marker configuration for the edge start */
    markerStart: PropTypes.any,
    /** Additional data passed to the edge */
    data: PropTypes.object,
    /** Whether the edge is currently selected */
    selected: PropTypes.bool,
};

export default FloatingEdge;
