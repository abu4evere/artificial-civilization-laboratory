"""Builds the blind-recompute files for NB2 from the raw world files (written before data):
  nb2_worlds.csv  per arm and world: extinct, living_weeks (years 100-600), and the births of years 100-600 with a known
                  outcome and those who reached 16
  nb2_g.csv       per arm and world: mean g at years 1, 50, 100, 200, 300, 400, 500, 600 (arms s, o, l, n)
  nb2_garden.csv  phase 2 (if present): per arm and source world: children with a known outcome and those reaching 16

  python experiments/NB2_connected_brain/recompute/build_nb2_counts.py [phase1_dir phase2_dir]
"""
import glob
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
P1 = Path(sys.argv[1]) if len(sys.argv) > 2 else HERE.parent / "output"
P2 = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE.parent / "output_garden"
YEARS = (1, 50, 100, 200, 300, 400, 500, 600)
w = ["arm,seed,extinct,living_weeks,known_births,reached16"]
gm = ["arm,seed," + ",".join(f"g_year{y}" for y in YEARS)]
for f in sorted(glob.glob(str(P1 / "*_seed_*.json"))):
    r = json.load(open(f))
    k, re16 = r["late_births"]
    w.append(f"{r['arm']},{r['seed']},{int(r['extinct'])},{round(float(r['sums'].get('living_weeks', 0)), 3)},{k},{re16}")
    if r["arm"] != "c":
        by = {y["year"]: y.get("g_mean") for y in r["years"]}
        gm.append(f"{r['arm']},{r['seed']}," + ",".join("" if by.get(y) is None else str(round(by[y], 6)) for y in YEARS))
(HERE / "nb2_worlds.csv").write_text("\n".join(w) + "\n", encoding="utf-8")
(HERE / "nb2_g.csv").write_text("\n".join(gm) + "\n", encoding="utf-8")
gd = ["arm,source_seed,known,reached16"]
for f in sorted(glob.glob(str(P2 / "*_seed_*.json"))):
    r = json.load(open(f))
    if "skipped" in r:
        continue
    gd.append(f"{r['arm']},{r['source_seed']},{r['known']},{r['reached16']}")
(HERE / "nb2_garden.csv").write_text("\n".join(gd) + "\n", encoding="utf-8")
print(len(w) - 1, "worlds;", len(gd) - 1, "garden worlds")
