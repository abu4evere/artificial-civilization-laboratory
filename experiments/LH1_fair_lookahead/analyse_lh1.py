"""LH1 analysis (questions.md, frozen as `LH1-frozen`); written before any data (committed before the cloud run's data
were fetched).

Per arm (e: the real next choice; m: the experienced value of the next situation), against v13 (c): validity ->
primary harm guards (population, extinction with paired worlds, hunger, killing, health) -> co-primary making (M3
wholly above 0; makes ratio's lower bound above 1) -> reading -> described. Paired world bootstrap: 10,000 replicates,
NumPy seed 20261118; ratios pooled over worlds (sum / sum).

  python experiments/LH1_fair_lookahead/analyse_lh1.py                      # writes results.md
  python experiments/LH1_fair_lookahead/analyse_lh1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_lh1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261118)
ARMS = ("c", "e", "m", "x")
NAME = {"c": "v13", "e": "e (the real next choice)", "m": "m (the experienced situation value)", "x": "sham"}
PERSON_ACTS = ("give", "care", "talk", "court", "steal", "attack")


def pct(x):
    x = x[np.isfinite(x)]
    return (float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))) if len(x) else (float("nan"),) * 2


def fmt(pt, lo, hi, d=4):
    return f"{pt:+.{d}f} [{lo:+.{d}f}, {hi:+.{d}f}]"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {a: {} for a in ARMS}
    for f in sorted(glob.glob(str(OUTDIR / "*_seed_*.json"))):
        r = json.load(open(f))
        if r["arm"] in runs:
            runs[r["arm"]][r["seed"]] = r
    zero = ""
    for name in ("zero_cloud.log", "zero_local.log"):
        if (HERE / name).exists():
            zero = (HERE / name).read_text(encoding="utf-8", errors="replace")
            break
    R.base.setup(R.CODE)
    fp_now = R.base.fingerprint(R.CODE)
    m = re.search(r"code_lh1 fingerprint: ([0-9a-f]{64})", zero)
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
    L = ["# LH1: a fairer look-ahead (results)", "",
         "Frozen as `LH1-frozen`. run_lh1.py, analyse_lh1.py (written before data). Years 100–200.", "",
         "## Validity", "",
         f"- Zero checks (All: PASS, same `code_lh1` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({sum(len(runs[a]) for a in ARMS)} of {len(ARMS) * len(R.SEEDS)}): "
         f"**{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_lh1`'s: **{'yes' if fps == {fp_now} else 'NO'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
        print("\n".join(L))
        return
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def col(a, f):
        return np.array([float(f(runs[a][s])) for s in seeds])

    def am(k):
        return lambda r: r["am1"]["sums"].get(k, 0)

    def pb(k):
        return lambda r: r["pb2"]["sums"].get(k, 0)

    def he(k):
        return lambda r: r["he1"].get(k, 0)

    def ratio(a, num, den):
        nu, de = col(a, num), col(a, den)
        with np.errstate(invalid="ignore", divide="ignore"):
            return (nu.sum() / de.sum() if de.sum() else float("nan")), (W @ nu) / (W @ de)

    def diff(va, vb):
        return va[0] - vb[0], *pct(va[1] - vb[1])

    def rat(va, vb):
        with np.errstate(invalid="ignore", divide="ignore"):
            return va[0] / vb[0], *pct(va[1] / vb[1])

    lw = {a: col(a, am("living_weeks")) for a in ARMS}
    lyears = lambda r: r["am1"]["sums"].get("living_weeks", 0) / R.WPY / 1000  # noqa: E731
    ext = {a: [s for s in seeds if runs[a][s]["extinct"]] for a in ARMS}
    starv = {a: ratio(a, he("death_starvation"), lyears) for a in ARMS}
    kill = {a: ratio(a, he("death_killed"), lyears) for a in ARMS}
    health = {a: ratio(a, he("census_health"), he("census_adults")) for a in ARMS}

    def chains(a, pre):
        gc, gm, mc, mm = (col(a, am(f"{pre}_{k}")) for k in ("g_chains", "g_made", "m_chains", "m_made"))
        with np.errstate(invalid="ignore", divide="ignore"):
            v = gm.sum() / gc.sum() - mm.sum() / mc.sum() if gc.sum() and mc.sum() else float("nan")
            return (v, (W @ gm) / (W @ gc) - (W @ mm) / (W @ mc)), int(gc.sum()), int(mc.sum())
    M3 = {a: chains(a, "m3") for a in ARMS}
    mk = {a: ratio(a, lambda r: r["pb2"]["actions"].get("make", 0) * R.WPY, pb("adult_weeks_win")) for a in ARMS}
    readings = {}
    L += ["## Primary: harm guards (each rule against v13)", "",
          "Rule: population ratio < 0.90 with upper bound < 1; 3+ extra extinct worlds; hunger ratio > 1.25 with lower "
          "bound > 1; killing rate higher by > 0.05 per 1,000 living-years with lower bound > 0; health lower by > 5 "
          "with upper bound < 0.", ""]
    for a in ("e", "m"):
        pop = (lw[a].sum() / lw["c"].sum(), *pct((W @ lw[a]) / (W @ lw["c"])))
        extra = len(ext[a]) - len(ext["c"])
        hunger = rat(starv[a], starv["c"])
        kd = diff(kill[a], kill["c"])
        hd = diff(health[a], health["c"])
        g = []
        if pop[0] < 0.90 and pop[2] < 1.0:
            g.append("population")
        if extra >= 3:
            g.append("extinction")
        if hunger[0] > 1.25 and hunger[1] > 1.0:
            g.append("hunger")
        if kd[0] > 0.05 and kd[1] > 0:
            g.append("killing")
        if hd[0] < -5 and hd[2] < 0:
            g.append("health")
        m3d = diff(M3[a][0], M3["c"][0])
        mkr = rat(mk[a], mk["c"])
        eff = m3d[1] > 0 and mkr[1] > 1.0
        readings[a] = ("SUPPORTED" if (not g and eff) else "not supported")
        L += [f"### {NAME[a]}", "",
              f"- Population: living-weeks ratio {pop[0]:.3f} [{pop[1]:.3f}, {pop[2]:.3f}]",
              f"- Extinction: v13 {len(ext['c'])}, this rule {len(ext[a])} (extra {extra:+d})" + (
                  "; extinct seeds: " + "; ".join(f"{s} (v13 {'x' if runs['c'][s]['extinct'] else 'alive'}, sham "
                                                   f"{'x' if runs['x'][s]['extinct'] else 'alive'})" for s in ext[a])
                  if ext[a] else ""),
              f"- Hunger: starvation deaths per 1,000 living-years v13 {starv['c'][0]:.3f}, this rule "
              f"{starv[a][0]:.3f}; ratio {hunger[0]:.3f} [{hunger[1]:.3f}, {hunger[2]:.3f}]",
              f"- Killing: deaths by killing per 1,000 living-years v13 {kill['c'][0]:.4f}, this rule {kill[a][0]:.4f}; "
              f"difference {fmt(*kd)}",
              f"- Health: adults' mean v13 {health['c'][0]:.2f}, this rule {health[a][0]:.2f}; difference "
              f"{fmt(*hd, d=2)}",
              f"- **Harm: {'none' if not g else 'GUARD RAISED: ' + ', '.join(g)}.**",
              f"- Making: M3 v13 {M3['c'][0][0]:.4f}, this rule {M3[a][0][0]:.4f}; difference {fmt(*m3d)}; makes per "
              f"adult-year {mk['c'][0]:.4f} → {mk[a][0]:.4f}, ratio {mkr[0]:.3f} [{mkr[1]:.3f}, {mkr[2]:.3f}]; "
              f"**{'making released' if eff else 'making not shown'}**",
              f"- **Reading: {readings[a]}.**", ""]
    both = [a for a in ("e", "m") if readings[a] == "SUPPORTED"]
    if len(both) == 2:
        first = min(both, key=lambda a: (starv[a][0], kill[a][0]))
        L += [f"**Both rules are supported.** The council chooses which goes to the confirmatory run; the pre-stated "
              f"tie-break (lower starvation, then lower killing) points to {NAME[first]}.", ""]
    elif both:
        L += [f"**{NAME[both[0]]} is supported: a confirmatory run on new seeds follows.**", ""]
    else:
        L += ["**Neither rule is supported.**", ""]

    # --- described
    L += ["## Described (no frozen prediction)", ""]
    for a in ("e", "m", "x"):
        v = (lw[a].sum() / lw["x"].sum(), *pct((W @ lw[a]) / (W @ lw["x"]))) if a != "x" else \
            (lw["x"].sum() / lw["c"].sum(), *pct((W @ lw["x"]) / (W @ lw["c"])))
        L.append(f"- Living-weeks {NAME[a]} ÷ {'sham' if a != 'x' else 'v13'}: {v[0]:.3f} [{v[1]:.3f}, {v[2]:.3f}]")

    def acts(a):
        return [runs[a][s]["pb2"]["actions"] for s in seeds]
    for a in ARMS:
        tot = np.array([sum(d.values()) for d in acts(a)], float)
        soc = np.array([sum(d.get(k, 0) for k in PERSON_ACTS) for d in acts(a)], float).sum() / tot.sum()
        st = sum(d.get("steal", 0) for d in acts(a)) / tot.sum()
        at = sum(d.get("attack", 0) for d in acts(a)) / tot.sum()
        K = col(a, lambda r: r["pb2"]["n_kinds"]).sum()
        Mr = col(a, lambda r: r["pb2"]["n_remade"]).sum()
        food = ratio(a, pb("census_food"), pb("census_adults"))[0]
        L.append(f"- {NAME[a]}: acts aimed at a person {soc:.4f}; steal {st * 1000:.3f}‰; attack {at * 1000:.3f}‰; "
                 f"world-new kinds {int(K):,}, remade {int(Mr):,}; edible food per adult {food:.3f}")
    causes = sorted({k[6:] for a in ARMS for s in seeds for k in runs[a][s]["he1"] if k.startswith("death_")})
    L += ["", "**Deaths by cause (years 100–200; all ages).**", "",
          "| cause | " + " | ".join(NAME[a] for a in ARMS) + " |", "|---|" + "---|" * len(ARMS)]
    for cz in causes:
        L.append(f"| {cz} | " + " | ".join(f"{int(col(a, he('death_' + cz)).sum()):,}" for a in ARMS) + " |")
    L += ["", "## Population (beside every measure)", "", "| arm | living-weeks | adult-weeks (16–49) | extinct worlds |",
          "|---|---|---|---|"]
    for a in ARMS:
        L.append(f"| {NAME[a]} | {int(lw[a].sum()):,} | {int(col(a, am('adult_weeks')).sum()):,} | {len(ext[a])} |")
    L.append("")
    text = "\n".join(L) + "\n"
    if SMOKE:
        print(text)
        return
    (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
