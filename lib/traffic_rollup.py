"""
Daily traffic rollup — the payload 2plot.ai's ``/traffic`` dashboard reads.

This is a deliberate mirror of the hub's own ``lib/traffic_insights.py``
(2plot.ai). The hub charts every satellite on the same axes, so a number only
means something if every app computed it the same way. The rules, copied from
the hub's honesty contract:

- a **visitor** is an ``(IP, user-agent)`` pair. Shared IPs/NATs can merge
  people and private windows can split them — the standard approximation.
- a **session** is consecutive hits from one visitor with gaps under 30
  minutes.
- a session's **duration** is its first→last hit span. A single-hit session has
  NO measurable duration; it is excluded from the median, never padded in.
- ``human_hits`` / ``bot_hits`` split on the tracker's ``device_type``.
- ``visitors``, ``sessions``, ``pages`` and ``countries`` are **humans only**.

Infrastructure paths (``/healthz``, ``/llms.txt``, ``/robots.txt``,
``/sitemap.xml``, asset and Dash-internal routes) are excluded here rather than
at write time, exactly like the hub — so the ledger keeps the full record while
the reported numbers stay comparable.

Since the network's 402 groundwork the rollup ALSO reports the machine
surfaces through the hub's optional v3 fields, mirroring the hub's own
self-report semantics exactly:

- ``bot_visitors`` — unique ``(IP, user-agent)`` pairs among BOT hits that
  day, machine surfaces included. A daily distinct count; the hub never
  sums it across days.
- machine-surface rows join ``pages`` with a per-row ``bot_hits`` split —
  the per-document crawl-demand signal the hub's /admin/402 board prices
  against.
- ``human_hits`` / ``bot_hits`` include machine-surface fetches (the
  tracker always recorded them; they were only hidden from the report).
"""
from __future__ import annotations

import hashlib
from collections import defaultdict
from datetime import date, datetime, timedelta

from lib.analytics_tracker import analytics_path

SESSION_GAP_MIN = 30

# Mirror of the hub's lib/traffic_insights._SKIP — keep them in sync.
# The last three entries are the tiered corpus docs and the per-page JSON
# twin: every machine surface load_agent_hits() picks up must be skipped
# here, or its fetches are counted TWICE in human_hits/bot_hits/pages
# (once as a regular visit, once as a machine-surface row). '/llms.txt'
# does not substring-match '/llms-small.txt', so each needs its own entry.
# The hub's tuple is missing these three as of 2026-08-15 — its comment
# claims the exclusion, its tuple doesn't deliver it; port this fix there.
_SKIP = ('.css', '.js', '.png', '.jpg', '.ico', '.svg', '.woff', '.ttf', '_dash',
         '_reload-hash', 'favicon', '/_dash-update-component', '/_dash-layout',
         '/assets/', '[]', '/healthz', '/llms.txt', '/sitemap', '/robots',
         '/llms-small.txt', '/llms-full.txt', 'page.json')


def load_visits(path=None):
    """Cleaned hit list, each with a parsed naive ``dt`` and a stable ``vkey``."""
    import json

    try:
        with open(path or analytics_path()) as f:
            raw = json.load(f).get("visits", [])
    except Exception:
        return []
    out = []
    for v in raw:
        p = v.get("path") or ""
        if not p.startswith('/') or any(s in p for s in _SKIP):
            continue
        try:
            dt = datetime.fromisoformat(v["timestamp"])
        except Exception:
            continue
        if dt.tzinfo is not None:      # tolerate aware timestamps from older
            dt = dt.replace(tzinfo=None)   # writers; the day key stays local
        v = dict(v)
        v["dt"] = dt
        v["vkey"] = visitor_key(v)
        out.append(v)
    out.sort(key=lambda v: v["dt"])
    return out


def visitor_key(v):
    ua = hashlib.md5((v.get("user_agent") or "?").encode()).hexdigest()[:8]
    return f"{v.get('ip_address') or '?'}|{ua}"


# Machine-readable document surfaces — the complement of _SKIP's llms/
# robots/sitemap rule (mirrors the hub's traffic_insights.is_agent_surface,
# including the tiered corpus docs from dash-improve-my-llms ≥ 2.4.0).
_AGENT_EXACT = ('/robots.txt', '/sitemap.xml')
_AGENT_SUFFIXES = ('/llms.txt', '/llms-small.txt', '/llms-full.txt',
                   '/page.json')


def is_agent_surface(path: str) -> bool:
    return (path in _AGENT_EXACT
            or path in ('/llms.txt', '/llms-small.txt', '/llms-full.txt')
            or path.endswith(_AGENT_SUFFIXES))


