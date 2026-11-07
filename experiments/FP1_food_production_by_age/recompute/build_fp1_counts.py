"""Builds the blind-recompute file for FP1: per world, age band and sex, the sums behind the main table. Written before
data.

  python experiments/FP1_food_production_by_age/recompute/build_fp1_counts.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
F = ("person_weeks", "production", "act:forage", "hunt", "need", "active_weeks", "active_production", "active_need")
rows = ["seed,band,sex," + ",".join(f.replace("act:", "") for f in F)]
for f in sorted(glob.glob(str(HERE.parent / "output" / "c_seed_*.json"))):
    r = json.load(open(f))
    for key, s in sorted(r["sums"].items()):
        b, sx = key.split("|")
        rows.append(f"{r['seed']},{b},{sx}," + ",".join(str(round(float(s.get(x, 0.0)), 4)) for x in F))
(HERE / "fp1_counts.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
