"""NB1 analysis (questions.md, NB1-frozen, amendments 1, 2 and 3). Written before data. Paired world bootstrap, 10,000 draws,
NumPy seed 20261131.

Phase 1: validity; viability (extinction, population ratio against v17); primary 1 (the per-world slope over generations
1-20 of survival to 16 per birth and of adult lifespan, pooled as the mean slope over worlds); the g trajectory; CI1's
eight guards (descriptive); the network's share of the decision; the action mix's entropy.
Phase 2 (if its output is present): inherited adaptation (generation 18 against 1, learning off, children's survival
to 16, paired by source world) and lifetime learning (on against off, pooled over generations).

  python experiments/NB1_neural_brain/analyse_nb1.py [--smoke] [--dir <phase-1 output>] [--garden <phase-2 output>]
"""
from __future__ import annotations

import glob
import json
import math
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_nb1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
GARDEN = Path(sys.argv[sys.argv.index("--garden") + 1]) if "--garden" in sys.argv else HERE / "output_garden"
REPS = 10_000
RNG = np.random.default_rng(20261131)
ARMS = ("c", "n", "e")
NAME = {"c": "v17", "n": "neural brain, learning", "e": "neural brain, evolution only"}
WPY = R.WPY
LY = 1000 * WPY
GMAX = 20             # amendment 3
MIN_KNOWN = 10        # a generation counts in a world's slope if at least 10 of its births have a known outcome


def pct(x):
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    return (float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))) if len(x) else (float("nan"),) * 2


def finish(L):
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


def wslope(xs, ys, ws):
    xs, ys, ws = (np.asarray(v, dtype=float) for v in (xs, ys, ws))
    if len(xs) < 3 or ws.sum() <= 0:
        return float("nan")
    mx = (ws * xs).sum() / ws.sum()
    my = (ws * ys).sum() / ws.sum()
    den = (ws * (xs - mx) ** 2).sum()
    return float((ws * (xs - mx) * (ys - my)).sum() / den) if den > 0 else float("nan")


