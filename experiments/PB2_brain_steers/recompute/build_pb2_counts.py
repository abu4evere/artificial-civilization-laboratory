"""Builds the blind-recompute file for PB2: per arm and world, the chain counts behind M3, the living weeks and
extinction (the guards), and arm c's sums behind the validity check. Written before data.

  python experiments/PB2_brain_steers/recompute/build_pb2_counts.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
AM = ("m3_g_chains", "m3_g_made", "m3_m_chains", "m3_m_made", "living_weeks")
VD = ("se_rhat", "se_q", "n_scored")
rows = ["arm,seed," + ",".join(AM) + ",extinct," + ",".join(VD)]
for f in sorted(glob.glob(str(HERE.parent / "output" / "*_seed_*.json"))):
    r = json.load(open(f))
    v = r["pb2"]["valid"]
    vd = f"{v[0]:.6f},{v[1]:.6f},{int(v[2])}" if v is not None else ",,"
    rows.append(f"{r['arm']},{r['seed']}," + ",".join(str(int(r['am1']['sums'].get(k, 0))) for k in AM)
                + f",{int(r['extinct'])},{vd}")
(HERE / "pb2_counts.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
