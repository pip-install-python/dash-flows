"""`.. kwargs::Component` directive.

Renders an auto-generated prop table for a component. Handles two docstring
styles:

* **Dash-generated components** (e.g. ``dash_flows.DashFlows``) use a
  ``Keyword arguments:`` section with ``- name (type; default X): desc`` items.
* **DMC / numpy-style** components use a ``----------`` parameter block.

Usage in markdown::

    .. kwargs::dash_flows.DashFlows
    .. kwargs::df.DashFlows          # `df` is aliased to dash_flows
    .. kwargs::dmc.Button
"""
import importlib
import inspect
import re

from markdown2dash.src.directives.kwargs import Kwargs as KwargsBase

# `package.Component` abbreviations understood in `.. kwargs::` titles.
PACKAGE_MAP = {
    "df": "dash_flows",
    "dash_flows": "dash_flows",
    "dmc": "dash_mantine_components",
    "html": "dash.html",
    "dcc": "dash.dcc",
    "dash": "dash",
}

DEFAULT_PACKAGE = "dash_flows"

# Matches a top-level Dash prop line:  "- nodes (list; optional): The nodes."
_DASH_PROP_RE = re.compile(r"^- (?P<name>[\w-]+) \((?P<type>[^)]*)\):\s*(?P<desc>.*)$")


def parse_dash_docstring(docstring):
    """Parse a Dash-generated ``Keyword arguments:`` block into prop dicts.

    Returns a list of ``{"name", "type", "description"}``. Nested/sub-props
    (indented ``- key`` items) are folded into the parent's description so the
    table stays flat and readable.
    """
    if "Keyword arguments:" in docstring:
        docstring = docstring.split("Keyword arguments:", 1)[1]

    params = []
    current = None
    for raw in docstring.split("\n"):
        # Only lines beginning at column 0 with "- " start a new top-level prop.
        if raw.startswith("- "):
            match = _DASH_PROP_RE.match(raw.strip())
            if match:
                if current:
                    params.append(current)
                current = {
                    "name": match.group("name"),
                    "type": match.group("type"),
                    "description": match.group("desc").strip(),
                }
                continue
        if current is not None:
            stripped = raw.strip()
            if stripped:
                joiner = " " if current["description"] else ""
                current["description"] += joiner + stripped
    if current:
        params.append(current)
    return params


def convert_numpy_docstring_to_dict(docstring):
    """Parse a numpy-style ``----------`` parameter block (DMC components)."""
    lines = docstring.split("----------\n")[-1].split("\n")
    params = []
    new_param = None
    for line in lines:
        if not line.startswith("    "):
            if new_param is not None:
                params.append(new_param)
                new_param = None
            if ": " not in line:
                continue
            name, type_ = line.split(": ", 1)
            new_param = {"name": name, "type": type_, "description": ""}
        elif new_param is not None:
            new_param["description"] += " " + line.strip()
    if new_param is not None:
        params.append(new_param)
    return params


def _resolve(component_spec: str, library: str | None = None):
    """``"dash_flows.DashFlows"`` / ``"dmc.Button"`` / ``"Button"`` (+
    ``library=``) -> the class, docstring."""
    if "." in component_spec:
        package_abbr, component_name = component_spec.rsplit(".", 1)
        package = PACKAGE_MAP.get(package_abbr, package_abbr)
    else:
        package = library or DEFAULT_PACKAGE
        component_name = component_spec
    imported = importlib.import_module(package)
    component = getattr(imported, component_name)
    return inspect.getdoc(component) or ""


def props_for(component_spec: str, library: str | None = None) -> list:
    """Every documented prop for ``component_spec``, or ``[]``.

    ONE parse for both consumers (a markdown2dash DIRECTIVE renders Dash
    COMPONENTS, so its table exists only in the browser's React tree — the
    machine lane and the non-JS prerender are built from the markdown
    SOURCE, where the directive line is stripped; `docs/api_reference/
    api_reference.md`'s `.. kwargs::` tables were silently EMPTY on both
    until this was ported, sync item 18 contract highlight 7-amended,
    muicharts' finding 2026-08-30). `Kwargs.hook` below (the browser
    table) and `pages/markdown.py`'s directive expansion (the machine
    prose) both call this — two implementations of "what are this
    component's props" is exactly how the lanes drifted apart.
    """
    try:
        docstring = _resolve(component_spec, library)
    except Exception:
        return []
    if "Keyword arguments:" in docstring:
        return parse_dash_docstring(docstring)
    if "----------" in docstring:
        return convert_numpy_docstring_to_dict(docstring)
    return []


def _cell(text) -> str:
    """A markdown table cell: no pipes, no newlines, both of which end a row."""
    return " ".join(str(text or "").split()).replace("|", "\\|")


def props_markdown(component_spec: str, library: str | None = None) -> str:
    """``props_for`` as a markdown table, for the machine lane
    (`pages/markdown.py`'s fence-aware `.. kwargs::` expansion — the same
    treatment as `.. source::`, for the same reason).

    An HTML comment rather than silence when there is nothing to say: a
    component whose props cannot be read is a defect worth seeing in the
    document's source, and this is the lane nobody looks at by default.
    """
    rows = props_for(component_spec, library)
    if not rows:
        return f"\n<!-- No documented props found for {component_spec} -->\n"
    out = ["", "| Name | Type | Description |", "| --- | --- | --- |"]
    for row in rows:
        out.append("| " + " | ".join(
            _cell(row.get(k)) for k in ("name", "type", "description")) + " |")
    out.append("")
    return "\n".join(out)


class Kwargs(KwargsBase):
    def hook(self, md, state):
        sections = [tok for tok in state.tokens if tok["type"] == self.block_name]

        for section in sections:
            attrs = section["attrs"]
            component_spec = attrs["title"]
            library = attrs.pop("library", None)
            attrs["kwargs"] = props_for(component_spec, library)
