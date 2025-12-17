// src/lib/components/DevTools.js
import React from 'react';
import PropTypes from 'prop-types';
import { Panel, useViewport } from '@xyflow/react';

const ViewportLogger = () => {
    const viewport = useViewport();
    return (
        <div style={{ padding: '8px', background: '#fff', borderRadius: '4px', margin: '4px' }}>
            <strong>Viewport:</strong>
            <div>x: {viewport.x.toFixed(2)}</div>
            <div>y: {viewport.y.toFixed(2)}</div>
            <div>zoom: {viewport.zoom.toFixed(2)}</div>
        </div>
    );
};

const NodeInspector = ({ nodes }) => (
    <div style={{ padding: '8px', background: '#fff', borderRadius: '4px', margin: '4px', maxHeight: '300px', overflow: 'auto' }}>
        <strong>Nodes ({nodes.length}):</strong>
        {nodes.map((node) => (
            <div key={node.id} style={{ fontSize: '11px', borderBottom: '1px solid #eee', padding: '2px 0' }}>
                <div><strong>ID:</strong> {node.id}</div>
                <div><strong>Type:</strong> {node.type || 'default'}</div>
                <div><strong>Position:</strong> ({node.position?.x?.toFixed(0)}, {node.position?.y?.toFixed(0)})</div>
            </div>
        ))}
    </div>
);

/**
 * DevTools component for displaying debug information about the flow
 */
const DevTools = ({ nodes }) => {
    return (
        <Panel position="top-right" style={{ maxHeight: '400px', overflow: 'auto', fontSize: '12px' }}>
            <ViewportLogger />
            <NodeInspector nodes={nodes} />
        </Panel>
    );
};

DevTools.propTypes = {
    /**
     * Array of nodes to display information about
     */
    nodes: PropTypes.arrayOf(PropTypes.shape({
        id: PropTypes.string.isRequired,
        type: PropTypes.string,
        position: PropTypes.shape({
            x: PropTypes.number,
            y: PropTypes.number
        })
    })).isRequired
};

DevTools.displayName = 'DevTools';

export default DevTools;