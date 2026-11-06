"""Builds the blind-recompute file for CI1: per arm and world, the sums behind the harm guards and the co-primary.
Written before data.

  python experiments/CI1_children_and_aims/recompute/build_ci1_counts.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
KEYS = ("living_weeks", "death_starvation", "death_killed", "census_adults", "census_health", "child_weeks",
        "child_deaths", "child_death_starvation", "adult_weeks", "gifts_kin_children")
rows = ["arm,seed," + ",".join(KEYS) + ",extinct,kinds,complete"]
for f in sorted(glob.glob(str(HERE.parent / "output" / "*_seed_*.json"))):
    r = json.load(open(f))
    s = r["sums"]
    rows.append(f"{r['arm']},{r['seed']}," + ",".join(str(round(float(s.get(k, 0)), 3)) for k in KEYS)
                + f",{int(r['extinct'])},{r['n_kinds']},{r['n_complete']}")
(HERE / "ci1_counts.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
