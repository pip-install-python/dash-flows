"""2plot.ai satellite analytics — hourly signed traffic rollup.

Drop-in module for every satellite documentation app (dash-flows,
dash-email, dash-mui-scheduler, dash-mui-charts, ...), the traffic
counterpart of ``lib/ad_client.py``. It makes this app show up on the
owner-only ``/traffic`` dashboard at 2plot.ai with numbers that mean the
same thing as every other app's.

The contract it implements is 2plot.ai's ``docs/satellite-analytics.md``:

    POST https://2plot.ai/api/satellite/traffic
    X-AI-Canvas-Timestamp: <unix seconds>
    X-AI-Canvas-Signature: HMAC_SHA256(CROSS_APP_WEBHOOK_SECRET,
                                       f"{ts}." + raw_body)

    {"app", "date", "human_hits", "bot_hits",            # v1 (required)
     "visitors", "sessions", "median_session_s",         # v2 (optional)
     "pages": [{"path", "hits"}], "countries": {CC: n}}

Accuracy notes — why this is more than a counter:

* **Definitions are copied from the hub**, not invented: the bot-UA list,
  the skip list, the ``ip|md5(ua)[:8]`` visitor key, the 30-minute
  session gap and the "median of MULTI-page sessions only" rule all
  mirror ``lib/traffic_insights.py`` + ``lib/pulse/network_jobs.py`` on
  2plot.ai, so /traffic compares this app against the hub fairly.
* **SPA navigations are counted.** A Dash multi-page app serves ONE HTML
  request per visit; every later page is a client-side route change that
  never hits the server. Counting only requests would report every
  session as single-page — ``pages`` would list entry pages only and
  ``median_session_s`` would always be null. So the browser beacons each
  route change to ``/api/pageview`` (same origin, ``keepalive``), and
  those views join the ledger. Bots don't run JS, so bot hits stay
  request-only, which is correct.
* **Hits survive a restart.** Hits append to a JSONL ledger
  (``SATELLITE_ANALYTICS_FILE``), not to process memory. Re-POSTing an
  (app, date) OVERWRITES at the hub, so a process that restarted with an
  empty counter would erase the day's real numbers.
* **One POST per interval across workers.** gunicorn runs 2+ workers,
  each with its own reporter thread reading the same ledger; an
  ``O_EXCL`` claim file elects one poster per interval.

Env:
    CROSS_APP_WEBHOOK_SECRET   shared HMAC secret (no secret → dormant)
    SATELLITE_APP_ID           network key for this app (default: AD_APP_ID
                               or "dash-flows")
    SATELLITE_HUB_URL          hub origin (default https://2plot.ai)
    SATELLITE_ANALYTICS_FILE   ledger path (default ./satellite_traffic.jsonl)
    SATELLITE_REPORT_INTERVAL_S  min seconds between POSTs (default 1800)
    SATELLITE_ANALYTICS_DRY_RUN  "1" → track + log rollups, never POST

Failure behaviour: every entry point is wrapped — analytics must never
break a page view, and a hub outage costs one connect timeout per
interval in a background thread.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import threading
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

try:
    # MUST be module level: with `from __future__ import annotations` the
    # FastAPI handler's `request: Request` hint stays a string that FastAPI
    # resolves against THIS module's globals. Imported inside a function it
    # would be unresolvable and FastAPI would treat `request` as a required
    # query param — every beacon would 422. (Same trap the hub documents in
    # lib/satellite_ingest.py.)
    from starlette.requests import Request
except ImportError:  # flask/quart-only install — the fastapi branch never runs
    Request = Any  # type: ignore[misc,assignment]

logger = logging.getLogger(__name__)

HUB_URL = (os.environ.get("SATELLITE_HUB_URL") or "https://2plot.ai").rstrip("/")
# "flows" is this app's 2plot network-directory key (lib/network_directory
# in the 2plotai repo) — the hub health-sweeps it and gives its series a
# named label + color. Do NOT fall back to AD_APP_ID: the ad network uses
# longer identifiers that are not directory keys.
APP_ID = os.environ.get("SATELLITE_APP_ID") or "flows"
LEDGER = Path(os.environ.get("SATELLITE_ANALYTICS_FILE")
              or "satellite_traffic.jsonl")

# The contract asks for hourly (minimum daily). We default to every 30
# minutes AND only POST when the numbers actually changed: free-tier
# containers sleep after ~15 min idle and lose the ledger, so a shorter
# window halves what an eviction can swallow, while the "only if changed"
# gate keeps an idle day at zero POSTs (each report writes a line in the
# hub's pulse feed, so silence matters).
REPORT_INTERVAL_S = int(os.environ.get("SATELLITE_REPORT_INTERVAL_S") or 1800)
DRY_RUN = (os.environ.get("SATELLITE_ANALYTICS_DRY_RUN") or "").strip() in ("1", "true", "yes")

SESSION_GAP_S = 30 * 60      # the hub's session rule — keep it so numbers compare
RETENTION_DAYS = 3           # today + yesterday are reportable; one day of slack
DEDUPE_S = 2.0               # same (visitor, path) inside 2s = one view
POST_TIMEOUT_S = 10
_MAX_PATH = 160

# Bot user-agents, copied from 2plot.ai lib/traffic_insights.py so a
# crawler is classified identically on both sides of the network.
_BOT_PATTERNS = (
    'gptbot', 'chatgpt-user', 'chatgpt', 'oai-searchbot', 'claudebot', 'claude-web',
    'claude', 'anthropic', 'perplexitybot', 'youbot', 'google-extended', 'googlebot',
    'bingbot', 'duckduckbot', 'slurp', 'yandex', 'baidu', 'ccbot', 'facebookbot',
    'python-requests', 'curl', 'wget', 'scraper', 'spider', 'crawler', 'bot',
)

# Paths that are not page views: static assets, Dash plumbing, machine
# endpoints. Mirrors the hub's _SKIP plus this app's own routes.
_SKIP = (
    '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.webp',
    '.woff', '.woff2', '.ttf', '.eot', '.map', '.txt', '.xml',
    '_dash', '_reload-hash', 'favicon', '/assets/', '[]',
    '/healthz', '/api/', '/llms', '/sitemap', '/robots',
)

_write_lock = threading.Lock()
_recent: dict[tuple[str, str], float] = {}
_reporter_started = False


# --------------------------------------------------------------------------
# Enablement
# --------------------------------------------------------------------------

def _secret() -> str | None:
    return os.environ.get("CROSS_APP_WEBHOOK_SECRET") or None


def enabled() -> bool:
    """Track only when we could actually report (or are dry-running)."""
    return bool(_secret()) or DRY_RUN


# --------------------------------------------------------------------------
# Request classification
# --------------------------------------------------------------------------

def is_bot(user_agent: str | None) -> bool:
    ua = (user_agent or "").lower()
    return any(p in ua for p in _BOT_PATTERNS)


def should_skip(path: str | None) -> bool:
    if not path or not path.startswith('/') or path.startswith('//'):
        return True
    return any(s in path for s in _SKIP)


def client_ip(headers: dict, remote_addr: str | None = None) -> str | None:
    """Real client address behind Cloudflare / Render's proxy."""
    lc = {k.lower(): v for k, v in headers.items()}
    cf = lc.get("cf-connecting-ip")
    if cf:
        return cf.strip()
    xff = lc.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    return remote_addr


