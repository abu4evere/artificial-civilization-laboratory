"""Builds the blind-recompute file for RF1: one row per world-new kind with the funnel flags. Written before data.

  python experiments/RF1_remaking_funnel/recompute/build_rf1_kinds.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
rows = ["seed,wanting_weeks,obtainable,offered,chosen,complete"]
for f in sorted(glob.glob(str(HERE.parent / "output" / "c_seed_*.json"))):
    r = json.load(open(f))
    F = {k: i for i, k in enumerate(r["rf1_fields"])}
    for k in r["rf1"]:
        rows.append(",".join(str(x) for x in (r["seed"], k[F["ww"]], k[F["obt"]], k[F["off"]], k[F["cho"]], k[F["full"]])))
(HERE / "rf1_kinds.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
