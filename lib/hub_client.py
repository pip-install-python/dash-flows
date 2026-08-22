"""Client for the network hub's agent-key and page-tier endpoints.

Three calls, all satellite → hub, never browser → hub::

    POST {hub}/api/agent-key/current   -> {"key": "k2p_..."}   for the copy button
    POST {hub}/api/agent-key/verify    -> {"verdict": ..., "ttl": ...}
    POST {hub}/api/page-tiers          -> {"tiers": {path: tier}, "ttl": ...}

Why a hub call exists at all
----------------------------
A signed-in visitor is resolved **locally** by Clerk and never reaches this
module. Only an agent fetch does: someone pastes a document URL into an
assistant, and it arrives with no cookie, carrying `?key=` instead. Only the
hub can validate that key, because only the hub holds the secret it was
derived from.

That asymmetry is the point of the design. A satellite holds **no key
material** — it cannot mint, and it cannot verify offline. Sharing the hub's
`SESSION_SECRET` would let any satellite verify locally, but anything that can
verify can also mint, including `scope=admin`; twenty deployments holding a
network-wide admin-minting secret is precisely the failure this avoids.

Authenticating the caller
-------------------------
The hub must know which satellite is asking — a verify endpoint open to the
internet is a key-guessing oracle. This reuses the network's existing
signed-webhook scheme (`CROSS_APP_WEBHOOK_SECRET`, HMAC-SHA256 over
`"{timestamp}." + body`), the same one `lib/satellite_reporter` already uses.
That secret authenticates a caller; it does not derive keys, so holding it
grants a satellite nothing it could not already do.

Failure behaviour
-----------------
Every failure path — no secret, timeout, DNS, 5xx, non-JSON, wrong shape —
returns ``gated``. Never ``allow``: a hub outage must not publish restricted
prose. Never ``deny``: an outage must not black-hole every document. ``gated``
leaks nothing and keeps the surface answering, which is the same fail-safe the
package applies when an app's own check raises.

Nothing here logs a key, or anything derived from one.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import time
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)

DEFAULT_HUB_URL = "https://2plot.dev"

# Allow verdicts outlive deny verdicts on purpose. A brief hub blip should not
# gate a reader who was fine a minute ago, whereas a revoked key should stop
# working promptly — so the cost of being slightly stale is paid by the side
# that fails safe. The hub may override both per response.
ALLOW_TTL_S = 900.0
DENY_TTL_S = 60.0

# key-hash + path -> (verdict, expires_at)
_VERDICT_CACHE: Dict[Tuple[str, str], Tuple[str, float]] = {}
_CACHE_MAX = 4096


def hub_url() -> str:
    return (os.getenv("NETWORK_HUB_URL") or DEFAULT_HUB_URL).rstrip("/")


def _secret() -> Optional[str]:
    return os.getenv("CROSS_APP_WEBHOOK_SECRET") or None


def app_id() -> str:
    """This satellite's identity to the hub. Same key the reporter uses."""
    return os.getenv("SATELLITE_APP_KEY") or os.getenv("AD_APP_ID") or "boilerplate"


def enabled() -> bool:
    """False when this deployment cannot talk to the hub at all.

    With no shared secret there is nobody to authenticate as, so every verify
    would fail anyway. Reporting that up front lets the caller skip the round
    trip and go straight to the fail-safe.
    """
    return bool(_secret())


def _fingerprint(key: str) -> str:
    """A cache handle for a key that is not the key.

    The cache lives in process memory and may be dumped by a debugger, a heap
    profiler or an error reporter. Storing a hash means none of those ever
    contain a capability.
    """
    return hashlib.sha256(key.encode("utf-8", "replace")).hexdigest()[:32]


def _cache_get(fingerprint: str, path: str) -> Optional[str]:
    entry = _VERDICT_CACHE.get((fingerprint, path))
    if not entry:
        return None
    verdict, expires_at = entry
    if expires_at < time.time():
        _VERDICT_CACHE.pop((fingerprint, path), None)
        return None
    return verdict


def _cache_put(fingerprint: str, path: str, verdict: str, ttl: float) -> None:
    if len(_VERDICT_CACHE) >= _CACHE_MAX:
        _VERDICT_CACHE.clear()
    _VERDICT_CACHE[(fingerprint, path)] = (verdict, time.time() + max(0.0, ttl))


def clear_cache() -> None:
    _VERDICT_CACHE.clear()
    clear_tiers_cache()


def _post(route: str, payload: dict, timeout: float) -> Optional[dict]:
    """Signed POST to the hub. Returns the decoded body, or None on any failure."""
    secret = _secret()
    if not secret:
        return None

    import requests

    from lib.constants import internal_ua

    # Sign the exact bytes sent — serialise once, sign that.
    body = json.dumps(payload).encode()
    ts = str(int(time.time()))
    signature = hmac.new(
        secret.encode(), f"{ts}.".encode() + body, hashlib.sha256
    ).hexdigest()

    try:
        response = requests.post(
            f"{hub_url()}{route}",
            data=body,
            timeout=timeout,
            headers={
                "Content-Type": "application/json",
                "X-AI-Canvas-Timestamp": ts,
                "X-AI-Canvas-Signature": signature,
                "X-Satellite-App": app_id(),
                # Internal-traffic contract (lib/constants.INTERNAL_UA): these
                # are satellite→hub machine calls, and a key verification is
                # not a reader of 2plot.dev's documentation.
                "User-Agent": internal_ua("hub-client"),
            },
        )
    except Exception as exc:  # noqa: BLE001 — DNS, TLS, timeouts all land here
        logger.debug("hub %s unreachable: %r", route, exc)
        return None

    if response.status_code != 200:
        logger.debug("hub %s returned HTTP %s", route, response.status_code)
        return None

    try:
        decoded = response.json()
    except Exception:
        # A hub whose catch-all serves an HTML app shell answers 200 with a
        # page. Treating that as a verdict would be worse than a timeout.
        logger.debug("hub %s did not return JSON", route)
        return None

    return decoded if isinstance(decoded, dict) else None


