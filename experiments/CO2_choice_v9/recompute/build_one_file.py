"""Builds CO2's one-file CSV for the blind recompute from the 32 output JSONs: raw sums only (no ratio, share,
weight or interval is computed here). Adults only.
  table q5: per seed, sums over late (years 100-200) offered weeks of the Q5 parts.
  table q2: per seed, period (early = years 0-10, late = years 100-200) and matched state, the summed counters.
python experiments/CO2_choice_v9/recompute/build_one_file.py"""
import csv
import glob
import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
EARLY, LATE = (0, 1), (5,)
with (HERE / "co2_one_file.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(("seed", "table", "period", "state", "field", "value"))
    for fp in sorted(glob.glob(str(HERE.parent / "output" / "*_seed_*.json"))):
        r = json.load(open(fp))
        q5 = Counter()
        q2 = defaultdict(Counter)
        for k, c in r["cells"].items():
            b, age, hb, tool, fb = k.split("|")
            if age != "adult":
                continue
            b = int(b)
            if b in LATE:
                q5.update({x: c.get(x, 0.0) for x in ("q5_n", "q5_gap", "q5_habit", "q5_curiosity", "q5_mult", "q5_built")})
            period = "early" if b in EARLY else "late" if b in LATE else None
            if period is None:
                continue
            st = f"{hb}-{tool}-{fb}"
            row = q2[(period, st)]
            row["offered"] += c.get("offered", 0)
            row["u_other"] += c.get("u_other", 0.0)
            row["spread"] += c.get("spread", 0.0)
            for kk, v in c.items():
                if ":" in kk:
                    fam, key = kk.split(":")
                    if key in ("sh", "sn", "sm"):
                        row[{"sh": "habit", "sn": "multiplicity", "sm": "per_entry"}[key]] += v
        for x, v in q5.items():
            w.writerow((r["seed"], "q5", "late", "all", x, round(v, 6)))
        for (period, st), row in sorted(q2.items()):
            for x in ("offered", "u_other", "habit", "multiplicity", "per_entry", "spread"):
                w.writerow((r["seed"], "q2", period, st, x, round(row[x], 6)))
print("written")
