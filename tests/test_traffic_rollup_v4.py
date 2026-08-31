"""Rollup v4 — the vendor dimension, additive (1.6.34; v3-AGNOSTIC since 1.6.36).

Kept OUT of tests/test_traffic_rollup.py on purpose: that file pins v3
and must pass unmodified on adoption. Everything here drives daily_rollup
with a hand-built ledger that has BOTH tables — and asserts ONLY v4:
`vendors[]`, `reads`, their shapes, and that the non-v4 keys do not move
when reads are added. It must pass against a lib/traffic_rollup.py that
has v4 but NOT v3 (clerkhook: no `load_agent_hits`, no `bot_visitors`,
`daily_rollup(app, day, visits=None, reads=None)`), which the template's
own suite proves by running this file against tests/fixtures/
rollup_pre_v3.py (tests/test_rollup_v4_is_v3_agnostic.py). Do not import
a v3 seam here; the fixture run goes red if you do.

The module under test is `lib.traffic_rollup` unless ROLLUP_V4_MODULE
names another importable module (the fixture run does).
"""

from __future__ import annotations

import importlib
import json
import os
from datetime import date, datetime

from dash_improve_my_llms._ledger import EVENT_FIELDS, TIERS

R = importlib.import_module(os.environ.get("ROLLUP_V4_MODULE", "lib.traffic_rollup"))

DAY = date(2026, 8, 29)


def _ts(hour=10, minute=0, day=DAY):
    return datetime(day.year, day.month, day.day, hour, minute).timestamp()


def _read(path="/llms.txt", *, tier="index", vendor_key="gptbot",
          vendor_class="training", verified="unverified", policy=None,
          nbytes=1000, minute=0, day=DAY):
    """A ledger row built THROUGH `AnalyticsTracker.record_read` from a
    classify()-shaped event (1.6.41, leaflet's finding): the stored row
    carries exactly the package's EVENT_FIELDS, so a key the package does
    not emit — `vendor_class` on 2.8.0 — is dropped here the way production
    drops it. A fixture written by hand asserted a shape production never
    produced, and every host's rollup sent `class: null` unnoticed."""
    import tempfile
    from pathlib import Path as _P

    from lib.analytics_tracker import AnalyticsTracker

    ev = {k: None for k in EVENT_FIELDS}
    ev.update(ts=_ts(minute=minute, day=day), host="x", path=path, method="GET",
              tier=tier, lane="crawler", bot_type=vendor_class or "unknown",
              vendor_key=vendor_key, vendor_class=vendor_class,
              verified=verified, policy=policy,
              verdict="served", status=200, bytes=nbytes, ua="ua", client_ip="203.0.113.9")
    with tempfile.TemporaryDirectory() as d:
        t = AnalyticsTracker(_P(d) / "l.json")
        t.record_read(ev)
        t.flush()
        return json.loads((_P(d) / "l.json").read_text())["reads"][0]


# What `class` can be on THIS package: the rollup reads `vendor_class` from
# the stored row, and the row carries only EVENT_FIELDS. On 2.8.0 that is
# None for every vendor (dimll 2.9.2 adds the field); the pin follows the
# seam instead of asserting a value production cannot produce.
CLASS_ON_THIS_PACKAGE = "training" if "vendor_class" in EVENT_FIELDS else None


def _visit(path, *, minute=0, ip="1.1.1.1", ua="Mozilla/5.0 Chrome",
           device_type="desktop"):
    return {"timestamp": f"2026-08-29T10:{minute:02d}:00", "path": path,
            "ip_address": ip, "user_agent": ua, "device_type": device_type}


def _ledger(tmp_path, visits=(), reads=()):
    p = tmp_path / "visitor_analytics.json"
    p.write_text(json.dumps({"visits": list(visits), "reads": list(reads)}))
    return str(p)


def _rollup(tmp_path, monkeypatch, visits=(), reads=(), day=DAY):
    """`daily_rollup(app, day)` with the ledger in the env — the ONE call
    shape every version of the module accepts. No v3 kwargs."""
    led = _ledger(tmp_path, visits, reads)
    monkeypatch.setenv("TRAFFIC_ANALYTICS_FILE", led)
    return R.daily_rollup("t", day)


def _non_v4(payload):
    return {k: v for k, v in payload.items() if k not in ("vendors", "reads")}


def test_vendors_block_is_absent_without_reads(tmp_path, monkeypatch):
    p = _rollup(tmp_path, monkeypatch, visits=[_visit("/")])
    assert p is not None
    assert "vendors" not in p and "reads" not in p


def test_a_pre_1_6_34_ledger_has_no_reads_key_and_that_is_empty(tmp_path):
    p = tmp_path / "old.json"
    p.write_text(json.dumps({"visits": []}))
    assert R.load_reads(str(p)) == []


