"""run.py must wire BOTH halves of dash-clerk-auth — the flexlayout class.

dash-clerk-auth splits its setup either side of ``Dash(...)``:
``register()`` loads the UI half (components, ClerkJS, appearance) and
``configure_app(app)`` registers the server half (``/api/auth/session``,
``/api/auth/signout``, the per-request identity population).

flexlayout shipped its batch-2 pass (2026-08-22) with the first call and
WITHOUT the second: every component rendered and ClerkJS reported
signed-in, while every server render read signed-out — the control board
served the owner the sign-in card forever, ``POST /api/auth/session``
answered 405 (the path fell through to Dash's GET-only page catch-all),
and sign-out never revoked. No suite could see it: Clerk is off in test
environments, and ``configure_app`` no-ops without keys, so the missing
call was indistinguishable from the deliberate no-op.

This pin is therefore STRUCTURAL — the wiring calls must exist in run.py
regardless of environment. The runtime half of the guard lives in
``scripts/smoke_live.py`` ("Auth wiring"), which proves the routes
actually answer on the deployed host.
"""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_CALLS = ("register", "configure_app")


def _module_aliases(tree: ast.Module) -> set[str]:
    """Names that ``lib.auth`` is bound to in run.py (e.g. ``_auth``)."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "lib":
            for alias in node.names:
                if alias.name == "auth":
                    names.add(alias.asname or alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "lib.auth":
                    names.add((alias.asname or alias.name).split(".")[0])
    return names


def test_run_py_calls_both_auth_wiring_halves():
    tree = ast.parse((ROOT / "run.py").read_text(encoding="utf-8"))
    aliases = _module_aliases(tree)
    assert aliases, (
        "run.py never imports lib.auth as a module — the auth stack is "
        "entirely unwired"
    )

    called: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            base = node.func.value
            if isinstance(base, ast.Name) and base.id in aliases:
                called.add(node.func.attr)

    for required in REQUIRED_CALLS:
        assert required in called, (
            f"run.py never calls {sorted(aliases)[0]}.{required}() — "
            "components without the server half (or vice versa): the site "
            "LOOKS signed in while every server render reads signed-out, "
            "auth POSTs answer 405 via the page catch-all, and sign-out "
            "never revokes. Both calls are required; see this file's "
            "docstring for the incident."
        )
