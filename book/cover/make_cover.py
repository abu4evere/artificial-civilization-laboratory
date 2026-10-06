"""Draw the book cover as SVG (2:3, 1600 x 2400): warm paper, the title above, and a framed daylight scene of an
archipelago (ACL's founders begin on islands): a camp with a fire on the near shore, people around it, a raft on the
water, wooded islands and far hills under a high sun.

    python book/cover/make_cover.py     -> book/cover/cover.svg
Render to PNG with a headless browser (see render_cover.ps1).

(Earlier covers, a dusk scene and a map of world 515, are in the repository's history.)
"""
import math
import random
from pathlib import Path

HERE = Path(__file__).parent
W, H = 1600, 2400
S = 1360                                          # the frame
FX, FY = (W - S) // 2, 690
HZ = FY + 700                                     # horizon
rng = random.Random(11)

PAPER, INK, SOFT, TERRA = "#f3eee3", "#1f2a36", "#6b6f6a", "#c4623c"
out = []
a = out.append


def path(d, fill, op=1.0, extra=""):
    a(f'<path d="{d}" fill="{fill}" fill-opacity="{op}" {extra}/>')


def hill(x0, x1, base, peaks, fill, op=1.0):
    """A ridge from x0 to x1 standing on `base`, through (x, height) peaks, drawn with smooth curves."""
    pts = [(x0, base)] + [(x, base - h) for x, h in peaks] + [(x1, base)]
    d = f"M{pts[0][0]},{pts[0][1]}"
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        mx = (xa + xb) / 2
        d += f" C{mx},{ya} {mx},{yb} {xb},{yb}"
    path(d + " Z", fill, op)


def tree(x, y, h, fill):
    w = h * 0.42
    path(f"M{x},{y - h} L{x + w},{y} L{x - w},{y} Z", fill)
    path(f"M{x},{y - h * 1.35} L{x + w * 0.75},{y - h * 0.45} L{x - w * 0.75},{y - h * 0.45} Z", fill)


def person(x, y, s, fill, sitting=False, arm=0):
    """A simple figure standing (or sitting) with its feet at (x, y), height about 100 * s."""
    if sitting:
        a(f'<circle cx="{x}" cy="{y - 62 * s}" r="{11 * s}" fill="{fill}"/>')
        path(f"M{x - 15 * s},{y} Q{x - 18 * s},{y - 48 * s} {x},{y - 50 * s} Q{x + 18 * s},{y - 48 * s} "
             f"{x + 22 * s},{y} Z", fill)
        return
    a(f'<circle cx="{x}" cy="{y - 88 * s}" r="{11 * s}" fill="{fill}"/>')
    path(f"M{x - 13 * s},{y - 8 * s} Q{x - 16 * s},{y - 70 * s} {x},{y - 74 * s} Q{x + 16 * s},{y - 70 * s} "
         f"{x + 13 * s},{y - 8 * s} Z", fill)
    path(f"M{x - 9 * s},{y - 10 * s} L{x - 7 * s},{y} L{x - 1 * s},{y} L{x - 2 * s},{y - 10 * s} Z", fill)
    path(f"M{x + 9 * s},{y - 10 * s} L{x + 7 * s},{y} L{x + 1 * s},{y} L{x + 2 * s},{y - 10 * s} Z", fill)
    if arm:
        a(f'<line x1="{x + 8 * s}" y1="{y - 60 * s}" x2="{x + 34 * s}" y2="{y - (60 + 22 * arm) * s}" '
          f'stroke="{fill}" stroke-width="{7 * s}" stroke-linecap="round"/>')


