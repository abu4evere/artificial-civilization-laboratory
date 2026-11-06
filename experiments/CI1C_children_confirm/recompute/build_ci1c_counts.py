"""Builds the blind-recompute file for CI1-C: per arm and world, the sums behind the harm guards, the co-primary, the
secondary (remaking) and the described making by others. Written before data.

  python experiments/CI1C_children_confirm/recompute/build_ci1c_counts.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
KEYS = ("living_weeks", "death_starvation", "death_killed", "census_adults", "census_health", "child_weeks",
        "child_deaths", "child_death_starvation", "adult_weeks", "gifts_kin_children")
rows = ["arm,seed," + ",".join(KEYS) + ",extinct,kinds,complete,remade,others"]
for f in sorted(glob.glob(str(HERE.parent / "output" / "*_seed_*.json"))):
    r = json.load(open(f))
    s = r["sums"]
    rows.append(f"{r['arm']},{r['seed']}," + ",".join(str(round(float(s.get(k, 0)), 3)) for k in KEYS)
                + f",{int(r['extinct'])},{r['n_kinds']},{r['n_complete']},{r['n_remade']},{r['n_others']}")
(HERE / "ci1c_counts.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
