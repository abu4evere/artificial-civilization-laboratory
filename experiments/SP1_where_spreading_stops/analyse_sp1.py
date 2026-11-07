"""SP1 analysis, written before any data (questions.md, frozen as `SP1-frozen`).

  python experiments/SP1_where_spreading_stops/analyse_sp1.py                      # writes results.md
  python experiments/SP1_where_spreading_stops/analyse_sp1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_sp1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261107)
INVENTED = ("made", "heated")
SOCIAL = ("taught", "copied", "read")
STAGES = ("A", "B", "C", "Dt", "Dany", "Dcopied", "E", "F", "Fany")
STEPS = (("B|A", "B", "A"), ("C|B", "C", "B"), ("D-taught|C", "Dt", "C"), ("E|D-any", "E", "Dany"),
         ("F|E", "F", "E"))
OUTCOMES = ("known", "distrust", "declined", "missing_part", "taken", "taken_wrong")


def stages(k):
    raw, w, lr, mo = k["raw"], k["w"], k["learned"], k["made_other"]
    return {"A": 1,
            "B": int(raw.get("offered_inv", 0) + raw.get("offered_oth", 0) > 0),
            "C": int(raw.get("top_shown", 0) > 0),
            "Dt": int(lr.get("taught", 0) > 0),
            "Dany": int(sum(lr.get(h, 0) for h in SOCIAL) > 0),
            "Dcopied": int(lr.get("copied", 0) > 0),
            "E": int(w.get("lrn_canmake", 0) > 0),
            "F": int(sum(mo.get(h, 0) for h in SOCIAL) > 0),
            "Fany": int(sum(mo.values()) > 0)}


def load():
    files = sorted(glob.glob(str(OUTDIR / "c_seed_*.json")))
    worlds = [json.loads(Path(f).read_text(encoding="utf-8")) for f in files]
    return worlds


def per_world(worlds):
    rows = []
    for d in worlds:
        c = Counter()
        sec = Counter()
        for k in d["kinds"].values():
            if k["origin"] not in INVENTED:
                c["copy_error_kinds"] += 1
                continue
            for s, v in stages(k).items():
                c[s] += v
            raw, w = k["raw"], k["w"]
            for o in OUTCOMES:
                sec[f"top_{o}"] += raw.get(f"top_{o}", 0)
            sec["top_shown"] += raw.get("top_shown", 0)
            sec["inv_taught_while_knowing"] += int(raw.get("occ_inv", 0) > 0)
            sec["inv_val15"] += int(w.get("inv_val15", 0) > 0)
            sec["inv_made_again"] += int(w.get("inv_makes", 0) > 0)
            for key in ("oth_weeks", "oth_val05", "oth_canmake", "lrn_weeks", "lrn_canmake", "oth_make_top4",
                        "oth_chose_make", "inv_weeks", "inv_val05", "inv_canmake"):
                sec[key] += w.get(key, 0)
            sec["own_or_heated_other"] += int(k["learned"].get("own", 0) + k["learned"].get("heated", 0) > 0)
            sec["lost"] += int(k["lost"] is not None)
        rows.append({"seed": d["seed"], "extinct": d["extinct"], **{s: c[s] for s in STAGES},
                     "copy_error_kinds": c["copy_error_kinds"], **sec})
    return rows


def ratio_ci(rows, num, den):
    n = np.array([r[num] for r in rows], float)
    m = np.array([r[den] for r in rows], float)
    pt = n.sum() / m.sum() if m.sum() else float("nan")
    idx = RNG.integers(0, len(rows), size=(REPS, len(rows)))
    ns, ms = n[idx].sum(1), m[idx].sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        bs = np.where(ms > 0, ns / np.where(ms > 0, ms, 1), np.nan)
    lo, hi = np.nanpercentile(bs, [2.5, 97.5]) if np.isfinite(bs).any() else (float("nan"), float("nan"))
    return pt, lo, hi


def main():
    worlds = load()
    rows = per_world(worlds)
    fps = {d["code_hash"] for d in worlds} | {d["code_hash_after"] for d in worlds}
    checks = Counter()
    for d in worlds:
        for k, v in d["check"].items():
            checks[k] += v
    L = ["# SP1 results (written by analyse_sp1.py; numbers from the raw output files)", ""]
    if SMOKE:
        L += ["**SMOKE: a code test of the analysis, not data.**", ""]
    L += [f"Worlds: {len(worlds)} (expected {len(R.SEEDS)}); extinct: {sum(r['extinct'] for r in rows)}; "
          f"fingerprints: {sorted(fps)}",
          f"Run checks pooled: {dict(checks)}", ""]
    tot = {s: sum(r[s] for r in rows) for s in STAGES}
    L += ["## The funnel (invented kinds, born in years 100-190; each kind counted once per stage)", ""]
    names = {"A": "born", "B": "offered at least once", "C": "shown at least once",
             "Dt": "learned by a non-inventor through a lesson", "Dany": "learned by a non-inventor by any social route",
             "Dcopied": "learned by watching", "E": "a learner had the parts in hand in some week",
             "F": "made by a non-inventor who learned it", "Fany": "made by any non-inventor (any route, incl. own)"}
    for s in STAGES:
        L.append(f"- {s} ({names[s]}): {tot[s]}")
    L += [f"- copy-error kinds (reported apart): {sum(r['copy_error_kinds'] for r in rows)}", "",
          "## Primary: conditional pass rate at each step (pooled; world bootstrap 95%, 10,000 draws)", ""]
    res = []
    for name, num, den in STEPS:
        pt, lo, hi = ratio_ci(rows, num, den)
        res.append((name, pt, lo, hi))
        L.append(f"- {name}: {pt:.4f} [{lo:.4f}, {hi:.4f}] ({tot[num]} of {tot[den]})")
    valid = sorted([x for x in res if np.isfinite(x[1])], key=lambda x: x[1])
    if valid:
        low = valid[0]
        tied = [x[0] for x in valid[1:] if np.isfinite(x[2]) and x[2] <= low[3]]
        L += ["", f"**Lowest step (frozen rule): {low[0]}** = {low[1]:.4f} [{low[2]:.4f}, {low[3]:.4f}]"
              + (f"; its interval overlaps: {', '.join(tied)}" if tied else "; no other step's interval overlaps it")]
    L += ["", "## Secondary", ""]
    sec = {k: sum(r[k] for r in rows) for k in rows[0] if k not in ("seed", "extinct")} if rows else {}
    shown = sec.get("top_shown", 0)
    L.append(f"- Lesson outcomes (top-level lessons of invented kinds, n = {shown}): "
             + "; ".join(f"{o} {sec.get('top_' + o, 0)} ({sec.get('top_' + o, 0) / shown:.3f})" if shown else o
                         for o in OUTCOMES))
    for label, num, den in (("D-copied | A", "Dcopied", "A"), ("D-any | A", "Dany", "A"), ("F-any | A", "Fany", "A"),
                            ("inventor ever teaches while knowing K | A", "inv_taught_while_knowing", "A"),
                            ("inventor's value for K ever > 0.15 | A", "inv_val15", "A"),
                            ("inventor made K again | A", "inv_made_again", "A"),
                            ("a non-inventor got K on their own (own or heated) | A", "own_or_heated_other", "A"),
                            ("lost by year 200 | A", "lost", "A"),
                            ("learner-weeks with the parts in hand", "lrn_canmake", "lrn_weeks"),
                            ("non-inventor knower-weeks with value > 0.05", "oth_val05", "oth_weeks"),
                            ("non-inventor knower-weeks with the parts in hand", "oth_canmake", "oth_weeks"),
                            ("non-inventor knower-weeks with make K in the top 4 options", "oth_make_top4", "oth_weeks"),
                            ("non-inventor knower-weeks choosing to make K", "oth_chose_make", "oth_weeks"),
                            ("inventor knower-weeks with value > 0.05", "inv_val05", "inv_weeks"),
                            ("inventor knower-weeks with the parts in hand", "inv_canmake", "inv_weeks")):
        pt, lo, hi = ratio_ci(rows, num, den)
        L.append(f"- {label}: {pt:.4f} [{lo:.4f}, {hi:.4f}] ({sec.get(num, 0)} of {sec.get(den, 0)})")
    L += ["", "## Per world (kinds per stage)", "",
          "seed | " + " | ".join(STAGES), "|".join(["---"] * (len(STAGES) + 1))]
    for r in rows:
        L.append(f"{r['seed']} | " + " | ".join(str(r[s]) for s in STAGES))
    text = "\n".join(L) + "\n"
    out = (OUTDIR / "results_smoke.md") if SMOKE else (HERE / "results.md")
    out.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