def client_country(headers: dict) -> str | None:
    """ISO country from Cloudflare's free header — no geo-IP lookup, no
    latency added to a page view. Absent (or XX/T1 for anonymised
    traffic) → the rollup simply omits the visitor from `countries`."""
    lc = {k.lower(): v for k, v in headers.items()}
    cc = (lc.get("cf-ipcountry") or "").strip().upper()
    return cc if cc and cc not in ("XX", "T1") else None


def visitor_key(ip: str | None, user_agent: str | None) -> str:
    """The hub's identity rule: ip | first 8 hex of md5(user-agent)."""
    ua = hashlib.md5((user_agent or "?").encode()).hexdigest()[:8]
    return f"{ip or '?'}|{ua}"


# --------------------------------------------------------------------------
# Ledger
# --------------------------------------------------------------------------

def track(path: str | None, user_agent: str | None, ip: str | None = None,
          country: str | None = None) -> None:
    """Append one page view. Never raises."""
    try:
        if not enabled() or should_skip(path):
            return
        path = path.split('?', 1)[0][:_MAX_PATH]
        vkey = visitor_key(ip, user_agent)
        now = time.time()
        key = (vkey, path)
        with _write_lock:
            # Per-process dedupe: a hard load whose beacon also fires, or a
            # double-submitted request, is one view. (Cross-worker dupes are
            # not possible in practice — the beacon skips the entry page.)
            last = _recent.get(key)
            if last is not None and now - last < DEDUPE_S:
                return
            _recent[key] = now
            if len(_recent) > 4096:
                cutoff = now - 60
                for k in [k for k, t in _recent.items() if t < cutoff]:
                    _recent.pop(k, None)
            row = {"t": round(now, 3), "p": path, "v": vkey,
                   "b": 1 if is_bot(user_agent) else 0}
            if country:
                row["c"] = country
            with open(LEDGER, "a") as fh:
                fh.write(json.dumps(row, separators=(",", ":")) + "\n")
    except Exception:  # noqa: BLE001 — analytics never breaks a request
        logger.debug("track failed", exc_info=True)


