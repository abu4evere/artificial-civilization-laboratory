"""Builds the blind-recompute file for UV2: per seed, the raw sums for the primary (arm r; k >= 80, ages 16-44, G not
closed by death): n and sum (q - G) in the cell Dn < 0.1 and over all Dn. No analysis logic beyond sums. Written before
data.

  python experiments/UV2_propagation/recompute/build_uv2_one_file.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
HIGH, PRIME, LOW_DN = ("80-159", "160+"), ("16-29", "30-44"), ("0-0.05", "0.05-0.1")
rows = ["seed,n_low_dn,sum_low_dn,n_all,sum_all"]
d = {}
for f in glob.glob(str(HERE.parent / "output" / "r_seed_*.json")):
    r = json.load(open(f))
    s = [0, 0.0, 0, 0.0]
    for key, v in r["uv2"].items():
        kb, ab, db, _, _, ce = key.split("|")
        if kb not in HIGH or ab not in PRIME or ce != "0":
            continue
        s[2] += v[0]
        s[3] += v[1]
        if db in LOW_DN:
            s[0] += v[0]
            s[1] += v[1]
    d[r["seed"]] = s
for seed in sorted(d):
    s = d[seed]
    rows.append(f"{seed},{s[0]},{s[1]:.6f},{s[2]},{s[3]:.6f}")
(HERE / "uv2_one_file.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "seeds")
