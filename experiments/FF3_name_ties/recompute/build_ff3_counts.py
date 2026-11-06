"""Builds the blind-recompute file for FF3: per arm and world, the counts behind the harm check. Written before data.

  python experiments/FF3_name_ties/recompute/build_ff3_counts.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
rows = ["arm,seed,living_weeks,extinct,recipes_evict,recipes_tie"]
for f in sorted(glob.glob(str(HERE.parent / "output" / "*_seed_*.json"))):
    r = json.load(open(f))
    s = r["sums"]
    rows.append(",".join(str(x) for x in (r["arm"], r["seed"], int(s.get("living_weeks", 0)), int(r["extinct"]),
                                          int(s.get("recipes_evict", 0)), int(s.get("recipes_tie", 0)))))
(HERE / "ff3_counts.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
