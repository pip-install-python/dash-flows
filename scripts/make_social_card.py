#!/usr/bin/env python3
"""Render the 1200x630 social card for a 2plot satellite.

    python scripts/make_social_card.py                    # defaults, this site
    python scripts/make_social_card.py --open             # ...and preview it
    python scripts/make_social_card.py \
        --artwork assets/current_project.png --brand "dash-flows" \
        --tagline "React Flow node graphs for Dash" --domain flows.2plot.dev

NETWORK FILE: copied from dash-documentation-boilerplate 1.2.4, with this
site's artwork, tagline and accent as the defaults. Every card in the network
is framed identically instead of being hand-made once per site and drifting.

Output goes to `build/social-cards/<domain>.png`, which is gitignored. The
card is NOT served by the app — publish it to the CDN:

    https://cdn.2plot.ai/github_assets/<domain>.png

That is deliberate and is the network rule. A card served by the app itself
is fetched by the scraper at unfurl time, and on a cold free-tier container
that request lands mid-wake and times out — the preview renders blank, once,
permanently, because platforms cache the miss. The CDN has no cold start.

WHY 1200x630 and not leaflet's 1280x515
---------------------------------------
1200x630 is exactly 1.91:1, the Open Graph documented ideal, and it degrades
cleanly into Twitter's 2:1 `summary_large_image` slot. leaflet.2plot.dev's is
1280x515 = 2.49:1, which is wider than both and gets cropped on each — and
what sits at that URL today is the 2plot wordmark rather than a per-site card
at all. This is the shape to converge on, not that one.

Pillow is a build-time dependency only. It is deliberately absent from
requirements.txt: nothing at runtime renders images, and a docs site should
not carry an image library into production to support a script run by hand
every few months.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover - the one dependency, named clearly
    sys.exit("This script needs Pillow:\n    pip install Pillow")

# Card geometry. WIDTH/HEIGHT are the contract; everything else is derived so
# a fork can change the padding without recomputing a layout by hand.
WIDTH, HEIGHT = 1200, 630
PAD = 72
ART_BOX = 430          # the square the artwork is fitted inside, right-hand side
RULE_W = 6             # the accent bar under the brand

# Palette. The accent is this site's Mantine primary
# (lib/constants.PRIMARY_COLOR = "blue", shade 6); the backgrounds are the
# Mantine dark body colours the appshell paints, so the card and the site
# cannot disagree.
BG_TOP = (26, 27, 30)        # #1a1b1e — Mantine dark body
BG_BOTTOM = (17, 20, 26)     # a shade deeper, for a gradient with a direction
ACCENT = (34, 139, 230)      # #228be6 — Mantine blue 6, this site's primary
TEXT = (245, 246, 247)
MUTED = (150, 158, 168)

# Font families in preference order. `truetype` is tried on each until one
# loads: macOS ships the first group, Debian/Ubuntu CI images the second.
# There is no bundled font on purpose — shipping a licensed TTF in a template
# every satellite forks is a licensing question nobody wants to answer.
FONT_CANDIDATES = {
    "bold": [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ],
    "regular": [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ],
    "mono": [
        "/System/Library/Fonts/Menlo.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    ],
}


def load_font(kind: str, size: int):
    for path in FONT_CANDIDATES[kind]:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    # Pillow >= 10.1 scales its built-in font; older ones give a 10px bitmap
    # and the card looks broken rather than merely plain. Say so.
    print(f"[card] WARNING: no {kind} system font found — falling back to "
          "Pillow's built-in, which will look wrong. Install DejaVu or "
          "Liberation fonts.", file=sys.stderr)
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # pragma: no cover - Pillow < 10.1
        return ImageFont.load_default()


def vertical_gradient(size, top, bottom):
    """A one-pixel-wide gradient stretched across the canvas.

    Cheaper and smoother than filling row by row on the full-width image, and
    the resample keeps the banding invisible at this height.
    """
    w, h = size
    strip = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(1, h - 1)
        strip.putpixel((0, y), tuple(
            round(top[i] + (bottom[i] - top[i]) * t) for i in range(3)
        ))
    return strip.resize((w, h), Image.BILINEAR)


def wrap(draw, text, font, max_width):
    """Greedy word wrap against measured pixel width, not a character count."""
    words, lines, current = text.split(), [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def build_card(artwork: Path, brand: str, tagline: str, domain: str) -> Image.Image:
    card = vertical_gradient((WIDTH, HEIGHT), BG_TOP, BG_BOTTOM).convert("RGBA")
    draw = ImageDraw.Draw(card)

    # --- artwork, right ----------------------------------------------------
    # `thumbnail` preserves aspect ratio, so a square-ish logo and a wide one
    # both land inside the same box without being stretched. The alpha bbox is
    # cropped first: assets/ddb.png carries ~66px of transparent margin, which
    # would otherwise be centred as if it were part of the image.
    art = Image.open(artwork).convert("RGBA")
    bbox = art.getchannel("A").getbbox()
    if bbox:
        art = art.crop(bbox)
    art.thumbnail((ART_BOX, ART_BOX), Image.LANCZOS)
    art_x = WIDTH - PAD - ART_BOX + (ART_BOX - art.width) // 2
    art_y = (HEIGHT - art.height) // 2
    card.alpha_composite(art, (art_x, art_y))

    # --- text, left --------------------------------------------------------
    text_width = WIDTH - (PAD * 2) - ART_BOX - 48

    brand_font = load_font("bold", 62)
    tagline_font = load_font("regular", 29)
    domain_font = load_font("mono", 25)

    brand_lines = wrap(draw, brand, brand_font, text_width)
    # Shrink once rather than overflow: a three-line brand at 62px collides
    # with the domain strip below.
    if len(brand_lines) > 2:
        brand_font = load_font("bold", 50)
        brand_lines = wrap(draw, brand, brand_font, text_width)

    tagline_lines = wrap(draw, tagline, tagline_font, text_width)[:3]

    brand_lh, tagline_lh = 74, 40
    block_h = (len(brand_lines) * brand_lh) + 26 + (len(tagline_lines) * tagline_lh)
    y = (HEIGHT - block_h - 60) // 2

    # Accent rule, aligned to the top of the brand block.
    draw.rounded_rectangle(
        [PAD, y + 6, PAD + RULE_W, y + block_h - 10], radius=RULE_W // 2, fill=ACCENT
    )
    text_x = PAD + RULE_W + 28

    for line in brand_lines:
        draw.text((text_x, y), line, font=brand_font, fill=TEXT)
        y += brand_lh
    y += 26
    for line in tagline_lines:
        draw.text((text_x, y), line, font=tagline_font, fill=MUTED)
        y += tagline_lh

    # Domain, bottom left — the one string a reader uses to decide whether the
    # link goes where they think it does.
    draw.text((text_x, HEIGHT - PAD - 26), domain, font=domain_font, fill=ACCENT)

    return card.convert("RGB")


def main() -> int:
    from lib.constants import BASE_URL, SITE_BRAND

    default_domain = BASE_URL.split("://", 1)[-1].rstrip("/")

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    # This repo ships no standalone logo, so the README's project screenshot
    # is the artwork — a real flow diagram, which is the most recognisable
    # thing this library produces.
    ap.add_argument("--artwork", default="assets/current_project.png",
                    help="source image, PNG (default: %(default)s)")
    ap.add_argument("--brand", default=SITE_BRAND.split(" — ")[0],
                    help="headline (default: the brand, minus its tagline)")
    ap.add_argument("--tagline",
                    default="Interactive React Flow node graphs for Plotly "
                            "Dash — glass-morphism theme, ELK layouts, full "
                            "callback integration.")
    ap.add_argument("--domain", default=default_domain)
    ap.add_argument("--out", default=None,
                    help="default: build/social-cards/<domain>.png")
    ap.add_argument("--open", action="store_true", help="preview when done (macOS)")
    args = ap.parse_args()

    artwork = (REPO_ROOT / args.artwork) if not Path(args.artwork).is_absolute() \
        else Path(args.artwork)
    if not artwork.exists():
        return print(f"artwork not found: {artwork}", file=sys.stderr) or 1

    out = Path(args.out) if args.out else \
        REPO_ROOT / "build" / "social-cards" / f"{args.domain}.png"
    out.parent.mkdir(parents=True, exist_ok=True)

    card = build_card(artwork, args.brand, args.tagline, args.domain)
    # optimize=True typically halves the file; scrapers fetch this on every
    # cold unfurl and some give up on slow responses.
    card.save(out, "PNG", optimize=True)

    kb = out.stat().st_size // 1024
    print(f"[card] {out.relative_to(REPO_ROOT)}  {card.width}x{card.height}  {kb} KB")
    print(f"[card] ratio {card.width / card.height:.2f}:1")
    print(f"[card] publish to: https://cdn.2plot.ai/github_assets/{args.domain}.png")
    print("[card] then update OG_IMAGE_URL / OG_IMAGE_WIDTH / OG_IMAGE_HEIGHT "
          "in lib/constants.py")

    if args.open and sys.platform == "darwin":
        subprocess.run(["open", str(out)], check=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
