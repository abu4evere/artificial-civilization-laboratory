"""Builds the blind-recompute file for AF1: per arm and world, the kinds invented in play in years 100-195, how many
had their own recipe made again by choice within five years, the living weeks and extinction. Written before data.

  python experiments/AF1_open_affordances/recompute/build_af1_counts.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
rows = ["arm,seed,kinds,remade,living_weeks,extinct"]
for f in sorted(glob.glob(str(HERE.parent / "output" / "*_seed_*.json"))):
    r = json.load(open(f))
    rows.append(f"{r['arm']},{r['seed']},{r['n_kinds']},{r['n_remade']},{int(r['sums'].get('living_weeks', 0))},"
                f"{int(r['extinct'])}")
(HERE / "af1_counts.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
