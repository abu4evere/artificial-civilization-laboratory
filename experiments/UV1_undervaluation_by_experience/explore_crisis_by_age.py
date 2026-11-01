"""UV1, EXPLORATORY (not frozen, decides nothing; written before data after the smoke showed the crisis cell is mostly
children): who makes the habit updates in the crisis situation (weak or under half a week of food, with company), and
how biased are rest and talk there, by age? All k, G not closed by death, both arms.

  python experiments/UV1_undervaluation_by_experience/explore_crisis_by_age.py     # prints; writes explore_crisis_by_age.md
"""
import glob
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_uv1 import AGE_BINS  # noqa: E402

cell = {a: defaultdict(lambda: [0, 0.0]) for a in ("c", "r")}     # (age, action) -> [n, sum (q - G)]
for f in glob.glob(str(HERE / "output" / "*_seed_*.json")):
    r = json.load(open(f))
    if r["arm"] not in cell:
        continue
    for key, v in r["uv"].items():
        kb, ab, cr, act, ce = key.split("|")
        if cr != "1" or ce != "0":
            continue
        for k in ((ab, act), (ab, "*")):
            cell[r["arm"]][k][0] += v[0]
            cell[r["arm"]][k][1] += v[1]

L = ["# UV1 — exploratory: the crisis situation by age (NOT frozen; decides nothing)", "",
     "Updates started in years 100-200 in the crisis situation (weak or under half a week of food, with company), G not "
     "closed by death, all k; both arms, 32 worlds each. B = mean(q - G).", "",
     "| age | v11 n (all actions) | share of v11's crisis updates | r n (all actions) | v11 rest n | v11 rest B | r rest n | "
     "r rest B | v11 talk n | v11 talk B | r talk n | r talk B |",
     "|---|---|---|---|---|---|---|---|---|---|---|---|"]
tot_c = sum(cell["c"][(ab, "*")][0] for ab in AGE_BINS)
for ab in AGE_BINS:
    row = [ab, f"{cell['c'][(ab, '*')][0]:,}",
           f"{cell['c'][(ab, '*')][0] / tot_c:.3f}" if tot_c else "-", f"{cell['r'][(ab, '*')][0]:,}"]
    for act in ("rest", "talk"):
        for a in ("c", "r"):
            n, s = cell[a][(ab, act)]
            row += [f"{n:,}", f"{s / n:+.3f}" if n else "-"]
    L.append("| " + " | ".join(row) + " |")
L.append("")
text = "\n".join(L) + "\n"
(HERE / "explore_crisis_by_age.md").write_text(text, encoding="utf-8", newline="\n")
print(text)
