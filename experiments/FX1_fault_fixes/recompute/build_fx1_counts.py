"""Builds the blind-recompute file for FX1: per arm and world, the living weeks, extinction, and the kinds invented in
play in years 100-195 with how many had their own recipe made again within five years. Written before data.

  python experiments/FX1_fault_fixes/recompute/build_fx1_counts.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
rows = ["arm,seed,living_weeks,extinct,kinds,remade"]
for f in sorted(glob.glob(str(HERE.parent / "output" / "*_seed_*.json"))):
    r = json.load(open(f))
    rows.append(f"{r['arm']},{r['seed']},{int(r['sums'].get('living_weeks', 0))},{int(r['extinct'])},{r['n_kinds']},"
                f"{r['n_remade']}")
(HERE / "fx1_counts.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
