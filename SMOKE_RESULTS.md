# Smoke Test Results

Runtime validation matrix for every app in `examples/`, produced by the two
committed gates (no browser required):

- **Import** — `python scripts/smoke_examples.py`: the module imports and its
  `@callback`s register without error.
- **Runtime** — `python scripts/smoke_runtime.py`: the app serves `/`,
  `/_dash-layout`, and `/_dash-dependencies` (HTTP 200 + valid JSON) via the
  Flask/WSGI test client.

**Summary:** Import 35/35 · Runtime 35/35

| Example | Import | Runtime |
|---------|:------:|:-------:|
| `01_basic_nodes_and_edges.py` | ✅ | ✅ |
| `02_all_node_types.py` | ✅ | ✅ |
| `03_all_edge_types.py` | ✅ | ✅ |
| `04_background_variants.py` | ✅ | ✅ |
| `05_controls_and_minimap.py` | ✅ | ✅ |
| `06_handle_configurations.py` | ✅ | ✅ |
| `07_node_interactions.py` | ✅ | ✅ |
| `08_connection_validation.py` | ✅ | ✅ |
| `09_viewport_controls.py` | ✅ | ✅ |
| `10_selection_multiselect.py` | ✅ | ✅ |
| `11_dark_mode_mantine.py` | ✅ | ✅ |
| `12_elk_layouts.py` | ✅ | ✅ |
| `13_complete_showcase.py` | ✅ | ✅ |
| `14_dash_components_in_nodes.py` | ✅ | ✅ |
| `15_save_restore.py` | ✅ | ✅ |
| `16_connection_limits.py` | ✅ | ✅ |
| `17_drag_and_drop.py` | ✅ | ✅ |
| `18_export_image.py` | ✅ | ✅ |
| `19_copy_paste.py` | ✅ | ✅ |
| `20_context_menu.py` | ✅ | ✅ |
| `21_ui_components.py` | ✅ | ✅ |
| `22_custom_icons.py` | ✅ | ✅ |
| `23_callback_stress_test.py` | ✅ | ✅ |
| `24_smart_handles.py` | ✅ | ✅ |
| `25_phase1_features.py` | ✅ | ✅ |
| `26_floating_edges.py` | ✅ | ✅ |
| `27_helper_lines.py` | ✅ | ✅ |
| `28_add_node_on_drop.py` | ✅ | ✅ |
| `29_accessibility.py` | ✅ | ✅ |
| `30_resize_constraints.py` | ✅ | ✅ |
| `31_animated_layout.py` | ✅ | ✅ |
| `32_undo_redo.py` | ✅ | ✅ |
| `33_computing_flows.py` | ✅ | ✅ |
| `34_viewport_portal.py` | ✅ | ✅ |
| `35_subflows.py` | ✅ | ✅ |

Browser-fidelity checks (React canvas mounts, no SEVERE console errors) live in
`tests/test_examples_render.py` and run under `pytest` with `dash[testing]`.

