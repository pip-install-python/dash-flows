"""Version claims are derived from the installed packages, never written.

Prose that states a package version writes ``{{VERSION:<distribution>}}``
— the name exactly as it appears on PyPI and in ``pip install`` — and the
markdown loaders substitute the version of whatever is actually installed.
The served documents are the network's point of truth, and a hardcoded
number is a lie waiting for the next release: "Powered by 2.3.4" shipped
on /llms.txt for months while 2.5.1 was serving the site.

The general form exists so every satellite forked from this template can
make the same claim about the package IT documents ("dash-mui-charts
{{VERSION:dash-mui-charts}}") without touching loader code — bump the
package, redeploy, and the browser page, the copy button, /llms.txt and
every /<page>/llms.txt publish the new number together.

Fenced code blocks and inline code spans are left verbatim: a code example
*showing* the placeholder syntax (docs/network-standard does) must render
the syntax, not the substituted number.

A placeholder naming a distribution that is not installed raises at load
time. Both loaders run at import, so a typo fails the boot (and therefore
CI) instead of leaking ``{{VERSION:...}}`` into served prose — the same
loud-over-silent choice the identity tests make.
"""
from __future__ import annotations

import re
from importlib.metadata import PackageNotFoundError, version

_PLACEHOLDER = re.compile(r"\{\{VERSION:([A-Za-z0-9._-]+)\}\}")

# The first placeholder, from before the general form existed (the 2026-08-14
# truth sweep). Satellites forked in that window may still write it.
_LEGACY = "{{DIMLL_VERSION}}"
_LEGACY_DIST = "dash-improve-my-llms"

_FENCE = re.compile(r"^\s*(```|~~~)")
# Inline code spans, shortest match — `code`. CommonMark lets a span cross a
# soft line break, so newlines are allowed inside. Split with a capture group
# so the spans survive into the output untouched.
_CODE_SPAN = re.compile(r"(`[^`]+`)")


def _substitute_prose(text: str, source: str) -> str:
    def replace(match: re.Match) -> str:
        dist = match.group(1)
        try:
            return version(dist)
        except PackageNotFoundError:
            raise LookupError(
                f"{source} claims a version for {dist!r}, but that "
                "distribution is not installed — the claim cannot be true. "
                "Fix the {{VERSION:...}} name or install the package."
            ) from None

    out = []
    for part in _CODE_SPAN.split(text):
        if part.startswith("`"):
            out.append(part)
            continue
        part = part.replace(_LEGACY, f"{{{{VERSION:{_LEGACY_DIST}}}}}")
        out.append(_PLACEHOLDER.sub(replace, part))
    return "".join(out)


def substitute_versions(content: str, *, source: str = "<markdown>") -> str:
    """Replace every version placeholder in ``content`` (outside code) with
    the installed distribution's version. ``source`` names the file in the
    error message."""
    out = []
    prose: list[str] = []
    in_fence = False

    def flush():
        if prose:
            out.append(_substitute_prose("".join(prose), source))
            prose.clear()

    for line in content.splitlines(keepends=True):
        if _FENCE.match(line):
            flush()
            in_fence = not in_fence
            out.append(line)
        elif in_fence:
            out.append(line)
        else:
            prose.append(line)
    flush()
    return "".join(out)
