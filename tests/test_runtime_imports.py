"""Every runtime import must be declared — the clean-image witness.

A fork of this template died in production on ``ModuleNotFoundError: No
module named 'PIL'``: the package arrived with half the scientific stack,
so every machine it was tested on already had it — suite green, boots
locally, dies in a clean image. And because Dash imports every page while
constructing the app, one undeclared import in one docs example took the
whole site down. "Works here" and "works in a clean image" are different
claims, and the gap is always a package someone installed by hand months
ago. The fix is not discipline — it is this test, which reads the code
instead of trusting the interpreter's search path.

The check walks every runtime module (``lib/``, ``pages/``,
``components/``, ``docs/``, ``run.py``) and asserts each absolute import
resolves in the environment CI actually installs (requirements.txt and
nothing else). Nesting is deliberately ignored: the fatal PIL import was
function-local, so "only check module-level imports" would have missed it.
Nesting does not predict whether an import can kill a boot.

Exemptions are earned, not asserted. Each one carries a companion check
below proving the condition that makes it safe still holds — a comment
explaining why a rule doesn't apply decays; a test doesn't.
"""

from __future__ import annotations

import ast
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNTIME_DIRS = ("lib", "pages", "components", "docs")
RUNTIME_ROOT_FILES = ("run.py",)

# Optional backends: DASH_BACKEND selects one at boot, so fastapi/quart and
# their dependencies are deliberately NOT in requirements.txt (they ship as
# commented extras lines). Two companion tests below enforce the two
# conditions that make this exemption safe.
OPTIONAL_BACKEND_MODULES = {
    "fastapi": "dash-improve-my-llms[fastapi] extra",
    "pydantic": "arrives with the fastapi extra",
    "starlette": "arrives with the fastapi extra",
    "quart": "dash-improve-my-llms[quart] extra",
    "hypercorn": "quart's server, arrives with the quart extra",
    "uvicorn": "fastapi's server, arrives with the fastapi extra",
}

# The two modules whose top-level imports NEED the exemption: they import
# fastapi/starlette unconditionally and are only ever imported behind a
# backend check. test_optional_backend_carriers_never_hoisted pins that.
CARRIER_MODULES = {"lib.asgi_routes", "lib.asgi_middleware"}


def _runtime_files():
    for d in RUNTIME_DIRS:
        yield from sorted((ROOT / d).rglob("*.py"))
    for f in RUNTIME_ROOT_FILES:
        yield ROOT / f


def _top_level_name(node: ast.AST) -> list[str]:
    if isinstance(node, ast.Import):
        return [alias.name.split(".")[0] for alias in node.names]
    if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
        return [node.module.split(".")[0]]
    return []


def _local_names() -> set[str]:
    names = {p.name for p in ROOT.iterdir() if p.is_dir()}
    names |= {p.stem for p in ROOT.glob("*.py")}
    return names


def test_every_runtime_import_is_declared_or_exempt():
    local = _local_names()
    stdlib = set(sys.stdlib_module_names)
    missing: list[str] = []
    checked: dict[str, bool] = {}

    for path in _runtime_files():
        if "__pycache__" in path.parts:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            for name in _top_level_name(node):
                if name in stdlib or name in local:
                    continue
                if name in OPTIONAL_BACKEND_MODULES:
                    continue
                if name not in checked:
                    try:
                        checked[name] = (
                            importlib.util.find_spec(name) is not None
                        )
                    except (ImportError, ValueError):
                        checked[name] = False
                if not checked[name]:
                    rel = path.relative_to(ROOT)
                    missing.append(f"{rel}:{node.lineno}: {name}")

    assert missing == [], (
        "Runtime imports that do not resolve in this environment. In CI this "
        "environment is exactly requirements.txt — an unresolvable import "
        "here is a boot-time ModuleNotFoundError in a clean image, even if "
        "it works on a dev machine that happens to have the package: "
        f"{missing}"
    )


def test_optional_backends_are_documented_in_requirements():
    """Condition 1 of the exemption: each optional backend the code can
    import must exist as a commented extras line where installs happen, so
    the operator flipping DASH_BACKEND finds the install step next to every
    other dependency instead of in a traceback.

    THIS REPO IS TWO THINGS, and the file this reads is the difference from
    the template: `requirements.txt` is the published COMPONENT LIBRARY's
    dependency set (dash alone — the wheel-purity job in CI proves it
    installs with nothing else), while `requirements-docs.txt` is the docs
    site's. The optional backends belong to the site, so they are documented
    there; asserting against requirements.txt would demand a docs-site
    dependency be advertised to every consumer of the pip package.
    """
    text = (ROOT / "requirements-docs.txt").read_text(encoding="utf-8")
    for extra in ("dash-improve-my-llms[fastapi]", "dash-improve-my-llms[quart]"):
        assert extra in text, (
            f"{extra} is not documented in requirements-docs.txt — the "
            "optional-backend import exemption in this file is only safe "
            "while the install path is written down where installs happen."
        )


def test_optional_backend_carriers_never_hoisted():
    """Condition 2 of the exemption: the modules that import fastapi and
    starlette unconditionally (the carriers) must never be imported at
    run.py's module body outside a conditional — that conditionality is
    the only thing keeping a Flask-backend boot alive without the
    optional packages installed."""
    tree = ast.parse((ROOT / "run.py").read_text(encoding="utf-8"))
    hoisted: list[str] = []
    for node in tree.body:  # module body only — nested/conditional is fine
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names: list[str] = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif node.level == 0 and node.module:
                names = [node.module]
            for name in names:
                if name in CARRIER_MODULES or (
                    name.split(".")[0] in OPTIONAL_BACKEND_MODULES
                ):
                    hoisted.append(f"run.py:{node.lineno}: {name}")
    assert hoisted == [], (
        "Optional-backend modules imported unconditionally at run.py's top "
        f"level — a Flask boot would die on them: {hoisted}"
    )


def test_runtime_code_never_imports_build_scripts():
    """scripts/ is excluded from the declared-imports walk because its
    tools (favicon and social-card generation) run at build time with
    out-of-band installs (Pillow). That exclusion is only safe while no
    runtime module reaches into scripts/ — the moment one does, its
    undeclared imports become boot-time imports."""
    offenders: list[str] = []
    for path in _runtime_files():
        if "__pycache__" in path.parts:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                if any(a.name.split(".")[0] == "scripts" for a in node.names):
                    offenders.append(f"{path.relative_to(ROOT)}:{node.lineno}")
            elif isinstance(node, ast.ImportFrom):
                if node.level == 0 and node.module and (
                    node.module.split(".")[0] == "scripts"
                ):
                    offenders.append(f"{path.relative_to(ROOT)}:{node.lineno}")
    assert offenders == [], (
        "Runtime code imports from scripts/ — build-time tools carry "
        f"undeclared dependencies by design: {offenders}"
    )