def _load_hits() -> list[dict]:
    """Every retained hit, chronological, with a UTC date stamp."""
    out: list[dict] = []
    try:
        with open(LEDGER) as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                    row["d"] = datetime.fromtimestamp(
                        row["t"], timezone.utc).strftime("%Y-%m-%d")
                except Exception:
                    continue
                out.append(row)
    except FileNotFoundError:
        return []
    except Exception:
        logger.debug("ledger read failed", exc_info=True)
        return []
    out.sort(key=lambda r: r["t"])
    return out


def _prune(hits: list[dict]) -> None:
    """Rewrite the ledger without hits older than RETENTION_DAYS.

    Called only by the worker holding the interval claim, and only when
    there is something to drop, so the append/rewrite race window is
    entered at most once a day.
    """
    cutoff = time.time() - RETENTION_DAYS * 86400
    keep = [r for r in hits if r["t"] >= cutoff]
    if len(keep) == len(hits):
        return
    tmp = LEDGER.with_suffix(LEDGER.suffix + ".tmp")
    try:
        with _write_lock, open(tmp, "w") as fh:
            for r in keep:
                fh.write(json.dumps({k: v for k, v in r.items() if k != "d"},
                                    separators=(",", ":")) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, LEDGER)
    except Exception:
        logger.debug("ledger prune failed", exc_info=True)


# --------------------------------------------------------------------------
# Rollup — the hub's own definitions, applied to this app's ledger
# --------------------------------------------------------------------------

def _sessions(hits: list[dict]) -> list[tuple[int, float]]:
    """(hit count, first→last seconds) per session, 30-minute gap rule."""
    by_visitor: dict[str, list[dict]] = {}
    for h in hits:
        by_visitor.setdefault(h["v"], []).append(h)
    sessions: list[tuple[int, float]] = []
    for rows in by_visitor.values():
        rows.sort(key=lambda r: r["t"])
        cur = [rows[0]]
        for r in rows[1:]:
            if r["t"] - cur[-1]["t"] > SESSION_GAP_S:
                sessions.append((len(cur), cur[-1]["t"] - cur[0]["t"]))
                cur = [r]
            else:
                cur.append(r)
        sessions.append((len(cur), cur[-1]["t"] - cur[0]["t"]))
    return sessions


def _dedupe(hits: list[dict]) -> list[dict]:
    """Collapse the same (visitor, path) seen twice within DEDUPE_S.

    :func:`track` already does this per process, but gunicorn runs several
    workers — a request and its beacon can land in different ones. Hits
    are chronological here, so one last-seen map finishes the job for the
    whole app.
    """
    seen: dict[tuple[str, str], float] = {}
    out = []
    for h in hits:
        key = (h["v"], h["p"])
        if h["t"] - seen.get(key, -1e9) < DEDUPE_S:
            continue
        seen[key] = h["t"]
        out.append(h)
    return out


