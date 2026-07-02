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


class Kwargs(KwargsBase):
    def hook(self, md, state):
        sections = [tok for tok in state.tokens if tok["type"] == self.block_name]

        for section in sections:
            attrs = section["attrs"]
            component_spec = attrs["title"]

            if "." in component_spec:
                package_abbr, component_name = component_spec.rsplit(".", 1)
                package = PACKAGE_MAP.get(package_abbr, package_abbr)
            else:
                package = attrs.pop("library", DEFAULT_PACKAGE)
                component_name = component_spec

            try:
                imported = importlib.import_module(package)
                component = getattr(imported, component_name)
                docstring = inspect.getdoc(component) or ""

                if "Keyword arguments:" in docstring:
                    attrs["kwargs"] = parse_dash_docstring(docstring)
                elif "----------" in docstring:
                    attrs["kwargs"] = convert_numpy_docstring_to_dict(docstring)
                else:
                    attrs["kwargs"] = []
            except Exception:
                attrs["kwargs"] = []
