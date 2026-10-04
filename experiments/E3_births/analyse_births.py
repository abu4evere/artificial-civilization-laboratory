"""E3 analysis: where were births lost between E1 and E2? Read-only.

Writes report.md (the decomposition and every hypothesis's numbers) and chart.html
(birth rate against partner encounters, E1 and E2, one point per seed).
"""
from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "output"
WPY = 52


def load(code):
    runs = {}
    for f in sorted(OUT.glob(f"{code}_seed_*.json")):
        r = json.loads(f.read_text(encoding="utf-8"))
        runs[r["seed"]] = r
    return runs


def totals(run):
    t = Counter()
    for row in run["rows"]:
        for k, v in row.items():
            if k not in ("year", "population"):
                t[k] += v
    t["years"] = len(run["rows"])
    return t


def rates(t):
    """Everything as a rate, so worlds of different sizes compare."""
    g = lambda k: t.get(k, 0)  # noqa: E731
    fw, ua, ch = g("fw") or 1, g("ua") or 1, g("choices") or 1
    r = {
        "births per fertile woman-year": WPY * g("birth") / fw,
        "with a partner": g("fw_partner") / fw,
        "partner within 2 tiles (of those with one)": g("fw_together") / max(1, g("fw_partner")),
        "free to conceive (of those together)": g("fw_can_conceive") / max(1, g("fw_together")),
        "conceptions per free week": g("pregnant") / max(1, g("fw_can_conceive")),
        "births per conception": g("birth") / max(1, g("pregnant")),
        "partner on another island (of those with one)": g("fw_apart_water") / max(1, g("fw_partner")),
        "mean distance to partner (tiles)": g("fw_partner_dist") / max(1, g("fw_partner")),
        "blocked: pregnant": g("blocked_pregnant") / max(1, g("fw_together")),
        "blocked: nursing": g("blocked_nursing") / max(1, g("fw_together")),
        "blocked: health under 50": g("blocked_health") / max(1, g("fw_together")),
        "blocked: starving": g("blocked_starving") / max(1, g("fw_together")),
        "unpaired adult-weeks with a possible mate in reach": g("ua_encounter") / ua,
        "possible mates in reach, per unpaired adult-week": g("ua_mates_in_reach") / ua,
        "possible mates on own island, per unpaired adult-week": g("ua_pool_island") / ua,
        "pairs formed per unpaired adult-year": WPY * g("pair") / ua,
        "courting by the unpaired, per unpaired adult-week": g("court_by_unpaired") / ua,
        "fertile women starving": g("fw_starving") / fw,
        "fertile women's mean health": g("fw_health") / fw,
        "fertile women's food on hand (weeks, capped at 10)": g("fw_food_weeks") / fw,
    }
    for k in sorted(t):
        if k.startswith("choice:"):
            r["chose " + k[7:]] = t[k] / ch
        if k.startswith("mind:"):
            r["mind on " + k[5:]] = t[k] / ch
    return r


def pooled(runs):
    t = Counter()
    for r in runs.values():
        t.update(totals(r))
    return t


FACTORS = ["with a partner", "partner within 2 tiles (of those with one)", "free to conceive (of those together)",
           "conceptions per free week"]


