"""Builds the blind-recompute file for TR1: per-world raw sums from the output JSONs (no analysis logic beyond sums).

  python experiments/TR1_tool_returns/recompute/build_tr1_one_file.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
rows = ["seed,food_with,food_without,food_world_best,food_known_best"]
for f in sorted(glob.glob(str(HERE.parent / "output" / "lp_seed_*.json"))):
    r = json.load(open(f))
    s = r["sums"]
    rows.append(f"{r['seed']},{s.get('with', 0):.6f},{s.get('without', 0):.6f},{s.get('world', 0):.6f},"
                f"{s.get('known', 0):.6f}")
(HERE / "tr1_one_file.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "worlds")
