"""Browser-level render test for representative examples.

Complements the two committed smoke gates (scripts/smoke_examples.py for
import level, scripts/smoke_runtime.py for WSGI runtime level) with real
browser fidelity: the app is served, Selenium waits for the `.react-flow`
canvas to mount, and the browser console must be free of SEVERE errors.

Needs `dash[testing]` and a chromedriver on PATH:
    pip install -r tests/requirements.txt
    pytest tests/test_examples_render.py
"""
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

# A representative slice of examples/: static graph, handle configuration,
# callback-driven interactions, and an advanced feature (undo/redo).
EXAMPLES = [
    "01_basic_nodes_and_edges",
    "06_handle_configurations",
    "07_node_interactions",
    "32_undo_redo",
]


def load_example_app(name):
    """Import examples/<name>.py (skipping its __main__ block) and return app."""
    path = ROOT / "examples" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"example_{name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.app


@pytest.mark.parametrize("name", EXAMPLES)
def test_example_renders_react_flow(dash_duo, name):
    app = load_example_app(name)
    dash_duo.start_server(app)

    dash_duo.wait_for_element(".react-flow", timeout=15)
    dash_duo.wait_for_element(".react-flow__node", timeout=15)

    severe = [
        entry
        for entry in dash_duo.get_logs() or []
        if entry.get("level") == "SEVERE"
    ]
    assert not severe, f"browser console errors in {name}: {severe}"
