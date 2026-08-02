"""SPA page-view beacon — counts client-side route changes as visits.

THIS APP'S OWN ENHANCEMENT over the network-standard analytics stack (only
flows and mui-charts carry it so far). A Dash multi-page app serves ONE HTML
request per visit; every later page is a client-side route change that never
hits the server. Counting only requests would report every session as
single-page — ``pages`` would list entry pages only and ``median_session_s``
would always be null. So the browser beacons each route change to
``/api/pageview`` (same origin, ``keepalive``) and the handler feeds it into
``lib.analytics_tracker.tracker`` like any other visit.

Bots don't run JS, so bot hits stay request-only — which is correct.

Three pieces, wired from run.py / components/appshell.py:

    register_pageview_route(app, backend)   # the POST endpoint, per backend
    beacon_component()                      # hidden Store in the app shell
    register_pageview_beacon()              # the clientside callback

``lib/analytics_tracker.py`` skips ``/api/`` at write time, so the beacon
POST itself is never double-counted alongside the path it carries.
"""
from __future__ import annotations

import json
from typing import Any

try:
    # MUST be module level: with `from __future__ import annotations` the
    # FastAPI handler's `request: Request` hint stays a string that FastAPI
    # resolves against THIS module's globals. Imported inside a function it
    # would be unresolvable and FastAPI would treat `request` as a required
    # query param — every beacon would 422.
    from starlette.requests import Request
except ImportError:  # flask/quart-only install — the fastapi branch never runs
    Request = Any  # type: ignore[misc,assignment]


def _pageview_path(raw: bytes) -> str | None:
    """The path out of a beacon body — `{"path": "/docs/nodes"}`."""
    try:
        path = json.loads(raw or b"{}").get("path")
    except Exception:
        return None
    return path if isinstance(path, str) and path.startswith("/") else None


def _track(headers: dict, path: str, remote_addr: str | None) -> None:
    from lib.analytics_tracker import tracker

    ua = {str(k).lower(): v for k, v in headers.items()}.get("user-agent", "")
    try:
        tracker.track_visit(path, ua, remote_addr, headers=headers)
    except Exception:  # noqa: BLE001 — analytics must never break a request
        pass


def register_pageview_route(app, backend: str) -> None:
    """Install ``POST /api/pageview`` on whichever backend serves the app."""
    server = app.server

    if backend == "fastapi":
        from starlette.responses import JSONResponse

        @server.post("/api/pageview", include_in_schema=False)
        async def _pageview(request: Request):  # pragma: no cover
            path = _pageview_path(await request.body())
            if path:
                client = request.client
                _track(dict(request.headers), path,
                       client.host if client else None)
            return JSONResponse({"ok": bool(path)},
                                status_code=200 if path else 400)

    elif backend == "quart":
        from quart import jsonify, request

        @server.post("/api/pageview")
        async def _pageview():  # pragma: no cover
            path = _pageview_path(await request.get_data())
            if path:
                _track(dict(request.headers), path, request.remote_addr)
            return jsonify({"ok": bool(path)}), 200 if path else 400

    else:
        from flask import jsonify, request

        @server.post("/api/pageview")
        def _pageview():
            path = _pageview_path(request.get_data())
            if path:
                _track(dict(request.headers), path, request.remote_addr)
            return jsonify({"ok": bool(path)}), 200 if path else 400


def register_pageview_beacon(location_id: str = "url") -> None:
    """Beacon every client-side route change to ``/api/pageview``.

    ``prevent_initial_call=True`` keeps the entry page out of it — that one
    already arrived as a real HTTP request. Output is the hidden Store from
    :func:`beacon_component`; nothing reads it.
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
