"""Every auth-gate demo entry resolves — on THIS site, loudly.

`build_demo` swallows import failures BY DESIGN (a broken example must never
take down the sign-in funnel), and its warning only fires when that
endpoint's card actually renders — which never happens when the endpoint is
not a page here at all. That combination made a dead entry perfectly silent:
every fork inherited the template's entry, it resolved on none of them, and
their gate cards rendered demo-less from fork time without a line of log
(batch-1 finding, excalidraw, 2026-08-25). This file is the one surface
where a dead entry is loud.

Byte-verbatim across the fleet: it sweeps THIS repo's DEMOS table against
THIS repo's page registry, so the same bytes hold everywhere. The entries
themselves are site judgment (swap in your own hero example) — an EMPTY
table passes; a dead entry never does.
"""

from __future__ import annotations

import importlib

from lib.auth_demos import DEMOS


def test_every_demo_endpoint_is_a_registered_page(app_module):
    import dash

    registered = {entry["path"] for entry in dash.page_registry.values()}
    dead = sorted(set(DEMOS) - registered)
    assert dead == [], (
        f"DEMOS endpoints that are not pages on this site: {dead} — "
        "a card that never renders can never surface its own broken demo"
    )


def test_every_demo_module_imports_and_exposes_component(app_module):
    # import_module is exactly what build_demo does in production; app_module
    # first, because the example modules assume the app (and the docs pass
    # that imports them at startup) already exists.
    problems = []
    for path, spec in sorted(DEMOS.items()):
        try:
            module = importlib.import_module(spec["module"])
        except Exception as e:
            problems.append(f"{path}: {spec['module']} failed to import ({e})")
            continue
        if not hasattr(module, "component"):
            problems.append(
                f"{path}: {spec['module']} has no module-level `component`"
            )
    assert problems == [], "; ".join(problems)
