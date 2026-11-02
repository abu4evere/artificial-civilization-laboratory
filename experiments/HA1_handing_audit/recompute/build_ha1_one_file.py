"""Builds the blind-recompute file for HA1: per seed, the raw sums for the primary (all givers): eligible decisions,
decisions with at least one handing option, and the summed softmax mass on handing options. Written before data.

  python experiments/HA1_handing_audit/recompute/build_ha1_one_file.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
rows = ["seed,decisions,with_option,mass"]
for f in sorted(glob.glob(str(HERE.parent / "output" / "h_seed_*.json"))):
    r = json.load(open(f))
    d = sum(v[0] for v in r["by"].values())
    o = sum(v[3] for v in r["by"].values())
    m = sum(v[4] for v in r["by"].values())
    rows.append(f"{r['seed']},{d},{o},{m:.6f}")
(HERE / "ha1_one_file.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "seeds")
