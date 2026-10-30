"""Builds the one-file CSV for LS2's blind recompute (Q1 dominant channels, Q3 decomposition, Q5 inheritance) from the
raw output JSONs. It only sums raw counters per world; it computes no ratio, share or interval (those are the
recomputers' job). Written before LS2's data arrived.

  python experiments/LS2_knowledge_v9/recompute/build_one_file.py [--dir <output folder>] [--out <csv>]
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
STUDY = HERE.parent
sys.path.insert(0, str(STUDY))
from run_ls2 import BIN_EDGES, WPY  # noqa: E402

OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else STUDY / "output"
CSV = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else HERE / "ls2_one_file.csv"
OUT_CH = ("pushout", "useless", "death")
ADULT = ("16-29", "30-49", "50+")
AFTER100 = [i for i in range(len(BIN_EDGES) - 1) if BIN_EDGES[i] >= 100]
EARLY, LATE = (0, 1), (BIN_EDGES.index(100),)          # years 0-10 (bins 0-5, 5-10) and years 100-200


def binv(r, i, key):
    return r["bins"].get(str(i), {}).get(key, 0)


def rows_for(r):
    s = r["seed"]
    out = [(s, "final_week", r["final_tick"])]
    for c in OUT_CH:
        out.append((s, f"copy_loss_{c}_after_year_100", sum(binv(r, i, "out_" + c) for i in AFTER100)))
        out.append((s, f"kind_extinction_{c}_after_year_100", sum(binv(r, i, "ext_" + c) for i in AFTER100)))
    for name, bins_ in (("years_0_10", EARLY), ("years_100_200", LATE)):
        for k in ("pw", "feasible", "weighed", "chosen"):
            out.append((s, f"adult_{k}_{name}", sum(binv(r, i, f"{k}_{a}") for i in bins_ for a in ADULT)))
    for lo in range(0, 1000, 50):
        ppl = [p for p in r["people"] if not p[3] and lo * WPY <= p[1] < (lo + 50) * WPY and p[12] is not None]
        out.append((s, f"people_born_{lo}_{lo + 50}", len(ppl)))
        out.append((s, f"inherited_born_{lo}_{lo + 50}", sum(p[12][0] for p in ppl)))
        out.append((s, f"inheritable_born_{lo}_{lo + 50}", sum(p[12][1] for p in ppl)))
    return out


def main():
    files = sorted(OUTDIR.glob("lp_seed_*.json"))
    with CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(("seed", "field", "value"))
        for fp in files:
            for s, k, v in rows_for(json.loads(fp.read_text(encoding="utf-8"))):
                w.writerow((s, k, round(v, 6) if isinstance(v, float) else v))
    print(f"{len(files)} worlds -> {CSV}")


if __name__ == "__main__":
    main()
