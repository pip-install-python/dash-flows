"""Who may read a page — the local half of the network's access rule.

Four tiers, least to most restrictive:

``public``   anyone, including agents and crawlers
``auth``     any signed-in user; anonymous readers get the gate document
``admin``    signed in AND allowlisted (``ADMIN_EMAILS`` / ``ADMIN_USER_IDS``)
``hidden``   nobody; the document 404s and the page is delisted everywhere

A page declares its tier in markdown frontmatter, because this template is
already frontmatter-driven and a satellite author should not need a control
board to mark one page::

    ---
    name: Internal Runbook
    endpoint: /runbook
    tier: admin
    ---

Absent that, :data:`DEFAULT_TIER` applies — ``public``, because a
documentation site that defaults to gated is a documentation site nobody
reads. Override the default per deployment with ``PAGE_DEFAULT_TIER``.

Two rules make this safe to run before the hub exists:

**Fail open for reading, closed for admin.** With Clerk unavailable — no keys,
package missing, which is the default — every tier except ``hidden`` degrades
to ``public``. A component library's documentation must never brick because a
deploy forgot a credential. ``hidden`` still holds, because it means "there is
nothing here", not "you may not read this yet".

**The hub sets the ceiling.** Once ``2plot.dev`` publishes tiers, the effective
tier is the *more restrictive* of the hub's and this site's. A satellite can
lock its own page down further; it can never loosen what the hub restricted.
That direction is deliberate: a satellite misconfiguration then cannot expose
something the network gated, and "loosen this page" stays a hub action, which
is where that authority belongs.
"""

from __future__ import annotations

import logging
import os
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Ordered least -> most restrictive. The order is the comparison.
TIERS = ("public", "auth", "admin", "hidden")


def _default_tier() -> str:
    tier = (os.getenv("PAGE_DEFAULT_TIER") or "public").strip().lower()
    if tier not in TIERS:
        logger.warning("PAGE_DEFAULT_TIER=%r is not a tier — using 'public'", tier)
        return "public"
    return tier


# endpoint -> tier, populated from frontmatter as pages/markdown.py loads docs.
_LOCAL_TIERS: Dict[str, str] = {}

# endpoint -> machine-surface openness, the SECOND axis. `tier` answers "who
# may use the page in a browser"; `llms_public` answers "does the machine
# twin (/<page>/llms.txt, crawler HTML, the prerender) stay open anyway".
# The split exists so the fleet can gate the interactive experience for
# humans while the 30-day crawl-demand window keeps measuring agents — and
# so the later agent flip is one env change (`LLMS_PUBLIC_DEFAULT=0`), not a
# code change. Only meaningful on `auth` pages: `public` needs no exemption,
# and `admin`/`hidden` must never leak through a machine surface.
_LOCAL_LLMS_PUBLIC: Dict[str, bool] = {}

_FALSE_VALUES = ("0", "false", "no", "off")


def _default_llms_public() -> bool:
    raw = (os.getenv("LLMS_PUBLIC_DEFAULT") or "").strip().lower()
    return raw not in _FALSE_VALUES if raw else True


def normalize(path: str) -> str:
    """One canonical path form, so registration and lookup cannot disagree."""
    path = (path or "/").strip()
    if not path.startswith("/"):
        path = "/" + path
    return path.rstrip("/") or "/"


def register(path: str, tier: Optional[str],
             llms_public: Optional[bool] = None) -> str:
    """Record a page's locally declared tier. Returns the tier applied.

    ``llms_public`` pins the machine-surface axis for this page; ``None``
    (the overwhelmingly common case) defers to ``LLMS_PUBLIC_DEFAULT`` at
    lookup time, so flipping the env flips every undeclared page at once.
    """
    resolved = (tier or _default_tier()).strip().lower()
    if resolved not in TIERS:
        logger.warning(
            "Page %s declares tier %r, which is not one of %s — using %r",
            path, tier, TIERS, _default_tier(),
        )
        resolved = _default_tier()
    _LOCAL_TIERS[normalize(path)] = resolved
    # Declarative: a registration fully describes the page, so None does not
    # mean "keep whatever was pinned before" — it clears the pin and defers
    # to the env default again.
    if llms_public is None:
        _LOCAL_LLMS_PUBLIC.pop(normalize(path), None)
    else:
        _LOCAL_LLMS_PUBLIC[normalize(path)] = bool(llms_public)
    return resolved


def get_llms_public(path: str) -> bool:
    """Whether ``path``'s machine twin stays open to anonymous fetches.

    Read at verdict time, not registration time, so `LLMS_PUBLIC_DEFAULT`
    governs every page that did not pin the axis in frontmatter.
    """
    return _LOCAL_LLMS_PUBLIC.get(normalize(path), _default_llms_public())


def local_tier(path: str) -> str:
    return _LOCAL_TIERS.get(normalize(path), _default_tier())


def registered() -> Dict[str, str]:
    """Every locally declared tier. For tests and for a future control board."""
    return dict(_LOCAL_TIERS)


def more_restrictive(first: str, second: str) -> str:
    """The stricter of two tiers. Unknown values are treated as the default."""
    def rank(tier: str) -> int:
        try:
            return TIERS.index((tier or "").strip().lower())
        except ValueError:
            return TIERS.index(_default_tier())

    return TIERS[max(rank(first), rank(second))]


def effective_tier(path: str, hub_tier: Optional[str] = None) -> str:
    """The tier actually enforced for ``path``.

    ``hub_tier`` is the ceiling published by the network hub, when one is
    known. Passing None means "hub unknown", which resolves to the local
    value — a hub outage must not silently *loosen* anything, and it cannot,
    because the local value is already the stricter-or-equal half whenever the
    hub is reachable.
    """
    local = local_tier(path)
    return more_restrictive(local, hub_tier) if hub_tier else local


def is_readable_without_auth(tier: str) -> bool:
    return tier == "public"


def degraded_tier(tier: str) -> str:
    """What ``tier`` means when authentication is unavailable entirely.

    Everything except ``hidden`` falls open. See the module docstring — this
    is the trade that keeps documentation readable when a credential is
    missing, and it is why ``admin`` surfaces use `auth.admin_access_open()`
    rather than relying on a tier.
    """
    return "hidden" if tier == "hidden" else "public"
