"""
Satellite traffic reporter — hourly signed rollup POST to 2plot.ai.

The other half of ``lib/traffic_rollup``: this ships the numbers to the hub so
the owner-only ``/traffic`` dashboard can chart this app alongside the rest of
the network. Contract: ``2plotai/docs/network/satellite-analytics.md``.

    POST https://2plot.ai/api/satellite/traffic
    X-AI-Canvas-Timestamp: <unix seconds>
    X-AI-Canvas-Signature: HMAC_SHA256(CROSS_APP_WEBHOOK_SECRET, f"{ts}." + body)

Re-POSTing the same ``(app, date)`` overwrites at the hub, so reporting today
every hour just firms the day up. Two details make the numbers *accurate*
rather than merely present:

- **Yesterday is closed out.** The last report of a day lands before midnight,
  so it misses that day's final minutes. During the first hours of a new local
  day the reporter re-POSTs yesterday, which overwrites the stale row.
- **One reporter per deployment.** Web servers run several workers, each with
  its own thread. A lease file (flock + timestamp) means exactly one worker
  reports per interval instead of N racing duplicates.

Deployment caveat: the hub keeps the LAST report per (app, date), so the local
ledger wants a persistent disk. On an ephemeral filesystem a mid-day deploy
resets the ledger and the next report overwrites today's real total with
whatever has accumulated since the restart — point ``TRAFFIC_ANALYTICS_FILE``
at mounted storage to avoid it.

A second, lighter thread posts a **presence ping** — ``{app, active}`` to
``/api/satellite/active`` roughly every minute — so the hub's board can show
"who is on this satellite right now" without waiting for a rollup. Presence
is display-only and ephemeral by contract (the hub keeps it in memory with a
~3-minute TTL and never writes it to the event log); the daily rollup stays
the single source of the board's daily numbers. Every presence failure is
swallowed silently: a hub that predates the endpoint 404s, and a failed ping
is not an error worth waking anyone for.

Env:
    CROSS_APP_WEBHOOK_SECRET    shared HMAC secret (required — no secret, no
                                reporting; the app runs on unaffected)
    SATELLITE_APP_KEY           network directory key for this app (falls back
                                to AD_APP_ID, then "dev")
    SATELLITE_TRAFFIC_URL       override the hub endpoint (default 2plot.ai);
                                the presence URL derives from it
    SATELLITE_REPORT_INTERVAL_S seconds between reports (default 3600)
    SATELLITE_REPORT_DELAY_S    delay before the first report (default 90)
    SATELLITE_PRESENCE_INTERVAL_S  seconds between presence pings (default
                                60, floor 30 per the hub contract; 0 disables)
    SATELLITE_PRESENCE_URL      override the presence endpoint
"""
from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path

import requests

try:
    import fcntl
except ImportError:  # pragma: no cover — Windows dev boxes
    fcntl = None

logger = logging.getLogger(__name__)

DEFAULT_ENDPOINT = "https://2plot.ai/api/satellite/traffic"
DEFAULT_INTERVAL_S = 3600
PRESENCE_DEFAULT_INTERVAL_S = 60
# The hub contract's floor: "do not post faster than every 30s".
PRESENCE_FLOOR_S = 30
# Re-post yesterday during the first hours of a new day so its final,
# post-last-report hits are included.
CLOSEOUT_HOUR = 3


def endpoint() -> str:
    return os.getenv("SATELLITE_TRAFFIC_URL") or DEFAULT_ENDPOINT


def presence_endpoint() -> str:
    """Derived from the traffic endpoint so one URL override retargets both."""
    override = os.getenv("SATELLITE_PRESENCE_URL")
    if override:
        return override
    base = endpoint()
    if base.endswith("/traffic"):
        return base[: -len("/traffic")] + "/active"
    return base.rstrip("/") + "/active"


def app_key() -> str:
    """This app's key in the hub's network directory.

    Deliberately NOT chained to ``AD_APP_ID``, even though on THIS app the two
    now agree ("boilerplate" in both). A fork is free to use a long ad
    identifier against a short directory key — leaflet.2plot.dev runs
    ``AD_APP_ID=dash-leaflet2`` with directory key "leaflet" — and setting one
    for ads must never silently re-key its analytics series off the directory.
    The convergence here is a convenience, not a contract to lean on.

    Default is "boilerplate" (this template's own directory key). The
    "dev" key belongs to 2plot.dev (the pip-docs+ deployment) — apps
    cloned from this template MUST set SATELLITE_APP_KEY to their own
    directory key or their reports overwrite each other's rows.
    """
    return os.getenv("SATELLITE_APP_KEY") or "boilerplate"


