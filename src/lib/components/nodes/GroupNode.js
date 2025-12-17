// src/lib/components/nodes/GroupNode.js
import React, { memo } from 'react';
import PropTypes from 'prop-types';
import { NodeResizer } from '@xyflow/react';

/**
 * GroupNode - A simple labeled group container for child nodes
 *
 * This follows the React Flow pattern for group nodes:
 * - The node's width/height is controlled via the style prop on the node definition
 * - Child nodes use parentId to reference this node
 * - Child nodes can use extent: 'parent' to stay within bounds
 *
 * Unlike standard nodes, group nodes are rendered as simple containers
 * that React Flow manages for parent-child relationships.
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

    const labelContent = data?.label
        ? (typeof data.label === 'string' ? data.label : renderDashComponent(data.label))
        : null;

    return (
        <>
            {/* NodeResizer for interactive resizing */}
            <NodeResizer
                isVisible={selected && data?.resizable !== false}
                minWidth={data?.minWidth || 100}
                minHeight={data?.minHeight || 50}
                handleStyle={{
                    width: '8px',
                    height: '8px',
                    background: 'var(--df-selection-border, rgba(59, 130, 246, 0.8))',
                    border: 'none',
                    borderRadius: '2px',
                }}
                lineStyle={{
                    borderWidth: 1,
                    borderColor: 'var(--df-selection-border, rgba(59, 130, 246, 0.4))',
                }}
            />

            {/* Label badge - positioned inside top-left */}
            {labelContent && (
                <div
                    className="df-group-node-label"
                    style={{
                        position: 'absolute',
                        top: '8px',
                        left: '8px',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '6px',
                        padding: '4px 10px',
                        background: 'var(--df-toolbar-bg, rgba(255, 255, 255, 0.95))',
                        backdropFilter: 'blur(8px)',
                        WebkitBackdropFilter: 'blur(8px)',
                        borderRadius: 'var(--df-radius-sm, 6px)',
                        border: '1px solid var(--df-node-border, rgba(200, 200, 200, 0.3))',
                        boxShadow: '0 1px 4px rgba(0, 0, 0, 0.05)',
                        fontSize: '11px',
                        fontWeight: 600,
                        color: 'var(--df-node-text-secondary, #6b7280)',
                        zIndex: 1,
                        pointerEvents: 'none',
                        ...data?.labelStyle,
                    }}
                >
                    {data?.icon && (
                        <span style={{ display: 'flex', alignItems: 'center' }}>
                            {data.icon}
                        </span>
                    )}
                    {labelContent}
                </div>
            )}
        </>
    );
});

GroupNode.displayName = 'GroupNode';

GroupNode.propTypes = {
    /**
     * Node data object containing label, icon, and styling options
     */
    data: PropTypes.shape({
        /** Label content for the group - displayed in top-left corner */
        label: PropTypes.any,
        /** Icon element to display next to the label */
        icon: PropTypes.any,
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