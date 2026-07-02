"""
dash-flows documentation site.

A lean, markdown-driven documentation app (seeded from the Dash Documentation
Boilerplate). Documentation lives in ``docs/<topic>/<topic>.md`` and is
auto-discovered by ``pages/markdown.py``. Each page renders prose plus live
component demos (``.. exec::``), syntax-highlighted source (``.. source::``),
and auto-generated prop tables (``.. kwargs::``).

Run:
    pip install -r requirements-docs.txt
    python run.py
Then open http://localhost:8560

Backend (Dash 4.1+): set DASH_BACKEND=flask|fastapi|quart (default flask).
On Dash < 4.1 the ``backend=`` kwarg is unsupported and is dropped
automatically, so the site still boots (minus the async backends).
"""
import os

import dash
from dash import Dash

from lib.backend import resolve_backend, get_backend_info

# Optional AI/LLM SEO integration (dash-improve-my-llms). The site runs fine
# without it — /llms.txt endpoints are simply not registered.
try:
    from dash_improve_my_llms import add_llms_routes, LLMSConfig, register_page_metadata
    _HAS_LLMS = True
except Exception:  # pragma: no cover - optional dependency
    _HAS_LLMS = False

BACKEND = resolve_backend()
BACKEND_INFO = get_backend_info(BACKEND)

print(f"[dash-flows docs] Dash {dash.__version__} · backend='{BACKEND}' · llms={_HAS_LLMS}")

_index_string = open(os.path.join("templates", "index.html")).read()

_dash_kwargs = dict(
    use_pages=True,
    suppress_callback_exceptions=True,
    update_title=None,
    index_string=_index_string,
)

# Dash 4.1+ accepts backend=; older Dash (3.x) does not — degrade gracefully.
try:
    app = Dash(__name__, backend=BACKEND, **_dash_kwargs)
except TypeError:
    app = Dash(__name__, **_dash_kwargs)

# Expose backend info so UI components can render a badge without re-reading env.
app._backend_info = BACKEND_INFO
app._base_url = os.environ.get("DASH_FLOWS_BASE_URL", "http://localhost:8560")

# Pages (home + every docs/*.md) are auto-discovered by Dash from the pages/
# folder because use_pages=True; importing pages/markdown.py there registers
# each markdown file as a page.

if _HAS_LLMS:
    register_page_metadata(
        path="/",
        name="dash-flows",
        description=(
            "dash-flows — React Flow (@xyflow/react) node-graph components for "
            "Plotly Dash, with a glass-morphism theme, ELK layouts, and full "
            "Dash callback integration."
        ),
    )
    add_llms_routes(app, LLMSConfig(warn_missing_llms_doc=False))

# Build the shell after pages are registered so the navbar can list them.
from components.appshell import create_appshell  # noqa: E402  (import after app init)

app.layout = create_appshell(dash.page_registry.values())
server = app.server


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8560)
