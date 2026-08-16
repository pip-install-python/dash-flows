"""The v3 machine-surface rollup — the numbers the 402 decision reads.

The owner rule for the network's 402 track is "instrument first, price
later": no payment code until crawl data justifies it. That makes THIS
module's output the evidence base for a business decision, which is a
stronger reason to test it than most code has. A silent double-count or a
dropped surface here doesn't crash anything — it prices a day pass off a
number that was never true.

Everything below drives daily_rollup() with hand-built ledgers, mirroring
the hub's self-report semantics (2plotai lib/traffic_insights):

- machine surfaces (llms tiers, twins, robots, sitemap, page.json) are
  EXCLUDED from load_visits and picked up ONLY by load_agent_hits — the
  two must partition the ledger, never overlap (the double-count bug);
- a day with only machine-surface fetches is reported, not skipped —
  crawlers hammering llms.txt with zero human visits is exactly the
  signal the hub's day-pass board exists to see;
- bot_visitors is a daily distinct (IP, UA) count across bot hits on both
  page and machine surfaces;
- visitors/sessions stay humans-on-pages only.
"""

from __future__ import annotations

import json
from datetime import date

import pytest

from lib.traffic_rollup import (
    daily_rollup,
    is_agent_surface,
    load_agent_hits,
    load_visits,
)

DAY = date(2026, 8, 14)


def _visit(path, *, minute=0, ip="1.1.1.1", ua="Mozilla/5.0 Chrome",
           device_type="desktop"):
    return {
        "timestamp": f"2026-08-14T10:{minute:02d}:00",
        "path": path,
        "ip_address": ip,
        "user_agent": ua,
        "device_type": device_type,
    }


def _ledger(tmp_path, visits):
    p = tmp_path / "visitor_analytics.json"
    p.write_text(json.dumps({"visits": visits}))
    return str(p)


BOT = dict(ip="2.2.2.2", ua="GPTBot/1.0", device_type="bot")


# ---------------------------------------------------------------------------
# The partition: every hit is a page visit or a machine-surface hit, never both
# ---------------------------------------------------------------------------


MACHINE_SURFACES = [
    "/llms.txt", "/llms-small.txt", "/llms-full.txt",
    "/robots.txt", "/sitemap.xml",
    "/backends/llms.txt", "/backends/page.json",
]

PAGE_SURFACES = ["/", "/backends", "/examples/ai-integration"]


@pytest.mark.parametrize("path", MACHINE_SURFACES)
def test_machine_surfaces_partition_cleanly(tmp_path, path):
    """The double-count guard. '/llms.txt' in _SKIP does not substring-match
    '/llms-small.txt', so before the tier docs joined _SKIP their fetches
    landed in BOTH load_visits and load_agent_hits — and were counted twice
    in every total the hub prices against."""
    ledger = _ledger(tmp_path, [_visit(path, **BOT)])
    assert load_visits(ledger) == [], f"{path} leaked into page visits"
    assert len(load_agent_hits(ledger)) == 1, f"{path} missed by agent hits"


@pytest.mark.parametrize("path", PAGE_SURFACES)
def test_page_surfaces_partition_cleanly(tmp_path, path):
    ledger = _ledger(tmp_path, [_visit(path)])
    assert len(load_visits(ledger)) == 1, f"{path} skipped as infrastructure"
    assert load_agent_hits(ledger) == [], f"{path} misread as machine surface"


def test_every_agent_surface_is_skipped_by_load_visits(tmp_path):
    """The structural invariant behind the parametrized cases: whatever
    is_agent_surface() claims, load_visits() must refuse — one rule, both
    readers, no path counted twice however either list grows."""
    ledger = _ledger(tmp_path, [_visit(p, **BOT) for p in MACHINE_SURFACES])
    for v in load_visits(ledger):
        assert not is_agent_surface(v["path"]), (
            f"{v['path']} is claimed by both load_visits and load_agent_hits"
        )


# ---------------------------------------------------------------------------
# The 402 board's signal: machine-only days, per-row bot splits
# ---------------------------------------------------------------------------


