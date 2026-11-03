"""Builds the blind-recompute file for HN1: per world, the funnel counts and the pooled sums behind the return ratio.
Written before data.

  python experiments/HN1_hunting_funnel/recompute/build_hn1_counts.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
KEYS = ("hunter_weeks", "no_prey", "roll_failed", "success", "kept_sum", "forage_weeks", "forage_sum", "living_weeks")
rows = ["seed," + ",".join(KEYS) + ",extinct"]
for f in sorted(glob.glob(str(HERE.parent / "output" / "c_seed_*.json"))):
    r = json.load(open(f))
    s = r["sums"]
    rows.append(f"{r['seed']}," + ",".join(str(round(float(s.get(k, 0)), 3)) for k in KEYS) + f",{int(r['extinct'])}")
(HERE / "hn1_counts.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
