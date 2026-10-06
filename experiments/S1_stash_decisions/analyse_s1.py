"""S1 tables (questions.md), written before the S1 data existed. Writes findings_tables.md.

  python experiments/S1_stash_decisions/analyse_s1.py
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


def main():
    D = {s: json.loads((OUT / f"seed_{s}.json").read_text(encoding="utf-8")) for s in SEEDS}
    L = []
    w = L.append
    w("# S1 — Why stashing almost never wins: tables\n")
    v = (OUT / "verify.txt").read_text(encoding="utf-8").strip()
    rep = all(r["replay_matches"] for r in D.values())
    w(f"Exactness: {v}. Replays match the saved E13R runs in all 16: **{'yes' if rep else 'NO'}**.\n")

    def N(s, key):
        return sum(D[x]["n"].get(str(s), {}).get(key, 0.0) for x in SEEDS)

    def NA(key):
        return sum(N(s, key) for s in range(4))

    w("## Q1. How often is stashing considered? (adult-weeks)\n")
    w("| season | adult-weeks | food above the line | seed above the line | put offered (any thing) | "
      "put offered for food or seed | put offered for a material | put food or seed chosen |")
    w("|---|---|---|---|---|---|---|---|")
    for i, name in enumerate(SEASONS + ("all",)):
        f = (lambda k: NA(k)) if name == "all" else (lambda k, i=i: N(i, k))
        wk = f("weeks")
        w(f"| {name} | {wk:,.0f} | {pct(f('elig_food'), wk)} | {pct(f('elig_seeds'), wk)} | {pct(f('put_offered'), wk)} | "
          f"{pct(f('put_food_offered'), wk)} | {pct(f('put_material'), wk)} | {pct(f('put_food_chosen'), wk, 2)} |")
    w(f"\nWeeks with food above the line in which put was offered for a material instead: "
      f"{NA('material_while_food_eligible'):,.0f} of {NA('elig_food'):,.0f}.")
    w(f"\nOf the weeks in which put was offered for food or seed, it was chosen in "
      f"{pct(NA('put_food_chosen'), NA('put_food_offered'), 2)}; per world: "
      + ", ".join(pct(sum(D[x]["n"].get(str(s), {}).get("put_food_chosen", 0) for s in range(4)),
                      sum(D[x]["n"].get(str(s), {}).get("put_food_offered", 0) for s in range(4)), 1) for x in SEEDS) + ".")

    w("\n## Q2. What beats it?\n")
    off = NA("put_food_offered")
    w(f"Mean probability the choice gave to putting, when offered: **{NA('prob_sum') / off:.3f}**. "
      f"Mean gap between the top option's score and put's: **{NA('gap') / off:.2f}**.\n")
    bins = Counter()
    for x in SEEDS:
        for k, c in D[x]["prob_bins"].items():
            bins[int(k)] += c
    w("| probability of putting | share of offers |")
    w("|---|---|")
    for b in range(10):
        w(f"| {b / 10:.1f}–{(b + 1) / 10:.1f} | {pct(bins[b], sum(bins.values()))} |")
    win = Counter()
    for x in SEEDS:
        for s, d in D[x]["winners"].items():
            win.update(d)
    tot = sum(win.values())
    w("\n| action chosen instead | share |")
    w("|---|---|")
    for a, c in win.most_common(10):
        w(f"| {a} | {pct(c, tot)} |")
    w("\nBy season, the three most common winners: " + "; ".join(
        f"{SEASONS[int(s)]}: " + ", ".join(f"{a} {pct(c, sum(cs.values()), 0)}" for a, c in cs.most_common(3))
        for s, cs in sorted(((s, sum((Counter(D[x]["winners"].get(s, {})) for x in SEEDS), Counter())) for s in "0123"))) + ".")

    w("\n## Q3. What value does stashing get, against foraging? (same weeks)\n")
    w("| | mean score | of which habit |")
    w("|---|---|---|")
    w(f"| put food or seed | {NA('put_score') / off:.3f} | {NA('put_habit') / off:.3f} |")
    wf = NA("with_forage")
    w(f"| forage, in the weeks put was offered | {NA('forage_score') / wf:.3f} | {NA('forage_habit') / wf:.3f} |")
    w(f"\nWhen put was offered for food or seed, the person held a belief about it from their own experience in "
      f"{pct(NA('has_belief'), off)} of weeks (mean belief, counting none as 0: {NA('belief_sum') / off:.3f}); only a "
      f"belief they had been told in {pct(NA('heard_only'), off)}.")

    w("\n## Q4. Do successful stashers learn that it worked?\n")
    ev = [e for x in SEEDS for e in D[x]["learn"]]
    up = down = same = 0
    for e in ev:
        ch = [((e["after"].get(k) or 0) - (e["before"].get(k) or 0)) for k in set(e["after"]) | set(e["before"])]
        big = max(ch, key=abs) if ch else 0.0
        if big > 1e-9:
            up += 1
        elif big < -1e-9:
            down += 1
        else:
            same += 1
    w(f"Owners taking their own stash back after two or more weeks: **{len(ev)}** times in 16 worlds × 120 years. "
      f"Belief about stashing rose {up}, fell {down}, unchanged {same}. Median weeks stored: "
      f"{statistics.median([e['weeks'] for e in ev]) if ev else '–'}. Stashes found gone: "
      f"{sum(D[x]['found_gone'] for x in SEEDS)}.")

    w("\n## Q5. Does it spread?\n")
    H = [h for x in SEEDS for h in D[x]["holders"]]
    ad = sum(h["adults"] for h in H)
    w(f"Ten-yearly samples: adults holding a positive belief about stashing food or seed from their own experience "
      f"{pct(sum(h['own_positive'] for h in H), ad)}; holding one they were told {pct(sum(h['told_positive'] for h in H), ad)}.")
    told = Counter()
    for x in SEEDS:
        told.update(D[x]["told"])
    w(f"\nTimes anyone was told a belief about stashing food or seed: {sum(told.values())} ({dict(told)}).")

    (HERE / "findings_tables.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