def test_a_machine_surface_only_day_is_reported(tmp_path):
    """The day the old rollup skipped. Crawlers pulling the corpus while no
    human visits is the exact demand signal the day-pass board exists to
    see — returning None here hides it."""
    ledger = _ledger(tmp_path, [
        _visit("/llms-full.txt", minute=1, **BOT),
        _visit("/llms-full.txt", minute=2, **BOT),
        _visit("/llms.txt", minute=3, ip="3.3.3.3", ua="ClaudeBot",
               device_type="bot"),
    ])
    payload = daily_rollup("boilerplate", DAY,
                           visits=load_visits(ledger),
                           agent_visits=load_agent_hits(ledger))
    assert payload is not None
    assert payload["human_hits"] == 0
    assert payload["bot_hits"] == 3
    assert payload["bot_visitors"] == 2      # GPTBot + ClaudeBot, distinct
    assert payload["visitors"] == 0          # humans-on-pages only
    assert payload["sessions"] == 0
    rows = {r["path"]: r for r in payload["pages"]}
    assert rows["/llms-full.txt"] == {"path": "/llms-full.txt", "hits": 2,
                                      "bot_hits": 2}


def test_an_empty_day_still_reports_nothing(tmp_path):
    """None means "no data", and stays the answer when nothing was tracked —
    an all-zero row would read as "we were up and nobody came"."""
    ledger = _ledger(tmp_path, [])
    assert daily_rollup("boilerplate", DAY,
                        visits=load_visits(ledger),
                        agent_visits=load_agent_hits(ledger)) is None


def test_mixed_day_totals_and_the_bot_split(tmp_path):
    """One human reading a page and fetching a twin; one bot crawling. Every
    number in the payload is checkable by hand here — if this test needs
    updating, the hub's axes changed and every satellite must move together."""
    ledger = _ledger(tmp_path, [
        # a human: two page views (one session), then their agent grabs a twin
        _visit("/backends", minute=1),
        _visit("/examples/ai-integration", minute=5),
        _visit("/backends/llms.txt", minute=6),
        # a bot: one page fetch, two machine-surface fetches
        _visit("/backends", minute=10, **BOT),
        _visit("/llms.txt", minute=11, **BOT),
        _visit("/backends/page.json", minute=12, **BOT),
    ])
    payload = daily_rollup("boilerplate", DAY,
                           visits=load_visits(ledger),
                           agent_visits=load_agent_hits(ledger))
    assert payload["human_hits"] == 3        # 2 page views + 1 human twin fetch
    assert payload["bot_hits"] == 3          # 1 page fetch + 2 machine fetches
    assert payload["visitors"] == 1          # the human; bots never count here
    assert payload["bot_visitors"] == 1      # one bot identity across surfaces
    assert payload["sessions"] == 1

    rows = {r["path"]: r for r in payload["pages"]}
    # the human page rows carry no bot split — nothing to split
    assert "bot_hits" not in rows["/examples/ai-integration"]
    # /backends: 2 human page views + 1 bot page view... but page visits by
    # bots are not in `pages` (humans only) — only machine-surface rows join
    assert rows["/backends"]["hits"] == 1
    # machine-surface rows carry the per-document demand split
    assert rows["/llms.txt"] == {"path": "/llms.txt", "hits": 1, "bot_hits": 1}
    assert rows["/backends/llms.txt"]["hits"] == 1
    assert "bot_hits" not in rows["/backends/llms.txt"]   # a human fetched it


def test_bot_visitors_is_distinct_not_summed(tmp_path):
    """The hub never sums bot_visitors across days; within a day the same
    (IP, UA) hammering every surface is ONE visitor, however many hits."""
    ledger = _ledger(tmp_path, [
        _visit("/llms.txt", minute=m, **BOT) for m in range(1, 8)
    ] + [_visit("/backends", minute=9, **BOT)])
    payload = daily_rollup("boilerplate", DAY,
                           visits=load_visits(ledger),
                           agent_visits=load_agent_hits(ledger))
    assert payload["bot_hits"] == 8
    assert payload["bot_visitors"] == 1
