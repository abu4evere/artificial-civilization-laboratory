"""E13R autopsy tables (questions.md), written before the autopsy data existed. Writes findings_tables.md.

  python experiments/E13R_replication/autopsy/analyse_autopsy.py
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "output"
SEEDS = tuple(range(501, 517))
BANDS = ("no carer", "under 5", "5-20", "20-50", "50+")
SEASONS = ("spring", "summer", "autumn", "winter")


def med(xs, d=1):
    xs = [x for x in xs if x is not None]
    return f"{statistics.median(xs):.{d}f}" if xs else "–"


def pct(a, b, d=2):
    return f"{100 * a / b:.{d}f}%" if b else "–"


def main():
    D = {(a, s): json.loads((OUT / f"{a}_seed_{s}.json").read_text(encoding="utf-8")) for a in "ab" for s in SEEDS}
    L = []
    w = L.append
    w("# E13R autopsy: tables\n")
    v = (OUT / "verify.txt").read_text(encoding="utf-8").strip()
    rep = all(r["replay_matches"] for r in D.values())
    w(f"Probe check:\n```\n{v}\n```\nReplays match the saved E13R runs in all 32: **{'yes' if rep else 'NO'}**.\n")

    def agree(f):
        """Seeds where B > A, B < A, for a per-seed value f(record) (None skipped)."""
        up = down = 0
        for s in SEEDS:
            x, y = f(D[("a", s)]), f(D[("b", s)])
            if x is None or y is None:
                continue
            up += y > x
            down += y < x
        return f"B higher in {up}, lower in {down} seeds"

    w("## Part 1: the children\n")
    w("### C1. Starvation by the carer's food at the start of winter\n")
    w("| carer's food | A starved / child-winters | A rate | B starved / child-winters | B rate |")
    w("|---|---|---|---|---|")
    rows = {a: [c for s in SEEDS for c in D[(a, s)]["child_rows"]] for a in "ab"}
    for b in BANDS:
        cells = []
        for a in "ab":
            g = [c for c in rows[a] if c["band"] == b]
            k = sum(c["starved"] for c in g)
            cells += [f"{k} / {len(g)}", pct(k, len(g))]
        w(f"| {b} | " + " | ".join(cells) + " |")
    for a in "ab":
        k = sum(c["starved"] for c in rows[a])
        w(f"\nAll children, {a.upper()}: {k} of {len(rows[a])} ({pct(k, len(rows[a]))}).")

    w("\n### C2. Composition\n")
    w("| measure | A | B | seeds |")
    w("|---|---|---|---|")
    for b in BANDS:
        sh = {a: sum(1 for c in rows[a] if c["band"] == b) / len(rows[a]) for a in "ab"}
        w(f"| share of child-winters with carer {b} | {100 * sh['a']:.1f}% | {100 * sh['b']:.1f}% | "
          + agree(lambda r, b=b: sum(1 for c in r["child_rows"] if c["band"] == b) / len(r["child_rows"]) if r["child_rows"] else None) + " |")
    dpc = {a: [x for s in SEEDS for x in D[(a, s)]["deps_per_carer"]] for a in "ab"}
    w(f"| children per carer (mean) | {statistics.mean(dpc['a']):.2f} | {statistics.mean(dpc['b']):.2f} | "
      + agree(lambda r: statistics.mean(r["deps_per_carer"]) if r["deps_per_carer"] else None) + " |")
    births = {a: sum(D[(a, s)]["births"] for s in SEEDS) for a in "ab"}
    w(f"| births, all worlds | {births['a']} | {births['b']} | " + agree(lambda r: r["births"]) + " |")
    w(f"| child-winters | {len(rows['a'])} | {len(rows['b'])} | " + agree(lambda r: len(r["child_rows"])) + " |")

    w("\n### C3. The children who starved\n")
    w("| | A | B |")
    w("|---|---|---|")
    st = {a: [c for c in rows[a] if c["starved"]] for a in "ab"}
    for label, f in (("carer dead by the end", lambda c: not c["carer_alive"]),
                     ("carer alive, holding under 1 at last sight", lambda c: c["carer_alive"] and (c["carer_food_last"] or 0) < 1),
                     ("carer alive, holding 1+ at last sight", lambda c: c["carer_alive"] and (c["carer_food_last"] or 0) >= 1)):
        w(f"| {label} | " + " | ".join(f"{sum(1 for c in st[a] if f(c))} of {len(st[a])}" for a in "ab") + " |")
    for label, key in (("median age", "age"), ("median dependents of their carer", "deps"), ("median week of winter", "death_week")):
        w(f"| {label} | " + " | ".join(med([c[key] for c in st[a]]) for a in "ab") + " |")

    w("\n### C4. Carers holding 20+ at the start of winter: where the food goes\n")
    w("| | A | B |")
    w("|---|---|---|")
    sr = {a: [r for s in SEEDS for r in D[(a, s)]["stocked_rows"]] for a in "ab"}
    w(f"| carer-winters | {len(sr['a'])} | {len(sr['b'])} |")
    for i, label in ((0, "start"), (1, "week 4"), (2, "week 8"), (3, "week 12")):
        w(f"| median food of those alive, {label} | " + " | ".join(med([r[i] for r in sr[a]]) for a in "ab") + " |")
        if i:
            w(f"| still alive, {label} | " + " | ".join(pct(sum(1 for r in sr[a] if r[i] is not None), len(sr[a]), 1)
                                                      for a in "ab") + " |")
    w("| share giving any food to non-dependents | " + " | ".join(
        pct(sum(1 for r in sr[a] if r[4] > 0), len(sr[a]), 1) for a in "ab") + " |")
    w("| mean food given to non-dependents | " + " | ".join(
        f"{statistics.mean([r[4] for r in sr[a]]):.1f}" if sr[a] else "–" for a in "ab") + " |")

    w("\n## Part 2: the habit\n")
    w("### H1. Adults' share of weeks spent foraging, by season\n")
    w("| season | A | B | B ÷ A | seeds |")
    w("|---|---|---|---|---|")
    for i, name in enumerate(SEASONS):
        sh = {}
        for a in "ab":
            f0 = sum(D[(a, s)]["forage"].get(str(i), [0, 0])[0] for s in SEEDS)
            f1 = sum(D[(a, s)]["forage"].get(str(i), [0, 0])[1] for s in SEEDS)
            sh[a] = f0 / f1 if f1 else None
        w(f"| {name} | {100 * sh['a']:.1f}% | {100 * sh['b']:.1f}% | {sh['b'] / sh['a']:.2f} | "
          + agree(lambda r, i=i: (r["forage"][str(i)][0] / r["forage"][str(i)][1]) if r["forage"].get(str(i), [0, 0])[1] else None) + " |")

    w("\n### H2. Adults' food at the start and end of winter\n")
    w("| | A | B | seeds |")
    w("|---|---|---|---|")
    for key, label in (("entry", "start of winter"), ("exit", "end of winter")):
        x = {a: [v for s in SEEDS for v in D[(a, s)][key]] for a in "ab"}
        w(f"| median, {label} | {statistics.median(x['a']):.1f} | {statistics.median(x['b']):.1f} | "
          + agree(lambda r, key=key: statistics.median(r[key]) if r[key] else None) + " |")
        for t in (20, 80):
            w(f"| holding {t}+, {label} | {pct(sum(v >= t for v in x['a']), len(x['a']), 1)} | "
              f"{pct(sum(v >= t for v in x['b']), len(x['b']), 1)} | "
              + agree(lambda r, key=key, t=t: sum(v >= t for v in r[key]) / len(r[key]) if r[key] else None) + " |")

    w("\n### H3. Adults in winter\n")
    w("| | A | B | seeds |")
    w("|---|---|---|---|")
    sw = {a: [sum(D[(a, s)]["short_winter"][i] for s in SEEDS) for i in (0, 1)] for a in "ab"}
    w(f"| winter-weeks going short | {pct(*sw['a'], 1)} | {pct(*sw['b'], 1)} | "
      + agree(lambda r: r["short_winter"][0] / r["short_winter"][1] if r["short_winter"][1] else None) + " |")
    w(f"| adult starvation deaths in winter | {sum(D[('a', s)]['adult_deaths_winter'] for s in SEEDS)} | "
      f"{sum(D[('b', s)]['adult_deaths_winter'] for s in SEEDS)} | " + agree(lambda r: r["adult_deaths_winter"]) + " |")

    (HERE / "findings_tables.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
