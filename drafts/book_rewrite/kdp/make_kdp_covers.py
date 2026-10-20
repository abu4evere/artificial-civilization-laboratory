"""Covers for the Amazon (KDP) edition of Part One, built from the book's own cover (book/cover/cover.svg).

    python drafts/book_rewrite/kdp/make_kdp_covers.py      -> paperback_cover.svg, kindle_cover.svg (this folder)
Render each with book/cover/render_cover.ps1 at the sizes printed below.

Paperback: 6 x 9 in trim, white paper, black-and-white interior; spine = pages x 0.002252 in (KDP's figure for white
paper); 0.125 in bleed on every outer edge; the barcode box on the back (2 x 1.2 in, bottom right) is left empty.
Kindle: 1600 x 2560, the front alone.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parents[2]
PAGES = int(sys.argv[1]) if len(sys.argv) > 1 else 87
DPI = 300
BLEED, TRIM_W, TRIM_H = 0.125, 6.0, 9.0
SPINE = PAGES * 0.002252

src = (ROOT / "book" / "cover" / "cover.svg").read_text(encoding="utf-8")
src = src.replace("How we tried", "How I tried")
inner = src[src.index(">") + 1: src.rindex("</svg>")]          # the cover's drawing without its root element
# "Part One" under the subtitle, in the cover's gold
inner += ('<text x="800" y="690" text-anchor="middle" font-family="Cormorant Garamond, Georgia, serif" '
          'font-size="44" fill="#e2a85c" letter-spacing="14">PART ONE</text>')
FONT = "Cormorant Garamond, Georgia, serif"
INK, SOFT, GOLD = "#f3efe6", "#b7c2d0", "#e2a85c"

BLURB = [
    "Twenty people wake up in a world knowing nothing. No language, no tools, no idea how to survive. "
    "Nobody tells them what to do. All they have is nature: hunger, cold, seasons, plants, water, and each other.",
    "The World That Nobody Wrote is the story of the Artificial Civilization Laboratory, a simulated world "
    "built to ask one question: can a civilization start by itself, from nothing?",
    "In its worlds, people tied a raft in their first weeks and almost never used it. Someone named Reibik made "
    "a vessel that could hold water and never once filled it. Whole worlds ended, not in war but in quiet, "
    "because too few people could find each other.",
    "Part One tells what happened, what was predicted wrong, and the questions it raised: about memory, about "
    "who a person is, and about what it means for a world to have a creator.",
]


def wrap(text, chars):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > chars and cur:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    lines.append(cur)
    return lines


def front(x, y, w, h):
    return (f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 1600 2400" '
            f'preserveAspectRatio="xMidYMid slice">{inner}</svg>')


def paperback():
    px = lambda inch: round(inch * DPI, 1)
    W = 2 * BLEED + 2 * TRIM_W + SPINE
    H = 2 * BLEED + TRIM_H
    back_x0, spine_x0 = 0, BLEED + TRIM_W
    front_x0 = spine_x0 + SPINE
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
         f'viewBox="0 0 {px(W)} {px(H)}" width="{px(W)}" height="{px(H)}">',
         '<defs><linearGradient id="bk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#010d1c"/>'
         '<stop offset="0.6" stop-color="#021428"/><stop offset="1" stop-color="#0c1013"/></linearGradient></defs>',
         f'<rect x="0" y="0" width="{px(front_x0)}" height="{px(H)}" fill="url(#bk)"/>',
         front(px(front_x0), 0, px(W - front_x0), px(H))]
    # back: blurb, inside a 0.5 in margin from the trim
    x = px(BLEED + 0.55)
    y = px(BLEED + 0.9)
    size, lead = 13.5 / 72 * DPI, 13.5 / 72 * DPI * 1.42
    o.append(f'<text x="{px(BLEED + TRIM_W / 2)}" y="{y}" text-anchor="middle" font-family="{FONT}" '
             f'font-size="{px(0.30)}" fill="{INK}">The World That Nobody Wrote</text>')
    y += px(0.42)
    o.append(f'<text x="{px(BLEED + TRIM_W / 2)}" y="{y}" text-anchor="middle" font-family="{FONT}" '
             f'font-size="{px(0.13)}" fill="{GOLD}" letter-spacing="{px(0.035)}">PART ONE</text>')
    y += px(0.55)
    for i, para in enumerate(BLURB):
        for line in wrap(para, 58):
            t = "The World That Nobody Wrote"
            if i == 1 and line.startswith(t):
                line = f'<tspan font-style="italic">{t}</tspan>{line[len(t):]}'
            o.append(f'<text x="{x}" y="{round(y, 1)}" font-family="{FONT}" font-size="{round(size, 1)}" '
                     f'fill="{INK}">{line}</text>')
            y += lead
        y += lead * 0.55
    y += lead * 0.4
    o.append(f'<text x="{x}" y="{round(y, 1)}" font-family="{FONT}" font-size="{round(size * 0.85, 1)}" '
             f'fill="{SOFT}">Every number in the book comes from the project\'s experiment records.</text>')
    o.append(f'<text x="{x}" y="{px(BLEED + TRIM_H - 0.55)}" font-family="{FONT}" font-size="{px(0.11)}" '
             f'fill="{SOFT}" letter-spacing="{px(0.03)}">ABDURASHID KHUDOYBERDIEV</text>')
    o.append(f'<text x="{x}" y="{px(BLEED + TRIM_H - 0.35)}" font-family="{FONT}" font-size="{px(0.08)}" '
             f'fill="{SOFT}" letter-spacing="{px(0.03)}">github.com/abu4evere/simulated-world</text>')
    # spine: title and author, rotated to read top to bottom
    cx, cy = px(spine_x0 + SPINE / 2), px(H / 2)
    o.append(f'<text transform="translate({cx},{cy}) rotate(90)" text-anchor="middle" dominant-baseline="central" '
             f'font-family="{FONT}" font-size="{px(0.095)}" fill="{INK}" letter-spacing="{px(0.012)}">'
             f'THE WORLD THAT NOBODY WROTE  ·  PART ONE  ·  KHUDOYBERDIEV</text>')
    o.append("</svg>")
    (HERE / "paperback_cover.svg").write_text("\n".join(o), encoding="utf-8")
    return round(W * DPI), round(H * DPI), W, H


def kindle():
    o = ['<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
         'viewBox="0 0 1600 2560" width="1600" height="2560">', front(0, 0, 1600, 2560), "</svg>"]
    (HERE / "kindle_cover.svg").write_text("\n".join(o), encoding="utf-8")


if __name__ == "__main__":
    w, h, W, H = paperback()
    kindle()
    print(f"paperback: {PAGES} pages, spine {SPINE:.4f} in, full cover {W:.4f} x {H:.4f} in = {w} x {h} px")
    print("kindle: 1600 x 2560 px")
