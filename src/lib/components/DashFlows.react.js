// DashFlows.react.js
import React, { useCallback, useEffect, useMemo, useRef } from 'react';
import PropTypes from 'prop-types';
import {
    ReactFlow,
    Controls,
    MiniMap,
    Background,
    ReactFlowProvider,
    useNodesState,
    useEdgesState,
    useReactFlow,
    useOnSelectionChange,
    MarkerType,
    ConnectionMode,
    SelectionMode,
    ConnectionLineType,
    Panel,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import '../styles/glass-theme.css';
import ELK from 'elkjs/lib/elk.bundled.js';
import { toPng, toSvg, toJpeg } from 'html-to-image';

// Import custom node types
import ResizableNode from './ResizableNode';
import AnimatedCircleNode from './AnimatedCircleNode';
import DevTools from './DevTools';

// Import custom edge types
import AnimatedNodeEdge from './AnimatedNodeEdge';

// Import built-in node types
import DefaultNode from './nodes/DefaultNode';
import InputNode from './nodes/InputNode';
import OutputNode from './nodes/OutputNode';
import GroupNode from './nodes/GroupNode';
import ToolbarNode from './nodes/ToolbarNode';

// Import built-in edge types
import StraightEdge from './edges/StraightEdge';
import StepEdge from './edges/StepEdge';
import SmoothStepEdge from './edges/SmoothStepEdge';
import SimpleBezierEdge from './edges/SimpleBezierEdge';
import ButtonEdge from './edges/ButtonEdge';
import DataEdge from './edges/DataEdge';
import AnimatedSvgEdge from './edges/AnimatedSvgEdge';

// Initialize ELK
const elk = new ELK();

// Node types definition - includes both custom and standard types
const nodeTypes = {
    // Custom types
    resizable: ResizableNode,
    circle: AnimatedCircleNode,
    toolbar: ToolbarNode,
    // Standard React Flow types
    default: DefaultNode,
    input: InputNode,
    output: OutputNode,
    group: GroupNode,
};

// Edge types definition - includes both custom and standard types
const edgeTypes = {
    // Custom types
    animated: AnimatedNodeEdge,
    button: ButtonEdge,
    data: DataEdge,
    animatedSvg: AnimatedSvgEdge,
    // Standard React Flow types (custom implementations for Dash compatibility)
    straight: StraightEdge,
    step: StepEdge,
    smoothstep: SmoothStepEdge,
    simplebezier: SimpleBezierEdge,
};

// Helper to convert string position to ConnectionLineType
const getConnectionLineType = (type) => {
    const types = {
        'bezier': ConnectionLineType.Bezier,
        'straight': ConnectionLineType.Straight,
        'step': ConnectionLineType.Step,
        'smoothstep': ConnectionLineType.SmoothStep,
        'simplebezier': ConnectionLineType.SimpleBezier,
    };
    return types[type?.toLowerCase()] || ConnectionLineType.Bezier;
};

// Helper to convert string to SelectionMode
const getSelectionMode = (mode) => {
    const modes = {
        'full': SelectionMode.Full,
        'partial': SelectionMode.Partial,
    };
    return modes[mode?.toLowerCase()] || SelectionMode.Full;
};

// Helper to convert string to ConnectionMode
const getConnectionMode = (mode) => {
    const modes = {
        'strict': ConnectionMode.Strict,
        'loose': ConnectionMode.Loose,
    };
    return modes[mode?.toLowerCase()] || ConnectionMode.Strict;
};

// Process Dash components - compatible with both Dash 2.x and Dash 3.x
const processDashComponents = (nodes) => {
    if (!nodes) return [];

    const processComponent = (component) => {
        if (!component || typeof component === 'string') return component;

        // Dash 3.0+ uses dash_component_api with componentPath
        if (component.props?.componentPath && window.dash_component_api) {
            const layout = window.dash_component_api.getLayout(component.props.componentPath);
            if (layout) {
                return {
                    props: {
                        ...component.props,
                        componentPath: component.props.componentPath
                    }
                };
            }
        }

        // Dash 2.x - If it's a Dash component with _dashprivate_layout
        if (component.props && component.props._dashprivate_layout) {
            const layout = component.props._dashprivate_layout;
            const processedChildren = Array.isArray(layout.props.children)
                ? layout.props.children.map(processComponent)
                : layout.props.children ? processComponent(layout.props.children) : null;
            return {
                props: {
                    _dashprivate_layout: {
                        ...layout,
                        props: {
                            ...layout.props,
                            children: processedChildren
                        }
                    }
                }
            };
        }

        // If it's a regular React component
        if (component.type && component.props) {
            const processedChildren = Array.isArray(component.props.children)
                ? component.props.children.map(processComponent)
                : component.props.children ? processComponent(component.props.children) : null;
            return {
                type: component.type,
                props: {
                    ...component.props,
                    children: processedChildren
                }
            };
        }

        return component;
    };

    return nodes.map(node => {
        if (!node.data?.label || typeof node.data.label === 'string') {
            return node;
        }

        return {
            ...node,
            data: {
                ...node.data,
                label: processComponent(node.data.label)
            }
        };
    });
};

const FlowWithProvider = (props) => {
    const [nodes, setNodes, onNodesChange] = useNodesState(props.nodes || []);
    const [edges, setEdges, onEdgesChange] = useEdgesState(props.edges || []);
    const reactFlowInstance = useReactFlow();
    const reactFlowWrapper = useRef(null);

    // Track initialization
    const initialized = useRef(false);

    // Apply ELK layout
    const applyLayout = async (options) => {
        if (!options) return;

        try {
            const layoutOptions = JSON.parse(options);
            const graph = {
                id: 'root',
                layoutOptions: layoutOptions,
                children: nodes.map(node => {
                    const isCircleNode = node.type === 'circle' || edges.some(edge =>
                        edge.type === 'animated' && edge.data?.animatedNode === node.id
                    );

                    if (isCircleNode) {
                        return {
                            id: node.id,
                            width: 60,
                            height: 60,
                            ...node,
                        };
                    }

                    return {
                        id: node.id,
                        width: node.style?.width || node.width || 150,
                        height: node.style?.height || node.height || 50,
                        ...node
                    };
                }),
                edges: edges.map(edge => ({
                    id: edge.id,
                    sources: [edge.source],
                    targets: [edge.target],
                    ...edge
                }))
            };

            const layout = await elk.layout(graph);

            const layoutedNodes = layout.children.map((node) => {
                const originalNode = nodes.find(n => n.id === node.id);
                return {
                    ...originalNode,
                    ...node,
                    position: { x: node.x, y: node.y },
                    style: originalNode?.style,
                };
            });

            setNodes(layoutedNodes);
            props.setProps({ nodes: layoutedNodes });
        } catch (error) {
            console.error('Layout error:', error);
            if (props.onError) {
                props.setProps({ lastError: { message: error.message, type: 'layout' } });
            }
        }
    };

    // Handle layout options changes
    useEffect(() => {
        if (props.layoutOptions) {
            applyLayout(props.layoutOptions);
        }
    }, [props.layoutOptions]);

    // Sync nodes with props
    useEffect(() => {
        if (props.nodes && JSON.stringify(props.nodes) !== JSON.stringify(nodes)) {
            setNodes(props.nodes);
        }
    }, [props.nodes]);

    // Sync edges with props
    useEffect(() => {
        if (props.edges && JSON.stringify(props.edges) !== JSON.stringify(edges)) {
            setEdges(props.edges);
        }
    }, [props.edges]);

    // Update props when nodes change
    useEffect(() => {
        if (nodes && nodes.length > 0) {
            props.setProps({ nodes });
        }
    }, [nodes]);

    // Update props when edges change
    useEffect(() => {
        if (edges) {
            props.setProps({ edges });
        }
    }, [edges]);

    // Export flow state when requested
    useEffect(() => {
        if (props.exportFlowState) {
            const viewport = reactFlowInstance.getViewport();
            const flowState = {
                nodes: nodes.map(node => ({
                    id: node.id,
                    type: node.type,
                    position: node.position,
                    data: node.data,
                    style: node.style,
                    width: node.width,
                    height: node.height,
                    parentId: node.parentId,
                    zIndex: node.zIndex,
                    extent: node.extent,
                    expandParent: node.expandParent,
                    draggable: node.draggable,
                    selectable: node.selectable,
                    connectable: node.connectable,
                    deletable: node.deletable,
                    selected: node.selected,
                })),
                edges: edges.map(edge => ({
                    id: edge.id,
                    type: edge.type,
                    source: edge.source,
                    target: edge.target,
                    sourceHandle: edge.sourceHandle,
                    targetHandle: edge.targetHandle,
                    data: edge.data,
                    style: edge.style,
                    animated: edge.animated,
                    label: typeof edge.label === 'string' ? edge.label : undefined,
                    markerStart: edge.markerStart,
                    markerEnd: edge.markerEnd,
                    selected: edge.selected,
                })),
                viewport: viewport,
            };
            props.setProps({
                flowState: flowState,
                exportFlowState: false,  // Reset trigger
            });
        }
    }, [props.exportFlowState, nodes, edges, reactFlowInstance]);

    // Import/restore flow state
    useEffect(() => {
        if (props.restoreFlowState && props.restoreFlowState.nodes) {
            const state = props.restoreFlowState;
            setNodes(state.nodes || []);
            setEdges(state.edges || []);
            if (state.viewport) {
                reactFlowInstance.setViewport(state.viewport);
            }
            props.setProps({
                nodes: state.nodes,
                edges: state.edges,
                restoreFlowState: null,  // Reset trigger
            });
        }
    }, [props.restoreFlowState, setNodes, setEdges, reactFlowInstance]);

    // Handle viewport actions
    useEffect(() => {
        if (props.viewportAction && reactFlowInstance) {
            const action = props.viewportAction;
            switch (action.action) {
                case 'fitView':
                    reactFlowInstance.fitView(action.options || {});
                    break;
                case 'zoomIn':
                    reactFlowInstance.zoomIn(action.options || {});
                    break;
                case 'zoomOut':
                    reactFlowInstance.zoomOut(action.options || {});
                    break;
                case 'setZoom':
                    if (action.zoom !== undefined) {
                        reactFlowInstance.setZoom(action.zoom, action.options || {});
                    }
                    break;
                case 'setCenter':
                    if (action.x !== undefined && action.y !== undefined) {
                        reactFlowInstance.setCenter(action.x, action.y, action.options || {});
                    }
                    break;
                case 'setViewport':
                    if (action.viewport) {
                        reactFlowInstance.setViewport(action.viewport, action.options || {});
                    }
                    break;
                case 'focusNode':
                    if (action.nodeId) {
                        const node = nodes.find(n => n.id === action.nodeId);
                        if (node) {
                            reactFlowInstance.setCenter(
                                node.position.x + (node.width || 150) / 2,
                                node.position.y + (node.height || 50) / 2,
                                { zoom: action.zoom || 1.5, duration: action.duration || 500 }
                            );
                        }
                    }
                    break;
                default:
                    break;
            }
            // Reset the action after execution
            props.setProps({ viewportAction: null });
        }
    }, [props.viewportAction, reactFlowInstance, nodes]);

    // Handle download image
    useEffect(() => {
        if (props.downloadImage && reactFlowWrapper.current) {
            const config = props.downloadImage;
            const format = config.format || 'png';
            const filename = config.filename || 'flow';
            const quality = config.quality || 0.95;
            const backgroundColor = config.backgroundColor || '#ffffff';

            // Find the ReactFlow viewport element
            const viewport = reactFlowWrapper.current.querySelector('.react-flow__viewport');
            if (!viewport) {
                props.setProps({ downloadImage: null });
                return;
            }

            // Get the image based on format
            const getImage = async () => {
                const options = {
                    backgroundColor: backgroundColor,
                    quality: quality,
                    pixelRatio: config.pixelRatio || 2,
                };

                try {
                    let dataUrl;
                    if (format === 'svg') {
                        dataUrl = await toSvg(viewport, options);
                    } else if (format === 'jpeg' || format === 'jpg') {
                        dataUrl = await toJpeg(viewport, options);
                    } else {
                        dataUrl = await toPng(viewport, options);
                    }

                    // Create download link
                    const link = document.createElement('a');
                    link.download = `${filename}.${format === 'jpeg' ? 'jpg' : format}`;
                    link.href = dataUrl;
                    link.click();

                    // Report success
                    props.setProps({
                        downloadImage: null,
                        imageDownloaded: {
                            filename: link.download,
                            format: format,
                            timestamp: Date.now(),
                        },
                    });
                } catch (error) {
                    props.setProps({
                        downloadImage: null,
                        lastError: {
                            id: 'download-image',
                            message: error.message,
                            type: 'image-export',
                            timestamp: Date.now(),
                        },
                    });
                }
            };

            getImage();
        }
    }, [props.downloadImage]);

    // Handle copy action
    useEffect(() => {
        if (props.copyAction) {
            // Get selected nodes and edges
            const selectedNodeIds = nodes.filter(n => n.selected).map(n => n.id);
            const selectedEdgeIds = edges.filter(e => e.selected).map(e => e.id);

            // If nothing selected, copy all
            const nodesToCopy = selectedNodeIds.length > 0
                ? nodes.filter(n => selectedNodeIds.includes(n.id))
                : nodes;

            // Copy edges that connect the copied nodes
            const nodeIdSet = new Set(nodesToCopy.map(n => n.id));
            const edgesToCopy = edges.filter(e =>
                (selectedEdgeIds.includes(e.id)) ||
                (nodeIdSet.has(e.source) && nodeIdSet.has(e.target))
            );

            props.setProps({
                clipboard: {
                    nodes: nodesToCopy.map(n => ({
                        ...n,
                        // Remove selection state
                        selected: false,
                    })),
                    edges: edgesToCopy.map(e => ({
                        ...e,
                        selected: false,
                    })),
                    timestamp: Date.now(),
                },
                copyAction: false,  // Reset trigger
            });
        }
    }, [props.copyAction, nodes, edges]);

    // Handle paste action
    useEffect(() => {
        if (props.pasteAction && props.clipboard) {
            const clipboard = props.clipboard;
            const offset = props.pasteAction.offset || { x: 50, y: 50 };

            // Generate new IDs for pasted nodes
            const idMap = {};
            const timestamp = Date.now();

            const newNodes = clipboard.nodes.map((node, index) => {
                const newId = `${node.id}-paste-${timestamp}-${index}`;
                idMap[node.id] = newId;
                return {
                    ...node,
                    id: newId,
                    position: {
                        x: node.position.x + offset.x,
                        y: node.position.y + offset.y,
                    },
                    selected: true,  // Select pasted nodes
                };
            });

            // Update edge references to new node IDs
            const newEdges = clipboard.edges.map((edge, index) => {
                const newSource = idMap[edge.source] || edge.source;
                const newTarget = idMap[edge.target] || edge.target;

                // Only include edge if both nodes exist
                if (!idMap[edge.source] || !idMap[edge.target]) {
                    return null;
                }

                return {
                    ...edge,
                    id: `${edge.id}-paste-${timestamp}-${index}`,
                    source: newSource,
                    target: newTarget,
                    selected: false,
                };
            }).filter(Boolean);

            // Deselect existing nodes
            const updatedNodes = nodes.map(n => ({ ...n, selected: false }));

            // Add pasted nodes and edges
            setNodes([...updatedNodes, ...newNodes]);
            setEdges([...edges, ...newEdges]);

            props.setProps({
                nodes: [...updatedNodes, ...newNodes],
                edges: [...edges, ...newEdges],
                pasteAction: null,  // Reset trigger
                pastedElements: {
                    nodeIds: newNodes.map(n => n.id),
                    edgeIds: newEdges.map(e => e.id),
                    timestamp: Date.now(),
                },
            });
        }
    }, [props.pasteAction, props.clipboard, nodes, edges, setNodes, setEdges]);

    // Selection change handler
    useOnSelectionChange({
        onChange: useCallback(({ nodes: selectedNodes, edges: selectedEdges }) => {
            props.setProps({
                selectedNodes: selectedNodes.map(n => n.id),
                selectedEdges: selectedEdges.map(e => e.id),
            });
        }, []),
    });

    // Connection handler
    const onConnect = useCallback((params) => {
        const newEdge = {
            ...params,
            id: `e${params.source}-${params.target}-${Date.now()}`,
            type: props.defaultEdgeOptions?.type || 'default',
            style: props.defaultEdgeOptions?.style || { strokeWidth: 2, stroke: '#555' },
            markerEnd: props.defaultEdgeOptions?.markerEnd || {
                type: MarkerType.ArrowClosed,
                color: '#555',
                width: 20,
                height: 20,
            },
            ...props.defaultEdgeOptions,
        };
        setEdges((eds) => [...eds, newEdge]);
        props.setProps({
            edges: [...edges, newEdge],
            lastConnection: params,
        });
    }, [edges, setEdges, props.defaultEdgeOptions]);

    // Connection start handler
    const onConnectStart = useCallback((event, params) => {
        props.setProps({
            connectionStartHandle: {
                nodeId: params.nodeId,
                handleId: params.handleId,
                handleType: params.handleType,
            }
        });
    }, []);

    // Connection end handler
    const onConnectEnd = useCallback((event) => {
        props.setProps({
            connectionStartHandle: null,
        });
    }, []);

    // Node click handler
    const onNodeClick = useCallback((event, node) => {
        props.setProps({
            clickedNode: { id: node.id, data: node.data, position: node.position },
        });
    }, []);

    // Node double click handler
    const onNodeDoubleClick = useCallback((event, node) => {
        props.setProps({
            doubleClickedNode: { id: node.id, data: node.data, position: node.position },
        });
    }, []);

    // Node context menu handler
    const onNodeContextMenu = useCallback((event, node) => {
        event.preventDefault();
        props.setProps({
            contextMenuNode: {
                id: node.id,
                data: node.data,
                position: node.position,
                clientX: event.clientX,
                clientY: event.clientY,
            },
        });
    }, []);

    // Node drag handlers
    const onNodeDragStart = useCallback((event, node) => {
        props.setProps({
            draggedNode: { id: node.id, isDragging: true, startPosition: node.position },
        });
    }, []);

    const onNodeDrag = useCallback((event, node) => {
        // Only update if we want real-time position updates (can be expensive)
        if (props.trackNodeDrag) {
            props.setProps({
                draggedNode: { id: node.id, isDragging: true, currentPosition: node.position },
            });
        }
    }, [props.trackNodeDrag]);

    const onNodeDragStop = useCallback((event, node) => {
        props.setProps({
            draggedNode: { id: node.id, isDragging: false, endPosition: node.position },
        });
    }, []);

    // Node mouse handlers
    const onNodeMouseEnter = useCallback((event, node) => {
        props.setProps({
            hoveredNode: { id: node.id, data: node.data },
        });
    }, []);

    const onNodeMouseLeave = useCallback((event, node) => {
        props.setProps({
            hoveredNode: null,
        });
    }, []);

    // Edge click handler
    const onEdgeClick = useCallback((event, edge) => {
        props.setProps({
            clickedEdge: { id: edge.id, source: edge.source, target: edge.target },
        });
    }, []);

    // Edge double click handler
    const onEdgeDoubleClick = useCallback((event, edge) => {
        props.setProps({
            doubleClickedEdge: { id: edge.id, source: edge.source, target: edge.target },
        });
    }, []);

    // Edge context menu handler
    const onEdgeContextMenu = useCallback((event, edge) => {
        event.preventDefault();
        props.setProps({
            contextMenuEdge: {
                id: edge.id,
                source: edge.source,
                target: edge.target,
                clientX: event.clientX,
                clientY: event.clientY,
            },
        });
    }, []);

    // Edge mouse handlers
    const onEdgeMouseEnter = useCallback((event, edge) => {
        props.setProps({
            hoveredEdge: { id: edge.id, source: edge.source, target: edge.target },
        });
    }, []);

    const onEdgeMouseLeave = useCallback((event, edge) => {
        props.setProps({
            hoveredEdge: null,
        });
    }, []);

    // Pane click handler
    const onPaneClick = useCallback((event) => {
        props.setProps({
            paneClickPosition: {
                clientX: event.clientX,
                clientY: event.clientY,
            },
            // Clear context menus on pane click
            contextMenuNode: null,
            contextMenuEdge: null,
        });
    }, []);

    // Pane context menu handler
    const onPaneContextMenu = useCallback((event) => {
        event.preventDefault();
        props.setProps({
            paneContextMenu: {
                clientX: event.clientX,
                clientY: event.clientY,
            },
        });
    }, []);

    // Drag and Drop handlers for adding nodes from external sources
    const onDragOver = useCallback((event) => {
        event.preventDefault();
        event.dataTransfer.dropEffect = 'move';
    }, []);

    const onDrop = useCallback((event) => {
        event.preventDefault();

        // Get the drop position in flow coordinates
        const reactFlowBounds = reactFlowWrapper.current?.getBoundingClientRect();
        if (!reactFlowBounds) return;

        // Try to get the transferred data
        let nodeType = 'default';
        let nodeData = {};

        try {
            const dataString = event.dataTransfer.getData('application/reactflow');
            if (dataString) {
                const parsedData = JSON.parse(dataString);
                nodeType = parsedData.type || 'default';
                nodeData = parsedData.data || {};
            }
        } catch (e) {
            // If parsing fails, try plain text
            const textData = event.dataTransfer.getData('text/plain');
            if (textData) {
                try {
                    const parsedData = JSON.parse(textData);
                    nodeType = parsedData.type || 'default';
                    nodeData = parsedData.data || {};
                } catch (e2) {
                    // Use text as label
                    nodeData = { label: textData };
                }
            }
        }

        // Convert screen coordinates to flow coordinates
        const position = reactFlowInstance.screenToFlowPosition({
            x: event.clientX - reactFlowBounds.left,
            y: event.clientY - reactFlowBounds.top,
        });

        // Report the drop event to Dash
        props.setProps({
            droppedNode: {
                type: nodeType,
                position: position,
                data: nodeData,
                clientX: event.clientX,
                clientY: event.clientY,
                timestamp: Date.now(),
            },
        });
    }, [reactFlowInstance]);

    // Viewport change handlers
    const onMoveStart = useCallback((event, viewport) => {
        props.setProps({
            viewportMoving: true,
        });
    }, []);

    const onMove = useCallback((event, viewport) => {
        if (props.trackViewport) {
            props.setProps({
                viewport: { x: viewport.x, y: viewport.y, zoom: viewport.zoom },
            });
        }
    }, [props.trackViewport]);

    const onMoveEnd = useCallback((event, viewport) => {
        props.setProps({
            viewport: { x: viewport.x, y: viewport.y, zoom: viewport.zoom },
            viewportMoving: false,
        });
    }, []);

    // Delete handler
    const onNodesDelete = useCallback((deletedNodes) => {
        props.setProps({
            deletedNodes: deletedNodes.map(n => n.id),
        });
    }, []);

    const onEdgesDelete = useCallback((deletedEdges) => {
        props.setProps({
            deletedEdges: deletedEdges.map(e => e.id),
        });
    }, []);

    // Before delete handler (for validation)
    const onBeforeDelete = useCallback(async ({ nodes: nodesToDelete, edges: edgesToDelete }) => {
        if (props.preventDelete) {
            // If preventDelete is set, check the lists
            const preventNodeIds = props.preventDeleteNodes || [];
            const preventEdgeIds = props.preventDeleteEdges || [];

            const allowedNodes = nodesToDelete.filter(n => !preventNodeIds.includes(n.id));
            const allowedEdges = edgesToDelete.filter(e => !preventEdgeIds.includes(e.id));

            return {
                nodes: allowedNodes,
                edges: allowedEdges,
            };
        }
        return { nodes: nodesToDelete, edges: edgesToDelete };
    }, [props.preventDelete, props.preventDeleteNodes, props.preventDeleteEdges]);

    // Init handler
    const onInit = useCallback((instance) => {
        if (!initialized.current) {
            initialized.current = true;
            props.setProps({
                initialized: true,
            });

            // Apply fitView if requested
            if (props.fitView) {
                instance.fitView(props.fitViewOptions || {});
            }
        }
    }, [props.fitView, props.fitViewOptions]);

    // Error handler
    const onError = useCallback((id, message) => {
        console.error('React Flow Error:', id, message);
        props.setProps({
            lastError: { id, message, timestamp: Date.now() },
        });
    }, []);

    // Helper to count connections for a node/handle
    const countConnections = useCallback((nodeId, handleId, handleType) => {
        return edges.filter(edge => {
            if (handleType === 'source') {
                return edge.source === nodeId && (!handleId || edge.sourceHandle === handleId);
            } else {
                return edge.target === nodeId && (!handleId || edge.targetHandle === handleId);
            }
        }).length;
    }, [edges]);

    // Connection validation
    const isValidConnection = useCallback((connection) => {
        // If custom validation rules are provided
        if (props.connectionRules) {
            const rules = props.connectionRules;

            // Check if self-connections are allowed
            if (!rules.allowSelfConnection && connection.source === connection.target) {
                return false;
            }

            // Check if duplicate connections are allowed
            if (!rules.allowDuplicateConnections) {
                const isDuplicate = edges.some(
                    e => e.source === connection.source &&
                        e.target === connection.target &&
                        e.sourceHandle === connection.sourceHandle &&
                        e.targetHandle === connection.targetHandle
                );
                if (isDuplicate) return false;
            }

            // Check source handle types if specified
            if (rules.validSourceTypes && rules.validSourceTypes.length > 0) {
                const sourceNode = nodes.find(n => n.id === connection.source);
                if (sourceNode && !rules.validSourceTypes.includes(sourceNode.type)) {
                    return false;
                }
            }

            // Check target handle types if specified
            if (rules.validTargetTypes && rules.validTargetTypes.length > 0) {
                const targetNode = nodes.find(n => n.id === connection.target);
                if (targetNode && !rules.validTargetTypes.includes(targetNode.type)) {
                    return false;
                }
            }
        }

        // Check connection limits
        const sourceNode = nodes.find(n => n.id === connection.source);
        const targetNode = nodes.find(n => n.id === connection.target);

        // Check source node connection limit
        if (sourceNode?.data?.maxConnections !== undefined) {
            const currentSourceConnections = countConnections(connection.source, null, 'source');
            if (currentSourceConnections >= sourceNode.data.maxConnections) {
                return false;
            }
        }

        // Check source handle connection limit
        if (sourceNode?.data?.maxSourceConnections !== undefined) {
            const currentHandleConnections = countConnections(
                connection.source,
                connection.sourceHandle,
                'source'
            );
            if (currentHandleConnections >= sourceNode.data.maxSourceConnections) {
                return false;
            }
        }

        // Check target node connection limit
        if (targetNode?.data?.maxConnections !== undefined) {
            const currentTargetConnections = countConnections(connection.target, null, 'target');
            if (currentTargetConnections >= targetNode.data.maxConnections) {
                return false;
            }
        }

        // Check target handle connection limit
        if (targetNode?.data?.maxTargetConnections !== undefined) {
            const currentHandleConnections = countConnections(
                connection.target,
                connection.targetHandle,
                'target'
            );
            if (currentHandleConnections >= targetNode.data.maxTargetConnections) {
                return false;
            }
        }

        return true;
    }, [edges, nodes, props.connectionRules, countConnections]);

    // Process nodes for Dash component compatibility
    const processedNodes = useMemo(() => processDashComponents(nodes), [nodes]);

    // Build default edge options
    const defaultEdgeOptions = useMemo(() => ({
        type: 'default',
        style: { strokeWidth: 2, stroke: '#555' },
        markerEnd: {
            type: MarkerType.ArrowClosed,
            color: props.defaultMarkerColor || '#555',
        },
        ...props.defaultEdgeOptions,
    }), [props.defaultEdgeOptions, props.defaultMarkerColor]);

    // Build fitView options
    const fitViewOptions = useMemo(() => ({
        padding: 0.1,
        ...props.fitViewOptions,
    }), [props.fitViewOptions]);

    return (
        <div
            ref={reactFlowWrapper}
            style={{ width: '100%', height: props.style?.height || '600px', ...props.style }}
            className={props.className}
            onDragOver={onDragOver}
            onDrop={onDrop}
        >
            <ReactFlow
                // Core props
                nodes={processedNodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                nodeTypes={nodeTypes}
                edgeTypes={edgeTypes}

                // Viewport props
                defaultViewport={props.defaultViewport}
                minZoom={props.minZoom}
                maxZoom={props.maxZoom}
                snapToGrid={props.snapToGrid}
                snapGrid={props.snapGrid}
                translateExtent={props.translateExtent}
                nodeExtent={props.nodeExtent}
                onlyRenderVisibleElements={props.onlyRenderVisibleElements}
                preventScrolling={props.preventScrolling}

                // Interaction props
                nodesDraggable={props.nodesDraggable}
                nodesConnectable={props.nodesConnectable}
                nodesFocusable={props.nodesFocusable}
                edgesFocusable={props.edgesFocusable}
                elementsSelectable={props.elementsSelectable}
                autoPanOnConnect={props.autoPanOnConnect}
                autoPanOnNodeDrag={props.autoPanOnNodeDrag}
                autoPanSpeed={props.autoPanSpeed}
                panOnDrag={props.panOnDrag}
                panOnScroll={props.panOnScroll}
                panOnScrollSpeed={props.panOnScrollSpeed}
                panOnScrollMode={props.panOnScrollMode}
                zoomOnScroll={props.zoomOnScroll}
                zoomOnPinch={props.zoomOnPinch}
                zoomOnDoubleClick={props.zoomOnDoubleClick}
                selectNodesOnDrag={props.selectNodesOnDrag}
                selectionOnDrag={props.selectionOnDrag}
                selectionMode={getSelectionMode(props.selectionMode)}
                connectOnClick={props.connectOnClick}
                connectionMode={getConnectionMode(props.connectionMode)}
                elevateNodesOnSelect={props.elevateNodesOnSelect}
                elevateEdgesOnSelect={props.elevateEdgesOnSelect}

                // Edge props
                defaultEdgeOptions={defaultEdgeOptions}
                edgesReconnectable={props.edgesReconnectable}
                reconnectRadius={props.reconnectRadius}

                // Connection line props
                connectionLineStyle={props.connectionLineStyle}
                connectionLineType={getConnectionLineType(props.connectionLineType)}
                connectionRadius={props.connectionRadius}

                // Keyboard props
                deleteKeyCode={props.deleteKeyCode}
                selectionKeyCode={props.selectionKeyCode}
                multiSelectionKeyCode={props.multiSelectionKeyCode}
                zoomActivationKeyCode={props.zoomActivationKeyCode}
                panActivationKeyCode={props.panActivationKeyCode}
                disableKeyboardA11y={props.disableKeyboardA11y}

                // Style props
                noPanClassName={props.noPanClassName}
                noDragClassName={props.noDragClassName}
                noWheelClassName={props.noWheelClassName}

                // Event handlers
                onInit={onInit}
                onError={onError}
                onConnect={onConnect}
                onConnectStart={onConnectStart}
                onConnectEnd={onConnectEnd}
                isValidConnection={isValidConnection}

                // Node events
                onNodeClick={onNodeClick}
                onNodeDoubleClick={onNodeDoubleClick}
                onNodeContextMenu={onNodeContextMenu}
                onNodeDragStart={onNodeDragStart}
                onNodeDrag={onNodeDrag}
                onNodeDragStop={onNodeDragStop}
                onNodeMouseEnter={onNodeMouseEnter}
                onNodeMouseLeave={onNodeMouseLeave}
                onNodesDelete={onNodesDelete}

                // Edge events
                onEdgeClick={onEdgeClick}
                onEdgeDoubleClick={onEdgeDoubleClick}
                onEdgeContextMenu={onEdgeContextMenu}
                onEdgeMouseEnter={onEdgeMouseEnter}
                onEdgeMouseLeave={onEdgeMouseLeave}
                onEdgesDelete={onEdgesDelete}

                // Pane events
                onPaneClick={onPaneClick}
                onPaneContextMenu={onPaneContextMenu}

                // Viewport events
                onMoveStart={onMoveStart}
                onMove={onMove}
                onMoveEnd={onMoveEnd}

                // Delete validation
                onBeforeDelete={onBeforeDelete}

                // Fit view
                fitView={props.fitView}
                fitViewOptions={fitViewOptions}

                // Color mode
                colorMode={props.colorMode}
            >
                {/* Controls */}
                {props.showControls && (
                    <Controls
                        showZoom={props.controlsShowZoom}
                        showFitView={props.controlsShowFitView}
                        showInteractive={props.controlsShowInteractive}
                        position={props.controlsPosition}
                    />
                )}

                {/* MiniMap */}
                {props.showMiniMap && (
                    <MiniMap
                        nodeColor={(node) => {
                            // Use custom color if provided, otherwise use type-based colors
                            if (props.miniMapNodeColor) return props.miniMapNodeColor;
                            switch(node.type) {
                                case 'input': return '#10b981';
                                case 'output': return '#8b5cf6';
                                case 'group': return '#6b7280';
                                case 'circle': return '#3b82f6';
                                case 'resizable': return '#f59e0b';
                                case 'toolbar': return '#06b6d4';
                                default: return '#64748b';
                            }
                        }}
                        nodeStrokeColor={(node) => {
                            if (props.miniMapNodeStrokeColor) return props.miniMapNodeStrokeColor;
                            switch(node.type) {
                                case 'input': return '#059669';
                                case 'output': return '#7c3aed';
                                case 'group': return '#4b5563';
                                default: return '#475569';
                            }
                        }}
                        nodeBorderRadius={props.miniMapNodeBorderRadius || 2}
                        maskColor={props.miniMapMaskColor || 'rgba(59, 130, 246, 0.2)'}
                        position={props.miniMapPosition}
                        pannable={props.miniMapPannable}
                        zoomable={props.miniMapZoomable}
                        style={{
                            backgroundColor: props.colorMode === 'dark' ? 'rgba(26, 27, 30, 0.9)' : 'rgba(255, 255, 255, 0.9)',
                        }}
                    />
                )}

                {/* Background */}
                {props.showBackground && (
                    <Background
                        variant={props.backgroundVariant}
                        gap={props.backgroundGap}
                        size={props.backgroundSize}
                        color={props.backgroundColor}
                    />
                )}

                {/* Custom Panels */}
                {props.panels && props.panels.map((panel, index) => (
                    <Panel key={index} position={panel.position || 'top-left'}>
                        {panel.children}
                    </Panel>
                ))}

                {/* DevTools */}
                {props.showDevTools && <DevTools nodes={processedNodes} />}
            </ReactFlow>
        </div>
    );
};

// Helper to build CSS variables from theme object
const buildThemeStyles = (theme) => {
    if (!theme) return {};

    const cssVars = {};

    // Glass effect properties
    if (theme.glassBlur !== undefined) cssVars['--df-glass-blur'] = `${theme.glassBlur}px`;
    if (theme.glassSaturate !== undefined) cssVars['--df-glass-saturate'] = `${theme.glassSaturate}%`;

    // Node colors
    if (theme.nodeBackground) cssVars['--df-node-bg'] = theme.nodeBackground;
    if (theme.nodeBorder) cssVars['--df-node-border'] = theme.nodeBorder;
    if (theme.nodeText) cssVars['--df-node-text'] = theme.nodeText;
    if (theme.nodeTextSecondary) cssVars['--df-node-text-secondary'] = theme.nodeTextSecondary;

    // Input node colors
    if (theme.inputNodeBackground) cssVars['--df-input-node-bg'] = theme.inputNodeBackground;
    if (theme.inputNodeBorder) cssVars['--df-input-node-border'] = theme.inputNodeBorder;
    if (theme.inputNodeAccent) cssVars['--df-input-node-accent'] = theme.inputNodeAccent;

    // Output node colors
    if (theme.outputNodeBackground) cssVars['--df-output-node-bg'] = theme.outputNodeBackground;
    if (theme.outputNodeBorder) cssVars['--df-output-node-border'] = theme.outputNodeBorder;
    if (theme.outputNodeAccent) cssVars['--df-output-node-accent'] = theme.outputNodeAccent;

    // Edge colors
    if (theme.edgeStroke) cssVars['--df-edge-stroke'] = theme.edgeStroke;
    if (theme.edgeStrokeSelected) cssVars['--df-edge-stroke-selected'] = theme.edgeStrokeSelected;
    if (theme.edgeStrokeAnimated) cssVars['--df-edge-stroke-animated'] = theme.edgeStrokeAnimated;
    if (theme.edgeStrokeWidth !== undefined) cssVars['--df-edge-stroke-width'] = theme.edgeStrokeWidth;

    // Handle colors
    if (theme.handleBackground) cssVars['--df-handle-bg'] = theme.handleBackground;
    if (theme.handleBorder) cssVars['--df-handle-border'] = theme.handleBorder;
    if (theme.handleConnected) cssVars['--df-handle-bg-connected'] = theme.handleConnected;

    // Background
    if (theme.backgroundColor) cssVars['--df-background-color'] = theme.backgroundColor;
    if (theme.backgroundPattern) cssVars['--df-background-pattern'] = theme.backgroundPattern;

    // Selection
    if (theme.selectionBackground) cssVars['--df-selection-bg'] = theme.selectionBackground;
    if (theme.selectionBorder) cssVars['--df-selection-border'] = theme.selectionBorder;

    // Border radius
    if (theme.borderRadius !== undefined) cssVars['--df-radius-lg'] = `${theme.borderRadius}px`;

    return cssVars;
};

// Get theme preset class name
const getThemePresetClass = (preset) => {
    const presets = {
        'glass': 'df-theme-glass',
        'solid': 'df-theme-solid',
        'minimal': 'df-theme-minimal',
    };
    return presets[preset] || '';
};

// Get color scheme class name
const getColorSchemeClass = (scheme) => {
    const schemes = {
        'default': 'df-scheme-default',
        'ocean': 'df-scheme-ocean',
        'forest': 'df-scheme-forest',
        'sunset': 'df-scheme-sunset',
        'midnight': 'df-scheme-midnight',
        'rose': 'df-scheme-rose',
    };
    return schemes[scheme] || '';
};

/**
 * DashFlows - A React Flow-based node graph component for Dash applications.
 * Provides interactive node-based workflow visualization with support for
 * custom node types, edge types, glass morphism styling, and extensive
 * callback integration for Python-based interactivity.
 */
const DashFlows = ({
    // Interaction defaults
    nodesDraggable = true,
    nodesConnectable = true,
    nodesFocusable = true,
    edgesFocusable = true,
    elementsSelectable = true,
    autoPanOnConnect = true,
    autoPanOnNodeDrag = true,
    autoPanSpeed = 15,
    panOnDrag = true,
    panOnScroll = false,
    panOnScrollSpeed = 0.5,
    panOnScrollMode = 'free',
    zoomOnScroll = true,
    zoomOnPinch = true,
    zoomOnDoubleClick = true,
    selectNodesOnDrag = true,
    selectionOnDrag = false,
    selectionMode = 'full',
    connectOnClick = true,
    connectionMode = 'strict',
    elevateNodesOnSelect = true,
    elevateEdgesOnSelect = false,

    // Viewport defaults
    minZoom = 0.5,
    maxZoom = 2,
    snapToGrid = false,
    snapGrid = [15, 15],
    preventScrolling = true,
    onlyRenderVisibleElements = false,
    fitView = false,

    // Edge defaults
    edgesReconnectable = true,
    reconnectRadius = 10,
    defaultMarkerColor = '#555',

    // Connection line defaults
    connectionLineType = 'bezier',
    connectionRadius = 20,

    // Keyboard defaults
    deleteKeyCode = 'Backspace',
    selectionKeyCode = 'Shift',
    panActivationKeyCode = 'Space',
    disableKeyboardA11y = false,

    // Style defaults
    noPanClassName = 'nopan',
    noDragClassName = 'nodrag',
    noWheelClassName = 'nowheel',

    // Display defaults
    showMiniMap = true,
    showControls = true,
    showBackground = true,
    showDevTools = false,

    // Controls defaults
    controlsShowZoom = true,
    controlsShowFitView = true,
    controlsShowInteractive = true,
    controlsPosition = 'bottom-left',

    // MiniMap defaults
    miniMapPannable = false,
    miniMapZoomable = false,
    miniMapPosition = 'bottom-right',

    // Background defaults
    backgroundVariant = 'dots',
    backgroundGap = 16,
    backgroundSize = 1,

    // Tracking defaults
    trackNodeDrag = false,
    trackViewport = false,

    // Delete prevention defaults
    preventDelete = false,

    // Color mode
    colorMode = 'light',

    // Data defaults
    nodes = [],
    edges = [],
    style = {},
    className = '',

    // Other props passed through
    ...restProps
}) => {
    // Reconstruct props object for passing to children
    const props = {
        nodesDraggable,
        nodesConnectable,
        nodesFocusable,
        edgesFocusable,
        elementsSelectable,
        autoPanOnConnect,
        autoPanOnNodeDrag,
        autoPanSpeed,
        panOnDrag,
        panOnScroll,
        panOnScrollSpeed,
        panOnScrollMode,
        zoomOnScroll,
        zoomOnPinch,
        zoomOnDoubleClick,
        selectNodesOnDrag,
        selectionOnDrag,
        selectionMode,
        connectOnClick,
        connectionMode,
        elevateNodesOnSelect,
        elevateEdgesOnSelect,
        minZoom,
        maxZoom,
        snapToGrid,
        snapGrid,
        preventScrolling,
        onlyRenderVisibleElements,
        fitView,
        edgesReconnectable,
        reconnectRadius,
        defaultMarkerColor,
        connectionLineType,
        connectionRadius,
        deleteKeyCode,
        selectionKeyCode,
        panActivationKeyCode,
        disableKeyboardA11y,
        noPanClassName,
        noDragClassName,
        noWheelClassName,
        showMiniMap,
        showControls,
        showBackground,
        showDevTools,
        controlsShowZoom,
        controlsShowFitView,
        controlsShowInteractive,
        controlsPosition,
        miniMapPannable,
        miniMapZoomable,
        miniMapPosition,
        backgroundVariant,
        backgroundGap,
        backgroundSize,
        trackNodeDrag,
        trackViewport,
        preventDelete,
        colorMode,
        nodes,
        edges,
        style,
        className,
        ...restProps
    };

    const themeStyles = useMemo(() => buildThemeStyles(props.theme), [props.theme]);
    const themePresetClass = useMemo(() => getThemePresetClass(props.themePreset), [props.themePreset]);
    const colorSchemeClass = useMemo(() => getColorSchemeClass(props.colorScheme), [props.colorScheme]);

    const containerClassName = useMemo(() => {
        return [className, themePresetClass, colorSchemeClass].filter(Boolean).join(' ');
    }, [className, themePresetClass, colorSchemeClass]);

    return (
        <div id={props.id} style={themeStyles}>
            <ReactFlowProvider>
                <FlowWithProvider {...props} className={containerClassName} />
            </ReactFlowProvider>
        </div>
    );
};

DashFlows.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    // ===================
    // CORE DATA PROPS
    // ===================

    /**
     * Array of nodes to display in the flow
     */
    nodes: PropTypes.arrayOf(PropTypes.shape({
        id: PropTypes.string.isRequired,
        type: PropTypes.string,
        data: PropTypes.object.isRequired,
        position: PropTypes.shape({
            x: PropTypes.number.isRequired,
            y: PropTypes.number.isRequired
        }).isRequired,
        style: PropTypes.object,
        className: PropTypes.string,
        hidden: PropTypes.bool,
        selected: PropTypes.bool,
        draggable: PropTypes.bool,
        selectable: PropTypes.bool,
        connectable: PropTypes.bool,
        deletable: PropTypes.bool,
        dragHandle: PropTypes.string,
        width: PropTypes.number,
        height: PropTypes.number,
        parentId: PropTypes.string,
        zIndex: PropTypes.number,
        extent: PropTypes.oneOfType([
            PropTypes.string,
            PropTypes.arrayOf(PropTypes.arrayOf(PropTypes.number))
        ]),
        expandParent: PropTypes.bool,
        positionAbsolute: PropTypes.shape({
            x: PropTypes.number,
            y: PropTypes.number
        }),
        ariaLabel: PropTypes.string,
        focusable: PropTypes.bool,
        resizing: PropTypes.bool,
    })),

    /**
     * Array of edges defining connections between nodes
     */
    edges: PropTypes.arrayOf(PropTypes.shape({
        id: PropTypes.string.isRequired,
        source: PropTypes.string.isRequired,
        target: PropTypes.string.isRequired,
        sourceHandle: PropTypes.string,
        targetHandle: PropTypes.string,
        type: PropTypes.string,
        data: PropTypes.object,
        style: PropTypes.object,
        className: PropTypes.string,
        hidden: PropTypes.bool,
        selected: PropTypes.bool,
        animated: PropTypes.bool,
        deletable: PropTypes.bool,
        selectable: PropTypes.bool,
        focusable: PropTypes.bool,
        zIndex: PropTypes.number,
        ariaLabel: PropTypes.string,
        interactionWidth: PropTypes.number,
        label: PropTypes.string,
        labelStyle: PropTypes.object,
        labelShowBg: PropTypes.bool,
        labelBgStyle: PropTypes.object,
        labelBgPadding: PropTypes.arrayOf(PropTypes.number),
        labelBgBorderRadius: PropTypes.number,
        markerStart: PropTypes.oneOfType([
            PropTypes.string,
            PropTypes.shape({
                type: PropTypes.string.isRequired,
                color: PropTypes.string,
                width: PropTypes.number,
                height: PropTypes.number,
                markerUnits: PropTypes.string,
                orient: PropTypes.string,
                strokeWidth: PropTypes.number,
            })
        ]),
        markerEnd: PropTypes.oneOfType([
            PropTypes.string,
            PropTypes.shape({
                type: PropTypes.string.isRequired,
                color: PropTypes.string,
                width: PropTypes.number,
                height: PropTypes.number,
                markerUnits: PropTypes.string,
                orient: PropTypes.string,
                strokeWidth: PropTypes.number,
            })
        ]),
    })),

    // ===================
    // VIEWPORT PROPS
    // ===================

    /**
     * The initial viewport position and zoom level
     */
    defaultViewport: PropTypes.shape({
        x: PropTypes.number,
        y: PropTypes.number,
        zoom: PropTypes.number,
    }),

    /**
     * Current viewport state (read-only, updated by callbacks)
     */
    viewport: PropTypes.shape({
        x: PropTypes.number,
        y: PropTypes.number,
        zoom: PropTypes.number,
    }),

    /**
     * Whether viewport is currently moving (panning/zooming)
     */
    viewportMoving: PropTypes.bool,

    /**
     * Minimum zoom level (default: 0.5)
     */
    minZoom: PropTypes.number,

    /**
     * Maximum zoom level (default: 2)
     */
    maxZoom: PropTypes.number,

    /**
     * Whether to snap nodes to a grid when dragging
     */
    snapToGrid: PropTypes.bool,

    /**
     * The grid size for snapping [x, y] (default: [15, 15])
     */
    snapGrid: PropTypes.arrayOf(PropTypes.number),

    /**
     * Limit the viewport panning extent [[minX, minY], [maxX, maxY]]
     */
    translateExtent: PropTypes.arrayOf(PropTypes.arrayOf(PropTypes.number)),

    /**
     * Limit where nodes can be placed [[minX, minY], [maxX, maxY]]
     */
    nodeExtent: PropTypes.arrayOf(PropTypes.arrayOf(PropTypes.number)),

    /**
     * Only render nodes and edges that are visible in the viewport
     */
    onlyRenderVisibleElements: PropTypes.bool,

    /**
     * Prevent scrolling on the page when the mouse is over the flow
     */
    preventScrolling: PropTypes.bool,

    /**
     * Automatically fit all nodes in view on initialization
     */
    fitView: PropTypes.bool,

    /**
     * Options for fitView behavior
     */
    fitViewOptions: PropTypes.shape({
        padding: PropTypes.number,
        includeHiddenNodes: PropTypes.bool,
        minZoom: PropTypes.number,
        maxZoom: PropTypes.number,
        duration: PropTypes.number,
        nodes: PropTypes.arrayOf(PropTypes.shape({
            id: PropTypes.string,
        })),
    }),

    // ===================
    // INTERACTION PROPS
    // ===================

    /**
     * Enable/disable node dragging behavior
     */
    nodesDraggable: PropTypes.bool,

    /**
     * Enable/disable the ability to make new connections between nodes
     */
    nodesConnectable: PropTypes.bool,

    /**
     * Enable/disable keyboard focus on nodes
     */
    nodesFocusable: PropTypes.bool,

    /**
     * Enable/disable keyboard focus on edges
     */
    edgesFocusable: PropTypes.bool,

    /**
     * Enable/disable the ability to select elements
     */
    elementsSelectable: PropTypes.bool,

    /**
     * Auto-pan viewport when making a new connection near edges
     */
    autoPanOnConnect: PropTypes.bool,

    /**
     * Auto-pan viewport when dragging a node near edges
     */
    autoPanOnNodeDrag: PropTypes.bool,

    /**
     * Speed of auto-panning (default: 15)
     */
    autoPanSpeed: PropTypes.number,

    /**
     * Enable/disable panning by dragging. Can be boolean or array of mouse buttons [0,1,2]
     */
    panOnDrag: PropTypes.oneOfType([
        PropTypes.bool,
        PropTypes.arrayOf(PropTypes.number)
    ]),

    /**
     * Enable panning by scrolling
     */
    panOnScroll: PropTypes.bool,

    /**
     * Speed of scroll-based panning (default: 0.5)
     */
    panOnScrollSpeed: PropTypes.number,

    /**
     * Restrict scroll panning direction: 'free', 'vertical', 'horizontal'
     */
    panOnScrollMode: PropTypes.oneOf(['free', 'vertical', 'horizontal']),

    /**
     * Enable zooming by scrolling
     */
    zoomOnScroll: PropTypes.bool,

    /**
     * Enable zooming by pinching on touch devices
     */
    zoomOnPinch: PropTypes.bool,

    /**
     * Enable zooming by double-clicking
     */
    zoomOnDoubleClick: PropTypes.bool,

    /**
     * Select nodes when dragging over them
     */
    selectNodesOnDrag: PropTypes.bool,

    /**
     * Enable selection box by dragging on the pane
     */
    selectionOnDrag: PropTypes.bool,

    /**
     * Selection mode: 'full' (fully enclosed) or 'partial' (touching)
     */
    selectionMode: PropTypes.oneOf(['full', 'partial']),

    /**
     * Enable click-based connection mode (click source then target)
     */
    connectOnClick: PropTypes.bool,

    /**
     * Connection mode: 'strict' (same handle type) or 'loose' (any handle)
     */
    connectionMode: PropTypes.oneOf(['strict', 'loose']),

    /**
     * Raise z-index of selected nodes
     */
    elevateNodesOnSelect: PropTypes.bool,

    /**
     * Raise z-index of selected edges
     */
    elevateEdgesOnSelect: PropTypes.bool,

    // ===================
    // EDGE PROPS
    // ===================

    /**
     * Default options applied to all new edges
     */
    defaultEdgeOptions: PropTypes.shape({
        type: PropTypes.string,
        style: PropTypes.object,
        animated: PropTypes.bool,
        markerStart: PropTypes.object,
        markerEnd: PropTypes.object,
    }),

    /**
     * Default color for edge markers
     */
    defaultMarkerColor: PropTypes.string,

    /**
     * Allow edges to be reconnected after creation
     */
    edgesReconnectable: PropTypes.bool,

    /**
     * Radius for reconnection detection (default: 10)
     */
    reconnectRadius: PropTypes.number,

    // ===================
    // CONNECTION LINE PROPS
    // ===================

    /**
     * Style for the connection line while dragging
     */
    connectionLineStyle: PropTypes.object,

    /**
     * Type of connection line: 'bezier', 'straight', 'step', 'smoothstep', 'simplebezier'
     */
    connectionLineType: PropTypes.oneOf(['bezier', 'straight', 'step', 'smoothstep', 'simplebezier']),

    /**
     * Radius for connection drop detection (default: 20)
     */
    connectionRadius: PropTypes.number,

    // ===================
    // CONNECTION VALIDATION
    // ===================

    /**
     * Rules for validating connections
     */
    connectionRules: PropTypes.shape({
        allowSelfConnection: PropTypes.bool,
        allowDuplicateConnections: PropTypes.bool,
        validSourceTypes: PropTypes.arrayOf(PropTypes.string),
        validTargetTypes: PropTypes.arrayOf(PropTypes.string),
    }),

    // ===================
    // KEYBOARD PROPS
    // ===================

    /**
     * Key code for deleting selected elements (default: 'Backspace', null to disable)
     */
    deleteKeyCode: PropTypes.string,

    /**
     * Key code for multi-selection box (default: 'Shift')
     */
    selectionKeyCode: PropTypes.string,

    /**
     * Key code for adding to selection
     */
    multiSelectionKeyCode: PropTypes.string,

    /**
     * Key code to activate zoom mode
     */
    zoomActivationKeyCode: PropTypes.string,

    /**
     * Key code to activate pan mode (default: 'Space')
     */
    panActivationKeyCode: PropTypes.string,

    /**
     * Disable keyboard accessibility features
     */
    disableKeyboardA11y: PropTypes.bool,

    // ===================
    // STYLE PROPS
    // ===================

    /**
     * CSS class name that prevents panning when applied to elements
     */
    noPanClassName: PropTypes.string,

    /**
     * CSS class name that prevents dragging when applied to elements
     */
    noDragClassName: PropTypes.string,

    /**
     * CSS class name that prevents wheel zoom when applied to elements
     */
    noWheelClassName: PropTypes.string,

    /**
     * Custom CSS styles for the container div
     */
    style: PropTypes.object,

    /**
     * CSS class name for the container div
     */
    className: PropTypes.string,

    /**
     * Color mode: 'light', 'dark', or 'system'
     */
    colorMode: PropTypes.oneOf(['light', 'dark', 'system']),

    /**
     * Theme preset: 'glass' (default), 'solid', or 'minimal'
     * - glass: Glassmorphism with blur and transparency
     * - solid: Opaque nodes with subtle shadows (better for complex backgrounds)
     * - minimal: Clean lines with minimal styling
     */
    themePreset: PropTypes.oneOf(['glass', 'solid', 'minimal']),

    /**
     * Color scheme preset for node and edge colors.
     * Works in combination with themePreset for full customization.
     * Each scheme includes light and dark mode variants.
     * - default: Neutral blue/purple (default)
     * - ocean: Blues and teals
     * - forest: Greens and browns
     * - sunset: Oranges and reds
     * - midnight: Deep blues and purples
     * - rose: Pinks and reds
     */
    colorScheme: PropTypes.oneOf(['default', 'ocean', 'forest', 'sunset', 'midnight', 'rose']),

    /**
     * Custom theme configuration. Overrides CSS variables for fine-grained control.
     * All properties are optional - only specify what you want to customize.
     */
    theme: PropTypes.shape({
        /** Glass blur intensity in pixels (default: 12) */
        glassBlur: PropTypes.number,
        /** Glass saturation percentage (default: 180) */
        glassSaturate: PropTypes.number,
        /** Node background color (e.g., 'rgba(255, 255, 255, 0.72)') */
        nodeBackground: PropTypes.string,
        /** Node border color */
        nodeBorder: PropTypes.string,
        /** Node primary text color */
        nodeText: PropTypes.string,
        /** Node secondary/subtitle text color */
        nodeTextSecondary: PropTypes.string,
        /** Input node background color */
        inputNodeBackground: PropTypes.string,
        /** Input node border color */
        inputNodeBorder: PropTypes.string,
        /** Input node accent color (top bar) */
        inputNodeAccent: PropTypes.string,
        /** Output node background color */
        outputNodeBackground: PropTypes.string,
        /** Output node border color */
        outputNodeBorder: PropTypes.string,
        /** Output node accent color (bottom bar) */
        outputNodeAccent: PropTypes.string,
        /** Edge stroke color */
        edgeStroke: PropTypes.string,
        /** Selected edge stroke color */
        edgeStrokeSelected: PropTypes.string,
        /** Animated edge stroke color */
        edgeStrokeAnimated: PropTypes.string,
        /** Edge stroke width in pixels */
        edgeStrokeWidth: PropTypes.number,
        /** Handle background color */
        handleBackground: PropTypes.string,
        /** Handle border color */
        handleBorder: PropTypes.string,
        /** Connected handle color */
        handleConnected: PropTypes.string,
        /** Flow background color */
        backgroundColor: PropTypes.string,
        /** Background pattern color */
        backgroundPattern: PropTypes.string,
        /** Selection box background color */
        selectionBackground: PropTypes.string,
        /** Selection box border color */
        selectionBorder: PropTypes.string,
        /** Node border radius in pixels */
        borderRadius: PropTypes.number,
    }),

    // ===================
    // DISPLAY COMPONENTS
    // ===================

    /**
     * Show/hide the minimap navigation component
     */
    showMiniMap: PropTypes.bool,

    /**
     * Show/hide the control panel
     */
    showControls: PropTypes.bool,

    /**
     * Show/hide the background pattern
     */
    showBackground: PropTypes.bool,

    /**
     * Show/hide the developer tools panel
     */
    showDevTools: PropTypes.bool,

    // ===================
    // CONTROLS OPTIONS
    // ===================

    /**
     * Show zoom buttons in controls
     */
    controlsShowZoom: PropTypes.bool,

    /**
     * Show fit-view button in controls
     */
    controlsShowFitView: PropTypes.bool,

    /**
     * Show interactive toggle in controls
     */
    controlsShowInteractive: PropTypes.bool,

    /**
     * Position of controls panel
     */
    controlsPosition: PropTypes.oneOf(['top-left', 'top-right', 'bottom-left', 'bottom-right', 'top-center', 'bottom-center']),

    // ===================
    // MINIMAP OPTIONS
    // ===================

    /**
     * Color function or string for minimap nodes
     */
    miniMapNodeColor: PropTypes.string,

    /**
     * Stroke color for minimap nodes
     */
    miniMapNodeStrokeColor: PropTypes.string,

    /**
     * Border radius for minimap nodes
     */
    miniMapNodeBorderRadius: PropTypes.number,

    /**
     * Color for the minimap mask (viewport indicator)
     */
    miniMapMaskColor: PropTypes.string,

    /**
     * Position of the minimap
     */
    miniMapPosition: PropTypes.oneOf(['top-left', 'top-right', 'bottom-left', 'bottom-right']),

    /**
     * Allow panning by dragging the minimap
     */
    miniMapPannable: PropTypes.bool,

    /**
     * Allow zooming via the minimap
     */
    miniMapZoomable: PropTypes.bool,

    // ===================
    // BACKGROUND OPTIONS
    // ===================

    /**
     * Background pattern type: 'dots', 'lines', 'cross'
     */
    backgroundVariant: PropTypes.oneOf(['dots', 'lines', 'cross']),

    /**
     * Gap between background pattern elements
     */
    backgroundGap: PropTypes.oneOfType([
        PropTypes.number,
        PropTypes.arrayOf(PropTypes.number)
    ]),

    /**
     * Size of background pattern elements
     */
    backgroundSize: PropTypes.number,

    /**
     * Color of the background pattern
     */
    backgroundColor: PropTypes.string,

    // ===================
    // PANELS
    // ===================

    /**
     * Array of panel configurations for custom UI overlays
     */
    panels: PropTypes.arrayOf(PropTypes.shape({
        position: PropTypes.oneOf(['top-left', 'top-right', 'bottom-left', 'bottom-right', 'top-center', 'bottom-center']),
        children: PropTypes.any,
    })),

    // ===================
    // LAYOUT OPTIONS
    // ===================

    /**
     * Layout options for arranging nodes using the ELK layout engine (JSON string)
     */
    layoutOptions: PropTypes.string,

    // ===================
    // TRACKING OPTIONS
    // ===================

    /**
     * Track node position during drag (can be expensive)
     */
    trackNodeDrag: PropTypes.bool,

    /**
     * Track viewport changes during pan/zoom
     */
    trackViewport: PropTypes.bool,

    // ===================
    // DELETE PREVENTION
    // ===================

    /**
     * Enable delete prevention checks
     */
    preventDelete: PropTypes.bool,

    /**
     * List of node IDs that cannot be deleted
     */
    preventDeleteNodes: PropTypes.arrayOf(PropTypes.string),

    /**
     * List of edge IDs that cannot be deleted
     */
    preventDeleteEdges: PropTypes.arrayOf(PropTypes.string),

    // ===================
    // SAVE/RESTORE
    // ===================

    /**
     * Trigger to export the current flow state. Set to true to export.
     * After export, this will be reset to false and flowState will be populated.
     */
    exportFlowState: PropTypes.bool,

    /**
     * The exported flow state as a serializable object containing nodes, edges, and viewport.
     * This is populated when exportFlowState is triggered.
     */
    flowState: PropTypes.shape({
        nodes: PropTypes.array,
        edges: PropTypes.array,
        viewport: PropTypes.shape({
            x: PropTypes.number,
            y: PropTypes.number,
            zoom: PropTypes.number,
        }),
    }),

    /**
     * Import/restore a previously exported flow state.
     * Set this to a flowState object to restore the flow.
     */
    restoreFlowState: PropTypes.shape({
        nodes: PropTypes.array,
        edges: PropTypes.array,
        viewport: PropTypes.shape({
            x: PropTypes.number,
            y: PropTypes.number,
            zoom: PropTypes.number,
        }),
    }),

    // ===================
    // VIEWPORT ACTIONS
    // ===================

    /**
     * Trigger viewport actions programmatically.
     * Set to an action object to execute. Will be reset to null after execution.
     *
     * Supported actions:
     * - { action: 'fitView', options: {...} }
     * - { action: 'zoomIn', options: {...} }
     * - { action: 'zoomOut', options: {...} }
     * - { action: 'setZoom', zoom: 1.5, options: {...} }
     * - { action: 'setCenter', x: 100, y: 100, options: {...} }
     * - { action: 'setViewport', viewport: {x, y, zoom}, options: {...} }
     * - { action: 'focusNode', nodeId: 'node-1', zoom: 1.5, duration: 500 }
     */
    viewportAction: PropTypes.shape({
        action: PropTypes.oneOf(['fitView', 'zoomIn', 'zoomOut', 'setZoom', 'setCenter', 'setViewport', 'focusNode']),
        nodeId: PropTypes.string,
        x: PropTypes.number,
        y: PropTypes.number,
        zoom: PropTypes.number,
        duration: PropTypes.number,
        viewport: PropTypes.shape({
            x: PropTypes.number,
            y: PropTypes.number,
            zoom: PropTypes.number,
        }),
        options: PropTypes.object,
    }),

    // ===================
    // IMAGE EXPORT
    // ===================

    /**
     * Trigger to download the flow as an image.
     * Set to a config object to initiate download. Will be reset to null after download.
     *
     * Config options:
     * - format: 'png' | 'svg' | 'jpeg' (default: 'png')
     * - filename: string (default: 'flow')
     * - quality: number 0-1 (default: 0.95, for jpeg only)
     * - backgroundColor: string (default: '#ffffff')
     * - pixelRatio: number (default: 2, for higher resolution)
     */
    downloadImage: PropTypes.shape({
        format: PropTypes.oneOf(['png', 'svg', 'jpeg', 'jpg']),
        filename: PropTypes.string,
        quality: PropTypes.number,
        backgroundColor: PropTypes.string,
        pixelRatio: PropTypes.number,
    }),

    /**
     * Information about the last successful image download.
     * Populated after a successful downloadImage operation.
     */
    imageDownloaded: PropTypes.shape({
        filename: PropTypes.string,
        format: PropTypes.string,
        timestamp: PropTypes.number,
    }),

    // ===================
    // COPY/PASTE
    // ===================

    /**
     * Trigger to copy selected nodes and edges to clipboard.
     * Set to true to copy. Will be reset to false after copying.
     * If nothing is selected, copies all nodes and their connecting edges.
     */
    copyAction: PropTypes.bool,

    /**
     * Trigger to paste nodes and edges from clipboard.
     * Set to an object with optional offset: { offset: { x: 50, y: 50 } }
     * Will be reset to null after pasting.
     */
    pasteAction: PropTypes.shape({
        offset: PropTypes.shape({
            x: PropTypes.number,
            y: PropTypes.number,
        }),
    }),

    /**
     * Internal clipboard containing copied nodes and edges.
     * Populated by copyAction, consumed by pasteAction.
     */
    clipboard: PropTypes.shape({
        nodes: PropTypes.array,
        edges: PropTypes.array,
        timestamp: PropTypes.number,
    }),

    /**
     * Information about the last paste operation.
     * Contains the IDs of newly created nodes and edges.
     */
    pastedElements: PropTypes.shape({
        nodeIds: PropTypes.arrayOf(PropTypes.string),
        edgeIds: PropTypes.arrayOf(PropTypes.string),
        timestamp: PropTypes.number,
    }),

    // ===================
    // CALLBACK OUTPUTS (Read-only props updated by component)
    // ===================

    /**
     * Whether the flow has been initialized
     */
    initialized: PropTypes.bool,

    /**
     * Last error that occurred
     */
    lastError: PropTypes.shape({
        id: PropTypes.string,
        message: PropTypes.string,
        type: PropTypes.string,
        timestamp: PropTypes.number,
    }),

    /**
     * IDs of currently selected nodes
     */
    selectedNodes: PropTypes.arrayOf(PropTypes.string),

    /**
     * IDs of currently selected edges
     */
    selectedEdges: PropTypes.arrayOf(PropTypes.string),

    /**
     * The last connection that was made
     */
    lastConnection: PropTypes.shape({
        source: PropTypes.string,
        sourceHandle: PropTypes.string,
        target: PropTypes.string,
        targetHandle: PropTypes.string,
    }),

    /**
     * Current connection being created
     */
    connectionStartHandle: PropTypes.shape({
        nodeId: PropTypes.string,
        handleId: PropTypes.string,
        handleType: PropTypes.string,
    }),

    /**
     * The node that was clicked
     */
    clickedNode: PropTypes.shape({
        id: PropTypes.string,
        data: PropTypes.object,
        position: PropTypes.object,
    }),

    /**
     * The node that was double-clicked
     */
    doubleClickedNode: PropTypes.shape({
        id: PropTypes.string,
        data: PropTypes.object,
        position: PropTypes.object,
    }),

    /**
     * Context menu info for a node
     */
    contextMenuNode: PropTypes.shape({
        id: PropTypes.string,
        data: PropTypes.object,
        position: PropTypes.object,
        clientX: PropTypes.number,
        clientY: PropTypes.number,
    }),

    /**
     * Node data from a drop event (drag and drop from external source).
     * Contains the type, position, and data of the dropped item.
     * Use this in a callback to create a new node at the drop position.
     */
    droppedNode: PropTypes.shape({
        type: PropTypes.string,
        position: PropTypes.shape({
            x: PropTypes.number,
            y: PropTypes.number,
        }),
        data: PropTypes.object,
        clientX: PropTypes.number,
        clientY: PropTypes.number,
        timestamp: PropTypes.number,
    }),

    /**
     * The node being dragged
     */
    draggedNode: PropTypes.shape({
        id: PropTypes.string,
        isDragging: PropTypes.bool,
        startPosition: PropTypes.object,
        currentPosition: PropTypes.object,
        endPosition: PropTypes.object,
    }),

    /**
     * The node being hovered
     */
    hoveredNode: PropTypes.shape({
        id: PropTypes.string,
        data: PropTypes.object,
    }),

    /**
     * The edge that was clicked
     */
    clickedEdge: PropTypes.shape({
        id: PropTypes.string,
        source: PropTypes.string,
        target: PropTypes.string,
    }),

    /**
     * The edge that was double-clicked
     */
    doubleClickedEdge: PropTypes.shape({
        id: PropTypes.string,
        source: PropTypes.string,
        target: PropTypes.string,
    }),

    /**
     * Context menu info for an edge
     */
    contextMenuEdge: PropTypes.shape({
        id: PropTypes.string,
        source: PropTypes.string,
        target: PropTypes.string,
        clientX: PropTypes.number,
        clientY: PropTypes.number,
    }),

    /**
     * The edge being hovered
     */
    hoveredEdge: PropTypes.shape({
        id: PropTypes.string,
        source: PropTypes.string,
        target: PropTypes.string,
    }),

    /**
     * Position where the pane was clicked
     */
    paneClickPosition: PropTypes.shape({
        clientX: PropTypes.number,
        clientY: PropTypes.number,
    }),

    /**
     * Context menu info for the pane
     */
    paneContextMenu: PropTypes.shape({
        clientX: PropTypes.number,
        clientY: PropTypes.number,
    }),

    /**
     * IDs of recently deleted nodes
     */
    deletedNodes: PropTypes.arrayOf(PropTypes.string),

    /**
     * IDs of recently deleted edges
     */
    deletedEdges: PropTypes.arrayOf(PropTypes.string),

    /**
     * Dash-assigned callback that should be called to report property changes
     */
    setProps: PropTypes.func,
};

DashFlows.displayName = 'DashFlows';

export default DashFlows;