def slopes(run):
    """Per world: the weighted slope over generations 1-20 of survival to 16 per birth (weights: known births) and of
    adult lifespan (weights: grown deaths)."""
    gens = run["gens"]
    xs, s16, w16, xa, la, wa = [], [], [], [], [], []
    for g in range(1, GMAX + 1):
        row = gens.get(str(g))
        if row is None:
            continue
        known, reached, adeaths, ages, _ = row
        if known >= MIN_KNOWN:
            xs.append(g)
            s16.append(reached / known)
            w16.append(known)
        if adeaths >= MIN_KNOWN:
            xa.append(g)
            la.append(ages / adeaths)
            wa.append(adeaths)
    return wslope(xs, s16, w16), wslope(xa, la, wa), len(xs)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {a: {} for a in ARMS}
    for f in sorted(glob.glob(str(OUTDIR / "*_seed_*.json"))):
        r = json.load(open(f))
        if r["arm"] in runs:
            runs[r["arm"]][r["seed"]] = r
    zero = (HERE / "zero_local.log").read_text(encoding="utf-8", errors="replace") if (HERE / "zero_local.log").exists() else ""
    R.base.setup(R.CODE)
    fp_now = R.base.fingerprint(R.CODE)
    m = re.search(r"code_nb1 fingerprint: ([0-9a-f]{64})", zero)
    zero_ok = "All: PASS" in zero and m is not None and m.group(1) == fp_now
    if SMOKE:
        seeds = sorted(set.intersection(*[set(runs[a]) for a in ARMS if runs[a]]))
        present = len(seeds) > 0
    else:
        seeds = sorted(R.SEEDS)
        present = all(sorted(runs[a]) == seeds for a in ARMS)
    allr = [r for a in ARMS for r in runs[a].values()]
    fps = {r["code_hash"] for r in allr} | {r["code_hash_after"] for r in allr}
    ok = bool(zero_ok and present and fps == {fp_now})
    L = ["# NB1: can a neural-brained people survive and improve over generations? (results)", "",
         "Frozen as `NB1-frozen` (amendments 1, 2 and 3). run_nb1.py, run_nb1_garden.py, analyse_nb1.py (written before data).",
         "", "## Validity", "",
         f"- Zero checks (All: PASS, `code_nb1` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All phase-1 worlds present ({len(allr)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_nb1`'s: **{'yes' if fps == {fp_now} else 'NO'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        finish(L)
        return
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def col(a, key):
        return np.array([float(runs[a][s]["sums"].get(key, 0)) for s in seeds])

    # viability
    ext = {a: sum(1 for s in seeds if runs[a][s]["extinct"]) for a in ARMS}
    pop = {}
    for a in ("n", "e"):
        la, lc = col(a, "living_weeks"), col("c", "living_weeks")
        with np.errstate(invalid="ignore", divide="ignore"):
            pop[a] = (la.sum() / lc.sum(), pct((W @ la) / (W @ lc)))
    viable = ext["n"] - ext["c"] <= 3 and pop["n"][1][1] >= 0.80

    # primary 1: the mean per-world slope, bootstrapped over worlds
    prim = {}
    for a in ("n", "e"):
        sl = [slopes(runs[a][s]) for s in seeds]
        s16 = np.array([x[0] for x in sl])
        sad = np.array([x[1] for x in sl])
        ngen = [x[2] for x in sl]

        def boot(v):
            ok_ = np.isfinite(v)
            if ok_.sum() == 0:
                return float("nan"), (float("nan"), float("nan")), 0
            vv = np.where(ok_, v, 0.0)
            with np.errstate(invalid="ignore", divide="ignore"):
                b = (W @ vv) / (W @ ok_.astype(float))
            return float(vv.sum() / ok_.sum()), pct(b), int(ok_.sum())
        prim[a] = {"s16": boot(s16), "adult": boot(sad), "ngen": ngen}
    improves1 = prim["n"]["s16"][1][0] > 0 or prim["n"]["adult"][1][0] > 0

    # the g trajectory: mean over worlds of mean g at each century's last year
    def g_at(a, year):
        vals = []
        for s in seeds:
            row = next((y for y in runs[a][s]["years"] if y["year"] == year), None)
            if row is not None and "g_mean" in row:
                vals.append(row["g_mean"])
        return float(np.mean(vals)) if vals else float("nan"), len(vals)
    years = [y for y in (1, 50, 100, 200, 300, 400, 500, 600)]
    gtraj = {a: [g_at(a, y) for y in years] for a in ("n", "e")}
    decorative = all((not math.isfinite(v)) or v >= 0.9 for v, _ in gtraj["n"])
    g_falls = math.isfinite(gtraj["n"][-1][0]) and gtraj["n"][-1][0] < 0.9

    # phase 2
    garden = {}
    for f in sorted(glob.glob(str(GARDEN / "*_seed_*.json"))):
        r = json.load(open(f))
        if "skipped" not in r:
            garden[(r["arm"], r["source_seed"])] = r
    inherited = lifetime = None
    if garden:
        def surv(r):
            return r["reached16"] / r["known"] if r["known"] else float("nan")
        src = [s for s in seeds if ("g18N", s) in garden and ("g1N", s) in garden]
        d = np.array([surv(garden[("g18N", s)]) - surv(garden[("g1N", s)]) for s in src])
        if len(d):
            okd = np.isfinite(d)
            dd = d[okd]
            k = len(dd)
            Wk = np.stack([np.bincount(row, minlength=k) for row in RNG.integers(0, k, size=(REPS, k))]).astype(float)
            inherited = (float(dd.mean()), pct((Wk @ dd) / k), k)
        pairs = [(garden[(f"g{g}L", s)], garden[(f"g{g}N", s)]) for g in (1, 9, 18) for s in seeds
                 if (f"g{g}L", s) in garden and (f"g{g}N", s) in garden]
        if pairs:
            dl = np.array([surv(a) - surv(b) for a, b in pairs])
            dl = dl[np.isfinite(dl)]
            k = len(dl)
            if k:
                Wk = np.stack([np.bincount(row, minlength=k) for row in RNG.integers(0, k, size=(REPS, k))]).astype(float)
                lifetime = (float(dl.mean()), pct((Wk @ dl) / k), k)
    inherited_yes = inherited is not None and inherited[1][0] > 0

    if not viable:
        reading = "neural people not viable"
    elif (improves1 or inherited_yes) and g_falls:
        reading = "improves by itself"
    elif decorative:
        reading = "decorative (g stays at or above 0.9)"
    else:
        reading = "no improvement shown"

    def f3(t):
        return f"{t[0]:+.5f} [{t[1][0]:+.5f}, {t[1][1]:+.5f}] ({t[2]} worlds)"
    L += ["## Reading (frozen)", "",
          f"- **{reading}.**",
          f"- Viability: extinct worlds c {ext['c']}, n {ext['n']}, e {ext['e']}; population (living-weeks, years 100-600) "
          f"n/c {pop['n'][0]:.4f} [{pop['n'][1][0]:.4f}, {pop['n'][1][1]:.4f}], e/c {pop['e'][0]:.4f} "
          f"[{pop['e'][1][0]:.4f}, {pop['e'][1][1]:.4f}]; viable: **{'yes' if viable else 'no'}**.",
          f"- Primary 1 (n): slope per generation of survival to 16 per birth {f3(prim['n']['s16'])}; of adult lifespan "
          f"(years) {f3(prim['n']['adult'])}; improves: **{'yes' if improves1 else 'no'}**.",
          f"- Primary 1 (e, evolution only): survival to 16 {f3(prim['e']['s16'])}; adult lifespan {f3(prim['e']['adult'])}.",
          f"- Primary 2, inherited (generation 18 - 1, learning off, children's survival to 16): "
          f"{f3(inherited) if inherited else 'phase 2 not present'}; yes: **{'yes' if inherited_yes else 'no'}**.",
          f"- Lifetime learning (on - off, pooled over generations): {f3(lifetime) if lifetime else 'phase 2 not present'}.",
          f"- g falls below 0.9 by year 600 (n): **{'yes' if g_falls else 'no'}**; decorative: **{'yes' if decorative else 'no'}**.",
          "", "Rule: 'not viable' if n has more than 3 extra extinct worlds or the population ratio's upper bound is below "
          "0.80; 'improves by itself' if primary 1 or primary 2 (inherited) is yes and g falls; 'decorative' if g stays "
          "at or above 0.9; otherwise 'no improvement shown'.", "",
          "## The g trajectory (mean over worlds of the mean g at each year)", "",
          "| year | " + " | ".join(str(y) for y in years) + " |", "|---|" + "---|" * len(years)]
    for a in ("n", "e"):
        L.append(f"| {NAME[a]} | " + " | ".join(f"{v:.3f}" if math.isfinite(v) else "-" for v, _ in gtraj[a]) + " |")

    # guards, descriptive
    def ratio(a, num, den, per=1.0):
        nu, de = col(a, num), col(a, den)
        nc, dc = col("c", num), col("c", den)
        with np.errstate(invalid="ignore", divide="ignore"):
            pa, pc = nu.sum() / de.sum() * per, nc.sum() / dc.sum() * per
            b = ((W @ nu) / (W @ de)) / ((W @ nc) / (W @ dc))
        return pa, pc, pa / pc if pc else float("nan"), pct(b)
    L += ["", "## CI1's eight guards, neural brain (n) against v17 (descriptive; 16 seeds cannot gate harm)", "",
          "| measure | n | v17 | ratio [95%] |", "|---|---|---|---|"]
    for lab, num, den, per in (("starvation deaths per 1,000 living-years", "death_starvation", "living_weeks", LY),
                               ("killing deaths per 1,000 living-years", "death_killed", "living_weeks", LY),
                               ("adult health, mean", "census_health", "census_adults", 1.0),
                               ("child deaths per 1,000 child-years", "child_deaths", "child_weeks", LY),
                               ("child starvation deaths per 1,000 child-years", "child_death_starvation", "child_weeks", LY),
                               ("gifts to kin's children per 1,000 adult-weeks", "gifts_kin_children", "adult_weeks", 1000)):
        pa, pc, rr, ci = ratio("n", num, den, per)
        L.append(f"| {lab} | {pa:.4f} | {pc:.4f} | {rr:.4f} [{ci[0]:.4f}, {ci[1]:.4f}] |")

    # the network's share of the decision; the action mix
    L += ["", "## The network's part of the decision (sampled every 50th decision)", "",
          "| arm | decisions | mean correlation, network and hand-written scores | spread ratio, network / hand-written |",
          "|---|---|---|---|"]
    for a in ("n", "e"):
        cs = [runs[a][s]["corr"] for s in seeds]
        looks = sum(c.get("looks", 0) for c in cs)
        cn = sum(c.get("corr_n", 0) for c in cs)
        cm = sum(c.get("corr_sum", 0.0) for c in cs) / cn if cn else float("nan")
        sr = sum(c.get("sd_net", 0.0) for c in cs) / max(1e-12, sum(c.get("sd_hand", 0.0) for c in cs))
        L.append(f"| {NAME[a]} | {looks:,} | {cm:.4f} | {sr:.4f} |")
    L += ["", "## Action mix of the grown: entropy (bits) by century", "", "| arm | " +
          " | ".join(f"{c * 100}-{c * 100 + 100}" for c in range(6)) + " |", "|---|" + "---|" * 6]
    for a in ARMS:
        cells = []
        for c in range(6):
            tot = {}
            for s in seeds:
                for k, v in runs[a][s]["acts"].get(str(c), {}).items():
                    tot[k] = tot.get(k, 0) + v
            t = sum(tot.values())
            cells.append(f"{-sum(v / t * math.log2(v / t) for v in tot.values() if v):.3f}" if t else "-")
        L.append(f"| {NAME[a]} | " + " | ".join(cells) + " |")
    L.append("")
    finish(L)


if __name__ == "__main__":
    main()
