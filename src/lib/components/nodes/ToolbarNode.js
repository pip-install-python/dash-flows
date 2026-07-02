// src/lib/components/nodes/ToolbarNode.js
import React, { memo } from 'react';
import PropTypes from 'prop-types';
import { Handle, Position, NodeToolbar } from '@xyflow/react';

/**
 * ToolbarNode - Glass morphism styled node with a configurable toolbar
 */
const ToolbarNode = memo(({ data, selected, isConnectable }) => {
    const renderDashComponent = (component) => {
        if (!component) return null;
        if (typeof component === 'string') return component;
        if (React.isValidElement(component)) return component;

        if (component.props?.componentPath && window.dash_component_api) {
            const layout = window.dash_component_api.getLayout(component.props.componentPath);
            if (!layout) return null;
            const namespace = window[layout.namespace];
            if (!namespace || !namespace[layout.type]) return null;
            const ComponentClass = namespace[layout.type];
            const { children, componentPath, ...otherProps } = layout.props;
            try {
                return React.createElement(ComponentClass, otherProps, children);
            } catch (error) {
                return null;
            }
        }

        if (component.props?._dashprivate_layout) {
            const layout = component.props._dashprivate_layout;
            const namespace = window[layout.namespace];
            if (!namespace || !namespace[layout.type]) return null;
            const ComponentClass = namespace[layout.type];
            const { children, ...otherProps } = layout.props;
            try {
                return React.createElement(ComponentClass, otherProps, children);
            } catch (error) {
                return null;
            }
        }

        return null;
    };

    const labelContent = typeof data.label === 'string'
        ? data.label
        : renderDashComponent(data.label);

    const toolbarContent = data.toolbar
        ? (typeof data.toolbar === 'string' ? data.toolbar : renderDashComponent(data.toolbar))
        : null;

    const getPosition = (pos) => {
        const positions = {
            'top': Position.Top,
            'bottom': Position.Bottom,
            'left': Position.Left,
            'right': Position.Right,
        };
        return positions[pos?.toLowerCase()] || Position.Top;
    };

    const glassStyle = {
        backdropFilter: 'blur(12px) saturate(180%)',
        WebkitBackdropFilter: 'blur(12px) saturate(180%)',
        background: 'var(--df-node-bg, rgba(255, 255, 255, 0.72))',
        border: '1px solid var(--df-node-border, rgba(255, 255, 255, 0.5))',
        borderRadius: 'var(--df-radius-lg, 14px)',
        boxShadow: selected
            ? 'var(--df-glass-shadow-hover, 0 8px 32px rgba(31, 38, 135, 0.25)), var(--df-glass-inset, inset 0 1px 0 0 rgba(255, 255, 255, 0.6)), 0 0 0 2px var(--df-selection-border, rgba(59, 130, 246, 0.4))'
            : 'var(--df-glass-shadow, 0 8px 32px rgba(31, 38, 135, 0.15)), var(--df-glass-inset, inset 0 1px 0 0 rgba(255, 255, 255, 0.6))',
        color: 'var(--df-node-text, #1a1b1e)',
        padding: '12px 16px',
        minWidth: '150px',
        textAlign: 'center',
        transition: 'all 250ms ease',
        willChange: 'transform, box-shadow',
        transform: 'translateZ(0)',
        ...data.style,
    };

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
        ...data.toolbarStyle,
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

    const handleStyle = {
        width: '14px',
        height: '14px',
        background: 'var(--df-handle-bg, #fff)',
        border: '2px solid var(--df-handle-border, #64748b)',
        zIndex: 10,
        ...data.handleStyle,
    };

    return (
        <>
            <NodeToolbar
                isVisible={data.toolbarVisible !== undefined ? data.toolbarVisible : selected}
                position={getPosition(data.toolbarPosition)}
                align={data.toolbarAlign || 'center'}
                offset={data.toolbarOffset || 10}
            >
                <div className="df-node-toolbar" style={toolbarStyle}>
                    {toolbarContent || (
                        <>
                            <button
                                className="df-toolbar-btn"
                                style={toolbarBtnStyle}
                                title="Edit"
                            >
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
                                </svg>
                            </button>
                            <button
                                className="df-toolbar-btn"
                                style={toolbarBtnStyle}
                                title="Duplicate"
                            >
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
                                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
                                </svg>
                            </button>
                            <button
                                className="df-toolbar-btn danger"
                                style={{...toolbarBtnStyle}}
                                title="Delete"
                            >
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <polyline points="3 6 5 6 21 6" />
                                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                                </svg>
                            </button>
                        </>
                    )}
                </div>
            </NodeToolbar>
            <div className={`df-glass-node df-toolbar-node ${selected ? 'selected' : ''}`} style={glassStyle}>
                {data.showTargetHandle !== false && (
                    data.smartHandles ? (
                        [Position.Top, Position.Bottom, Position.Left, Position.Right].map((pos, i) => {
                            const names = ['top', 'bottom', 'left', 'right'];
                            return (
                                <Handle
                                    key={`target-${names[i]}`}
                                    id={`target-${names[i]}`}
                                    type="target"
                                    position={pos}
                                    isConnectable={isConnectable}
                                    style={handleStyle}
                                />
                            );
                        })
                    ) : (
                        <Handle
                            type="target"
                            position={getPosition(data.targetPosition) || Position.Top}
                            isConnectable={isConnectable}
                            style={handleStyle}
                        />
                    )
                )}
                <div className="df-node-label" style={{ fontSize: '13px', fontWeight: 500 }}>
                    {labelContent}
                </div>
                {data.sublabel && (
                    <div className="df-node-sublabel" style={{
                        fontSize: '11px',
                        color: 'var(--df-node-text-secondary, #495057)',
                        marginTop: '4px'
                    }}>
                        {data.sublabel}
                    </div>
                )}
                {data.showSourceHandle !== false && (
                    data.smartHandles ? (
                        [Position.Top, Position.Bottom, Position.Left, Position.Right].map((pos, i) => {
                            const names = ['top', 'bottom', 'left', 'right'];
                            return (
                                <Handle
                                    key={`source-${names[i]}`}
                                    id={`source-${names[i]}`}
                                    type="source"
                                    position={pos}
                                    isConnectable={isConnectable}
                                    style={handleStyle}
                                />
                            );
                        })
                    ) : (
                        <Handle
                            type="source"
                            position={getPosition(data.sourcePosition) || Position.Bottom}
                            isConnectable={isConnectable}
                            style={handleStyle}
                        />
                    )
                )}
            </div>
        </>
    );
});

