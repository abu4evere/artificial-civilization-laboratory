"""Builds the blind-recompute files for NB3 from the raw world files (written before data):
  nb3_worlds.csv  per arm and world: extinct, living_weeks (years 100-600), and the births of years 100-600 with a known
                  outcome and those who reached 16
  nb3_genes.csv   arm f, per world: mean g, E, G, L, A, C, H at years 1, 50, 100, 200, 300, 400, 500, 600
  nb3_garden.csv  phase 2 (if present): per arm and source world: founders, founders alive after a year, children with a
                  known outcome and those reaching 16

  python experiments/NB3_feelings/recompute/build_nb3_counts.py [phase1_dir phase2_dir]
"""
import glob
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
P1 = Path(sys.argv[1]) if len(sys.argv) > 2 else HERE.parent / "output"
P2 = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE.parent / "output_garden"
YEARS = (1, 50, 100, 200, 300, 400, 500, 600)
GENES = ("g", "E", "G", "L", "A", "C", "H")
w = ["arm,seed,extinct,living_weeks,known_births,reached16"]
gm = ["seed," + ",".join(f"{k}_year{y}" for k in GENES for y in YEARS)]
for f in sorted(glob.glob(str(P1 / "*_seed_*.json"))):
    r = json.load(open(f))
    k, re16 = r["late_births"]
    w.append(f"{r['arm']},{r['seed']},{int(r['extinct'])},{round(float(r['sums'].get('living_weeks', 0)), 3)},{k},{re16}")
    if r["arm"] == "f":
        by = {y["year"]: y for y in r["years"]}
        cells = []
        for k_ in GENES:
            for y in YEARS:
                v = by.get(y, {}).get(f"{k_}_mean")
                cells.append("" if v is None else str(round(v, 6)))
        gm.append(f"{r['seed']}," + ",".join(cells))
(HERE / "nb3_worlds.csv").write_text("\n".join(w) + "\n", encoding="utf-8")
(HERE / "nb3_genes.csv").write_text("\n".join(gm) + "\n", encoding="utf-8")
gd = ["arm,source_seed,founders,alive_1y,known,reached16"]
for f in sorted(glob.glob(str(P2 / "*_seed_*.json"))):
    r = json.load(open(f))
    if "skipped" in r:
        continue
    gd.append(f"{r['arm']},{r['source_seed']},{r['founders']},{r['alive_1y']},{r['known']},{r['reached16']}")
(HERE / "nb3_garden.csv").write_text("\n".join(gd) + "\n", encoding="utf-8")
print(len(w) - 1, "worlds;", len(gd) - 1, "garden worlds")
