"""Builds the blind-recompute files for NB1 from the raw world files (written before data):
  nb1_worlds.csv  per arm and world: extinct and the guard sums (years 100-600)
  nb1_gens.csv    per arm, world and generation: births with a known outcome, reached 16, grown deaths, their summed ages
  nb1_g.csv       per arm and world: mean g at years 1, 50, 100, 200, 300, 400, 500, 600 (n and e)
  nb1_garden.csv  phase 2 (if present): per arm and source world: births with a known outcome and those reaching 16

  python experiments/NB1_neural_brain/recompute/build_nb1_counts.py [phase1_dir phase2_dir]
"""
import glob
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
P1 = Path(sys.argv[1]) if len(sys.argv) > 2 else HERE.parent / "output"
P2 = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE.parent / "output_garden"
SUMS = ("living_weeks", "death_starvation", "death_killed", "census_adults", "census_health", "child_weeks",
        "child_deaths", "child_death_starvation", "adult_weeks", "gifts_kin_children")
YEARS = (1, 50, 100, 200, 300, 400, 500, 600)
w = ["arm,seed,extinct," + ",".join(SUMS)]
g = ["arm,seed,generation,known,reached16,adult_deaths,sum_adult_age_years"]
gm = ["arm,seed," + ",".join(f"g_year{y}" for y in YEARS)]
for f in sorted(glob.glob(str(P1 / "*_seed_*.json"))):
    r = json.load(open(f))
    s = r["sums"]
    w.append(f"{r['arm']},{r['seed']},{int(r['extinct'])}," + ",".join(str(round(float(s.get(k, 0)), 3)) for k in SUMS))
    for gen, row in sorted(r["gens"].items(), key=lambda kv: int(kv[0])):
        g.append(f"{r['arm']},{r['seed']},{gen},{row[0]},{row[1]},{row[2]},{round(row[3], 4)}")
    if r["arm"] in ("n", "e"):
        by = {y["year"]: y.get("g_mean") for y in r["years"]}
        gm.append(f"{r['arm']},{r['seed']}," + ",".join("" if by.get(y) is None else str(round(by[y], 6)) for y in YEARS))
(HERE / "nb1_worlds.csv").write_text("\n".join(w) + "\n", encoding="utf-8")
(HERE / "nb1_gens.csv").write_text("\n".join(g) + "\n", encoding="utf-8")
(HERE / "nb1_g.csv").write_text("\n".join(gm) + "\n", encoding="utf-8")
gd = ["arm,source_seed,known,reached16,founder_weeks,births"]
for f in sorted(glob.glob(str(P2 / "*_seed_*.json"))):
    r = json.load(open(f))
    if "skipped" in r:
        continue
    gd.append(f"{r['arm']},{r['source_seed']},{r['known']},{r['reached16']},{r['founder_weeks']},{r['births']}")
(HERE / "nb1_garden.csv").write_text("\n".join(gd) + "\n", encoding="utf-8")
print(len(w) - 1, "worlds;", len(g) - 1, "generation rows;", len(gd) - 1, "garden worlds")
