"""Builds the blind-recompute file for DF1: per world, the grown person-weeks and feeding-caused short weeks of women and
of men, read straight from the raw world files. Written before data.

  python experiments/DF1_dependents_feeding/recompute/build_df1_counts.py [output_dir out_csv]
"""
import glob
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 2 else HERE.parent / "output"
DST = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "df1_counts.csv"
rows = ["seed,women_weeks,women_fcs,men_weeks,men_fcs"]
for f in sorted(glob.glob(str(SRC / "c_seed_*.json"))):
    r = json.load(open(f))
    t = {"F": [0, 0], "M": [0, 0]}
    for k, v in r["sums"].items():
        sx = k.split("|")[0]
        t[sx][0] += v.get("weeks", 0)
        t[sx][1] += v.get("fcs", 0)
    rows.append(f"{r['seed']},{t['F'][0]},{t['F'][1]},{t['M'][0]},{t['M'][1]}")
DST.write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
