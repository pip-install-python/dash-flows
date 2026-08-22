"""Access control — the checks that justify this design over the simpler ones.

The package already covers the six-surface gate matrix in its own suite. What
is new *here* is the two-source resolution: a local Clerk session answering for
a person in a browser, and a hub call answering for an agent with a key. So
these tests concentrate on the seam between them, and specifically on what
happens when the hub is unavailable.

From AUTH-NETWORK.md, checks 1 and 3 are the point:

    1. Signed-in browser, hub UNREACHABLE  -> still allowed (local resolution)
    3. Agent with valid key, hub down      -> gated, not 500, not prose

If 1 fails, every satellite's availability is coupled to one host for no
benefit. If 3 fails, an outage either leaks prose or takes the site down.

`configure_access` is process-wide, so `access_on` saves and restores it —
otherwise a gate configured here would leak into every later test in the
session and the failures would look like anything but the cause.
"""

from __future__ import annotations

import re

import pytest

from conftest import CRAWLER_UA
from lib import access, auth, hub_client, page_tiers

# Two REAL pages on this site. They must exist in the registry: a path that
# 404s hands the canonical/prerender assertions an empty document, which
# passes several of them vacuously (the leaflet lesson about verification
# that "passes" by doing nothing).
GATED_PAGE = "/nodes"
PUBLIC_PAGE = "/getting-started"
VALID_KEY = "k2p_testref_testsig"


@pytest.fixture
def restore_tiers():
    """Any test that registers a tier outside `access_on` must clean up, or the
    inertness assertion below sees a gate a later reader cannot explain."""
    saved = page_tiers.registered()
    saved_llms = dict(page_tiers._LOCAL_LLMS_PUBLIC)
    yield
    page_tiers._LOCAL_TIERS.clear()
    page_tiers._LOCAL_TIERS.update(saved)
    page_tiers._LOCAL_LLMS_PUBLIC.clear()
    page_tiers._LOCAL_LLMS_PUBLIC.update(saved_llms)


class FakeUser:
    """Stands in for ClerkUser. Only the attributes lib/auth reads."""

    def __init__(self, email="reader@example.com", user_id="user_1",
                 session_id="sess_1", plan=None):
        self.email = email
        self.user_id = user_id
        self.session_id = session_id
        self.plan = plan


@pytest.fixture
def access_on(app_module, monkeypatch):
    """Turn gating on for one test, then put the process back as it was."""
    import dash_improve_my_llms as pkg
    from dash_improve_my_llms import access as pkg_access

    saved_tiers = page_tiers.registered()
    saved_llms = dict(page_tiers._LOCAL_LLMS_PUBLIC)
    # llms_public=False: these tests exercise a machine lane that actually
    # gates. The default-open axis (the data-window posture) has its own
    # section below.
    page_tiers.register(GATED_PAGE, "auth", llms_public=False)
    hub_client.clear_cache()
    access.configure(force=True)
    try:
        yield pkg
    finally:
        # The package ships reset() for exactly this; using it rather than
        # restoring _config by hand means the teardown cannot drift from
        # whatever configure_access sets next release.
        pkg_access.reset()
        page_tiers._LOCAL_TIERS.clear()
        page_tiers._LOCAL_TIERS.update(saved_tiers)
        page_tiers._LOCAL_LLMS_PUBLIC.clear()
        page_tiers._LOCAL_LLMS_PUBLIC.update(saved_llms)
        hub_client.clear_cache()


@pytest.fixture
def hub_down(monkeypatch):
    """Every hub call fails, the way a real outage does: no exception escapes."""
    def unreachable(route, payload, timeout):
        return None

    monkeypatch.setattr(hub_client, "_post", unreachable)
    monkeypatch.setattr(hub_client, "enabled", lambda: True)
    hub_client.clear_cache()


@pytest.fixture
def hub_allows(monkeypatch):
    def allow(route, payload, timeout):
        return {"verdict": "allow", "ttl": 60}

    monkeypatch.setattr(hub_client, "_post", allow)
    monkeypatch.setattr(hub_client, "enabled", lambda: True)
    hub_client.clear_cache()


def signed_in(monkeypatch, user=None):
    monkeypatch.setattr(auth, "clerk_enabled", lambda: True)
    monkeypatch.setattr(auth, "current_user", lambda: user or FakeUser())


def anonymous(monkeypatch):
    monkeypatch.setattr(auth, "clerk_enabled", lambda: True)
    monkeypatch.setattr(auth, "current_user", lambda: None)


# ---------------------------------------------------------------------------
# The two checks that justify the design
# ---------------------------------------------------------------------------


