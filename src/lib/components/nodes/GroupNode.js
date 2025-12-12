// src/lib/components/nodes/GroupNode.js
import React, { memo } from 'react';
import PropTypes from 'prop-types';
import { NodeResizer } from '@xyflow/react';

/**
 * GroupNode - Glass morphism styled container node that can hold other nodes
 * Child nodes should have parentId set to this node's ID
 *
 * IMPORTANT: Group nodes should have zIndex set lower than child nodes
 * in the node definition to ensure proper layering.
 */
const GroupNode = memo(({ data, selected }) => {
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

    const labelContent = data.label
        ? (typeof data.label === 'string' ? data.label : renderDashComponent(data.label))
        : null;

    const glassStyle = {
        width: '100%',
        height: '100%',
        backdropFilter: 'blur(8px) saturate(120%)',
        WebkitBackdropFilter: 'blur(8px) saturate(120%)',
        background: 'var(--df-group-node-bg, rgba(243, 244, 246, 0.5))',
        border: '2px dashed var(--df-group-node-border, rgba(156, 163, 175, 0.4))',
        borderRadius: 'var(--df-radius-xl, 20px)',
        boxShadow: selected
            ? 'var(--df-glass-shadow, 0 8px 32px rgba(31, 38, 135, 0.15)), 0 0 0 2px var(--df-selection-border, rgba(59, 130, 246, 0.4))'
            : 'var(--df-glass-shadow, 0 8px 32px rgba(31, 38, 135, 0.1))',
        position: 'relative',
        transition: 'all 250ms ease',
        // Ensure group is behind child nodes - React Flow handles z-index
        // but we set pointer-events to allow clicking through to children
        pointerEvents: 'all',
        ...data.style,
    };

    const labelStyle = {
        position: 'absolute',
        top: '-12px',
        left: '16px',
        display: 'inline-flex',
        alignItems: 'center',
        gap: '6px',
        padding: '4px 10px',
        background: 'var(--df-toolbar-bg, rgba(255, 255, 255, 0.95))',
        backdropFilter: 'blur(8px)',
        WebkitBackdropFilter: 'blur(8px)',
        borderRadius: 'var(--df-radius-sm, 6px)',
        border: '1px solid var(--df-node-border, rgba(255, 255, 255, 0.5))',
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)',
        fontSize: '11px',
        fontWeight: 600,
        textTransform: 'uppercase',
        letterSpacing: '0.5px',
        color: 'var(--df-node-text-secondary, #495057)',
        ...data.labelStyle,
    };

    const resizerHandleStyle = {
        width: '10px',
        height: '10px',
        background: 'var(--df-handle-bg, #fff)',
        border: '2px solid var(--df-handle-border, #64748b)',
        borderRadius: '2px',
    };

    return (
        <div className={`df-glass-node df-group-node ${selected ? 'selected' : ''}`} style={glassStyle}>
            <NodeResizer
                isVisible={selected && data.resizable !== false}
                minWidth={data.minWidth || 200}
                minHeight={data.minHeight || 150}
                handleStyle={resizerHandleStyle}
                lineStyle={{ borderWidth: 1, borderColor: 'var(--df-selection-border, rgba(59, 130, 246, 0.4))' }}
            />
            {labelContent && (
                <div className="df-group-node-label" style={labelStyle}>
                    {data.icon && (
                        <span style={{ display: 'flex', alignItems: 'center' }}>
                            {data.icon}
                        </span>
                    )}
                    {labelContent}
                </div>
            )}
        </div>
    );
});

GroupNode.displayName = 'GroupNode';

GroupNode.propTypes = {
    /**
     * Node data object containing label, icon, and styling options
     */
    data: PropTypes.shape({
        /** Label content for the group - displayed above the group container */
        label: PropTypes.any,
        /** Icon element to display next to the label */
        icon: PropTypes.any,
        /** Custom CSS styles for the group container */
        style: PropTypes.object,
        /** Custom CSS styles for the label element */
        labelStyle: PropTypes.object,
        /** Whether the group can be resized (default: true) */
        resizable: PropTypes.bool,
        /** Minimum width constraint for resizing */
        minWidth: PropTypes.number,
        /** Minimum height constraint for resizing */
        minHeight: PropTypes.number,
    }),
    /** Whether the group is currently selected */
    selected: PropTypes.bool,
};

export default GroupNode;