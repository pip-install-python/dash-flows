"""The presence beacon (lib/satellite_reporter.py, presence half).

Presence is display-only and fail-silent by contract: the payload mirrors
the hub's own "active now" derivation (distinct human visitor keys inside
the session window — one measurement rule), the interval respects the hub's
30s floor and 0-disables, and no failure of any kind escapes the loop.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta

import pytest

from lib import satellite_reporter as sr
from lib.constants import INTERNAL_UA_TOKEN


def _visit(path, *, dt, ip="1.1.1.1", ua="Mozilla/5.0 Chrome",
           device_type="desktop"):
    return {
        "timestamp": dt.strftime("%Y-%m-%dT%H:%M:%S"),
        "path": path,
        "ip_address": ip,
        "user_agent": ua,
        "device_type": device_type,
    }


@pytest.fixture
def ledger(tmp_path, monkeypatch):
    path = tmp_path / "visitor_analytics.json"

    def write(visits):
        path.write_text(json.dumps({"visits": visits}))
        monkeypatch.setenv("TRAFFIC_ANALYTICS_FILE", str(path))
        # The suite shares one app whose tracker buffers the other tests'
        # client hits; a real flush() would pour those into this ledger and
        # the count under test would depend on test ordering.
        from lib.analytics_tracker import tracker

        monkeypatch.setattr(tracker, "flush", lambda: None)
        return path

    return write


def test_active_counts_distinct_humans_inside_the_session_window(
    ledger, monkeypatch
):
    now = datetime.now()
    fresh, stale = now - timedelta(minutes=5), now - timedelta(minutes=90)
    ledger([
        _visit("/a", dt=fresh, ip="1.1.1.1"),
        _visit("/b", dt=fresh, ip="1.1.1.1"),              # same visitor
        _visit("/c", dt=fresh, ip="2.2.2.2"),              # second visitor
        _visit("/d", dt=stale, ip="3.3.3.3"),              # outside window
        _visit("/e", dt=fresh, ip="4.4.4.4",
               ua="GPTBot/1.0", device_type="bot"),        # bots never count
    ])
    payload = sr.build_presence_payload(app="testapp")
    assert payload == {"app": "testapp", "active": 2}


def test_an_empty_ledger_reports_zero_not_an_error(ledger):
    ledger([])
    assert sr.build_presence_payload(app="t")["active"] == 0


def test_interval_floor_and_disable():
    import os

    os.environ["SATELLITE_PRESENCE_INTERVAL_S"] = "5"
    assert sr._presence_interval() == sr.PRESENCE_FLOOR_S
    os.environ["SATELLITE_PRESENCE_INTERVAL_S"] = "0"
    assert sr._presence_interval() == 0
    os.environ["SATELLITE_PRESENCE_INTERVAL_S"] = "junk"
    assert sr._presence_interval() == sr.PRESENCE_DEFAULT_INTERVAL_S
    del os.environ["SATELLITE_PRESENCE_INTERVAL_S"]
    assert sr._presence_interval() == sr.PRESENCE_DEFAULT_INTERVAL_S


def test_presence_url_derives_from_the_traffic_override(monkeypatch):
    """One SATELLITE_TRAFFIC_URL override retargets both endpoints — a
    staging hub does not need a second env var."""
    monkeypatch.delenv("SATELLITE_PRESENCE_URL", raising=False)
    monkeypatch.delenv("SATELLITE_TRAFFIC_URL", raising=False)
    assert sr.presence_endpoint() == "https://2plot.ai/api/satellite/active"
    monkeypatch.setenv("SATELLITE_TRAFFIC_URL",
                       "https://staging.example/api/satellite/traffic")
    assert sr.presence_endpoint() == "https://staging.example/api/satellite/active"
    monkeypatch.setenv("SATELLITE_PRESENCE_URL", "https://x.example/ping")
    assert sr.presence_endpoint() == "https://x.example/ping"


def test_a_failed_post_is_swallowed_never_raised(monkeypatch):
    import requests

    def boom(*args, **kwargs):
        raise requests.ConnectionError("hub is down")

    monkeypatch.setattr(requests, "post", boom)
    ok, detail = sr._post_signed("https://2plot.ai/api/satellite/active",
                                 {"app": "t", "active": 1},
                                 "presence-beacon", secret="s")
    assert ok is False and "request failed" in detail


def test_the_presence_post_sends_the_internal_token(monkeypatch):
    """The internal-traffic contract's outbound half, presence edition —
    without it the hub counts its own fleet pinging as bot traffic, once
    per satellite per minute, forever."""
    import requests

    seen = {}

    def fake(*args, **kwargs):
        seen.update(kwargs.get("headers") or {})
        raise RuntimeError("captured")

    monkeypatch.setattr(requests, "post", fake)
    ok, _ = sr._post_signed(sr.presence_endpoint(), {"app": "t", "active": 0},
                            "presence-beacon", secret="test-secret")
    assert ok is False
    assert INTERNAL_UA_TOKEN in seen.get("User-Agent", "")
    assert "presence-beacon" in seen.get("User-Agent", "")


def test_rollup_and_presence_use_separate_leases(ledger):
    ledger([])
    assert sr._lease_path() != sr._presence_lease_path()
    assert sr._presence_lease_path().name == ".satellite_presence.lease"
