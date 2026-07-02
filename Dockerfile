# syntax=docker/dockerfile:1
# ---------------------------------------------------------------------------
# dash-flows documentation site (run.py) — production image for Render.
#
# The React component bundle (dash_flows/dash_flows.min.js) is committed, so no
# Node/webpack build is needed: this is a pure-Python image that serves the
# pre-built Dash app with gunicorn. node_modules/ is excluded via .dockerignore.
# ---------------------------------------------------------------------------
FROM python:3.12-slim

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

WORKDIR /app

# Install Python deps first so this layer is cached across app-code changes.
COPY requirements-docs.txt ./
RUN pip install --no-cache-dir -r requirements-docs.txt gunicorn

# Copy the application. run.py resolves templates/, dash_flows/, docs/,
# examples/, components/, lib/, pages/ relative to the working directory, so it
# must run from /app (the repo root) — which it does under this WORKDIR.
COPY . .

# Documentation only; the process actually binds to $PORT (below).
EXPOSE 8560

# run:server is the Flask WSGI callable (run.py: `server = app.server`).
# Shell form so ${PORT} / ${WEB_CONCURRENCY} expand when the container starts.
CMD gunicorn run:server --bind "0.0.0.0:${PORT}" --workers "${WEB_CONCURRENCY:-2}" --threads 4 --timeout 120 --access-logfile - --error-logfile -
