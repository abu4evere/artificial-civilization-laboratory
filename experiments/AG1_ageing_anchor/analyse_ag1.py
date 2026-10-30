"""AG1 analysis, written before any data (questions.md, frozen as `AG1-frozen`).

  python experiments/AG1_ageing_anchor/analyse_ag1.py                       # writes results.md
  python experiments/AG1_ageing_anchor/analyse_ag1.py --smoke --dir <folder> [--from-year Y]
"""
from __future__ import annotations

import glob
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_ag1  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
SEEDS = run_ag1.SMOKE_SEEDS if SMOKE else run_ag1.SEEDS
ARMS = tuple(run_ag1.ARMS)
WPY = run_ag1.WPY
BANDS = run_ag1.BANDS
REPS = 10_000
RNG = np.random.default_rng(20261030)
FROM = int(sys.argv[sys.argv.index("--from-year") + 1]) if "--from-year" in sys.argv else 100   # frozen: 100
TO = 1000                                    # years 100-999
PRIMARY = ((30, 45), (45, 60), (60, 70))
MID = {(30, 45): 37.5, (45, 60): 52.5, (60, 70): 65.0}
LATE = (800, 1000)
MARGIN = 0.012                               # LC1's skill margin, shown for scale only


def ref(x):
    """The frozen forager reference: total hazard per year (SA1 note's a2 and senescent part)."""
    return 0.013 + 1.47e-4 * math.exp(0.086 * x)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {a: {} for a in ARMS}
    for f in glob.glob(str(OUTDIR / "*_seed_*.json")):
        r = json.load(open(f))
        if r["arm"] in runs:
            runs[r["arm"]][r["seed"]] = r
    zero = (OUTDIR / "zero.txt").read_text(encoding="utf-8") if (OUTDIR / "zero.txt").exists() else ""
    present = all(sorted(runs[a]) == sorted(SEEDS) for a in ARMS)
    fps = {r["code_hash"] for a in ARMS for r in runs[a].values()} | \
          {r["code_hash_after"] for a in ARMS for r in runs[a].values()}
    mism = sum(sum(r["mismatch"].values()) for a in ARMS for r in runs[a].values())
    ok = "All: PASS" in zero and present and len(fps) == 1 and mism == 0
    L = ["# AG1 — Ageing anchored to forager evidence: results" + (" (SMOKE TEST, throwaway seeds)" if SMOKE else ""),
         "", "Frozen as `AG1-frozen`. run_ag1.py, analyse_ag1.py (written before data).", "", "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({sum(len(v) for v in runs.values())} of {len(ARMS) * len(SEEDS)}): "
         f"**{'yes' if present else 'NO'}**",
         f"- One fingerprint (`code_v9`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- Observer deaths equal the world's dead in every world: **{'yes' if mism == 0 else f'NO ({mism})'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    seeds = sorted(SEEDS)
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))])
    L += [f"Paired seeds: {n}; mortality_base: " + ", ".join(
        f"{a} {runs[a][seeds[0]]['mortality_base']:.4e}" for a in ARMS) + ".", ""]

    # per-world deaths and person-years in each band, years FROM-TO
    def band_index(lo, hi):
        return BANDS.index((lo, hi))

    def deaths_py(arm, lo, hi):
        D, P = [], []
        for s in seeds:
            r = runs[arm][s]
            D.append(sum(1 for t, age, cause, gen in r["deaths"]
                         if FROM * WPY <= t < TO * WPY and age is not None and lo <= age < hi))
            bi = band_index(lo, hi)
            P.append(sum(v[bi] for c, v in r["person_weeks"].items() if FROM <= int(c) * 100 < TO) / WPY)
        return np.array(D, float), np.array(P, float)

    data = {a: {b: deaths_py(a, *b) for b in PRIMARY} for a in ARMS}

    def dist(arm, w=None):
        """D for the pooled data (w None) or for each bootstrap replicate (w = weight matrix)."""
        terms = []
        for b in PRIMARY:
            Dd, Pp = data[arm][b]
            with np.errstate(divide="ignore", invalid="ignore"):
                rate = (Dd.sum() / Pp.sum()) if w is None else (w @ Dd) / (w @ Pp)
                terms.append(np.abs(np.log(rate / ref(MID[b]))))
        return sum(terms) / len(terms)

    L += ["## Primary — calibration distance", "",
          f"All-cause death rates per person-year, years {FROM}–{TO - 1}, pooled over worlds; reference h(x) = 0.013 + "
          "1.47e-4 exp(0.086 x) at the band midpoints; D = mean |ln(rate / reference)| over the three bands.", "",
          "| arm | " + " | ".join(f"{lo}–{hi}: deaths / person-years = rate (ref {ref(MID[(lo, hi)]):.5f})"
                                   for lo, hi in PRIMARY) + " | D |",
          "|---|" + "---|" * (len(PRIMARY) + 1)]
    Dpt = {}
    for a in ARMS:
        cells = []
        for b in PRIMARY:
            Dd, Pp = data[a][b]
            cells.append(f"{int(Dd.sum())} / {Pp.sum():,.0f} = {Dd.sum() / Pp.sum() if Pp.sum() else float('nan'):.4f}")
        Dpt[a] = float(dist(a))
        L.append(f"| {a} | " + " | ".join(cells) + f" | {Dpt[a]:.4f} |")
    reps = {a: dist(a, W) for a in ARMS}
    keep = np.all([np.isfinite(reps[a]) for a in ARMS], axis=0)
    dropped = int((~keep).sum())

    def ci(x):
        return np.percentile(x[keep], [2.5, 97.5])
    diff = {a: (Dpt[a] - Dpt["v"], *ci(reps[a] - reps["v"])) for a in ("b", "a", "x")}
    L += ["", f"Paired world bootstrap, {REPS:,} replicates (dropped for an empty band: {dropped}).", "",
          "| arm | D(arm) − D(v) [95%] |", "|---|---|"]
    for a in ("b", "a", "x"):
        L.append(f"| {a} | {diff[a][0]:+.4f} [{diff[a][1]:+.4f}, {diff[a][2]:+.4f}] |")

    # flags
    ext = {a: sum(1 for s in seeds if runs[a][s]["extinct"]) for a in ARMS}

    def living_py(arm, lo, hi):
        i = runs[arm][seeds[0]]["census_fields"].index("living")
        return np.array([sum(row[i] for row in runs[arm][s]["census"] if lo <= row[0] < hi) for s in seeds], float)
    pop = {a: living_py(a, *LATE).sum() for a in ARMS}
    verdict = {}
    L += ["", "## The frozen rule", ""]
    for a in ("b", "a"):
        realistic = diff[a][2] < 0 and diff[a][2] < diff["x"][1]
        f1 = ext[a] - ext["v"] >= 3
        f2 = pop[a] < 0.90 * pop["v"]
        verdict[a] = (realistic, f1, f2)
        L.append(f"- **{a}:** upper bound {diff[a][2]:+.4f} below 0 and below the sham's lower bound "
                 f"{diff['x'][1]:+.4f}: **{'more realistic' if realistic else 'not shown'}**. Flags: extinct "
                 f"{ext[a]} vs v {ext['v']} ({'FLAG' if f1 else 'no flag'}); living person-years, years 800–999, "
                 f"{a} ÷ v = {pop[a] / pop['v'] if pop['v'] else float('nan'):.3f} ({'FLAG' if f2 else 'no flag'}).")
    both = verdict["b"][0] and verdict["a"][0]
    if both:
        overlap = not (diff["a"][2] < diff["b"][1] or diff["b"][2] < diff["a"][1])
        if overlap:
            L.append("- Both are more realistic and their intervals overlap: **both calibrate; the choice is the "
                     "creator's.**")
        else:
            better = "a" if Dpt["a"] < Dpt["b"] else "b"
            L.append(f"- Both are more realistic; their intervals do not overlap: **{better} is the better anchor** "
                     f"(lower D).")
    L += ["", "Exploratory (20 seeds): adoption needs a confirmatory run and the creator's decision.", ""]

    # described
    L += ["## Described (not part of the rule)", "",
          "| arm | adult (16+) deaths | mean adult age at death | adult deaths at 60+ | at 70+ | living aged 60+ (share, years 800–999) | extinct |",
          "|---|---|---|---|---|---|---|"]
    for a in ARMS:
        ages = [age for s in seeds for t, age, cause, gen in runs[a][s]["deaths"]
                if FROM * WPY <= t < TO * WPY and age is not None and age >= 16]
        i_l = runs[a][seeds[0]]["census_fields"].index("living")
        i_o = runs[a][seeds[0]]["census_fields"].index("aged_60")
        liv = sum(row[i_l] for s in seeds for row in runs[a][s]["census"] if LATE[0] <= row[0] < LATE[1])
        old = sum(row[i_o] for s in seeds for row in runs[a][s]["census"] if LATE[0] <= row[0] < LATE[1])
        L.append(f"| {a} | {len(ages)} | {np.mean(ages) if ages else float('nan'):.1f} | "
                 f"{np.mean([x >= 60 for x in ages]) if ages else float('nan'):.3f} | "
                 f"{np.mean([x >= 70 for x in ages]) if ages else float('nan'):.3f} | "
                 f"{old / liv if liv else float('nan'):.3f} | {ext[a]} of {n} |")

    def cen(arm, field, lo, hi):
        out = []
        for s in seeds:
            r = runs[arm][s]
            i = r["census_fields"].index(field)
            out.append(float(sum(row[i] for row in r["census"] if lo <= row[0] < hi)))
        return np.array(out)

    def pooled(arm, num, den, win):
        N, Dn = cen(arm, num, *win), cen(arm, den, *win)
        with np.errstate(invalid="ignore", divide="ignore"):
            return (N.sum() / Dn.sum() if Dn.sum() else float("nan")), (W @ N) / (W @ Dn)
    L += ["", "| measure (years 800–999) | v | b − v [95%] | a − v [95%] | x − v [95%] |", "|---|---|---|---|---|"]
    for name, num, den in (("world-born adults' (20–40) crafting skill", "wb_craft_sum_20_40", "wb_adults_20_40"),
                           ("making events per adult-year", "makes", "adults"),
                           ("made things held per adult", "items_adults", "adults")):
        p0, r0 = pooled("v", num, den, LATE)
        cells = []
        for a in ("b", "a", "x"):
            p1, r1 = pooled(a, num, den, LATE)
            d = r1 - r0
            d = d[np.isfinite(d)]
            lo, hi = np.percentile(d, [2.5, 97.5]) if len(d) else (float("nan"),) * 2
            cells.append(f"{p1 - p0:+.4f} [{lo:+.4f}, {hi:+.4f}]")
        L.append(f"| {name} | {p0:.4f} | " + " | ".join(cells) + " |")
    L += ["", f"(LC1's skill margin ±{MARGIN}, for scale only.)", "",
          "| arm | mean living per century (worlds alive or 0): " + " / ".join(f"{c}" for c in range(0, 1000, 100)) + " |",
          "|---|---|"]
    for a in ARMS:
        cells = []
        for lo in range(0, 1000, 100):
            cells.append(f"{living_py(a, lo, lo + 100).sum() / (n * 100):.1f}")
        L.append(f"| {a} | " + " / ".join(cells) + " |")
    L += ["", "| arm | adult causes of death (shares) | child (under 16) deaths from starvation or thirst per child-year |",
          "|---|---|---|"]
    for a in ARMS:
        from collections import Counter
        c = Counter(cause for s in seeds for t, age, cause, gen in runs[a][s]["deaths"]
                    if FROM * WPY <= t < TO * WPY and age is not None and age >= 16)
        tot = sum(c.values()) or 1
        kid = sum(1 for s in seeds for t, age, cause, gen in runs[a][s]["deaths"]
                  if FROM * WPY <= t < TO * WPY and age is not None and age < 16 and cause in ("starvation", "thirst"))
        kpy = sum(v[0] for s in seeds for cc, v in runs[a][s]["person_weeks"].items()
                  if FROM <= int(cc) * 100 < TO) / WPY
        L.append(f"| {a} | " + ", ".join(f"{k} {v / tot:.2f}" for k, v in c.most_common(6)) +
                 f" | {kid / kpy if kpy else float('nan'):.4f} |")
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
