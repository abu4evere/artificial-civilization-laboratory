"""Builds the blind-recompute file for UP1: per world, the person x kind x decision counts at each step, for new and
old kinds (summed over complexity and timing). Written before data.

  python experiments/UP1_uptake_of_new_kinds/recompute/build_up1_counts.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
STEPS = ("1", "2", "3", "4a", "4b", "5", "made")
rows = ["seed,kinds,step,count"]
for f in sorted(glob.glob(str(HERE.parent / "output" / "c_seed_*.json"))):
    r = json.load(open(f))
    for cls in ("new", "old"):
        tot = [0] * 7
        for k, v in r["steps"].items():
            if k.split("|")[0] == cls:
                tot = [a + b for a, b in zip(tot, v)]
        for st, c in zip(STEPS, tot):
            rows.append(f"{r['seed']},{cls},{st},{c}")
(HERE / "up1_counts.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
