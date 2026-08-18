#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regenerates assets/og.jpg - the social preview image.

This is NOT part of building the site. The site itself is plain static files
with no build step; this script only exists so the preview image can be rebuilt
when the copy, the numbers or the game artwork change, instead of being
redrawn by hand.

    pip install pillow
    python tools/generate-og.py

Fonts are downloaded once into tools/.fonts/ (git-ignored) from the official
Google Fonts repository. Weights, letter-spacing and line-height below mirror
styles.css, so the image stays typographically identical to the hero section.
"""
import os
import sys
import urllib.request

from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")
FONT_DIR = os.path.join(HERE, ".fonts")
OUT = os.path.join(ASSETS, "og.jpg")

FONT_BASE = "https://raw.githubusercontent.com/google/fonts/main/ofl/barlowcondensed"
WEIGHTS = ("Medium", "SemiBold", "Bold", "ExtraBold")

# --- canvas -----------------------------------------------------------------
W, H = 1200, 631
BG = (11, 12, 12)          # --bg
YEL = (255, 229, 0)        # --yellow
TEXT = (245, 244, 239)     # --text
MUTED = (198, 199, 194)
X, TEXT_W, CARDS_X = 64, 596, 700

# --- copy -------------------------------------------------------------------
WORDMARK = "LEVELAP GAMES"
EYEBROW = "INDEPENDENT GAME STUDIO / PRAGUE"
HEADLINE = [("WE BUILD GAMES FAST.", YEL),
            ("PLAYERS DECIDE", TEXT),
            ("WHAT GROWS.", TEXT)]
INTRO = "Rapid production, real-player testing, disciplined iteration."
PROOF = [("3", "GAMES BUILT", "IN 4 MONTHS"),
         ("1", "SIGNED WEB", "PUBLISHING DEAL"),
         ("1", "GOOGLE PLAY", "RELEASE")]
CARDS = [("bugs-icon.jpg", 226, 3, "BUGS.IO", (CARDS_X, 70)),
         ("silent-strike-icon.jpg", 226, -3, "SILENT STRIKE", (CARDS_X + 234, 54)),
         ("my-backrooms-icon.jpg", 212, -2, "MY BACKROOMS", (CARDS_X + 118, 322))]


def ensure_fonts():
    os.makedirs(FONT_DIR, exist_ok=True)
    for weight in WEIGHTS:
        name = "BarlowCondensed-%s.ttf" % weight
        path = os.path.join(FONT_DIR, name)
        if os.path.exists(path):
            continue
        url = "%s/%s" % (FONT_BASE, name)
        print("downloading %s" % name)
        urllib.request.urlretrieve(url, path)


_cache = {}


def bc(weight, size):
    key = (weight, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(
            os.path.join(FONT_DIR, "BarlowCondensed-%s.ttf" % weight), size)
    return _cache[key]


def text_width(draw, text, font, tracking=0.0):
    """Line width including letter-spacing, expressed in em."""
    if not text:
        return 0
    return (sum(draw.textlength(c, font=font) for c in text)
            + tracking * font.size * (len(text) - 1))


def draw_tracked(draw, xy, text, font, fill, tracking=0.0):
    """Pillow has no letter-spacing, so glyphs are placed one by one."""
    x, y = xy
    for char in text:
        draw.text((x, y), char, font=font, fill=fill)
        x += draw.textlength(char, font=font) + tracking * font.size
    return x


def rounded(img, radius):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, img.size[0] - 1, img.size[1] - 1], radius=radius, fill=255)
    img.putalpha(mask)
    return img


def build_card(filename, size, rotation, label):
    img = Image.open(os.path.join(ASSETS, filename)).convert("RGB")
    side = min(img.size)
    img = img.crop(((img.width - side) // 2, (img.height - side) // 2,
                    (img.width + side) // 2, (img.height + side) // 2))
    img = rounded(img.resize((size, size), Image.LANCZOS).convert("RGBA"),
                  int(size * 0.13))

    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, size - 1, size - 1],
                           radius=int(size * 0.13), outline=(255, 255, 255, 38), width=2)

    font = bc("ExtraBold", 24)                       # .hero-game span: 800
    box_w = text_width(draw, label, font, 0.01) + 22
    box_h = font.getmetrics()[0] + 8
    bx, by = int(size * 0.055), size - box_h - int(size * 0.055)
    draw.rounded_rectangle([bx, by, bx + box_w, by + box_h], radius=7, fill=YEL)
    draw_tracked(draw, (bx + 11, by + 2), label, font, (9, 10, 10), 0.01)

    return img.rotate(rotation, resample=Image.BICUBIC, expand=True)


def paste_with_shadow(base, card, xy):
    shadow = Image.new("RGBA", (card.width + 80, card.height + 80), (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 150), (40, 52), card.split()[3])
    shadow = shadow.filter(ImageFilter.GaussianBlur(20))
    base.alpha_composite(shadow, (xy[0] - 40, xy[1] - 40))
    base.alpha_composite(card, xy)


def main():
    ensure_fonts()

    canvas = Image.new("RGBA", (W, H), BG + (255,))

    # dot texture, mirrors body::before
    dots = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dots)
    for y in range(0, H, 4):
        for x in range(0, W, 4):
            dd.point((x, y), fill=(255, 255, 255, 8))
    canvas = Image.alpha_composite(canvas, dots)

    for filename, size, rotation, label, xy in CARDS:
        paste_with_shadow(canvas, build_card(filename, size, rotation, label), xy)

    draw = ImageDraw.Draw(canvas)

    logo = Image.open(os.path.join(ASSETS, "logo-banana.png")).convert("RGB")
    logo = rounded(logo.resize((44, 44), Image.LANCZOS).convert("RGBA"), 11)
    canvas.alpha_composite(logo, (X, 44))

    draw_tracked(draw, (X + 58, 42), WORDMARK, bc("ExtraBold", 40), YEL, 0.03)
    draw_tracked(draw, (X, 118), EYEBROW, bc("SemiBold", 19), (185, 186, 181), 0.12)

    # h1 is clamp(56px, 6.4vw, 104px); pick the largest size that still clears
    # the artwork on the right instead of hard-coding one.
    size = 104
    while size > 40:
        font = bc("SemiBold", size)
        if max(text_width(draw, t, font, -0.025) for t, _ in HEADLINE) <= TEXT_W:
            break
        size -= 1
    font = bc("SemiBold", size)
    step = int(size * 0.9)                           # line-height: 0.9
    print("headline size: %dpx, line step: %dpx" % (size, step))

    y = 150
    for line, colour in HEADLINE:
        draw_tracked(draw, (X, y), line, font, colour, -0.025)
        y += step
    head_bottom = y + int(size * 0.12)

    draw.text((X, head_bottom + 14), INTRO, font=bc("Medium", 26), fill=(183, 184, 179))
    intro_bottom = head_bottom + 14 + 32

    divider_y = max(intro_bottom + 60, 470)
    draw.line([X, divider_y, 660, divider_y], fill=(255, 255, 255, 40), width=1)

    py, px = divider_y + 20, X
    f_num, f_lbl = bc("Bold", 58), bc("Bold", 19)
    for num, line1, line2 in PROOF:
        draw.text((px, py - 6), num, font=f_num, fill=YEL)
        draw_tracked(draw, (px + 38, py + 4), line1, f_lbl, MUTED, 0.02)
        draw_tracked(draw, (px + 38, py + 26), line2, f_lbl, MUTED, 0.02)
        px += 200

    canvas.convert("RGB").save(OUT, "JPEG", quality=90, optimize=True, progressive=True)
    print("wrote %s (%dx%d, %.0f KB)"
          % (os.path.relpath(OUT, ROOT), W, H, os.path.getsize(OUT) / 1024))
    print("og:image:width / og:image:height in index.html must match %d / %d" % (W, H))


if __name__ == "__main__":
    sys.exit(main())
