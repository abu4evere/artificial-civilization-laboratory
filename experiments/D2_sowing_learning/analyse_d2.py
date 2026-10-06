"""D2 tables (questions.md), written before the D2 data existed. Writes findings_tables.md.

  python experiments/D2_sowing_learning/analyse_d2.py
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "output"
SEEDS = tuple(range(501, 517))
SEASONS = ("spring", "summer", "autumn", "winter")
SOURCES = ("look at this spot", "look at another spot", "other surprise", "fading")


def pct(a, b, d=1):
    return f"{100 * a / b:.{d}f}%" if b else "–"


def med(xs, d=2):
    xs = [x for x in xs if x is not None]
    return f"{statistics.median(xs):.{d}f}" if xs else "–"


def main():
    D = {s: json.loads((OUT / f"seed_{s}.json").read_text(encoding="utf-8")) for s in SEEDS}
    L = []
    w = L.append
    w("# D2 — Why do sowers learn failure? Tables\n")
    v = (OUT / "verify.txt").read_text(encoding="utf-8").strip()
    rep = all(r["replay_matches"] for r in D.values())
    w(f"Exactness: {v}. Replays match the saved E13R runs in all 16: **{'yes' if rep else 'NO'}**.\n")
    R = [r for s in SEEDS for r in D[s]["records"]]
    LK = [x for s in SEEDS for x in D[s]["looks"]]

    w("## Q1. Capture: what did the sower's family get back? (sowings followed a full year)\n")
    sown = sum(r["amt"] for r in R)
    tot = {k: sum(r[k] for r in R) for k in ("grown", "h_self", "h_kin", "h_others")}
    w(f"Sowings: {len(R):,}; seed sown {sown:,.0f}. Crop grown on the sown spots within a year: {tot['grown']:,.0f} "
      f"({tot['grown'] / sown:.2f} per unit of seed; counts all crop on the spot, including from others' sowing).")
    w(f"\nHarvested from those spots within the year (harvests of one unit or more): by the sower {tot['h_self']:,.0f}, by the "
      f"sower's close kin {tot['h_kin']:,.0f}, by others {tot['h_others']:,.0f}.")
    fam = [(r["h_self"] + r["h_kin"]) / r["amt"] for r in R if r["amt"] > 0]
    w(f"\n**Per unit of seed, the sower's family got back: pooled {(tot['h_self'] + tot['h_kin']) / sown:.2f}; median sowing "
      f"{med(fam)}.** Share of sowings where the family got back more than the seed: {pct(sum(1 for x in fam if x > 1), len(fam))}.")
    w("\n| season sown | sowings | family's return per unit of seed (pooled) | others' harvest per unit of seed (pooled) |")
    w("|---|---|---|---|")
    for i, name in enumerate(SEASONS):
        g = [r for r in R if r["season"] == i]
        sg = sum(r["amt"] for r in g)
        w(f"| {name} | {len(g):,} | {sum(r['h_self'] + r['h_kin'] for r in g) / sg:.2f} | {sum(r['h_others'] for r in g) / sg:.2f} |"
          if sg else f"| {name} | 0 | – | – |")

    w("\n## Q2. Where does a sower's change of belief come from? (the year after sowing)\n")
    tot_src = defaultdict(float)
    for r in R:
        for k, val in r["src"].items():
            tot_src[k] += val
    w("| source | total change in belief, all sowings | share of sowings with any change from it |")
    w("|---|---|---|")
    for k in SOURCES:
        w(f"| {k} | {tot_src[k]:+,.1f} | {pct(sum(1 for r in R if abs(r['src'].get(k, 0)) > 1e-12), len(R))} |")
    net = [sum(r["src"].values()) for r in R]
    w(f"\nNet change summed over all sowings: {sum(net):+,.1f}. Without fading: "
      f"{sum(net) - tot_src['fading']:+,.1f}.")
    known = [r for r in R if r["b52"] is not None]
    fell = [r for r in known if r["b52"] - (r["b0"] or 0) < -1e-9]
    fell_fade_only = [r for r in fell if all(abs(val) < 1e-12 for k, val in r["src"].items() if k != "fading")]
    w(f"\nOf sowings where the sower's belief was lower a year later (D1's 'fell'): {len(fell):,} of {len(known):,}; "
      f"in {pct(len(fell_fade_only), len(fell))} of them the only change was fading.")

    w("\n## Q3. What do the looks at one's own sown spot see?\n")
    w(f"Looks at a spot the looker sowed: {len(LK):,}. Credit positive {pct(sum(1 for x in LK if x['change'] > 0), len(LK))}, "
      f"negative {pct(sum(1 for x in LK if x['change'] < 0), len(LK))}, none (difference under 0.1) "
      f"{pct(sum(1 for x in LK if x['change'] == 0), len(LK))}. Weeks since sowing: median {med([x['weeks'] for x in LK], 0)}.")
    w("\n| at the look | looks | credit positive | credit negative |")
    w("|---|---|---|---|")
    cats = {
        "no crop grown yet": lambda x: x["grown"] < 0.5,
        "crop grown, and some harvested by others": lambda x: x["grown"] >= 0.5 and x["harvest_others"] > 0,
        "crop grown, none harvested by others": lambda x: x["grown"] >= 0.5 and x["harvest_others"] == 0,
    }
    for label, f in cats.items():
        g = [x for x in LK if f(x)]
        w(f"| {label} | {len(g):,} | {pct(sum(1 for x in g if x['change'] > 0), len(g))} | {pct(sum(1 for x in g if x['change'] < 0), len(g))} |")
    neg = [x for x in LK if x["change"] < 0 and x["spot_then"]]
    if neg:
        spot_fell = sum(1 for x in neg if (x["spot_now"][0] + x["spot_now"][1]) < (x["spot_then"][0] + x["spot_then"][1]))
        nb_rose = sum(1 for x in neg if x["spot_now"][2] > x["spot_then"][2])
        w(f"\nIn negative looks: the spot's own food (plants and crop) had fallen in {pct(spot_fell, len(neg))}; its neighbours' "
          f"had risen in {pct(nb_rose, len(neg))}.")
    by_s = defaultdict(list)
    for x in LK:
        by_s[x["season"]].append(x)
    w("\n| season sown | looks | positive | negative |")
    w("|---|---|---|---|")
    for i, name in enumerate(SEASONS):
        g = by_s.get(i, [])
        w(f"| {name} | {len(g):,} | {pct(sum(1 for x in g if x['change'] > 0), len(g))} | {pct(sum(1 for x in g if x['change'] < 0), len(g))} |")

    w("\n## Q4. Are the lessons right?\n")
    grown = [x for x in LK if x["grown"] >= 0.5]
    none = [x for x in LK if x["grown"] < 0.5]
    w(f"When crop had grown on the spot since sowing: credit positive {pct(sum(1 for x in grown if x['change'] > 0), len(grown))}, "
      f"negative {pct(sum(1 for x in grown if x['change'] < 0), len(grown))} (n={len(grown):,}).")
    w(f"When no crop had grown yet: positive {pct(sum(1 for x in none if x['change'] > 0), len(none))}, negative "
      f"{pct(sum(1 for x in none if x['change'] < 0), len(none))} (n={len(none):,}).")

    w("\n## Q5. Where are spots sown?\n")
    cs = [x["contrast_at_sowing"] for x in LK if x["contrast_at_sowing"] is not None]
    w(f"How much the spot stood out when sown (its food against its neighbours', with 5 added below): median {med(cs)}; "
      f"above 1 (richer than its surroundings) in {pct(sum(1 for c in cs if c > 1), len(cs))}. Looks where the spot was "
      f"richer than its surroundings at sowing: credit negative "
      f"{pct(sum(1 for x in LK if (x['contrast_at_sowing'] or 0) > 1 and x['change'] < 0), sum(1 for x in LK if (x['contrast_at_sowing'] or 0) > 1))}; "
      f"poorer: negative {pct(sum(1 for x in LK if (x['contrast_at_sowing'] or 9) <= 1 and x['change'] < 0), sum(1 for x in LK if (x['contrast_at_sowing'] or 9) <= 1))}.")
    o = [sum(D[s]["other_looks"][i] for s in SEEDS) for i in range(3)]
    w(f"\nLooks by people at seed spots they did not sow (seen sown, or turned earth): {o[0]:,}; positive {pct(o[1], o[0])}, "
      f"negative {pct(o[2], o[0])}.")

    (HERE / "findings_tables.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
