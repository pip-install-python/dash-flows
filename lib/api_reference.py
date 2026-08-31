"""Component prop tables from an installed Dash component package (1.6.38).

Three sources, in order (1.6.41 — leaflet's and modelviewer's findings):

1. ``metadata.json`` next to the package's ``__init__`` — react-docgen
   output: one entry per component source file with ``displayName`` and
   ``props`` → ``{type, required, description, defaultValue}``. On a
   pip-installed package it is there; in a component REPO it can be a
   27 MB gitignored build artifact excluded from the wheel (leaflet), so
   /api passes locally and is EMPTY on the host.
2. ``api_metadata.json`` next to the package — the committed extract
   ``scripts/build_api_metadata.py`` writes in this module's output shape
   (~1% of the size), stamped ``generated`` for the sitemap lastmod.
3. The component classes' docstrings — Dash's generated classes list
   every prop under ``Keyword arguments:`` as ``- name (type; optional):
   description``; hook-based packages ship no metadata at all
   (modelviewer) and this is what remains.

(The drop named ``_prop_names``; Dash 4 no longer sets it on generated
classes — the docstring and metadata.json are what exist.)
"""
from __future__ import annotations

import importlib
import inspect
import json
import re
from pathlib import Path

SLIM_METADATA = "api_metadata.json"
_SKIP_PROPS = ("setProps", "loading_state")


def _type_name(t) -> str:
    if not isinstance(t, dict):
        return str(t or "")
    name = t.get("name") or ""
    if name == "enum" and isinstance(t.get("value"), list):
        vals = [str(v.get("value", v)) for v in t["value"]]
        return "one of " + ", ".join(vals[:8]) + (" …" if len(vals) > 8 else "")
    if name == "union" and isinstance(t.get("value"), list):
        return " | ".join(_type_name(v) for v in t["value"])
    if name == "arrayOf":
        return f"list of {_type_name(t.get('value'))}"
    if name in ("shape", "exact"):
        return "dict"
    return name or "any"


def _default(prop) -> str:
    d = prop.get("defaultValue")
    if isinstance(d, dict):
        return str(d.get("value", ""))
    return "" if d is None else str(d)


def _sort(props: list[dict]) -> list[dict]:
    props.sort(key=lambda p: (p["name"] != "id", p["name"]))
    return props


def _from_metadata(mod, meta_path: Path) -> list[dict]:
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    out = []
    for entry in meta.values():
        name = entry.get("displayName") or ""
        if not name or not hasattr(mod, name):
            continue
        props = [{
            "name": pname,
            "type": _type_name(p.get("type") or p.get("flowType") or p.get("tsType")),
            "required": bool(p.get("required")),
            "default": _default(p),
            "description": (p.get("description") or "").strip(),
        } for pname, p in (entry.get("props") or {}).items() if pname not in _SKIP_PROPS]
        out.append({"name": name, "description": (entry.get("description") or "").strip(),
                    "props": _sort(props)})
    out.sort(key=lambda c: c["name"])
    return out


# `- name (type; optional): description` / `- name (type; required)` /
# `- name (type; default 0): description`, description continuing on
# indented lines until the next `- ` or a blank line.
_DOC_PROP = re.compile(r"^- (?P<name>\w+) \((?P<type>.*?)(?:; (?P<req>optional|required|default [^)]*))?\):\s*(?P<desc>.*)$")


def _from_docstrings(mod) -> list[dict]:
    """Every exported class whose docstring carries a ``Keyword arguments:``
    section — Dash's generated components all do."""
    out = []
    for name, obj in vars(mod).items():
        if not inspect.isclass(obj) or name.startswith("_"):
            continue
        doc = inspect.getdoc(obj) or ""
        if "Keyword arguments:" not in doc:
            continue
        head, _, tail = doc.partition("Keyword arguments:")
        props, current = [], None
        for line in tail.splitlines():
            m = _DOC_PROP.match(line.strip()) if line.startswith("- ") else None
            if m:
                req = m.group("req") or ""
                current = {"name": m.group("name"), "type": m.group("type"),
                           "required": req == "required",
                           "default": req[len("default "):] if req.startswith("default ") else "",
                           "description": m.group("desc").strip()}
                if current["name"] not in _SKIP_PROPS:
                    props.append(current)
            elif current is not None and line.strip() and line.startswith(" "):
                current["description"] = (current["description"] + " " + line.strip()).strip()
            elif not line.strip():
                current = None
        description = " ".join(ln.strip() for ln in head.splitlines()[1:] if ln.strip())
        out.append({"name": name, "description": description, "props": _sort(props)})
    out.sort(key=lambda c: c["name"])
    return out


def load_package(package: str) -> list[dict]:
    """``[{name, description, props: [{name, type, required, default, description}]}]``
    for every component the package exports, sorted by name — from
    metadata.json, else the committed extract, else the docstrings. Raises
    ImportError if the package is not installed."""
    mod = importlib.import_module(package)
    pkg_dir = Path(mod.__file__).resolve().parent
    meta_path = pkg_dir / "metadata.json"
    if meta_path.is_file():
        return _from_metadata(mod, meta_path)
    slim = pkg_dir / SLIM_METADATA
    if slim.is_file():
        data = json.loads(slim.read_text(encoding="utf-8"))
        return data["components"] if isinstance(data, dict) else data
    return _from_docstrings(mod)


def slim_generated_on(package: str) -> str | None:
    """The ``generated`` date of the committed extract — /api's lastmod. It
    moves exactly when the script that regenerates the content runs, and it
    is committed, so a Docker rebuild cannot reset it the way an mtime can."""
    try:
        mod = importlib.import_module(package)
        data = json.loads((Path(mod.__file__).resolve().parent / SLIM_METADATA).read_text(encoding="utf-8"))
        return data.get("generated") if isinstance(data, dict) else None
    except Exception:  # noqa: BLE001
        return None


def load_packages(packages) -> list[dict]:
    """Every package's components, in declaration order; a missing package
    is reported as one entry with an ``error`` rather than raising — the
    page must render on a host whose extra is not installed."""
    out = []
    for pkg in packages:
        try:
            out.append({"package": pkg, "components": load_package(pkg)})
        except Exception as exc:  # noqa: BLE001
            out.append({"package": pkg, "components": [], "error": f"{type(exc).__name__}: {exc}"})
    return out


def _cell(text) -> str:
    """One Markdown table cell: no newlines, no unescaped pipes — in EVERY
    cell (a type like `a | b` broke the table as surely as a description)."""
    return str(text).replace("\n", " ").replace("|", "\\|")


def as_markdown(packages) -> str:
    """The same tables as Markdown — the page's LLMS_DOC."""
    lines = ["# API reference", ""]
    for pkg in load_packages(packages):
        lines += [f"## {pkg['package']}", ""]
        if pkg.get("error"):
            lines += [f"_not installed: {pkg['error']}_", ""]
        for c in pkg["components"]:
            lines += [f"### {c['name']}", ""]
            if c["description"]:
                lines += [c["description"], ""]
            lines += ["| prop | type | default | description |", "|---|---|---|---|"]
            for p in c["props"]:
                lines.append(f"| `{_cell(p['name'])}`{' *' if p['required'] else ''} | {_cell(p['type'])} | {_cell(p['default'])} | {_cell(p['description'])} |")
            lines.append("")
    return "\n".join(lines)
