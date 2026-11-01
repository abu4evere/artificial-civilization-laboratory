"""ES2, EXPLORATORY (not frozen, decides nothing): in which situations does rest's calibration worsen under the
realized look-ahead? Reads ES2's raw output only. Situation = food level (0 = weak or under half a week of food,
1 = under 2 weeks, 2 = under 6 weeks, 3 = more) x company (people within reach or not) x season (`mind.context_index`).

  python experiments/ES2_realized_lookahead/explore_rest.py     # prints; writes explore_rest.md
"""
import glob
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
FOOD = {0: "weak/<0.5 wk", 1: "<2 wk", 2: "<6 wk", 3: "6+ wk"}
cells = {a: defaultdict(lambda: [0, 0.0, 0.0]) for a in ("c", "r")}   # (food, company) -> [n, sum_abs, sum_signed]
for f in glob.glob(str(HERE / "output" / "*_seed_*.json")):
    r = json.load(open(f))
    if r["arm"] not in cells:
        continue
    for k, v in r["cal"].items():
        ctx, act = k.split("|", 1)
        if act != "rest":
            continue
        ctx = int(ctx)
        key = (ctx // 8, (ctx % 8) // 4)
        c = cells[r["arm"]][key]
        c[0] += v[0]
        c[1] += v[1]
        c[2] += v[2]
L = ["# ES2 — exploratory: where rest's calibration worsens (NOT frozen; decides nothing)", "",
     "Reads ES2's raw output (`output/`, 32 seeds per arm). Rest's habit updates started in years 100-200, by the "
     "situation they were made in (food level x company; seasons pooled).", "",
     "| food | company | v11 n | v11 mean abs(q-G) | v11 bias | r n | r mean abs(q-G) | r bias | rise |",
     "|---|---|---|---|---|---|---|---|---|"]
tot = {a: [0, 0.0] for a in cells}
for food in range(4):
    for comp in (0, 1):
        c, r = cells["c"][(food, comp)], cells["r"][(food, comp)]
        for a, x in (("c", c), ("r", r)):
            tot[a][0] += x[0]
            tot[a][1] += x[1]
        if c[0] and r[0]:
            mc, mr = c[1] / c[0], r[1] / r[0]
            L.append(f"| {FOOD[food]} | {'yes' if comp else 'no'} | {c[0]:,} | {mc:.3f} | {c[2] / c[0]:+.3f} | "
                     f"{r[0]:,} | {mr:.3f} | {r[2] / r[0]:+.3f} | {mr - mc:+.3f} |")
L += ["", f"All rest updates: v11 {tot['c'][1] / tot['c'][0]:.4f} over {tot['c'][0]:,}; r {tot['r'][1] / tot['r'][0]:.4f} "
          f"over {tot['r'][0]:,} (the frozen guard's numbers: 0.237 -> 0.391).", ""]
text = "\n".join(L) + "\n"
(HERE / "explore_rest.md").write_text(text, encoding="utf-8")
print(text)
