"""Make the app see the scheme the *client* used, not the last proxy hop.

TEMPLATE FILE: satellites copy this verbatim and call it from `run.py`.

The defect, measured on boilerplate.2plot.dev on 2026-08-01::

    <meta property="twitter:url" content="http://boilerplate.2plot.dev/">
                                               ^^^^

Dash builds that tag from ``request.url`` for every page
(``dash/_pages.py:_page_meta_tags``), and on Flask ``request.url`` is
assembled from ``wsgi.url_scheme``. The request reaches the app over
Cloudflare → Render → gunicorn, and the last hop is plain HTTP, so the app
sees ``http`` and advertises it. Social scrapers do not run JavaScript, so
that string is what they record — and ``og:url`` looked fine the whole time
because ``templates/index.html`` hard-codes it.

Why gunicorn does not already fix this
--------------------------------------
It tries to. gunicorn rewrites ``wsgi.url_scheme`` from ``X-Forwarded-Proto``,
but only when the *immediate peer* is in ``forwarded_allow_ips``, which
defaults to ``127.0.0.1``. On Render's native Python runtime the proxy is not
on loopback, so gunicorn declines and the header is left sitting in the
environ, unread. (The sibling satellite leaflet.2plot.dev serves ``https`` in
the same tag from the same Cloudflare/Render/gunicorn stack with no proxy
configuration of its own — the difference we could observe is that it deploys
as a Docker service rather than a native one. That is a plausible explanation
for why one honours the header and the other does not, but it is inference:
we cannot read Render's internal topology. The fix below does not depend on
which is true, which is the point of doing it in the app.)

Reading the header ourselves, one layer above gunicorn, sidesteps the whole
question: ``HTTP_X_FORWARDED_PROTO`` is in the environ either way.

Trust
-----
This trusts ``X-Forwarded-Proto`` from whoever connected. That is correct
*here* and would not be everywhere: Render terminates TLS and overwrites the
header on every inbound request, so a client cannot forge it. An app exposed
directly to the internet must not do this — a spoofed header would let a
plaintext request claim to be secure. ``TRUST_PROXY_HEADERS=0`` turns it off
for such a deployment.

Only the scheme is taken. Host is deliberately NOT rewritten from
``X-Forwarded-Host``: ``lib/constants.BASE_URL`` is already this project's
single source of truth for the public origin (canonical tags, sitemap.xml,
llms.txt), it is guarded by ``require_owned_base_url()``, and a second,
header-derived notion of "what host am I" is exactly how a fork ends up
serving two.
"""

from __future__ import annotations

import os

_SECURE_VALUES = ("https", "on", "ssl", "1")


def enabled() -> bool:
    """Off only when explicitly disabled — see the Trust note above."""
    return os.environ.get("TRUST_PROXY_HEADERS", "1") != "0"


def _scheme_from(value: str) -> str | None:
    """The scheme a forwarding header is claiming, or None.

    ``X-Forwarded-Proto`` is a comma-separated list when several proxies each
    append to it; the CLIENT's hop is the first, exactly as with
    ``X-Forwarded-For``. Taking the last would report the scheme of the hop
    nearest the app, which is the plaintext one we are trying to see past.
    """
    first = (value or "").split(",")[0].strip().lower()
    if not first:
        return None
    if first in _SECURE_VALUES:
        return "https"
    return "http" if first == "http" else None


# ------------------------------------------------------------------- WSGI --


def _wsgi_proxy_fix(wsgi_app):
    def middleware(environ, start_response):
        scheme = _scheme_from(environ.get("HTTP_X_FORWARDED_PROTO", ""))
        if scheme is None and environ.get("HTTP_X_FORWARDED_SSL", "").lower() == "on":
            scheme = "https"
        if scheme:
            environ["wsgi.url_scheme"] = scheme
        return wsgi_app(environ, start_response)

    return middleware


# ------------------------------------------------------------------- ASGI --


def _asgi_proxy_fix(asgi_app):
    async def middleware(scope, receive, send):
        # Lifespan and websocket scopes carry no forwarding headers worth
        # rewriting; touching them risks breaking startup for no gain.
        if scope.get("type") == "http":
            headers = {k.decode("latin-1").lower(): v.decode("latin-1")
                       for k, v in scope.get("headers") or []}
            scheme = _scheme_from(headers.get("x-forwarded-proto", ""))
            if scheme is None and headers.get("x-forwarded-ssl", "").lower() == "on":
                scheme = "https"
            if scheme:
                scope = dict(scope)
                scope["scheme"] = scheme
        return await asgi_app(scope, receive, send)

    return middleware


# ------------------------------------------------------------------ apply --


def apply(app, backend: str) -> bool:
    """Wrap ``app.server`` so the request scheme survives the proxy hop.

    Returns whether it was applied, so ``run.py`` can say so at boot — the
    failure this prevents is silent, and a line in the log is the only way
    anyone finds out it was switched off.

    Wrapping the server callable rather than registering a `before_request`
    hook is deliberate and the same reasoning as ``lib/analytics_tracker``'s
    placement: dash-improve-my-llms installs bot middleware that answers some
    crawler requests itself, and a hook registered after it never runs for
    them. A social scraper is precisely the traffic that must not be missed.
    """
    if not enabled():
        return False

    # NEVER rebind `app.server` itself. It is the Flask/FastAPI/Quart object
    # that `run.py` hangs `before_request` off and that gunicorn imports as
    # `run:server`; replacing it with a bare callable breaks both. Wrap the
    # inner `wsgi_app` / `asgi_app` attribute the frameworks expose for exactly
    # this purpose.
    if backend == "fastapi":
        app.server.add_middleware(_StarletteProxyFix)
        return True

    if backend == "quart":
        # Quart mirrors Flask's `wsgi_app` with `asgi_app`.
        if not hasattr(app.server, "asgi_app"):  # pragma: no cover - old Quart
            return False
        app.server.asgi_app = _asgi_proxy_fix(app.server.asgi_app)
        return True

    app.server.wsgi_app = _wsgi_proxy_fix(app.server.wsgi_app)
    return True


class _StarletteProxyFix:
    """`_asgi_proxy_fix` in the shape Starlette's `add_middleware` expects."""

    def __init__(self, app):
        self._inner = _asgi_proxy_fix(app)

    async def __call__(self, scope, receive, send):
        return await self._inner(scope, receive, send)