def test_signed_in_browser_is_allowed_while_the_hub_is_unreachable(
    access_on, hub_down, monkeypatch
):
    """Check 1. The reason Clerk runs on satellites at all.

    Without local resolution every access decision needs the hub, so one host
    being down gates every restricted document on all twenty subdomains.
    """
    signed_in(monkeypatch)
    assert access.check(GATED_PAGE) == "allow"


def test_agent_with_a_key_is_gated_when_the_hub_is_down(
    access_on, hub_down, monkeypatch
):
    """Check 3. Not 500, not prose — gated."""
    anonymous(monkeypatch)
    monkeypatch.setattr(access, "_request_key", lambda: VALID_KEY)
    assert access.check(GATED_PAGE) == "gated"


def test_agent_with_a_valid_key_is_allowed_when_the_hub_answers(
    access_on, hub_allows, monkeypatch
):
    """Check 2."""
    anonymous(monkeypatch)
    monkeypatch.setattr(access, "_request_key", lambda: VALID_KEY)
    assert access.check(GATED_PAGE) == "allow"


def test_the_hub_is_not_consulted_for_a_signed_in_reader(
    access_on, monkeypatch
):
    """Local-first is an ordering claim; this asserts the ordering itself.

    A passing check-1 could also be produced by a hub that happened to allow.

    "Zero hub calls" means the per-reader agent-key endpoints. The page-tiers
    feed is different in kind: one cached per-app fetch per TTL, consulted for
    every path (a hub ceiling must bind even on locally-public pages), and its
    failure resolves to the local tier — so it never couples a signed-in
    reader's access to hub availability, which is what this test protects.
    """
    calls = []
    monkeypatch.setattr(hub_client, "_post", lambda *a, **k: calls.append(a) or None)
    monkeypatch.setattr(hub_client, "enabled", lambda: True)
    signed_in(monkeypatch)
    assert access.check(GATED_PAGE) == "allow"
    agent_key_calls = [c for c in calls if "/api/agent-key/" in c[0]]
    assert agent_key_calls == [], "a signed-in reader triggered a per-reader hub call"


# ---------------------------------------------------------------------------
# Tiers, degradation and the hub ceiling
# ---------------------------------------------------------------------------


def test_public_pages_never_reach_the_session_or_the_hub(access_on, monkeypatch):
    monkeypatch.setattr(auth, "current_user", lambda: pytest.fail("session consulted"))
    monkeypatch.setattr(hub_client, "_post", lambda *a, **k: pytest.fail("hub consulted"))
    assert access.check(PUBLIC_PAGE) == "allow"


def test_admin_tier_gates_a_signed_in_non_admin(access_on, monkeypatch):
    page_tiers.register(GATED_PAGE, "admin")
    signed_in(monkeypatch)
    monkeypatch.setattr(auth, "is_admin_user", lambda user=None: False)
    assert access.check(GATED_PAGE) == "gated"
    monkeypatch.setattr(auth, "is_admin_user", lambda user=None: True)
    assert access.check(GATED_PAGE) == "allow"


def test_hidden_is_deny_even_with_a_session(access_on, monkeypatch):
    page_tiers.register(GATED_PAGE, "hidden")
    signed_in(monkeypatch)
    assert access.check(GATED_PAGE) == "deny"


def test_everything_but_hidden_falls_open_without_clerk(access_on, monkeypatch):
    """Documentation must not brick over a missing credential.

    `hidden` still holds, because it means "there is nothing here" rather than
    "not yet" — and admin surfaces gate on `admin_access_open()`, not on this.
    """
    monkeypatch.setattr(auth, "clerk_enabled", lambda: False)
    for tier, expected in (("auth", "allow"), ("admin", "allow"), ("hidden", "deny")):
        page_tiers.register(GATED_PAGE, tier)
        assert access.check(GATED_PAGE) == expected, tier


def test_the_hub_sets_the_ceiling(restore_tiers):
    """A satellite may restrict further; it may never loosen."""
    page_tiers.register("/x", "public")
    assert page_tiers.effective_tier("/x", "auth") == "auth", "hub ceiling did not hold"
    page_tiers.register("/x", "admin")
    assert page_tiers.effective_tier("/x", "auth") == "admin", "local restriction lost"
    assert page_tiers.effective_tier("/x", None) == "admin", "hub outage changed the tier"


