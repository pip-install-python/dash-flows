"""The control board: override precedence, cross-worker reload, loud persistence.

Three fleet lessons pinned as tests, so no fork re-learns them live:

* an override written by the board WINS over frontmatter and the env
  defaults, and clears back to them when the file says so;
* a board toggle made by ANOTHER gunicorn worker lands here within one
  stat-throttle window (the leaflet pilot's coin-flip defect);
* a store that cannot survive a redeploy announces itself at boot
  (the twice-observed silent-reset class).
"""

import importlib
import json
import os
import time

import pytest

from lib import access, page_tiers, page_visibility


@pytest.fixture
def clean_store(monkeypatch):
    """Snapshot module state; leave no store file behind for later tests."""
    saved_overrides = {
        path: dict(entry) for path, entry in page_visibility._overrides.items()
    }
    saved_defaults = {
        path: dict(entry) for path, entry in page_visibility._defaults.items()
    }
    saved_stamp = page_visibility._store_mtime_ns
    saved_tiers = page_tiers.registered()
    saved_llms = dict(page_tiers._LOCAL_LLMS_PUBLIC)
    yield
    page_visibility._STORE_PATH.unlink(missing_ok=True)
    page_visibility._overrides.clear()
    page_visibility._overrides.update(saved_overrides)
    page_visibility._defaults.clear()
    page_visibility._defaults.update(saved_defaults)
    page_visibility._store_mtime_ns = saved_stamp
    page_visibility._next_stat_at = 0.0
    page_tiers._LOCAL_TIERS.clear()
    page_tiers._LOCAL_TIERS.update(saved_tiers)
    page_tiers._LOCAL_LLMS_PUBLIC.clear()
    page_tiers._LOCAL_LLMS_PUBLIC.update(saved_llms)


def _foreign_write(payload: dict) -> None:
    """A write by 'another worker': same file, not through this module."""
    path = page_visibility._STORE_PATH
    path.write_text(json.dumps(payload))
    stamp = time.time_ns()
    os.utime(path, ns=(stamp, stamp))  # guarantee the mtime actually moves


# ---------------------------------------------------------------------------
# Override precedence — the resolver half
# ---------------------------------------------------------------------------

def test_a_board_override_beats_frontmatter(clean_store):
    page_tiers.register("/cb-page", "public")
    page_visibility.register_default("/cb-page", "CB Page",
                                     visibility="public")
    assert access.local_tier("/cb-page") == "public"

    page_visibility.set_visibility("/cb-page", "auth")
    assert access.local_tier("/cb-page") == "auth"


def test_a_board_override_beats_the_env_default(clean_store, monkeypatch):
    """The live-toggle promise: publish a page while PAGE_DEFAULT_TIER=auth."""
    monkeypatch.setenv("PAGE_DEFAULT_TIER", "auth")
    page_tiers.register("/cb-gated", None)  # undeclared → env default
    page_visibility.register_default("/cb-gated", "CB Gated")
    assert access.local_tier("/cb-gated") == "auth"

    page_visibility.set_visibility("/cb-gated", "public")
    assert access.local_tier("/cb-gated") == "public"


def test_llms_override_follows_the_same_precedence(clean_store):
    page_tiers.register("/cb-page", "auth")  # axis unpinned → default open
    page_visibility.register_default("/cb-page", "CB Page", visibility="auth")
    assert access.llms_public("/cb-page") is True

    page_visibility.set_llms_public("/cb-page", False)
    assert access.llms_public("/cb-page") is False


def test_an_untouched_page_falls_through_to_the_network_ledger(
        clean_store, monkeypatch):
    """Board rows must show what lib.access ENFORCES for an untouched page.

    In this template the tier env resolves at registration (an env flip
    takes a restart — run.py's documented semantics), so the board must
    mirror page_tiers' resolved value, not re-read the env itself.
    """
    monkeypatch.setenv("PAGE_DEFAULT_TIER", "auth")
    page_tiers.register("/cb-undeclared", None)  # resolves NOW, to auth
    page_visibility.register_default("/cb-undeclared", "Undeclared")
    monkeypatch.setenv("PAGE_DEFAULT_TIER", "public")  # later flip, no restart
    assert page_visibility.get_settings("/cb-undeclared")["visibility"] == "auth"
    assert access.local_tier("/cb-undeclared") == "auth"  # board == enforcement


# ---------------------------------------------------------------------------
# Cross-worker reload
# ---------------------------------------------------------------------------

def test_a_foreign_workers_toggle_is_picked_up(clean_store):
    _foreign_write({"/cb-canary": {"visibility": "public"}})
    page_visibility._next_stat_at = 0.0  # skip the 1s stat throttle

    assert page_visibility.tier_override("/cb-canary") == "public"


