"""Builds the blind-recompute file for ES2: per seed and arm, the raw sums of the calibration error over all actions
(no analysis logic beyond sums). Written before data.

  python experiments/ES2_realized_lookahead/recompute/build_es2_one_file.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
d = {}
for f in glob.glob(str(HERE.parent / "output" / "*_seed_*.json")):
    r = json.load(open(f))
    n = sum(v[0] for v in r["cal"].values())
    s = sum(v[1] for v in r["cal"].values())
    d.setdefault(r["seed"], {})[r["arm"]] = (n, s)
rows = ["seed,v11_n,v11_sum_abs,r_n,r_sum_abs,sham_n,sham_sum_abs"]
for seed in sorted(d):
    a = d[seed]
    rows.append(f"{seed},{a['c'][0]},{a['c'][1]:.6f},{a['r'][0]},{a['r'][1]:.6f},{a['x'][0]},{a['x'][1]:.6f}")
(HERE / "es2_one_file.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "seeds")