def test_vendor_rows_group_on_key_verified_policy(tmp_path, monkeypatch):
    reads = [
        _read(vendor_key="gptbot", verified="unverified", nbytes=100),
        _read(vendor_key="gptbot", verified="unverified", nbytes=150, tier="full"),
        _read(vendor_key="gptbot", verified="verified", nbytes=1),
        _read(vendor_key="gptbot", verified="unverified", policy="meter", nbytes=1),
        _read(vendor_key="claudebot", verified="n/a", nbytes=7),
        _read(vendor_key=None, vendor_class=None, verified="n/a", nbytes=3),
    ]
    p = _rollup(tmp_path, monkeypatch, reads=reads)
    rows = {(r["key"], r["verified"], r["policy"]): r for r in p["vendors"]}
    assert set(rows) == {("gptbot", "unverified", "default"),
                         ("gptbot", "verified", "default"),
                         ("gptbot", "unverified", "meter"),
                         ("claudebot", "n/a", "default"),
                         (None, "n/a", "default")}
    top = rows[("gptbot", "unverified", "default")]
    assert top["hits"] == 2 and top["bytes"] == 250 and top["class"] == CLASS_ON_THIS_PACKAGE
    assert top["tiers"] == {**{t: 0 for t in TIERS}, "index": 1, "full": 1}
    assert p["reads"] == 6 == sum(r["hits"] for r in p["vendors"])
    assert p["vendors"][0]["hits"] == 2          # sorted by hits desc
    assert rows[(None, "n/a", "default")]["class"] is None   # null key KEPT, class null regardless


def test_tiers_always_carry_all_seven_keys(tmp_path, monkeypatch):
    p = _rollup(tmp_path, monkeypatch, reads=[_read(tier="sitemap")])
    row = p["vendors"][0]
    assert tuple(row["tiers"]) == TIERS
    assert row["tiers"]["sitemap"] == 1
    assert all(isinstance(n, int) for n in row["tiers"].values())


def test_reads_are_joined_not_summed(tmp_path, monkeypatch):
    """The request hook still writes the visits row for the same request;
    reads is a SECOND table. Every non-v4 key must be identical with and
    without reads — whatever keys this version of the rollup emits."""
    visits = [_visit("/", ip="2.2.2.2", ua="GPTBot/1.2", device_type="bot"),
              _visit("/backends", minute=1)]
    without = _rollup(tmp_path, monkeypatch, visits=visits)
    with_reads = _rollup(tmp_path, monkeypatch, visits=visits, reads=[_read()] * 5)
    assert _non_v4(with_reads) == _non_v4(without)
    assert with_reads["reads"] == 5


def test_a_reads_only_day_is_reported(tmp_path, monkeypatch):
    """A host whose request hook lost the row still reports what the
    package says it served — the machine-only-day rule, extended."""
    p = _rollup(tmp_path, monkeypatch, reads=[_read()])
    assert p is not None
    assert p["reads"] == 1 and p["vendors"][0]["key"] == "gptbot"


def test_reads_from_another_day_do_not_leak(tmp_path, monkeypatch):
    p = _rollup(tmp_path, monkeypatch, visits=[_visit("/")],
                reads=[_read(day=date(2026, 8, 28))])
    assert "vendors" not in p


def test_vendor_rows_are_capped_and_sorted(tmp_path):
    reads = [_read(vendor_key=f"v{i:03d}") for i in range(50)]
    reads += [_read(vendor_key="big")] * 3
    rows = R.vendor_rows(R.load_reads(_ledger(tmp_path, reads=reads)))
    assert len(rows) == 40
    assert rows[0]["key"] == "big" and rows[0]["hits"] == 3


def test_the_reporter_payload_carries_v4_on_a_read_day(tmp_path, monkeypatch):
    """The reporter changes nothing: it POSTs whatever daily_rollup returns,
    and daily_rollup loads reads itself when not handed them."""
    p = _rollup(tmp_path, monkeypatch, visits=[_visit("/")], reads=[_read()])
    assert p["reads"] == 1 and p["vendors"][0]["key"] == "gptbot"


def test_the_fixture_rows_are_what_record_read_stores():
    """The seam itself (1.6.41): a row is EVENT_FIELDS + kind, nothing else —
    client_ip dropped by default, and any key the package does not emit
    (vendor_class on 2.8.0) absent, not None-by-hand."""
    row = _read()
    assert row["kind"] == "read" and "client_ip" not in row
    assert set(row) - {"kind"} <= set(EVENT_FIELDS)
    assert ("vendor_class" in row) == ("vendor_class" in EVENT_FIELDS)