def verify(key: str, path: str, tier: str, timeout: float = 3.0) -> str:
    """``allow`` | ``gated`` | ``deny`` for an agent fetch carrying ``key``.

    Cached on (key fingerprint, path). Anything unexpected is ``gated``.
    """
    if not key:
        return "gated"

    fingerprint = _fingerprint(key)
    cached = _cache_get(fingerprint, path)
    if cached is not None:
        return cached

    if not enabled():
        logger.debug("hub verify skipped: no CROSS_APP_WEBHOOK_SECRET")
        return "gated"

    decoded = _post(
        "/api/agent-key/verify",
        {"key": key, "path": path, "tier": tier, "app": app_id()},
        timeout,
    )
    if decoded is None:
        return "gated"

    verdict = str(decoded.get("verdict") or "").strip().lower()
    if verdict not in ("allow", "gated", "deny"):
        logger.debug("hub verify returned an unrecognised verdict")
        return "gated"

    # The hub may set the TTL; fall back to ours. allow outlives deny.
    default_ttl = ALLOW_TTL_S if verdict == "allow" else DENY_TTL_S
    try:
        ttl = float(decoded.get("ttl", default_ttl))
    except (TypeError, ValueError):
        ttl = default_ttl
    _cache_put(fingerprint, path, verdict, ttl)
    return verdict


def current_key(token: str, timeout: float = 3.0) -> Optional[str]:
    """This user's current agent key, minted by the hub if needed.

    For the "copy for LLM" button: a signed-in reader gets a URL that still
    works after it is pasted into an assistant. ``token`` is the browser's
    Clerk session token — server-side, the ``__session`` cookie value on a
    Clerk-authenticated request. The hub verifies it against Clerk's JWKS and
    mints at ``scope=auth``, never admin.

    The hub 401s any caller-asserted identity (a ``user_id`` in the payload is
    the forgery path — this satellite could claim to be anyone), which is why
    the token travels instead: only Clerk's signature says who the reader is.

    Two rules from the hub session: call this on copy-button CLICK, never on
    page render — every call is a hub round trip and each mint is recorded
    hub-side; and ``None`` degrades to copying the plain URL, which is what an
    anonymous reader gets anyway. None when the hub is unreachable or auth is
    off.
    """
    if not token or not enabled():
        return None

    decoded = _post(
        "/api/agent-key/current",
        {"token": token, "app": app_id()},
        timeout,
    )
    if decoded is None:
        return None

    key = decoded.get("key")
    return key if isinstance(key, str) and key else None


# hub_tiers cache: (tiers, expires_at). One entry — the feed is per-app, and
# this process is one app. A failed fetch caches {} briefly so an outage costs
# one timeout per FAILURE_TTL_S, not one per request (access.check calls this
# on every non-public resolution).
TIERS_TTL_S = 900.0
TIERS_FAILURE_TTL_S = 60.0
_TIERS_CACHE: Tuple[Dict[str, str], float] = ({}, 0.0)


def clear_tiers_cache() -> None:
    global _TIERS_CACHE
    _TIERS_CACHE = ({}, 0.0)


def hub_tiers(timeout: float = 3.0) -> Dict[str, str]:
    """Tiers published by the hub — the ceiling for this site's pages.

    Signed POST ``/api/page-tiers`` with ``{"app": app_id()}`` →
    ``{"tiers": {path: tier}, "ttl": seconds}``, cached for the returned TTL.
    Each fetch is recorded hub-side — the hub admin's "last pulled" indicator
    is how a published ceiling is confirmed to have landed on this satellite.

    Every failure returns ``{}``, meaning "hub unknown", which
    `page_tiers.effective_tier` resolves to the local value. The ceiling only
    ever restricts, so an outage loosens nothing — and an outage that served
    a ceiling a moment ago degrades to the local tier, never below it.
    """
    global _TIERS_CACHE
    tiers, expires_at = _TIERS_CACHE
    if expires_at > time.time():
        return tiers

    if not enabled():
        # No secret -> nobody to authenticate as; don't re-check every request.
        _TIERS_CACHE = ({}, time.time() + TIERS_FAILURE_TTL_S)
        return {}

    decoded = _post("/api/page-tiers", {"app": app_id()}, timeout)
    raw = decoded.get("tiers") if isinstance(decoded, dict) else None
    if not isinstance(raw, dict):
        _TIERS_CACHE = ({}, time.time() + TIERS_FAILURE_TTL_S)
        return {}

    # Keep only well-formed entries; a junk value must not become a tier.
    tiers = {
        str(path): str(tier).strip().lower()
        for path, tier in raw.items()
        if isinstance(path, str) and isinstance(tier, str)
    }

    try:
        ttl = float(decoded.get("ttl", TIERS_TTL_S))
    except (TypeError, ValueError):
        ttl = TIERS_TTL_S
    _TIERS_CACHE = (tiers, time.time() + max(0.0, ttl))
    return tiers
