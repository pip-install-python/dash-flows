"""The control board's ledger — live per-page overrides over the declared tiers.

This template enforces access through :mod:`lib.access`, which resolves each
page's tier from three inputs, strongest claim first:

1. **An override written here** by ``/admin/control-board`` — the operator
   flipped a switch, and that decision wins.
2. **The page's frontmatter** (``tier:`` / ``llms_public:``), recorded in
   :mod:`lib.page_tiers` at registration.
3. **The deployment defaults** (``PAGE_DEFAULT_TIER`` / ``LLMS_PUBLIC_DEFAULT``)
   for every page that declared nothing.

The hub's network ceiling still applies ON TOP of whatever resolves locally —
an override can loosen a local declaration, never a network restriction.

This module deliberately does NOT enforce anything. It is a registry (what
pages exist, what they declared) plus an override store (what the board
wrote), and lib.access consults it per render — which is what makes a board
toggle apply on the next page load with no restart and no redeploy.

Overrides persist to ``PAGE_VISIBILITY_FILE`` (render.yaml points it at the
``/var/data`` disk). Two hard-won fleet lessons are built in rather than
hoped for:

* **Cross-worker reconciliation.** gunicorn runs more than one worker; a
  board toggle mutates ``_overrides`` only in the worker that served the
  POST. Every reader re-checks the store file's mtime (throttled to one
  ``os.stat``/second) so a toggle lands on all workers within ~1s — without
  this, an anonymous refresh of a just-published page was a coin flip
  decided by which worker answered (the leaflet pilot's live defect).
* **Loud persistence failure.** The store path env rode render.yaml without
  reaching the live service twice on the pilot host, silently resetting
  every toggle per deploy. Boot prints a warning when the env is unset OR
  when it points under ``/var/`` and that directory is not actually a
  mounted disk (an app can ``mkdir /var/data`` on the container filesystem
  and everything works — until the next deploy wipes it). Absence of the
  ``[visibility]`` warning in a deploy log is the acceptance check.
"""
from __future__ import annotations

import json
import logging
import os
import threading
import time
from pathlib import Path

from lib import page_tiers

logger = logging.getLogger(__name__)

TIERS = page_tiers.TIERS

_STORE_PATH = Path(os.environ.get("PAGE_VISIBILITY_FILE") or "page_visibility.json")
_lock = threading.Lock()

# endpoint -> {"visibility": tier, "llms_public": bool|None, "name": str}
# _defaults is registered at startup from frontmatter; _overrides is what the
# control board wrote and always wins.
_defaults: dict[str, dict] = {}
_overrides: dict[str, dict] = {}

_store_mtime_ns: int | None = None
_next_stat_at = 0.0
_STAT_INTERVAL_S = 1.0


def _load_overrides() -> None:
    global _overrides, _store_mtime_ns
    try:
        if _STORE_PATH.exists():
            # stat BEFORE read: a write landing between the two is picked up
            # by the next mtime check instead of being masked forever.
            stamp = _STORE_PATH.stat().st_mtime_ns
            loaded = json.loads(_STORE_PATH.read_text())
            _overrides = loaded if isinstance(loaded, dict) else {}
            _store_mtime_ns = stamp
    except Exception as exc:  # a corrupt file must not kill the app
        logger.error("%s unreadable (%s) — ignoring overrides", _STORE_PATH, exc)
        _overrides = {}


def _persist() -> None:
    """Write overrides to disk. Call while holding ``_lock``."""
    global _store_mtime_ns
    try:
        _STORE_PATH.write_text(json.dumps(_overrides, indent=2, sort_keys=True))
        # Record our own write's stamp so this worker doesn't re-read it.
        _store_mtime_ns = _STORE_PATH.stat().st_mtime_ns
    except Exception as exc:
        logger.error("Could not persist %s: %s", _STORE_PATH, exc)


def _maybe_reload() -> None:
    """Pick up another worker's board writes; no-op when nothing changed.

    Reload triggers ONLY on an observed mtime change of the store file: a
    missing file, a stat error, or an unchanged stamp all leave the
    in-memory dict alone — which is also what keeps tests that inject
    straight into ``_overrides`` (without touching the file) valid.
    """
    global _next_stat_at
    if time.monotonic() < _next_stat_at:
        return
    with _lock:
        if time.monotonic() < _next_stat_at:  # another thread just checked
            return
        _next_stat_at = time.monotonic() + _STAT_INTERVAL_S
        try:
            stamp = _STORE_PATH.stat().st_mtime_ns
        except OSError:
            return
        if stamp == _store_mtime_ns:
            return
        _load_overrides()


