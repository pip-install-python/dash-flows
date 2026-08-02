"""
Visitor Analytics Tracker
Tracks visitor information including device type, bot detection, and geolocation.

This ledger is the raw material for two things:

1. the app's own record of who read the docs, and
2. the hourly rollup this app POSTs to 2plot.ai (``lib/satellite_reporter``),
   which is what the network ``/traffic`` dashboard charts.

Because the hub compares apps side by side, the fields written here match the
hub's own ledger exactly: ``{timestamp, path, device_type, user_agent,
bot_type?, ip_address?, location?}``.

Accuracy notes (these are the things that quietly wreck the numbers):

- **Network machinery is never a visitor.** Any request whose User-Agent
  carries ``lib.constants.INTERNAL_UA_TOKEN`` is dropped in ``track_visit``
  before device detection — the network's internal-traffic contract
  (https://2plot.ai/docs/satellite-analytics). ``/healthz`` is dropped there
  too. Both are write-time rules on purpose; see the comment in ``track_visit``.
- **Client IP** comes from the proxy headers first (``CF-Connecting-IP``,
  ``X-Forwarded-For``, ...). Behind Cloudflare/Render, ``remote_addr`` is the
  *proxy*, so every visitor would collapse into one and geolocation would point
  at a datacenter.
- **Country** prefers Cloudflare's ``CF-IPCountry`` header — free, accurate and
  instant. The ip-api.com lookup is only a fallback (set
  ``ANALYTICS_GEO_LOOKUP=0`` to disable it entirely).
- **Writes are buffered, locked and pruned.** Multiple gunicorn/uvicorn workers
  share this file; without an ``flock`` around the read-modify-write they
  silently overwrite each other's hits. The buffer keeps a docs site from
  rewriting the whole file on every request, and retention keeps it bounded.
"""
import atexit
import json
import os
import threading
import time
from pathlib import Path
from datetime import datetime, timedelta
from functools import lru_cache

import requests

try:  # POSIX only — Windows dev boxes just run without the cross-process lock
    import fcntl
except ImportError:  # pragma: no cover
    fcntl = None


_REPO_ROOT = Path(__file__).resolve().parent.parent

# How many hits to hold in memory before touching disk, and the longest a hit
# may sit in the buffer. Both are tiny; the point is to turn "rewrite the file
# on every request" into "rewrite it a few times a minute".
FLUSH_EVERY = int(os.getenv("ANALYTICS_FLUSH_EVERY", "10"))
FLUSH_INTERVAL_S = float(os.getenv("ANALYTICS_FLUSH_INTERVAL_S", "30"))

# Retention. The hub keeps the durable history (every rollup we POST rides its
# heartbeat store), so this file only needs enough runway to build a rollup and
# show recent local history.
RETENTION_DAYS = int(os.getenv("ANALYTICS_RETENTION_DAYS", "45"))
MAX_VISITS = int(os.getenv("ANALYTICS_MAX_VISITS", "20000"))

_IP_HEADERS = (
    "cf-connecting-ip",     # Cloudflare
    "true-client-ip",       # Cloudflare Enterprise / Akamai
    "x-real-ip",            # nginx
    "x-forwarded-for",      # everything else (first hop = the client)
)

_PRIVATE_PREFIXES = ('10.', '172.', '192.168.', 'fe80:', 'fc00:', 'fd00:')


def analytics_path() -> Path:
    """Resolve the ledger path (env override, else repo root).

    Absolute on purpose: the old relative default wrote a *different* file
    depending on the process working directory, which split the numbers.
    """
    return Path(os.getenv("TRAFFIC_ANALYTICS_FILE")
                or _REPO_ROOT / "visitor_analytics.json")


def _lower_headers(headers) -> dict:
    """Normalise any header mapping (Flask, Starlette, dict) to lowercase."""
    if not headers:
        return {}
    try:
        return {str(k).lower(): v for k, v in headers.items()}
    except Exception:
        return {}


def client_ip(headers=None, fallback=None):
    """The real client address, reading proxy headers before ``remote_addr``."""
    lc = _lower_headers(headers)
    for name in _IP_HEADERS:
        raw = lc.get(name)
        if not raw:
            continue
        # X-Forwarded-For is "client, proxy1, proxy2" — the client is first.
        ip = str(raw).split(",")[0].strip()
        if ip:
            return ip
    return fallback


