"""/api/agent-key — the person→agent handoff (lib/agent_key.py).

Contract pins: 204 for anonymous/Clerk-off/hub-down (the copy button falls
back to the plain URL), 200 + private,no-store for a minted key, the token
read from the __session cookie and never from the query string.
"""

from __future__ import annotations

import flask
import pytest

from lib import agent_key

NO_STORE = "private, no-store"


class _App:
    def __init__(self, server):
        self.server = server


@pytest.fixture
def route_client():
    server = flask.Flask(__name__)
    agent_key.register_agent_key_route(_App(server), "flask")
    return server.test_client()


def test_anonymous_gets_204_with_no_store(route_client):
    r = route_client.get("/api/agent-key")
    assert r.status_code == 204
    assert r.headers["Cache-Control"] == NO_STORE


def test_a_minted_key_returns_200_json_with_no_store(route_client, monkeypatch):
    monkeypatch.setattr(agent_key, "_mint_from_token",
                        lambda t: "k2p_minted" if t == "tok" else None)
    route_client.set_cookie("__session", "tok")
    r = route_client.get("/api/agent-key")
    assert r.status_code == 200
    assert r.get_json() == {"key": "k2p_minted"}
    assert r.headers["Cache-Control"] == NO_STORE


def test_the_token_is_read_from_the_cookie_never_the_query(route_client, monkeypatch):
    seen = []
    monkeypatch.setattr(agent_key, "_mint_from_token",
                        lambda t: seen.append(t) or None)
    route_client.get("/api/agent-key?token=forged&__session=forged2")
    assert seen == [""], "a query-string token reached the mint path"


def test_mint_is_none_when_clerk_is_off(monkeypatch):
    from lib import auth

    monkeypatch.setattr(auth, "clerk_enabled", lambda: False)
    assert agent_key._mint_from_token("tok") is None


def test_mint_passes_the_token_to_the_hub(monkeypatch):
    from lib import auth, hub_client

    monkeypatch.setattr(auth, "clerk_enabled", lambda: True)
    monkeypatch.setattr(hub_client, "current_key",
                        lambda tok: "k2p_x" if tok == "tok" else None)
    assert agent_key._mint_from_token("tok") == "k2p_x"
    assert agent_key._mint_from_token("") is None


def test_a_hub_failure_degrades_to_none_never_raises(monkeypatch):
    from lib import auth, hub_client

    monkeypatch.setattr(auth, "clerk_enabled", lambda: True)

    def boom(tok):
        raise RuntimeError("hub exploded")

    monkeypatch.setattr(hub_client, "current_key", boom)
    assert agent_key._mint_from_token("tok") is None


def test_the_route_is_mounted_on_the_running_app(client):
    """End to end on whichever backend the suite runs: Clerk is off in the
    test env, so the route answers 204 — mounted, safe, and cache-proof."""
    r = client.get("/api/agent-key")
    assert r.status == 204
    assert r.header("Cache-Control") == NO_STORE
