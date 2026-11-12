"""NB3-A analysis (questions.md, NB3A-frozen). Written before data. Descriptive: the six starvation patterns in f
against c, fH and f's matched survivors; each pattern as deaths per 1,000 living-years; the food economy per
adult-week. World bootstrap, 10,000 draws, NumPy seed 20261114, paired by seed.

  python experiments/NB3A_feeding_autopsy/analyse_nb3a.py [--dir OUT]
"""
from __future__ import annotations

import glob
import itertools
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
ARMS = ("c", "fH", "f")
SEEDS = list(range(25801, 25817))
REPS = 10_000
RNG = np.random.default_rng(20261114)
WPY = 52
PATTERNS = ("cannot_find", "does_not_try", "not_shared", "caregiver_short", "no_caregiver", "hard_times")
LABEL = {"cannot_find": "cannot find", "does_not_try": "does not try", "not_shared": "not shared",
         "caregiver_short": "caregiver short", "no_caregiver": "no caregiver", "hard_times": "hard times"}


def patterns(hist, row, age_group, window=8):
    """The frozen patterns for one person's history (the weeks before death, oldest first)."""
    last = hist[-window:]
    early = hist[-window:-2] if len(hist) > 2 else []
    out = dict.fromkeys(PATTERNS, False)
    chosen = [h for h in early if h["food_chosen"]]
    if chosen:
        out["cannot_find"] = sum(1 for h in chosen if h["gained"] > 0) < 0.5 * len(chosen)
    if early:
        offered = sum(1 for h in early if h["food_offered"]) > 0.5 * len(early)
        able = min(h["health"] for h in early) >= 30
        out["does_not_try"] = offered and able and len(chosen) < 0.25 * len(early)
    out["not_shared"] = sum(1 for h in last if h["kin_rich"]) >= 2
    if age_group == "u12":
        short = sum(1 for h in last if h.get("cg", {}).get("alive") and
                    h["cg"]["held"] < h["cg"]["need"] + h.get("want", 0.0))
        gone = sum(1 for h in last if "cg" in h and not h["cg"]["alive"])
        out["caregiver_short"] = short >= 2
        out["no_caregiver"] = gone >= 2
    out["hard_times"] = (row["wet"] is not None and row["wet"] < 0.65) or (row["hard"] is not None and
                                                                        row["hard"] > 0.1) or row["weather"] < 0.80
    return out


CORR1 = "--correction1" in sys.argv
NB3_OUT = HERE.parent / "NB3_feelings" / "output"


def same_history(a, s, r):
    """Correction 1: the replay's living-weeks and deaths by cause (years 100-600) and final week equal NB3's."""
    o = json.loads((NB3_OUT / f"{a}_seed_{s}.json").read_text())
    lw = sum(v.get("living_weeks", 0) for d, v in r["decades"].items() if 10 <= int(d) < 60)
    dr = {}
    for d, v in r["decades"].items():
        if 10 <= int(d) < 60:
            for k, c in v.items():
                if k.startswith("death:"):
                    dr[k.split(":")[1]] = dr.get(k.split(":")[1], 0) + c
    od = {k[6:]: v for k, v in o["sums"].items() if k.startswith("death_") and not k.startswith("death_?")}
    return (lw == o["sums"].get("living_weeks", 0) and all(dr.get(k, 0) == v for k, v in od.items())
            and r["final_tick"] == o["final_tick"])


