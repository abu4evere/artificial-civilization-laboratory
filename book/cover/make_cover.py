"""Draw the book cover as SVG (2:3, 1600 x 2400): an archipelago at dusk, campfires on the islands,
one raft between them, and a lone watcher on a cliff who can see the world but not touch it.

    python book/cover/make_cover.py      -> book/cover/cover.svg
Render to PNG with a headless browser (see render_cover.ps1).
"""
import math
import random
from pathlib import Path

W, H = 1600, 2400
HORIZON = 1360
rng = random.Random(7)
out = []
a = out.append

a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
a("""<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#070b18"/>
    <stop offset="0.30" stop-color="#14203d"/>
    <stop offset="0.55" stop-color="#3b3a62"/>
    <stop offset="0.75" stop-color="#8a5a6a"/>
    <stop offset="0.90" stop-color="#d98a5a"/>
    <stop offset="1" stop-color="#f6c27a"/>
  </linearGradient>
  <linearGradient id="sea" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#e3a066"/>
    <stop offset="0.10" stop-color="#9a6670"/>
    <stop offset="0.35" stop-color="#3c3a5c"/>
    <stop offset="1" stop-color="#0c1022"/>
  </linearGradient>
  <radialGradient id="sunglow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#fff2cf" stop-opacity="1"/>
    <stop offset="0.12" stop-color="#ffd690" stop-opacity="0.95"/>
    <stop offset="0.35" stop-color="#f3a35f" stop-opacity="0.45"/>
    <stop offset="1" stop-color="#f3a35f" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="fire" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#fff0b0"/>
    <stop offset="0.3" stop-color="#ffb347" stop-opacity="0.9"/>
    <stop offset="1" stop-color="#ff7a1a" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="vignette" cx="0.5" cy="0.45" r="0.75">
    <stop offset="0.55" stop-color="#000" stop-opacity="0"/>
    <stop offset="1" stop-color="#000" stop-opacity="0.65"/>
  </radialGradient>
  <linearGradient id="topshade" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#03050c" stop-opacity="0.85"/>
    <stop offset="1" stop-color="#03050c" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="rock" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#1c1a26"/>
    <stop offset="1" stop-color="#07080d"/>
  </linearGradient>
  <filter id="blur6"><feGaussianBlur stdDeviation="6"/></filter>
  <filter id="blur20"><feGaussianBlur stdDeviation="20"/></filter>
  <filter id="blur2"><feGaussianBlur stdDeviation="1.6"/></filter>
</defs>""")