def _secret() -> str | None:
    return os.getenv("CROSS_APP_WEBHOOK_SECRET") or None


def _interval() -> int:
    try:
        return max(60, int(os.getenv("SATELLITE_REPORT_INTERVAL_S",
                                     DEFAULT_INTERVAL_S)))
    except ValueError:
        return DEFAULT_INTERVAL_S


def _presence_interval() -> int:
    """Seconds between presence pings; 0 disables the thread entirely."""
    try:
        raw = int(os.getenv("SATELLITE_PRESENCE_INTERVAL_S",
                            PRESENCE_DEFAULT_INTERVAL_S))
    except ValueError:
        return PRESENCE_DEFAULT_INTERVAL_S
    if raw <= 0:
        return 0
    return max(PRESENCE_FLOOR_S, raw)


# ---------------------------------------------------------------- transport --


def _post_signed(url: str, payload: dict, ua_label: str,
                 secret: str | None = None, timeout: float = 10.0):
    """Sign and POST one payload. Returns ``(ok, detail)``; never raises."""
    secret = secret or _secret()
    if not secret:
        return False, "no CROSS_APP_WEBHOOK_SECRET"

    from lib.constants import internal_ua

    # The signature covers the EXACT bytes sent — serialise once, sign that.
    body = json.dumps(payload).encode()
    ts = str(int(time.time()))
    sig = hmac.new(secret.encode(), f"{ts}.".encode() + body,
                   hashlib.sha256).hexdigest()
    try:
        r = requests.post(
            url, data=body, timeout=timeout,
            headers={"Content-Type": "application/json",
                     "X-AI-Canvas-Timestamp": ts,
                     "X-AI-Canvas-Signature": sig,
                     # The internal-traffic contract's outbound half: without
                     # this the POST arrives at 2plot.ai as
                     # `python-requests/2.x` and the hub counts its own
                     # analytics pipeline as a bot visit, on every report,
                     # forever.
                     "User-Agent": internal_ua(ua_label)},
        )
    except Exception as e:
        return False, f"request failed: {e!r}"
    if r.status_code != 200:
        return False, f"HTTP {r.status_code}: {r.text[:200]}"
    return True, r.text[:200]


def post_rollup(payload: dict, secret: str | None = None, timeout: float = 10.0):
    """Sign and POST one rollup. Returns ``(ok, detail)``; never raises."""
    return _post_signed(endpoint(), payload, "traffic-reporter",
                        secret=secret, timeout=timeout)


# -------------------------------------------------------------------- lease --


def _lease_path() -> Path:
    from lib.analytics_tracker import analytics_path

    return analytics_path().with_name(".satellite_report.lease")


def _presence_lease_path() -> Path:
    from lib.analytics_tracker import analytics_path

    return analytics_path().with_name(".satellite_presence.lease")


def _claim(interval: int, path: Path | None = None) -> bool:
    """True for the one worker that should report this interval.

    The lease file holds the epoch of the last report. Whoever takes the lock
    and finds the lease stale claims it; everyone else backs off. Without
    ``fcntl`` (Windows) the lock is skipped — the timestamp check alone still
    prevents most duplicates, and duplicates are harmless anyway (the hub
    overwrites on (app, date)).
    """
    path = path or _lease_path()
    try:
        fh = open(path, "a+")
    except OSError:
        return True   # can't coordinate — better to report than to go silent
    try:
        if fcntl:
            fcntl.flock(fh, fcntl.LOCK_EX)
        fh.seek(0)
        try:
            last = float((fh.read() or "0").strip() or 0)
        except ValueError:
            last = 0.0
        now = time.time()
        # 0.9 slack: worker clocks drift apart by a few seconds, and a strict
        # comparison would let a slightly-early worker skip the whole hour.
        if now - last < interval * 0.9:
            return False
        fh.seek(0)
        fh.truncate()
        fh.write(str(now))
        fh.flush()
        return True
    except Exception:
        return True
    finally:
        try:
            if fcntl:
                fcntl.flock(fh, fcntl.LOCK_UN)
        finally:
            fh.close()


# ------------------------------------------------------------------ reports --


