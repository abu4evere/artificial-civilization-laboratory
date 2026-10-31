"""Builds AG1's one-file CSV for the blind recompute from the 80 output JSONs: raw per-world counts only (no rate,
distance, share or interval is computed here).
  deaths_<band>: deaths at ages in the band, years 100-999; pyears_<band>: person-years lived in the band, years 100-999
  (person-weeks / 52, from the centuries 1-9); extinct; living_py_800_999 (sum of the yearly census 'living').
python experiments/AG1_ageing_anchor/recompute/build_one_file.py"""
import csv
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
BANDS = ((30, 45), (45, 60), (60, 70))
with (HERE / "ag1_one_file.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(("seed", "arm", "field", "value"))
    for fp in sorted(glob.glob(str(HERE.parent / "output" / "*_seed_*.json"))):
        r = json.load(open(fp))
        bands = [tuple(b) for b in r["bands"]]
        for lo, hi in BANDS:
            d = sum(1 for t, age, cause, gen in r["deaths"] if 100 * 52 <= t < 1000 * 52 and age is not None and lo <= age < hi)
            bi = bands.index((lo, hi))
            py = sum(v[bi] for c, v in r["person_weeks"].items() if 1 <= int(c) <= 9) / 52
            w.writerow((r["seed"], r["arm"], f"deaths_{lo}_{hi}", d))
            w.writerow((r["seed"], r["arm"], f"pyears_{lo}_{hi}", round(py, 4)))
        w.writerow((r["seed"], r["arm"], "extinct", int(r["extinct"])))
        i = r["census_fields"].index("living")
        w.writerow((r["seed"], r["arm"], "living_py_800_999", sum(row[i] for row in r["census"] if 800 <= row[0] < 1000)))
print("written")
