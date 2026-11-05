"""Builds the blind-recompute file for LD1: per world, the decisions and the summed make-share probabilities under the
four score versions, and the stage counts of the tracked kinds. Written before data.

  python experiments/LD1_lookahead_diagnosis/recompute/build_ld1_counts.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
V = ("actual", "scale", "direction", "none")
rows = ["arm,seed,decisions," + ",".join(f"make_{v}" for v in V) + ",kinds," + ",".join(f"stage{k}" for k in range(6))]
for f in sorted(glob.glob(str(HERE.parent / "output" / "*_seed_*.json"))):
    r = json.load(open(f))
    s = r["sums"]
    rows.append(f"{r['arm']},{r['seed']},{int(s.get('decisions', 0))}," +
                ",".join(f"{s.get(f'sh_{v}_make', 0.0):.6f}" for v in V) + f",{r['n_kinds']}," +
                ",".join(str(r["stages"].get(str(k), 0)) for k in range(6)))
(HERE / "ld1_counts.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
