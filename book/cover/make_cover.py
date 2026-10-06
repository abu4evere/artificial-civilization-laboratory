"""Draw the book cover as SVG (2:3, 1600 x 2400): a real ACL world seen from above, on warm paper. The map is world 515
(control code, A2-full) tile by tile; terracotta marks where its people walked over 120 years, darker where more often;
ink dots are the 76 people alive at the end. Nothing on the map is invented.

    python book/cover/record_world.py   -> book/cover/world_515.json  (the world's record)
    python book/cover/make_cover.py     -> book/cover/cover.svg
Render to PNG with a headless browser (see render_cover.ps1).

(The earlier cover, an archipelago at dusk, is in the repository's history.)
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).parent
REC = json.loads((HERE / "world_515.json").read_text(encoding="utf-8"))
W, H = 1600, 2400
N = REC["width"]
CELL = 34
MAP = N * CELL                                   # 1360
X0, Y0 = (W - MAP) // 2, 690
GAP = 3

PAPER, INK, SOFT = "#f3eee3", "#1f2a36", "#6b6f6a"
SEA = "#d6e2e3"
LAND = {"beach": "#eadfbf", "plains": "#d3d8a6", "woods": "#b4c792", "forest": "#93ae80", "hills": "#cdbd94",
        "tundra": "#d2d3c2", "mountain": "#b3aa98", "snow": "#fbfaf5", "river": "#a9c7d1"}
WALK = (196, 98, 60)                             # terracotta

out = []
a = out.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
a(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')

# the map: every tile, with a small gap so the world reads as tiles
steps = REC["steps"]
top = math.log1p(max(steps.values()))
a(f'<rect x="{X0 - 14}" y="{Y0 - 14}" width="{MAP + 28}" height="{MAP + 28}" fill="{SEA}" rx="6"/>')
for y, row in enumerate(REC["tiles"]):
    for x, t in enumerate(row):
        px, py = X0 + x * CELL + GAP / 2, Y0 + y * CELL + GAP / 2
        s = CELL - GAP
        if t["b"] == "sea":
            continue
        a(f'<rect x="{px:.1f}" y="{py:.1f}" width="{s}" height="{s}" rx="3" fill="{LAND.get(t["b"], "#d3d8a6")}"/>')
        n = steps.get(f"{x},{y}", 0)
        if n:
            op = 0.05 + 0.55 * (math.log1p(n) / top) ** 2.6
            a(f'<rect x="{px:.1f}" y="{py:.1f}" width="{s}" height="{s}" rx="3" '
              f'fill="rgb{WALK}" fill-opacity="{op:.3f}"/>')

# the living at the end: ink dots, a few to a tile, set around the tile's centre
here = {}
for x, y in REC["living"]:
    here.setdefault((x, y), 0)
    k = here[(x, y)]
    here[(x, y)] += 1
    ang = k * 2.4
    r = 0 if k == 0 else 6 + 2 * k
    cx = X0 + x * CELL + CELL / 2 + r * math.cos(ang)
    cy = Y0 + y * CELL + CELL / 2 + r * math.sin(ang)
    a(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="7.5" fill="{PAPER}"/>')
    a(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="5" fill="{INK}"/>')

# type
FONT = "Cormorant Garamond, Georgia, serif"
a(f'<text x="{W / 2}" y="300" text-anchor="middle" font-family="{FONT}" font-weight="500" font-size="150" '
  f'fill="{INK}" letter-spacing="2">The World That</text>')
a(f'<text x="{W / 2}" y="455" text-anchor="middle" font-family="{FONT}" font-weight="500" font-size="150" '
  f'fill="{INK}" letter-spacing="2">Nobody Wrote</text>')
a(f'<line x1="{W / 2 - 60}" y1="525" x2="{W / 2 + 60}" y2="525" stroke="rgb{WALK}" stroke-width="3"/>')
a(f'<text x="{W / 2}" y="598" text-anchor="middle" font-family="{FONT}" font-style="italic" font-size="50" '
  f'fill="{SOFT}">How we tried to build a civilization instead of simulating one</text>')
cap = (f'World {REC["seed"]} after {REC["years"]} years  &#183;  {len(REC["living"])} people  &#183;  '
       f'every tile where someone walked')
a(f'<text x="{W / 2}" y="{Y0 + MAP + 78}" text-anchor="middle" font-family="{FONT}" font-style="italic" '
  f'font-size="34" fill="{SOFT}">{cap}</text>')
a(f'<text x="{W / 2}" y="2290" text-anchor="middle" font-family="{FONT}" font-size="36" fill="{INK}" '
  f'letter-spacing="11">ARTIFICIAL CIVILIZATION LABORATORY</text>')
a("</svg>")
(HERE / "cover.svg").write_text("\n".join(out), encoding="utf-8")
print("wrote cover.svg")
