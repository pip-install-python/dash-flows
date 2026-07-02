# Task: Add a New Node Type

## Purpose
Create a new custom node type for dash-flows with glass morphism styling.

## Parameters
- `NODE_NAME`: PascalCase name (e.g., `DiamondNode`)
- `TYPE_STRING`: Lowercase string used in `type` field (e.g., `diamond`)

## Steps

1. **Create the React component**
   - Copy `src/lib/components/nodes/DefaultNode.js` as template
   - Save as `src/lib/components/nodes/{NODE_NAME}.js`
   - Modify the JSX structure for the new node shape/behavior
   - Include the `renderDashComponent()` helper if icons are needed (copy from InputNode.js)
   - Wrap in `React.memo()`
   - Add complete `PropTypes` with JSDoc descriptions for every prop

2. **Export from nodes index**
   - Add to `src/lib/components/nodes/index.js`:
     ```javascript
     export { default as {NODE_NAME} } from './{NODE_NAME}';
     ```

3. **Export from library index**
   - Add import and export to `src/lib/index.js`

4. **Register the type**
   - In `src/lib/components/DashFlows.react.js`, add to `nodeTypes` object (~line 53):
     ```javascript
     {TYPE_STRING}: {NODE_NAME},
     ```
   - Add the import at the top of the file

5. **Add CSS styling**
   - Add node-specific styles to `src/lib/styles/glass-theme.css`
   - Follow the `.df-glass-node.df-{type}-node` pattern
   - Include dark mode overrides

6. **Build**
   ```bash
   npm run build
   ```

7. **Verify**
   - Check `dash_flows/{NODE_NAME}.py` was generated
   - Check `dash_flows/metadata.json` includes the new component

8. **Create example**
   - Add `examples/NN_{type_string}_node.py`
   - Demonstrate the node in a flow with connections

## Verification
- [ ] Component renders in browser
- [ ] Handles connect properly
- [ ] Glass morphism styling applies
- [ ] Dark mode works
- [ ] Python wrapper has all props documented
- [ ] Example runs without errors