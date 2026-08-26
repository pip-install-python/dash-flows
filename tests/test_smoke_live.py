"""Exercise scripts/smoke_live.py against the app itself.

NETWORK FILE: adapted from dash-documentation-boilerplate 1.2.4. The script
itself is copied verbatim, so these tests are too — minus the backend matrix,
which this suite pins to flask (the deployed backend).

The script only ever runs in CD, against a host that already exists, which is
exactly the kind of code that rots unnoticed — a typo in a regex turns every
check into a silent pass and CD keeps reporting green over a broken deploy.
So it gets run here too, with its `fetch` pointed at the in-process app
instead of the network.
"""

from __future__ import annotations

import importlib.util
import re
import sys

import pytest

from conftest import REPO_ROOT
from lib.constants import BASE_URL, OG_IMAGE_HEIGHT, OG_IMAGE_URL, OG_IMAGE_WIDTH


def _png_bytes(width: int, height: int) -> str:
    """A minimal PNG whose IHDR declares `width` x `height`.

    Returned as a `surrogateescape`-decoded str because that is the shape
    `smoke_live.fetch` hands back — the script re-encodes it the same way to
    recover the bytes. Only the 8-byte signature and the IHDR matter here; the
    card check reads nothing else.
    """
    header = b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\rIHDR"
    body = width.to_bytes(4, "big") + height.to_bytes(4, "big") + b"\x08\x06\x00\x00\x00"
    return (header + body).decode("utf-8", "surrogateescape")


# The app's real origin, because the script checks that canonical tags and
# sitemap URLs match the host being requested. Pointing it at a made-up
# hostname would fail those checks for the wrong reason.
BASE = BASE_URL