def header_country(headers=None):
    """ISO country code from Cloudflare's ``CF-IPCountry``, if present.

    ``XX`` (unknown) and ``T1`` (Tor) are not countries — treated as absent.
    """
    cc = (_lower_headers(headers).get("cf-ipcountry") or "").strip().upper()
    return cc if cc and cc not in ("XX", "T1") else None


_geo_cache: dict = {}
_geo_inflight: set = set()
_geo_lock = threading.Lock()
_GEO_MAX_INFLIGHT = 4


@lru_cache(maxsize=2000)
def _geolocate(ip_address):
    """Geolocate an IP via ip-api.com (free, 45 req/min). Cached, including
    misses, so one slow lookup never repeats for the same visitor."""
    if not ip_address or ip_address in ('127.0.0.1', 'localhost', '::1'):
        return None
    if ip_address.startswith(_PRIVATE_PREFIXES):
        return None
    try:
        response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=2)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                return {
                    'country': data.get('country'),
                    'country_code': data.get('countryCode'),
                    'region': data.get('regionName'),
                    'city': data.get('city'),
                    'latitude': data.get('lat'),
                    'longitude': data.get('lon'),
                    'timezone': data.get('timezone'),
                }
    except Exception as e:
        # Silently fail - geolocation is optional
        print(f"Geolocation failed for {ip_address}: {e}")
    return None


def geo_for(ip_address):
    """Non-blocking geolocation.

    Returns the cached result if we already know this IP, otherwise kicks the
    lookup off in the background and returns ``None``. Hits sit in the write
    buffer for up to ``FLUSH_INTERVAL_S`` before landing on disk, and ``flush``
    backfills whatever resolved in the meantime — so the country still gets
    recorded without ever putting an HTTP round trip in front of a page view.
    """
    if not ip_address:
        return None
    with _geo_lock:
        if ip_address in _geo_cache:
            return _geo_cache[ip_address]
        # Bounded: a crawler sweep must not spawn a thread per address.
        if ip_address in _geo_inflight or len(_geo_inflight) >= _GEO_MAX_INFLIGHT:
            return None
        _geo_inflight.add(ip_address)

    def _resolve():
        try:
            result = _geolocate(ip_address)
        except Exception:
            result = None
        with _geo_lock:
            _geo_cache[ip_address] = result
            _geo_inflight.discard(ip_address)

    threading.Thread(target=_resolve, name="geo-lookup", daemon=True).start()
    return None


