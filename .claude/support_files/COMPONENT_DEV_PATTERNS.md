# Component Development Patterns for dash-flows

## New Node Type Checklist

1. Create `src/lib/components/nodes/MyNode.js`
2. Export from `src/lib/components/nodes/index.js`
3. Import + export from `src/lib/index.js`
4. Register in `DashFlows.react.js` `nodeTypes` object (~line 53)
5. Run `npm run build`
6. Verify `dash_flows/MyNode.py` was generated
7. Create example in `examples/`

## New Edge Type Checklist

1. Create `src/lib/components/edges/MyEdge.js`
2. Export from `src/lib/components/edges/index.js`
3. Import + export from `src/lib/index.js`
4. Register in `DashFlows.react.js` `edgeTypes` object (~line 66)
5. Run `npm run build`
6. Verify `dash_flows/MyEdge.py` was generated
7. Create example in `examples/`

## PropTypes Requirements

Every prop MUST have a JSDoc comment for `dash-generate-components`:

```javascript
MyComponent.propTypes = {
    /** Unique identifier for the component */
    id: PropTypes.string.isRequired,

    /** Label text displayed in the component */
    label: PropTypes.string,

    /** Additional data passed to the component */
    data: PropTypes.shape({
        /** Main display text */
        label: PropTypes.string,
        /** Whether to show the icon */
        showIcon: PropTypes.bool,
    }),
};
```

Without descriptions, the build shows "Description is missing!" warnings and Python docstrings will be empty.

## DashIconify Rendering in Nodes

Nodes that support custom icons must include the full `renderDashComponent()` function. The canonical implementation is in `src/lib/components/nodes/InputNode.js` (lines 17-100). It handles:

1. React elements directly
2. Dash 3.x `componentPath` format
3. Dash 2.x `_dashprivate_layout` format
4. Serialized Dash components (from callbacks)
5. DashIconify-specific fallback using Iconify API URLs

## Smart Handles Pattern

Nodes support a `smartHandles` mode for optimal edge routing. When `data.smartHandles` is true, the node renders handles on all 4 sides (top, bottom, left, right) instead of just top/bottom.

**How it works:**
1. `DashFlows(smartHandles=True)` injects `data.smartHandles=True` into every node
2. Node components render 4 source + 4 target handles (IDs: `source-top`, `source-bottom`, etc.)
3. DashFlows computes the optimal `sourceHandle`/`targetHandle` per edge based on relative node positions
4. Edges with explicit `sourceHandle`/`targetHandle` are not overridden

**Adding smart handles to a new node type:**
```javascript
// In your node component, add conditional multi-handle rendering:
const renderSmartHandles = (type) => {
    const positions = [
        { pos: Position.Top, name: 'top' },
        { pos: Position.Bottom, name: 'bottom' },
        { pos: Position.Left, name: 'left' },
        { pos: Position.Right, name: 'right' },
    ];
    return positions.map(({ pos, name }) => (
        <Handle
            key={`${type}-${name}`}
            id={`${type}-${name}`}
            type={type}
            position={pos}
            isConnectable={isConnectable}
            style={data.handleStyle}
        />
    ));
};

// Then in the JSX:
{data.smartHandles ? renderSmartHandles('target') : (
    <Handle type="target" position={data.targetPosition || Position.Top} ... />
)}
```

**Manual handle positioning (without smartHandles):**
```python
# Set sourcePosition/targetPosition in node data for manual control
node = {
    "id": "1",
    "type": "default",
    "data": {
        "label": "Horizontal Node",
        "sourcePosition": "right",
        "targetPosition": "left",
    },
    "position": {"x": 100, "y": 100},
}
```

See `examples/24_smart_handles.py` for a complete demonstration.

## Testing a New Component

Minimal test script:
```python
import dash
from dash import html
import dash_flows

app = dash.Dash(__name__)
app.layout = html.Div([
    dash_flows.DashFlows(
        id="test",
        nodes=[{
            "id": "1",
            "type": "myNewType",
            "data": {"label": "Test"},
            "position": {"x": 100, "y": 100},
        }],
        edges=[],
        style={"height": "400px"},
        fitView=True,
    )
])
if __name__ == "__main__":
    app.run(debug=True)
```

## EdgeToolbar Pattern

The `EdgeToolbar` component (from `@xyflow/react` 12.9.0+) attaches a toolbar overlay to edges.
Integrated in `ButtonEdge.js` — shown when `data.showToolbar=true` and edge is selected.

```javascript
import { EdgeToolbar } from '@xyflow/react';

// Inside an edge component:
{selected && data?.showToolbar && (
    <EdgeToolbar>
        <div className="df-edge-toolbar" style={toolbarStyle}>
            <button onClick={handleEdit}>Edit</button>
            <button onClick={handleDelete}>Delete</button>
        </div>
    </EdgeToolbar>
)}
```

## Adding New Pass-through Props

To add a new React Flow prop to DashFlows, edit 4 locations in `DashFlows.react.js`:

1. **Default value** in the outer component destructuring (~line 1355)
2. **Props object** in the reconstruction block (~line 1455)
3. **`<ReactFlow>` passthrough** in the JSX (~line 1095)
4. **PropTypes** with JSDoc description (~line 1870+)

## Key File Paths

| Purpose | Path |
|---------|------|
| Main component | `src/lib/components/DashFlows.react.js` |
| Node type registry | `DashFlows.react.js` ~line 53 |
| Edge type registry | `DashFlows.react.js` ~line 66 |
| Library exports | `src/lib/index.js` |
| Node components | `src/lib/components/nodes/` |
| Edge components | `src/lib/components/edges/` |
| Theme CSS | `src/lib/styles/glass-theme.css` |
| Node reference | `src/lib/components/nodes/InputNode.js` |
| Edge reference | `src/lib/components/edges/StraightEdge.js` |