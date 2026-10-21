"""TU1 analysis (questions.md, frozen as `TU1-frozen`): routes to first tool use, spread and persistence; described.

  python experiments/TU1_tool_use_spread/analyse_tu1.py     -> results.md (outcomes shown only if every check passes)
"""
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_tu1 import ARMS, OUT, ROUTES, SEEDS  # noqa: E402

rows, missing = {}, []
for a in ARMS:
    for s in SEEDS:
        f = OUT / f"{a}_seed_{s}.json"
        if f.exists():
            rows[(a, s)] = json.loads(f.read_text(encoding="utf-8"))
        else:
            missing.append(f.name)
z = OUT / "zero.txt"
zt = z.exists() and "All: PASS" in z.read_text(encoding="utf-8")
rs = list(rows.values())
repro = bool(rs) and all(r.get("reproduces") is True for r in rs)
fps = {r["code_hash"] for r in rs} | {r["code_hash_after"] for r in rs}
L = ["# TU1 — how tool use is learned, and whether it spreads: results", "",
     "Frozen as `TU1-frozen`. run_tu1.py, analyse_tu1.py. Described, no tests.", "", "## Validity", "",
     f"- Zero check (observer changes nothing): **{'yes' if zt else 'NO'}**",
     f"- All 512 worlds present: **{'yes' if not missing else 'NO, missing ' + str(len(missing))}**",
     f"- Every replay equals FX3's saved world: **{'yes' if repro else 'NO'}** "
     f"({sum(r.get('reproduces') is True for r in rs)} of {len(rs)})",
     f"- One code fingerprint (`code_fx2`): **{'yes' if len(fps) == 1 else 'NO'}**", ""]
ok = zt and not missing and repro and len(fps) == 1
if not ok:
    L.append("**Not valid: no outcome is shown.**")
else:
    L += ["**Valid.**", "", "## Q1: how people came to their first tool use", "",
          "| arm | first users | " + " | ".join(ROUTES) + " | main route |", "|" + "---|" * (len(ROUTES) + 3)]
    mains = {}
    for a in ARMS:
        rr = [r for (x, _), r in rows.items() if x == a]
        c = Counter()
        for r in rr:
            c.update(r["routes"])
        n = sum(c.values())
        top = max(ROUTES, key=lambda k: c[k])
        mains[a] = top
        L.append(f"| {a} | {n} | " + " | ".join(f"{c[k] / n:.1%}" if n else "–" for k in ROUTES) + f" | {top} |")
    same = len(set(mains.values())) == 1
    L += ["", f"**Main route: {mains[list(ARMS)[0]] + ' (the same in both arms; stands)' if same else 'no reading (arms disagree)'}**", "",
          "## Q2: did it spread? (at each person's first use, anyone within sight using a tool on embedded food in the 13 weeks before)", "",
          "| arm | nobody nearby | someone nearby | of whom kin |", "|---|---|---|---|"]
    for a in ARMS:
        c = Counter()
        for (x, _), r in rows.items():
            if x == a:
                c.update(r["seen_before"])
        n = c["nobody"] + c["someone"]
        L.append(f"| {a} | {c['nobody'] / n:.1%} | {c['someone'] / n:.1%} | {c['kin'] / c['someone']:.1%} |" if n and c["someone"] else f"| {a} | – | – | – |")
    L += ["", "Share of adults who had ever used a tool on embedded food, by decade (median over worlds alive then):", "",
          "| arm | " + " | ".join(f"year {10 * d + 10}" for d in range(12)) + " |", "|" + "---|" * 13]
    for a in ARMS:
        cells = []
        for d in range(12):
            v = [r["decade_users"].get(str(d)) for (x, _), r in rows.items() if x == a]
            v = [x for x in v if x is not None]
            cells.append(f"{statistics.median(v):.0%}" if v else "–")
        L.append(f"| {a} | " + " | ".join(cells) + " |")
    L += ["", "## Q3: did it last?", "", "| arm | users | median weeks with a tool use | median weeks from first to last use |",
          "|---|---|---|---|"]
    for a in ARMS:
        u = [x for (y, _), r in rows.items() if y == a for x in r["uses_per_user"]]
        sp = [x for (y, _), r in rows.items() if y == a for x in r["spans"]]
        L.append(f"| {a} | {len(u)} | {statistics.median(u):.0f} | {statistics.median(sp):.0f} |" if u else f"| {a} | 0 | – | – |")
text = "\n".join(L) + "\n"
(HERE / "results.md").write_text(text, encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
print(text)
