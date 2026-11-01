"""Builds the blind-recompute file for UV1: per seed and arm, the raw sums for the primary (ages 16-44, G not closed
by death): n and sum (q - G) at k 0-19 and at k 80+. No analysis logic beyond sums. Written before data.

  python experiments/UV1_undervaluation_by_experience/recompute/build_uv1_one_file.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
LOW, HIGH, PRIME = ("0-9", "10-19"), ("80-159", "160+"), ("16-29", "30-44")
d = {}
for f in glob.glob(str(HERE.parent / "output" / "*_seed_*.json")):
    r = json.load(open(f))
    s = [0, 0.0, 0, 0.0]                      # n low, sum signed low, n high, sum signed high
    for key, v in r["uv"].items():
        kb, ab, _, _, ce = key.split("|")
        if ab not in PRIME or ce != "0":
            continue
        if kb in LOW:
            s[0] += v[0]
            s[1] += v[1]
        elif kb in HIGH:
            s[2] += v[0]
            s[3] += v[1]
    d.setdefault(r["seed"], {})[r["arm"]] = s
rows = ["seed,v11_n_low,v11_sum_low,v11_n_high,v11_sum_high,r_n_low,r_sum_low,r_n_high,r_sum_high"]
for seed in sorted(d):
    a, b = d[seed]["c"], d[seed]["r"]
    rows.append(f"{seed},{a[0]},{a[1]:.6f},{a[2]},{a[3]:.6f},{b[0]},{b[1]:.6f},{b[2]},{b[3]:.6f}")
(HERE / "uv1_one_file.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "seeds")
