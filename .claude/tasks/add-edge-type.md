# Task: Add a New Edge Type

## Purpose
Create a new custom edge type for dash-flows.

## Parameters
- `EDGE_NAME`: PascalCase name (e.g., `GradientEdge`)
- `TYPE_STRING`: Lowercase string used in `type` field (e.g., `gradient`)

## Steps

1. **Create the React component**
   - Copy `src/lib/components/edges/StraightEdge.js` as template (simplest)
   - Or `ButtonEdge.js` if the edge needs interactive elements
   - Save as `src/lib/components/edges/{EDGE_NAME}.js`
   - Use a path helper: `getBezierPath`, `getStraightPath`, `getSmoothStepPath`, or `getSimpleBezierPath`
   - Render with `<BaseEdge>` for the path and `<EdgeLabelRenderer>` for labels
   - Add glass morphism label styling
   - Add complete `PropTypes` with JSDoc descriptions

2. **Export from edges index**
   - Add to `src/lib/components/edges/index.js`:
     ```javascript
     export { default as {EDGE_NAME} } from './{EDGE_NAME}';
     ```

3. **Export from library index**
   - Add import and export to `src/lib/index.js`

4. **Register the type**
   - In `src/lib/components/DashFlows.react.js`, add to `edgeTypes` object (~line 66):
     ```javascript
     {TYPE_STRING}: {EDGE_NAME},
     ```
   - Add the import at the top of the file

5. **Build**
   ```bash
   npm run build
   ```

6. **Verify**
   - Check `dash_flows/{EDGE_NAME}.py` was generated

7. **Create example**
   - Add edge to an existing example or create `examples/NN_{type_string}_edge.py`

## Verification
- [ ] Edge renders between two nodes
- [ ] Label displays correctly with glass styling
- [ ] Selection highlight works
- [ ] Markers (arrows) work
- [ ] Dark mode works
- [ ] Python wrapper has all props documented