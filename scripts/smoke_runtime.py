#!/usr/bin/env python
"""Runtime smoke test: serve every app in examples/ and confirm it responds.

Goes one level beyond scripts/smoke_examples.py (which only import-executes
the module body): each example's Dash app is exercised through Flask's
in-process test client — the same WSGI app `app.run()` would serve, minus
the socket. That validates the full index render and layout serialization
without needing to bind a port (which sandboxed/CI environments may forbid).

For each examples/NN_*.py, in an isolated subprocess:
  1. import the module (its `if __name__ == "__main__":` block is skipped),
  2. GET /              -> expect HTTP 200 (Dash index page),
  3. GET /_dash-layout  -> expect HTTP 200 + valid JSON (layout serializes),
  4. GET /_dash-dependencies -> expect HTTP 200 + valid JSON (callback map).

Usage:
    python scripts/smoke_runtime.py            # all examples
    python scripts/smoke_runtime.py 07 23      # just these numbers
Exit code is non-zero if any example fails (suitable for CI).
"""
import glob
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

TIMEOUT_SECONDS = 60

RUNNER = """
import importlib.util, json, sys
path = sys.argv[1]
spec = importlib.util.spec_from_file_location("smoke_target", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
client = module.app.server.test_client()
BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
for route in ("/", "/_dash-layout", "/_dash-dependencies"):
    resp = client.get(route, headers={"User-Agent": BROWSER_UA})
    if resp.status_code != 200:
        sys.exit(f"GET {route} -> {resp.status_code}")
    if route != "/":
        json.loads(resp.data)  # must be valid JSON
print("SERVED")
"""


def check_example(path):
    """Return (ok: bool, note: str)."""
    try:
        proc = subprocess.run(
            [sys.executable, "-c", RUNNER, path],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return False, f"timed out after {TIMEOUT_SECONDS}s"

    if proc.returncode != 0 or "SERVED" not in proc.stdout:
        err = (proc.stderr or "").strip().splitlines()
        return False, err[-1] if err else f"exit code {proc.returncode}"
    if "Traceback (most recent call last)" in (proc.stderr or ""):
        return False, "traceback in stderr: " + proc.stderr.strip().splitlines()[-1]
    return True, ""


def main():
    files = sorted(glob.glob("examples/[0-9]*.py"))
    if len(sys.argv) > 1:
        wanted = set(sys.argv[1:])
        files = [f for f in files if os.path.basename(f)[:2] in wanted]

    results = []
    for f in files:
        name = os.path.basename(f)
        ok, note = check_example(f)
        results.append((name, ok, note))
        print(f"{'OK  ' if ok else 'FAIL'} {name}" + (f": {note}" if note else ""))

    fails = [r for r in results if not r[1]]
    print("\n==== SUMMARY ====")
    print(f"OK:   {len(results) - len(fails)}/{len(results)}")
    print(f"FAIL: {len(fails)}")
    for name, _, note in fails:
        print(f"  - {name}: {note}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
