// src/lib/components/edges/ButtonEdge.js
import React from 'react';
import PropTypes from 'prop-types';
import { BaseEdge, EdgeLabelRenderer, getBezierPath, useReactFlow } from '@xyflow/react';

/**
 * ButtonEdge - Glass morphism styled edge with an interactive button
 */
const ButtonEdge = ({
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
    const { setEdges } = useReactFlow();

    const [edgePath, labelX, labelY] = getBezierPath({
        sourceX,
        sourceY,
        sourcePosition,
        targetX,
        targetY,
        targetPosition,
    });

    const onEdgeClick = () => {
        if (data?.onButtonClick) {
            data.onButtonClick(id);
        } else {
            setEdges((edges) => edges.filter((edge) => edge.id !== id));
        }
    };

    const edgeLabel = label || data?.label;
    const buttonLabel = data?.buttonLabel || '\u00d7';
    const showButton = data?.showButton !== false;

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

    const glassButtonStyle = {
        width: '22px',
        height: '22px',
        backdropFilter: 'blur(8px) saturate(150%)',
        WebkitBackdropFilter: 'blur(8px) saturate(150%)',
        background: 'var(--df-edge-button-bg, rgba(255, 255, 255, 0.9))',
        border: '1px solid var(--df-edge-button-border, rgba(0, 0, 0, 0.1))',
        borderRadius: '50%',
        cursor: 'pointer',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '14px',
        fontWeight: 600,
        lineHeight: '1',
        padding: 0,
        color: 'var(--df-node-text-secondary, #495057)',
        boxShadow: 'var(--df-edge-button-shadow, 0 2px 6px rgba(0, 0, 0, 0.1))',
        transition: 'all 150ms ease',
        ...data?.buttonStyle,
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
            <EdgeLabelRenderer>
                <div
                    style={{
                        position: 'absolute',
                        transform: `translate(-50%, -50%) translate(${labelX}px, ${labelY}px)`,
                        pointerEvents: 'all',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '6px',
                    }}
                    className="nodrag nopan df-edge-label-container"
                >
                    {edgeLabel && (
                        <span className="df-edge-label" style={glassLabelStyle}>
                            {edgeLabel}
                        </span>
                    )}
                    {showButton && (
                        <button
                            className="df-edge-button"
                            style={glassButtonStyle}
                            onClick={onEdgeClick}
                            title={data?.buttonTitle || 'Remove edge'}
                        >
                            {buttonLabel}
                        </button>
                    )}
                </div>
            </EdgeLabelRenderer>
        </>
    );
};

ButtonEdge.propTypes = {
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
    /** Whether the edge is currently selected */
    selected: PropTypes.bool,
    /** Configuration data for the button edge */
    data: PropTypes.shape({
        /** Label text to display next to the button */
        label: PropTypes.any,
        /** Whether to show the button (default: true) */
        showButton: PropTypes.bool,
        /** Text/symbol to display on the button (default: '×') */
        buttonLabel: PropTypes.string,
        /** Custom CSS styles for the button */
        buttonStyle: PropTypes.object,
        /** Tooltip title for the button */
        buttonTitle: PropTypes.string,
        /** Callback function when button is clicked */
        onButtonClick: PropTypes.func,
    }),
};

export default ButtonEdge;