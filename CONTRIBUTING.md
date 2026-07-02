# Contributing to dash-flows

dash-flows wraps [@xyflow/react](https://reactflow.dev) (React Flow 12) for
Plotly Dash. The React components in `src/lib/` are the source of truth; the
Python package in `dash_flows/` is auto-generated from their PropTypes.

## Setup

```bash
npm install
pip install -r requirements.txt        # library + examples
pip install -r requirements-docs.txt   # documentation site
```

## Workflow

1. Edit React components in `src/lib/components/` (never `dash_flows/*.py` —
   they are generated).
2. Rebuild: `npm run build` (webpack bundle → `dash_flows/dash_flows.min.js`,
   then `dash-generate-components` regenerates the Python wrappers).
3. See it running: `python run.py` → http://localhost:8560 — the docs site
   embeds a live demo of every example. Standalone apps live in `examples/`
   (`python examples/01_basic_nodes_and_edges.py`).

## Before you commit

Run the three validation gates (all CI-friendly, no browser needed):

```bash
python scripts/smoke_examples.py   # every example imports & registers callbacks
python scripts/smoke_runtime.py    # every example serves /, /_dash-layout, /_dash-dependencies
python scripts/validate_docs.py    # every docs page renders through markdown2dash
```

Browser-fidelity tests (need `dash[testing]` + chromedriver):

```bash
pip install -r tests/requirements.txt
pytest
```

## Adding an example + its docs page section

1. Add `examples/NN_name.py` — a standalone app (`app = Dash(...)`, global
   `@callback`, `app.run()` under `if __name__ == "__main__":`).
2. Add its embeddable twin `docs/<topic>/exNN.py` — exposes a module-level
   `component`, uses global `@callback`, **prefixes every Dash component id
   with `exNN-`** (callback ids are global across the whole docs app — an
   unprefixed id will collide with another page's demo and crash startup).
3. Add a section to `docs/<topic>/<topic>.md`: prose + `.. exec::docs.<topic>.exNN`
   + `.. source::examples/NN_name.py` + a "How it works" bullet list.
   Headings must be plain text (no backticks/bold/links — the renderer builds
   anchors from the first heading token).
4. Re-run the three gates above.

## Gotchas

- `assets/` is auto-served by Dash — every `.css`/`.js` there loads on every
  docs page.
- Version lives in two files: bump `package.json` **and** `package-info.json`.
- One source-map generator only: `devtool` XOR `SourceMapDevToolPlugin` in
  `webpack.config.js`.
- Never run `npm audit fix --force` — it breaks the build toolchain.
