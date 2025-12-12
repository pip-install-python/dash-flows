// src/lib/components/nodes/DefaultNode.js
import React, { memo } from 'react';
import PropTypes from 'prop-types';
import { Handle, Position } from '@xyflow/react';

/**
 * DefaultNode - Glass morphism styled node with source and target handles
 * Equivalent to React Flow's built-in 'default' node type
 *
 * Uses CSS classes from glass-theme.css for styling, supporting:
 * - Light/dark mode via colorMode prop or Mantine color scheme
 * - Theme presets (glass, solid, minimal)
 * - Custom CSS variable overrides via theme prop
 * - Status indicators (initial, loading, success, error)
 * - Custom icons via DashIconify or any Dash component
 */
const DefaultNode = memo(({ data, selected, isConnectable }) => {
    const renderDashComponent = (component) => {
        if (!component) return null;
        if (typeof component === 'string') return component;
        if (React.isValidElement(component)) return component;

        // Handle Dash 3.0+ componentPath format
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

        // Handle Dash 2.x _dashprivate_layout format
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

        // Handle serialized Dash component format (from callbacks)
        // This is when a component like DashIconify is passed through node data
        if (component.namespace && component.type && component.props) {
            // Try the namespace directly first
            let namespace = window[component.namespace];

            // If not found, try window.dash_clientside.no_update workaround
            // Some libraries expose components differently
            if (!namespace && window.dash_clientside) {
                // Check if it's available through the Dash renderer
                const dashRenderer = window.DashRenderer;
                if (dashRenderer && dashRenderer.componentsRegistry) {
                    namespace = dashRenderer.componentsRegistry[component.namespace];
                }
            }

            if (!namespace || !namespace[component.type]) {
                // Fallback: for DashIconify, we can render it as an img/svg via iconify API
                if (component.namespace === 'dash_iconify' && component.type === 'DashIconify' && component.props.icon) {
                    const iconName = component.props.icon;
                    const width = component.props.width || 20;
                    const height = component.props.height || width;
                    const color = component.props.color || 'currentColor';
                    // Use Iconify API to load the icon
                    const iconUrl = `https://api.iconify.design/${iconName.replace(':', '/')}.svg?color=${encodeURIComponent(color)}&width=${width}&height=${height}`;
                    return React.createElement('img', {
                        src: iconUrl,
                        alt: iconName,
                        width: width,
                        height: height,
                        style: { display: 'block' }
                    });
                }
                return null;
            }
            const ComponentClass = namespace[component.type];
            const { children, ...otherProps } = component.props;
            try {
                return React.createElement(ComponentClass, otherProps, children);
            } catch (error) {
                return null;
            }
        }

        return null;
    };

    // Support both 'label' and 'title' props (title is alias for label)
    const labelText = data.title || data.label;
    const labelContent = typeof labelText === 'string'
        ? labelText
        : renderDashComponent(labelText);

    // Render custom icon or default SVG (cog/gear icon for process node)
    const renderIcon = () => {
        if (data.icon) {
            const iconContent = renderDashComponent(data.icon);
            if (iconContent) {
                return iconContent;
            }
        }
        // Default SVG icon - gear/cog for process
        return (
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="3" />
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
            </svg>
        );
    };

    // Get status class based on data.status
    const getStatusClass = () => {
        switch (data.status) {
            case 'loading':
                return data.loadingVariant === 'overlay'
                    ? 'df-status-loading-overlay'
                    : 'df-status-loading';
            case 'success':
                return 'df-status-success';
            case 'error':
                return 'df-status-error';
            default:
                return '';
        }
    };

    // Determine content configuration
    const hasIcon = data.showIcon !== undefined ? data.showIcon : !!data.icon;
    const hasLabel = !!(data.label || data.title);
    const hasBody = !!data.body;
    const hasSublabel = !!data.sublabel;
    const hasText = hasLabel || hasBody || hasSublabel;

    // Determine layout mode (default: stacked)
    const layout = data.layout || 'stacked';

    // Determine content class for sizing
    const getContentClass = () => {
        if (hasIcon && !hasText) return 'df-icon-only';
        if (!hasIcon && hasText) return 'df-text-only';
        if (hasIcon && hasText) return 'df-full-content';
        return '';
    };

    // Build class names
    const nodeClasses = [
        'df-glass-node',
        'df-default-node',
        `df-layout-${layout}`,
        getContentClass(),
        selected ? 'selected' : '',
        getStatusClass(),
        data.className || '',
    ].filter(Boolean).join(' ');

    const labelClasses = [
        'df-node-label',
        data.multiline ? 'multiline' : '',
    ].filter(Boolean).join(' ');

    const iconClasses = [
        'df-node-icon',
        data.icon ? 'df-icon-custom' : '',
    ].filter(Boolean).join(' ');

    // Build icon style with optional color override
    const iconStyle = data.iconColor ? { backgroundColor: data.iconColor } : {};

    // Body text classes
    const bodyClasses = [
        'df-node-body',
        data.multiline ? 'multiline' : '',
    ].filter(Boolean).join(' ');

    // Render horizontal layout
    if (layout === 'horizontal' && hasIcon && hasText) {
        return (
            <div className={nodeClasses} style={data.style}>
                <Handle
                    type="target"
                    position={data.targetPosition || Position.Top}
                    isConnectable={isConnectable}
                    style={data.handleStyle}
                />
                <div className="df-node-icon-column">
                    <div className={iconClasses} style={iconStyle}>
                        {renderIcon()}
                    </div>
                </div>
                <div className="df-node-text-column">
                    {hasLabel && (
                        <div className={labelClasses}>
                            {labelContent}
                        </div>
                    )}
                    {data.sublabel && (
                        <div className="df-node-sublabel">
                            {data.sublabel}
                        </div>
                    )}
                    {data.body && (
                        <div className={bodyClasses}>
                            {typeof data.body === 'string' ? data.body : renderDashComponent(data.body)}
                        </div>
                    )}
                </div>
                <Handle
                    type="source"
                    position={data.sourcePosition || Position.Bottom}
                    isConnectable={isConnectable}
                    style={data.handleStyle}
                />
                {data.status === 'loading' && data.loadingVariant === 'overlay' && (
                    <div className="df-status-overlay">
                        <div className="df-status-spinner" />
                    </div>
                )}
            </div>
        );
    }

    // Default stacked layout
    return (
        <div className={nodeClasses} style={data.style}>
            <Handle
                type="target"
                position={data.targetPosition || Position.Top}
                isConnectable={isConnectable}
                style={data.handleStyle}
            />
            {hasIcon && (
                <div className={iconClasses} style={iconStyle}>
                    {renderIcon()}
                </div>
            )}
            {hasText && (
                <div className="df-node-content">
                    {hasLabel && (
                        <div className={labelClasses}>
                            {labelContent}
                        </div>
                    )}
                    {data.sublabel && (
                        <div className="df-node-sublabel">
                            {data.sublabel}
                        </div>
                    )}
                    {data.body && (
                        <div className={bodyClasses}>
                            {typeof data.body === 'string' ? data.body : renderDashComponent(data.body)}
                        </div>
                    )}
                </div>
            )}
            <Handle
                type="source"
                position={data.sourcePosition || Position.Bottom}
                isConnectable={isConnectable}
                style={data.handleStyle}
            />
            {/* Loading overlay spinner */}
            {data.status === 'loading' && data.loadingVariant === 'overlay' && (
                <div className="df-status-overlay">
                    <div className="df-status-spinner" />
                </div>
            )}
        </div>
    );
});