def test_a_hub_published_tier_gates_a_locally_public_page(access_on, monkeypatch):
    """The ceiling, end to end through the real feed: this site says public,
    the hub's /api/page-tiers says auth, an anonymous reader is gated."""
    anonymous(monkeypatch)

    def hub(route, payload, timeout):
        assert route == "/api/page-tiers"
        assert payload == {"app": hub_client.app_id()}
        return {"tiers": {PUBLIC_PAGE: "auth"}, "ttl": 300}

    monkeypatch.setattr(hub_client, "_post", hub)
    monkeypatch.setattr(hub_client, "enabled", lambda: True)
    hub_client.clear_cache()
    assert access.check(PUBLIC_PAGE) == "gated", "hub ceiling not applied"


def test_the_tier_feed_is_fetched_once_per_ttl_not_per_request(monkeypatch):
    calls = []

    def hub(route, payload, timeout):
        calls.append(route)
        return {"tiers": {"/x": "auth"}, "ttl": 300}

    monkeypatch.setattr(hub_client, "_post", hub)
    monkeypatch.setattr(hub_client, "enabled", lambda: True)
    hub_client.clear_cache()
    for _ in range(5):
        assert hub_client.hub_tiers() == {"/x": "auth"}
    assert len(calls) == 1, "every request paid a hub round trip"


def test_a_failed_tier_fetch_is_cached_and_loosens_nothing(
    restore_tiers, monkeypatch
):
    """An outage answers {} (hub unknown -> local tier holds) and is cached,
    so a down hub costs one timeout per window, not one per request."""
    calls = []
    monkeypatch.setattr(hub_client, "_post", lambda *a, **k: calls.append(a) or None)
    monkeypatch.setattr(hub_client, "enabled", lambda: True)
    hub_client.clear_cache()
    for _ in range(5):
        assert hub_client.hub_tiers() == {}
    assert len(calls) == 1, "a down hub was hammered per-request"
    page_tiers.register("/x", "admin")
    assert page_tiers.effective_tier("/x", hub_client.hub_tiers().get("/x")) == "admin"


def test_a_junk_tier_from_the_hub_cannot_loosen_a_local_tier(restore_tiers):
    page_tiers.register("/x", "admin")
    assert page_tiers.effective_tier("/x", "not-a-tier") == "admin"
    assert page_tiers.effective_tier("/x", "public") == "admin"


# ---------------------------------------------------------------------------
# The mint path (nothing calls it on this deployment; forks will)
# ---------------------------------------------------------------------------


def test_current_key_sends_the_token_never_an_asserted_identity(monkeypatch):
    """The hub 401s caller-asserted identity by design — a satellite POSTing
    {"user_id": ...} could claim to be anyone. Only the Clerk session token
    travels, because only Clerk's signature says who the reader is."""
    captured = {}

    def hub(route, payload, timeout):
        captured.update({"route": route, "payload": payload})
        return {"key": "k2p_minted"}

    monkeypatch.setattr(hub_client, "_post", hub)
    monkeypatch.setattr(hub_client, "enabled", lambda: True)
    assert hub_client.current_key("clerk-session-token") == "k2p_minted"
    assert captured["route"] == "/api/agent-key/current"
    assert captured["payload"] == {
        "token": "clerk-session-token", "app": hub_client.app_id()
    }
    assert "user_id" not in captured["payload"]


def test_current_key_degrades_to_none_when_the_hub_is_down(hub_down):
    """None -> the copy button falls back to the plain URL."""
    assert hub_client.current_key("clerk-session-token") is None
    assert hub_client.current_key("") is None


# ---------------------------------------------------------------------------
# What must never leak
# ---------------------------------------------------------------------------


def test_a_key_never_reaches_the_sitemap_or_canonical_tags(access_on, client):
    """Authority is scoped to the response it arrived in.

    A key in a canonical tag or a sitemap entry would be published to every
    crawler that reads them.
    """
    sitemap = client.get(f"/sitemap.xml?key={VALID_KEY}").text
    assert VALID_KEY not in sitemap

    html = client.get(f"{PUBLIC_PAGE}?key={VALID_KEY}", user_agent=CRAWLER_UA).text
    canonicals = re.findall(r'rel="canonical"\s+href="([^"]*)"', html)
    assert canonicals and all(VALID_KEY not in c for c in canonicals)


def test_a_key_never_reaches_a_peer_host(access_on, client):
    """The directory points at other origins; a capability must not travel.

    Judged by PARSED ORIGIN, not substring: the leaflet port found that bare
    host matching flags a site's own links whenever a peer host is a
    substring of its own (2plot.dev ⊂ leaflet.2plot.dev) — this file was
    saved only by its host being boilerplate.2plot.dev. The invariant stated
    properly: any URL carrying the key must be same-origin.
    """
    from urllib.parse import urlparse

    from lib.constants import BASE_URL

    own_host = urlparse(BASE_URL).netloc
    body = client.get(f"/llms.txt?key={VALID_KEY}").text
    for url in re.findall(r"https?://[^\s)\"'>\]]+", body):
        if VALID_KEY in url:
            assert urlparse(url).netloc == own_host, \
                f"key leaked to a peer link: {url}"