def pct(x):
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    return (float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))) if len(x) else (float("nan"),) * 2


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {a: {} for a in ARMS}
    for f in sorted(glob.glob(str(OUTDIR / "*_seed_*.json"))):
        r = json.load(open(f))
        if r["arm"] in runs:
            runs[r["arm"]][r["seed"]] = r
    present = all(sorted(runs[a]) == SEEDS for a in ARMS)
    differ = [(a, s) for a in ARMS for s, r in runs[a].items() if not r["same_as_nb3"]]
    if CORR1:                                   # Correction 1 (questions.md): read replays whose history matches NB3's
        differ = [(a, s) for a in ARMS for s, r in runs[a].items() if not same_history(a, s, r)]
    zero = (HERE / "zero_local.log").read_text(encoding="utf-8") if (HERE / "zero_local.log").exists() else ""
    valid = present and len(differ) <= 4 and "All: PASS" in zero
    L = ["# NB3-A: why do the feeling people starve? (results)", "",
         "Frozen as `NB3A-frozen`. run_nb3a.py, analyse_nb3a.py (written before data).",
         *(["", "**Correction 1** (questions.md, after the data): replays are read if their history matches NB3's "
            "exactly; the frozen fingerprint rule failed (`results_frozen_rule.md`)."] if CORR1 else []),
         "", "## Validity", "",
         f"- Read-only check (zero_local.log, All: PASS): **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All 48 replays present: **{'yes' if present else 'NO'}**",
         f"- Replays {'with NB3' + chr(39) + 's exact history (Correction 1)' if CORR1 else 'ending with NB3' + chr(39) + 's fingerprint'}: {48 - len(differ)} of 48; differing (reported beside, not read): "
         f"{', '.join(f'{a}:{s}' for a, s in differ) or 'none'}",
         f"- **{'Valid.' if valid else 'NOT VALID: nothing is concluded (more than 4 differ, or missing).'}**", ""]
    if not valid:
        print("\n".join(L))
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        return
    read = {a: {s: r for s, r in runs[a].items() if (same_history(a, s, r) if CORR1 else r["same_as_nb3"])}
            for a in ARMS}
    L.append("Worlds read: " + ", ".join(f"{a} {len(read[a])}" for a in ARMS) + ".")
    checks = sum(r["checks"].get("held_but_did_not_eat", 0) for a in ARMS for r in read[a].values())
    L += [f"Code check, 'held food but did not eat' weeks: {checks} (expected 0).", ""]

    # patterns per death and per survivor
    def classify(a, window=8):
        deaths, survs = {}, {}
        for s, r in read[a].items():
            ds, ss = [], []
            for row in r["starved"]:
                ds.append(patterns(row["hist"], row, row["age_group"], window))
            for sv in r["survivors"]:
                if sv["found"] and sv["hist"]:
                    row = r["starved"][sv["death_idx"]]
                    ss.append(patterns(sv["hist"], row, row["age_group"], window))
            deaths[s], survs[s] = ds, ss
        return deaths, survs

    def share(by_seed, p):
        rows = [x for v in by_seed.values() for x in v]
        return (sum(1 for x in rows if x[p]) / len(rows)) if rows else float("nan"), len(rows)

    for window in (8, 24):
        cls = {a: classify(a, window) for a in ARMS}
        title = "frozen, last 8 weeks" if window == 8 else "sensitivity, last 24 weeks"
        L += [f"## The six patterns ({title})", "",
              "| pattern | f deaths | f survivors | fH deaths | c deaths | f/c | f/survivors | leads |",
              "|---|---|---|---|---|---|---|---|"]
        for p in PATTERNS:
            sf, nf = share(cls["f"][0], p)
            sv, nv = share(cls["f"][1], p)
            sh, nh = share(cls["fH"][0], p)
            sc, nc = share(cls["c"][0], p)
            r_c = sf / sc if sc > 0 else (float("inf") if sf > 0 else float("nan"))
            r_s = sf / sv if sv > 0 else (float("inf") if sf > 0 else float("nan"))
            leads = sf >= 0.25 and r_c >= 1.5 and r_s >= 1.5
            L.append(f"| {LABEL[p]} | {sf:.3f} (n {nf}) | {sv:.3f} (n {nv}) | {sh:.3f} (n {nh}) | {sc:.3f} (n {nc}) | "
                     f"{r_c:.2f} | {r_s:.2f} | {'**yes**' if (leads and window == 8) else ('yes' if leads else 'no')} |")
        if window == 8:
            rows = [x for v in cls["f"][0].values() for x in v]
            L += ["", "Overlaps among f's starvation deaths (both patterns):", ""]
            for p, q in itertools.combinations(PATTERNS, 2):
                n = sum(1 for x in rows if x[p] and x[q])
                if n:
                    L.append(f"- {LABEL[p]} + {LABEL[q]}: {n}")
            none = sum(1 for x in rows if not any(x.values()))
            L.append(f"- none of the six: {none} of {len(rows)}")
            # deaths per 1,000 living-years, f against c and fH, paired by seed
            L += ["", "## Each pattern as deaths per 1,000 living-years (paired seed bootstrap)", "",
                  "| pattern | f | fH | c | f/c [95%] | f/fH [95%] |", "|---|---|---|---|---|---|"]
            for p in ("all",) + PATTERNS:
                def counts(a, seeds):
                    num = np.array([sum(1 for x in cls[a][0][s] if p == "all" or x[p]) for s in seeds], float)
                    den = np.array([sum(v.get("living_weeks", 0) for v in read[a][s]["decades"].values()) / WPY
                                    for s in seeds], float)
                    return num, den
                cells, cis = {}, {}
                for a in ARMS:
                    n_, d_ = counts(a, sorted(read[a]))
                    cells[a] = 1000 * n_.sum() / d_.sum() if d_.sum() else float("nan")
                for b in ("c", "fH"):
                    seeds = sorted(set(read["f"]) & set(read[b]))
                    nf_, df_ = counts("f", seeds)
                    nb_, db_ = counts(b, seeds)
                    k = len(seeds)
                    W = np.stack([np.bincount(row, minlength=k) for row in RNG.integers(0, k, size=(REPS, k))]).astype(float)
                    with np.errstate(invalid="ignore", divide="ignore"):
                        rr = ((W @ nf_) / (W @ df_)) / ((W @ nb_) / (W @ db_))
                    cis[b] = pct(rr)
                lab = "all starvation" if p == "all" else LABEL[p]
                L.append(f"| {lab} | {cells['f']:.3f} | {cells['fH']:.3f} | {cells['c']:.3f} | "
                         f"{cells['f'] / cells['c']:.2f} [{cis['c'][0]:.2f}, {cis['c'][1]:.2f}] | "
                         f"{cells['f'] / cells['fH']:.2f} [{cis['fH'][0]:.2f}, {cis['fH'][1]:.2f}] |")
        L.append("")
    L += ["Rule (frozen): a pattern leads if, among f's starvation deaths, its share is at least 25%, at least 1.5 times "
          "c's share and at least 1.5 times its share among f's matched survivors.", ""]

    # the food economy per adult-week, years 100-600 (decades 10-59)
    keys = ["gained:forage", "gained:hunt", "gained:take", "eaten", "fed_to_dependents", "given:own_child",
            "given:kin", "given:other", "stored", "spoiled"]
    L += ["## The food economy per adult-week (years 100-600; paired seed bootstrap of f/c)", "",
          "| measure | f | fH | c | f/c [95%] |", "|---|---|---|---|---|"]
    for key in keys:
        def tot(a, s, k):
            return sum(v.get(k, 0.0) for d, v in read[a][s]["decades"].items() if 10 <= int(d) < 60)
        cells = {}
        for a in ARMS:
            num = sum(tot(a, s, key) for s in read[a])
            den = sum(tot(a, s, "adult_weeks") for s in read[a])
            cells[a] = num / den if den else float("nan")
        seeds = sorted(set(read["f"]) & set(read["c"]))
        nf_ = np.array([tot("f", s, key) for s in seeds])
        df_ = np.array([tot("f", s, "adult_weeks") for s in seeds])
        nc_ = np.array([tot("c", s, key) for s in seeds])
        dc_ = np.array([tot("c", s, "adult_weeks") for s in seeds])
        k = len(seeds)
        W = np.stack([np.bincount(row, minlength=k) for row in RNG.integers(0, k, size=(REPS, k))]).astype(float)
        with np.errstate(invalid="ignore", divide="ignore"):
            rr = ((W @ nf_) / (W @ df_)) / ((W @ nc_) / (W @ dc_))
        ci = pct(rr)
        L.append(f"| {key} | {cells['f']:.3f} | {cells['fH']:.3f} | {cells['c']:.3f} | "
                 f"{cells['f'] / cells['c'] if cells['c'] else float('nan'):.2f} [{ci[0]:.2f}, {ci[1]:.2f}] |")
    found = {a: (sum(1 for r in read[a].values() for sv in r["survivors"] if sv["found"]),
                 sum(len(r["survivors"]) for r in read[a].values())) for a in ARMS}
    L += ["", "Matched survivors found (alive 8 weeks later): " +
          ", ".join(f"{a} {f_}/{n_}" for a, (f_, n_) in found.items()) + ".", ""]
    text = "\n".join(L) + "\n"
    (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
