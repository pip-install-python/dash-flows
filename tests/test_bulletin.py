"""The network bulletin — wired, or off, and never a comment.

NETWORK FILE: adapted from dash-documentation-boilerplate 1.2.4, where this
existed because the wiring had sat COMMENTED OUT in run.py for weeks against a
hub endpoint that was already serving. Nothing failed. `configure_bulletin` is
opt-in, so an unwired app makes no request at all and the viewer header renders
perfectly well on the package's built-in tips and an "No announcements." empty
state. The only symptom was an announcement that never appeared — which nobody
goes looking for.

The load-bearing test is the last one: commented-out wiring cannot define the
name it asserts on, so it fails the moment somebody comments it out again.
"""

from __future__ import annotations

import pytest

from conftest import REPO_ROOT


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    """conftest pins NETWORK_BULLETIN_URL to "" for the whole session; these
    tests set it themselves and must not leak it into the others."""
    monkeypatch.delenv("NETWORK_BULLETIN_URL", raising=False)
    monkeypatch.delenv("NETWORK_BULLETIN_TTL_S", raising=False)


def test_no_url_means_the_feature_is_simply_off():
    from lib import bulletin

    assert bulletin.url() is None
    assert bulletin.configure() is False


def test_configure_reports_that_it_wired(monkeypatch, app_module):
    """`app_module` is requested for the app_id assertion at the end: the
    identity this satellite announces to the hub is claimed by run.py's fork
    point, so a test that never boots the app would measure the byte-
    identical reporter's "boilerplate" fallback instead of what production
    sends."""
    from lib import bulletin

    monkeypatch.setenv("NETWORK_BULLETIN_URL", bulletin.HUB_BULLETIN_URL)

    seen = {}

    def fake_configure_bulletin(**kwargs):
        seen.update(kwargs)

    import dash_improve_my_llms

    monkeypatch.setattr(dash_improve_my_llms, "configure_bulletin",
                        fake_configure_bulletin)

    assert bulletin.configure() is True
    assert seen["url"] == bulletin.HUB_BULLETIN_URL
    assert seen["app_id"] == "flows"


def test_the_reporters_own_fallback_says_boilerplate_and_that_is_correct():
    """The byte-copy identity trap, pinned from the side people get wrong.

    `lib/satellite_reporter.py` is kept BYTE-IDENTICAL to the boilerplate's
    across the whole fleet — `shasum` against the template's copy is the
    acceptance check for every sync — so its unset fallback necessarily says
    "boilerplate", the TEMPLATE's directory key, on every fork. Three
    template-copied modules share that fallback while this fork's own
    `ad_client` says "flows", and an unset SATELLITE_APP_KEY would file this
    site's traffic under the template's hub row (found live on pannellum
    2026-08-21; this repo has its own contamination in the hub's history).

    Repairing the fallback here is the WRONG fix — it breaks the byte
    identity the fleet checks. The right fix is the fork point in run.py,
    pinned by the test below. This test exists so that anyone who "helpfully"
    edits the reporter to say "flows" fails here and reads why.
    """
    from lib import hub_client, satellite_reporter

    with_nothing_set = {}
    import os
    saved = {k: os.environ.pop(k, None) for k in ("SATELLITE_APP_KEY", "AD_APP_ID")}
    try:
        with_nothing_set["reporter"] = satellite_reporter.app_key()
        with_nothing_set["hub"] = hub_client.app_id()
    finally:
        for k, v in saved.items():
            if v is not None:
                os.environ[k] = v

    assert with_nothing_set["reporter"] == "boilerplate", (
        "the byte-identical reporter's fallback changed — either the file is "
        "no longer byte-identical to the template's (shasum it) or someone "
        "repaired the fallback instead of setting the run.py fork point"
    )
    assert with_nothing_set["hub"] == "boilerplate"


def test_run_py_claims_this_apps_identity_before_any_hub_facing_import():
    """THE FORK POINT. Read run.py's source, not the environment.

    An env-based assertion would pass on any developer machine that happens
    to export SATELLITE_APP_KEY, and on Render where the dashboard sets it —
    which is precisely the configuration whose absence this line exists to
    survive. So this reads the file: the `setdefault` must be there, must
    name this app, and must sit above the first hub-facing import.
    """
    import ast
    import pathlib

    source = pathlib.Path(__file__).resolve().parent.parent / "run.py"
    tree = ast.parse(source.read_text(encoding="utf-8"))

    claim_line = None
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Attribute) and func.attr == "setdefault"):
            continue
        if len(node.args) != 2:
            continue
        key, value = node.args
        if getattr(key, "value", None) == "SATELLITE_APP_KEY":
            assert getattr(value, "value", None) == "flows", (
                f"the fork point claims {value.value!r}, not 'flows' — this "
                "site's traffic would file under another app's hub row"
            )
            claim_line = node.lineno

    assert claim_line, (
        "run.py has no os.environ.setdefault(\"SATELLITE_APP_KEY\", \"flows\") "
        "— the byte-identical reporter would fall back to \"boilerplate\" and "
        "this site's traffic would land on the template's hub row"
    )

    first_hub_import = min(
        node.lineno
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for name in (
            [node.module or ""] if isinstance(node, ast.ImportFrom)
            else [a.name for a in node.names]
        )
        if "satellite_reporter" in name or "hub_client" in name
        or "bulletin" in name or "ad_client" in name
    )
    assert claim_line < first_hub_import, (
        f"the fork point is on line {claim_line}, below the first hub-facing "
        f"import on line {first_hub_import} — modules that read the key at "
        "import time would already have taken the fallback"
    )


def test_every_hub_surface_names_this_app_the_same_way(app_module):
    """One id on every hub surface, measured on the RUNNING app.

    Four modules present an identity to the hub and each carries its own
    fallback, so they can drift apart without anything failing — the symptom
    is a column on /admin/ad-board that does not line up with /traffic, which
    nobody reconciles. Requesting `app_module` is the point: this asserts the
    state after run.py's fork point has executed, which is the state the
    deployed process is actually in.
    """
    from lib import ad_client, bulletin, hub_client, satellite_reporter

    assert ad_client.APP_ID == "flows"
    assert satellite_reporter.app_key() == "flows"
    assert hub_client.app_id() == "flows"
    assert bulletin.app_id() == "flows"


def test_a_bad_ttl_falls_back_rather_than_crashing_the_boot(monkeypatch):
    from lib import bulletin

    monkeypatch.setenv("NETWORK_BULLETIN_TTL_S", "not-a-number")
    assert bulletin._ttl() == bulletin.DEFAULT_TTL_S
    monkeypatch.setenv("NETWORK_BULLETIN_TTL_S", "5")
    assert bulletin._ttl() == 60.0, "a too-short TTL would hammer the hub"


def test_run_py_wires_it_rather_than_leaving_it_commented_out():
    """The regression this file exists for.

    Commented-out wiring cannot define the name it asserts on, so requiring a
    real call here is what makes commenting it out fail loudly.
    """
    source = (REPO_ROOT / "run.py").read_text()
    live = "\n".join(
        line for line in source.splitlines() if not line.strip().startswith("#")
    )
    assert "bulletin.configure()" in live, (
        "run.py no longer calls bulletin.configure() outside a comment"
    )