def chart(e1, e2):
    seeds = sorted(set(e1) & set(e2))
    pts = []
    for s in seeds:
        for code, runs in (("E1", e1), ("E2", e2)):
            r = rates(totals(runs[s]))
            pts.append((s, code, r["unpaired adult-weeks with a possible mate in reach"],
                        r["births per fertile woman-year"]))
    W, H, L_, R_, T_, B_ = 720, 440, 64, 24, 24, 52
    xmax = max(0.05, max(p[2] for p in pts)) * 1.1
    ymax = max(0.05, max(p[3] for p in pts)) * 1.1

    def X(v):
        return L_ + v / xmax * (W - L_ - R_)

    def Y(v):
        return H - B_ - v / ymax * (H - T_ - B_)
    grid = []
    for i in range(6):
        gx, gy = xmax * i / 5, ymax * i / 5
        grid.append(f'<line x1="{L_}" x2="{W - R_}" y1="{Y(gy):.1f}" y2="{Y(gy):.1f}" class="grid"/>'
                    f'<text x="{L_ - 8}" y="{Y(gy) + 4:.1f}" class="tick" text-anchor="end">{gy:.2f}</text>'
                    f'<text x="{X(gx):.1f}" y="{H - B_ + 18}" class="tick" text-anchor="middle">{100 * gx:.0f}%</text>')
    links, marks = [], []
    for s in seeds:
        a = next(p for p in pts if p[0] == s and p[1] == "E1")
        b = next(p for p in pts if p[0] == s and p[1] == "E2")
        links.append(f'<line x1="{X(a[2]):.1f}" y1="{Y(a[3]):.1f}" x2="{X(b[2]):.1f}" y2="{Y(b[3]):.1f}" class="link"/>')
    placed = []
    for s, code, x, y in pts:
        cls = "e1" if code == "E1" else "e2"
        tip = f"Seed {s}, {code}: {100 * x:.0f}% of unpaired weeks with a possible mate in reach; {y:.2f} births per fertile woman-year"
        marks.append(f'<g class="pt" tabindex="0" data-tip="{tip}"><circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="12" class="hit"/>'
                     f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="5" class="{cls}"/></g>')
        if code == "E2":
            lx, ly = X(x) + 8, Y(y) - 7
            while any(abs(lx - px) < 26 and abs(ly - py) < 12 for px, py in placed):
                ly += 12                       # keep labels from sitting on each other
            placed.append((lx, ly))
            marks.append(f'<text x="{lx:.1f}" y="{ly:.1f}" class="lab">{s}</text>')
    rows = "".join(f"<tr><td>{s}</td><td>{code}</td><td>{100 * x:.0f}%</td><td>{y:.2f}</td></tr>" for s, code, x, y in pts)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Births and Encounters</title>
<style>
.viz-root {{ color-scheme: light; --surface-1:#fcfcfb; --text-primary:#0b0b0b; --text-secondary:#52514e;
  --grid:#e4e3df; --series-1:#2a78d6; --series-2:#eb6834; }}
@media (prefers-color-scheme: dark) {{ :root:where(:not([data-theme="light"])) .viz-root {{ color-scheme: dark;
  --surface-1:#1a1a19; --text-primary:#ffffff; --text-secondary:#c3c2b7; --grid:#383835; --series-1:#3987e5; --series-2:#d95926; }} }}
:root[data-theme="dark"] .viz-root {{ color-scheme: dark; --surface-1:#1a1a19; --text-primary:#ffffff;
  --text-secondary:#c3c2b7; --grid:#383835; --series-1:#3987e5; --series-2:#d95926; }}
body {{ margin:0; background:var(--surface-1); }}
.viz-root {{ background:var(--surface-1); color:var(--text-primary); font:14px/1.45 system-ui, sans-serif;
  max-width:760px; margin:0 auto; padding:20px 16px; }}
h1 {{ font-size:18px; margin:0 0 4px; }} p {{ margin:0 0 12px; color:var(--text-secondary); }}
svg {{ width:100%; height:auto; display:block; }}
.grid {{ stroke:var(--grid); stroke-width:1; }} .tick {{ fill:var(--text-secondary); font-size:11px; }}
.axis {{ fill:var(--text-secondary); font-size:12px; }} .lab {{ fill:var(--text-secondary); font-size:11px; }}
.link {{ stroke:var(--text-secondary); stroke-opacity:.35; stroke-width:2; }}
.e1 {{ fill:var(--series-1); stroke:var(--surface-1); stroke-width:2; }}
.e2 {{ fill:var(--series-2); stroke:var(--surface-1); stroke-width:2; }}
.hit {{ fill:transparent; }} .pt:focus {{ outline:none; }} .pt:focus .e1, .pt:focus .e2, .pt:hover .e1, .pt:hover .e2 {{ r:7; }}
.legend {{ display:flex; gap:18px; margin:4px 0 8px; color:var(--text-primary); font-size:13px; }}
.legend span::before {{ content:""; display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:6px; vertical-align:-1px; }}
.legend .l1::before {{ background:var(--series-1); }} .legend .l2::before {{ background:var(--series-2); }}
#tip {{ position:fixed; pointer-events:none; background:var(--surface-1); color:var(--text-primary); border:1px solid var(--grid);
  border-radius:6px; padding:6px 8px; font-size:12px; max-width:260px; display:none; box-shadow:0 2px 8px rgba(0,0,0,.15); }}
details {{ margin-top:12px; color:var(--text-secondary); }} table {{ border-collapse:collapse; font-size:12px; margin-top:6px; }}
td, th {{ padding:3px 10px; border-bottom:1px solid var(--grid); text-align:left; color:var(--text-primary); }}
</style></head>
<body><div class="viz-root">
<h1>Births per fertile woman-year against partner encounters</h1>
<p>One point per world and experiment; a line joins each world's E1 and E2. Partner encounters: the share of weeks an
unpaired adult had a possible mate within reach. First 100 years of each world.</p>
<div class="legend"><span class="l1">E1 (before the four changes)</span><span class="l2">E2 (after)</span></div>
<svg viewBox="0 0 {W} {H}" role="img" aria-label="Scatter of birth rate against partner encounters for E1 and E2">
{''.join(grid)}
<text x="{(L_ + W - R_) / 2}" y="{H - 10}" class="axis" text-anchor="middle">Unpaired adult-weeks with a possible mate within reach</text>
<text x="16" y="{(T_ + H - B_) / 2}" class="axis" text-anchor="middle" transform="rotate(-90 16 {(T_ + H - B_) / 2})">Births per fertile woman-year</text>
{''.join(links)}{''.join(marks)}
</svg>
<div id="tip" role="tooltip"></div>
<details><summary>Table</summary><table><tr><th>World</th><th>Experiment</th><th>Encounters</th><th>Births per fertile woman-year</th></tr>{rows}</table></details>
</div>
<script>
const tip = document.getElementById("tip");
document.querySelectorAll(".pt").forEach(g => {{
  const show = ev => {{ tip.textContent = g.dataset.tip; tip.style.display = "block";
    const r = g.getBoundingClientRect(); const x = ev && ev.clientX ? ev.clientX : r.left + r.width / 2, y = ev && ev.clientY ? ev.clientY : r.top;
    tip.style.left = Math.min(window.innerWidth - 270, x + 12) + "px"; tip.style.top = (y + 12) + "px"; }};
  g.addEventListener("mousemove", show); g.addEventListener("focus", () => show());
  g.addEventListener("mouseleave", () => tip.style.display = "none"); g.addEventListener("blur", () => tip.style.display = "none");
}});
</script>
</body></html>
"""


def main():
    e1, e2 = load("e1"), load("e2")
    seeds = sorted(set(e1) & set(e2))
    L = ["# E3 — Why births fell in E2 · Results", ""]
    w = L.append
    ok1 = {s: e1[s]["identical"] for s in seeds}
    ok2 = {s: e2[s]["identical"] for s in seeds}
    w(f"Seeds {', '.join(map(str, seeds))}; first 100 years of each. Every re-run matched its saved experiment "
      f"exactly: E1 {sum(1 for v in ok1.values() if v)}/{len(seeds)}, E2 {sum(1 for v in ok2.values() if v)}/{len(seeds)} "
      "(a seed that died before year 100 was checked at the end it reached). Nothing in the world was changed.")
    w("")
    a, b = rates(pooled({s: e1[s] for s in seeds})), rates(pooled({s: e2[s] for s in seeds}))
    w("## The chain from fertile woman to birth (pooled over all seeds)")
    w("")
    w("| step | E1 | E2 | E2 / E1 | share of the drop |")
    w("|---|---|---|---|---|")
    total_log = math.log(b["births per fertile woman-year"] / a["births per fertile woman-year"])
    for f in FACTORS + ["births per conception"]:
        ratio = b[f] / a[f] if a[f] else float("nan")
        share = math.log(ratio) / total_log if total_log and ratio > 0 else float("nan")
        w(f"| {f} | {a[f]:.3f} | {b[f]:.3f} | {ratio:.2f} | {100 * share:.0f}% |")
    w(f"| **births per fertile woman-year** | **{a['births per fertile woman-year']:.3f}** | "
      f"**{b['births per fertile woman-year']:.3f}** | **{b['births per fertile woman-year'] / a['births per fertile woman-year']:.2f}** | 100% |")
    w("")
    w("(The steps multiply to the birth rate. \"Share of the drop\" splits the fall on a log scale; a negative share means "
      "that step rose and offset part of the fall.)")
    w("")
    sections = [
        ("B — Island separation and partner encounters", ["unpaired adult-weeks with a possible mate in reach",
         "possible mates in reach, per unpaired adult-week", "possible mates on own island, per unpaired adult-week",
         "pairs formed per unpaired adult-year", "courting by the unpaired, per unpaired adult-week",
         "partner on another island (of those with one)", "mean distance to partner (tiles)"]),
        ("Thresholds — what stops couples who are together", ["blocked: pregnant", "blocked: nursing",
         "blocked: health under 50", "blocked: starving"]),
        ("D — Food reaching fertile women", ["fertile women starving", "fertile women's mean health",
         "fertile women's food on hand (weeks, capped at 10)"]),
    ]
    for title, keys in sections:
        w(f"## {title}")
        w("")
        w("| measure | E1 | E2 |")
        w("|---|---|---|")
        for k in keys:
            w(f"| {k} | {a.get(k, 0):.3f} | {b.get(k, 0):.3f} |")
        w("")
    w("## A / C — What fertile-age adults chose, and what was on their minds")
    w("")
    w("| share of their weekly choices | E1 | E2 | change |")
    w("|---|---|---|---|")
    keys = sorted({k for k in list(a) + list(b) if k.startswith("chose ")}, key=lambda k: -max(a.get(k, 0), b.get(k, 0)))
    for k in keys:
        w(f"| {k} | {100 * a.get(k, 0):.1f}% | {100 * b.get(k, 0):.1f}% | {100 * (b.get(k, 0) - a.get(k, 0)):+.1f} |")
    w("")
    w("| top thought that week | E1 | E2 | change |")
    w("|---|---|---|---|")
    keys = sorted({k for k in list(a) + list(b) if k.startswith("mind on ")}, key=lambda k: -max(a.get(k, 0), b.get(k, 0)))
    for k in keys:
        w(f"| {k} | {100 * a.get(k, 0):.1f}% | {100 * b.get(k, 0):.1f}% | {100 * (b.get(k, 0) - a.get(k, 0)):+.1f} |")
    w("")
    w("## Per world")
    w("")
    w("| seed | births / fertile woman-yr E1 → E2 | with a partner | partner within 2 tiles | free to conceive | encounters (unpaired weeks with a mate in reach) | mates on own island |")
    w("|---|---|---|---|---|---|---|")
    for s in seeds:
        x, y = rates(totals(e1[s])), rates(totals(e2[s]))
        f = lambda k, pct=True: (f"{100 * x[k]:.0f}% → {100 * y[k]:.0f}%" if pct else f"{x[k]:.2f} → {y[k]:.2f}")  # noqa: E731
        w(f"| {s} | {f('births per fertile woman-year', False)} | {f('with a partner')} | "
          f"{f('partner within 2 tiles (of those with one)')} | {f('free to conceive (of those together)')} | "
          f"{f('unpaired adult-weeks with a possible mate in reach')} | {f('possible mates on own island, per unpaired adult-week', False)} |")
    w("")
    (HERE / "report.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    (HERE / "chart.html").write_text(chart(e1, e2), encoding="utf-8")
    print("wrote report.md and chart.html")


if __name__ == "__main__":
    main()