# --- sky, stars, sun, clouds -----------------------------------------------------------------------
a(f'<rect width="{W}" height="{HORIZON + 2}" fill="url(#sky)"/>')
for _ in range(260):
    x, y = rng.uniform(0, W), rng.uniform(0, 820) ** 1.0
    r = rng.choice((0.8, 1.0, 1.2, 1.6, 2.2)) if rng.random() < 0.97 else 3.0
    op = max(0.15, 1.0 - y / 900) * rng.uniform(0.5, 1.0)
    a(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fdf6e3" opacity="{op:.2f}"/>')
SUN = (1010, HORIZON - 40)
a(f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="520" fill="url(#sunglow)" opacity="0.55"/>')
a(f'<circle cx="{SUN[0]}" cy="{SUN[1]}" r="190" fill="url(#sunglow)"/>')
a(f'<circle cx="{SUN[0]}" cy="{SUN[1] + 6}" r="52" fill="#fff4d6"/>')
for cx, cy, rx, op in ((420, 1050, 420, 0.5), (1180, 1000, 380, 0.45), (760, 1150, 520, 0.4),
                       (1360, 1175, 300, 0.35), (240, 1205, 260, 0.3)):
    for k in range(7):
        ox = rng.uniform(-rx * 0.8, rx * 0.8)
        w = rx * rng.uniform(0.25, 0.55)
        hgt = rng.uniform(7, 16)
        a(f'<ellipse cx="{cx + ox:.0f}" cy="{cy + rng.uniform(-8, 8):.0f}" rx="{w:.0f}" ry="{hgt:.0f}" fill="#2a2440" opacity="{op * rng.uniform(0.5, 1):.2f}" filter="url(#blur6)"/>')
        a(f'<ellipse cx="{cx + ox + 12:.0f}" cy="{cy + hgt * 0.8:.0f}" rx="{w * 0.8:.0f}" ry="{hgt * 0.35:.0f}" fill="#f2a96a" opacity="{op * 0.6:.2f}" filter="url(#blur6)"/>')

# --- sea --------------------------------------------------------------------------------------------
a(f'<rect y="{HORIZON}" width="{W}" height="{H - HORIZON}" fill="url(#sea)"/>')
# the sun's path on the water
for i in range(90):
    y = HORIZON + 6 + (i ** 1.35) * 2.2
    if y > 2050:
        break
    spread = 30 + (y - HORIZON) * 0.32
    for _ in range(2):
        x = SUN[0] + rng.gauss(0, spread * 0.45)
        w = rng.uniform(20, 90) * (1 + (y - HORIZON) / 500)
        op = max(0.06, 0.85 - (y - HORIZON) / 800) * rng.uniform(0.4, 1)
        a(f'<rect x="{x - w / 2:.0f}" y="{y:.0f}" width="{w:.0f}" height="{1.6 + (y - HORIZON) / 260:.1f}" rx="2" fill="#ffd9a0" opacity="{op:.2f}"/>')
# faint swell lines
for _ in range(140):
    y = rng.uniform(HORIZON + 20, 2200)
    x = rng.uniform(0, W)
    w = rng.uniform(30, 160) * (1 + (y - HORIZON) / 600)
    a(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="1.5" fill="#c9a5b0" opacity="{rng.uniform(0.04, 0.14):.2f}"/>')


def ridge(x0, x1, base, peak, jag, seed, color, op=1.0):
    """A silhouette of land between x0 and x1 standing on y=base, highest near the middle."""
    r = random.Random(seed)
    pts = [(x0, base)]
    n = 40
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        h = peak * math.sin(math.pi * t) ** 0.8 + r.uniform(-jag, jag) * math.sin(math.pi * t)
        pts.append((x, base - max(0, h)))
    pts.append((x1, base))
    d = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in pts) + " Z"
    a(f'<path d="{d}" fill="{color}" opacity="{op}"/>')
    return pts


def ground(pts, x):
    """Height of a ridge outline at x."""
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        if xa <= x <= xb and xb > xa:
            return ya + (yb - ya) * (x - xa) / (xb - xa)
    return pts[0][1]


def trees(x0, x1, land, height, count, seed, color):
    r = random.Random(seed)
    for _ in range(count):
        x = r.uniform(x0, x1)
        base = ground(land, x) + 4
        h = height * r.uniform(0.6, 1.2)
        wdt = h * 0.35
        a(f'<path d="M{x:.0f},{base - h:.0f} L{x + wdt / 2:.0f},{base:.0f} L{x - wdt / 2:.0f},{base:.0f} Z" fill="{color}"/>')


def campfire(x, y, size):
    a(f'<circle cx="{x}" cy="{y}" r="{size * 6}" fill="url(#fire)" opacity="0.55"/>')
    a(f'<circle cx="{x}" cy="{y}" r="{size * 2}" fill="url(#fire)"/>')
    a(f'<circle cx="{x}" cy="{y}" r="{max(1.2, size * 0.6):.1f}" fill="#fff6d0"/>')
    # smoke
    a(f'<path d="M{x},{y - size * 2} C{x + 10},{y - 40 - size * 4} {x - 14},{y - 80 - size * 5} {x + 6},{y - 130 - size * 6}" '
      f'stroke="#c8b6c8" stroke-width="{2 + size * 0.6:.1f}" fill="none" opacity="0.22" filter="url(#blur2)"/>')


def hut(x, y, s, color):
    a(f'<path d="M{x - s},{y} L{x},{y - s * 1.1} L{x + s},{y} Z" fill="{color}"/>')


def person(x, y, s, color):
    a(f'<circle cx="{x}" cy="{y - s * 2.6:.1f}" r="{s * 0.45:.1f}" fill="{color}"/>')
    a(f'<rect x="{x - s * 0.35:.1f}" y="{y - s * 2.2:.1f}" width="{s * 0.7:.1f}" height="{s * 2.2:.1f}" rx="{s * 0.3:.1f}" fill="{color}"/>')


# --- far islands on the horizon (hazy) ---------------------------------------------------------------
ridge(-40, 520, HORIZON + 4, 120, 18, 1, "#5a4560", 0.85)
ridge(1250, 1700, HORIZON + 4, 90, 14, 2, "#5a4560", 0.8)
ridge(560, 760, HORIZON + 3, 34, 6, 3, "#6a4f66", 0.7)
campfire(300, HORIZON - 36, 1.2)
campfire(1420, HORIZON - 24, 1.0)

# --- middle islands with people, huts, fires ----------------------------------------------------------
west = ridge(-80, 700, 1560, 150, 22, 4, "#2a2440")
trees(-40, 430, west, 46, 70, 5, "#1d1a30")
hut(470, 1520, 16, "#1b1828")
hut(520, 1526, 12, "#1b1828")
campfire(500, 1532, 3.4)
for px in (455, 548, 562):
    person(px, 1540, 6.5, "#15131f")

east = ridge(1050, 1700, 1610, 170, 26, 6, "#262038")
trees(1270, 1640, east, 50, 60, 7, "#1a1729")
hut(1150, 1575, 18, "#181524")
campfire(1190, 1586, 3.6)
for px in (1168, 1214, 1230):
    person(px, 1596, 7, "#13111c")

# --- the raft, between the islands ------------------------------------------------------------------
RX, RY = 820, 1640
a(f'<ellipse cx="{RX}" cy="{RY + 6}" rx="70" ry="6" fill="#ffd9a0" opacity="0.18"/>')
a(f'<rect x="{RX - 34}" y="{RY - 4}" width="68" height="8" rx="3" fill="#120f1a"/>')
person(RX + 4, RY - 4, 7.5, "#120f1a")
a(f'<line x1="{RX + 14}" y1="{RY - 26}" x2="{RX + 42}" y2="{RY + 10}" stroke="#120f1a" stroke-width="2.5"/>')
# its wake
for i in range(6):
    a(f'<rect x="{RX - 60 - i * 26}" y="{RY + 4 + i * 1.5:.0f}" width="{30 - i * 3}" height="1.6" fill="#ffd9a0" opacity="{0.35 - i * 0.05:.2f}"/>')

# --- the foreground cliff ----------------------------------------------------------------------------
cliff = [(0, 1900), (120, 1880), (260, 1905), (420, 1890), (600, 1930), (760, 1955), (900, 1948),
         (1000, 1962), (1080, 1950), (1180, 1958), (1290, 1980), (1420, 1972), (1600, 1995),
         (1600, H), (0, H)]
a('<path d="M' + " L".join(f"{x},{y}" for x, y in cliff) + ' Z" fill="url(#rock)"/>')
# lit rim of the cliff edge (the sun is ahead of the watcher)
a('<path d="M' + " L".join(f"{x},{y}" for x, y in cliff[:13]) + '" stroke="#e39a63" stroke-width="3" fill="none" opacity="0.45"/>')
# grass tufts on the edge
for _ in range(120):
    x = rng.uniform(0, W)
    base = 1900 + (x / W) * 95 + rng.uniform(-6, 10)
    h = rng.uniform(10, 34)
    lean = rng.uniform(-8, 8)
    a(f'<path d="M{x:.0f},{base:.0f} q{lean / 2:.0f},{-h / 2:.0f} {lean:.0f},{-h:.0f}" stroke="#0c0d14" stroke-width="2.4" fill="none"/>')

# strata and cracks in the rock, faintly lit
for _ in range(16):
    y0 = rng.uniform(1990, 2380)
    x0 = rng.uniform(-100, 1500)
    pts = [(x0, y0)]
    for _ in range(6):
        pts.append((pts[-1][0] + rng.uniform(40, 120), pts[-1][1] + rng.uniform(-14, 14)))
    a('<path d="M' + " L".join(f"{x:.0f},{y:.0f}" for x, y in pts) + f'" stroke="#3a3346" stroke-width="{rng.uniform(1.5, 3):.1f}" fill="none" opacity="{rng.uniform(0.25, 0.5):.2f}"/>')
# marks scratched into the rock: shapes the people of ACL invent and give meaning to
MARKS = [("<", "o", "^", "v"), ("/", "^", "\\"), ("v", "\\", "v")]
mx, my = 120, 2050
for row, mark in enumerate(MARKS):
    x = mx + row * 36
    y = my + row * 66
    for ch in mark:
        if ch == "o":
            a(f'<circle cx="{x + 14}" cy="{y - 14}" r="13" stroke="#c9b3a6" stroke-width="3.4" stroke-linecap="round" fill="none" opacity="0.42"/>')
        elif ch == "<":
            a(f'<path d="M{x + 26},{y - 30} L{x + 2},{y - 14} L{x + 26},{y + 2}" stroke="#c9b3a6" stroke-width="3.4" stroke-linecap="round" fill="none" opacity="0.42"/>')
        elif ch == "^":
            a(f'<path d="M{x},{y} L{x + 14},{y - 30} L{x + 28},{y}" stroke="#c9b3a6" stroke-width="3.4" stroke-linecap="round" fill="none" opacity="0.42"/>')
        elif ch == "v":
            a(f'<path d="M{x},{y - 30} L{x + 14},{y} L{x + 28},{y - 30}" stroke="#c9b3a6" stroke-width="3.4" stroke-linecap="round" fill="none" opacity="0.42"/>')
        elif ch == "/":
            a(f'<path d="M{x + 2},{y} L{x + 24},{y - 30}" stroke="#c9b3a6" stroke-width="3.4" stroke-linecap="round" fill="none" opacity="0.42"/>')
        elif ch == "\\":
            a(f'<path d="M{x + 2},{y - 30} L{x + 24},{y}" stroke="#c9b3a6" stroke-width="3.4" stroke-linecap="round" fill="none" opacity="0.42"/>')
        x += 40

# --- the watcher, seated on the edge, seen from behind -----------------------------------------------
X, Y = 1180, 1958          # where they sit
FIG = "#07080c"
a(f'<g transform="translate({X},{Y})">')
# hips and folded legs on the rock: knees show either side of the body
a(f'<ellipse cx="-62" cy="-18" rx="34" ry="22" fill="{FIG}"/>')
a(f'<ellipse cx="62" cy="-18" rx="34" ry="22" fill="{FIG}"/>')
a(f'<path d="M-70,2 L70,2 L64,-30 L-64,-30 Z" fill="{FIG}"/>')
# back, widening to the shoulders
a(f'<path d="M-58,-20 C-62,-70 -70,-118 -64,-142 C-58,-160 -36,-168 -14,-170 L14,-170 '
  f'C36,-168 58,-160 64,-142 C70,-118 62,-70 58,-20 Z" fill="{FIG}"/>')
# upper arms falling forward to the knees
a(f'<path d="M-64,-140 C-84,-110 -88,-64 -80,-30 L-62,-28 C-66,-62 -62,-104 -50,-130 Z" fill="{FIG}"/>')
a(f'<path d="M64,-140 C84,-110 88,-64 80,-30 L62,-28 C66,-62 62,-104 50,-130 Z" fill="{FIG}"/>')
# neck and head, tilted a little toward the sun
a(f'<rect x="-11" y="-186" width="22" height="22" rx="6" fill="{FIG}"/>')
a(f'<ellipse cx="-4" cy="-212" rx="25" ry="29" fill="{FIG}" transform="rotate(-8 -4 -212)"/>')
# rim light from the sunset ahead
a('<path d="M-64,-142 C-58,-160 -36,-168 -14,-170" stroke="#f0a96c" stroke-width="2.6" fill="none" opacity="0.6"/>')
a('<path d="M14,-170 C36,-168 58,-160 64,-142" stroke="#f0a96c" stroke-width="2" fill="none" opacity="0.35"/>')
a('<path d="M-28,-218 C-24,-238 -4,-244 12,-236" stroke="#f0a96c" stroke-width="2.2" fill="none" opacity="0.6"/>')
a('</g>')

# --- shading and type --------------------------------------------------------------------------------
a(f'<rect width="{W}" height="{H}" fill="url(#vignette)"/>')
a(f'<rect width="{W}" height="760" fill="url(#topshade)"/>')

SERIF = "'Cormorant Garamond', 'Garamond', 'Georgia', serif"
a(f'<text x="{W / 2}" y="300" text-anchor="middle" font-family="{SERIF}" font-size="132" font-weight="500" '
  f'fill="#f4ead8" letter-spacing="2">The World That</text>')
a(f'<text x="{W / 2}" y="450" text-anchor="middle" font-family="{SERIF}" font-size="132" font-weight="500" '
  f'fill="#f4ead8" letter-spacing="2">Nobody Wrote</text>')
a(f'<rect x="{W / 2 - 60}" y="512" width="120" height="2" fill="#e9b47c" opacity="0.8"/>')
a(f'<text x="{W / 2}" y="590" text-anchor="middle" font-family="{SERIF}" font-size="44" font-style="italic" '
  f'fill="#e8d8c0" opacity="0.92">How we tried to build a civilization</text>')
a(f'<text x="{W / 2}" y="646" text-anchor="middle" font-family="{SERIF}" font-size="44" font-style="italic" '
  f'fill="#e8d8c0" opacity="0.92">instead of simulating one</text>')
a(f'<text x="{W / 2}" y="2310" text-anchor="middle" font-family="{SERIF}" font-size="30" '
  f'fill="#e8d8c0" opacity="0.75" letter-spacing="9">ARTIFICIAL CIVILIZATION LABORATORY</text>')
a("</svg>")

Path(__file__).with_name("cover.svg").write_text("\n".join(out), encoding="utf-8")
print("wrote cover.svg")
