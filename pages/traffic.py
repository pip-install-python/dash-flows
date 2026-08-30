"""/admin/traffic — this host's own ledger, read from the wire it served.

The read table dash-improve-my-llms 2.8.0 emits (``on_document_read``, kept
by ``lib.analytics_tracker.AnalyticsTracker.record_read``) is what makes
"does ClaudeBot actually get the corpus here?" answerable from the host
itself, before the hub folds anything: vendor × day, vendor → tier, and the
paths each vendor pulled, next to the v3 headline numbers for the same day
so the two systems can be eyeballed together.

Reads ``visitor_analytics.json`` directly — no hub call, last 14 days.

Access: the control board's exact gate (``lib.auth.is_admin_user`` /
``admin_access_open()``); fails CLOSED without Clerk, exactly as
``pages/control_board.py`` does and for the same reason. Set
``ALLOW_UNGATED_ADMIN=1`` to work on it locally.

Render-cost rule (fleet fact 18, measured on the hub 2026-08-28): plain
tables, NO charts, mount once, no interval callback. A 14 × 40 table of
strings costs about a millisecond; five charts cost ten seconds. The day
picker is the only control.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime, timedelta

import dash
import dash_mantine_components as dmc
from dash import Input, Output, callback, html
from dash_iconify import DashIconify

from lib.auth import admin_access_open, clerk_enabled, current_user, is_admin_user
from lib.constants import OG_IMAGE_URL, PAGE_TITLE_PREFIX
from lib.gate_layouts import forbidden_layout, hidden_layout, sign_in_layout
from lib.traffic_rollup import daily_rollup, load_reads, vendor_rows

TRAFFIC_PATH = "/admin/traffic"
DAYS = 14
TOP_VENDORS = 8
TOP_PATHS = 10

try:
    # Same treatment as the control board: sitemap exclusion, llms.txt 404,
    # no MCP resource, no prerender, crawler 404 — from the package's own
    # hidden set, so it holds on forks whose lib.access is not wired.
    from dash_improve_my_llms import mark_hidden

    mark_hidden(TRAFFIC_PATH)
except Exception:  # pragma: no cover — the optional-SEO degrade
    pass

dash.register_page(
    __name__,
    path=TRAFFIC_PATH,
    name="Traffic",
    title=PAGE_TITLE_PREFIX + "Traffic",
    description="This host's own crawler ledger — vendor, tier and verification per day.",
    image_url=OG_IMAGE_URL,
)


# --------------------------------------------------------------- the data --


def _window(today: date | None = None) -> list[date]:
    today = today or datetime.now().date()
    return [today - timedelta(days=n) for n in range(DAYS - 1, -1, -1)]


def _vendor_label(key, verified) -> str:
    return f"{key or '(unidentified)'} · {verified}"


def vendor_by_day(reads, days) -> tuple[list[tuple], dict, dict]:
    """``(rows, cells, bytes_total)`` where rows are ``(key, verified)`` sorted
    by total hits desc, ``cells[(row, day)]`` is hits and ``bytes_total[row]``
    the window's byte sum."""
    cells: dict = defaultdict(int)
    totals: dict = defaultdict(int)
    nbytes: dict = defaultdict(int)
    wanted = set(days)
    for r in reads:
        d = r["dt"].date()
        if d not in wanted:
            continue
        row = (r.get("vendor_key"), r.get("verified") or "n/a")
        cells[(row, d)] += 1
        totals[row] += 1
        try:
            nbytes[row] += int(r.get("bytes") or 0)
        except (TypeError, ValueError):
            pass
    rows = sorted(totals, key=lambda k: (-totals[k], k[0] or "~"))
    return rows, cells, nbytes


def top_paths(reads_day) -> list[tuple]:
    """``[(key, verified, [(path, hits), ...]), ...]`` — top vendors, top paths."""
    by_vendor: dict = defaultdict(lambda: defaultdict(int))
    totals: dict = defaultdict(int)
    for r in reads_day:
        row = (r.get("vendor_key"), r.get("verified") or "n/a")
        by_vendor[row][r.get("path") or "?"] += 1
        totals[row] += 1
    out = []
    for row in sorted(totals, key=lambda k: (-totals[k], k[0] or "~"))[:TOP_VENDORS]:
        paths = sorted(by_vendor[row].items(), key=lambda kv: (-kv[1], kv[0]))
        out.append((row[0], row[1], paths[:TOP_PATHS]))
    return out


