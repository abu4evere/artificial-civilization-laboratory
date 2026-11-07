"""Builds the blind-recompute file for EG1: per world, the sums behind the primary and secondaries 1, 3, 4 and 7, read
straight from the raw world files. Written before data.

  python experiments/EG1_energy_gate/recompute/build_eg1_counts.py [output_dir out_csv]
"""
import glob
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 2 else HERE.parent / "output"
DST = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "eg1_counts.csv"
COLS = ("starving_weeks", "starving_a", "starving_b", "starving_c", "starving_d", "starving_c_quirk",
        "nonstarving_weeks", "nonstarving_c", "nonstarving_c_quirk", "starvation_deaths_6plus",
        "starvation_deaths_blocked_last4")
rows = ["seed," + ",".join(COLS) + ",extinct"]
for f in sorted(glob.glob(str(SRC / "c_seed_*.json"))):
    r = json.load(open(f))
    t = {0: Counter(), 1: Counter()}
    for k, v in r["sums"].items():
        t[int(k.split("|")[2])].update(v)
    v = (t[1]["weeks"], t[1]["a"], t[1]["b"], t[1]["c"], t[1]["d"], t[1]["c_affordable_tile_with_food"],
         t[0]["weeks"], t[0]["c"], t[0]["c_affordable_tile_with_food"], r["deaths"].get("starvation", 0),
         r["deaths"].get("starvation_blocked_last4", 0))
    rows.append(f"{r['seed']}," + ",".join(str(int(x)) for x in v) + f",{int(r['extinct'])}")
DST.write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
