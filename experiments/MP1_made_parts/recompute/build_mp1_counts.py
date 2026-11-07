"""Builds the blind-recompute file for MP1: per world, the stage counts and the first-fate counts, read straight from
the raw world files. Written before data.

  python experiments/MP1_made_parts/recompute/build_mp1_counts.py [output_dir out_csv]
"""
import glob
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 2 else HERE.parent / "output"
DST = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "mp1_counts.csv"
FATES = (("used: into its kind", "used_into_kind"), ("used: into another thing", "used_into_other"),
         ("used: lost in a fire", "lost_in_fire"), ("worn out in use", "worn_use"), ("worn out by the cold", "worn_cold"),
         ("dropped at the carry limit", "dropped"), ("handed to another", "handed"),
         ("died: passed to an heir", "died_heir"), ("died: left with the body", "died_body"), ("still held", "still_held"),
         ("unexplained", "unexplained"))
rows = ["seed,kinds," + ",".join(f"stage_{s}" for s in "ABCDE") + "," + ",".join(c for _, c in FATES)]
for f in sorted(glob.glob(str(SRC / "c_seed_*.json"))):
    r = json.load(open(f))
    st, fa = r["stages"], r["fates"]
    rows.append(f"{r['seed']},{st.get('kinds', 0)}," + ",".join(str(st.get(f"stage_{s}", 0)) for s in "ABCDE") + ","
                + ",".join(str(fa.get(k, 0)) for k, _ in FATES))
DST.write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
