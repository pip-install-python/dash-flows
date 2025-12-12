// src/lib/components/edges/StepEdge.js
import React from 'react';
import PropTypes from 'prop-types';
import { BaseEdge, EdgeLabelRenderer, getSmoothStepPath } from '@xyflow/react';

/**
 * StepEdge - Glass morphism styled stepped edge with sharp corners
 */
const StepEdge = ({
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
    const [edgePath, labelX, labelY] = getSmoothStepPath({
        sourceX,
        sourceY,
        sourcePosition,
        targetX,
        targetY,
        targetPosition,
        borderRadius: 0, // Sharp corners for step edge
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

StepEdge.propTypes = {
    id: PropTypes.string.isRequired,
    sourceX: PropTypes.number.isRequired,
    sourceY: PropTypes.number.isRequired,
    targetX: PropTypes.number.isRequired,
    targetY: PropTypes.number.isRequired,
    sourcePosition: PropTypes.string,
    targetPosition: PropTypes.string,
    label: PropTypes.any,
    labelStyle: PropTypes.object,
    style: PropTypes.object,
    markerEnd: PropTypes.any,
    markerStart: PropTypes.any,
    data: PropTypes.object,
    selected: PropTypes.bool,
};

export default StepEdge;