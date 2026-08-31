#!/usr/bin/env python3
"""Smoke battery for a 2plot satellite — CI container and production alike.

One script, two seats, the SAME named checks either way, so a failure in CI
and a failure against production read identically:

    CI container   python scripts/network_smoke.py --base-url http://localhost:8560
    Production     python scripts/network_smoke.py --base-url https://flows.2plot.dev

Stdlib-only on purpose: CI runs it from the host against the booted container
with a bare `python3`, before anything is pip-installed.

NETWORK FILE. Copied from dash-documentation-boilerplate 1.2.4 (with the
social-card checks from leaflet.2plot.dev and the hub's real-pixels shape).
Only the block marked "per-site" below differs; everything else is the network
standard, and if a check here is wrong it is wrong on twenty hosts.

What a satellite is to the network is what the battery proves: that it states
its identity, that its agent-facing document surfaces are real, that it runs
the intended dash-improve-my-llms artifact, that its share card is not blank,
and that no owner-only surface leaks. A satellite holds no key material, so
unlike the hub's copy of this script there is no agent-key API to fail closed —
the corresponding check here is that this host's llms.txt points *back* at the
hub that does.

Every UA this script sends carries the internal-traffic token (the analytics
point of truth — https://2plot.ai/docs/satellite-analytics, "Internal
traffic"): a battery must never register as a visitor or a "bot" in any
network ledger. Even the deliberately crawler-shaped probe appends the token
— the target still exercises its bot path, but its analytics know the caller
is machinery.

Exit code: 1 if any check fails, else 0.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TIMEOUT = 30
try:
    from lib.constants import INTERNAL_UA as _INTERNAL_UA
except Exception:  # running outside a repo checkout — keep the token intact
    _INTERNAL_UA = "2plot-internal/1.0 (+https://2plot.ai/docs/satellite-analytics)"
# The default UA names the BROWSER lane first (sync item 17; muischeduler's
# finding on its item-12 port): at dash-improve-my-llms >= 2.8 a UA with no
# browser engine token is classified crawler-lane, so a bare internal token
# made every default-UA check read the prerendered crawler document — a
# manifest-link or og:image check goes red the moment a floor moves, in CD's
# verify job. The internal token stays IN the string, after the engine token:
# INTERNAL_UA_TOKEN is a substring match, so the far side's internal-traffic
# exclusion still holds. CRAWLER_UA is the other lane and is deliberately
# untouched.
BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 "
    + _INTERNAL_UA + " network-smoke"
)
UA = BROWSER_UA
CRAWLER_UA = "Mozilla/5.0 (compatible; Googlebot/2.1) " + _INTERNAL_UA

# The body dash-improve-my-llms serves when a page has no prose registered.
# Matched IN FULL, not as a substring of the phrase "requires JavaScript".
# The template used to carry a <noscript> fallback whose own HTML comment
# spelled that phrase, so a substring check reported a perfectly healthy host
# as broken. That block is gone — the 2.6.1 prerender is served VISIBLE and
# hidden only by a script JS-disabled readers never run, so it covered the
# same readers better — but the full match stays, because it is strictly the
# safer comparison and this class of false positive is cheap to reintroduce.
STUB_MARKER = "This page contains interactive content that requires JavaScript"

# ---------------------------------------------------------------- per-site --
# The values a fork changes. Everything below this block is the network
# standard and is copied verbatim.

# This app's one identity (lib/constants.SITE_BRAND). tests/test_site_identity
# asserts every local surface carries it; this pins the DEPLOYED artifact to
# it, which is the half no unit test can reach.
SITE_H1 = "# dash-flows — React Flow node graphs for Dash"

# The container port. Matches the Dockerfile's EXPOSE/CMD and run.py.
DEFAULT_BASE_URL = "http://localhost:8560"

# A real documentation page, used to prove `/<page>/llms.txt` works at all.
# The getting-started page is the one this library cannot lose.
SAMPLE_PAGE = "/getting-started"

# Owner-only surfaces that must 404 their llms.txt to an anonymous reader —
# every registered /admin/* page (sync item 18: pinned against the registry
# by tests/test_nav_contract.py::test_battery_hidden_paths_match_the_registry,
# so a page added, renamed or deleted moves this tuple in the same change).
HIDDEN_DOC_PATHS = (
    "/admin/control-board/llms.txt",
    "/admin/traffic/llms.txt",
)

# The hub one level up the chain. A satellite's llms.txt must name it — that
# is what lets an agent walk from any leaf to the network root.
HUB_URL = "https://2plot.dev"

# The social card. Dash emits `og:image` on every page and leaves it EMPTY
# when it can find no image, which renders a blank preview on every platform
# and is invisible from inside the app — nobody sees their own unfurls. Served
# from the 2plot CDN so a sleeping free-tier container never costs a preview.
# Keep in step with lib/constants.OG_IMAGE_*.
OG_IMAGE_URL = "https://cdn.2plot.ai/github_assets/flows.2plot.dev.png"
OG_IMAGE_WIDTH = 1200
OG_IMAGE_HEIGHT = 630

# ---------------------------------------------------------------------------


def _ssl_context() -> ssl.SSLContext:
    """Verify certificates via certifi when available. Same fix, same reason
    as scripts/smoke_live.py's copy.

    macOS Python ships without OS trust-store integration, so a bare urllib
    https fetch dies in the handshake — and THIS battery turns that into
    `FAIL healthz responds 200`, i.e. it reads a perfectly healthy host as
    down, from a Mac, every time. CI never sees it (Linux verifies fine),
    which is exactly why it survived here until the fleet round of
    2026-08-26. Verification stays ON either way; certifi only supplies the
    CA bundle.
    """
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


SSL_CONTEXT = _ssl_context()

PASS, FAIL, WARN, SKIP = "pass", "FAIL", "warn", "skip"
_RESULTS: list[tuple[str, str, str]] = []  # (name, verdict, detail)


class SmokeFailure(Exception):
    pass


def fetch_raw(url: str, ua: str = UA, method: str = "GET",
              body: bytes | None = None, headers: dict | None = None,
              timeout: int = TIMEOUT, retries: int = 3):
    """(status, headers, BYTES) — HTTP errors are results, not exceptions;
    network errors raise AFTER retries.

    Bytes rather than text, because one caller needs them: the social card is a
    PNG and its real dimensions live in the IHDR chunk at bytes 16..24. A
    decode with `errors="replace"` substitutes U+FFFD for every invalid byte
    and is one-way, so the header would be gone before it could be read.

    Response headers come back lower-cased: gunicorn sends `content-type`,
    proxies often re-case it — callers must not care. (A CI-only failure in the
    network root's battery was exactly that difference.)
    """
    last_exc: Exception | None = None
    for attempt in range(retries):
        if attempt:
            time.sleep(2 * attempt)
        req = urllib.request.Request(url, data=body, method=method)
        req.add_header("User-Agent", ua)
        for k, v in (headers or {}).items():
            req.add_header(k, v)
        try:
            with urllib.request.urlopen(
                req, timeout=timeout, context=SSL_CONTEXT
            ) as r:
                return (r.status, {k.lower(): v for k, v in r.headers.items()},
                        r.read())
        except urllib.error.HTTPError as e:
            return (e.code, {k.lower(): v for k, v in e.headers.items()},
                    e.read())
        except Exception as exc:  # timeout, reset, truncated read, …
            last_exc = exc
    raise last_exc


def fetch(url: str, **kw):
    """(status, headers, text) — the text-flavoured `fetch_raw`."""
    status, headers, raw = fetch_raw(url, **kw)
    return status, headers, raw.decode("utf-8", "replace")


def record(name: str, verdict: str, detail: str = "") -> None:
    _RESULTS.append((name, verdict, detail))
    print(f"[{verdict:>4}] {name}" + (f" — {detail}" if detail else ""), flush=True)
    if verdict == WARN and os.getenv("GITHUB_ACTIONS"):
        print(f"::warning title=network-smoke {name}::{detail}", flush=True)


def check(name: str, fn) -> None:
    try:
        fn()
        record(name, PASS)
    except SmokeFailure as exc:
        record(name, FAIL, str(exc))
    except Exception as exc:  # network/parse error → still a failure
        record(name, FAIL, f"{type(exc).__name__}: {exc}")


def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise SmokeFailure(msg)


# ------------------------------------------------------------- the battery --

def declared_python_minor():
    """The fleet Python this checkout declares: the Dockerfile's FROM minor.

    The Dockerfile is the ONLY declaration in this repo — the Render service
    is `runtime: docker`, so there is no PYTHON_VERSION lane to cross-check
    (DIVERGENCES.md 5).

    None when there is nothing to hold the host against — no Dockerfile beside
    this script (the script run outside a checkout) — or when the seat itself
    is off-contract: SMOKE_PYTHON_DECLARED=ignore is set by any seat whose
    interpreter is NOT a deploy artifact. The seats that leave it armed are
    exactly the ones where it is: the docker container in CI, and production
    in CD.
    """
    if os.environ.get("SMOKE_PYTHON_DECLARED") == "ignore":
        return None
    dockerfile = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "Dockerfile")
    try:
        with open(dockerfile, encoding="utf-8") as fh:
            for line in fh:
                m = re.match(r"FROM\s+python:(\d+\.\d+)", line)
                if m:
                    return m.group(1)
    except OSError:
        pass
    return None


def satellite_checks(base: str) -> None:
    get = lambda path, **kw: fetch(base + path, **kw)  # noqa: E731

    def healthz_ok():
        status, _, text = get("/healthz")
        expect(status == 200, f"/healthz {status}")
        expect(json.loads(text).get("ok") is True, f"unexpected body {text[:120]!r}")

    def python_matches_declared():
        # WHICH interpreter serves, versus the one this repo declares. Three
        # Pythons coexisted for months on the template (image 3.11.8, matrix
        # 3.12, render.yaml 3.12.0) because nothing on the wire could
        # contradict any of them — /healthz's `python` field is the
        # observability, and this check is the teeth: the served minor must
        # equal the Dockerfile's FROM minor. A copy of this script running
        # outside a checkout has no declaration to compare, so field presence
        # alone is the check there.
        status, _, text = get("/healthz")
        expect(status == 200, f"/healthz {status}")
        served = json.loads(text).get("python") or ""
        expect(bool(served), "/healthz carries no `python` field — the "
               "serving interpreter is invisible (pre-1.6.27 build?)")
        declared = declared_python_minor()
        if declared is None:
            return
        served_minor = ".".join(served.split(".")[:2])
        expect(served_minor == declared,
               f"host serves Python {served}, repo declares {declared} — "
               "a stale image, or a platform runtime nobody aligned")

    def llms_txt_identity():
        # The check this whole standard exists for. The H1 is what an agent
        # fetching /llms.txt cold reads as the name of this site, and a
        # pre-2.3.4 artifact publishes `app.title` (or a bare "Dash") there
        # with nothing else looking wrong.
        status, headers, text = get("/llms.txt")
        expect(status == 200, f"/llms.txt {status}")
        ct = headers.get("content-type", "")
        expect(ct.startswith("text/markdown"), f"content-type {ct!r}")
        first = text.splitlines()[0] if text else ""
        expect(first == SITE_H1, f"H1 {first!r} — identity regression?")
        expect("## Pages" in text, "page index section missing")
        expect("## Network" in text, "cross-host directory missing")

    def llms_txt_names_the_hub():
        _status, _, text = get("/llms.txt")
        expect(HUB_URL in text, f"the directory does not name {HUB_URL}")

    def page_llms_nav():
        status, _, text = get(f"{SAMPLE_PAGE}/llms.txt")
        expect(status == 200, f"{SAMPLE_PAGE}/llms.txt {status}")
        expect("/llms.txt" in text, "llms_nav header missing — page doc is a dead end")

    def hidden_pages_404():
        for path in HIDDEN_DOC_PATHS:
            status, _, _ = get(path)
            expect(status == 404, f"{path} {status} (owner surface leaked)")

    def robots_artifact_fingerprint():
        # pip metadata is invisible from outside, so the robots.txt crawler
        # split is how a live host is proven to run the intended package:
        # 2.3.2 allowed OAI-SearchBot; 2.3.3 moved ClaudeBot (the training
        # crawler) to Disallow while allowing Claude-User / Claude-SearchBot.
        status, _, text = get("/robots.txt")
        expect(status == 200, f"/robots.txt {status}")
        lines = [ln.strip() for ln in text.splitlines()]

        def rule(agent):
            marker = f"User-agent: {agent}"
            expect(marker in lines, f"{marker} stanza missing")
            return lines[lines.index(marker) + 1]

        for agent, expected, since in (
            ("OAI-SearchBot", "Allow: /", "2.3.2"),
            ("Claude-User", "Allow: /", "2.3.3"),
            ("Claude-SearchBot", "Allow: /", "2.3.3"),
        ):
            got = rule(agent)
            expect(got == expected,
                   f"{agent} -> {got!r}, expected {expected!r}: pre-{since} artifact")
        # Posture, not artifact (sync item 15): no training stanza is emitted
        # at all when the wall is retired; absent or Allow is the allow shape.
        for agent in ("ClaudeBot", "GPTBot"):
            marker = f"User-agent: {agent}"
            walled = marker in lines and lines[lines.index(marker) + 1] == "Disallow: /"
            expect(not walled, f"{agent} still Disallowed: the item 15 posture flip has not landed")
        expect(any(ln.startswith("Sitemap:") for ln in lines), "Sitemap line missing")

    def sitemap_absolute_and_on_this_host():
        status, _, text = get("/sitemap.xml")
        expect(status == 200, f"/sitemap.xml {status}")
        expect("<loc>https://" in text or "<loc>http://" in text,
               "no absolute <loc> URLs")
        for path in HIDDEN_DOC_PATHS:
            leaked = path.rsplit("/llms.txt", 1)[0]
            expect(leaked not in text, f"hidden path {leaked} leaked into sitemap")

    def crawler_gets_prose():
        # The prerender. A crawler that receives the JavaScript stub indexes
        # nothing, and the page looks perfect in a browser the whole time.
        status, _, text = get("/", ua=CRAWLER_UA)
        expect(status == 200, f"/ {status}")
        expect("<title>" in text, "crawler HTML has no <title>")
        expect(STUB_MARKER not in text,
               "the home page served the JavaScript stub to a crawler")
        expect('rel="canonical"' in text, "no canonical tag for a crawler")

    def agents_and_browsers_get_different_types():
        # One URL, two audiences, and a `Vary` that stops a CDN mixing them.
        status, md_headers, md = get(f"{SAMPLE_PAGE}/llms.txt")
        expect(status == 200, f"{SAMPLE_PAGE}/llms.txt {status}")
        expect(md_headers.get("content-type", "").startswith("text/markdown"),
               f"agents got {md_headers.get('content-type')!r}")
        expect("<!DOCTYPE html>" not in md, "viewer chrome reached an agent")

        _status, html_headers, html = get(
            f"{SAMPLE_PAGE}/llms.txt",
            headers={"Accept": "text/html,application/xhtml+xml,*/*;q=0.8"})
        expect("text/html" in html_headers.get("content-type", ""),
               f"browsers got {html_headers.get('content-type')!r}")
        expect("mk-wordmark" in html, "the network wordmark is missing")

        for label, headers in (("markdown", md_headers), ("html", html_headers)):
            expect("accept" in headers.get("vary", "").lower(),
                   f"no Vary: Accept on the {label} variant — a shared cache "
                   "may serve it to everyone")

    def social_card_real_pixels():
        """The link preview, which nobody on the team ever sees.

        Every part of it breaks silently. An empty `og:image` (Dash's default
        when it is passed no `image_url` and can infer nothing) renders a blank
        card; a CDN object that starts 404ing takes every preview with it while
        the site itself looks fine; and a re-upload at a different size leaves
        every offline test green while the platform reserves the box the tags
        declare and crops into it.

        A blank preview is self-inflicting, too: platforms cache a failed
        scrape, so the first person to share the link poisons it for everyone.

        This host shipped an EMPTY og:image on every page until the 1.3.x
        network-standard pass — no register_page() call passed image_url=, so
        Dash emitted the tag with content="".
        """
        status, _, html = get("/")
        expect(status == 200, f"/ {status}")

        images = re.findall(
            r'<meta[^>]+property="og:image"[^>]*content="([^"]*)"', html)
        expect(bool(images), "no og:image tag at all")
        expect(all(src.strip() for src in images),
               "og:image is EMPTY — the link preview renders a blank card")
        expect(len(images) == 1, f"{len(images)} og:image tags — scrapers pick one")
        expect(images[0] == OG_IMAGE_URL, f"og:image is {images[0]!r}")
        expect("/assets/" not in images[0],
               "the app is serving its own card — a cold container blanks the "
               "preview, and the platform caches the miss")

        twitter = re.findall(
            r'<meta[^>]+(?:property|name)="twitter:image"[^>]*content="([^"]*)"',
            html)
        expect(bool(twitter) and all(t.strip() for t in twitter),
               "twitter:image is missing or empty")

        # The file has to exist AND be the shape the tags promise. Read the
        # bytes, not the decoded text: PNG stores its dimensions in the IHDR
        # chunk at bytes 16..24, which a lossy decode destroys.
        img_status, img_headers, raw = fetch_raw(OG_IMAGE_URL)
        expect(img_status == 200, f"the og:image URL returns {img_status}")
        expect(img_headers.get("content-type", "").startswith("image/"),
               f"og:image serves {img_headers.get('content-type')!r}")
        # 24 bytes is exactly the signature plus the IHDR width/height, which
        # is all this check reads — `>` rather than `>=` would reject a
        # perfectly readable header for being minimal.
        expect(raw[1:4] == b"PNG" and len(raw) >= 24,
               "og:image is not a PNG (or is truncated)")

        actual_w = int.from_bytes(raw[16:20], "big")
        actual_h = int.from_bytes(raw[20:24], "big")
        expect((actual_w, actual_h) == (OG_IMAGE_WIDTH, OG_IMAGE_HEIGHT),
               f"the CDN file is {actual_w}x{actual_h}, the tags declare "
               f"{OG_IMAGE_WIDTH}x{OG_IMAGE_HEIGHT}")

        declared_w = re.findall(
            r'<meta[^>]+property="og:image:width"[^>]*content="([^"]*)"', html)
        declared_h = re.findall(
            r'<meta[^>]+property="og:image:height"[^>]*content="([^"]*)"', html)
        expect(declared_w == [str(actual_w)] and declared_h == [str(actual_h)],
               f"index.html declares {declared_w}x{declared_h}, the file is "
               f"{actual_w}x{actual_h}")

    def installable_as_an_app():
        """The manifest, and whether a browser could offer to install this.

        An install prompt that is never offered reports nothing, and a
        manifest naming another site is the string an installed icon would
        carry on somebody's home screen forever.
        """
        status, _, html = get("/")
        expect(status == 200, f"/ {status}")
        visible = re.sub(r"<!--.*?-->", "", html, flags=re.S)
        match = re.search(r'<link[^>]+rel="manifest"[^>]+href="([^"]+)"', visible)
        expect(match is not None, "no manifest link — no install prompt")

        status, headers, body = get(match.group(1))
        expect(status == 200, f"the manifest link returns {status}")
        manifest = json.loads(body)
        expect(bool(manifest.get("name", "").strip()), "manifest has no name")
        expect(bool(manifest.get("short_name", "").strip()),
               "manifest has no short_name")
        for icon in manifest.get("icons") or []:
            icon_status, _, _ = get(icon["src"])
            expect(icon_status == 200, f"manifest icon {icon['src']} -> {icon_status}")

    for name, fn in (
        ("healthz_ok", healthz_ok),
        ("python_matches_declared", python_matches_declared),
        ("llms_txt_identity", llms_txt_identity),
        ("llms_txt_names_the_hub", llms_txt_names_the_hub),
        ("page_llms_nav", page_llms_nav),
        ("hidden_pages_404", hidden_pages_404),
        ("robots_artifact_fingerprint", robots_artifact_fingerprint),
        ("sitemap_absolute_and_on_this_host", sitemap_absolute_and_on_this_host),
        ("crawler_gets_prose", crawler_gets_prose),
        ("agents_and_browsers_get_different_types",
         agents_and_browsers_get_different_types),
        ("social_card_real_pixels", social_card_real_pixels),
        ("installable_as_an_app", installable_as_an_app),
    ):
        check(name, fn)


# ------------------------------------------------------------------- main --

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL,
                    help="the satellite under test (default: the CI container)")
    args = ap.parse_args()

    base = args.base_url.rstrip("/")
    print(f"network-smoke → {base}\n")
    satellite_checks(base)

    counts = {v: sum(1 for _, verdict, _ in _RESULTS if verdict == v)
              for v in (PASS, FAIL, WARN, SKIP)}
    print(f"\n{counts[PASS]} passed, {counts[FAIL]} failed, "
          f"{counts[WARN]} warnings, {counts[SKIP]} skipped")
    return 1 if counts[FAIL] else 0


if __name__ == "__main__":
    sys.exit(main())
