"""Builds the blind-recompute file for LW1: per arm and world, the sums behind the guards, the co-primary and the
secondaries, read straight from the raw world files. Written before data.

  python experiments/LW1_learners_wish/recompute/build_lw1_counts.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
SUMS = ("living_weeks", "death_starvation", "death_killed", "census_adults", "census_health", "child_weeks",
        "child_deaths", "child_death_starvation", "adult_weeks", "gifts_kin_children")
TOP = ("lw_kinds", "lw_learned", "lw_made_other", "lw_pairs", "lw_pairs_got_part")
rows = ["arm,seed," + ",".join(SUMS) + ",extinct," + ",".join(TOP)]
for f in sorted(glob.glob(str(HERE.parent / "output" / "*_seed_*.json"))):
    r = json.load(open(f))
    s = r["sums"]
    rows.append(f"{r['arm']},{r['seed']}," + ",".join(str(round(float(s.get(k, 0)), 3)) for k in SUMS)
                + f",{int(r['extinct'])}," + ",".join(str(int(r.get(k, 0))) for k in TOP))
(HERE / "lw1_counts.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