def test_the_cache_never_stores_the_key_itself():
    hub_client.clear_cache()
    hub_client._cache_put(hub_client._fingerprint(VALID_KEY), "/x", "allow", 60)
    assert all(VALID_KEY not in str(k) for k in hub_client._VERDICT_CACHE)


# ---------------------------------------------------------------------------
# Identity
# ---------------------------------------------------------------------------


def test_markdown_is_byte_identical_with_and_without_a_signed_in_reader(
    access_on, client, monkeypatch
):
    """Check 5. Identity is chrome for people; it must cost an agent nothing."""
    anonymous(monkeypatch)
    anonymous_body = client.get(f"{PUBLIC_PAGE}/llms.txt").text
    signed_in(monkeypatch)
    signed_in_body = client.get(f"{PUBLIC_PAGE}/llms.txt").text
    assert anonymous_body == signed_in_body


def test_viewer_identity_uses_session_first_seen_not_the_token_iat(monkeypatch):
    """A Clerk session token refreshes about every 60 seconds, so its `iat`
    renders a "signed in since" clock that resets. This must be stable."""
    monkeypatch.setattr(auth, "clerk_enabled", lambda: True)
    monkeypatch.setattr(auth, "current_user", lambda: FakeUser(session_id="sess_stable"))
    auth._SESSION_FIRST_SEEN.clear()
    first = auth.viewer_identity()
    second = auth.viewer_identity()
    assert first["since"] == second["since"]
    assert first["name"] == "reader@example.com"


def test_viewer_identity_is_none_when_nobody_is_signed_in(monkeypatch):
    monkeypatch.setattr(auth, "clerk_enabled", lambda: True)
    monkeypatch.setattr(auth, "current_user", lambda: None)
    assert auth.viewer_identity() is None


# ---------------------------------------------------------------------------
# Inertness
# ---------------------------------------------------------------------------


def test_access_control_is_off_when_every_page_is_public():
    """A fork inherits the machinery without inheriting a gate.

    It also keeps the per-request check off the hot path for the sites — most
    of them — that have nothing to gate.
    """
    assert not access.gating_configured()
    assert access.configure() is False


def test_a_check_that_raises_degrades_to_gated(access_on, monkeypatch):
    """The package's fail-safe, asserted from this side of the contract.

    Not `allow` — a bug in this repo's policy must not publish gated prose.
    Not `deny` — a bug must not black-hole every document on the site.
    """
    from dash_improve_my_llms import access as pkg_access

    def boom(path):
        raise RuntimeError("policy bug")

    monkeypatch.setattr(pkg_access._config, "check", boom)
    assert pkg_access.resolve(GATED_PAGE) == "gated"


# ---------------------------------------------------------------------------
# The second axis: llms_public — "interactive gated, machine open"
# ---------------------------------------------------------------------------


def test_interactive_gated_machine_open_is_the_window_contract(
    access_on, monkeypatch
):
    """THE contract of the data-window posture, in one test: the same
    anonymous request is gated in a browser and allowed on the machine lane.
    Do not "fix" either half — the split is the design (the prose is
    anonymously fetchable at /<page>/llms.txt by decision, while the
    interactive experience funnels through the sign-in card)."""
    page_tiers.register(GATED_PAGE, "auth")  # llms_public -> env default: open
    anonymous(monkeypatch)
    assert access.check(GATED_PAGE) == "allow"
    assert access.resolve_page_access(GATED_PAGE) == "sign_in"


def test_llms_public_false_gates_the_anonymous_machine_fetch(
    access_on, monkeypatch
):
    """The phase-4 posture, per page: axis pinned closed, anonymous machine
    fetches meet the gate doc. (access_on registers llms_public=False.)"""
    anonymous(monkeypatch)
    assert access.check(GATED_PAGE) == "gated"


def test_llms_public_default_env_is_the_phase_4_flip(access_on, monkeypatch):
    """LLMS_PUBLIC_DEFAULT=0 flips every page that did not pin the axis —
    the whole agent flip is this env change, no code."""
    page_tiers.register(GATED_PAGE, "auth")  # no pin -> follows the env
    anonymous(monkeypatch)
    assert access.check(GATED_PAGE) == "allow"
    monkeypatch.setenv("LLMS_PUBLIC_DEFAULT", "0")
    assert access.check(GATED_PAGE) == "gated"


