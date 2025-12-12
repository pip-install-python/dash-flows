// src/lib/components/nodes/ButtonHandle.js
import React, { memo } from 'react';
import PropTypes from 'prop-types';
import { Handle, Position } from '@xyflow/react';

/**
 * ButtonHandle - A handle that can also function as a button
 * Useful for triggering actions when clicking on a connection point
 */
const ButtonHandle = memo(({
    id,
    type,
    position,
    isConnectable,
    onClick,
    onConnect,
    children,
    className,
    style,
    showButton,
    buttonContent,
    buttonClassName,
    buttonStyle,
}) => {
    // Get position enum
    const getPosition = () => {
        switch (position) {
            case 'top': return Position.Top;
            case 'bottom': return Position.Bottom;
            case 'left': return Position.Left;
            case 'right': return Position.Right;
            default: return Position.Bottom;
        }
    };

    const handleClasses = [
        'df-button-handle',
        showButton ? 'df-button-handle-with-button' : '',
        className || '',
    ].filter(Boolean).join(' ');

    const buttonClasses = [
        'df-button-handle-button',
        buttonClassName || '',
    ].filter(Boolean).join(' ');

    const handleClick = (e) => {
        if (onClick) {
            e.stopPropagation();
            onClick(e, { id, type, position });
        }
    };

    return (
        <div className="df-button-handle-container">
            <Handle
                id={id}
                type={type}
                position={getPosition()}
                isConnectable={isConnectable}
                onConnect={onConnect}
                className={handleClasses}
                style={style}
            />
            {showButton && (
                <button
                    className={buttonClasses}
                    style={buttonStyle}
                    onClick={handleClick}
                    type="button"
                >
                    {buttonContent || children || '+'}
                </button>
            )}
        </div>
    );
});

ButtonHandle.displayName = 'ButtonHandle';

ButtonHandle.propTypes = {
    /** Unique identifier for the handle */
    id: PropTypes.string,
    /** Type of handle - source or target */
    type: PropTypes.oneOf(['source', 'target']).isRequired,
    /** Position of the handle on the node */
    position: PropTypes.oneOf(['top', 'bottom', 'left', 'right']),
    /** Whether the handle can connect to other nodes */
    isConnectable: PropTypes.bool,
    /** Click handler for the button */
    onClick: PropTypes.func,
    /** Called when a connection is made */
    onConnect: PropTypes.func,
    /** Child content for the button */
    children: PropTypes.node,
    /** CSS class for the handle */
    className: PropTypes.string,
    /** Inline styles for the handle */
    style: PropTypes.object,
    /** Whether to show the button (default: false) */
    showButton: PropTypes.bool,
    /** Content to display in the button */
    buttonContent: PropTypes.node,
    /** CSS class for the button */
    buttonClassName: PropTypes.string,
    /** Inline styles for the button */
    buttonStyle: PropTypes.object,
};

ButtonHandle.defaultProps = {
    position: 'bottom',
    isConnectable: true,
    showButton: false,
};

export default ButtonHandle;