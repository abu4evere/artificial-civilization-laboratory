"""Builds the blind-recompute file for SC1: per world, the raw sums behind each primary contrast (written before
data). C12's per-world held-out errors come from the analysis (`c12_sse.npz`), since the ridge models are fitted there;
the recompute checks the ratio and its interval for C12, not the regression.

  python experiments/SC1_bob_scorecard/recompute/build_sc1_sums.py
"""
import glob
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
rows = ["seed,measure,key,n,x,y"]
for f in sorted(glob.glob(str(HERE.parent / "output" / "c_seed_*.json"))):
    r = json.load(open(f))
    s = r["seed"]
    for k, v in sorted(r["c3"].items()):
        rows.append(f"{s},c3,{k},{v[0]},{v[1]:.6f},")
    for k, v in sorted(r["c4"].items()):
        rows.append(f"{s},c4,{k},{v[1]},{v[2]},")
    for k, v in sorted(r["c5"].items()):
        rows.append(f"{s},c5,{k},{v[0]},{v[1]},")
    for i, (bf, re) in enumerate(r["c6_kinds"]):
        rows.append(f"{s},c6,{i},1,{re},{bf}")
    for k, v in sorted(r["c7"].items()):
        rows.append(f"{s},c7,{k},{v[0]},{v[1]},")
    for k, v in sorted(r["c9"].items()):
        rows.append(f"{s},c9,{k[0]},{v[0]},{v[1]},{v[2]}")
    c = r["c10"]
    rows.append(f"{s},c10,nested,{int(c.get('nested', 0))},{int(c.get('social_part', 0))},{c.get('opportunity', 0.0):.6f}")
z = np.load(HERE / "c12_sse.npz")
for s, a, b in zip(z["seeds"], z["sse_a"], z["sse_b"]):
    rows.append(f"{int(s)},c12,sse,0,{a:.6f},{b:.6f}")
(HERE / "sc1_sums.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