# -------------------------------------------------------------- the tables --


def _table(head, body_rows, **kw):
    return dmc.Table(
        [
            dmc.TableThead(dmc.TableTr([dmc.TableTh(h) for h in head])),
            dmc.TableTbody(
                [dmc.TableTr([dmc.TableTd(c) for c in row]) for row in body_rows]
            ),
        ],
        striped=True,
        highlightOnHover=True,
        withTableBorder=True,
        fz="xs",
        **kw,
    )


def _fmt_bytes(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} GB"  # pragma: no cover


def vendor_day_table(reads, days):
    rows, cells, nbytes = vendor_by_day(reads, days)
    head = ["vendor · verified"] + [d.strftime("%m-%d") for d in days] + ["bytes"]
    body = [
        [_vendor_label(*row)]
        + [str(cells.get((row, d), 0)) or "" for d in days]
        + [_fmt_bytes(nbytes[row])]
        for row in rows
    ]
    if not body:
        return dmc.Text("No read events in the last 14 days.", c="dimmed", size="sm")
    return _table(head, body, id="traffic-vendor-day")


def vendor_tier_table(reads_day):
    from dash_improve_my_llms._ledger import TIERS

    rows = vendor_rows(reads_day)
    head = ["vendor", "class", "verified", "policy", "hits", "bytes"] + list(TIERS)
    body = [
        [
            str(r["key"] or "(unidentified)"),
            str(r["class"] or "—"),
            r["verified"],
            r["policy"],
            str(r["hits"]),
            _fmt_bytes(r["bytes"]),
        ]
        + [str(r["tiers"][t]) for t in TIERS]
        for r in rows
    ]
    if not body:
        return dmc.Text("No read events on this day.", c="dimmed", size="sm")
    return _table(head, body, id="traffic-vendor-tier")


def top_paths_block(reads_day):
    blocks = []
    for key, verified, paths in top_paths(reads_day):
        blocks.append(
            dmc.Stack(
                [
                    dmc.Text(_vendor_label(key, verified), fw=600, size="sm"),
                    _table(["path", "hits"], [[p, str(n)] for p, n in paths]),
                ],
                gap=4,
            )
        )
    if not blocks:
        return dmc.Text("No paths on this day.", c="dimmed", size="sm")
    return dmc.SimpleGrid(blocks, cols={"base": 1, "md": 2}, spacing="md")


def _stat_cards(stats):
    return dmc.Group(
        [
            dmc.Paper(
                dmc.Stack(
                    [
                        dmc.Text(str(v), size="24px", fw=700, id=f"traffic-stat-{k.replace(' ', '-')}"),
                        dmc.Text(k, size="xs", c="dimmed", tt="uppercase"),
                    ],
                    gap=2,
                    align="center",
                ),
                withBorder=True,
                radius="md",
                p="sm",
                style={"minWidth": "110px"},
            )
            for k, v in stats
        ],
        gap="sm",
    )


def people_block(day: date):
    """PEOPLE — the v3 human numbers, in their own section (owner requirement
    11, 2026-08-30). Humans never enter the read ledger: the package emits a
    read event for the crawler document only, so the tables below this
    section are crawlers, and "unidentified" there is the UA-less crawler
    lane, never a person."""
    from lib.satellite_reporter import app_key

    payload = daily_rollup(app_key(), day) or {}
    median = payload.get("median_session_s")
    stats = [
        ("human hits", payload.get("human_hits", 0)),
        ("visitors", payload.get("visitors", 0)),
        ("sessions", payload.get("sessions", 0)),
        ("median session", f"{int(median)} s" if median is not None else "—"),
    ]
    return dmc.Stack(
        [
            dmc.Title("People", order=4),
            _stat_cards(stats),
            dmc.Text(
                "Humans never enter the read ledger — the tables below are crawlers only. "
                "\"(unidentified)\" there is the crawler lane with no vendor match, never a person.",
                size="xs", c="dimmed", id="traffic-people-note",
            ),
        ],
        gap="xs",
        id="traffic-people",
    )


def headline_block(day: date):
    """The v3 crawler numbers for the same day, beside the ledger's own."""
    from lib.satellite_reporter import app_key

    payload = daily_rollup(app_key(), day) or {}
    return _stat_cards([
        ("bot hits", payload.get("bot_hits", 0)),
        ("bot visitors", payload.get("bot_visitors", 0)),
        ("reads", payload.get("reads", 0)),
    ])


