"""``GET /api/agent-key`` — the person→agent handoff, satellite side.

A signed-in reader clicks "Copy for LLM" and gets a URL that still works
after it is pasted into an assistant, because the assistant's fetch arrives
with no cookie. This route turns the browser's Clerk session into that
portable authority: it reads the ``__session`` cookie and asks the hub to
mint (or return) the reader's current agent key via
:func:`lib.hub_client.current_key` — the hub verifies the token against
Clerk's JWKS and pins ``scope=auth``, so a satellite can never mint an admin
key and never asserts an identity of its own.

Contract (mirror of pip-docs+ ``/api/agent-key``):

- 204, no body — anonymous request, Clerk off, or the hub declined/was
  unreachable. The caller copies the plain URL, which is exactly what an
  anonymous reader gets anyway.
- 200 ``{"key": "k2p_…"}`` with ``Cache-Control: private, no-store`` — the
  key must never enter a shared cache; it is why the key is fetched on click
  rather than embedded in the page HTML.

Consumed by ``assets/llms_copy.js`` (lazily, on the first copy click — every
call is a hub round trip and each mint is recorded hub-side).

No ``from __future__ import annotations`` here, deliberately: PEP 563 turns
the FastAPI handler's ``request: Request`` into a string that FastAPI then
tries to resolve from module globals — where the locally imported ``Request``
does not exist — and the parameter silently becomes a required query field
(422 on every call).
"""

_NO_STORE = "private, no-store"


def _mint() -> str | None:
    """The current request's agent key, or None. Never raises."""
    try:
        from flask import request

        token = (request.cookies.get("__session") or "").strip()
    except Exception:
        return None
    return _mint_from_token(token)


def _mint_from_token(token: str) -> str | None:
    if not token:
        return None
    try:
        from lib import auth, hub_client

        if not auth.clerk_enabled():
            return None
        return hub_client.current_key(token)
    except Exception:
        return None


def register_agent_key_route(app, backend: str) -> None:
    """Mount ``/api/agent-key`` on whichever backend is running."""
    server = app.server

    if backend == "fastapi":
        from fastapi import Request
        from fastapi.responses import JSONResponse, Response

        @server.get("/api/agent-key")
        def _agent_key(request: Request):  # sync: runs in the threadpool
            token = (request.cookies.get("__session") or "").strip()
            key = _mint_from_token(token)
            if not key:
                return Response(status_code=204,
                                headers={"Cache-Control": _NO_STORE})
            return JSONResponse({"key": key},
                                headers={"Cache-Control": _NO_STORE})

    elif backend == "quart":
        from quart import jsonify, request

        @server.get("/api/agent-key")
        async def _agent_key():  # pragma: no cover — quart runtime
            token = (request.cookies.get("__session") or "").strip()
            key = _mint_from_token(token)
            if not key:
                return "", 204, {"Cache-Control": _NO_STORE}
            resp = jsonify({"key": key})
            resp.headers["Cache-Control"] = _NO_STORE
            return resp

    else:
        from flask import jsonify

        @server.get("/api/agent-key")
        def _agent_key():
            key = _mint()
            if not key:
                return "", 204, {"Cache-Control": _NO_STORE}
            resp = jsonify({"key": key})
            resp.headers["Cache-Control"] = _NO_STORE
            return resp
