"""Builds the blind-recompute file for OD1: per arm and world, the sums behind CI1's eight guards and the manipulation
counts per door, read straight from the raw world files. Written before data.

  python experiments/OD1_open_doors/recompute/build_od1_counts.py [output_dir out_csv]
"""
import glob
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 2 else HERE.parent / "output"
DST = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "od1_counts.csv"
SUMS = ("living_weeks", "death_starvation", "death_killed", "census_adults", "census_health", "child_weeks",
        "child_deaths", "child_death_starvation", "adult_weeks", "gifts_kin_children")
OD = ("grown_weeks", "made_by_make", "made_standin", "over_items_weeks", "over_mats_weeks", "made_binder_used",
      "made_hammer_used", "layer_cold_weeks", "layer_carry_weeks")
rows = ["arm,seed," + ",".join(SUMS) + ",extinct," + ",".join(OD)]
for f in sorted(glob.glob(str(SRC / "*_seed_*.json"))):
    r = json.load(open(f))
    s, od = r["sums"], r["od"]
    rows.append(f"{r['arm']},{r['seed']}," + ",".join(str(round(float(s.get(k, 0)), 3)) for k in SUMS)
                + f",{int(r['extinct'])}," + ",".join(str(int(od.get(k, 0))) for k in OD))
DST.write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
