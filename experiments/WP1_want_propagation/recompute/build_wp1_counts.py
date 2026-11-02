"""Builds the blind-recompute file for WP1: per arm and world, the kinds invented in play in years 100-195, the number
made again within five years, and the living weeks (for the population guard). Written before data.

  python experiments/WP1_want_propagation/recompute/build_wp1_counts.py
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
(HERE / "wp1_counts.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
