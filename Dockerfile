# syntax=docker/dockerfile:1
# ---------------------------------------------------------------------------
# dash-flows documentation site (run.py) — production image for Render.
#
# The React component bundle (dash_flows/dash_flows.min.js) is committed, so no
# Node/webpack build is needed: this is a pure-Python image that serves the
# pre-built Dash app with gunicorn. node_modules/ is excluded via .dockerignore.
# ---------------------------------------------------------------------------
# MINOR tag on purpose — never a patch pin. A `3.X.Y-slim` FROM never
# receives 3.X security releases; the minor tag tracks them through the
# registry. The minor itself is the ONE fleet Python (3.14, template 1.6.27),
# and because this service is `runtime: docker` this line is the ONLY place
# this repo declares a Python — there is no render.yaml PYTHON_VERSION lane
# to agree with (see DIVERGENCES.md 5). tests/test_python_version.py holds
# this tag, the CI matrix main and the CI/CD singleton pins together;
# /healthz reports the interpreter that actually serves, so the wire can
# contradict a stale image.
#
# The tag itself arrived as dependabot PR #7, merged 2026-08-25 — the image
# half of spec item 5, landed before the rest of the item. Production has
# served 3.14 since build 4a62a9f, which is what proves this dependency set
# builds and boots on it.
FROM python:3.14-slim

# PYTHONUNBUFFERED   -> stream logs straight to stdout (Render shows them live)
# PYTHONDONTWRITEBYTECODE -> no .pyc clutter in the image
# DASH_BACKEND=flask -> WSGI backend served by gunicorn (not fastapi/quart/ASGI)
# PORT               -> local default; Render overrides this at runtime
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DASH_BACKEND=flask \
    PORT=8560

# curl only — the HEALTHCHECK below uses it. Deliberately NO nodejs/npm:
# this repo DOES build JS (src/lib/ -> dash_flows/dash_flows.min.js), but the
# bundle is committed and .dockerignore drops node_modules/, src/ and
# package-lock.json, so the image stays a pure-Python artifact. The toolchain
# is developer-side; shipping it would put a Node dependency tree into
# production for an asset that is already built (DIVERGENCES.md 1).
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# vendor/ holds dash_clerk_auth, which is not on PyPI and which
# requirements-docs.txt installs from a relative path. It MUST be copied
# BEFORE the requirements layer: without it pip reports the missing path as
# a SOFT warning and then dies seconds later on an OSError that reads like a
# registry outage, and a vendor/ that resolves to an empty directory
# installs nothing at all, silently. CI imports dash_clerk_auth inside the
# built image for exactly that reason (emojimart's image died on this).
COPY vendor/ ./vendor/

# Install Python deps first so this layer is cached across app-code changes.
#
# CACHE SEMANTICS (the round-2 fleet lesson, pannellum 2026-08-22): this
# layer re-runs ONLY when vendor/ or requirements-docs.txt bytes change. A
# `>=` floor can NEVER pull a newer release through a cache hit — a
# code-only commit rebuilds the app layers below while pip silently keeps
# whatever version the image was first built with. Ship every dependency
# upgrade as a floor bump in requirements-docs.txt (grep the number — it
# also lives in run.py's boot floor, ci.yml and the tests): the bump IS the
# cache bust, and the boot floor turns a stale image from a silent
# downgrade into a loud refusal to start.
#
# markdown2dash installs with --no-deps ON PURPOSE: 0.1.2 pins
# gunicorn>=21.2.0,<22.0.0, a range vulnerable to CVE-2024-6827 and
# CVE-2024-1135, and unresolvable against the gunicorn>=23 floor in
# requirements-docs.txt. Its real dependencies (mistune, docutils, jsonpath,
# pydantic, frontmatter) are listed there explicitly. CI asserts the gunicorn
# version inside this image so the pin cannot quietly come back.
COPY requirements-docs.txt ./
RUN pip install --no-cache-dir -r requirements-docs.txt \
    && pip install --no-cache-dir --no-deps markdown2dash==0.1.2

# Copy the application. run.py resolves templates/, dash_flows/, docs/,
# examples/, components/, lib/, pages/ relative to the working directory, so it
# must run from /app (the repo root) — which it does under this WORKDIR.
COPY . .

# The 2plot.ai hub's hourly sweep probes /healthz; give the container the same
# check so an unhealthy process is visible to its orchestrator too — and so
# ci.yml can assert Docker's OWN verdict rather than an external curl. Without
# a HEALTHCHECK `docker inspect` reports health `none`: the container is a box
# CI cannot see into, and a broken probe ships silently (emojimart's
# template-class finding, 1.6.19).
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -fsS http://localhost:${PORT:-8560}/healthz || exit 1

# Documentation only; the process actually binds to $PORT (below).
EXPOSE 8560

# run:server is the Flask WSGI callable (run.py: `server = app.server`).
# Shell form so ${PORT} / ${WEB_CONCURRENCY} expand when the container starts.
# The default is at the POINT OF USE, not only in ENV above: `PORT=` set to
# the EMPTY string is a real platform state, and a bare "0.0.0.0:${PORT}"
# then collapses to "0.0.0.0:" and binds nothing the probe can reach.
CMD gunicorn run:server --bind "0.0.0.0:${PORT:-8560}" --workers "${WEB_CONCURRENCY:-2}" --threads 4 --timeout 120 --access-logfile - --error-logfile -
