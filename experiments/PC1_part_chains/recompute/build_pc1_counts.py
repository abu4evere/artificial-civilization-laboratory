"""Builds the blind-recompute file for PC1: per-world counts, counted here independently of analyse_pc1.py, straight
from the raw world files. Written before data.

  python experiments/PC1_part_chains/recompute/build_pc1_counts.py
"""
import glob
import json
from pathlib import Path

HERE = Path(__file__).parent
COLS = ("kinds", "depth0", "depth1", "depth2", "depth3", "failed", "miss1", "miss2", "miss3", "deep1", "deep2", "deep3",
        "tk_all", "tk_some", "tk_none", "part_shown", "part_knew", "part_declined", "part_missing_part", "part_taken",
        "part_distrust", "part_was_missing", "pairs", "got_part", "got_K", "made_K")
rows = ["seed," + ",".join(COLS)]
for f in sorted(glob.glob(str(HERE.parent / "output" / "c_seed_*.json"))):
    r = json.load(open(f))
    c = dict.fromkeys(COLS, 0)
    c["kinds"] = len(r["kinds"])
    for kind in r["kinds"]:
        depth = kind[1]
        c["depth3" if depth >= 3 else f"depth{depth}"] += 1
    c["failed"] = len(r["rows"])
    for n_missing, n_teacher, _all, _alive, deepest, shown, outcome, was_missing in r["rows"]:
        c["miss3" if n_missing >= 3 else f"miss{n_missing}"] += 1
        c["deep3" if deepest >= 3 else f"deep{deepest}"] += 1
        if n_missing > 0 and n_teacher == n_missing:
            c["tk_all"] += 1
        elif n_teacher == 0:
            c["tk_none"] += 1
        else:
            c["tk_some"] += 1
        if shown:
            c["part_shown"] += 1
            c["part_" + outcome] += 1
            c["part_was_missing"] += was_missing
    for k in ("pairs", "got_part", "got_K", "made_K"):
        c[k] = r["later"].get(k, 0)
    rows.append(f"{r['seed']}," + ",".join(str(int(c[k])) for k in COLS))
(HERE / "pc1_counts.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(len(rows) - 1, "rows")
