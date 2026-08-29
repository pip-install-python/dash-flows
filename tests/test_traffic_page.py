"""/admin/traffic — the host's own ledger, behind the control board's gate."""

from __future__ import annotations

import importlib
import json
from datetime import date, datetime

import pytest

from conftest import CRAWLER_UA

from dash_improve_my_llms._ledger import EVENT_FIELDS

TODAY = date(2026, 8, 29)
YESTERDAY = date(2026, 8, 28)


def _page():
    import pages.traffic as traffic
    return importlib.reload(traffic)


def _read(day, vendor_key, verified, path="/llms.txt", tier="index", nbytes=500):
    ev = {k: None for k in EVENT_FIELDS}
    ev.update(ts=datetime(day.year, day.month, day.day, 12).timestamp(),
              path=path, method="GET", tier=tier, lane="crawler",
              bot_type="training", vendor_key=vendor_key, verified=verified,
              verdict="served", status=200, bytes=nbytes, ua="ua", kind="read")
    ev.pop("client_ip")
    return ev


@pytest.fixture
def fixture_ledger(tmp_path, monkeypatch):
    """3 vendors × 2 days, with distinct counts so a cell cannot pass by luck."""
    reads = (
        [_read(TODAY, "gptbot", "unverified")] * 5
        + [_read(YESTERDAY, "gptbot", "unverified")] * 2
        + [_read(TODAY, "claudebot", "n/a", path="/backends/llms.txt", tier="page")] * 3
        + [_read(YESTERDAY, "claudebot", "n/a")] * 1
        + [_read(TODAY, "googlebot", "verified", path="/sitemap.xml", tier="sitemap")] * 7
        + [_read(YESTERDAY, "googlebot", "verified")] * 4
    )
    p = tmp_path / "visitor_analytics.json"
    p.write_text(json.dumps({"visits": [], "reads": reads}))
    monkeypatch.setenv("TRAFFIC_ANALYTICS_FILE", str(p))
    return p


def test_the_page_is_hidden_from_every_machine_surface(app_module, client):
    from dash_improve_my_llms import is_hidden

    assert is_hidden("/admin/traffic")
    assert "/admin/traffic</loc>" not in client.get("/sitemap.xml").text
    assert "/admin/traffic" not in client.get("/llms.txt").text
    # and a crawler asking for it gets the package's 404, like the board
    assert client.get("/admin/traffic", user_agent=CRAWLER_UA).status == \
        client.get("/admin/control-board", user_agent=CRAWLER_UA).status


def test_anonymous_is_denied_exactly_like_the_control_board(app_module, monkeypatch):
    import pages.control_board as board
    traffic = _page()
    monkeypatch.delenv("ALLOW_UNGATED_ADMIN", raising=False)
    ours, theirs = str(traffic.layout()), str(board.layout())
    assert "traffic-day" not in ours
    assert "404" in ours and "not currently published" in ours
    assert ours == theirs, "the two admin pages must fail closed identically"


def test_the_tables_render_the_fixture_numbers(app_module, monkeypatch, fixture_ledger):
    traffic = _page()
    monkeypatch.setenv("ALLOW_UNGATED_ADMIN", "1")
    from lib.traffic_rollup import load_reads

    reads = load_reads()
    days = traffic._window(TODAY)
    rows, cells, nbytes = traffic.vendor_by_day(reads, days)
    assert rows == [("googlebot", "verified"), ("gptbot", "unverified"),
                    ("claudebot", "n/a")]
    assert cells[(("googlebot", "verified"), TODAY)] == 7
    assert cells[(("googlebot", "verified"), YESTERDAY)] == 4
    assert cells[(("gptbot", "unverified"), TODAY)] == 5
    assert cells[(("gptbot", "unverified"), YESTERDAY)] == 2
    assert cells[(("claudebot", "n/a"), TODAY)] == 3
    assert cells[(("claudebot", "n/a"), YESTERDAY)] == 1
    assert nbytes[("googlebot", "verified")] == 11 * 500

    rendered = str(traffic._build_page(TODAY, reads))
    for cell in ("googlebot · verified", "gptbot · unverified", "claudebot · n/a",
                 "'7'", "'5'", "'3'", "'4'", "'2'", "'1'"):
        assert cell in rendered, cell
    # vendor → tier for TODAY
    day = str(traffic.day_view(TODAY, reads))
    assert "traffic-vendor-tier" in day
    assert "/backends/llms.txt" in day and "/sitemap.xml" in day
    # the verified legend, so the owner reads n/a as a vendor property
    assert "Anthropic does not" in rendered
    assert "traffic-day" in rendered


def test_the_gate_opens_locally_with_the_dev_override(app_module, monkeypatch, fixture_ledger):
    traffic = _page()
    monkeypatch.setenv("ALLOW_UNGATED_ADMIN", "1")
    assert "traffic-day" in str(traffic.layout())
