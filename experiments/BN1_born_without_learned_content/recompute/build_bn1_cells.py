"""Builds the blind-recompute file for BN1: per arm, seed and cell (situation|action), the raw sums for early-life
habit updates (ages 52-103 weeks, years 100-200, G not closed by death): n and sum |q - G|. The reference worlds
(arm r) give the fixed cell weights. No analysis logic beyond sums. Written before data.

  python experiments/BN1_born_without_learned_content/recompute/build_bn1_cells.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
rows = ["arm,seed,cell,n,sum_abs"]
for f in sorted(glob.glob(str(HERE.parent / "output" / "*_seed_*.json"))):
    r = json.load(open(f))
    for cell, v in sorted(r["early"].get("0", {}).items()):
        rows.append(f"{r['arm']},{r['seed']},{cell},{v[0]},{v[1]:.6f}")
(HERE / "bn1_cells.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
