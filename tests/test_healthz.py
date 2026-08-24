"""The /healthz probe contract.

Four pins ported from the boilerplate's tests/test_llms_routes.py (template
1.6.10 4523c69, 1.6.12 9462aff), adapted to where this fork keeps the payload.

WHY THEY LOOK DIFFERENT FROM THE TEMPLATE'S: the template factored the probe
into lib/health.py + lib/asgi_routes.py because its three backends each
registered their own route and the FastAPI one had silently drifted — it built
its own body and forgot `build`, the exact field cd.yml's build-match wait
polls for. This fork never had that split: all three backends here render from
the ONE `_health_body()` in run.py and always have, so both of the defects
1.6.10 fixed were already absent. Porting lib/health.py verbatim would have
created a SECOND source of truth for a payload whose shape this fork does not
share anyway (`app`/`version`/`dash`/`reporting`, which scripts/network_smoke.py
asserts by name, against the template's `ok`/`backend`/`dash_version`). What is
ported is the contract: per-request construction, the identity field, the geo
diagnostic, and each backend handing its own headers through.
"""

import json

import pytest


@pytest.fixture(scope="module")
def probe(app):
    """A raw Werkzeug client and a JSON reader for it.

    Not the shared `client` fixture: that wrapper takes a user_agent and an
    accept and nothing else — it is shaped for the page tests — and these
    need an arbitrary request header (CF-IPCountry) and a decoded body.
    Kept local rather than widening the fleet-shared wrapper for one file.
    """
    raw = app.server.test_client()

    def get(path="/healthz", **headers):
        return json.loads(raw.get(path, headers=headers).get_data().decode())

    return get


def test_healthz_is_live_not_a_snapshot(probe, monkeypatch):
    """The payload must be built per request, not closed over at registration.

    A snapshot was harmless while every field was static — ok/version/dash
    never change for a running process — and silently wrong the moment one is
    not. `geo` is that field: /healthz is registered ~90 lines before
    `lib.access.configure()` runs, so a value captured at registration would
    report the guardrail unconfigured on a host where it IS configured, the
    diagnostic lying in exactly the situation it exists for.

    Pinned through `build`, which reads its env var at call time and is
    trivially observable, rather than through geo state that needs a
    configured denylist to move.
    """
    monkeypatch.setenv("RENDER_GIT_COMMIT", "cafebabe")
    assert probe()["build"] == "cafebabe"

    monkeypatch.setenv("RENDER_GIT_COMMIT", "deadbeef")
    assert probe()["build"] == "deadbeef", (
        "the second request served the first request's payload — /healthz is "
        "snapshotting again"
    )

    monkeypatch.delenv("RENDER_GIT_COMMIT")
    assert "build" not in probe(), (
        "`build` must be OMITTED where the platform variable does not exist, "
        "so the fleet's probe contract is unchanged off-Render"
    )


def test_healthz_identity_fields(app_module, monkeypatch):
    """`build` says which commit answered, `app` says which satellite.

    Different questions on a fleet where every host shares one template and a
    hostname can be repointed between services. `app` here comes from
    lib.satellite_reporter.app_key(), so its no-env fallback is "boilerplate"
    — NOT the template's "unknown". That is deliberate and load-bearing: the
    reporter is byte-identical fleet-wide (shasum acceptance), so identity is
    claimed by run.py's fork point instead, and tests/test_bulletin.py pins
    both halves. A fallback of "boilerplate" reaching production would mean
    the fork point stopped running before the first hub-facing import.
    """
    monkeypatch.setenv("RENDER_GIT_COMMIT", "cafebabe")
    body = app_module._health_body()
    assert body["build"] == "cafebabe"
    assert body["app"] == "flows"

    monkeypatch.delenv("SATELLITE_APP_KEY")
    assert app_module._health_body()["app"] == "boilerplate", (
        "the reporter's byte-identical fallback changed — see "
        "tests/test_bulletin.py, this is the fork-point contract"
    )


def test_healthz_geo_block_is_counts_not_codes(app_module):
    """Present on dash-improve-my-llms >= 2.7.0, OMITTED on older packages.

    Counts and flags only — never the denylist's country codes. A health
    endpoint is not where anyone should learn policy. Omitted rather than
    error-flagged below the floor because a host on an older package is not
    broken, it predates the diagnostic — which also makes the block's ABSENCE
    in production the tell that a floor bump never reached the image through
    the Docker cache.
    """
    body = app_module._health_body()
    try:
        from dash_improve_my_llms import geo  # noqa: F401
    except ImportError:  # pragma: no cover — the floor is >=2.7.1
        assert "geo" not in body
    else:
        block = body["geo"]
        assert isinstance(block["configured"], bool)
        assert isinstance(block["denied"], int), "counts, never country codes"
        assert "resolved" in block
        # Nothing in the block may leak the policy itself.
        assert "deny_countries" not in json.dumps(block)


def test_healthz_resolves_this_requests_country(probe):
    """THIS request's headers must reach geo's `resolved`.

    geo can be fully configured with a denylist and still never match if the
    country header is not reaching the app; `resolved` is what localises that
    failure from outside, and it is the per-host check docs/GEO.md calls
    mandatory before trusting a denylist. The template's first cut read
    Flask's request context unconditionally, which made the FastAPI and Quart
    lanes answer "no request context" forever (pannellum's production
    /healthz, 2026-08-23) — this fork deploys flask, but DASH_BACKEND is a
    supported env var here, so every route hands its own headers through.

    A CONTRACT PIN, NOT THE REGRESSION ALARM. Deleting the flask route's
    `headers=` argument leaves this test passing: inside a Flask request the
    module's own fallback reads the same headers off the request context, so
    the two paths are indistinguishable on the deployed backend. The lane
    that actually breaks — a Starlette or Quart request, which the fallback
    can never see — is not reachable from this suite (conftest pins
    DASH_BACKEND=flask and hands out a Werkzeug client). The test below is
    the one that fires.
    """
    body = probe(**{"CF-IPCountry": "FR"})
    if not body.get("geo"):  # pragma: no cover — the floor is >=2.7.1
        return
    assert "FR" in body["geo"]["resolved"], body["geo"]

    plain = probe()
    assert plain["geo"]["resolved"] == "unknown", (
        "a request with no country header must resolve to 'unknown', not to "
        "the previous caller's country"
    )


def test_resolved_country_reads_the_headers_it_is_given(app_module):
    """The pannellum defect, pinned where it is actually reachable.

    `_resolved_country` must answer from the headers HANDED TO IT, with no
    request context anywhere — that is precisely the situation the FastAPI
    and Quart routes call it in, and precisely what the template's first cut
    got wrong by reading Flask's context unconditionally. Called outside any
    request context on purpose: without the explicit-headers branch this
    returns "no request context" and the assertion fires. The route-level
    test above cannot make this distinction, because on flask the fallback
    reads the same headers.
    """
    from flask import has_request_context

    assert not has_request_context(), "this pin is meaningless inside a request"

    resolved = app_module._resolved_country({"CF-IPCountry": "DE"})
    assert "DE" in resolved, (
        f"_resolved_country ignored the headers it was passed (got {resolved!r})"
        " — the FastAPI and Quart lanes would report 'no request context' "
        "forever"
    )
    assert app_module._resolved_country({}) == "unknown"
