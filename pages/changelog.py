"""/changelog — CHANGELOG.md as a DMC Timeline; the file itself is the LLMS_DOC.

Ported from pip-docs+ (the reference, 1.6.38). One source of truth: the
timeline is parsed from CHANGELOG.md at render time, and the crawler
document reproduces the file verbatim (minus its H1, which this page
already supplies), so the two never disagree.
"""
from __future__ import annotations

import re
from pathlib import Path

import dash
import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from lib.constants import OG_IMAGE_URL, PAGE_TITLE_PREFIX, SITE_SHORT_NAME

CHANGELOG_PATH = Path(__file__).resolve().parent.parent / "CHANGELOG.md"

dash.register_page(
    __name__,
    path="/changelog",
    name="Changelog",
    title=PAGE_TITLE_PREFIX + "Changelog",
    description=f"Version history of {SITE_SHORT_NAME}, rendered from CHANGELOG.md.",
    image_url=OG_IMAGE_URL,
    icon="tabler:history",
)


def _build_llms_doc() -> str:
    intro = (
        "# Changelog\n\n"
        f"> Version history of {SITE_SHORT_NAME}. The timeline on this page is "
        "rendered from `CHANGELOG.md`, reproduced below.\n\n---\n\n"
    )
    try:
        body = CHANGELOG_PATH.read_text(encoding="utf-8")
    except OSError:
        return intro
    # CHANGELOG.md opens with its own `# Changelog` H1 and the intro already
    # supplies one — two identical h1s is the every-page structure pin's red.
    lines = body.split("\n")
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        if line.startswith("# "):
            lines = lines[i + 1:]
        break
    return intro + "\n".join(lines).lstrip("\n")


LLMS_DOC = _build_llms_doc()


def parse_changelog(path: Path = CHANGELOG_PATH) -> list[dict]:
    """``[{version, date, sections: {name: [items]}}]`` in file order."""
    if not path.exists():
        return []
    versions: list[dict] = []
    current = None
    sections: dict = {}
    section = None
    items: list = []

    def close_section():
        if current is not None and section:
            sections.setdefault(section, []).extend(items)

    for line in path.read_text(encoding="utf-8").split("\n"):
        vm = re.match(r"^## \[([^\]]+)\](?: - (.+))?", line)
        if vm:
            close_section()
            if current is not None:
                versions.append({**current, "sections": sections})
            current = {"version": vm.group(1), "date": vm.group(2) or ""}
            sections, section, items = {}, None, []
            continue
        sm = re.match(r"^### (.+)", line)
        if sm and current is not None:
            close_section()
            section, items = sm.group(1), []
            continue
        if current is None or not section:
            continue
        if line.startswith("- "):
            items.append({"type": "item", "text": line[2:]})
        elif line.startswith("  - "):
            items.append({"type": "subitem", "text": line[4:]})
        elif line.startswith("  ") and items and items[-1]["type"] in ("item", "subitem"):
            items[-1]["text"] += " " + line.strip()      # wrapped bullet
    close_section()
    if current is not None:
        versions.append({**current, "sections": sections})
    return versions


_SECTION_ICONS = {
    "added": ("tabler:plus", "green"),
    "changed": ("tabler:refresh", "blue"),
    "fixed": ("tabler:bug", "orange"),
    "removed": ("tabler:trash", "red"),
    "deprecated": ("tabler:alert-triangle", "yellow"),
    "security": ("tabler:shield-check", "violet"),
    "recorded": ("tabler:notes", "gray"),
}


def _section_icon(name: str):
    for key, val in _SECTION_ICONS.items():
        if key in name.lower():
            return val
    return "tabler:point", "gray"


def _inline(text: str):
    """`code` and **bold** inside one bullet."""
    out = []
    for i, part in enumerate(re.split(r"`([^`]+)`", text)):
        if i % 2:
            out.append(dmc.Code(part, style={"overflowWrap": "anywhere"}))
            continue
        for j, bp in enumerate(re.split(r"\*\*([^*]+)\*\*", part)):
            if not bp:
                continue
            out.append(html.Strong(bp) if j % 2 else bp)
    return out


