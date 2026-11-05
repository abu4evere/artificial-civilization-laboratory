"""Builds the blind-recompute file for PB1b: per world, the summed squared standardised errors (over the 9 outputs) of
the table B, E-own and E-obs on the unfamiliar cases (gate part 1) and on the familiar cases (gate part 2).

  python experiments/PB1b_episodic_predictor/recompute/build_pb1b_sums.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
cols = []
for v in ("B", "E", "Eo"):
    for c in ("u_pair", "fam"):
        cols.append((v, c))
rows = ["seed," + ",".join(f"sse_{v}_{c}" for v, c in cols) + ",n_u_pair,n_fam"]
for f in sorted(glob.glob(str(HERE.parent / "output" / "c_seed_*.json"))):
    r = json.load(open(f))
    rows.append(f"{r['seed']}," + ",".join(f"{sum(r['sse'][v][c]):.6f}" for v, c in cols)
                + f",{r['counts'].get('u_pair', 0)},{r['counts'].get('fam', 0)}")
(HERE / "pb1b_sums.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