a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
a(f"""<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#a9d0e2"/><stop offset="0.6" stop-color="#d8e9ea"/><stop offset="1" stop-color="#f8ecd2"/>
  </linearGradient>
  <linearGradient id="sea" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#a7d0d6"/><stop offset="1" stop-color="#5f9db0"/>
  </linearGradient>
  <linearGradient id="sand" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f0dfb2"/><stop offset="1" stop-color="#e2c690"/>
  </linearGradient>
  <radialGradient id="glow"><stop offset="0" stop-color="#ffe7a3" stop-opacity="0.9"/>
    <stop offset="1" stop-color="#ffe7a3" stop-opacity="0"/></radialGradient>
  <clipPath id="frame"><rect x="{FX}" y="{FY}" width="{S}" height="{S}" rx="18"/></clipPath>
</defs>""")
a(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
a('<g clip-path="url(#frame)">')

# sky, sun, clouds, birds
a(f'<rect x="{FX}" y="{FY}" width="{S}" height="{HZ - FY}" fill="url(#sky)"/>')
sx, sy = FX + 960, FY + 250
a(f'<circle cx="{sx}" cy="{sy}" r="230" fill="url(#glow)"/>')
a(f'<circle cx="{sx}" cy="{sy}" r="88" fill="#fbd98a"/>')
for cx, cy, k in ((FX + 300, FY + 190, 1.0), (FX + 560, FY + 300, 0.7), (FX + 1180, FY + 430, 0.8)):
    for dx, dy, rx, ry in ((0, 0, 110, 34), (70, -22, 80, 36), (-70, -12, 70, 28), (140, 4, 60, 22)):
        a(f'<ellipse cx="{cx + dx * k}" cy="{cy + dy * k}" rx="{rx * k}" ry="{ry * k}" fill="#ffffff" fill-opacity="0.78"/>')
for bx, by, bs in ((FX + 700, FY + 170, 1.0), (FX + 760, FY + 205, 0.8), (FX + 655, FY + 215, 0.7)):
    path(f"M{bx - 18 * bs},{by} Q{bx - 9 * bs},{by - 10 * bs} {bx},{by} Q{bx + 9 * bs},{by - 10 * bs} {bx + 18 * bs},{by}",
         "none", 1, f'stroke="{INK}" stroke-opacity="0.55" stroke-width="3" stroke-linecap="round"')

# far islands on the horizon
hill(FX - 20, FX + 520, HZ, ((FX + 120, 70), (FX + 260, 130), (FX + 400, 60)), "#9db5c2")
hill(FX + 760, FX + 1380, HZ, ((FX + 880, 50), (FX + 1060, 150), (FX + 1220, 90)), "#a9bfca")

# the sea, with glitter under the sun
a(f'<rect x="{FX}" y="{HZ}" width="{S}" height="{FY + S - HZ}" fill="url(#sea)"/>')
for _ in range(70):
    y = HZ + 12 + rng.random() ** 1.7 * 520
    x = sx + rng.gauss(0, 60 + (y - HZ) * 0.35)
    ln = rng.uniform(14, 46) * (1 + (y - HZ) / 400)
    a(f'<line x1="{x - ln / 2:.0f}" y1="{y:.0f}" x2="{x + ln / 2:.0f}" y2="{y:.0f}" stroke="#ffffff" '
      f'stroke-opacity="{rng.uniform(0.35, 0.8):.2f}" stroke-width="3" stroke-linecap="round"/>')

# a wooded island, middle right
hill(FX + 820, FX + 1300, HZ + 120, ((FX + 930, 90), (FX + 1060, 160), (FX + 1190, 100)), "#8fb27a")
path(f"M{FX + 800},{HZ + 120} Q{FX + 1060},{HZ + 150} {FX + 1320},{HZ + 120} Z", "#eedcae")
for i in range(11):
    tx = FX + 900 + i * 32 + rng.uniform(-8, 8)
    base = HZ + 115 - 60 * math.sin(math.pi * (tx - FX - 820) / 480)
    tree(tx, base, rng.uniform(34, 52), "#5e8a5c")

# the raft
rx_, ry_ = FX + 560, HZ + 230
path(f"M{rx_ - 80},{ry_} L{rx_ + 80},{ry_} L{rx_ + 70},{ry_ + 16} L{rx_ - 70},{ry_ + 16} Z", "#a87a4f")
for k in range(-60, 70, 24):
    a(f'<line x1="{rx_ + k}" y1="{ry_}" x2="{rx_ + k - 4}" y2="{ry_ + 16}" stroke="#7d5a3a" stroke-width="2"/>')
person(rx_ - 10, ry_, 0.62, "#3f342d")
a(f'<line x1="{rx_ + 12}" y1="{ry_ - 52}" x2="{rx_ + 60}" y2="{ry_ + 40}" stroke="#3f342d" stroke-width="4" '
  f'stroke-linecap="round"/>')
path(f"M{rx_ - 110},{ry_ + 22} Q{rx_},{ry_ + 34} {rx_ + 110},{ry_ + 22}", "none", 1,
     'stroke="#ffffff" stroke-opacity="0.6" stroke-width="3"')

# the near shore
GY = FY + 1010
path(f"M{FX},{GY + 40} C{FX + 300},{GY - 60} {FX + 700},{GY - 10} {FX + 1000},{GY + 70} "
     f"C{FX + 1180},{GY + 120} {FX + 1300},{GY + 110} {FX + S},{GY + 150} L{FX + S},{FY + S} L{FX},{FY + S} Z",
     "url(#sand)")
path(f"M{FX},{GY + 40} C{FX + 300},{GY - 60} {FX + 700},{GY - 10} {FX + 1000},{GY + 70} "
     f"C{FX + 1180},{GY + 120} {FX + 1300},{GY + 110} {FX + S},{GY + 150}", "none", 1,
     'stroke="#ffffff" stroke-opacity="0.75" stroke-width="5"')
hill(FX - 40, FX + 420, FY + S + 10, ((FX + 60, 330), (FX + 200, 300), (FX + 330, 180)), "#9cbb84")
for tx, h in ((FX + 70, 120), (FX + 150, 95), (FX + 230, 110), (FX + 40, 80)):
    tree(tx, FY + S - 230 + (tx - FX) * 0.35, h, "#557f53")

for _ in range(26):
    gx = FX + rng.uniform(380, 1300)
    gy = FY + rng.uniform(1120, 1340)
    path(f"M{gx},{gy} q-4,-16 -10,-22 M{gx},{gy} q1,-18 2,-26 M{gx},{gy} q5,-14 11,-20", "none", 1,
         'stroke="#b89a5e" stroke-width="3" stroke-linecap="round"')

# the camp: a shelter, a fire, people
cx0, cy0 = FX + 720, FY + 1250
path(f"M{cx0 - 330},{cy0 - 10} L{cx0 - 240},{cy0 - 150} L{cx0 - 140},{cy0 - 10} Z", "#c39a68")
path(f"M{cx0 - 240},{cy0 - 150} L{cx0 - 205},{cy0 - 10} L{cx0 - 140},{cy0 - 10} Z", "#a87f52")
for k in (-1, 1):
    a(f'<line x1="{cx0 - 240}" y1="{cy0 - 150}" x2="{cx0 - 240 + 26 * k}" y2="{cy0 - 182}" stroke="#7d5a3a" '
      f'stroke-width="5" stroke-linecap="round"/>')
a(f'<ellipse cx="{cx0}" cy="{cy0 + 6}" rx="62" ry="14" fill="#7d5a3a" fill-opacity="0.35"/>')
for k in (-1, 1):
    a(f'<line x1="{cx0 - 40}" y1="{cy0 + 4 * k}" x2="{cx0 + 40}" y2="{cy0 - 4 * k}" stroke="#6e4b31" '
      f'stroke-width="9" stroke-linecap="round"/>')
path(f"M{cx0 - 32},{cy0} Q{cx0 - 30},{cy0 - 60} {cx0},{cy0 - 96} Q{cx0 + 28},{cy0 - 56} {cx0 + 32},{cy0} Z", "#e0703f")
path(f"M{cx0 - 17},{cy0} Q{cx0 - 14},{cy0 - 40} {cx0 + 2},{cy0 - 62} Q{cx0 + 16},{cy0 - 34} {cx0 + 17},{cy0} Z",
     "#f4b54b")
for k in range(6):
    oy = cy0 - 120 - k * 48
    ox = cx0 + 6 + k * 14 + 10 * math.sin(k * 1.3)
    a(f'<ellipse cx="{ox:.0f}" cy="{oy}" rx="{18 + k * 7}" ry="{14 + k * 5}" fill="#ffffff" '
      f'fill-opacity="{0.42 - k * 0.06:.2f}"/>')
person(cx0 - 120, cy0 + 30, 1.05, "#3f342d", sitting=True)
person(cx0 + 120, cy0 + 34, 1.0, "#4a3d34", sitting=True)
person(cx0 + 230, cy0 + 70, 1.25, "#3f342d", arm=1)
person(cx0 + 300, cy0 + 72, 0.72, "#4a3d34")
person(cx0 - 30, cy0 + 82, 1.0, "#4a3d34", sitting=True)
a("</g>")

# type (unchanged)
FONT = "Cormorant Garamond, Georgia, serif"
a(f'<text x="{W / 2}" y="300" text-anchor="middle" font-family="{FONT}" font-weight="500" font-size="150" '
  f'fill="{INK}" letter-spacing="2">The World That</text>')
a(f'<text x="{W / 2}" y="455" text-anchor="middle" font-family="{FONT}" font-weight="500" font-size="150" '
  f'fill="{INK}" letter-spacing="2">Nobody Wrote</text>')
a(f'<line x1="{W / 2 - 60}" y1="525" x2="{W / 2 + 60}" y2="525" stroke="{TERRA}" stroke-width="3"/>')
a(f'<text x="{W / 2}" y="598" text-anchor="middle" font-family="{FONT}" font-style="italic" font-size="50" '
  f'fill="{SOFT}">How we tried to build a civilization instead of simulating one</text>')
a(f'<text x="{W / 2}" y="2290" text-anchor="middle" font-family="{FONT}" font-size="36" fill="{INK}" '
  f'letter-spacing="11">ARTIFICIAL CIVILIZATION LABORATORY</text>')
a("</svg>")
(HERE / "cover.svg").write_text("\n".join(out), encoding="utf-8")
print("wrote cover.svg")