def day_view(day: date, reads=None):
    """Everything below the day picker, for one day. Pure of Dash callbacks
    so a test can drive it directly."""
    reads = load_reads() if reads is None else reads
    reads_day = [r for r in reads if r["dt"].date() == day]
    return dmc.Stack(
        [
            dmc.Text(f"Selected day: {day.isoformat()}", size="sm", c="dimmed"),
            people_block(day),
            dmc.Title("Crawlers", order=4),
            headline_block(day),
            dmc.Title("Vendor → tier", order=4),
            vendor_tier_table(reads_day),
            dmc.Title("Top paths per vendor", order=4),
            top_paths_block(reads_day),
        ],
        gap="sm",
        id="traffic-day-view",
    )


def _footnote():
    try:
        from dash_improve_my_llms import __version__ as pkg_version
    except Exception:  # pragma: no cover
        pkg_version = "?"
    return dmc.Text(
        [
            f"Rows come from dash-improve-my-llms {pkg_version}'s read events "
            "(one per corpus document served). ",
            html.B("verified"),
            " means the request came from an IP range the vendor publishes; ",
            html.B("unverified"),
            " means it did not; ",
            html.B("n/a"),
            " means the operator publishes no ranges at all — Anthropic does "
            "not, so ClaudeBot is always n/a here. That is a property of the "
            "vendor, not a defect on this host. The (unidentified) row is the "
            "crawler lane with no vendor match — UA-less and library clients.",
        ],
        size="xs",
        c="dimmed",
    )


def day_picker(days, reads):
    """`dmc.DatePickerInput` — a picker, not a plain dropdown (the fleet's
    DMC-first rule, 2026-08-30): bounded by the ledger's first and last
    day, with presets for the days someone actually asks about."""
    today = days[-1]
    have = sorted({r["dt"].date() for r in reads}) or [today]
    lo, hi = min(have[0], days[0]), max(have[-1], today)
    presets = [
        {"value": today.isoformat(), "label": "Today"},
        {"value": (today - timedelta(days=1)).isoformat(), "label": "Yesterday"},
        {"value": (today - timedelta(days=6)).isoformat(), "label": "Last 7 days (start)"},
    ]
    return dmc.Group(
        [
            dmc.Text("Day", size="sm", fw=600),
            dmc.DatePickerInput(
                id="traffic-day",
                value=today.isoformat(),
                minDate=lo.isoformat(),
                maxDate=hi.isoformat(),
                valueFormat="YYYY-MM-DD",
                presets=presets,
                clearable=False,
                w=200,
                leftSection=DashIconify(icon="tabler:calendar", width=16),
                **{"aria-label": "Ledger day"},
            ),
        ],
        gap="sm",
    )


def _build_page(today: date | None = None, reads=None):
    days = _window(today)
    reads = load_reads() if reads is None else reads
    return dmc.Container(
        dmc.Stack(
            [
                dmc.Title("Traffic — this host's ledger", order=2),
                _footnote(),
                dmc.Title("Vendor × day (hits)", order=4),
                html.Div(vendor_day_table(reads, days), style={"overflowX": "auto"}),
                day_picker(days, reads),
                html.Div(day_view(days[-1], reads), id="traffic-day-container"),
            ],
            gap="md",
        ),
        size="xl",
        py="xl",
    )


def layout(**kwargs):
    """Admin-gated at render time; ``**kwargs`` absorbs Clerk handshake params."""
    if clerk_enabled():
        user = current_user()
        if user is None:
            return sign_in_layout("Traffic")
        if not is_admin_user(user):
            return forbidden_layout("Traffic")
    elif not admin_access_open():
        # Fail CLOSED, like the control board: this page lists which vendors
        # pull which documents from this host, which is operator information.
        return hidden_layout()
    return _build_page()


@callback(
    Output("traffic-day-container", "children"),
    Input("traffic-day", "value"),
    prevent_initial_call=True,
)
def _select_day(value):
    # Same server-side re-check as the control board's write callback: a
    # gated layout only hides the UI, the callback endpoint is open to a
    # reconstructed request.
    if clerk_enabled():
        if not is_admin_user():
            raise dash.exceptions.PreventUpdate
    elif not admin_access_open():
        raise dash.exceptions.PreventUpdate
    try:
        day = date.fromisoformat(value)
    except (TypeError, ValueError):
        raise dash.exceptions.PreventUpdate
    return day_view(day)
