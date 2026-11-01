"""Builds the blind-recompute file for UV3: per seed and cell (age bin x situation x action), the raw sums for the
primary population (k >= 80, ages 16-44, G not closed by death) in years 100-124 (q1) and 175-199 (q4): n and sum G.
No analysis logic beyond sums. Written before data.

  python experiments/UV3_time_trend/recompute/build_uv3_cells.py
"""
import glob
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
rows = ["seed,cell,n_q1,sumG_q1,n_q4,sumG_q4"]
for f in sorted(glob.glob(str(HERE.parent / "output" / "r_seed_*.json"))):
    r = json.load(open(f))
    c = defaultdict(lambda: [0, 0.0, 0, 0.0])
    for key, v in r["prim"].items():
        qt, ab, ctx, act, ce = key.split("|")
        if ce != "0" or qt not in ("0", "3"):
            continue
        j = 0 if qt == "0" else 2
        c[f"{ab}/{ctx}/{act}"][j] += v[0]
        c[f"{ab}/{ctx}/{act}"][j + 1] += v[2]
    for cell in sorted(c):
        x = c[cell]
        rows.append(f"{r['seed']},{cell},{x[0]},{x[1]:.6f},{x[2]},{x[3]:.6f}")
(HERE / "uv3_cells.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