ToolbarNode.displayName = 'ToolbarNode';

ToolbarNode.propTypes = {
    /** Node data configuration object */
    data: PropTypes.shape({
        /** Primary content to display in the node */
        label: PropTypes.any,
        /** Secondary text displayed below the main label */
        sublabel: PropTypes.string,
        /** Custom toolbar content - DashIconify or other components */
        toolbar: PropTypes.any,
        /** Whether the toolbar is visible (default: shows when selected) */
        toolbarVisible: PropTypes.bool,
        /** Position of the toolbar relative to the node */
        toolbarPosition: PropTypes.oneOf(['top', 'bottom', 'left', 'right']),
        /** Alignment of the toolbar ('start', 'center', 'end') */
        toolbarAlign: PropTypes.oneOf(['start', 'center', 'end']),
        /** Offset distance of the toolbar from the node */
        toolbarOffset: PropTypes.number,
        /** Custom CSS styles for the toolbar */
        toolbarStyle: PropTypes.object,
        /** Custom CSS styles for the node container */
        style: PropTypes.object,
        /** Custom CSS styles for connection handles */
        handleStyle: PropTypes.object,
        /** Position for the target (input) handle */
        targetPosition: PropTypes.string,
        /** Position for the source (output) handle */
        sourcePosition: PropTypes.string,
        /** Whether to show the target handle (default: true) */
        showTargetHandle: PropTypes.bool,
        /** Whether to show the source handle (default: true) */
        showSourceHandle: PropTypes.bool,
    }).isRequired,
    /** Whether the node is currently selected */
    selected: PropTypes.bool,
    /** Whether connections can be made to/from this node */
    isConnectable: PropTypes.bool,
};

export default ToolbarNode;