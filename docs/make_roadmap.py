"""Draw the ACL roadmap picture from ROADMAP.md's stages: docs/roadmap.svg (for the repository) and
docs/roadmap.png (for the book).

    python docs/make_roadmap.py

To update after an experiment, edit STAGES and BRANCHES below (status: done, now or ahead) and run it again.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent

STAGES = [  # (title, subtitle, status)
    ("0. The world", "N9: search effort unanchored", "now"),
    ("1. Culture appears", "Traditions and stories, E1–E5", "done"),
    ("2. Why it stops", "Bottleneck mapped, E6–E13", "done"),
    ("3. Transmission", "Paused until stage 0 holds", "ahead"),
    ("4. Persistence", "Survives with models gone?", "ahead"),
    ("5. A people's practice", "Preparing becomes a tradition", "ahead"),
    ("6. Scale", "100 people against 30", "ahead"),
    ("7. Accumulation", "Tools build on tools", "ahead"),
    ("8. Society", "Trade, roles, their own rules", "ahead"),
]
BRANCH_FROM = 3                                   # the stage whose outcomes are drawn to the right
BRANCH_LABEL = "E13R outcomes, fixed in advance"
TAKEN = 2                                         # index of the branch E13R took (None before the result)
BRANCHES = [("Safeguard fails", "Fix code, rerun E13R"),
            ("No replication", "Try another route"),
            ("Replicates", "Changed: why food runs out")]

COLORS = {  # fill, stroke, title, subtitle
    "done": ("#E1F5EE", "#0F6E56", "#085041", "#0F6E56"),
    "now": ("#FAECE7", "#993C1D", "#712B13", "#993C1D"),
    "ahead": ("#F1EFE8", "#888780", "#444441", "#5F5E5A"),
    "box": ("#FFFFFF", "#B4B2A9", "#2C2C2A", "#5F5E5A"),
}
LINE = "#888780"
W = 680
X0, BW, BH, STEP, Y0 = 40, 300, 52, 66, 40
BX, BBW = 425, 200
FONT, FONT_BOLD = "C:/Windows/Fonts/GARA.TTF", "C:/Windows/Fonts/GARABD.TTF"


def layout():
    boxes = []
    for i, (t, s, st) in enumerate(STAGES):
        boxes.append(("stage", X0, Y0 + i * STEP, BW, t, s, st))
    cy = Y0 + BRANCH_FROM * STEP + BH // 2
    n = len(BRANCHES)
    ys = [cy + (k - (n - 1) / 2) * 68 for k in range(n)]
    for k, ((t, s), y) in enumerate(zip(BRANCHES, ys)):
        boxes.append(("branch", BX, int(y - BH / 2), BBW, t, s, "now" if k == TAKEN else "box"))
    legend_y = Y0 + len(STAGES) * STEP + 14
    return boxes, cy, [int(y) for y in ys], legend_y, legend_y + 40


def arrow_head(x, y, dx, dy, size=5):
    """Two short strokes forming an open chevron pointing along (dx, dy)."""
    px, py = -dy, dx
    return [((x - dx * size + px * size * 0.7, y - dy * size + py * size * 0.7), (x, y)),
            ((x - dx * size - px * size * 0.7, y - dy * size - py * size * 0.7), (x, y))]


def segments(cy, ys):
    """Connector lines: (start, end, with arrowhead)."""
    out = []
    for i in range(len(STAGES) - 1):
        x = X0 + BW // 2
        out.append(((x, Y0 + i * STEP + BH + 1), (x, Y0 + (i + 1) * STEP - 2), True))
    fork = BX - 40
    out.append(((X0 + BW + 1, cy), (fork, cy), False))
    out.append(((fork, ys[0]), (fork, ys[-1]), False))
    for y in ys:
        out.append(((fork, y), (BX - 2, y), True))
    return out


def svg(boxes, cy, ys, legend_y, H) -> str:
    e = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         'font-family="Garamond, Georgia, serif" role="img">',
         '<title>ACL roadmap</title>', f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>']
    top = min(ys) - BH // 2 - 30
    bottom = max(ys) + BH // 2 + 14
    e.append(f'<rect x="{BX - 20}" y="{top}" width="{BBW + 40}" height="{bottom - top}" rx="4" fill="none" '
             f'stroke="#B4B2A9" stroke-width="0.8" stroke-dasharray="4 3"/>')
    e.append(f'<text x="{BX - 4}" y="{top + 20}" font-size="13" fill="#5F5E5A">{BRANCH_LABEL}</text>')
    for (x1, y1), (x2, y2), head in segments(cy, ys):
        e.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{LINE}" stroke-width="1.2"/>')
        if head:
            dx, dy = (x2 - x1), (y2 - y1)
            n = (dx * dx + dy * dy) ** 0.5
            for (a, b), (c, d) in arrow_head(x2, y2, dx / n, dy / n):
                e.append(f'<line x1="{a:.1f}" y1="{b:.1f}" x2="{c}" y2="{d}" stroke="{LINE}" stroke-width="1.2" '
                         'stroke-linecap="round"/>')
    for _, x, y, w, t, s, st in boxes:
        f, k, tc, sc = COLORS[st]
        sw = 1.4 if st == "now" else 0.8
        e.append(f'<rect x="{x}" y="{y}" width="{w}" height="{BH}" rx="4" fill="{f}" stroke="{k}" stroke-width="{sw}"/>')
        e.append(f'<text x="{x + 16}" y="{y + 22}" font-size="16" font-weight="bold" fill="{tc}">{t}</text>')
        e.append(f'<text x="{x + 16}" y="{y + 41}" font-size="13.5" fill="{sc}">{s}</text>')
    lx = X0
    for label, st in (("Done", "done"), ("Now", "now"), ("Ahead", "ahead")):
        f, k, _, _ = COLORS[st]
        e.append(f'<rect x="{lx}" y="{legend_y}" width="14" height="14" rx="3" fill="{f}" stroke="{k}" stroke-width="0.8"/>')
        e.append(f'<text x="{lx + 22}" y="{legend_y + 12}" font-size="13.5" fill="#5F5E5A">{label}</text>')
        lx += 80
    e.append("</svg>")
    return "\n".join(e)


def png(boxes, cy, ys, legend_y, H, scale=3) -> Image.Image:
    img = Image.new("RGB", (W * scale, H * scale), "#FFFFFF")
    d = ImageDraw.Draw(img)

    def S(v):
        return v * scale

    ft = ImageFont.truetype(FONT_BOLD, S(16))
    fs = ImageFont.truetype(FONT, S(13.5))
    fl = ImageFont.truetype(FONT, S(13))
    top = min(ys) - BH // 2 - 30
    bottom = max(ys) + BH // 2 + 14
    x1, x2 = BX - 20, BX + BBW + 20
    for xa, ya, xb, yb in ((x1, top, x2, top), (x1, bottom, x2, bottom), (x1, top, x1, bottom), (x2, top, x2, bottom)):
        length = max(abs(xb - xa), abs(yb - ya))
        for p in range(0, length, 7):
            q = min(p + 4, length)
            if ya == yb:
                d.line([(S(xa + p), S(ya)), (S(xa + q), S(ya))], fill="#B4B2A9", width=2)
            else:
                d.line([(S(xa), S(ya + p)), (S(xa), S(ya + q))], fill="#B4B2A9", width=2)
    d.text((S(BX - 4), S(top + 20)), BRANCH_LABEL, font=fl, fill="#5F5E5A", anchor="ls")
    for (a, b), (c, e), head in segments(cy, ys):
        d.line([(S(a), S(b)), (S(c), S(e))], fill=LINE, width=4)
        if head:
            dx, dy = (c - a), (e - b)
            n = (dx * dx + dy * dy) ** 0.5
            for (p, q), (r, t) in arrow_head(c, e, dx / n, dy / n):
                d.line([(S(p), S(q)), (S(r), S(t))], fill=LINE, width=4)
    for _, x, y, w, t, s, st in boxes:
        f, k, tc, sc = COLORS[st]
        d.rounded_rectangle([S(x), S(y), S(x + w), S(y + BH)], radius=S(4), fill=f, outline=k,
                            width=5 if st == "now" else 3)
        d.text((S(x + 16), S(y + 22)), t, font=ft, fill=tc, anchor="ls")
        d.text((S(x + 16), S(y + 41)), s, font=fs, fill=sc, anchor="ls")
    lx = X0
    for label, st in (("Done", "done"), ("Now", "now"), ("Ahead", "ahead")):
        f, k, _, _ = COLORS[st]
        d.rounded_rectangle([S(lx), S(legend_y), S(lx + 14), S(legend_y + 14)], radius=S(3), fill=f, outline=k, width=3)
        d.text((S(lx + 22), S(legend_y + 12)), label, font=fs, fill="#5F5E5A", anchor="ls")
        lx += 80
    return img


if __name__ == "__main__":
    boxes, cy, ys, legend_y, H = layout()
    (HERE / "roadmap.svg").write_text(svg(boxes, cy, ys, legend_y, H), encoding="utf-8")
    png(boxes, cy, ys, legend_y, H).save(HERE / "roadmap.png", optimize=True)
    print(f"wrote docs/roadmap.svg and docs/roadmap.png ({W}x{H})")