# A bullet in a no-wrap Group: without min-width:0 the Text grows to the
# width of its longest unbreakable token — a 60-character test name in a
# `code` span — and the row leaves its card (measured on a phone: a 429px
# paragraph in a 218px group, a 549px document at 391px). `anywhere` lets
# that token break; the Code spans get the same.
_WRAP = {"flex": 1, "minWidth": 0, "overflowWrap": "anywhere"}


def _section(name: str, items: list):
    icon, color = _section_icon(name)
    rows = []
    for it in items:
        if it["type"] == "item":
            rows.append(dmc.Group(
                [DashIconify(icon="tabler:point-filled", width=8, color=f"var(--mantine-color-{color}-6)"),
                 dmc.Text(_inline(it["text"]), size="sm", style=_WRAP)],
                gap="xs", align="flex-start", wrap="nowrap"))
        else:
            rows.append(dmc.Group(
                [dmc.Box(w=16), DashIconify(icon="tabler:point", width=6),
                 dmc.Text(_inline(it["text"]), size="xs", c="dimmed", style=_WRAP)],
                gap="xs", align="flex-start", wrap="nowrap", ml="md"))
    return dmc.Paper(
        [dmc.Group([dmc.ThemeIcon(DashIconify(icon=icon, width=16), color=color,
                                  variant="light", size="sm", radius="xl"),
                    dmc.Text(name, fw=600, size="sm")], gap="xs", mb="xs"),
         dmc.Stack(rows, gap=4)],
        p="sm", radius="md", withBorder=True, mb="xs")


def _version_item(v: dict, is_current: bool):
    cards = [_section(n, items) for n, items in v["sections"].items() if items]
    return dmc.TimelineItem(
        bullet=dmc.ThemeIcon(DashIconify(icon="tabler:rocket", width=16),
                             variant="filled" if is_current else "light", size=28, radius="xl"),
        title=dmc.Group(
            [dmc.Badge(f"v{v['version']}", variant="filled" if is_current else "light", size="lg"),
             dmc.Text(v["date"], size="sm", c="dimmed") if v["date"] else None,
             dmc.Badge("Current", color="green", variant="outline", size="sm") if is_current else None],
            gap="sm"),
        children=dmc.Stack(cards, gap="xs", mt="sm") if cards
        else dmc.Text("No changes documented", c="dimmed", size="sm"),
    )


def timeline(versions: list[dict]):
    if not versions:
        return dmc.Text("CHANGELOG.md could not be found or parsed.", c="dimmed")
    return dmc.Timeline(
        [_version_item(v, i == 0) for i, v in enumerate(versions)],
        active=0, bulletSize=32, lineWidth=2,
    )


def layout(**kwargs):
    versions = parse_changelog()
    return dmc.Container(
        [
            dmc.Group(
                [dmc.ThemeIcon(DashIconify(icon="tabler:history", width=28), size=48, radius="md", variant="light"),
                 dmc.Stack([dmc.Title("Changelog", order=1),
                            dmc.Text(f"All notable changes to {SITE_SHORT_NAME}.", c="dimmed")], gap=0)],
                gap="md", mb="md"),
            dmc.Badge(f"{len(versions)} release{'s' if len(versions) != 1 else ''}",
                      variant="light", size="lg", mb="xl"),
            dmc.Divider(mb="xl"),
            timeline(versions),
            dmc.Text(
                ["This changelog follows ",
                 dmc.Anchor("Keep a Changelog", href="https://keepachangelog.com/en/1.1.0/", target="_blank"),
                 " and ", dmc.Anchor("Semantic Versioning", href="https://semver.org/", target="_blank"), "."],
                size="sm", c="dimmed", mt="xl"),
        ],
        id="m2d-page-changelog",
        size="md",
        py="xl",
    )