class AnalyticsTracker:
    """Track visitor analytics to JSON file."""

    def __init__(self, data_file=None):
        self._data_file = Path(data_file) if data_file else None
        self._buffer = []
        self._buffer_lock = threading.Lock()
        self._last_flush = time.time()
        atexit.register(self.flush)

    @property
    def data_file(self) -> Path:
        return self._data_file or analytics_path()

    def _ensure_file_exists(self):
        """Create analytics file if it doesn't exist."""
        if not self.data_file.exists():
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            self.data_file.write_text(json.dumps({
                "visits": [],
                "stats": {
                    "desktop": 0,
                    "mobile": 0,
                    "tablet": 0,
                    "bot": 0,
                    "total": 0
                }
            }, indent=2))

    def detect_device_type(self, user_agent):
        """Detect device type from user agent string."""
        if not user_agent:
            return "desktop"

        user_agent = user_agent.lower()

        # Check for bots first
        if self.is_bot(user_agent):
            return "bot"

        # Check for tablet before mobile — iPads and most Android tablets also
        # carry a mobile token, so the mobile test would swallow them.
        if any(tablet in user_agent for tablet in ['ipad', 'tablet', 'kindle', 'silk']):
            return "tablet"

        if any(mobile in user_agent for mobile in ['mobile', 'android', 'iphone', 'ipod', 'blackberry', 'windows phone']):
            return "mobile"

        return "desktop"

    def is_bot(self, user_agent):
        """Check if user agent is a bot."""
        if not user_agent:
            return False

        bot_patterns = [
            'bot', 'crawler', 'spider', 'scraper', 'curl', 'wget',
            'python-requests', 'gptbot', 'anthropic', 'claude',
            'googlebot', 'bingbot', 'slurp', 'duckduckbot',
            'perplexitybot', 'chatgpt', 'headlesschrome', 'phantomjs',
            'monitoring', 'uptime', 'pingdom', 'better-uptime',
        ]

        return any(pattern in user_agent.lower() for pattern in bot_patterns)

    def detect_bot_type(self, user_agent):
        """Detect the type of bot from user agent."""
        if not user_agent:
            return "unknown"

        user_agent = user_agent.lower()

        # AI Training bots
        training_bots = ['gptbot', 'anthropic-ai', 'claude-web', 'ccbot', 'google-extended', 'facebookbot']
        if any(bot in user_agent for bot in training_bots):
            return "training"

        # AI Search bots
        search_bots = ['chatgpt-user', 'claudebot', 'perplexitybot', 'youbot', 'oai-searchbot']
        if any(bot in user_agent for bot in search_bots):
            return "search"

        # Traditional search bots
        traditional_bots = ['googlebot', 'bingbot', 'slurp', 'duckduckbot', 'yandex', 'baidu']
        if any(bot in user_agent for bot in traditional_bots):
            return "traditional"

        return "unknown"

    def get_geolocation(self, ip_address):
        """Get geolocation data from IP address (ip-api.com fallback path).

        Non-blocking: see ``geo_for``. Disable entirely with
        ``ANALYTICS_GEO_LOOKUP=0`` (deployments behind Cloudflare don't need
        it — ``CF-IPCountry`` already answers the question).
        """
        if os.getenv("ANALYTICS_GEO_LOOKUP", "1") == "0":
            return None
        return geo_for(ip_address)

    def track_visit(self, path, user_agent, ip_address=None, headers=None):
        """Track a visitor.

        ``headers`` is optional but strongly recommended — it's what makes the
        client IP and country correct behind a proxy. See ``client_ip``.
        """
        # --- The network's internal-traffic contract, applied at WRITE time --
        #
        # https://2plot.ai/docs/satellite-analytics, "Internal traffic": a
        # request carrying INTERNAL_UA_TOKEN is 2plot machinery talking to
        # itself and is counted nowhere. This has to happen HERE, before
        # `detect_device_type`, and not in lib/traffic_rollup's read-time
        # filter, for two reasons:
        #
        #   1. classification would run first, and the health sweep and smoke
        #      batteries look like bots — they would land in `bot_hits` and be
        #      reported to the hub as crawler interest in these docs;
        #   2. the ledger is what a person reads on a local analytics view. A
        #      row that exists but is filtered on the way out is still a row
        #      somebody has to know to discount.
        #
        # The token is matched case-insensitively so a caller may capitalise
        # its suffix however it likes.
        from lib.constants import INTERNAL_UA_TOKEN

        if INTERNAL_UA_TOKEN in (user_agent or "").lower():
            return

        # Skip internal Dash paths and static assets. `/healthz` and `/health`
        # are here too: the hub sweeps /healthz hourly and Render's own probe
        # hits it far more often than that, so storing it turns the ledger into
        # a record of monitoring. lib/traffic_rollup also drops it at read time
        # — that stays, for ledgers written before this rule existed.
        skip_paths = [
            '.css', '.js', '.png', '.jpg', '.ico', '.svg', '.woff', '.woff2', '.ttf', '.eot',
            '_dash', '_reload-hash', 'favicon', '/_dash-update-component',
            '/_dash-layout', '/_dash-dependencies', '/_dash-component-suites',
            '/assets/', '/healthz', '/health', '[]',  # Also skip malformed paths
            # The SPA pageview beacon endpoint (lib/pageview_beacon.py). The
            # beacon's *payload* path is tracked by the route handler; the
            # POST that carries it must not be counted as a second view.
            '/api/',
        ]
        if any(skip in path for skip in skip_paths):
            return

        # Only track valid paths that start with /
        if not path or not path.startswith('/') or path.startswith('//'):
            return

        device_type = self.detect_device_type(user_agent)

        visit_data = {
            "timestamp": datetime.now().isoformat(),
            "path": path,
            "device_type": device_type,
            "user_agent": user_agent or "Unknown",
        }

        # Add bot type if it's a bot
        if device_type == "bot":
            visit_data["bot_type"] = self.detect_bot_type(user_agent)

        ip_address = client_ip(headers, ip_address)
        if ip_address:
            visit_data["ip_address"] = ip_address

        # Country first from the edge header (free + instant), then ip-api.
        cc = header_country(headers)
        if cc:
            visit_data["location"] = {"country": cc, "country_code": cc}
        elif ip_address and device_type != "bot":
            geo_data = self.get_geolocation(ip_address)
            if geo_data:
                visit_data["location"] = geo_data
            else:
                # Lookup is in flight — flush() backfills it before the record
                # hits disk (the marker never survives into the ledger).
                visit_data["_geo_pending"] = ip_address

        with self._buffer_lock:
            self._buffer.append(visit_data)
            due = (len(self._buffer) >= FLUSH_EVERY
                   or (time.time() - self._last_flush) >= FLUSH_INTERVAL_S)
        if due:
            self.flush()

    # ------------------------------------------------------------------ disk --

    def flush(self):
        """Write buffered hits to disk under a cross-process lock.

        Safe to call at any time (the satellite reporter calls it before
        building a rollup so the numbers include the current minute).
        """
        with self._buffer_lock:
            pending, self._buffer = self._buffer, []
            self._last_flush = time.time()
        if not pending:
            return
        try:
            self._backfill_geo(pending)
            self._write(pending)
        except Exception:
            # Never lose the app over analytics; put the hits back so the next
            # flush can retry them.
            with self._buffer_lock:
                self._buffer = pending + self._buffer

    @staticmethod
    def _backfill_geo(pending):
        """Attach any background lookup that resolved while hits were buffered.

        The marker is left in place — a flush that fails to write puts these
        records back on the buffer, and the next attempt gets another chance at
        a lookup that has since landed. ``_write`` strips it before serialising.
        """
        for v in pending:
            ip = v.get("_geo_pending")
            if not ip or v.get("location"):
                continue
            with _geo_lock:
                loc = _geo_cache.get(ip)
            if loc:
                v["location"] = loc

    def _write(self, pending):
        self._ensure_file_exists()
        path = self.data_file
        lock_path = path.with_suffix(path.suffix + ".lock")
        lock_fh = open(lock_path, "a+") if fcntl else None
        try:
            if lock_fh:
                fcntl.flock(lock_fh, fcntl.LOCK_EX)
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                if not isinstance(data, dict):
                    raise ValueError("ledger is not an object")
            except Exception:
                data = {"visits": [], "stats": {"desktop": 0, "mobile": 0,
                                                "tablet": 0, "bot": 0, "total": 0}}

            visits = data.setdefault("visits", [])
            stats = data.setdefault("stats", {})
            # Internal markers stay on the buffered copy (for a retry) and
            # never reach the ledger.
            visits.extend({k: val for k, val in v.items() if k != "_geo_pending"}
                          for v in pending)
            for v in pending:
                dt = v["device_type"]
                stats[dt] = stats.get(dt, 0) + 1
                stats["total"] = stats.get("total", 0) + 1

            data["visits"] = _prune(visits)

            # Atomic replace: a crash mid-write can't leave a truncated ledger.
            tmp = path.with_suffix(path.suffix + ".tmp")
            with open(tmp, 'w') as f:
                json.dump(data, f, indent=2)
            os.replace(tmp, path)
        finally:
            if lock_fh:
                try:
                    fcntl.flock(lock_fh, fcntl.LOCK_UN)
                finally:
                    lock_fh.close()


def _prune(visits):
    """Drop hits older than the retention window, then cap the total."""
    if RETENTION_DAYS > 0:
        cutoff = (datetime.now() - timedelta(days=RETENTION_DAYS)).isoformat()
        visits = [v for v in visits if (v.get("timestamp") or "") >= cutoff]
    if MAX_VISITS > 0 and len(visits) > MAX_VISITS:
        visits = visits[-MAX_VISITS:]
    return visits


# Global tracker instance
tracker = AnalyticsTracker()
