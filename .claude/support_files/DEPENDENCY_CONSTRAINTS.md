# Dependency Constraints & Compatibility

## Critical Constraints

### zustand must stay on 4.x
`@xyflow/react` declares `zustand: ^4.4.0` as a dependency. Zustand 5.x is incompatible.
Do NOT upgrade zustand until React Flow updates their requirement.

### elkjs is 77% of the bundle (1.45MB)
The `elkjs/lib/elk.bundled.js` file dominates the webpack bundle.
Consider lazy-loading via dynamic import when `layoutOptions` is first used.

### ramda is minimally used
Only imported via `^0.26.1`. Can likely be replaced with native JS to reduce bundle.
Check usage before removing: `grep -r "ramda" src/`

## Version Matrix (as of March 2026)

| Package | Pinned | Installed | Latest | Constraint |
|---------|--------|-----------|--------|------------|
| @xyflow/react | ^12.10.1 | 12.10.1 | 12.10.1 | None — safe to update within 12.x |
| elkjs | ^0.9.3 | 0.9.3 | 0.11.1 | 0.x semver — test before major bumps |
| html-to-image | ^1.11.13 | 1.11.13 | 1.11.13 | At latest |
| zustand | ^4.5.5 | 4.5.6 | 5.0.12 | **Blocked by React Flow** |
| ramda | ^0.26.1 | 0.26.1 | 0.32.0 | 0.x semver — breaking changes likely |
| react | ^18.2.0 | 18.2.0 | 19.x | Dash bundles React — follow Dash's version |
| react-dom | ^18.2.0 | 18.2.0 | 19.x | Must match react version |

## React Flow 12.x New Features Timeline

| Version | Key Addition |
|---------|-------------|
| 12.4.0 | `useNodeConnections` hook |
| 12.5.0 | Enhanced fitView padding |
| 12.6.0 | `resizeDirection` for NodeResizeControl |
| 12.7.0 | `ariaRole`, `ariaLabelConfig`, `autoPanOnNodeFocus`, `ease`/`interpolate` on viewport |
| 12.8.0 | `connectionDragThreshold` |
| 12.9.0 | `EdgeToolbar` component |
| 12.10.0 | `zIndexMode`, `experimental_useOnNodesChangeMiddleware` |