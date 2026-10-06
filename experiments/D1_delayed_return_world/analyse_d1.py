"""D1 tables (questions.md), written before the D1 data existed. Writes findings_tables.md.

  python experiments/D1_delayed_return_world/analyse_d1.py
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "output"
SEEDS = tuple(range(501, 517))
SEASONS = ("spring", "summer", "autumn", "winter")


def pct(a, b, d=1):
    return f"{100 * a / b:.{d}f}%" if b else "–"


def med(xs, d=2):
    xs = [x for x in xs if x is not None]
    return f"{statistics.median(xs):.{d}f}" if xs else "–"


def main():
    D = {s: json.loads((OUT / f"seed_{s}.json").read_text(encoding="utf-8")) for s in SEEDS}
    L = []
    w = L.append
    w("# D1 — Is delayed return adaptive in ACL's world? Tables\n")
    v = (OUT / "verify.txt").read_text(encoding="utf-8").strip()
    rep = all(r["replay_matches"] for r in D.values())
    w(f"Probe check: {v}. Replays match the saved E13R runs in all 16: **{'yes' if rep else 'NO'}**.\n")

    w("## Part A — the world\n")
    w("### 1 and 3. Density, and how lean winter is (mid-season samples, all worlds and years)\n")
    w("| season | share of all plant food on the richest 10% of land | plant food on land per person |")
    w("|---|---|---|")
    S = [x for s in SEEDS for x in D[s]["samples"]]
    for i, name in enumerate(SEASONS):
        g = [x for x in S if x["season"] == i and x["people"]]
        w(f"| {name} | {med([x['top10'] for x in g], 3)} | {med([x['total'] / x['people'] for x in g], 0)} |")
    w("\n(If plant food were spread perfectly evenly, the richest 10% of land would hold 10%.)")

    w("\n### 2. Predictability\n")
    rs = [r for s in SEEDS for r in D[s]["autumn_r"]]
    w(f"Correlation of each land tile's mid-autumn plant food with the same tile's a year later: median {med(rs, 2)} "
      f"(range {min(rs):.2f}–{max(rs):.2f}; {len(rs):,} year pairs).")
    tot = {}
    for s in SEEDS:
        a = [x["total"] for x in D[s]["samples"] if x["season"] == 2]
        if len(a) > 2:
            m = statistics.mean(a)
            tot[s] = statistics.pstdev(a) / m if m else None
    w(f"\nYear-to-year variation of a world's total mid-autumn plant food (coefficient of variation): median "
      f"{med(list(tot.values()), 3)} (range {min(tot.values()):.3f}–{max(tot.values()):.3f}).")

    w("\n### 4. Storability (from the rules, and from W1)\n")
    w("Weeks until half is gone, with no eating: loose food 17 (4% a week); fired or smoke-kept food 69 (1%); seed 138 "
      "(0.5%). Of what people hold at the start of winter, 69% is already seed (W1). Seed sown outside the growing seasons "
      "loses 3% a week to animals; standing crop loses 5% a week in winter.")

    w("\n## Part B — sowing\n")
    sown = Counter()
    for s in SEEDS:
        for k, v in D[s]["sown_by_season"].items():
            sown[int(k)] += v
    total_sown = sum(sown.values())
    w("### 5. How much is sown, when, by how many\n")
    w(f"Seed sown in 16 worlds × 120 years: {total_sown:,.0f}; by season: " +
      ", ".join(f"{SEASONS[i]} {pct(sown[i], total_sown)}" for i in range(4)) +
      f". Distinct sowers per world: median {med([D[s]['sowers'] for s in SEEDS], 0)}.")
    rec = [r for s in SEEDS for r in D[s]["sowings"]]
    w(f"\nSowing acts followed for a full year: {len(rec):,}; median amount {med([r['amt'] for r in rec], 1)}.")

    w("\n### 6. What it yields, and when\n")
    grown = sum(D[s]["crop_grown"] for s in SEEDS)
    rotted = sum(D[s]["crop_rotted"] for s in SEEDS)
    w(f"Crop grown from sown seed, all worlds: {grown:,.0f}, against {total_sown:,.0f} seed sown: **{grown / total_sown:.2f} "
      f"food per unit of seed**. Crop lost to winter rot: {rotted:,.0f}.")
    w("\n| season sown | sowings | crop grown on the tile within a year, per unit sown (median) | weeks until the first crop (median) |")
    w("|---|---|---|---|")
    for i, name in enumerate(SEASONS):
        g = [r for r in rec if r["season"] == i]
        w(f"| {name} | {len(g):,} | {med([r['crop_52'] / r['amt'] for r in g if r['amt'] > 0], 2)} | "
          f"{med([r['first_crop'] for r in g], 0)} |")
    w("\n(Crop on a tile within a year counts all crop grown there, including from others' sowing on the same tile.)")

    w("\n### 7. Who eats it (crop harvested from tiles sown in the past year; harvests of one unit or more)\n")
    hv = Counter()
    for s in SEEDS:
        hv.update(D[s]["harvest"])
    th = sum(hv.values())
    kin = hv["sower's kin"]
    w(f"Harvested: {th:,.0f}. By the sower {pct(hv['sower'], th)}; by the sower's close kin {pct(kin, th)}; "
      f"by others {pct(hv['others'], th)}.")

    w("\n### 8. Do sowers learn it paid?\n")
    ret = [r for r in rec if r["returned"]]
    w(f"Sowers who came back to the spot 4–52 weeks later: {pct(len(ret), len(rec))}.")
    up = [r for r in rec if r["b52"] is not None and (r["b52"] - (r["b0"] or 0.0)) > 1e-9]
    down = [r for r in rec if r["b52"] is not None and (r["b52"] - (r["b0"] or 0.0)) < -1e-9]
    known = [r for r in rec if r["b52"] is not None]
    w(f"Belief about sowing in that season, a year later against at sowing (sowers still alive): rose {pct(len(up), len(known))}, "
      f"fell {pct(len(down), len(known))}, unchanged {pct(len(known) - len(up) - len(down), len(known))}.")
    for label, g in (("rose", up), ("fell", down)):
        w(f"- Sowed again 13–65 weeks later, when belief {label}: {pct(sum(r['again'] for r in g), len(g))} (n={len(g):,}).")
    w(f"- Sowed again 13–65 weeks later, all sowings: {pct(sum(r['again'] for r in rec), len(rec))}.")

    (HERE / "findings_tables.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
