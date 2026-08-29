"""Rollup v4 — the vendor dimension, additive (1.6.34).

Kept OUT of tests/test_traffic_rollup.py on purpose: that file pins v3
and must pass unmodified on adoption. Everything here drives daily_rollup
with a hand-built ledger that has BOTH tables.
"""

from __future__ import annotations

import json
from datetime import date, datetime


from dash_improve_my_llms._ledger import EVENT_FIELDS, TIERS

from lib.traffic_rollup import daily_rollup, load_reads, vendor_rows

DAY = date(2026, 8, 29)


def _ts(hour=10, minute=0, day=DAY):
    return datetime(day.year, day.month, day.day, hour, minute).timestamp()


def _read(path="/llms.txt", *, tier="index", vendor_key="gptbot",
          vendor_class="training", verified="unverified", policy=None,
          nbytes=1000, minute=0, day=DAY):
    ev = {k: None for k in EVENT_FIELDS}
    ev.update(ts=_ts(minute=minute, day=day), host="x", path=path, method="GET",
              tier=tier, lane="crawler", bot_type=vendor_class or "unknown",
              vendor_key=vendor_key, vendor_class=vendor_class,
              verified=verified, policy=policy,
              verdict="served", status=200, bytes=nbytes, ua="ua")
    ev.pop("client_ip")
    ev["kind"] = "read"
    return ev


def _visit(path, *, minute=0, ip="1.1.1.1", ua="Mozilla/5.0 Chrome",
           device_type="desktop"):
    return {"timestamp": f"2026-08-29T10:{minute:02d}:00", "path": path,
            "ip_address": ip, "user_agent": ua, "device_type": device_type}


def _ledger(tmp_path, visits=(), reads=()):
    p = tmp_path / "visitor_analytics.json"
    p.write_text(json.dumps({"visits": list(visits), "reads": list(reads)}))
    return str(p)


def _rollup(tmp_path, visits=(), reads=(), day=DAY):
    from lib.traffic_rollup import load_agent_hits, load_visits

    led = _ledger(tmp_path, visits, reads)
    return daily_rollup("t", day, visits=load_visits(led),
                        agent_visits=load_agent_hits(led), reads=load_reads(led))


def test_vendors_block_is_absent_without_reads(tmp_path):
    p = _rollup(tmp_path, visits=[_visit("/")])
    assert "vendors" not in p and "reads" not in p
    # and the v3 keys are exactly what v3 emitted
    assert set(p) == {"app", "date", "human_hits", "bot_hits", "visitors",
                      "sessions", "bot_visitors", "pages", "countries"}


def test_a_pre_1_6_34_ledger_has_no_reads_key_and_that_is_empty(tmp_path):
    p = tmp_path / "old.json"
    p.write_text(json.dumps({"visits": []}))
    assert load_reads(str(p)) == []


def test_vendor_rows_group_on_key_verified_policy(tmp_path):
    reads = [
        _read(vendor_key="gptbot", verified="unverified", nbytes=100),
        _read(vendor_key="gptbot", verified="unverified", nbytes=150, tier="full"),
        _read(vendor_key="gptbot", verified="verified", nbytes=1),
        _read(vendor_key="gptbot", verified="unverified", policy="meter", nbytes=1),
        _read(vendor_key="claudebot", verified="n/a", nbytes=7),
        _read(vendor_key=None, vendor_class=None, verified="n/a", nbytes=3),
    ]
    p = _rollup(tmp_path, reads=reads)
    rows = {(r["key"], r["verified"], r["policy"]): r for r in p["vendors"]}
    assert set(rows) == {("gptbot", "unverified", "default"),
                         ("gptbot", "verified", "default"),
                         ("gptbot", "unverified", "meter"),
                         ("claudebot", "n/a", "default"),
                         (None, "n/a", "default")}
    top = rows[("gptbot", "unverified", "default")]
    assert top["hits"] == 2 and top["bytes"] == 250 and top["class"] == "training"
    assert top["tiers"] == {**{t: 0 for t in TIERS}, "index": 1, "full": 1}
    assert p["reads"] == 6 == sum(r["hits"] for r in p["vendors"])
    # sorted by hits desc; the first row is the 2-hit one
    assert p["vendors"][0] is not None and p["vendors"][0]["hits"] == 2
    # the null-key row is KEPT — it is the unverifiable bulk
    assert rows[(None, "n/a", "default")]["class"] is None


def test_tiers_always_carry_all_seven_keys(tmp_path):
    p = _rollup(tmp_path, reads=[_read(tier="sitemap")])
    row = p["vendors"][0]
    assert tuple(row["tiers"]) == TIERS
    assert row["tiers"]["sitemap"] == 1
    assert all(isinstance(n, int) for n in row["tiers"].values())


def test_reads_are_joined_not_summed(tmp_path):
    """The request hook still writes the visits row for the same request;
    reads is a SECOND table. human_hits/bot_hits/pages must not move."""
    visits = [_visit("/llms.txt", ip="2.2.2.2", ua="GPTBot/1.2", device_type="bot")]
    without = _rollup(tmp_path, visits=visits)
    with_reads = _rollup(tmp_path, visits=visits, reads=[_read()] * 5)
    for k in ("human_hits", "bot_hits", "bot_visitors", "pages", "visitors"):
        assert with_reads[k] == without[k], k
    assert with_reads["reads"] == 5


def test_a_reads_only_day_is_reported(tmp_path):
    """Extends the machine-only-day rule: a host whose request hook lost
    the row (or a fork that skips it) still reports what the package
    says it served."""
    p = _rollup(tmp_path, reads=[_read()])
    assert p is not None
    assert p["human_hits"] == 0 and p["bot_hits"] == 0
    assert p["reads"] == 1


def test_reads_from_another_day_do_not_leak(tmp_path):
    p = _rollup(tmp_path, visits=[_visit("/")],
                reads=[_read(day=date(2026, 8, 28))])
    assert "vendors" not in p


def test_vendor_rows_are_capped_and_sorted(tmp_path):
    reads = [_read(vendor_key=f"v{i:03d}") for i in range(50)]
    reads += [_read(vendor_key="big")] * 3
    rows = vendor_rows(load_reads(_ledger(tmp_path, reads=reads)))
    assert len(rows) == 40
    assert rows[0]["key"] == "big" and rows[0]["hits"] == 3


def test_the_reporter_payload_carries_v4_on_a_read_day(tmp_path, monkeypatch):
    """lib/satellite_reporter changes nothing: it POSTs whatever daily_rollup
    returns, and daily_rollup loads reads itself when not handed them."""
    led = _ledger(tmp_path, visits=[_visit("/")], reads=[_read()])
    monkeypatch.setenv("TRAFFIC_ANALYTICS_FILE", led)
    p = daily_rollup("t", DAY)
    assert p["reads"] == 1 and p["vendors"][0]["key"] == "gptbot"
