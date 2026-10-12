"""WS1, descriptive and NOT pre-registered: median population at each decade mark, per arm, all worlds and surviving
worlds; and, for each arm, the share of worlds still declining over the last 30 years. Reads saved outputs only.

  python experiments/S1_world_size/trajectories.py
"""
import json
import statistics as st
from pathlib import Path

OUT = Path(__file__).with_name("output")
ARMS = {"c": "C (40x40, 20)", "l": "L (80x80, 20)", "lp": "LP (80x80, 80)", "p": "P (40x40, 80)", "s": "S sham"}


def pops(arm):
    rows = []
    for f in sorted(OUT.glob(f"{arm}_seed_*.json")):
        p = json.loads(f.read_text(encoding="utf-8"))["pops"]
        rows.append(p + [0] * (12 - len(p)))
    return rows


print("median population at decade marks (years 9, 19, ... 119); all worlds | surviving worlds")
for a, name in ARMS.items():
    rows = pops(a)
    alive = [r for r in rows if r[-1] > 0]
    allm = [int(st.median(r[i] for r in rows)) for i in range(12)]
    alm = [int(st.median(r[i] for r in alive)) for i in range(12)] if alive else []
    falling = sum(1 for r in alive if r[-1] < r[-4]) / len(alive) if alive else float("nan")
    print(f"{name:16s} all  {allm}")
    print(f"{'':16s} live {alm}   (n={len(alive)}; share of survivors smaller at 119 than at 89: {falling:.2f})")