def build_payloads(app: str | None = None) -> list[dict]:
    """Today's rollup, plus yesterday's during the close-out window."""
    from lib.analytics_tracker import tracker
    from lib.traffic_rollup import daily_rollup, load_visits

    tracker.flush()          # include hits still sitting in the write buffer
    app = app or app_key()
    now = datetime.now()
    visits = load_visits()

    days = [now.date()]
    if now.hour < CLOSEOUT_HOUR:
        days.append((now - timedelta(days=1)).date())
    return [p for p in (daily_rollup(app, d, visits=visits) for d in days) if p]


def report_once(app: str | None = None, dry_run: bool = False) -> list[dict]:
    """Build and send the due rollups. Returns what was built (for logging)."""
    payloads = build_payloads(app)
    for payload in payloads:
        if dry_run:
            logger.info("[satellite-traffic] dry run: %s", payload)
            continue
        ok, detail = post_rollup(payload)
        if ok:
            logger.info("[satellite-traffic] reported %s %s — %s human / %s bot",
                        payload["app"], payload["date"],
                        payload["human_hits"], payload["bot_hits"])
        else:
            logger.warning("[satellite-traffic] report failed for %s %s — %s",
                           payload["app"], payload["date"], detail)
    return payloads


def _loop(interval: int, first_delay: float):
    time.sleep(first_delay)
    while True:
        try:
            if _claim(interval):
                report_once()
        except Exception:
            logger.exception("[satellite-traffic] reporter cycle failed")
        # Wake more often than the interval so the worker holding the lease can
        # change without the network losing an hour of reporting.
        time.sleep(max(60, interval / 4))


# ----------------------------------------------------------------- presence --


def build_presence_payload(app: str | None = None) -> dict:
    """``{app, active}`` — distinct human visitors inside the session window.

    The exact mirror of the hub's own "active now" count (its board derives
    the same number from its local sessions), honouring the one-measurement
    rule: same ledger, same session gap, same bot exclusion. Presence never
    carries hits/pages — those stay the rollup's job.
    """
    from lib.analytics_tracker import tracker
    from lib.traffic_rollup import SESSION_GAP_MIN, load_visits

    tracker.flush()
    cutoff = datetime.now() - timedelta(minutes=SESSION_GAP_MIN)
    active = {
        v["vkey"]
        for v in load_visits()
        if v.get("device_type") != "bot" and v["dt"] >= cutoff
    }
    return {"app": app or app_key(), "active": len(active)}


def _presence_loop(interval: int):
    # Short first delay: presence is the board's "it's alive" signal, so it
    # should appear well before the first rollup (which waits ~90s + build).
    time.sleep(20)
    while True:
        try:
            if _claim(interval, path=_presence_lease_path()):
                payload = build_presence_payload()
                ok, detail = _post_signed(presence_endpoint(), payload,
                                          "presence-beacon", timeout=5.0)
                if not ok:
                    # Silently, by contract: a hub that predates /active 404s
                    # here, and a missed ping self-heals on the next one.
                    logger.debug("[satellite-presence] %s", detail)
        except Exception:
            logger.debug("[satellite-presence] cycle failed", exc_info=True)
        # Wake at half the interval so the lease can move between workers
        # without the board seeing a gap longer than one TTL.
        time.sleep(max(15, interval / 2))


def start_reporter() -> bool:
    """Start the background reporter. No-op (and says so) without a secret."""
    if not _secret():
        print("[satellite-traffic] disabled — set CROSS_APP_WEBHOOK_SECRET "
              "to report traffic to 2plot.ai")
        return False
    interval = _interval()
    try:
        first_delay = float(os.getenv("SATELLITE_REPORT_DELAY_S", "90"))
    except ValueError:
        first_delay = 90.0
    threading.Thread(target=_loop, args=(interval, first_delay),
                     name="satellite-traffic-reporter", daemon=True).start()
    print(f"[satellite-traffic] reporting app='{app_key()}' to {endpoint()} "
          f"every {interval}s")

    presence_interval = _presence_interval()
    if presence_interval:
        threading.Thread(target=_presence_loop, args=(presence_interval,),
                         name="satellite-presence-beacon", daemon=True).start()
        print(f"[satellite-presence] pinging {presence_endpoint()} "
              f"every {presence_interval}s (0 disables)")
    return True


if __name__ == "__main__":   # python -m lib.satellite_reporter [--dry-run]
    import sys

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    dry = "--dry-run" in sys.argv
    built = report_once(dry_run=dry)
    if not built:
        print("no tracked hits for today — nothing to report")
    else:
        print(json.dumps(built, indent=2))
