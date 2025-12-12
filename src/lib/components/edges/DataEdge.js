// src/lib/components/edges/DataEdge.js
import React from 'react';
import PropTypes from 'prop-types';
import { BaseEdge, EdgeLabelRenderer, getBezierPath, useReactFlow } from '@xyflow/react';

/**
 * DataEdge - An edge that displays data from the source node
 * Useful for showing data flow between nodes
 */
const DataEdge = ({
    id,
    sourceX,
    sourceY,
    targetX,
    targetY,
    sourcePosition,
    targetPosition,
    source,
    style,
    markerEnd,
    markerStart,
    data,
    selected,
}) => {
    const { getNode } = useReactFlow();

    const [edgePath, labelX, labelY] = getBezierPath({
        sourceX,
        sourceY,
        sourcePosition,
        targetX,
        targetY,
        targetPosition,
    });

    // Get the source node's data
    const sourceNode = getNode(source);
    const dataKey = data?.key;
    const dataValue = dataKey && sourceNode?.data ? sourceNode.data[dataKey] : null;

    // Format the displayed value
    const formatValue = (value) => {
        if (value === null || value === undefined) return '';
        if (typeof value === 'object') return JSON.stringify(value);
        return String(value);
    };

    const displayValue = formatValue(dataValue);

    const glassLabelStyle = {
        backdropFilter: 'blur(8px) saturate(150%)',
        WebkitBackdropFilter: 'blur(8px) saturate(150%)',
        background: 'var(--df-edge-label-bg, rgba(255, 255, 255, 0.85))',
        padding: '4px 10px',
        borderRadius: 'var(--df-radius-sm, 6px)',
        fontSize: '11px',
        fontWeight: 600,
        fontFamily: 'ui-monospace, SFMono-Regular, SF Mono, Menlo, monospace',
        color: 'var(--df-edge-data-color, #3b82f6)',
        border: '1px solid var(--df-edge-label-border, rgba(255, 255, 255, 0.6))',
        boxShadow: 'var(--df-edge-label-shadow, 0 2px 8px rgba(0, 0, 0, 0.08))',
        ...data?.labelStyle,
    };

    const edgeStyle = {
        stroke: selected
            ? 'var(--df-edge-selected, #3b82f6)'
            : 'var(--df-edge-stroke, #64748b)',
        strokeWidth: selected ? 2 : 1.5,
        ...style,
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
            {displayValue && (
                <EdgeLabelRenderer>
                    <div
                        style={{
                            position: 'absolute',
                            transform: `translate(-50%, -50%) translate(${labelX}px, ${labelY}px)`,
                            pointerEvents: 'none',
                        }}
                        className="nodrag nopan df-edge-data-label"
                    >
                        <span style={glassLabelStyle}>
                            {data?.prefix || ''}{displayValue}{data?.suffix || ''}
                        </span>
                    </div>
                </EdgeLabelRenderer>
            )}
        </>
    );
};

DataEdge.propTypes = {
    id: PropTypes.string.isRequired,
    sourceX: PropTypes.number.isRequired,
    sourceY: PropTypes.number.isRequired,
    targetX: PropTypes.number.isRequired,
    targetY: PropTypes.number.isRequired,
    sourcePosition: PropTypes.string,
    targetPosition: PropTypes.string,
    source: PropTypes.string.isRequired,
    style: PropTypes.object,
    markerEnd: PropTypes.any,
    markerStart: PropTypes.any,
    selected: PropTypes.bool,
    data: PropTypes.shape({
        /** Key to read from source node's data */
        key: PropTypes.string.isRequired,
        /** Prefix to display before the value */
        prefix: PropTypes.string,
        /** Suffix to display after the value */
        suffix: PropTypes.string,
        /** Custom label styles */
        labelStyle: PropTypes.object,
    }),
};

export default DataEdge;