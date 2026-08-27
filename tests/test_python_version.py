"""One fleet Python — the image, the CI matrix and the wire must agree.

Found by the ops seat reading the template's tree, not a report (2026-08-25):
the Dockerfile said `python:3.11.8-slim` — a PATCH pin, so the image never
received a 3.11.x security release — while the CI matrix said 3.12 and
render.yaml said 3.12.0. Three declared Pythons, the docker boot/battery
testing an interpreter the matrix never ran, and nothing on the wire able to
contradict any of them. These pins hold every encoding to ONE minor, sourced
from the Dockerfile's FROM tag; /healthz's `python` field plus the
`python_matches_declared` battery check (scripts/network_smoke.py) hold the
serving host to the same one.

ADAPTED FROM THE TEMPLATE'S COPY, in two places, because this fork's shape
differs (DIVERGENCES.md 5 and 1):

  * The template's service is `runtime: python`, where Render honours a
    PYTHON_VERSION env var, so its copy pins that value's minor against the
    image. This service is `runtime: docker`: the image IS the runtime and
    the key is inert. Pinning an inert key would be worse than not having it
    — a decorative version string in the Blueprint is exactly the confusion
    the item exists to end — so the pin below asserts the ABSENCE instead,
    and flips to the template's assertion the day the runtime changes.

  * This repo's examples matrix varies dash AND python, so its window legs
    are `python:` scalars nested under `- dash:` entries rather than the
    template's `- python:` list items. Same contract, different selector.

WHICH LANE EACH PIN READS (template 1.6.28's amendment: name it, because a
fork with two lanes has two Pythons and a session must be able to tell which
one a red pin is about). This repo has both:

  * SITE lane — `lint`, `docs-tests`, `pip-audit`, the `docker` job and
    cd.yml's verify job. These install `requirements-docs.txt` and boot or
    probe the docs app, so they are the image's business and every one of
    them is pinned to the Dockerfile's minor below.
  * PACKAGE lanes — `examples` (every example app imported and served across
    a dash x python matrix) and `package` (the dash-flows wheel built and
    installed in a clean venv). These are the COMPONENT LIBRARY's business
    and the spec puts them outside item 5.

Today both lanes sit on the fleet minor, and the pins below hold all of
ci.yml's literal `python-version:` values to it — deliberately stricter than
the spec requires, because nothing here yet needs a wider window and one
number is easier to keep honest than two. If the library ever needs to prove
a broader `requires-python` (3.9-3.13 is the fleet-normal shape), relax
`test_ci_matrix_main_and_singleton_jobs_agree_with_the_image` to read the
SITE jobs only rather than deleting it — the site half is the half this item
is about.

What is deliberately NOT here: no comparison of the RUNNING interpreter to
the fleet minor — the suite legitimately runs on the adjacent window legs
(3.13/3.12), where that assertion would be false by design. Image-vs-served
is the battery's job, against a host.
"""
from __future__ import annotations

import re

from conftest import REPO_ROOT


def _fleet_minor() -> str:
    """The single source: the Dockerfile's FROM tag."""
    for line in (REPO_ROOT / "Dockerfile").read_text(encoding="utf-8").splitlines():
        m = re.match(r"FROM\s+python:(\S+)", line)
        if m:
            return m.group(1)
    raise AssertionError("Dockerfile has no `FROM python:` line")


def _uncommented(path) -> list[str]:
    return [
        ln for ln in (REPO_ROOT / path).read_text(encoding="utf-8").splitlines()
        if not ln.lstrip().startswith("#")
    ]


def test_dockerfile_tag_is_minor_only():
    """The patch pin IS the security bug: `3.11.8-slim` never receives a
    3.11.x fix release. The minor tag tracks them through the registry."""
    tag = _fleet_minor()
    assert re.fullmatch(r"\d+\.\d+-slim", tag), (
        f"Dockerfile FROM tag is {tag!r} — must be a MINOR tag "
        "(python:X.Y-slim), never a patch pin"
    )