def load_agent_hits(path=None):
    """Machine-surface hit list — same ``dt``/``vkey`` shape as
    :func:`load_visits`, keeping ONLY what that function skips for the
    llms/robots/sitemap surfaces."""
    import json

    try:
        with open(path or analytics_path()) as f:
            raw = json.load(f).get("visits", [])
    except Exception:
        return []
    out = []
    for v in raw:
        p = v.get("path") or ""
        if not p.startswith('/') or not is_agent_surface(p):
            continue
        try:
            dt = datetime.fromisoformat(v["timestamp"])
        except Exception:
            continue
        if dt.tzinfo is not None:
            dt = dt.replace(tzinfo=None)
        v = dict(v)
        v["dt"] = dt
        v["vkey"] = visitor_key(v)
        out.append(v)
    out.sort(key=lambda v: v["dt"])
    return out


def sessionize(visits, gap_min=SESSION_GAP_MIN):
    """Group hits into per-visitor sessions on the 30-minute gap rule."""
    by_key = defaultdict(list)
    for v in visits:
        by_key[v["vkey"]].append(v)
    gap = timedelta(minutes=gap_min)
    sessions = []
    for key, hits in by_key.items():
        cur = [hits[0]]
        for h in hits[1:]:
            if h["dt"] - cur[-1]["dt"] > gap:
                sessions.append(_session(key, cur))
                cur = [h]
            else:
                cur.append(h)
        sessions.append(_session(key, cur))
    sessions.sort(key=lambda s: s["start"])
    return sessions


def _session(key, hits):
    first, last = hits[0], hits[-1]
    return {
        "key": key,
        "start": first["dt"],
        "end": last["dt"],
        "duration_s": (last["dt"] - first["dt"]).total_seconds(),
        "hits": len(hits),
        "pages": [h["path"] for h in hits],
    }


def _country(v):
    """ISO code when we have one (CF-IPCountry / ip-api), else the name."""
    loc = v.get("location") or {}
    return loc.get("country_code") or loc.get("country") or None


def daily_rollup(app: str, day: date | None = None, visits=None,
                 agent_visits=None) -> dict | None:
    """Build the v2+v3 satellite payload for ``day`` (default: today, local).

    Returns ``None`` when the day has no tracked hits at all — there is
    nothing truthful to report, and an all-zero row would read as "we were
    up and nobody came" rather than "no data". A day with ONLY machine-
    surface fetches IS reported: crawlers hammering llms.txt while no
    human visits is exactly the signal the hub's 402 board exists to see.
    """
    day = day or datetime.now().date()
    visits = load_visits() if visits is None else visits
    agent_visits = load_agent_hits() if agent_visits is None else agent_visits
    hits = [v for v in visits if v["dt"].date() == day]
    agent = [v for v in agent_visits if v["dt"].date() == day]
    if not hits and not agent:
        return None

    humans = [v for v in hits if v.get("device_type") != "bot"]
    agent_bots = [v for v in agent if v.get("device_type") == "bot"]
    sessions = sessionize(humans) if humans else []
    multi = sorted(s["duration_s"] for s in sessions if s["hits"] > 1)

    pages: dict[str, int] = {}
    pages_bot: dict[str, int] = {}
    countries: dict[str, int] = {}
    for v in humans:
        pages[v["path"]] = pages.get(v["path"], 0) + 1
        cc = _country(v)
        if cc:
            countries[cc] = countries.get(cc, 0) + 1
    # Machine-surface rows join the same table, carrying the v3 bot split
    # (the hub folds pages[].bot_hits into its per-app demand columns).
    for v in agent:
        pages[v["path"]] = pages.get(v["path"], 0) + 1
        if v.get("device_type") == "bot":
            pages_bot[v["path"]] = pages_bot.get(v["path"], 0) + 1

    page_rows = []
    for p, n in sorted(pages.items(), key=lambda kv: -kv[1])[:20]:
        row = {"path": p, "hits": n}
        if p in pages_bot:
            row["bot_hits"] = pages_bot[p]
        page_rows.append(row)

    bot_vkeys = ({v["vkey"] for v in hits if v.get("device_type") == "bot"}
                 | {v["vkey"] for v in agent_bots})

    payload = {
        "app": app,
        "date": day.strftime("%Y-%m-%d"),
        "human_hits": len(humans) + (len(agent) - len(agent_bots)),
        "bot_hits": (len(hits) - len(humans)) + len(agent_bots),
        "visitors": len({v["vkey"] for v in humans}),
        "sessions": len(sessions),
        "bot_visitors": len(bot_vkeys),
        "pages": page_rows,
        "countries": dict(sorted(countries.items(), key=lambda kv: -kv[1])[:20]),
    }
    if multi:
        # Median of MULTI-PAGE human sessions only. Omitted (not zero) when no
        # session had a second pageview — zero would be a claim we can't make.
        payload["median_session_s"] = multi[len(multi) // 2]
    return payload
