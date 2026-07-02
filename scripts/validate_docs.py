#!/usr/bin/env python
"""Parse every docs/**/*.md through the real markdown2dash pipeline.

Uses the exact directive set from pages/markdown.py so it exercises
`.. exec::` (imports + builds each demo's `component`), `.. kwargs::`
(docstring -> prop table), `.. source::`, `.. toc::`, and `.. llms_copy::`.

It does NOT call dash.register_page, so no running Dash app is required —
this catches doc render crashes offline, before `python run.py`.

Usage:
    python scripts/validate_docs.py     (needs requirements-docs.txt installed)
Exit code is non-zero if any page fails to render.
"""
import os
import sys
import traceback
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)

import frontmatter  # noqa: E402
from markdown2dash import (  # noqa: E402
    Admonition,
    BlockExec,
    Divider,
    Image,
    create_parser,
)

from lib.directives.kwargs import Kwargs  # noqa: E402
from lib.directives.llms_copy import LlmsCopy  # noqa: E402
from lib.directives.source import SC  # noqa: E402
from lib.directives.toc import TOC  # noqa: E402


def main():
    directives = [
        Admonition(), BlockExec(), Divider(), Image(),
        Kwargs(), LlmsCopy(), SC(), TOC(),
    ]
    parse = create_parser(directives)

    ok, fail = [], []
    for f in sorted(Path("docs").glob("**/*.md")):
        try:
            _, content = frontmatter.parse(f.read_text())
            parse(content)
            ok.append(str(f))
            print(f"OK   {f}")
        except Exception:
            last = traceback.format_exc().strip().splitlines()[-1]
            fail.append((str(f), last))
            print(f"FAIL {f}: {last}")

    print("\n==== SUMMARY ====")
    print(f"OK:   {len(ok)}/{len(ok) + len(fail)}")
    for f, err in fail:
        print(f"  - {f}: {err}")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
