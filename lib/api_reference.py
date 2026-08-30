"""Component prop tables from an installed Dash component package (1.6.38).

A Dash component package ships ``metadata.json`` next to its ``__init__``
(react-docgen output: one entry per component source file with
``displayName`` and ``props`` → ``{type, required, description,
defaultValue}``), and every generated component class carries the same
props in its docstring. ``metadata.json`` is the one machine-readable
source, so this reads it; the classes exist in the package namespace and
are used only to confirm a component is exported. (The drop named
``_prop_names``; Dash 4 no longer sets it on generated classes — the
docstring and metadata.json are what remain.)
"""
from __future__ import annotations

import importlib
import json
from pathlib import Path


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


def load_package(package: str) -> list[dict]:
    """``[{name, description, props: [{name, type, required, default, description}]}]``
    for every component the package exports, sorted by name. Raises
    ImportError if the package is not installed; returns [] if it ships no
    metadata.json (not a Dash component package)."""
    mod = importlib.import_module(package)
    meta_path = Path(mod.__file__).resolve().parent / "metadata.json"
    if not meta_path.is_file():
        return []
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    out = []
    for entry in meta.values():
        name = entry.get("displayName") or ""
        if not name or not hasattr(mod, name):
            continue
        props = []
        for pname, p in (entry.get("props") or {}).items():
            if pname in ("setProps", "loading_state"):
                continue
            props.append({
                "name": pname,
                "type": _type_name(p.get("type") or p.get("flowType") or p.get("tsType")),
                "required": bool(p.get("required")),
                "default": _default(p),
                "description": (p.get("description") or "").strip(),
            })
        props.sort(key=lambda p: (p["name"] != "id", p["name"]))
        out.append({"name": name, "description": (entry.get("description") or "").strip(), "props": props})
    out.sort(key=lambda c: c["name"])
    return out


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
                desc = p["description"].replace("\n", " ").replace("|", "\\|")
                lines.append(f"| `{p['name']}`{' *' if p['required'] else ''} | {p['type']} | {p['default']} | {desc} |")
            lines.append("")
    return "\n".join(lines)
