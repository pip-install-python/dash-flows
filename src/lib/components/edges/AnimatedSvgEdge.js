// src/lib/components/edges/AnimatedSvgEdge.js
import React from 'react';
import PropTypes from 'prop-types';
import { BaseEdge, getBezierPath } from '@xyflow/react';

/**
 * AnimatedSvgEdge - An edge that animates a custom SVG element along the path
 * Useful for showing data flow direction or active connections
 */
const AnimatedSvgEdge = ({
    id,
    sourceX,
    sourceY,
    targetX,
    targetY,
    sourcePosition,
    targetPosition,
    style,
    markerEnd,
    markerStart,
    data,
    selected,
}) => {
    const [edgePath] = getBezierPath({
        sourceX,
        sourceY,
        sourcePosition,
        targetX,
        targetY,
        targetPosition,
    });

    // Animation configuration from data prop
    const animationDuration = data?.duration || 2;
    const animationShape = data?.shape || 'circle';
    const animationSize = data?.size || 5;
    const animationColor = data?.color || 'var(--df-edge-animated-color, #3b82f6)';
    const animationCount = data?.count || 1;
    const reverse = data?.reverse || false;

    const edgeStyle = {
        stroke: selected
            ? 'var(--df-edge-selected, #3b82f6)'
            : 'var(--df-edge-stroke, #64748b)',
        strokeWidth: selected ? 2 : 1.5,
        ...style,
    };

    // Render the animated shape based on configuration
    const renderAnimatedShape = (index) => {
        const delay = (animationDuration / animationCount) * index;
        const keyTimes = reverse ? '0;1' : '0;1';
        const calcMode = 'linear';

        switch (animationShape) {
            case 'circle':
                return (
                    <circle
                        key={`${id}-anim-${index}`}
                        r={animationSize}
                        fill={animationColor}
                    >
                        <animateMotion
                            dur={`${animationDuration}s`}
                            repeatCount="indefinite"
                            path={edgePath}
                            begin={`${delay}s`}
                            keyPoints={reverse ? '1;0' : '0;1'}
                            keyTimes={keyTimes}
                            calcMode={calcMode}
                        />
                    </circle>
                );
            case 'rect':
                return (
                    <rect
                        key={`${id}-anim-${index}`}
                        width={animationSize * 2}
                        height={animationSize}
                        x={-animationSize}
                        y={-animationSize / 2}
                        rx={2}
                        fill={animationColor}
                    >
                        <animateMotion
                            dur={`${animationDuration}s`}
                            repeatCount="indefinite"
                            path={edgePath}
                            begin={`${delay}s`}
                            rotate="auto"
                            keyPoints={reverse ? '1;0' : '0;1'}
                            keyTimes={keyTimes}
                            calcMode={calcMode}
                        />
                    </rect>
                );
            case 'arrow':
                const arrowSize = animationSize;
                return (
                    <polygon
                        key={`${id}-anim-${index}`}
                        points={`${-arrowSize},-${arrowSize / 2} ${arrowSize},0 ${-arrowSize},${arrowSize / 2}`}
                        fill={animationColor}
                    >
                        <animateMotion
                            dur={`${animationDuration}s`}
                            repeatCount="indefinite"
                            path={edgePath}
                            begin={`${delay}s`}
                            rotate="auto"
                            keyPoints={reverse ? '1;0' : '0;1'}
                            keyTimes={keyTimes}
                            calcMode={calcMode}
                        />
                    </polygon>
                );
            case 'pulse':
                return (
                    <circle
                        key={`${id}-anim-${index}`}
                        r={animationSize}
                        fill={animationColor}
                    >
                        <animateMotion
                            dur={`${animationDuration}s`}
                            repeatCount="indefinite"
                            path={edgePath}
                            begin={`${delay}s`}
                            keyPoints={reverse ? '1;0' : '0;1'}
                            keyTimes={keyTimes}
                            calcMode={calcMode}
                        />
                        <animate
                            attributeName="r"
                            values={`${animationSize};${animationSize * 1.5};${animationSize}`}
                            dur="0.5s"
                            repeatCount="indefinite"
                        />
                        <animate
                            attributeName="opacity"
                            values="1;0.5;1"
                            dur="0.5s"
                            repeatCount="indefinite"
                        />
                    </circle>
                );
            default:
                return (
                    <circle
                        key={`${id}-anim-${index}`}
                        r={animationSize}
                        fill={animationColor}
                    >
                        <animateMotion
                            dur={`${animationDuration}s`}
                            repeatCount="indefinite"
                            path={edgePath}
                            begin={`${delay}s`}
                            keyPoints={reverse ? '1;0' : '0;1'}
                            keyTimes={keyTimes}
                            calcMode={calcMode}
                        />
                    </circle>
                );
        }
    };

    // Create array of animated shapes
    const animatedShapes = [];
    for (let i = 0; i < animationCount; i++) {
        animatedShapes.push(renderAnimatedShape(i));
    }

    return (
        <>
            <BaseEdge
                id={id}
                path={edgePath}
                style={edgeStyle}
                markerEnd={markerEnd}
                markerStart={markerStart}
            />
            <g className="df-animated-svg-edge">
                {animatedShapes}
            </g>
        </>
    );
};

AnimatedSvgEdge.propTypes = {
    id: PropTypes.string.isRequired,
    sourceX: PropTypes.number.isRequired,
    sourceY: PropTypes.number.isRequired,
    targetX: PropTypes.number.isRequired,
    targetY: PropTypes.number.isRequired,
    sourcePosition: PropTypes.string,
    targetPosition: PropTypes.string,
    style: PropTypes.object,
    markerEnd: PropTypes.any,
    markerStart: PropTypes.any,
    selected: PropTypes.bool,
    data: PropTypes.shape({
        /** Animation duration in seconds */
        duration: PropTypes.number,
        /** Shape to animate: 'circle', 'rect', 'arrow', 'pulse' */
        shape: PropTypes.oneOf(['circle', 'rect', 'arrow', 'pulse']),
        /** Size of the animated shape */
        size: PropTypes.number,
        /** Color of the animated shape */
        color: PropTypes.string,
        /** Number of shapes to animate along the path */
        count: PropTypes.number,
        /** Reverse the animation direction */
        reverse: PropTypes.bool,
    }),
};

export default AnimatedSvgEdge;