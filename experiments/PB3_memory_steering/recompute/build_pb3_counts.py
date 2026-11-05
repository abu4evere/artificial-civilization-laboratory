"""Builds the blind-recompute file for PB3: per arm and world, the chain counts behind M3, the living weeks and
extinction. Written before data.

  python experiments/PB3_memory_steering/recompute/build_pb3_counts.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
AM = ("m3_g_chains", "m3_g_made", "m3_m_chains", "m3_m_made", "living_weeks")
rows = ["arm,seed," + ",".join(AM) + ",extinct"]
for f in sorted(glob.glob(str(HERE.parent / "output" / "*_seed_*.json"))):
    r = json.load(open(f))
    rows.append(f"{r['arm']},{r['seed']}," + ",".join(str(int(r['am1']['sums'].get(k, 0))) for k in AM)
                + f",{int(r['extinct'])}")
(HERE / "pb3_counts.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
