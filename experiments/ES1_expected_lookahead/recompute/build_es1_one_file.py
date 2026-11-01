"""Builds the blind-recompute file for ES1: per seed and arm, the raw sums of the calibration error over all actions
(no analysis logic beyond sums). Written before data.

  python experiments/ES1_expected_lookahead/recompute/build_es1_one_file.py
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
rows = ["seed,v11_n,v11_sum_abs,e_n,e_sum_abs,sham_n,sham_sum_abs"]
for seed in sorted(d):
    a = d[seed]
    rows.append(f"{seed},{a['c'][0]},{a['c'][1]:.6f},{a['e'][0]},{a['e'][1]:.6f},{a['x'][0]},{a['x'][1]:.6f}")
(HERE / "es1_one_file.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "seeds")
