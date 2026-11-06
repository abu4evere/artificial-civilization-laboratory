"""Builds the blind-recompute file for VA1: one row per tracked kind. Written before data.

  python experiments/VA1_value_at_invention/recompute/build_va1_kinds.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
rows = ["seed,full,minval,vsim,vmean,used_before_loss,n_uses,first_felt,held_first_week"]
for f in sorted(glob.glob(str(HERE.parent / "output" / "c_seed_*.json"))):
    r = json.load(open(f))
    idx = {k: i for i, k in enumerate(r["kind_fields"])}
    for k in r["kinds"]:
        def v(name):
            x = k[idx[name]]
            return "" if x is None else (f"{x:.6f}" if isinstance(x, float) else str(x))
        rows.append(",".join([str(r["seed"])] + [v(n) for n in ("full", "minval", "vsim", "vmean", "used_before_loss",
                                                                 "n_uses", "first_felt", "held_first_week")]))
(HERE / "va1_kinds.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
