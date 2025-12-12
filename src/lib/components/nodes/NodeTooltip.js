// src/lib/components/nodes/NodeTooltip.js
import React, { memo, useState } from 'react';
import PropTypes from 'prop-types';
import { NodeToolbar, Position } from '@xyflow/react';

/**
 * NodeTooltip - A wrapper that displays a tooltip when hovered
 * Built on top of React Flow's NodeToolbar component
 */
const NodeTooltip = memo(({
    children,
    tooltipContent,
    position,
    offset,
    className,
    tooltipClassName,
    style,
    tooltipStyle,
    showOnHover,
}) => {
    const [isHovered, setIsHovered] = useState(false);

    const handleMouseEnter = () => {
        if (showOnHover) {
            setIsHovered(true);
        }
    };

    const handleMouseLeave = () => {
        if (showOnHover) {
            setIsHovered(false);
        }
    };

    const containerClasses = [
        'df-node-tooltip-container',
        className || '',
    ].filter(Boolean).join(' ');

    const tooltipClasses = [
        'df-node-tooltip',
        tooltipClassName || '',
    ].filter(Boolean).join(' ');

    // Get position enum
    const getPosition = () => {
        switch (position) {
            case 'top': return Position.Top;
            case 'bottom': return Position.Bottom;
            case 'left': return Position.Left;
            case 'right': return Position.Right;
            default: return Position.Top;
        }
    };

    return (
        <div
            className={containerClasses}
            style={style}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
        >
            {tooltipContent && (showOnHover ? isHovered : true) && (
                <NodeToolbar
                    isVisible={showOnHover ? isHovered : true}
                    position={getPosition()}
                    offset={offset}
                    className={tooltipClasses}
                    style={tooltipStyle}
                >
                    {tooltipContent}
                </NodeToolbar>
            )}
            {children}
        </div>
    );
});

NodeTooltip.displayName = 'NodeTooltip';

NodeTooltip.propTypes = {
    /** The node content */
    children: PropTypes.node,
    /** Content to display in the tooltip */
    tooltipContent: PropTypes.node,
    /** Position of the tooltip relative to the node */
    position: PropTypes.oneOf(['top', 'bottom', 'left', 'right']),
    /** Offset from the node in pixels */
    offset: PropTypes.number,
    /** CSS class for the container */
    className: PropTypes.string,
    /** CSS class for the tooltip */
    tooltipClassName: PropTypes.string,
    /** Inline styles for the container */
    style: PropTypes.object,
    /** Inline styles for the tooltip */
    tooltipStyle: PropTypes.object,
    /** Show tooltip only on hover (default: true) */
    showOnHover: PropTypes.bool,
};

NodeTooltip.defaultProps = {
    position: 'top',
    offset: 10,
    showOnHover: true,
};

export default NodeTooltip;