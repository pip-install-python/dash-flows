// src/lib/components/edges/ButtonEdge.js
import React, { useState, useRef, useEffect } from 'react';
import PropTypes from 'prop-types';
import { BaseEdge, EdgeLabelRenderer, EdgeToolbar, getBezierPath, useReactFlow } from '@xyflow/react';

/**
 * ButtonEdge - Glass morphism styled edge with an interactive button and optional toolbar
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
    const [isEditing, setIsEditing] = useState(false);
    const [editValue, setEditValue] = useState('');
    const inputRef = useRef(null);

    const [edgePath, labelX, labelY] = getBezierPath({
        sourceX,
        sourceY,
        sourcePosition,
        targetX,
        targetY,
        targetPosition,
    });

    const onEdgeDelete = () => {
        if (data?.onButtonClick) {
            data.onButtonClick(id);
        } else {
            setEdges((edges) => edges.filter((edge) => edge.id !== id));
        }
    };

    const onEditStart = () => {
        setEditValue(label || data?.label || '');
        setIsEditing(true);
    };

    const onEditSave = () => {
        setIsEditing(false);
        const newLabel = editValue.trim();
        setEdges((edges) => edges.map((edge) =>
            edge.id === id
                ? { ...edge, label: newLabel, data: { ...edge.data, label: newLabel } }
                : edge
        ));
    };

    const onEditKeyDown = (e) => {
        if (e.key === 'Enter') {
            onEditSave();
        } else if (e.key === 'Escape') {
            setIsEditing(false);
        }
    };

    // Focus the input when editing starts
    useEffect(() => {
        if (isEditing && inputRef.current) {
            inputRef.current.focus();
            inputRef.current.select();
        }
    }, [isEditing]);

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

    const showToolbar = !!data?.showToolbar;

    const toolbarStyle = {
        display: 'flex',
        gap: '4px',
        padding: '6px 10px',
        background: 'var(--df-toolbar-bg, rgba(255, 255, 255, 0.95))',
        backdropFilter: 'blur(12px) saturate(150%)',
        WebkitBackdropFilter: 'blur(12px) saturate(150%)',
        borderRadius: 'var(--df-radius-md, 10px)',
        border: '1px solid var(--df-toolbar-border, rgba(0, 0, 0, 0.1))',
        boxShadow: 'var(--df-toolbar-shadow, 0 4px 12px rgba(0, 0, 0, 0.1))',
        ...data?.toolbarStyle,
    };

    const toolbarBtnStyle = {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        width: '28px',
        height: '28px',
        border: 'none',
        borderRadius: 'var(--df-radius-sm, 6px)',
        background: 'transparent',
        color: 'var(--df-node-text-secondary, #495057)',
        cursor: 'pointer',
        transition: 'all 150ms ease',
        fontSize: '14px',
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
                            onClick={onEdgeDelete}
                            title={data?.buttonTitle || 'Remove edge'}
                        >
                            {buttonLabel}
                        </button>
                    )}
                </div>
            </EdgeLabelRenderer>
            {showToolbar && (
                <EdgeToolbar edgeId={id} x={labelX} y={labelY - 40}>
                    <div className="df-edge-toolbar nodrag nopan" style={toolbarStyle}>
                        {isEditing ? (
                            <input
                                ref={inputRef}
                                value={editValue}
                                onChange={(e) => setEditValue(e.target.value)}
                                onKeyDown={onEditKeyDown}
                                onBlur={onEditSave}
                                style={{
                                    border: '1px solid var(--df-edge-label-border, rgba(0,0,0,0.15))',
                                    borderRadius: 'var(--df-radius-sm, 6px)',
                                    padding: '4px 8px',
                                    fontSize: '12px',
                                    width: '120px',
                                    outline: 'none',
                                    background: 'var(--df-node-bg, rgba(255,255,255,0.9))',
                                    color: 'var(--df-node-text, #1a1b1e)',
                                }}
                                placeholder="Edge label..."
                            />
                        ) : (
                            <>
                                <button style={toolbarBtnStyle} title="Edit label" onClick={onEditStart}>
                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
                                    </svg>
                                </button>
                                <button style={{...toolbarBtnStyle, color: '#ef4444'}} title="Delete edge" onClick={onEdgeDelete}>
                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                        <polyline points="3 6 5 6 21 6" />
                                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                                    </svg>
                                </button>
                            </>
                        )}
                    </div>
                </EdgeToolbar>
            )}
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
        /** Show glass morphism toolbar when edge is selected */
        showToolbar: PropTypes.bool,
        /** Custom CSS styles for the toolbar container */
        toolbarStyle: PropTypes.object,
    }),
};

export default ButtonEdge;