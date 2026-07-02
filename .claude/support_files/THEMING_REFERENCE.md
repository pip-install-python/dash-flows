# Theming Reference for dash-flows

## CSS Variable Quick Reference

### Core Variables

| Variable | Default (Light) | Description |
|----------|----------------|-------------|
| `--df-glass-blur` | `12px` | Backdrop blur amount |
| `--df-glass-saturate` | `180%` | Backdrop saturation |
| `--df-node-bg` | `rgba(255,255,255,0.72)` | Node background |
| `--df-node-text` | `#1a1b1e` | Primary text color |
| `--df-node-text-secondary` | `#495057` | Secondary text color |
| `--df-node-border` | `rgba(255,255,255,0.5)` | Node border |
| `--df-node-shadow` | `0 8px 32px rgba(31,38,135,0.15)` | Node shadow |
| `--df-edge-stroke` | `#64748b` | Edge color |
| `--df-edge-stroke-selected` | `#3b82f6` | Selected edge color |
| `--df-handle-bg` | `#fff` | Handle background |
| `--df-handle-border` | `#64748b` | Handle border |
| `--df-handle-size` | `14px` | Handle diameter |
| `--df-background-color` | `#fafafa` | Canvas background |

### Spacing Scale

| Variable | Value |
|----------|-------|
| `--df-spacing-xs` | `4px` |
| `--df-spacing-sm` | `8px` |
| `--df-spacing-md` | `12px` |
| `--df-spacing-lg` | `16px` |
| `--df-spacing-xl` | `24px` |

### Border Radius Scale

| Variable | Value |
|----------|-------|
| `--df-radius-xs` | `4px` |
| `--df-radius-sm` | `6px` |
| `--df-radius-md` | `10px` |
| `--df-radius-lg` | `14px` |
| `--df-radius-xl` | `20px` |

### Transition Timings

| Variable | Value |
|----------|-------|
| `--df-transition-fast` | `150ms cubic-bezier(0.4, 0, 0.2, 1)` |
| `--df-transition-normal` | `250ms cubic-bezier(0.4, 0, 0.2, 1)` |
| `--df-transition-slow` | `350ms cubic-bezier(0.4, 0, 0.2, 1)` |

## Theme Presets

Activate via `DashFlows(themePreset="glass")`:

| Preset | Description |
|--------|-------------|
| `glass` | Full glass morphism (default) |
| `solid` | Opaque backgrounds, no blur |
| `minimal` | Thin borders, minimal shadows |

## Color Schemes

Activate via `DashFlows(colorScheme="ocean")`:

| Scheme | Accent Colors |
|--------|--------------|
| `default` | Blue/Green/Purple |
| `ocean` | Blues and teals |
| `forest` | Greens |
| `sunset` | Oranges and reds |
| `midnight` | Deep blues |
| `rose` | Pinks |

## Programmatic Theming

Override variables via the `theme` prop:
```python
DashFlows(
    theme={
        "glassBlur": 15,
        "glassSaturate": 200,
        "nodeBackground": "rgba(0, 0, 0, 0.8)",
        "nodeBorder": "#333",
        "nodeText": "#ffffff",
        "edgeStroke": "#888888",
        "borderRadius": 12,
    }
)
```

## Dark Mode Activation

Three methods:
1. `DashFlows(colorMode="dark")` -- React Flow native
2. `dmc.MantineProvider(forceColorScheme="dark", ...)` -- Mantine
3. Add `.dark` class to parent element

## CSS File Location

All styles in: `src/lib/styles/glass-theme.css`