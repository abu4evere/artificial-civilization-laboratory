"""Builds the blind-recompute file for HE1: per arm and world, the counts behind the harm guards and the co-primary.
Written before data.

  python experiments/HE1_habits_from_experience/recompute/build_he1_counts.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
rows = ["arm,seed,living_weeks,extinct,starvation_deaths,census_adults,census_health,m3_g_chains,m3_g_made,"
        "m3_m_chains,m3_m_made,makes,adult_weeks_win"]
for f in sorted(glob.glob(str(HERE.parent / "output" / "*_seed_*.json"))):
    r = json.load(open(f))
    s, h, p = r["am1"]["sums"], r["he1"], r["pb2"]
    rows.append(",".join(str(x) for x in (
        r["arm"], r["seed"], int(s.get("living_weeks", 0)), int(r["extinct"]), int(h.get("death_starvation", 0)),
        int(h.get("census_adults", 0)), round(h.get("census_health", 0.0), 3), int(s.get("m3_g_chains", 0)),
        int(s.get("m3_g_made", 0)), int(s.get("m3_m_chains", 0)), int(s.get("m3_m_made", 0)),
        int(p["actions"].get("make", 0)), int(p["sums"].get("adult_weeks_win", 0)))))
(HERE / "he1_counts.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
