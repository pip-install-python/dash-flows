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

CHANGELOG_DESCRIPTION = f"Version history of {SITE_SHORT_NAME}, rendered from CHANGELOG.md."

dash.register_page(
    __name__,
    path="/changelog",
    name="Changelog",
    title=PAGE_TITLE_PREFIX + "Changelog",
    description=CHANGELOG_DESCRIPTION,
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


def newest_date(path: Path = CHANGELOG_PATH) -> str | None:
    """The newest dated release heading — /changelog's sitemap lastmod. It
    moves exactly when the content moves (a release is dated by hand)."""
    dates = [v["date"] for v in parse_changelog(path) if v.get("date")]
    return max(dates) if dates else None


def _is_version(label: str) -> bool:
    return bool(re.fullmatch(r"\d+(\.\d+)*", label))


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
        # ASCII hyphen, en dash or em dash between version and date —
        # leaflet's headings use "—" and rendered every version DATELESS.
        # Every heading shape the fleet writes (measured 2026-08-30):
        #   ## [1.4.0] - 2026-08-03            hyphen
        #   ## [1.0.0] — 2026-08-21            em dash (en dash too)
        #   ## 2.0.0 — 2026-08-02              no brackets
        #   ## [0.2.0] — 2026-07-31 (note)     trailing note
        #   ## [0.1.0] — unreleased            words where the date goes
        #   ## [2026-08-30] — title            the date IS the label
        #   ## [Unreleased]
        # Parsed as [?label]? (sep)? rest?, with the ISO date taken from
        # wherever it sits and the leftover kept as a note.
        vm = re.match(r"^## \[?(?P<label>[^\]#\n]+?)\]?(?:\s+[-–—]\s+(?P<rest>.+?))?\s*$", line)
        if vm:
            close_section()
            if current is not None:
                versions.append({**current, "sections": sections})
            label, rest = vm.group("label").strip(), (vm.group("rest") or "").strip()
            iso = re.search(r"\d{4}-\d{2}-\d{2}", rest) or re.search(r"\d{4}-\d{2}-\d{2}", label)
            date = iso.group(0) if iso else ""
            note = rest.replace(date, "").strip(" -–—()") if rest else ""
            current = {"version": label, "date": date, "note": note}
            sections, section, items = {}, None, []
            continue
        sm = re.match(r"^### (.+)", line)
        if sm and current is not None:
            close_section()
            section, items = sm.group(1), []
            continue
        if current is None:
            continue
        if not section:
            # Prose-first releases (pannellum: `## 2.0.0 — date` then
            # paragraphs, no ### sections) rendered EIGHT EMPTY HEADINGS
            # silently. Prose under a version heading is its own section.
            if line.strip() and not line.startswith("#"):
                section, items = "Notes", []
            else:
                continue
        if line.startswith("- "):
            items.append({"type": "item", "text": line[2:]})
        elif line.startswith("  - "):
            items.append({"type": "subitem", "text": line[4:]})
        elif line.startswith("  ") and items and items[-1]["type"] in ("item", "subitem"):
            items[-1]["text"] += " " + line.strip()      # wrapped bullet
        elif line.strip() and not line.startswith("#"):
            if items and items[-1]["type"] == "para" and not items[-1].get("closed"):
                items[-1]["text"] += " " + line.strip()
            else:
                items.append({"type": "para", "text": line.strip()})
        elif not line.strip() and items and items[-1]["type"] == "para":
            items[-1]["closed"] = True
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


def _code(text: str):
    out = []
    for i, part in enumerate(re.split(r"`([^`]+)`", text)):
        if not part:
            continue
        out.append(dmc.Code(part, style={"overflowWrap": "anywhere"}) if i % 2 else part)
    return out


def _inline(text: str):
    """**bold** first, then `code` — in that order on purpose (note 67):
    a bold span CONTAINING inline code rendered its asterisks raw when
    code was split first, because the bold markers then sat in different
    fragments."""
    out = []
    for j, part in enumerate(re.split(r"\*\*(.+?)\*\*", text)):
        if not part:
            continue
        if j % 2:
            out.append(html.Strong(_code(part)))
        else:
            out.extend(_code(part))
    return out or [text]


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
        elif it["type"] == "para":
            rows.append(dmc.Text(_inline(it["text"]), size="sm", style=_WRAP))
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
    # `v` only when the label IS a version: `## [Unreleased]` read as
    # "VUNRELEASED" and a date-labelled release as "v2026-08-30" (note 67).
    label = f"v{v['version']}" if _is_version(v["version"]) else v["version"]
    when = " ".join(x for x in (v.get("date", ""), v.get("note", "")) if x)
    return dmc.TimelineItem(
        bullet=dmc.ThemeIcon(DashIconify(icon="tabler:rocket", width=16),
                             variant="filled" if is_current else "light", size=28, radius="xl"),
        title=dmc.Group(
            [dmc.Badge(label, variant="filled" if is_current else "light", size="lg"),
             dmc.Text(when, size="sm", c="dimmed") if when else None,
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


# The full machine record (1.6.41; leaflet's finding): a module-level
# LLMS_DOC alone leaves the package to discover the page with no
# `lastmod`, so /changelog entered the sitemap undated — and outside the
# control board's llms.txt toggle. Same two calls pages/markdown.py makes
# for every docs page; lastmod = the newest dated release heading.
from dash_improve_my_llms import register_page_metadata  # noqa: E402

from lib import page_tiers, page_visibility  # noqa: E402

page_visibility.register_default("/changelog", "Changelog", visibility="public", llms_public=True)
page_tiers.register("/changelog", "public", llms_public=True)
register_page_metadata(
    path="/changelog",
    name="Changelog",
    description=CHANGELOG_DESCRIPTION,
    title=PAGE_TITLE_PREFIX + "Changelog",
    image_url=OG_IMAGE_URL,
    schema_type="TechArticle",
    lastmod=newest_date(),
    llms_doc=LLMS_DOC,
)
