import React, { memo, useEffect, useRef, useState } from 'react';
import PropTypes from 'prop-types';
import { Handle, Position, NodeResizer } from '@xyflow/react';

/**
 * ResizableNode - A node that can be resized by the user
 *
 * This node supports embedding Dash components that will resize
 * along with the node container. The node receives width/height
 * from React Flow when resized.
 */
const ResizableNode = memo(({ data, selected = false, width, height }) => {
    // Track node dimensions for child components
    const [dimensions, setDimensions] = useState({
        width: width || data.initialWidth || 200,
        height: height || data.initialHeight || 100,
    });
    const contentRef = useRef(null);

    // Update dimensions when node is resized
    useEffect(() => {
        if (width && height) {
            setDimensions({ width, height });
        }
    }, [width, height]);

    const renderDashComponent = (component) => {
        if (!component) return null;
        if (typeof component === 'string') return component;
        if (React.isValidElement(component)) return component;

        // Dash 3.0+ uses dash_component_api with componentPath
        // Check for Dash 3.0+ style component (has componentPath)
        if (component.props?.componentPath && window.dash_component_api) {
            const layout = window.dash_component_api.getLayout(component.props.componentPath);
            if (!layout) {
                console.warn('Could not get layout for component path:', component.props.componentPath);
                return null;
            }

            // Get the component class from the namespace
            const namespace = window[layout.namespace];
            if (!namespace || !namespace[layout.type]) {
                console.error('Could not find component:', layout.type, 'in namespace:', layout.namespace);
                return null;
            }

            const ComponentClass = namespace[layout.type];

            // Process children recursively if they exist
            const processChildren = (children) => {
                if (!children) return null;
                if (Array.isArray(children)) {
                    return children.map((child, index) => {
                        const processed = renderDashComponent(child);
                        return processed ? React.cloneElement(processed, { key: index }) : null;
                    });
                }
                return renderDashComponent(children);
            };

            // Process props to ensure they're in the right format for React
            const processProps = (rawProps) => {
                const { children, componentPath, ...otherProps } = rawProps;
                const processedProps = {};
                Object.entries(otherProps).forEach(([key, value]) => {
                    if (key === 'style') {
                        processedProps.style = {
                            width: '100%',
                            height: '100%',
                            ...(value || {})
                        };
                    } else if (key.startsWith('_dashprivate')) {
                        // Skip internal Dash props
                        return;
                    } else {
                        processedProps[key] = value;
                    }
                });
                return processedProps;
            };

            const children = processChildren(layout.props.children);
            const props = processProps(layout.props);

            try {
                return React.createElement(ComponentClass, props, children);
            } catch (error) {
                console.error('Error creating element:', error);
                return null;
            }
        }

        // Handle Dash 2.x components with _dashprivate_layout (backwards compatibility)
        if (component.props?._dashprivate_layout) {
            const layout = component.props._dashprivate_layout;

            // Get the component class from the namespace
            const namespace = window[layout.namespace];
            if (!namespace || !namespace[layout.type]) {
                console.error('Could not find component:', layout.type, 'in namespace:', layout.namespace);
                return null;
            }

            const ComponentClass = namespace[layout.type];

            // Process children recursively if they exist
            const processChildren = (children) => {
                if (!children) return null;
                if (Array.isArray(children)) {
                    return children.map((child, index) => {
                        const processed = renderDashComponent(child);
                        return processed ? React.cloneElement(processed, { key: index }) : null;
                    });
                }
                return renderDashComponent(children);
            };

            // Process props to ensure they're in the right format for React
            const processProps = (rawProps) => {
                const { children, ...otherProps } = rawProps;

                // Convert any prop keys from camelCase to lowercase for HTML elements
                const processedProps = {};
                Object.entries(otherProps).forEach(([key, value]) => {
                    if (key === 'style') {
                        processedProps.style = {
                            width: '100%',
                            height: '100%',
                            ...(value || {})
                        };
                    } else if (key === '_dashprivate_layout') {
                        // Skip internal Dash props
                        return;
                    } else {
                        processedProps[key] = value;
                    }
                });

                return processedProps;
            };

            // Process children and create the element
            const children = processChildren(layout.props.children);
            const props = processProps(layout.props);

            try {
                return React.createElement(ComponentClass, props, children);
            } catch (error) {
                console.error('Error creating element:', error);
                return null;
            }
        }

        // Handle HTML elements
        if (typeof component.type === 'string') {
            const processedChildren = component.props?.children ?
                (Array.isArray(component.props.children) ?
                    component.props.children.map((child, index) => React.cloneElement(renderDashComponent(child), { key: index })) :
                    renderDashComponent(component.props.children)
                ) : null;

            return React.createElement(
                component.type.toLowerCase(),
                {
                    ...component.props,
                    style: { ...component.props.style }
                },
                processedChildren
            );
        }

        console.warn('Could not process component:', component);
        return null;
    };

    const processHandleProps = (handles) => {
        const processedHandles = handles.map(handle => {
            const {
                id,
                type,
                position,
                style,
                isConnectable,
                isConnectableStart,
                isConnectableEnd,
                onConnect,
                isValidConnection
            } = handle;
    
            // Convert position from string to Position enum if possible
            let processedPosition = position;
    
            return {
                id:id,
                type:type,
                position: processedPosition,
                style: style,
                isConnectable: isConnectable,
                isConnectableStart: isConnectableStart,
                isConnectableEnd: isConnectableEnd,
                onConnect: onConnect,
                isValidConnection: isValidConnection
            };
        });

        return processedHandles;
    };

    const processedHandles = processHandleProps(data.handles || []);

    // Glass morphism styling for the resizable node
    const nodeStyle = {
        width: '100%',
        height: '100%',
        backdropFilter: 'blur(12px) saturate(180%)',
        WebkitBackdropFilter: 'blur(12px) saturate(180%)',
        background: 'var(--df-glass-bg, rgba(255, 255, 255, 0.72))',
        border: selected
            ? '2px solid var(--df-selection-border, rgba(59, 130, 246, 0.4))'
            : '1px solid var(--df-glass-border, rgba(255, 255, 255, 0.5))',
        borderRadius: 'var(--df-radius-lg, 14px)',
        boxShadow: selected
            ? 'var(--df-glass-shadow-hover, 0 8px 32px rgba(31, 38, 135, 0.25))'
            : 'var(--df-glass-shadow, 0 8px 32px rgba(31, 38, 135, 0.15))',
        position: 'relative',
        // Use visible overflow so handles are not clipped
        overflow: 'visible',
        transition: 'all 250ms ease',
        ...data.style,
    };

    const contentStyle = {
        padding: data.padding !== undefined ? data.padding : 10,
        width: '100%',
        height: '100%',
        display: 'flex',
        alignItems: data.alignItems || 'stretch',
        justifyContent: data.justifyContent || 'stretch',
        flexDirection: data.flexDirection || 'column',
        boxSizing: 'border-box',
        overflow: 'auto',
    };

    // Calculate inner dimensions for child components (accounting for padding)
    const padding = data.padding !== undefined ? data.padding : 10;
    const innerWidth = dimensions.width - (padding * 2);
    const innerHeight = dimensions.height - (padding * 2);

    return (
        <div className="df-glass-node df-resizable-node" style={nodeStyle}>
            <NodeResizer
                isVisible={selected}
                minWidth={data.minWidth || 100}
                minHeight={data.minHeight || 50}
                keepAspectRatio={data.keepAspectRatio || false}
                maxWidth={data.maxWidth}
                maxHeight={data.maxHeight}
                shouldResize={(event, params) => {
                    if (data.maxWidth && params.width > data.maxWidth) return false;
                    if (data.maxHeight && params.height > data.maxHeight) return false;
                    return true;
                }}
                handleStyle={{
                    width: 10,
                    height: 10,
                    background: 'var(--df-handle-bg, #fff)',
                    border: '2px solid var(--df-handle-border, #64748b)',
                    borderRadius: '2px',
                }}
                lineStyle={{
                    borderWidth: 1,
                    borderColor: 'var(--df-selection-border, rgba(59, 130, 246, 0.4))',
                }}
            />
            {processedHandles.map((handle, index) => (
                <Handle
                    key={handle.id || index}
                    type={handle.type}
                    position={handle.position}
                    id={handle.id}
                    style={{
                        width: 14,
                        height: 14,
                        background: 'var(--df-handle-bg, #fff)',
                        border: '2px solid var(--df-handle-border, #64748b)',
                        zIndex: 10,
                        ...handle.style,
                    }}
                    isConnectable={handle.isConnectable}
                    isConnectableStart={handle.isConnectableStart}
                    isConnectableEnd={handle.isConnectableEnd}
                    onConnect={handle.onConnect}
                    isValidConnection={handle.isValidConnection}
                />
            ))}
            <div
                ref={contentRef}
                className="df-resizable-node-content"
                style={contentStyle}
                data-inner-width={innerWidth}
                data-inner-height={innerHeight}
            >
                {data.label && renderDashComponent(data.label)}
            </div>
        </div>
    );
});

