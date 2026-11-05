"""Builds the blind-recompute file for PB1: per world, the summed squared standardised errors of L-own and of the
baseline B (over the 9 outputs) on the primary cases (compositionally unfamiliar common-action weeks) and on the
mandatory secondary cases (unfamiliar property combinations), with the case counts.

  python experiments/PB1_shadow_predictor/recompute/build_pb1_sums.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
rows = ["seed,sse_L_pair,sse_B_pair,n_pair,sse_L_prop,sse_B_prop,n_prop"]
for f in sorted(glob.glob(str(HERE.parent / "output" / "c_seed_*.json"))):
    r = json.load(open(f))
    s, c = r["sse"], r["counts"]
    rows.append(f"{r['seed']},{sum(s['L']['u_pair']):.6f},{sum(s['B']['u_pair']):.6f},{c.get('u_pair', 0)},"
                f"{sum(s['L']['u_prop']):.6f},{sum(s['B']['u_prop']):.6f},{c.get('u_prop', 0)}")
(HERE / "pb1_sums.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