def test_an_explicit_llms_public_pin_survives_the_env_flip(
    access_on, monkeypatch
):
    page_tiers.register(GATED_PAGE, "auth", llms_public=True)
    monkeypatch.setenv("LLMS_PUBLIC_DEFAULT", "0")
    anonymous(monkeypatch)
    assert access.check(GATED_PAGE) == "allow"


def test_the_open_axis_never_loosens_a_hub_imposed_gate(
    access_on, monkeypatch
):
    """Hub ceiling says auth, local axis says open — the machine lane stays
    gated. A satellite env default must not expose what the network
    restricted; the exemption is for locally declared gates only."""
    anonymous(monkeypatch)

    def hub(route, payload, timeout):
        return {"tiers": {PUBLIC_PAGE: "auth"}, "ttl": 300}

    monkeypatch.setattr(hub_client, "_post", hub)
    monkeypatch.setattr(hub_client, "enabled", lambda: True)
    hub_client.clear_cache()
    assert access.check(PUBLIC_PAGE) == "gated"


def test_machine_surfaces_follow_the_axis_end_to_end(
    access_on, client, monkeypatch
):
    """Through the real routes: the gate doc when the axis is closed, the
    prose when it is open — same page, same anonymous reader."""
    anonymous(monkeypatch)
    gated_body = client.get(f"{GATED_PAGE}/llms.txt").text
    assert "not public" in gated_body
    page_tiers.register(GATED_PAGE, "auth", llms_public=True)
    open_body = client.get(f"{GATED_PAGE}/llms.txt").text
    assert "not public" not in open_body
    assert open_body != gated_body


# ---------------------------------------------------------------------------
# resolve_page_access — the interactive verdict
# ---------------------------------------------------------------------------


def test_resolve_page_access_anonymous_matrix(access_on, monkeypatch):
    anonymous(monkeypatch)
    for tier, expected in (("public", "allow"), ("auth", "sign_in"),
                           ("admin", "sign_in"), ("hidden", "hidden")):
        page_tiers.register(GATED_PAGE, tier)
        assert access.resolve_page_access(GATED_PAGE) == expected, tier


def test_resolve_page_access_signed_in_matrix(access_on, monkeypatch):
    signed_in(monkeypatch)
    monkeypatch.setattr(auth, "is_admin_user", lambda user=None: False)
    page_tiers.register(GATED_PAGE, "auth")
    assert access.resolve_page_access(GATED_PAGE) == "allow"
    page_tiers.register(GATED_PAGE, "admin")
    assert access.resolve_page_access(GATED_PAGE) == "forbidden"
    monkeypatch.setattr(auth, "is_admin_user", lambda user=None: True)
    assert access.resolve_page_access(GATED_PAGE) == "allow"


def test_admin_layouts_fail_closed_without_clerk_docs_fall_open(
    access_on, monkeypatch
):
    """The boilerplate's posture, pinned so a future port from pip-docs+
    (whose resolve_access falls fully open without Clerk keys) cannot
    regress it: docs stay readable, admin stays sealed."""
    monkeypatch.setattr(auth, "clerk_enabled", lambda: False)
    monkeypatch.setattr(auth, "admin_access_open", lambda: False)
    page_tiers.register(GATED_PAGE, "auth")
    assert access.resolve_page_access(GATED_PAGE) == "allow"
    page_tiers.register(GATED_PAGE, "admin")
    assert access.resolve_page_access(GATED_PAGE) == "forbidden"
    monkeypatch.setattr(auth, "admin_access_open", lambda: True)
    assert access.resolve_page_access(GATED_PAGE) == "allow"


def test_a_key_never_unlocks_a_browser_layout(
    access_on, hub_allows, monkeypatch
):
    """Keys are machine-surface capabilities. A ?key= that opened layouts
    would turn every copied URL into a shareable session."""
    page_tiers.register(GATED_PAGE, "auth", llms_public=False)
    anonymous(monkeypatch)
    monkeypatch.setattr(access, "_request_key", lambda: VALID_KEY)
    assert access.check(GATED_PAGE) == "allow"        # machine lane: yes
    assert access.resolve_page_access(GATED_PAGE) == "sign_in"  # layout: no


def test_run_py_pins_the_funnel_public(app_module):
    """PAGE_DEFAULT_TIER=auth must never gate the funnel or the corpus
    pseudo-paths — run.py and frontmatter pin them explicitly, and this is
    the regression net for those pins."""
    for path in ("/", "/getting-started", "/llms-small.txt", "/llms-full.txt"):
        assert page_tiers.local_tier(path) == "public", path
