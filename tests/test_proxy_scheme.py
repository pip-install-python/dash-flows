"""The forwarded-scheme fix — `lib/proxy.py`.

TEMPLATE FILE: satellites copy this verbatim.

What shipped to production and stayed there: Dash builds `twitter:url` from
`request.url`, the request arrives over Cloudflare -> Render -> gunicorn, and
the last hop is plain HTTP, so every social scraper was told

    <meta property="twitter:url" content="http://boilerplate.2plot.dev/">

`og:url` looked right the whole time because `templates/index.html` hard-codes
it, and the template's client-side URL sync cannot help either — scrapers do
not run JavaScript. So the only place this is observable from inside the
codebase is here.

The unit tests below drive the middleware directly rather than through the
test client, because a test client synthesises its own environ and would not
reproduce a proxy hop. `test_the_tag_dash_emits_follows_the_forwarded_scheme`
is the end-to-end one: it asserts the actual meta tag, which is the thing that
was wrong.
"""

from __future__ import annotations

import re

import pytest

from conftest import BROWSER_UA, backend
from lib import proxy


def _wsgi_scheme(environ_extra: dict) -> str:
    """Run the WSGI middleware over a synthetic environ, return the scheme."""
    seen = {}

    def inner(environ, start_response):
        seen["scheme"] = environ["wsgi.url_scheme"]
        start_response("200 OK", [])
        return [b""]

    environ = {"wsgi.url_scheme": "http", **environ_extra}
    proxy._wsgi_proxy_fix(inner)(environ, lambda *a, **k: None)
    return seen["scheme"]


# ------------------------------------------------------------ the mechanism --


def test_a_forwarded_https_hop_is_believed():
    assert _wsgi_scheme({"HTTP_X_FORWARDED_PROTO": "https"}) == "https"


def test_no_header_leaves_the_scheme_alone():
    """Local development over plain HTTP must not start claiming TLS."""
    assert _wsgi_scheme({}) == "http"


def test_a_forwarded_http_hop_is_also_believed():
    assert _wsgi_scheme({"HTTP_X_FORWARDED_PROTO": "http"}) == "http"


def test_the_first_hop_wins_in_a_proxy_chain():
    """`X-Forwarded-Proto: https, http` means the CLIENT used https.

    Each proxy appends, exactly as with X-Forwarded-For, so the last entry is
    the hop nearest the app — the plaintext one we are trying to see past.
    Reading the list from the wrong end reinstates the original defect and
    looks correct in a single-proxy test.
    """
    assert _wsgi_scheme({"HTTP_X_FORWARDED_PROTO": "https, http"}) == "https"
    assert _wsgi_scheme({"HTTP_X_FORWARDED_PROTO": "  https ,http"}) == "https"


def test_the_older_ssl_header_is_understood():
    assert _wsgi_scheme({"HTTP_X_FORWARDED_SSL": "on"}) == "https"


def test_junk_is_ignored_rather_than_trusted():
    for value in ("", "   ", "gopher", "https-ish", ","):
        assert _wsgi_scheme({"HTTP_X_FORWARDED_PROTO": value}) == "http", value


def test_the_kill_switch_disables_it(monkeypatch):
    """An app exposed directly to the internet must be able to turn this off.

    Without a proxy in front, a client can set X-Forwarded-Proto itself and a
    plaintext request could claim to be secure.
    """
    monkeypatch.setenv("TRUST_PROXY_HEADERS", "0")
    assert proxy.enabled() is False
    assert proxy.apply(object(), "flask") is False


def test_it_is_on_by_default(monkeypatch):
    monkeypatch.delenv("TRUST_PROXY_HEADERS", raising=False)
    assert proxy.enabled() is True


# --------------------------------------------------------------- the wiring --


def test_run_py_applied_it(app_module):
    """It has to be wired in, not merely importable."""
    assert app_module.PROXY_FIX_APPLIED is True


@pytest.mark.skipif(backend() != "flask", reason="WSGI-only assertion")
def test_the_server_callable_is_wrapped_not_replaced(app, app_module):
    """`app.server` must stay the Flask object.

    gunicorn imports it as `run:server` and `run.py` hangs `before_request`
    off it; wrapping the outer object instead of its `wsgi_app` would break
    the entrypoint and the analytics hook at once.
    """
    assert app.server is app_module.server
    assert hasattr(app.server, "before_request")
    assert callable(app.server.wsgi_app)


# ------------------------------------------------------------- end to end --


@pytest.mark.skipif(backend() != "flask", reason="one backend proves the tag")
def test_the_tag_dash_emits_follows_the_forwarded_scheme(app):
    """The actual defect: `twitter:url`, as a social scraper receives it.

    The request NAMES the browser lane. Since dash-improve-my-llms 2.8.0
    a request with no User-Agent is classified as a crawler and receives
    the crawler document, which carries no `twitter:url` at all — so a
    UA-less probe here fails on "no tag" without saying anything about
    the scheme (found by the 1.6.34 floor bump: green on 2.7.1, red on
    2.8.0, on every Flask leg). Either lane can be the one you did not
    mean to test; the browser one is the one this tag lives in.
    """
    client = app.server.test_client()
    html = client.get(
        "/",
        headers={
            "X-Forwarded-Proto": "https",
            "Host": "boilerplate.2plot.dev",
            "User-Agent": BROWSER_UA,
        },
    ).get_data().decode("utf-8", "replace")

    urls = re.findall(
        r'<meta[^>]*property="twitter:url"[^>]*content="([^"]*)"', html
    )
    assert urls, "no twitter:url tag at all"
    for url in urls:
        assert url.startswith("https://"), (
            f"twitter:url={url!r} — a scraper records this verbatim"
        )
