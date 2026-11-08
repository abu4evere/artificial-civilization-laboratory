"""Builds the blind-recompute file for VW1: per arm and world, the sums behind the eight guards and the two
co-primaries (MP1's stages), read straight from the raw world files. Written before data.

  python experiments/VW1_value_of_wholes/recompute/build_vw1_counts.py [output_dir out_csv]
"""
import glob
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 2 else HERE.parent / "output"
DST = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "vw1_counts.csv"
SUMS = ("living_weeks", "death_starvation", "death_killed", "census_adults", "census_health", "child_weeks",
        "child_deaths", "child_death_starvation", "adult_weeks", "gifts_kin_children")
rows = ["arm,seed," + ",".join(SUMS) + ",extinct,kinds,any_part_held,all_parts_held"]
for f in sorted(glob.glob(str(SRC / "*_seed_*.json"))):
    r = json.load(open(f))
    s, st = r["sums"], r["stages"]
    anyp = sum(st.get(f"stage_{k}", 0) for k in "BCDE")
    allp = sum(st.get(f"stage_{k}", 0) for k in "CDE")
    rows.append(f"{r['arm']},{r['seed']}," + ",".join(str(round(float(s.get(k, 0)), 3)) for k in SUMS)
                + f",{int(r['extinct'])},{st.get('kinds', 0)},{anyp},{allp}")
DST.write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
