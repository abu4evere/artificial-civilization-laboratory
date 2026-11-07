"""Builds the blind-recompute file for FF4: per arm and world, the sums behind the eight guards and EG1's P, read
straight from the raw world files. Written before data.

  python experiments/FF4_affordable_targets/recompute/build_ff4_counts.py [output_dir out_csv]
"""
import glob
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 2 else HERE.parent / "output"
DST = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "ff4_counts.csv"
SUMS = ("living_weeks", "death_starvation", "death_killed", "census_adults", "census_health", "child_weeks",
        "child_deaths", "child_death_starvation", "adult_weeks", "gifts_kin_children")
EG = ("starving_weeks", "starving_c", "women30_starving_weeks", "women30_starving_c", "men30_starving_weeks",
      "men30_starving_c")


def eg(r, part, band=None, sex=None):
    t = 0
    for k, v in r["eg"].items():
        b, s, st = k.split("|")
        if st != "1" or (band and b != band) or (sex and s != sex):
            continue
        t += v.get(part, 0)
    return t


rows = ["arm,seed," + ",".join(SUMS) + ",extinct," + ",".join(EG)]
for f in sorted(glob.glob(str(SRC / "*_seed_*.json"))):
    r = json.load(open(f))
    s = r["sums"]
    e = (eg(r, "weeks"), eg(r, "c"), eg(r, "weeks", "30-49", "F"), eg(r, "c", "30-49", "F"),
         eg(r, "weeks", "30-49", "M"), eg(r, "c", "30-49", "M"))
    rows.append(f"{r['arm']},{r['seed']}," + ",".join(str(round(float(s.get(k, 0)), 3)) for k in SUMS)
                + f",{int(r['extinct'])}," + ",".join(str(int(x)) for x in e))
DST.write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
