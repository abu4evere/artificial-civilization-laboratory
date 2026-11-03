"""Builds the blind-recompute file for AM1: per arm and world, the chain counts behind M3 and M5 and the living weeks.
Written before data. (M1 is recomputed from c12-style held-out error sums written by the analysis, as in SC1.)

  python experiments/AM1_autonomy_measures/recompute/build_am1_counts.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
KEYS = ("m3_g_chains", "m3_g_made", "m3_m_chains", "m3_m_made", "m5_g_chains", "m5_g_made", "m5_m_chains", "m5_m_made",
        "living_weeks")
rows = ["arm,seed," + ",".join(KEYS) + ",extinct"]
for f in sorted(glob.glob(str(HERE.parent / "output" / "*_seed_*.json"))):
    r = json.load(open(f))
    rows.append(f"{r['arm']},{r['seed']}," + ",".join(str(int(r['sums'].get(k, 0))) for k in KEYS)
                + f",{int(r['extinct'])}")
(HERE / "am1_counts.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