def rollup(date: str, hits: list[dict] | None = None) -> dict | None:
    """The full v1+v2 payload for one UTC day, or None if nothing happened."""
    day = _dedupe([h for h in (hits if hits is not None else _load_hits())
                   if h["d"] == date])
    if not day:
        return None
    humans = [h for h in day if not h.get("b")]

    sessions = _sessions(humans)
    # Median of MULTI-page sessions only — a one-hit visit has no measurable
    # duration, and padding zeros in would drag every app's median to 0.
    multi = sorted(dur for n, dur in sessions if n > 1)

    pages: dict[str, int] = {}
    countries: dict[str, int] = {}
    for h in humans:
        pages[h["p"]] = pages.get(h["p"], 0) + 1
        if h.get("c"):
            countries[h["c"]] = countries.get(h["c"], 0) + 1

    payload = {
        "app": APP_ID,
        "date": date,
        "human_hits": len(humans),
        "bot_hits": len(day) - len(humans),
        "visitors": len({h["v"] for h in humans}),
        "sessions": len(sessions),
        "median_session_s": (round(multi[len(multi) // 2], 1) if multi else None),
        "pages": [{"path": p, "hits": n}
                  for p, n in sorted(pages.items(), key=lambda kv: -kv[1])[:20]],
    }
    if countries:
        payload["countries"] = dict(
            sorted(countries.items(), key=lambda kv: -kv[1])[:20])
    return payload


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------

def post_rollup(payload: dict) -> bool:
    """Sign and POST one rollup. Returns True on a 2xx from the hub."""
    secret = _secret()
    if DRY_RUN or not secret:
        logger.info("[satellite-analytics] dry-run rollup: %s",
                    json.dumps(payload, separators=(",", ":")))
        return bool(DRY_RUN)
    import requests

    body = json.dumps(payload, separators=(",", ":")).encode()
    ts = str(int(time.time()))
    sig = hmac.new(secret.encode(), f"{ts}.".encode() + body,
                   hashlib.sha256).hexdigest()
    try:
        resp = requests.post(
            f"{HUB_URL}/api/satellite/traffic", data=body,
            headers={"Content-Type": "application/json",
                     "X-AI-Canvas-Timestamp": ts,
                     "X-AI-Canvas-Signature": sig},
            timeout=POST_TIMEOUT_S,
        )
        if resp.status_code == 200:
            logger.info("[satellite-analytics] reported %s %s: %s human / %s bot",
                        APP_ID, payload["date"], payload["human_hits"],
                        payload["bot_hits"])
            return True
        logger.warning("[satellite-analytics] hub rejected %s: %s %s",
                       payload["date"], resp.status_code, resp.text[:200])
    except Exception as exc:  # noqa: BLE001 — a hub outage is not our problem
        logger.warning("[satellite-analytics] report failed: %s", exc)
    return False


def _claim(bucket: int) -> bool:
    """Elect ONE gunicorn worker to post for this interval bucket."""
    claim = LEDGER.with_name(f".{LEDGER.name}.claim-{bucket}")
    try:
        fd = os.open(str(claim), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        os.close(fd)
    except FileExistsError:
        return False
    except Exception:
        return True  # unwritable dir (read-only fs): don't silence reporting
    # Sweep claims older than a day; cheap, and keeps the dir tidy.
    try:
        for old in claim.parent.glob(f".{LEDGER.name}.claim-*"):
            if old != claim and time.time() - old.stat().st_mtime > 86400:
                old.unlink(missing_ok=True)
    except Exception:
        pass
    return True


# Hit count last successfully reported per date — the "did anything
# change?" gate. Process-local: a restart just re-POSTs, and the hub
# overwrites on (app, date), so a duplicate is harmless.
_reported: dict[str, int] = {}


def report_now(force: bool = False) -> list[str]:
    """POST today's rollup (and yesterday's, once it stops changing).

    Yesterday is included so the tail of a day — everything after its last
    in-day report — still lands. Returns the dates actually POSTed.
    """
    hits = _load_hits()
    now = datetime.now(timezone.utc)
    dates = [now.strftime("%Y-%m-%d"),
             (now - timedelta(days=1)).strftime("%Y-%m-%d")]
    posted: list[str] = []
    for date in dates:
        payload = rollup(date, hits)
        if not payload:
            continue
        total = payload["human_hits"] + payload["bot_hits"]
        if not force and _reported.get(date) == total:
            continue  # nothing new since the last report
        if post_rollup(payload):
            _reported[date] = total
            posted.append(date)
    return posted


def _reporter_loop() -> None:
    # A first pass shortly after boot picks up a ledger left behind by a
    # restart before the process can be evicted again.
    time.sleep(60)
    while True:
        try:
            bucket = int(time.time() // REPORT_INTERVAL_S)
            if _claim(bucket):
                hits = _load_hits()
                if hits:
                    report_now()
                    _prune(hits)
        except Exception:
            logger.exception("[satellite-analytics] reporter cycle failed")
        time.sleep(max(60, REPORT_INTERVAL_S))


def start_reporter() -> bool:
    """Start the background reporter once per process."""
    global _reporter_started
    if _reporter_started or not enabled():
        return False
    # Flask's dev reloader runs two processes; only the reloaded child serves.
    if os.environ.get("WERKZEUG_RUN_MAIN") == "false":
        return False
    _reporter_started = True
    threading.Thread(target=_reporter_loop, name="satellite-analytics",
                     daemon=True).start()
    return True


# --------------------------------------------------------------------------
# Wiring
# --------------------------------------------------------------------------

def _track_from(headers: dict, path: str, remote_addr: str | None) -> None:
    ua = {k.lower(): v for k, v in headers.items()}.get("user-agent", "")
    track(path, ua, client_ip(headers, remote_addr), client_country(headers))


def _pageview_path(raw: bytes) -> str | None:
    """The path out of a beacon body — `{"path": "/docs/nodes"}`."""
    try:
        path = json.loads(raw or b"{}").get("path")
    except Exception:
        return None
    return path if isinstance(path, str) and path.startswith("/") else None


def register_routes(app, backend: str) -> None:
    """Install per-request tracking, ``/healthz`` and ``/api/pageview``.

    ``/healthz`` is the network convention the hub's hourly pulse sweep
    probes (``PULSE_POLL_TARGETS=<key>=<url>/healthz`` on the hub adds
    this app), so it is registered even when reporting is dormant.
    """
    server = app.server

    if backend == "fastapi":
        from starlette.responses import JSONResponse

        @server.middleware("http")
        async def _satellite_track(request: Request, call_next):  # pragma: no cover
            try:
                client = request.client
                _track_from(dict(request.headers), request.url.path,
                            client.host if client else None)
            except Exception:
                pass
            return await call_next(request)

        @server.get("/healthz", include_in_schema=False)
        async def _healthz():  # pragma: no cover
            return JSONResponse(_health_body())

        @server.post("/api/pageview", include_in_schema=False)
        async def _pageview(request: Request):  # pragma: no cover
            path = _pageview_path(await request.body())
            if path:
                client = request.client
                _track_from(dict(request.headers), path,
                            client.host if client else None)
            return JSONResponse({"ok": bool(path)}, status_code=200 if path else 400)

    elif backend == "quart":
        from quart import jsonify, request

        @server.before_request
        async def _satellite_track():  # pragma: no cover
            _track_from(dict(request.headers), request.path, request.remote_addr)

        @server.get("/healthz")
        async def _healthz():  # pragma: no cover
            return jsonify(_health_body())

        @server.post("/api/pageview")
        async def _pageview():  # pragma: no cover
            path = _pageview_path(await request.get_data())
            if path:
                _track_from(dict(request.headers), path, request.remote_addr)
            return jsonify({"ok": bool(path)}), 200 if path else 400

    else:
        from flask import jsonify, request

        @server.before_request
        def _satellite_track():
            _track_from(dict(request.headers), request.path, request.remote_addr)

        @server.get("/healthz")
        def _healthz():
            return jsonify(_health_body())

        @server.post("/api/pageview")
        def _pageview():
            path = _pageview_path(request.get_data())
            if path:
                _track_from(dict(request.headers), path, request.remote_addr)
            return jsonify({"ok": bool(path)}), 200 if path else 400

    print(f"[satellite-analytics] /healthz + /api/pageview registered ({backend})")


def register_pageview_beacon(location_id: str = "url") -> None:
    """Beacon every client-side route change to ``/api/pageview``.

    ``prevent_initial_call=True`` keeps the entry page out of it — that
    one already arrived as a real HTTP request. Output is the hidden
    Store from :func:`beacon_component`; nothing reads it.
    """
    from dash import Input, Output, clientside_callback

    clientside_callback(
        """
        function(pathname) {
            if (pathname) {
                try {
                    fetch('/api/pageview', {
                        method: 'POST',
                        keepalive: true,
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({path: pathname})
                    }).catch(function(){});
                } catch (e) {}
            }
            return window.dash_clientside.no_update;
        }
        """,
        Output("satellite-pageview-beacon", "data"),
        Input(location_id, "pathname"),
        prevent_initial_call=True,
    )


def beacon_component():
    """Hidden sink for the beacon callback; place it in the app shell."""
    from dash import dcc

    return dcc.Store(id="satellite-pageview-beacon", data=None)


def _health_body() -> dict:
    from lib.constants import APP_VERSION

    return {"ok": True, "app": APP_ID, "version": APP_VERSION,
            "reporting": bool(_secret()) and not DRY_RUN}


def register(app, backend: str) -> None:
    """One call from run.py: routes + beacon callback + reporter thread."""
    register_routes(app, backend)
    if not enabled():
        print("[satellite-analytics] dormant — set CROSS_APP_WEBHOOK_SECRET "
              "to report traffic to 2plot.ai")
        return
    register_pageview_beacon()
    started = start_reporter()
    print(f"[satellite-analytics] app='{APP_ID}' hub={HUB_URL} "
          f"interval={REPORT_INTERVAL_S}s dry_run={DRY_RUN} reporter={started}")
