// src/lib/components/nodes/NodeStatusIndicator.js
import React, { memo } from 'react';
import PropTypes from 'prop-types';

/**
 * NodeStatusIndicator - A wrapper component that shows status indicators around nodes
 * Status can be: "initial", "loading", "success", "error"
 * Loading variants: "border" (spinning border) or "overlay" (full overlay with spinner)
 */
const NodeStatusIndicator = memo(({ status, loadingVariant, children, className, style }) => {
    const getStatusClass = () => {
        switch (status) {
            case 'loading':
                return loadingVariant === 'overlay'
                    ? 'df-node-status-loading-overlay'
                    : 'df-node-status-loading-border';
            case 'success':
                return 'df-node-status-success';
            case 'error':
                return 'df-node-status-error';
            case 'initial':
            default:
                return 'df-node-status-initial';
        }
    };

    const containerClasses = [
        'df-node-status-indicator',
        getStatusClass(),
        className || '',
    ].filter(Boolean).join(' ');

    return (
        <div className={containerClasses} style={style}>
            {children}
            {status === 'loading' && loadingVariant === 'overlay' && (
                <div className="df-node-status-overlay">
                    <div className="df-node-status-spinner" />
                </div>
            )}
        </div>
    );
});

NodeStatusIndicator.displayName = 'NodeStatusIndicator';

NodeStatusIndicator.propTypes = {
    /** The current status of the node */
    status: PropTypes.oneOf(['initial', 'loading', 'success', 'error']),
    /** Loading animation variant - "border" shows spinning border, "overlay" shows full overlay */
    loadingVariant: PropTypes.oneOf(['border', 'overlay']),
    /** The node content to wrap */
    children: PropTypes.node,
    /** Additional CSS class name */
    className: PropTypes.string,
    /** Custom inline styles */
    style: PropTypes.object,
};

NodeStatusIndicator.defaultProps = {
    status: 'initial',
    loadingVariant: 'border',
};

export default NodeStatusIndicator;