def _persistence_warning() -> None:
    """Loud when board toggles would not survive a redeploy.

    Two failure shapes, both observed live on the pilot host:

    * env unset → the store falls back to the app directory, which a Docker
      deploy replaces wholesale;
    * env set to a ``/var/...`` path whose top directory is NOT a mount —
      render.yaml declares the disk, but disks materialize only via a
      Blueprint sync or a dashboard add, and a bare ``mkdir`` on the
      container filesystem behaves identically until the next deploy.
    """
    configured = os.environ.get("PAGE_VISIBILITY_FILE")
    if not configured:
        print(
            "[visibility] WARNING: PAGE_VISIBILITY_FILE unset — control-board "
            "toggles are writing to the app directory and will NOT survive a "
            "redeploy. Set PAGE_VISIBILITY_FILE=/var/data/page_visibility.json "
            "on the service (render.yaml declares it, but only a Blueprint "
            "sync or a dashboard add makes it live)."
        )
        return
    path = Path(configured)
    if str(path).startswith("/var/"):
        anchor = Path("/") / path.parts[1] / path.parts[2] \
            if len(path.parts) > 2 else path.parent
        if not os.path.ismount(str(anchor)):
            print(
                f"[visibility] WARNING: {anchor} is not a mounted disk on "
                "this instance — the control-board store will vanish on the "
                "next deploy. Attach the render.yaml disk (Blueprint sync, "
                "or add it in the dashboard)."
            )


_load_overrides()
_persistence_warning()


# ---------------------------------------------------------------------------
# Registration + the board's model
# ---------------------------------------------------------------------------

def register_default(path: str, name: str, visibility: str | None = None,
                     llms_public: bool | None = None) -> None:
    """Called once per page at registration time (frontmatter defaults).

    ``visibility=None`` / ``llms_public=None`` mean "this page did not pin
    the axis" and fall through to lib.page_tiers: the tier resolves to what
    the network ledger recorded (``PAGE_DEFAULT_TIER`` is read there at
    registration, so an env flip takes effect on restart — this template's
    documented semantics), while ``llms_public`` resolves LIVE against
    ``LLMS_PUBLIC_DEFAULT`` at every lookup. Either way the board's rows show
    exactly what lib.access enforces.
    """
    tier = (visibility or "").strip().lower() or None
    if tier is not None and tier not in TIERS:
        logger.warning("Page %s: unknown visibility %r — treating as "
                       "undeclared", path, tier)
        tier = None
    _defaults[path] = {"visibility": tier, "llms_public": llms_public,
                       "name": name}


def pin_default(path: str, visibility: str) -> None:
    """Force a registered page's baseline tier; board rows follow.

    The funnel pins in run.py must land on BOTH ledgers or the board would
    display a tier the site does not enforce. An operator can still override
    the pin from the board — that is the point of an override.
    """
    if visibility not in TIERS:
        raise ValueError(f"unknown tier {visibility!r}")
    entry = _defaults.get(path)
    if entry is not None:
        entry["visibility"] = visibility


def get_settings(path: str) -> dict:
    """Baseline + override, unpinned axes resolved live — the BOARD's model.

    The resolver (lib.access) reads the override accessors below instead,
    because a merged value cannot say whether an operator chose it.
    """
    _maybe_reload()
    base = _defaults.get(path)
    if base is None:
        base = {"visibility": None, "llms_public": None, "name": path}
    merged = dict(base)
    merged.update(_overrides.get(path, {}))
    if merged.get("visibility") is None:
        merged["visibility"] = page_tiers.local_tier(path)
    if merged.get("llms_public") is None:
        merged["llms_public"] = page_tiers.get_llms_public(path)
    return merged


def controllable_pages() -> dict[str, dict]:
    """Every registered page with overrides applied — the board's rows."""
    return {path: get_settings(path) for path in sorted(_defaults)}


def override_count() -> int:
    """How many pages carry at least one board override (boot diagnostics)."""
    return len(_overrides)


# ---------------------------------------------------------------------------
# Overrides, read by lib.access
# ---------------------------------------------------------------------------
# Two accessors that answer None for "no override": an untouched page must
# fall through to its frontmatter registration in lib.page_tiers, not to
# this store's unknown-path default.

def tier_override(path: str) -> str | None:
    """The tier the control board wrote for ``path``, or None."""
    _maybe_reload()
    tier = (_overrides.get(path) or {}).get("visibility")
    return tier if tier in TIERS else None


def llms_public_override(path: str) -> bool | None:
    """The machine-surface switch the control board wrote, or None."""
    _maybe_reload()
    value = (_overrides.get(path) or {}).get("llms_public")
    return None if value is None else bool(value)


# ---------------------------------------------------------------------------
# Writers — the control board's callbacks
# ---------------------------------------------------------------------------

def set_visibility(path: str, tier: str) -> None:
    if tier not in TIERS:
        raise ValueError(f"unknown tier {tier!r}")
    with _lock:
        _overrides.setdefault(path, {})["visibility"] = tier
        _persist()


def set_llms_public(path: str, value: bool) -> None:
    with _lock:
        _overrides.setdefault(path, {})["llms_public"] = bool(value)
        _persist()