DefaultNode.displayName = 'DefaultNode';

DefaultNode.propTypes = {
    /**
     * Node data object containing label, styling, and handle configuration
     */
    data: PropTypes.shape({
        /** Primary content to display in the node - string or Dash component */
        label: PropTypes.any,
        /** Alias for label - use for clarity when also using body text */
        title: PropTypes.any,
        /** Secondary text displayed below the main label */
        sublabel: PropTypes.string,
        /** Body text displayed below title/sublabel */
        body: PropTypes.any,
        /** Custom icon - DashIconify component or any Dash component */
        icon: PropTypes.any,
        /** Background color for the icon container */
        iconColor: PropTypes.string,
        /** Show/hide icon (default: true if icon prop provided, false otherwise) */
        showIcon: PropTypes.bool,
        /** Layout mode: 'stacked' (vertical) or 'horizontal' (icon left, text right) */
        layout: PropTypes.oneOf(['stacked', 'horizontal']),
        /** Allow multiline text wrapping */
        multiline: PropTypes.bool,
        /** Custom CSS styles for the node container */
        style: PropTypes.object,
        /** Additional CSS class name */
        className: PropTypes.string,
        /** Custom CSS styles for connection handles */
        handleStyle: PropTypes.object,
        /** Position for the target (input) handle: 'top', 'bottom', 'left', 'right' */
        targetPosition: PropTypes.string,
        /** Position for the source (output) handle: 'top', 'bottom', 'left', 'right' */
        sourcePosition: PropTypes.string,
        /** Node status: 'initial', 'loading', 'success', 'error' */
        status: PropTypes.oneOf(['initial', 'loading', 'success', 'error']),
        /** Loading animation variant: 'border' or 'overlay' */
        loadingVariant: PropTypes.oneOf(['border', 'overlay']),
    }).isRequired,
    /** Whether the node is currently selected */
    selected: PropTypes.bool,
    /** Whether connections can be made to/from this node */
    isConnectable: PropTypes.bool,
};

export default DefaultNode;