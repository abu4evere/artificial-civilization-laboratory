"""Builds the blind-recompute file for PB0 (written before any data): one row per studied option of every sampled
decision, with its outcome at H = 4 on each of the four replays (reward + mood parts summed), its score and whether it is
the top-scored option. The recompute picks the winner itself (replays 1-2) and measures the held-out gain (replays 3-4).

  python experiments/PB0_prediction_audit/recompute/build_pb0_outcomes.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
rows = ["seed,decision,option,score,is_top,r1,r2,r3,r4"]
for f in sorted(glob.glob(str(HERE.parent / "output" / "c_seed_*.json"))):
    r = json.load(open(f))
    for d in r["decisions"]:
        if d.get("skipped"):
            continue
        for k, v in sorted(d["outcomes"].items(), key=lambda kv: int(kv[0])):
            marks = [rp.get("4") for rp in v["replays"]]
            if any(m is None for m in marks):
                continue
            tot = [round(m[0] + m[1], 5) for m in marks]
            rows.append(f"{r['seed']},{d['dn']},{k},{d['options'][int(k)][0]},{int(int(k) == d['top'])},"
                        + ",".join(str(x) for x in tot))
(HERE / "pb0_outcomes.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
