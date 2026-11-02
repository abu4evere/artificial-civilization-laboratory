"""SC1 follow-up, exploratory (outside any frozen plan): the C3 puzzle. SC1 found experienced habits (k 80+) have a
larger absolute error |q - G| than new ones (k 0-19). UV1's existing outputs (ES2's v11 arm, 32 worlds, years 100-200)
hold, by k bin and age bin, the sums of (q - G) and |q - G| for updates whose G was not closed by death. This reads
them for ages 16-44: if the signed bias shrinks with k while the absolute error grows, experience removes bias but
widens the spread around what follows. Read-only; no new run.

  python experiments/SC1_bob_scorecard/explore/c3_from_uv1.py
"""
import glob
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
UV1 = HERE.parent.parent / "UV1_undervaluation_by_experience" / "output"
agg = defaultdict(lambda: [0, 0.0, 0.0])
worlds = 0
for f in sorted(glob.glob(str(UV1 / "c_seed_*.json"))):
    r = json.load(open(f))
    worlds += 1
    for key, (n, ss, sa) in r["uv"].items():
        kb, ab, crisis, act, cens = key.split("|")
        if cens != "0" or ab not in ("16-29", "30-44"):
            continue
        a = agg[kb]
        a[0] += n
        a[1] += ss
        a[2] += sa
out = {"worlds": worlds, "by_k": {}}
for kb in ("0-9", "10-19", "20-39", "40-79", "80-159", "160+"):
    n, ss, sa = agg[kb]
    if n:
        out["by_k"][kb] = {"n": n, "mean_signed": round(ss / n, 4), "mean_abs": round(sa / n, 4)}
(HERE / "c3_from_uv1.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out, indent=1))