ResizableNode.displayName = 'ResizableNode';

ResizableNode.propTypes = {
    /**
     * Node data object containing label, handles, and styling options
     */
    data: PropTypes.shape({
        /** Content to render inside the node - can be string, React element, or Dash component */
        label: PropTypes.any,
        /** Array of connection handles for this node */
        handles: PropTypes.arrayOf(PropTypes.shape({
            /** Unique identifier for the handle */
            id: PropTypes.string.isRequired,
            /** Handle type: 'source' or 'target' */
            type: PropTypes.string.isRequired,
            /** Handle position: 'top', 'bottom', 'left', or 'right' */
            position: PropTypes.string.isRequired,
            /** Custom CSS styles for the handle */
            style: PropTypes.object,
            /** Whether the handle can be connected */
            isConnectable: PropTypes.bool,
            /** Whether connections can start from this handle */
            isConnectableStart: PropTypes.bool,
            /** Whether connections can end at this handle */
            isConnectableEnd: PropTypes.bool,
            /** Callback when a connection is made */
            onConnect: PropTypes.func,
            /** Validation function for connections */
            isValidConnection: PropTypes.func
        })).isRequired,
        /** Custom CSS styles for the node container */
        style: PropTypes.object,
        /** Initial width of the node before resize */
        initialWidth: PropTypes.number,
        /** Initial height of the node before resize */
        initialHeight: PropTypes.number,
        /** Minimum width constraint for resizing */
        minWidth: PropTypes.number,
        /** Minimum height constraint for resizing */
        minHeight: PropTypes.number,
        /** Maximum width constraint for resizing */
        maxWidth: PropTypes.number,
        /** Maximum height constraint for resizing */
        maxHeight: PropTypes.number,
        /** Maintain aspect ratio when resizing */
        keepAspectRatio: PropTypes.bool,
        /** Padding inside the node content area */
        padding: PropTypes.number,
        /** Flexbox align-items value for content */
        alignItems: PropTypes.string,
        /** Flexbox justify-content value for content */
        justifyContent: PropTypes.string,
        /** Flexbox flex-direction value for content */
        flexDirection: PropTypes.string,
    }).isRequired,
    /** Whether the node is currently selected */
    selected: PropTypes.bool,
    /** Current width of the node (set by React Flow during resize) */
    width: PropTypes.number,
    /** Current height of the node (set by React Flow during resize) */
    height: PropTypes.number,
};

export default ResizableNode;