@pytest.fixture(scope="module")
def smoke():
    spec = importlib.util.spec_from_file_location(
        "smoke_live", REPO_ROOT / "scripts" / "smoke_live.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["smoke_live"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def wired(smoke, client, monkeypatch):
    """Point the script's fetch at the test client.

    Off-host URLs (the peers' llms.txt) resolve to a stub 200 — reaching over
    the network from a unit test would make the suite depend on eleven other
    deployments being up.
    """
    def fetch(url, user_agent=smoke.BROWSER_UA, accept=None):
        if url.startswith(BASE):
            path = url[len(BASE):] or "/"
            response = client.get(path, user_agent=user_agent, accept=accept)
            return response.status, response.text, response.headers
        if url == OG_IMAGE_URL:
            # The social card lives on the CDN, so it is off-host like the
            # peers — but answering it with "# peer\n" would make the card
            # checks fail for the wrong reason and, worse, would mean the
            # dimension check never ran against anything. A real PNG header
            # at the declared size exercises it properly.
            return 200, _png_bytes(OG_IMAGE_WIDTH, OG_IMAGE_HEIGHT), {
                "Content-Type": "image/png"
            }
        return 200, "# peer\n", {"Content-Type": "text/markdown"}

    monkeypatch.setattr(smoke, "fetch", fetch)
    monkeypatch.setattr(smoke, "failures", [])
    monkeypatch.setattr(smoke, "warnings", [])
    monkeypatch.setattr(smoke, "checks_run", 0)
    return smoke


def test_smoke_script_passes_against_this_app(wired, capsys):
    exit_code = wired.main(BASE)
    output = capsys.readouterr().out
    assert exit_code == 0, f"smoke_live reported failures:\n{output}"
    assert "checks passed" in output


def test_smoke_script_detects_a_stub_body(wired, smoke, monkeypatch, capsys):
    """The check that matters most must actually fire when it should."""
    original = smoke.fetch

    def stubbed(url, user_agent=smoke.BROWSER_UA, accept=None):
        status, body, headers = original(url, user_agent, accept)
        if user_agent == smoke.CRAWLER_UA:
            body = f"<main><p>{smoke.STUB_MARKER}</p></main>"
        return status, body, headers

    monkeypatch.setattr(smoke, "fetch", stubbed)
    assert wired.main(BASE) > 0
    assert "served the JavaScript stub" in capsys.readouterr().out


def test_smoke_script_detects_a_foreign_canonical(wired, smoke, monkeypatch, capsys):
    original = smoke.fetch

    def rehosted(url, user_agent=smoke.BROWSER_UA, accept=None):
        status, body, headers = original(url, user_agent, accept)
        return status, body.replace(
            'rel="canonical" href="https://flows.2plot.dev',
            'rel="canonical" href="https://someone-elses-host.example.com',
        ), headers

    monkeypatch.setattr(smoke, "fetch", rehosted)
    assert wired.main(BASE) > 0
    assert "canonical on" in capsys.readouterr().out


def test_smoke_script_detects_viewer_chrome_leaking_to_agents(
    wired, smoke, monkeypatch, capsys
):
    """The other check ROLLOUT.md calls out as silent and expensive.

    If the viewer's HTML ever reaches a plain fetch, every agent in the
    network pays tokens for decoration and nothing anywhere reports it.
    """
    original = smoke.fetch

    def leaky(url, user_agent=smoke.BROWSER_UA, accept=None):
        status, body, headers = original(url, user_agent, accept)
        if url.endswith("/llms.txt") and accept is None:
            body = '<!DOCTYPE html><div class="dv-banner">chrome</div>' + body
        return status, body, headers

    monkeypatch.setattr(smoke, "fetch", leaky)
    assert wired.main(BASE) > 0
    assert "viewer chrome" in capsys.readouterr().out


def test_peer_urls_survive_markdown_link_syntax(wired, smoke, capsys):
    """The 2.2.0 nav block writes `[https://host/llms.txt](https://host/llms.txt)`.

    A URL pattern that stops only at whitespace and `)` swallows the label and
    the opening paren into one malformed URL, which then 404s and fails a
    perfectly good deploy. Every extracted URL must be fetchable as-is.
    """
    assert wired.main(BASE) == 0
    # Either label: a peer that answers is reported as "serves a document",
    # one that doesn't as "reachable".
    reported = [
        line.split(": ", 1)[1].strip()
        for line in capsys.readouterr().out.splitlines()
        if "peer reachable: " in line or "peer serves a document: " in line
    ]
    assert reported, "no peer URLs were extracted at all"
    malformed = [u for u in reported if any(ch in u for ch in "()[]")]
    assert malformed == [], f"markdown syntax leaked into peer URLs: {malformed}"


def test_smoke_script_detects_a_missing_vary_header(wired, smoke, monkeypatch, capsys):
    """A CDN that never sees `Vary: Accept` will serve one cached variant to
    everyone — the one failure that only appears in front of a real cache."""
    original = smoke.fetch

    def unvaried(url, user_agent=smoke.BROWSER_UA, accept=None):
        status, body, headers = original(url, user_agent, accept)
        return status, body, {k: v for k, v in headers.items() if k.lower() != "vary"}

    monkeypatch.setattr(smoke, "fetch", unvaried)
    assert wired.main(BASE) > 0
    assert "Vary: Accept" in capsys.readouterr().out


def test_smoke_script_rejects_a_peer_serving_its_spa_shell(
    wired, smoke, monkeypatch, capsys
):
    """A 200 alone does not mean a host serves the document.

    A Dash app answers its catch-all with the SPA shell for any unmatched
    path, so a peer that publishes no llms.txt still returns 200 text/html.
    Verified against 2plot.dev, where `/api/this-endpoint-cannot-exist` also
    returns 200 text/html — a status-only check passes on every such host and
    the directory looks healthy while pointing at nothing.
    """
    original = smoke.fetch

    def spa_shell(url, user_agent=smoke.BROWSER_UA, accept=None):
        # The CDN-hosted card is off-host too, but it is not a peer. Leaving it
        # to the stub would fail the (correctly fatal) card checks and this
        # test would pass or fail for a reason unrelated to its name.
        if not url.startswith(BASE) and url != OG_IMAGE_URL:
            return 200, "<!DOCTYPE html><html><body>app</body></html>", {
                "Content-Type": "text/html; charset=utf-8"
            }
        return original(url, user_agent, accept)

    monkeypatch.setattr(smoke, "fetch", spa_shell)
    # Reported, but NOT fatal: this is somebody else's host. See `check()`.
    assert wired.main(BASE) == 0
    output = capsys.readouterr().out
    assert "that host's catch-all" in output
    assert "warn  peer serves a document" in output
    assert wired.warnings, "the peer problem was detected but not recorded"


def test_a_dead_peer_is_reported_but_does_not_fail_the_deploy(
    wired, smoke, monkeypatch, capsys
):
    """Every peer in the network down at once, and this deploy still ships.

    The policy this pins: a check about THIS host is fatal, a check about
    somebody else's host is a warning. Gating on peers is shared fate — one
    expired certificate anywhere in the network would stop every satellite
    from deploying, which is both wrong and the fastest way to teach people
    that a red CD means nothing.
    """
    original = smoke.fetch

    def dead_peers(url, user_agent=smoke.BROWSER_UA, accept=None):
        # Peers only — the card is off-host but is this deployment's own
        # responsibility, and its checks are fatal on purpose.
        if not url.startswith(BASE) and url != OG_IMAGE_URL:
            return 404, "", {}
        return original(url, user_agent, accept)

    monkeypatch.setattr(smoke, "fetch", dead_peers)
    assert wired.main(BASE) == 0
    output = capsys.readouterr().out
    assert "warn  peer reachable" in output
    assert "warnings (peers — not this deployment)" in output


def test_a_reshaped_card_on_the_cdn_fails_the_deploy(wired, smoke, monkeypatch, capsys):
    """The failure only this check can see.

    The card's dimensions are declared in three places — lib/constants.py,
    templates/index.html, and the CDN object itself. The first two are pinned
    against each other by tests/test_social_card.py, but nothing offline can
    look at the third. Replace the uploaded file with a differently-shaped one
    and every test stays green while the platform reserves the wrong box and
    crops into it.
    """
    original = smoke.fetch

    def reshaped(url, user_agent=smoke.BROWSER_UA, accept=None):
        if url == OG_IMAGE_URL:
            return 200, _png_bytes(600, 600), {"Content-Type": "image/png"}
        return original(url, user_agent, accept)

    monkeypatch.setattr(smoke, "fetch", reshaped)
    assert wired.main(BASE) > 0
    output = capsys.readouterr().out
    assert "dimensions match the declared" in output
    assert "file is 600x600" in output


def test_an_empty_og_image_fails_the_deploy(wired, smoke, monkeypatch, capsys):
    """An empty og:image renders a BLANK card, and platforms cache the miss.

    This is 2plot.dev's live state as of 2026-08-01: Dash emits
    `image_url or ""` when no image_url is passed, and its tag comes last in
    document order, so the empty one wins. Worse than declaring none, because
    with none most platforms fall back to an in-page image.
    """
    original = smoke.fetch

    def blanked(url, user_agent=smoke.BROWSER_UA, accept=None):
        status, body, headers = original(url, user_agent, accept)
        if url.rstrip("/") == BASE.rstrip("/"):
            body = body.replace(f'property="og:image" content="{OG_IMAGE_URL}"',
                                'property="og:image" content=""')
        return status, body, headers

    monkeypatch.setattr(smoke, "fetch", blanked)
    assert wired.main(BASE) > 0
    assert "og:image is not empty" in capsys.readouterr().out


def test_a_broken_local_surface_still_fails_the_deploy(
    wired, smoke, monkeypatch, capsys
):
    """The other half of the policy, and the one worth guarding.

    Demoting peers to warnings is only safe if everything about this host
    stayed fatal. Break a local surface while every peer is healthy and the
    exit code must still be non-zero.
    """
    original = smoke.fetch

    def no_sitemap(url, user_agent=smoke.BROWSER_UA, accept=None):
        if url.startswith(BASE) and url.endswith("/sitemap.xml"):
            return 500, "", {}
        return original(url, user_agent, accept)

    monkeypatch.setattr(smoke, "fetch", no_sitemap)
    assert wired.main(BASE) > 0
    assert "FAIL  /sitemap.xml responds 200" in capsys.readouterr().out


def test_an_unwired_bulletin_warns_but_does_not_fail_the_deploy(
    wired, smoke, capsys
):
    """How email.2plot.dev shipped with an empty "What's new" panel.

    The conftest pins `NETWORK_BULLETIN_URL` to "" for the whole suite, so the
    in-process app IS the unwired case — no monkeypatching needed to reproduce
    it. Both banner panels still render (the package falls back to one generic
    tip and "No announcements."), which is why nothing looked broken and why
    only a check can report it.

    Warn, not fail: a satellite may legitimately run without a bulletin, and a
    hub outage must never fail a deploy.
    """
    assert wired.main(BASE) == 0
    output = capsys.readouterr().out
    assert "warn  the network bulletin is wired" in output
    assert any("bulletin" in w for w in wired.warnings)


def test_a_wired_bulletin_raises_no_warning(wired, smoke, monkeypatch, capsys):
    """The positive case, so the check cannot pass by always warning."""
    original = smoke.fetch

    def announced(url, user_agent=smoke.BROWSER_UA, accept=None):
        status, body, headers = original(url, user_agent, accept)
        return status, body.replace("No announcements.", "Launched a Federated Network"), headers

    monkeypatch.setattr(smoke, "fetch", announced)
    assert wired.main(BASE) == 0
    output = capsys.readouterr().out
    assert "ok    the network bulletin is wired" in output


def test_smoke_live_urlopens_pass_the_ssl_context():
    """Source pin: every urlopen in smoke_live.py must carry
    context=SSL_CONTEXT.

    It shipped without it on post(), so on any Python missing OS trust-store
    integration (macOS — the fleet's whole local-dev half) every auth POST
    died in the TLS handshake, returned 0, and the check accused the app of
    the exact configure_app regression it exists to detect. CI never saw it
    (Linux verifies fine) and no wired test can (they monkeypatch fetch and
    post) — a SOURCE pin is the only net with a mesh this fine. Found by
    flexlayout, F1 kit adoption 2026-08-24; ported here 2026-08-26.

    This fork keeps the pin in the smoke-live file rather than upstream's
    tests/test_auth_wiring.py: the pin is not auth-specific, it lives in the
    auth file upstream only because that is where the incident surfaced
    (batch-1 correction, accepted for pannellum and excalidraw).
    """
    source = (REPO_ROOT / "scripts" / "smoke_live.py").read_text(
        encoding="utf-8"
    )
    calls = re.findall(r"urlopen\((?:[^)]|\n)*?\)", source)
    assert calls, "no urlopen calls found in smoke_live.py — probe rewritten?"
    naked = [c for c in calls if "context=SSL_CONTEXT" not in c]
    assert not naked, (
        f"urlopen without context=SSL_CONTEXT in smoke_live.py: {naked} — "
        "on macOS this dies in the handshake and reads as missing auth wiring"
    )
