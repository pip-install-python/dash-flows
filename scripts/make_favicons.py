#!/usr/bin/env python3
"""Render the favicon set + webmanifest for flows.2plot.dev.

    python scripts/make_favicons.py          # writes assets/favicon/*
    python scripts/make_favicons.py --open   # ...and preview the 512px source

The mark is a three-node flow — input, default, output — in this library's
own type colours (the same ones the MiniMap paints: green=input, blue=default,
purple=output) on the Mantine dark body the glass theme sits on. It is the
smallest honest picture of what dash-flows draws.

Everything is rendered from ONE 1024px master and downscaled, so the sizes
cannot drift from each other. Outputs:

    favicon.ico                16/32/48 multi-size (Dash's {%favicon%} finds it)
    favicon-16x16.png ... favicon-96x96.png
    android-chrome-192x192.png / android-chrome-512x512.png
    apple-touch-icon.png       180x180, opaque (iOS composites no alpha)
    site.webmanifest           name/short_name from lib/constants.py

Pillow is a build-time dependency only, same rule as make_social_card.py.
`tests/test_social_card.py` asserts the manifest describes THIS site and that
every icon it lists resolves; `scripts/network_smoke.py` probes the manifest
on every CI container and every deploy (`installable_as_an_app`).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

try:
    from PIL import Image, ImageDraw
except ImportError:  # pragma: no cover - the one dependency, named clearly
    sys.exit("This script needs Pillow:\n    pip install Pillow")

# Master canvas. Everything below is expressed as fractions of this so the
# geometry survives any future size change.
SIZE = 1024

# The glass theme's surfaces and this library's node-type colours
# (src/lib/styles/glass-theme.css / the MiniMap's type colouring).
BG = (26, 27, 30, 255)          # #1a1b1e — Mantine dark body
BG_EDGE = (17, 20, 26, 255)     # a shade deeper, for the corner falloff
NODE_INPUT = (81, 207, 102)     # #51cf66 — green, source-only
NODE_DEFAULT = (34, 139, 230)   # #228be6 — blue, this site's primary
NODE_OUTPUT = (151, 117, 250)   # #9775fa — purple, target-only
EDGE = (140, 160, 185)          # muted slate — reads on the dark bg
HANDLE = (222, 226, 230)        # near-white handle dots


def rounded_node(draw, box, colour, radius):
    """A node: filled rounded rect with a brighter 'glass' border."""
    draw.rounded_rectangle(box, radius=radius, fill=colour + (235,))
    light = tuple(min(255, c + 45) for c in colour)
    draw.rounded_rectangle(box, radius=radius, outline=light + (255,),
                           width=max(2, SIZE // 100))


def build_master() -> Image.Image:
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background: rounded square, subtly darker toward the bottom-right so it
    # reads as a surface rather than a flat chip.
    corner = int(SIZE * 0.22)
    draw.rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], radius=corner, fill=BG)
    overlay = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    odraw.rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], radius=corner,
                            fill=BG_EDGE)
    mask = Image.new("L", (SIZE, SIZE), 0)
    mdraw = ImageDraw.Draw(mask)
    for y in range(SIZE):
        mdraw.line([(0, y), (SIZE, y)], fill=int(90 * y / SIZE))
    img = Image.composite(overlay, img, mask)
    draw = ImageDraw.Draw(img)

    # The flow: input (top-left) -> default (right) -> output (bottom-left).
    # Node geometry, as fractions of the canvas.
    def box(cx, cy, w, h):
        return [int((cx - w / 2) * SIZE), int((cy - h / 2) * SIZE),
                int((cx + w / 2) * SIZE), int((cy + h / 2) * SIZE)]

    n_in = box(0.315, 0.27, 0.36, 0.20)
    n_def = box(0.685, 0.50, 0.36, 0.20)
    n_out = box(0.315, 0.73, 0.36, 0.20)
    node_r = int(SIZE * 0.055)

    # Edges first, so nodes sit on top. Simple bezier-ish elbows drawn as
    # thick arcs: right side of input -> top of default, bottom of default ->
    # right side of output.
    ew = max(6, int(SIZE * 0.028))

    def edge(p0, p1, p2, steps=400):
        # Stamped circles along the quadratic, not a segmented polyline —
        # PIL's joint rendering leaves a furry stroke at this width.
        r = ew / 2
        for i in range(steps + 1):
            t = i / steps
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
            draw.ellipse([x - r, y - r, x + r, y + r], fill=EDGE + (255,))

    a_out = (n_in[2], (n_in[1] + n_in[3]) / 2)          # right of input
    b_in = ((n_def[0] + n_def[2]) / 2, n_def[1])        # top of default
    edge(a_out, (b_in[0], a_out[1]), b_in)

    b_out = ((n_def[0] + n_def[2]) / 2, n_def[3])       # bottom of default
    c_in = (n_out[2], (n_out[1] + n_out[3]) / 2)        # right of output
    edge(b_out, (b_out[0], c_in[1]), c_in)

    rounded_node(draw, n_in, NODE_INPUT, node_r)
    rounded_node(draw, n_def, NODE_DEFAULT, node_r)
    rounded_node(draw, n_out, NODE_OUTPUT, node_r)

    # Handle dots where the edges meet the nodes — the detail that says
    # "React Flow" rather than "three rectangles".
    hr = int(SIZE * 0.026)
    for cx, cy in (a_out, b_in, b_out, c_in):
        draw.ellipse([cx - hr, cy - hr, cx + hr, cy + hr],
                     fill=HANDLE + (255,))

    return img


def main() -> int:
    from lib.constants import SITE_BRAND, SITE_DESCRIPTION, SITE_SHORT_NAME

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--open", action="store_true", help="preview (macOS)")
    args = ap.parse_args()

    out_dir = REPO_ROOT / "assets" / "favicon"
    out_dir.mkdir(parents=True, exist_ok=True)

    master = build_master()

    def scaled(px):
        return master.resize((px, px), Image.LANCZOS)

    pngs = {
        "favicon-16x16.png": 16,
        "favicon-32x32.png": 32,
        "favicon-96x96.png": 96,
        "android-chrome-192x192.png": 192,
        "android-chrome-512x512.png": 512,
    }
    for name, px in pngs.items():
        scaled(px).save(out_dir / name, "PNG", optimize=True)

    # iOS renders no alpha — composite onto the background colour.
    touch = Image.new("RGB", (180, 180), BG[:3])
    touch.paste(scaled(180), (0, 0), scaled(180))
    touch.save(out_dir / "apple-touch-icon.png", "PNG", optimize=True)

    # Multi-size .ico; Dash's {%favicon%} walks assets/ and links it.
    scaled(48).save(out_dir / "favicon.ico", "ICO",
                    sizes=[(16, 16), (32, 32), (48, 48)])

    manifest = {
        "name": SITE_BRAND,
        "short_name": SITE_SHORT_NAME,
        "description": SITE_DESCRIPTION,
        "start_url": "/",
        "icons": [
            {"src": "/assets/favicon/android-chrome-192x192.png",
             "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/favicon/android-chrome-512x512.png",
             "sizes": "512x512", "type": "image/png"},
        ],
        # The manifest carries ONE theme colour; it is the dark surface, same
        # as background_color, which is what the install splash paints. The
        # template's two media-scoped theme-colours cover the browser chrome.
        "theme_color": "#1a1b1e",
        "background_color": "#1a1b1e",
        "display": "standalone",
    }
    (out_dir / "site.webmanifest").write_text(
        json.dumps(manifest, indent=2) + "\n")

    for f in sorted(out_dir.iterdir()):
        print(f"[favicon] {f.relative_to(REPO_ROOT)}  {f.stat().st_size} B")

    if args.open and sys.platform == "darwin":
        subprocess.run(["open", str(out_dir / "android-chrome-512x512.png")],
                       check=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
