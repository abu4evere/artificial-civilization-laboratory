"""Builds AW1's one-file CSV for the blind recompute: raw per-world sums over census rows with year 100-199 (no ratio,
share or interval is computed here).   python experiments/AW1_watch_and_teach/recompute/build_one_file.py"""
import csv
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
FIELDS = ("makes", "adults", "living", "wb_craft_sum_20_40", "wb_adults_20_40")
with (HERE / "aw1_one_file.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(("seed", "arm", "field", "value"))
    for fp in sorted(glob.glob(str(HERE.parent / "output" / "*_seed_*.json"))):
        r = json.load(open(fp))
        idx = {k: r["census_fields"].index(k) for k in FIELDS}
        rows = [row for row in r["census"] if 100 <= row[0] < 200]
        for k in FIELDS:
            v = sum(row[idx[k]] for row in rows)
            w.writerow((r["seed"], r["arm"], f"{k}_years_100_199", round(v, 6) if isinstance(v, float) else v))
        w.writerow((r["seed"], r["arm"], "extinct_by_200", int(r["extinct"])))
print("written")
