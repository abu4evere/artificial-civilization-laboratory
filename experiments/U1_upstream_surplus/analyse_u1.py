"""U1 tables (questions.md), written before the U1 data existed. Writes findings_tables.md.

  python experiments/U1_upstream_surplus/analyse_u1.py
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
FOOD_BANDS = ("under 0.5", "0.5-1", "1-2", "2-4", "4+")


def pct(a, b, d=1):
    return f"{100 * a / b:.{d}f}%" if b else "–"


def main():
    D = {s: json.loads((OUT / f"seed_{s}.json").read_text(encoding="utf-8")) for s in SEEDS}
    L = []
    w = L.append
    w("# U1 — Why is there no surplus to store: tables\n")
    v = (OUT / "verify.txt").read_text(encoding="utf-8").strip()
    rep = all(r["replay_matches"] for r in D.values())
    w(f"Probe check: {v}. Replays match the saved E13R runs in all 16: **{'yes' if rep else 'NO'}**.\n")

    def N(s, k):
        return sum(D[x]["n"].get(str(s), {}).get(k, 0.0) for x in SEEDS)

    w("## Q1. How much food is there, and how much is gathered? (autumn)\n")
    for when in ("start", "end"):
        vals = [l["food_per_adult"] for x in SEEDS for l in D[x]["land"] if l["when"] == when]
        w(f"- Plant food on land within reach of adults, per adult, at the {when} of autumn: median {statistics.median(vals):.0f} "
          f"(middle half {sorted(vals)[len(vals) // 4]:.0f}–{sorted(vals)[3 * len(vals) // 4]:.0f}).")
    rows = [r for x in SEEDS for r in D[x]["autumn_rows"]]
    w(f"- Food gathered by foraging in autumn, per adult: median {statistics.median([r[0] for r in rows]):.0f} "
      f"(adult-autumns: {len(rows):,}).")

    w("\n## Q2. How do people spend each season? (adults' chosen actions)\n")
    acts = {s: sum((Counter(D[x]["actions"].get(str(s), {})) for x in SEEDS), Counter()) for s in range(4)}
    top = [a for a, _ in sum(acts.values(), Counter()).most_common(10)]
    w("| action | " + " | ".join(SEASONS) + " |")
    w("|---|---|---|---|---|")
    for a in top:
        w(f"| {a} | " + " | ".join(pct(acts[s][a], sum(acts[s].values())) for s in range(4)) + " |")

    w("\n## Q3. Do they reach the carrying limit? (autumn)\n")
    w(f"Adult autumn-weeks holding 90% or more of what they can carry: {pct(N(2, 'near_cap'), N(2, 'weeks'), 2)}.")

    w("\n## Q4. Do they move too much, and is the land near them stripped?\n")
    w("| season | tiles moved per adult-week | forage weeks | food per forage week | most the formula allows | gathered ÷ allowed |")
    w("|---|---|---|---|---|---|")
    for s in range(4):
        fw = N(s, "forage_weeks")
        w(f"| {SEASONS[s]} | {N(s, 'moved') / N(s, 'weeks'):.2f} | {pct(fw, N(s, 'weeks'))} | {N(s, 'forage_got') / fw:.1f} | "
          f"{N(s, 'forage_rate') / fw:.1f} | {N(s, 'forage_got') / N(s, 'forage_rate'):.2f} |")

    w("\n## Q5. Do they stop when fed? (autumn; food held when choosing, in weeks of their and their dependents' need)\n")
    w("| food held | adult autumn-weeks | share spent foraging |")
    w("|---|---|---|")
    for b in FOOD_BANDS:
        f = sum(D[x]["by_band"].get(b, [0, 0])[0] for x in SEEDS)
        t = sum(D[x]["by_band"].get(b, [0, 0])[1] for x in SEEDS)
        w(f"| {b} weeks | {t:,} | {pct(f, t)} |")

    w("\n## Q6. How much surplus could there have been? (upper bound, per adult per autumn)\n")
    pot = sorted(r[1] for r in rows)
    w(f"Extra food from foraging in every autumn week they did not forage (formula, capped by their tile's food and their "
      f"room to carry): median **{statistics.median(pot):.0f}** (middle half {pot[len(pot) // 4]:.0f}–{pot[3 * len(pot) // 4]:.0f}). "
      f"Actually gathered: median {statistics.median([r[0] for r in rows]):.0f}. Gathered plus potential reaching 91 (an adult's "
      f"winter): {pct(sum(1 for r in rows if r[0] + r[1] >= 91), len(rows))}; reaching 195 (a carer with two children): "
      f"{pct(sum(1 for r in rows if r[0] + r[1] >= 195), len(rows))}. Potential alone reaching 91: "
      f"{pct(sum(1 for r in rows if r[1] >= 91), len(rows))}.")

    (HERE / "findings_tables.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
