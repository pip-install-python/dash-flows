#!/usr/bin/env python
"""Import-level smoke test for every app in examples/.

Executes each example's module body (which builds the layout and registers
callbacks) WITHOUT running the server — the `if __name__ == "__main__":`
server block is skipped because the module is imported, not run.

A per-file SIGALRM guard prevents a stray blocking call from hanging the run.

Usage:
    python scripts/smoke_examples.py
Exit code is non-zero if any example fails (suitable for CI).
"""
import glob
import importlib.util
import os
import signal
import sys
import traceback

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)

TIMEOUT_SECONDS = 25


class Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise Timeout("import exceeded time budget")


signal.signal(signal.SIGALRM, _alarm)


def main():
    files = sorted(glob.glob("examples/[0-9]*.py"))
    ok, fail = [], []
    for f in files:
        name = os.path.basename(f)
        try:
            signal.alarm(TIMEOUT_SECONDS)
            spec = importlib.util.spec_from_file_location(
                "ex_" + name.replace(".", "_"), f
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            signal.alarm(0)
            ok.append(name)
            print(f"OK   {name}")
        except Timeout as exc:
            signal.alarm(0)
            fail.append((name, f"Timeout: {exc}"))
            print(f"TIME {name}: {exc}")
        except Exception:
            signal.alarm(0)
            last = traceback.format_exc().strip().splitlines()[-1]
            fail.append((name, last))
            print(f"FAIL {name}: {last}")

    print("\n==== SUMMARY ====")
    print(f"OK:   {len(ok)}/{len(files)}")
    print(f"FAIL: {len(fail)}")
    for name, err in fail:
        print(f"  - {name}: {err}")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
