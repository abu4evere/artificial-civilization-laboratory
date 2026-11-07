"""Builds the blind-recompute file for PM1: per world, the furthest-stage counts of the followed kinds (P0a ... P7),
the depth-3+ counts and the never-valued counts, read straight from the raw world files. Written before data.

  python experiments/PM1_part_making/recompute/build_pm1_counts.py [output_dir out_csv]
"""
import glob
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 2 else HERE.parent / "output"
DST = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "pm1_counts.csv"
ST = ("P0a", "P0b", "P1", "P2", "P3", "P4", "P5", "P6", "P7")
rows = ["seed,kinds," + ",".join(ST) + ",never_valued,never_valued_P0a"]
for f in sorted(glob.glob(str(SRC / "c_seed_*.json"))):
    s = json.load(open(f))
    r, st = s, s["stages"]
    rows.append(f"{r['seed']},{st.get('kinds', 0)}," + ",".join(str(st.get(f"stage_{x}", 0)) for x in ST)
                + f",{st.get('valued0', 0)},{st.get('valued0_P0a', 0)}")
DST.write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
