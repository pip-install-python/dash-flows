// src/lib/components/nodes/NodeSearch.js
import React, { memo, useState, useCallback, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import { useReactFlow, useNodes } from '@xyflow/react';

/**
 * NodeSearch - A search panel for finding and focusing nodes
 * Supports searching by node id, label, or data properties
 */
const NodeSearch = memo(({
    isOpen,
    onClose,
    placeholder,
    className,
    style,
    searchKeys,
    focusOnSelect,
    highlightOnSelect,
    highlightDuration,
    zoomLevel,
}) => {
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedIndex, setSelectedIndex] = useState(0);
    const inputRef = useRef(null);
    const nodes = useNodes();
    const { setCenter, getNode, setNodes } = useReactFlow();

    // Focus input when panel opens
    useEffect(() => {
        if (isOpen && inputRef.current) {
            inputRef.current.focus();
            setSearchTerm('');
            setSelectedIndex(0);
        }
    }, [isOpen]);

    // Filter nodes based on search term
    const filteredNodes = nodes.filter((node) => {
        if (!searchTerm) return false;
        const term = searchTerm.toLowerCase();

        // Search through specified keys
        for (const key of searchKeys) {
            if (key === 'id' && node.id.toLowerCase().includes(term)) {
                return true;
            }
            if (key === 'type' && node.type?.toLowerCase().includes(term)) {
                return true;
            }
            if (node.data) {
                const value = node.data[key];
                if (value && String(value).toLowerCase().includes(term)) {
                    return true;
                }
            }
        }
        return false;
    });

    // Handle node selection
    const handleSelectNode = useCallback((node) => {
        if (focusOnSelect) {
            const nodeData = getNode(node.id);
            if (nodeData) {
                const x = nodeData.position.x + (nodeData.width || 150) / 2;
                const y = nodeData.position.y + (nodeData.height || 50) / 2;
                setCenter(x, y, { zoom: zoomLevel, duration: 500 });
            }
        }

        if (highlightOnSelect) {
            // Add highlight class to node
            setNodes((nds) =>
                nds.map((n) => ({
                    ...n,
                    className: n.id === node.id
                        ? `${n.className || ''} df-node-search-highlight`.trim()
                        : n.className,
                }))
            );

            // Remove highlight after duration
            setTimeout(() => {
                setNodes((nds) =>
                    nds.map((n) => ({
                        ...n,
                        className: n.className?.replace('df-node-search-highlight', '').trim() || '',
                    }))
                );
            }, highlightDuration);
        }

        onClose?.();
    }, [focusOnSelect, highlightOnSelect, highlightDuration, getNode, setCenter, setNodes, zoomLevel, onClose]);

    // Keyboard navigation
    const handleKeyDown = useCallback((e) => {
        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                setSelectedIndex((prev) =>
                    Math.min(prev + 1, filteredNodes.length - 1)
                );
                break;
            case 'ArrowUp':
                e.preventDefault();
                setSelectedIndex((prev) => Math.max(prev - 1, 0));
                break;
            case 'Enter':
                e.preventDefault();
                if (filteredNodes[selectedIndex]) {
                    handleSelectNode(filteredNodes[selectedIndex]);
                }
                break;
            case 'Escape':
                e.preventDefault();
                onClose?.();
                break;
            default:
                break;
        }
    }, [filteredNodes, selectedIndex, handleSelectNode, onClose]);

    // Get display label for node
    const getNodeLabel = (node) => {
        if (node.data?.label) return node.data.label;
        if (node.data?.title) return node.data.title;
        if (node.data?.name) return node.data.name;
        return node.id;
    };

    if (!isOpen) return null;

    const containerClasses = [
        'df-node-search',
        className || '',
    ].filter(Boolean).join(' ');

    const glassStyle = {
        position: 'absolute',
        top: '20px',
        left: '50%',
        transform: 'translateX(-50%)',
        zIndex: 1000,
        minWidth: '300px',
        maxWidth: '400px',
        backdropFilter: 'blur(12px) saturate(150%)',
        WebkitBackdropFilter: 'blur(12px) saturate(150%)',
        background: 'var(--df-search-bg, rgba(255, 255, 255, 0.9))',
        borderRadius: 'var(--df-radius-lg, 12px)',
        border: '1px solid var(--df-search-border, rgba(255, 255, 255, 0.6))',
        boxShadow: 'var(--df-search-shadow, 0 8px 32px rgba(0, 0, 0, 0.12))',
        overflow: 'hidden',
        ...style,
    };

    const inputStyle = {
        width: '100%',
        padding: '12px 16px',
        border: 'none',
        outline: 'none',
        fontSize: '14px',
        background: 'transparent',
        color: 'var(--df-search-text, #1e293b)',
        fontFamily: 'inherit',
    };

    const resultsStyle = {
        maxHeight: '300px',
        overflowY: 'auto',
        borderTop: filteredNodes.length > 0 ? '1px solid var(--df-search-divider, rgba(0, 0, 0, 0.1))' : 'none',
    };

    const resultItemStyle = (isSelected) => ({
        padding: '10px 16px',
        cursor: 'pointer',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        background: isSelected ? 'var(--df-search-selected-bg, rgba(59, 130, 246, 0.1))' : 'transparent',
        transition: 'background 0.15s ease',
    });

    const nodeTypeStyle = {
        fontSize: '11px',
        padding: '2px 8px',
        borderRadius: '4px',
        background: 'var(--df-search-type-bg, rgba(0, 0, 0, 0.05))',
        color: 'var(--df-search-type-color, #64748b)',
        fontFamily: 'ui-monospace, SFMono-Regular, SF Mono, Menlo, monospace',
    };

    return (
        <div className={containerClasses} style={glassStyle}>
            <input
                ref={inputRef}
                type="text"
                value={searchTerm}
                onChange={(e) => {
                    setSearchTerm(e.target.value);
                    setSelectedIndex(0);
                }}
                onKeyDown={handleKeyDown}
                placeholder={placeholder}
                style={inputStyle}
                className="df-node-search-input"
            />
            {filteredNodes.length > 0 && (
                <div style={resultsStyle} className="df-node-search-results">
                    {filteredNodes.map((node, index) => (
                        <div
                            key={node.id}
                            style={resultItemStyle(index === selectedIndex)}
                            className={`df-node-search-item ${index === selectedIndex ? 'selected' : ''}`}
                            onClick={() => handleSelectNode(node)}
                            onMouseEnter={() => setSelectedIndex(index)}
                        >
                            <span className="df-node-search-label">
                                {getNodeLabel(node)}
                            </span>
                            <span style={nodeTypeStyle} className="df-node-search-type">
                                {node.type || 'default'}
                            </span>
                        </div>
                    ))}
                </div>
            )}
            {searchTerm && filteredNodes.length === 0 && (
                <div
                    style={{ padding: '12px 16px', color: 'var(--df-search-empty, #94a3b8)', fontSize: '13px' }}
                    className="df-node-search-empty"
                >
                    No nodes found
                </div>
            )}
        </div>
    );
});

NodeSearch.displayName = 'NodeSearch';

NodeSearch.propTypes = {
    /** Whether the search panel is open */
    isOpen: PropTypes.bool,
    /** Callback when the panel should close */
    onClose: PropTypes.func,
    /** Placeholder text for the search input */
    placeholder: PropTypes.string,
    /** Additional CSS class name */
    className: PropTypes.string,
    /** Custom inline styles */
    style: PropTypes.object,
    /** Keys to search in node data (default: ['id', 'label', 'type']) */
    searchKeys: PropTypes.arrayOf(PropTypes.string),
    /** Whether to focus on the selected node */
    focusOnSelect: PropTypes.bool,
    /** Whether to highlight the selected node */
    highlightOnSelect: PropTypes.bool,
    /** Duration of highlight effect in ms */
    highlightDuration: PropTypes.number,
    /** Zoom level when focusing on a node */
    zoomLevel: PropTypes.number,
};

NodeSearch.defaultProps = {
    isOpen: false,
    placeholder: 'Search nodes...',
    searchKeys: ['id', 'label', 'type', 'title', 'name'],
    focusOnSelect: true,
    highlightOnSelect: true,
    highlightDuration: 2000,
    zoomLevel: 1.5,
};

export default NodeSearch;