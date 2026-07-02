// src/lib/components/edges/SmoothStepEdge.js
import React from 'react';
import PropTypes from 'prop-types';
import { BaseEdge, EdgeLabelRenderer, getSmoothStepPath } from '@xyflow/react';

/**
 * SmoothStepEdge - Glass morphism styled stepped edge with rounded corners
 */
const SmoothStepEdge = ({
    id,
    sourceX,
    sourceY,
    targetX,
    targetY,
    sourcePosition,
    targetPosition,
    label,
    labelStyle,
    style,
    markerEnd,
    markerStart,
    data,
    selected,
}) => {
    const borderRadius = data?.borderRadius || 8;

    const [edgePath, labelX, labelY] = getSmoothStepPath({
        sourceX,
        sourceY,
        sourcePosition,
        targetX,
        targetY,
        targetPosition,
        borderRadius,
    });

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

SmoothStepEdge.propTypes = {
    /** Unique identifier for the edge */
    id: PropTypes.string.isRequired,
    /** X coordinate of the edge source */
    sourceX: PropTypes.number.isRequired,
    /** Y coordinate of the edge source */
    sourceY: PropTypes.number.isRequired,
    /** X coordinate of the edge target */
    targetX: PropTypes.number.isRequired,
    /** Y coordinate of the edge target */
    targetY: PropTypes.number.isRequired,
    /** Position of the source handle ('top', 'bottom', 'left', 'right') */
    sourcePosition: PropTypes.string,
    /** Position of the target handle ('top', 'bottom', 'left', 'right') */
    targetPosition: PropTypes.string,
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
    /** Additional data passed to the edge (borderRadius can be set here) */
    data: PropTypes.object,
    /** Whether the edge is currently selected */
    selected: PropTypes.bool,
};

export default SmoothStepEdge;