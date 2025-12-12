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
    selected: PropTypes.bool,
    data: PropTypes.shape({
        label: PropTypes.any,
        showButton: PropTypes.bool,
        buttonLabel: PropTypes.string,
        buttonStyle: PropTypes.object,
        buttonTitle: PropTypes.string,
        onButtonClick: PropTypes.func,
    }),
};

export default ButtonEdge;