def test_a_second_foreign_write_supersedes_the_first(clean_store):
    _foreign_write({"/cb-canary": {"visibility": "public"}})
    page_visibility._next_stat_at = 0.0
    assert page_visibility.tier_override("/cb-canary") == "public"

    _foreign_write({"/cb-canary": {"visibility": "auth",
                                   "llms_public": False}})
    page_visibility._next_stat_at = 0.0
    assert page_visibility.tier_override("/cb-canary") == "auth"
    assert page_visibility.llms_public_override("/cb-canary") is False


def test_direct_injection_survives_when_the_file_never_moves(clean_store):
    """The suite-wide convention: tests may write ``_overrides`` directly."""
    page_visibility._STORE_PATH.unlink(missing_ok=True)
    page_visibility._overrides["/cb-injected"] = {"visibility": "hidden"}
    page_visibility._next_stat_at = 0.0

    assert page_visibility.tier_override("/cb-injected") == "hidden"


def test_own_persist_does_not_bounce_back(clean_store):
    page_visibility.set_visibility("/cb-canary", "public")
    page_visibility._overrides["/cb-injected"] = {"visibility": "hidden"}
    page_visibility._next_stat_at = 0.0

    assert page_visibility.tier_override("/cb-injected") == "hidden"
    assert page_visibility.tier_override("/cb-canary") == "public"


# ---------------------------------------------------------------------------
# Loud persistence
# ---------------------------------------------------------------------------

def test_persistence_warning_fires_when_the_env_is_unset(monkeypatch, capsys):
    monkeypatch.delenv("PAGE_VISIBILITY_FILE", raising=False)
    page_visibility._persistence_warning()
    assert "will NOT survive a redeploy" in capsys.readouterr().out


def test_persistence_warning_fires_when_var_data_is_not_a_mount(
        monkeypatch, capsys):
    monkeypatch.setenv("PAGE_VISIBILITY_FILE",
                       "/var/data/page_visibility.json")
    monkeypatch.setattr(os.path, "ismount", lambda _p: False)
    page_visibility._persistence_warning()
    assert "not a mounted disk" in capsys.readouterr().out


def test_persistence_warning_is_silent_when_the_disk_is_real(
        monkeypatch, capsys):
    monkeypatch.setenv("PAGE_VISIBILITY_FILE",
                       "/var/data/page_visibility.json")
    monkeypatch.setattr(os.path, "ismount", lambda _p: True)
    page_visibility._persistence_warning()
    assert capsys.readouterr().out == ""


# ---------------------------------------------------------------------------
# The board page itself
# ---------------------------------------------------------------------------

def _board_module():
    """Import the board page, standing up a bare Dash app if none exists.

    ``dash.register_page`` refuses to run before app instantiation;
    ``pages_folder=""`` keeps the throwaway app from importing the whole
    docs tree.
    """
    import dash

    try:
        return importlib.import_module("pages.control_board")
    except dash.exceptions.PageError:
        dash.Dash(__name__, use_pages=True, pages_folder="")
        return importlib.import_module("pages.control_board")


def test_the_board_fails_closed_without_clerk(clean_store, monkeypatch):
    """No Clerk and no ALLOW_UNGATED_ADMIN → the 404-style card, never rows."""
    control_board = _board_module()
    monkeypatch.delenv("ALLOW_UNGATED_ADMIN", raising=False)
    rendered = control_board.layout()
    assert "cb-feedback" not in str(rendered)


def test_the_board_opens_locally_with_the_dev_override(clean_store, monkeypatch):
    control_board = _board_module()
    monkeypatch.setenv("ALLOW_UNGATED_ADMIN", "1")
    page_tiers.register("/cb-page", "public")
    page_visibility.register_default("/cb-page", "CB Page",
                                     visibility="public")
    rendered = str(control_board.layout())
    assert "cb-feedback" in rendered
    assert "/cb-page" in rendered


def test_the_board_stays_out_of_both_ledgers(clean_store):
    """The board's gate is its own fail-closed layout(), NOT a tier entry.

    Registering it `hidden` in lib.page_tiers would flip
    ``access.gating_configured()`` on for EVERY fork — including all-public
    sites — and the template's contract is that the per-request machine
    check stays off until a real tier says otherwise. No ledger entry is
    needed for safety: no prose is ever registered for this path, so the
    llms.txt family and the sitemap have nothing to serve.
    """
    # No reload: Dash's page loader imports this module without its parent
    # package, so importlib.reload breaks under the full app. Every
    # assertion here is an ABSENCE invariant, valid however the module was
    # loaded.
    _board_module()
    assert "/admin/control-board" not in page_tiers.registered()
    assert "/admin/control-board" not in page_visibility.controllable_pages()

    # The machine surfaces are silenced package-side instead — sitemap,
    # llms.txt, MCP, prerender, crawler HTML all treat the board as absent.
    from dash_improve_my_llms import is_hidden
    assert is_hidden("/admin/control-board")
