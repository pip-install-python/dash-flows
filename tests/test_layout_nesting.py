"""No page layout nests a list directly inside a children list.

THE DEFECT (modelviewer, found on the wire 2026-08-30, reported by the
ops seat): a page composed its layout as

    children=[hero, create_parser(...)(content)]

markdown2dash's parser returns a **list**, so that expression puts a
list *inside* a children list. Dash does not descend into a nested
list — React logs #31 and the page subtree renders EMPTY while the app
shell around it looks perfectly healthy. The suite was green. Every
smoke check was green. The page was blank.

WHY NOTHING SAW IT: the prerender is built from the MARKDOWN, so every
machine-lane check reads a fine document while the browser lane is
empty — item 17's lane split, one layer up. The only surface that shows
it is a browser, which is why this is a pin and not a review note.

Adopted from emojimart (44ae41b), which reproduces modelviewer's
failing path character for character; the positive-control page is
derived from the registry here rather than named.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest
from dash.development.base_component import Component

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def _walk(node, path: str, findings: list) -> None:
    """Depth-first, recording any list found as a direct element of a
    children list. `path` mirrors the modelviewer report's shape:
    `/.Container.children[1]`."""
    if isinstance(node, (list, tuple)):
        for i, child in enumerate(node):
            _walk(child, f"{path}[{i}]", findings)
        return
    if not isinstance(node, Component):
        return
    children = getattr(node, "children", None)
    here = f"{path}.{type(node).__name__}"
    if isinstance(children, (list, tuple)):
        for i, child in enumerate(children):
            if isinstance(child, (list, tuple)):
                findings.append(f"{here}.children[{i}]")
                # Keep walking it — one nest can hide another.
            _walk(child, f"{here}.children[{i}]", findings)
    elif children is not None:
        _walk(children, f"{here}.children", findings)


def _resolve(layout):
    """Page layouts may be values or callables (this repo wraps every docs
    page in `gate_layouts.gated_layout`, which decides per render)."""
    return layout() if callable(layout) else layout


@pytest.fixture(scope="module")
def registry(app_module):
    import dash

    return dict(dash.page_registry)


def test_the_walk_itself_sees_a_nested_list():
    """Non-vacuity: the walk must flag the modelviewer shape when it exists
    — a guard that cannot go red guards nothing."""
    import dash_mantine_components as dmc

    bad = dmc.Container([dmc.Title("Hero"), [dmc.Text("parsed"), dmc.Text("list")]])
    findings: list = []
    _walk(bad, "/fixture", findings)
    assert findings == ["/fixture.Container.children[1]"]


def test_no_page_nests_a_list_inside_a_children_list(registry):
    findings: list[str] = []
    unresolved: list[str] = []

    for page in registry.values():
        path = page.get("path") or page.get("module")
        try:
            layout = _resolve(page.get("layout"))
        except Exception as exc:  # a layout needing a request context
            unresolved.append(f"{path}: {type(exc).__name__}")
            continue
        _walk(layout, path, findings)

    assert not findings, (
        "a list nested directly inside a children list renders EMPTY and "
        "says nothing about it (Dash does not descend; React #31). Splat it "
        f"(`*parsed`) or concatenate (`[...] + parsed`): {findings}"
    )
    # Not a silent skip: if a layout could not be built, say which, so this
    # test cannot pass by having walked nothing.
    assert len(unresolved) < len(registry), f"nothing walked; all failed: {unresolved}"


def test_a_docs_page_really_carries_its_parsed_content(registry, monkeypatch):
    """The positive control. The walk alone passes on a page that is empty
    for any OTHER reason — the same symptom the defect produces. A real
    docs page (derived from the registry: the first page that registered a
    TOC) must render real depth and contain its own heading."""
    monkeypatch.setenv("ALLOW_UNGATED_ADMIN", "0")
    from lib.aside import ASIDE_PATHS

    by_path = {p.get("path"): p for p in registry.values()}
    page = by_path[sorted(ASIDE_PATHS)[0]]
    layout = _resolve(page["layout"])

    nodes: list = []

    def count(node):
        if isinstance(node, (list, tuple)):
            for c in node:
                count(c)
            return
        if isinstance(node, Component):
            nodes.append(node)
            children = getattr(node, "children", None)
            if children is not None:
                count(children)

    count(layout)
    assert len(nodes) > 20, f"only {len(nodes)} components — is the page empty?"
    assert page["name"] in str(layout), "the page's own heading is missing"


def test_the_markdown_page_builder_concatenates_rather_than_nesting():
    """The source pin, because the walk only sees the pages that exist
    today. `parse()` returns a LIST; the builders must flatten it."""
    for fname, parser_name in (("pages/markdown.py", "parse"),
                               ("pages/home.py", "create_parser")):
        src = (REPO_ROOT / fname).read_text()
        tree = ast.parse(src)
        nested = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.List):
                continue
            for element in node.elts:
                if isinstance(element, ast.Call):
                    f = element.func
                    name = getattr(f, "id", getattr(f, "attr", ""))
                    called = getattr(getattr(element.func, "func", None), "id", "")
                    if name == parser_name or called == parser_name:
                        nested.append(f"{fname}: {ast.dump(element)[:60]}")
        assert not nested, (
            "parse() returns a list; putting that call directly inside a "
            f"list display nests it and the page renders blank: {nested}"
        )
