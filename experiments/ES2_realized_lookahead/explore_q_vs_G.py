"""ES2, EXPLORATORY (not frozen, decides nothing): is rest's worse calibration under the realized look-ahead special to
rest, or one case of a general under-valuation? For each action, in the crisis situation (weak or under half a week of
food, with company) and in all other situations pooled: mean habit value q, mean realized return G and mean |q - G|,
under v11 and r. Reads ES2's raw output only (the observer's `cal` sums: n, sum_abs, sum_signed, censored, sum_q, sum_G).

  python experiments/ES2_realized_lookahead/explore_q_vs_G.py     # prints; writes explore_q_vs_G.md
"""
import glob
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
MIN_N = 10_000
cells = {a: defaultdict(lambda: [0.0] * 6) for a in ("c", "r")}    # (group, action) -> summed cal fields
for f in glob.glob(str(HERE / "output" / "*_seed_*.json")):
    r = json.load(open(f))
    if r["arm"] not in cells:
        continue
    assert r["cal_fields"] == ["n", "sum_abs", "sum_signed", "censored", "sum_q", "sum_G"]
    for k, v in r["cal"].items():
        ctx, act = k.split("|", 1)
        ctx = int(ctx)
        crisis = ctx // 8 == 0 and (ctx % 8) // 4 == 1
        c = cells[r["arm"]][("crisis, with company" if crisis else "all other situations", act)]
        for i in range(6):
            c[i] += v[i]

L = ["# ES2 — exploratory: habit value against realized return, by action (NOT frozen; decides nothing)", "",
     "Reads ES2's raw output (`output/`, 32 seeds per arm), habit updates started in years 100-200. q = the habit "
     "value when the update started; G = the return that followed (VC1's measure). Actions with at least "
     f"{MIN_N:,} closed updates in both arms.", "",
     "| situation | action | v11 n | v11 q | v11 G | v11 abs(q-G) | r n | r q | r G | r abs(q-G) | rise |",
     "|---|---|---|---|---|---|---|---|---|---|---|"]
below = {"c": [0, 0], "r": [0, 0]}
tot = {a: [0.0, 0.0, 0.0] for a in cells}
for key in sorted(set(cells["c"]) | set(cells["r"])):
    c, r = cells["c"][key], cells["r"][key]
    for a, x in (("c", c), ("r", r)):
        tot[a][0] += x[0]
        tot[a][1] += x[4]
        tot[a][2] += x[5]
    if c[0] < MIN_N or r[0] < MIN_N:
        continue
    for a, x in (("c", c), ("r", r)):
        below[a][0] += x[4] / x[0] < x[5] / x[0]
        below[a][1] += 1
    L.append(f"| {key[0]} | {key[1]} | {int(c[0]):,} | {c[4] / c[0]:+.3f} | {c[5] / c[0]:+.3f} | {c[1] / c[0]:.3f} | "
             f"{int(r[0]):,} | {r[4] / r[0]:+.3f} | {r[5] / r[0]:+.3f} | {r[1] / r[0]:.3f} | "
             f"{r[1] / r[0] - c[1] / c[0]:+.3f} |")
L += ["",
      f"- **All updates:** v11 mean q {tot['c'][1] / tot['c'][0]:+.3f}, mean G {tot['c'][2] / tot['c'][0]:+.3f}; "
      f"r mean q {tot['r'][1] / tot['r'][0]:+.3f}, mean G {tot['r'][2] / tot['r'][0]:+.3f}.",
      f"- **Rows where q is below G:** v11 {below['c'][0]} of {below['c'][1]}; r {below['r'][0]} of {below['r'][1]}.",
      "",
      "## Reading (the assistant's; a hypothesis for the council, not a finding)",
      "- **Under r, rest is not a special case.** The realized return G hardly moves between the arms in any row. What "
      "changes is q: under r it sits below G for every action listed, so the whole habit system under-values.",
      "  - Under v11 the max look-ahead's inflation lifted the common actions above G and partly hid this.",
      "  - In the crisis rows, talk worsens even more than rest. The frozen per-action guard pooled each action over all "
      "situations, so talk's rise there was diluted by its other situations.",
      "- **A candidate cause, from the code** (not tested): habits start low and learn slowly.",
      "  - A newborn's habits start at half the parents' mean (`child.q = 0.25 * (mother.q + father.q)`, "
      "`acl/biology.py` line 553).",
      "  - They then move 5% of the way per update (`learning_rate` 0.05).",
      "  - Without the max's upward push, a value built from the next choice's (still low) value may climb slowly "
      "within one life.",
      "- **What would test it, read-only:** calibration split by age, or by how many times the person had already "
      "updated that habit. It would need a new frozen diagnostic study, debated with GPT and Gemini first.",
      ""]
text = "\n".join(L) + "\n"
(HERE / "explore_q_vs_G.md").write_text(text, encoding="utf-8", newline="\n")
print(text)
