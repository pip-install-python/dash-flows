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


def test_configure_reports_that_it_wired(monkeypatch):
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


def test_the_app_id_is_the_directory_key_not_a_second_opinion():
    """One id on every hub surface. A satellite still announcing itself as
    "boilerplate" would receive the template's announcements."""
    from lib import bulletin
    from lib.satellite_reporter import app_key

    assert bulletin.app_id() == app_key() == "flows"


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
