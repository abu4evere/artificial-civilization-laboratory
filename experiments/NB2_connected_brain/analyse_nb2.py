"""NB2 analysis (questions.md, NB2-frozen). Written before data. Paired world bootstrap, 10,000 draws, NumPy seed
20261110.

Phase 1: validity; viability (extinction; population ratio against v17); the primary (survival to 16 per birth, births
in years 100-600, n against s, paired); what each fix adds (o - s, l - o, n - l); g's trajectory; CI1's eight guards
(n against c, descriptive); how often the network changes the top option.
Phase 2 (if present): inherited competence (generation 18 - 1, g = 0, learning off; children's survival to 16, paired by
source world) and learning's worth (generation 18, on - off).

  python experiments/NB2_connected_brain/analyse_nb2.py [--smoke] [--dir <phase-1 output>] [--garden <phase-2 output>]
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
import run_nb2 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
GARDEN = Path(sys.argv[sys.argv.index("--garden") + 1]) if "--garden" in sys.argv else HERE / "output_garden"
REPS = 10_000
RNG = np.random.default_rng(20261110)
ARMS = ("c", "s", "o", "l", "n")
NAME = {"c": "v17 (old minds)", "s": "sham: new options and sight, learning off", "o": "o: + NB1's REINFORCE",
        "l": "l: + actor-critic", "n": "n: + social learning (full NB2)"}
WPY = R.WPY
LY = 1000 * WPY


def pct(x):
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    return (float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))) if len(x) else (float("nan"),) * 2


def finish(L):
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


def boot_mean(d):
    d = np.asarray(d, dtype=float)
    d = d[np.isfinite(d)]
    k = len(d)
    if k == 0:
        return None
    Wk = np.stack([np.bincount(row, minlength=k) for row in RNG.integers(0, k, size=(REPS, k))]).astype(float)
    return float(d.mean()), pct((Wk @ d) / k), k


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
    m = re.search(r"code_nb2 fingerprint: ([0-9a-f]{64})", zero)
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
    L = ["# NB2: connect the world to the neural brain. Can the network decide? (results)", "",
         "Frozen as `NB2-frozen`. run_nb2.py, run_nb2_garden.py, analyse_nb2.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks (All: PASS, `code_nb2` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All phase-1 worlds present ({len(allr)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_nb2`'s: **{'yes' if fps == {fp_now} else 'NO'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        finish(L)
        return
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def col(a, key):
        return np.array([float(runs[a][s]["sums"].get(key, 0)) for s in seeds])

    def births(a):
        return (np.array([float(runs[a][s]["late_births"][0]) for s in seeds]),
                np.array([float(runs[a][s]["late_births"][1]) for s in seeds]))

    # viability (n against c)
    ext = {a: sum(1 for s in seeds if runs[a][s]["extinct"]) for a in ARMS}
    pop = {}
    for a in ARMS[1:]:
        la, lc = col(a, "living_weeks"), col("c", "living_weeks")
        with np.errstate(invalid="ignore", divide="ignore"):
            pop[a] = (la.sum() / lc.sum(), pct((W @ la) / (W @ lc)))
    viable = ext["n"] - ext["c"] <= 3 and pop["n"][1][1] >= 0.80

    # survival to 16 per birth (years 100-600), and paired differences
    surv = {}
    for a in ARMS:
        k, r = births(a)
        with np.errstate(invalid="ignore", divide="ignore"):
            surv[a] = (r.sum() / k.sum() if k.sum() else float("nan"), (W @ r) / (W @ k), int(k.sum()))

    def diff(a, b):
        return surv[a][0] - surv[b][0], pct(surv[a][1] - surv[b][1])
    prim = diff("n", "s")
    learn_helps = prim[1][0] > 0

    # phase 2
    garden = {}
    for f in sorted(glob.glob(str(GARDEN / "*_seed_*.json"))):
        r = json.load(open(f))
        if "skipped" not in r:
            garden[(r["arm"], r["source_seed"])] = r

    def gs(r):
        return r["reached16"] / r["known"] if r["known"] else float("nan")
    inherited = worth = None
    if garden:
        inherited = boot_mean([gs(garden[("g18Z", s)]) - gs(garden[("g1Z", s)]) for s in seeds
                               if ("g18Z", s) in garden and ("g1Z", s) in garden])
        worth = boot_mean([gs(garden[("g18L", s)]) - gs(garden[("g18N", s)]) for s in seeds
                           if ("g18L", s) in garden and ("g18N", s) in garden])
    inherited_yes = inherited is not None and inherited[1][0] > 0

    if not viable:
        reading = "not viable"
    elif learn_helps and inherited_yes:
        reading = "the network decides"
    elif learn_helps:
        reading = "learning helps, but the instincts still carry it"
    else:
        reading = "no improvement shown"

    def fd(t):
        return f"{t[0]:+.4f} [{t[1][0]:+.4f}, {t[1][1]:+.4f}]"

    def fb(t):
        return f"{t[0]:+.4f} [{t[1][0]:+.4f}, {t[1][1]:+.4f}] ({t[2]} source worlds)" if t else "phase 2 not present"
    L += ["## Reading (frozen)", "",
          f"- **{reading}.**",
          f"- Viability: extinct worlds " + ", ".join(f"{a} {ext[a]}" for a in ARMS) + "; population (living-weeks, "
          f"years 100-600) against c: " + ", ".join(f"{a} {pop[a][0]:.4f} [{pop[a][1][0]:.4f}, {pop[a][1][1]:.4f}]"
                                                      for a in ARMS[1:]) + f"; n viable: **{'yes' if viable else 'no'}**.",
          f"- **Primary**, survival to 16 per birth (born years 100-600), n - s: {fd(prim)}; above 0: "
          f"**{'yes' if learn_helps else 'no'}**.",
          f"- Inherited competence (generation 18 - 1, g = 0, learning off): {fb(inherited)}; above 0: "
          f"**{'yes' if inherited_yes else 'no'}**.",
          f"- Learning's worth (generation 18, on - off): {fb(worth)}.", "",
          "Rule: 'not viable' if n has more than 3 extra extinct worlds than c or the population ratio's upper bound is "
          "below 0.80; 'the network decides' if n - s and the inherited garden both have lower bounds above 0; 'learning "
          "helps, but the instincts still carry it' if only n - s does; otherwise 'no improvement shown'.", "",
          "## Survival to 16 per birth, by arm (born years 100-600)", "", "| arm | survival | births with known outcome |",
          "|---|---|---|"]
    for a in ARMS:
        L.append(f"| {NAME[a]} | {surv[a][0]:.4f} | {surv[a][2]:,} |")
    L += ["", "## What each fix adds (paired differences in survival to 16)", ""]
    for a, b, lab in (("o", "s", "NB1's learning on the new options (o - s)"), ("l", "o", "actor-critic instead (l - o)"),
                      ("n", "l", "social learning (n - l)"), ("s", "c", "new options and sight, no learning, against the old minds (s - c)"),
                      ("n", "c", "full NB2 against the old minds (n - c)")):
        L.append(f"- {lab}: {fd(diff(a, b))}")

    # g's trajectory
    years = (1, 50, 100, 200, 300, 400, 500, 600)

    def g_at(a, year):
        vals = [next((y["g_mean"] for y in runs[a][s]["years"] if y["year"] == year and "g_mean" in y), None)
                for s in seeds]
        vals = [v for v in vals if v is not None]
        return (float(np.mean(vals)) if vals else float("nan")), len(vals)
    L += ["", "## g, the weight on the instincts (mean over worlds; worlds counted in brackets)", "",
          "| arm | " + " | ".join(str(y) for y in years) + " |", "|---|" + "---|" * len(years)]
    for a in ARMS[1:]:
        L.append(f"| {a} | " + " | ".join((f"{v:.3f} ({k})" if math.isfinite(v) else "-") for v, k in
                                         (g_at(a, y) for y in years)) + " |")

    # guards
    def ratio(a, num, den, per=1.0):
        nu, de, nc, dc = col(a, num), col(a, den), col("c", num), col("c", den)
        with np.errstate(invalid="ignore", divide="ignore"):
            pa, pc = nu.sum() / de.sum() * per, nc.sum() / dc.sum() * per
            b = ((W @ nu) / (W @ de)) / ((W @ nc) / (W @ dc))
        return pa, pc, pa / pc if pc else float("nan"), pct(b)
    L += ["", "## CI1's eight guards, full NB2 (n) against v17 (descriptive; 16 seeds cannot gate harm)", "",
          "| measure | n | v17 | ratio [95%] |", "|---|---|---|---|"]
    for lab, num, den, per in (("starvation deaths per 1,000 living-years", "death_starvation", "living_weeks", LY),
                               ("killing deaths per 1,000 living-years", "death_killed", "living_weeks", LY),
                               ("adult health, mean", "census_health", "census_adults", 1.0),
                               ("child deaths per 1,000 child-years", "child_deaths", "child_weeks", LY),
                               ("child starvation deaths per 1,000 child-years", "child_death_starvation", "child_weeks", LY),
                               ("gifts to kin's children per 1,000 adult-weeks", "gifts_kin_children", "adult_weeks", 1000)):
        pa, pc, rr, ci = ratio("n", num, den, per)
        L.append(f"| {lab} | {pa:.4f} | {pc:.4f} | {rr:.4f} [{ci[0]:.4f}, {ci[1]:.4f}] |")

    # the network's part
    L += ["", "## The network's part of the decision (every 50th decision)", "",
          "| arm | decisions | options per decision | network changes the top option | correlation, network and instinct | spread ratio |",
          "|---|---|---|---|---|---|"]
    for a in ARMS[1:]:
        es = [runs[a][s].get("ext", {}) for s in seeds]
        cs = [runs[a][s]["corr"] for s in seeds]
        looks = sum(e.get("looks", 0) for e in es)
        opts = sum(e.get("options", 0) for e in es) / looks if looks else float("nan")
        ov = sum(e.get("override", 0) for e in es) / looks if looks else float("nan")
        cn = sum(c.get("corr_n", 0) for c in cs)
        cm = sum(c.get("corr_sum", 0.0) for c in cs) / cn if cn else float("nan")
        sr = sum(c.get("sd_net", 0.0) for c in cs) / max(1e-12, sum(c.get("sd_hand", 0.0) for c in cs))
        L.append(f"| {a} | {looks:,} | {opts:.1f} | {ov:.4f} | {cm:.4f} | {sr:.4f} |")
    L.append("")
    finish(L)


if __name__ == "__main__":
    main()