def test_render_yaml_declares_no_python_while_the_runtime_is_docker():
    """A docker service takes its interpreter from the image, not from a
    Blueprint variable — so there must be exactly ONE declaration here.

    Render's PYTHON_VERSION configures its NATIVE python runtime. On
    `runtime: docker` it is read by nothing, and a value sitting there would
    read to the next session as the platform's actual setting: a second
    declared Python that no deploy can honour and no check can contradict,
    which is precisely the drift class this file exists for.

    If this service is ever moved to the native runtime, this test fails and
    the fix is to port the template's assertion — PYTHON_VERSION present, a
    full X.Y.Z, minor equal to the image's.
    """
    lines = _uncommented("render.yaml")
    runtime = next(
        (m.group(1) for ln in lines
         if (m := re.match(r"\s*runtime:\s*(\S+)", ln))), None
    )
    assert runtime == "docker", (
        f"render.yaml runtime is {runtime!r}, not 'docker' — this repo's "
        "single-declaration assumption (DIVERGENCES.md 5) no longer holds; "
        "port the template's PYTHON_VERSION agreement pin"
    )
    declared = [ln for ln in lines if re.match(r"\s*- key: PYTHON_VERSION$", ln)]
    assert declared == [], (
        "render.yaml declares PYTHON_VERSION on a `runtime: docker` service "
        "— Render ignores it and the image's FROM tag is what actually "
        "serves, so this is a second declared Python that can never be true"
    )


def test_ci_matrix_main_and_singleton_jobs_agree_with_the_image():
    minor = _fleet_minor().removesuffix("-slim")
    ci = _uncommented(".github/workflows/ci.yml")

    mains = [m.group(1) for ln in ci
             if (m := re.match(r'\s*python:\s*\["([\d.]+)"\]', ln))]
    assert mains == [minor], (
        f"ci.yml matrix main {mains} vs image python:{minor}-slim"
    )

    # lint, docs-tests, package and pip-audit run literal python-version
    # pins; the examples job's is `${{ matrix.python }}` and is deliberately
    # not a literal.
    literals = [m.group(1) for ln in ci
                if (m := re.match(r'\s*python-version:\s*"([\d.]+)"', ln))]
    assert literals and set(literals) == {minor}, (
        f"ci.yml singleton jobs pin {literals}, image is python:{minor}-slim"
    )

    cd = _uncommented(".github/workflows/cd.yml")
    cd_literals = [m.group(1) for ln in cd
                   if (m := re.match(r'\s*python-version:\s*"([\d.]+)"', ln))]
    assert cd_literals and set(cd_literals) == {minor}, (
        f"cd.yml verify job pins {cd_literals}, image is python:{minor}-slim"
    )


def test_matrix_legs_are_the_adjacent_minors():
    """The compat window stays three wide: the include legs are X.Y-1 and
    X.Y-2 (or X.Y+1 once it exists).

    This repo's include entries lead with `- dash:` and carry `python:` as a
    nested scalar, so the selector is a bare `python: "X.Y"` — the matrix
    main is the list form `python: ["X.Y"]` and never matches it.
    """
    major, y = (int(p) for p in _fleet_minor().removesuffix("-slim").split("."))
    allowed = {f"{major}.{y}", f"{major}.{y - 1}", f"{major}.{y - 2}",
               f"{major}.{y + 1}"}
    ci = _uncommented(".github/workflows/ci.yml")
    legs = [m.group(1) for ln in ci
            if (m := re.match(r'\s*python:\s*"([\d.]+)"\s*$', ln))]
    assert legs, "the matrix has no include legs — the window collapsed to one"
    outside = [leg for leg in legs if leg not in allowed]
    assert not outside, (
        f"matrix legs {outside} fall outside the three-wide window around "
        f"{major}.{y}"
    )


def test_healthz_reports_the_serving_interpreter(app_module):
    """The observability half. Without this field the wire cannot contradict
    a stale image, and `python_matches_declared` has nothing to hold."""
    import platform

    body = app_module._health_body()
    assert body.get("python") == platform.python_version(), (
        "/healthz must report the interpreter that is actually serving"
    )
