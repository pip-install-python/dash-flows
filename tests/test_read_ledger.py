"""The app keeps the row — on_document_read → AnalyticsTracker.record_read.

dash-improve-my-llms 2.8.0 emits one event per corpus document it serves
and does no I/O with it. Before 1.6.34 nothing here listened, so tier,
verified, verdict, bytes and policy were discarded at the app boundary
exactly as the package used to discard them internally. These pins drive
the REAL app (conftest's client) and read the ledger file back.
"""

from __future__ import annotations

import json
import time
import warnings
from pathlib import Path


from conftest import BROWSER_UA

GPTBOT = "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.2; +https://openai.com/gptbot)"


def _reads(app_module):
    from lib.analytics_tracker import tracker

    tracker.flush()
    path = Path(tracker.data_file)
    if not path.exists():
        return []
    return json.loads(path.read_text()).get("reads") or []


def _new_reads(app_module, before):
    return _reads(app_module)[len(before):]


def test_one_llms_txt_fetch_writes_exactly_one_read_row(app_module, client):
    before = _reads(app_module)
    r = client.get("/llms.txt", user_agent=GPTBOT)
    assert r.status == 200
    rows = _new_reads(app_module, before)
    assert len(rows) == 1, rows
    row = rows[0]
    assert row["kind"] == "read"
    assert row["path"] == "/llms.txt"
    assert row["tier"] == "index"
    assert row["lane"] == "crawler"
    assert row["bot_type"] == "training"
    assert row["vendor_key"] == "gptbot"
    # In-process the test client carries NO client address, so the package
    # cannot check GPTBot's published ranges and says n/a; on the wire
    # (behind Cloudflare) the same request is verified/unverified. The
    # drop expected only the latter pair — the tree says the triple.
    assert row["verified"] in ("verified", "unverified", "n/a")
    assert row["verdict"] == "served"
    assert row["status"] == 200
    assert row["bytes"] > 0
    assert "client_ip" not in row, "ANALYTICS_KEEP_CLIENT_IP is off by default"
    assert row["ua"] == GPTBOT[:160]
    # policy is None until dimll 2.8.1 writes it; the rollup groups it as
    # "default". The KEY is present regardless (EVENT_FIELDS is fixed).
    assert "policy" in row


def test_a_browser_page_view_writes_no_read_row(app_module, client):
    """The package emits for the crawler document only (measured on the
    2.8.0 wheel by the ops seat); a Chrome GET / is the browser lane."""
    before = _reads(app_module)
    assert client.get("/", user_agent=BROWSER_UA).status == 200
    assert _new_reads(app_module, before) == []


def test_the_hook_is_registered_exactly_once(app_module):
    """Tests import run.py more than once per process and on_document_read
    appends; a second import must not double-write."""
    from dash_improve_my_llms import _ledger

    from lib.analytics_tracker import tracker

    assert _ledger._callbacks.count(tracker.record_read) == 1
    assert getattr(tracker, "_read_hook_registered", False) is True


def test_a_raising_writer_never_touches_the_response(app_module, client):
    """The package's fail-open: the writer raising is warned about, the
    document still goes out. Assert the warning, not silence."""
    from dash_improve_my_llms import _ledger

    def boom(event):
        raise RuntimeError("ledger disk is gone")

    _ledger._callbacks.append(boom)
    _ledger._warned.clear()
    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            r = client.get("/llms.txt", user_agent=GPTBOT)
        assert r.status == 200 and len(r.text) > 200
        msgs = [str(w.message) for w in caught if "on_document_read" in str(w.message)]
        assert msgs, "the package should warn once about a raising callback"
        assert "ledger disk is gone" in msgs[0]
    finally:
        _ledger._callbacks.remove(boom)
        _ledger._warned.clear()


def test_record_read_keeps_client_ip_only_when_asked(tmp_path, monkeypatch):
    from lib import analytics_tracker as at

    ev = {k: None for k in at.EVENT_FIELDS}
    # a CURRENT ts: the reads table shares the visits' retention window
    ev.update(ts=time.time(), path="/llms.txt", tier="index", client_ip="203.0.113.9")

    t = at.AnalyticsTracker(tmp_path / "a.json")
    t.record_read(ev)
    t.flush()
    row = json.loads((tmp_path / "a.json").read_text())["reads"][0]
    assert "client_ip" not in row and row["kind"] == "read"

    monkeypatch.setattr(at, "KEEP_CLIENT_IP", True)
    t2 = at.AnalyticsTracker(tmp_path / "b.json")
    t2.record_read(ev)
    t2.flush()
    row = json.loads((tmp_path / "b.json").read_text())["reads"][0]
    assert row["client_ip"] == "203.0.113.9"


def test_a_pre_1_6_34_ledger_gains_reads_without_losing_visits(tmp_path):
    from lib.analytics_tracker import AnalyticsTracker, EVENT_FIELDS

    p = tmp_path / "old.json"
    p.write_text(json.dumps({"visits": [{"timestamp": "2099-01-01T00:00:00",
                                         "path": "/", "device_type": "desktop",
                                         "user_agent": "x"}],
                             "stats": {"total": 1}}))
    t = AnalyticsTracker(p)
    ev = {k: None for k in EVENT_FIELDS}
    ev.update(ts=4_000_000_000.0, path="/llms.txt", tier="index")
    t.record_read(ev)
    t.flush()
    data = json.loads(p.read_text())
    assert len(data["visits"]) == 1 and len(data["reads"]) == 1
