"""The interactive gate's presentation layer (lib/gate_layouts.py).

The verdict logic is tested in test_access.py; here the contract is the
wrapper itself: the right card per verdict, content only on allow, the
**kwargs tolerance Dash Pages requires, and the funnel surviving a broken
teaser demo.
"""

from __future__ import annotations

import pytest

from lib import access, gate_layouts


def _ids(component, found=None):
    """Every component id in a Dash tree."""
    found = found if found is not None else set()
    comp_id = getattr(component, "id", None)
    if isinstance(comp_id, str):
        found.add(comp_id)
    children = getattr(component, "children", None)
    if isinstance(children, (list, tuple)):
        for child in children:
            _ids(child, found)
    elif children is not None:
        _ids(children, found)
    return found


CONTENT = "the real page content"


@pytest.fixture
def wrapped(app_module):
    return gate_layouts.gated_layout("/some-page", "Some Page", CONTENT)


def test_allow_returns_the_content(wrapped, monkeypatch):
    monkeypatch.setattr(access, "resolve_page_access", lambda p: "allow")
    assert wrapped() == CONTENT


def test_allow_calls_a_callable_layout(app_module, monkeypatch):
    monkeypatch.setattr(access, "resolve_page_access", lambda p: "allow")
    layout = gate_layouts.gated_layout("/p", "P", lambda: CONTENT)
    assert layout() == CONTENT


def test_sign_in_renders_the_funnel_card_with_both_buttons(wrapped, monkeypatch):
    monkeypatch.setattr(access, "resolve_page_access", lambda p: "sign_in")
    card = wrapped()
    ids = _ids(card)
    assert "auth-gate-signup" in ids and "auth-gate-signin" in ids
    assert CONTENT not in str(card)


def test_forbidden_and_hidden_render_cards_not_content(wrapped, monkeypatch):
    for verdict in ("forbidden", "hidden"):
        monkeypatch.setattr(access, "resolve_page_access", lambda p: verdict)
        assert CONTENT not in str(wrapped())


def test_the_layout_accepts_dash_pages_kwargs(wrapped, monkeypatch):
    """Dash Pages forwards query params (incl. Clerk's ?__clerk_handshake=)
    into layout callables — the wrapper must swallow them."""
    monkeypatch.setattr(access, "resolve_page_access", lambda p: "allow")
    assert wrapped(__clerk_handshake="abc", utm_source="x") == CONTENT


def test_the_verdict_runs_per_render_not_per_registration(wrapped, monkeypatch):
    """An env flip applies on the next navigation — nothing is baked in."""
    monkeypatch.setattr(access, "resolve_page_access", lambda p: "sign_in")
    assert CONTENT not in str(wrapped())
    monkeypatch.setattr(access, "resolve_page_access", lambda p: "allow")
    assert wrapped() == CONTENT


def test_a_broken_demo_never_breaks_the_funnel(app_module, monkeypatch):
    """lib/auth_demos degrades to the demo-less card on any failure, and the
    card itself tolerates build_demo raising — a broken example must never
    take down the sign-in funnel."""
    from lib import auth_demos

    monkeypatch.setitem(
        auth_demos.DEMOS, "/broken",
        {"module": "docs.does_not_exist.nope", "caption": "x"},
    )
    assert auth_demos.build_demo("/broken") is None

    def boom(path):
        raise RuntimeError("demo table bug")

    monkeypatch.setattr(auth_demos, "build_demo", boom)
    card = gate_layouts.sign_in_layout("Page", "/broken")
    assert "auth-gate-signup" in _ids(card)


def test_the_gate_card_names_the_sign_in_destination(app_module, monkeypatch):
    """No hardcoded URLs: the destination comes from access.sign_in_url()
    (bulletin first, env second), falling back to the network primary."""
    monkeypatch.setattr(access, "sign_in_url", lambda: "https://example.test/in")
    assert "https://example.test/in" in str(gate_layouts.sign_in_layout("P"))
    monkeypatch.setattr(access, "sign_in_url", lambda: None)
    assert "https://2plot.ai" in str(gate_layouts.sign_in_layout("P"))


def test_a_fake_clerk_config_renders_the_CONFIGURED_gate_card(monkeypatch):
    """Spec item 7 (template 1.6.29, found by clerkhook): a page that renders
    differently once secrets are present must have its CONFIGURED branch
    certified by something.

    conftest blanks every CLERK_* var before run.py is imported — the right
    posture for the rest of the suite, and the reason this branch was
    certified by nothing here: the local lane never has a config, and
    production ships DARK so smoke_live's live probe skips too. This test is
    the one place a NON-EMPTY (fake, never real) config reaches the gate.

    Driven from the ENV rather than by stubbing access.sign_in_url, so the
    whole chain is exercised: env -> access.sign_in_url() ->
    gate_layouts._sign_in_destination() -> the rendered card. The assertion
    is non-vacuous by construction — the unconfigured branch emits the
    network primary instead, which the second half pins.
    """
    configured = "https://accounts.example.test/sign-in"
    monkeypatch.setenv("CLERK_SIGN_IN_URL", configured)
    card = str(gate_layouts.sign_in_layout("P"))
    assert configured in card, (
        "a non-empty CLERK_SIGN_IN_URL did not reach the gate card — the "
        "configured branch is unreachable from the config that turns it on"
    )
    assert "https://2plot.ai" not in card, "both branches rendered at once?"

    monkeypatch.setenv("CLERK_SIGN_IN_URL", "")
    assert "https://2plot.ai" in str(gate_layouts.sign_in_layout("P"))
