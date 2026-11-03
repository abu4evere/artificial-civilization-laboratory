"""Builds the blind-recompute file for FF2: per arm and world, the counts behind the frozen decision and the described
hunting measure. Written after the frozen analysis ran, before any recompute; it adds no new measure.

  python experiments/FF2_fault_fixes_2/recompute/build_ff2_counts.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
KEYS = ("living_weeks", "adult_weeks", "adult_hunter_weeks", "hunts", "hunt_successes")
rows = ["arm,seed," + ",".join(KEYS) + ",extinct"]
for f in sorted(glob.glob(str(HERE.parent / "output" / "*_seed_*.json"))):
    r = json.load(open(f))
    rows.append(f"{r['arm']},{r['seed']}," + ",".join(str(int(r['sums'].get(k, 0))) for k in KEYS)
                + f",{int(r['extinct'])}")
(HERE / "ff2_counts.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
