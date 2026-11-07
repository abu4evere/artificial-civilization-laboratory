"""SP1 blind recompute: the per-world count file (written before data). Independent of analyse_sp1.py: it reads the raw
world files and counts, per world, the invented kinds (origin made or heated) that reach each stage.

  python experiments/SP1_where_spreading_stops/recompute/build_sp1_counts.py [<output dir>]  -> sp1_counts.csv
"""
import csv
import glob
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
src = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "output"
SOCIAL = ("taught", "copied", "read")
COLS = ("seed", "born", "offered", "shown", "learned_taught", "learned_social", "learner_had_parts",
        "made_by_learner", "lessons_shown", "lessons_declined", "lessons_missing_part", "lessons_taken")
rows = []
for f in sorted(glob.glob(str(src / "c_seed_*.json"))):
    d = json.loads(Path(f).read_text(encoding="utf-8"))
    r = dict.fromkeys(COLS, 0)
    r["seed"] = d["seed"]
    for k in d["kinds"].values():
        if k["origin"] not in ("made", "heated"):
            continue
        raw, lr = k["raw"], k["learned"]
        r["born"] += 1
        r["offered"] += (raw.get("offered_inv", 0) + raw.get("offered_oth", 0)) > 0
        r["shown"] += raw.get("top_shown", 0) > 0
        r["learned_taught"] += lr.get("taught", 0) > 0
        r["learned_social"] += sum(lr.get(h, 0) for h in SOCIAL) > 0
        r["learner_had_parts"] += k["w"].get("lrn_canmake", 0) > 0
        r["made_by_learner"] += sum(k["made_other"].get(h, 0) for h in SOCIAL) > 0
        r["lessons_shown"] += raw.get("top_shown", 0)
        r["lessons_declined"] += raw.get("top_declined", 0)
        r["lessons_missing_part"] += raw.get("top_missing_part", 0)
        r["lessons_taken"] += raw.get("top_taken", 0)
    rows.append({k: int(v) for k, v in r.items()})
with open(HERE / "sp1_counts.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=COLS)
    w.writeheader()
    w.writerows(rows)
print(f"{len(rows)} worlds -> {HERE / 'sp1_counts.csv'}")
