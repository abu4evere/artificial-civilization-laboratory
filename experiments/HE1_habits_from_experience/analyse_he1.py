"""HE1 analysis (questions.md, frozen as `HE1-frozen`); written before any data.

Order: validity -> primary harm guards (h against c: population, extinction with paired worlds, hunger, health) ->
co-primary effect (M3 h - c wholly above 0; makes per adult-year h / c lower bound above 1) -> reading -> described.
Paired world bootstrap: 10,000 replicates, NumPy seed 20261117; ratios pooled over worlds (sum / sum).

  python experiments/HE1_habits_from_experience/analyse_he1.py                      # writes results.md
  python experiments/HE1_habits_from_experience/analyse_he1.py --smoke --dir <folder>
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
import run_he1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261117)
ARMS = ("c", "h", "x")
NAME = {"c": "v13", "h": "the law (habits from experience)", "x": "sham"}
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
    m = re.search(r"code_v13 fingerprint: ([0-9a-f]{64})", zero)
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
    L = ["# HE1: habits learn from experience — a law test in a copy (results)", "",
         "Frozen as `HE1-frozen`. run_he1.py, analyse_he1.py (written before data). Years 100–200.", "",
         "## Validity", "",
         f"- Zero checks (All: PASS, same `code_v13` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({sum(len(runs[a]) for a in ARMS)} of {len(ARMS) * len(R.SEEDS)}): "
         f"**{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_v13`'s: **{'yes' if fps == {fp_now} else 'NO'}**", "",
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
    # --- primary: harm guards
    pop = (lw["h"].sum() / lw["c"].sum(), *pct((W @ lw["h"]) / (W @ lw["c"])))
    ext = {a: [s for s in seeds if runs[a][s]["extinct"]] for a in ARMS}
    extra = len(ext["h"]) - len(ext["c"])
    starv = {a: ratio(a, he("death_starvation"), lambda r: r["am1"]["sums"].get("living_weeks", 0) / R.WPY / 1000)
             for a in ARMS}
    hunger = rat(starv["h"], starv["c"])
    health = {a: ratio(a, he("census_health"), he("census_adults")) for a in ARMS}
    hdiff = diff(health["h"], health["c"])
    g = []
    if pop[0] < 0.90 and pop[2] < 1.0:
        g.append("population")
    if extra >= 3:
        g.append("extinction")
    if hunger[0] > 1.25 and hunger[1] > 1.0:
        g.append("hunger")
    if hdiff[0] < -5 and hdiff[2] < 0:
        g.append("health")
    L += ["## Primary: harm guards (the law against v13)", "",
          f"- Population: living-weeks ratio {pop[0]:.3f} [{pop[1]:.3f}, {pop[2]:.3f}]",
          f"- Extinction: v13 {len(ext['c'])}, the law {len(ext['h'])}, sham {len(ext['x'])} (extra {extra:+d}). "
          "Extinct worlds, with the same seed in the other arms: " + ("; ".join(
              f"seed {s}: v13 {'extinct' if runs['c'][s]['extinct'] else 'alive'}, law "
              f"{'extinct' if runs['h'][s]['extinct'] else 'alive'}, sham {'extinct' if runs['x'][s]['extinct'] else 'alive'}"
              for s in sorted(set(ext['c']) | set(ext['h']) | set(ext['x']))) or "none"),
          f"- Hunger: starvation deaths per 1,000 living-years: v13 {starv['c'][0]:.3f}, law {starv['h'][0]:.3f}; "
          f"ratio {hunger[0]:.3f} [{hunger[1]:.3f}, {hunger[2]:.3f}]",
          f"- Health: adults' mean health at year ends: v13 {health['c'][0]:.2f}, law {health['h'][0]:.2f}; "
          f"difference {fmt(*hdiff, d=2)}", "",
          "Rule: population ratio < 0.90 with upper bound < 1; 3+ extra extinct worlds; hunger ratio > 1.25 with lower "
          "bound > 1; health difference < −5 with upper bound < 0.", "",
          f"**Primary reading: {'no harm' if not g else 'HARM: ' + ', '.join(g) + ' (investigate; not adopted)'}.**", ""]

    # --- co-primary: the effect
    def chains(a, pre):
        gc, gm, mc, mm = (col(a, am(f"{pre}_{k}")) for k in ("g_chains", "g_made", "m_chains", "m_made"))
        with np.errstate(invalid="ignore", divide="ignore"):
            v = gm.sum() / gc.sum() - mm.sum() / mc.sum() if gc.sum() and mc.sum() else float("nan")
            return (v, (W @ gm) / (W @ gc) - (W @ mm) / (W @ mc)), int(gc.sum()), int(mc.sum())
    M3 = {a: chains(a, "m3") for a in ARMS}
    M5 = {a: chains(a, "m5") for a in ARMS}
    mk = {a: ratio(a, lambda r: r["pb2"]["actions"].get("make", 0) * R.WPY, pb("adult_weeks_win")) for a in ARMS}
    m3d = diff(M3["h"][0], M3["c"][0])
    mkr = rat(mk["h"], mk["c"])
    eff = m3d[1] > 0 and mkr[1] > 1.0
    L += ["## Co-primary: the effect", "",
          "| arm | M3 | gather chains | matched chains | makes per adult-year |", "|---|---|---|---|---|"]
    for a in ARMS:
        L.append(f"| {NAME[a]} | {M3[a][0][0]:.4f} | {M3[a][1]:,} | {M3[a][2]:,} | {mk[a][0]:.4f} |")
    L += ["", f"- M3, the law − v13: {fmt(*m3d)}", f"- Makes per adult-year, the law ÷ v13: "
          f"{mkr[0]:.3f} [{mkr[1]:.3f}, {mkr[2]:.3f}]", "",
          "Rule: \"the law releases making\" if the M3 interval lies wholly above 0 and the makes ratio's lower bound "
          "is above 1.", "", f"**Co-primary reading: {'the law releases making' if eff else 'not shown'}.**", "",
          f"## Reading", "", f"**HE1: {'SUPPORTED (no harm, and the law releases making): a confirmatory run on new seeds follows' if (not g and eff) else 'not supported'}.**", ""]

    # --- described
    L += ["## Described (no frozen prediction)", ""]
    for a, b in (("h", "x"), ("x", "c")):
        v = (lw[a].sum() / lw[b].sum(), *pct((W @ lw[a]) / (W @ lw[b])))
        L.append(f"- Living-weeks {NAME[a]} ÷ {NAME[b]}: {v[0]:.3f} [{v[1]:.3f}, {v[2]:.3f}]")
    L.append(f"- M3, sham − v13: {fmt(*diff(M3['x'][0], M3['c'][0]))}")
    L.append(f"- M5: v13 {M5['c'][0][0]:.4f}, law {M5['h'][0][0]:.4f}, sham {M5['x'][0][0]:.4f}; law − v13 "
             f"{fmt(*diff(M5['h'][0], M5['c'][0]))}")

    def acts(a):
        return [runs[a][s]["pb2"]["actions"] for s in seeds]
    soc = {}
    for a in ARMS:
        tot = np.array([sum(d.values()) for d in acts(a)], float)
        nu = np.array([sum(d.get(k, 0) for k in PERSON_ACTS) for d in acts(a)], float)
        with np.errstate(invalid="ignore", divide="ignore"):
            soc[a] = (nu.sum() / tot.sum() if tot.sum() else float("nan"), (W @ nu) / (W @ tot))
    L.append(f"- Acts aimed at a person: v13 {soc['c'][0]:.4f}, law {soc['h'][0]:.4f}; law − v13 "
             f"{fmt(*diff(soc['h'], soc['c']))}")
    K = {a: col(a, lambda r: r["pb2"]["n_kinds"]) for a in ARMS}
    Mr = {a: col(a, lambda r: r["pb2"]["n_remade"]) for a in ARMS}
    L.append("- World-new kinds (years 100–195) and R: " + "; ".join(
        f"{NAME[a]} {int(K[a].sum()):,} kinds, {int(Mr[a].sum()):,} remade" for a in ARMS))
    food = {a: ratio(a, pb("census_food"), pb("census_adults")) for a in ARMS}
    L.append(f"- Edible food per adult at year ends: v13 {food['c'][0]:.3f}, law {food['h'][0]:.3f}; law − v13 "
             f"{fmt(*diff(food['h'], food['c']), d=3)}")
    m2 = {a: ratio(a, am("m2_mi_sum"), am("m2_person_years")) for a in ARMS}
    L.append(f"- M2: v13 {m2['c'][0]:.4f}, law {m2['h'][0]:.4f}; law − v13 {fmt(*diff(m2['h'], m2['c']))}")
    causes = sorted({k[6:] for a in ARMS for s in seeds for k in runs[a][s]["he1"] if k.startswith("death_")})
    L += ["", "**Deaths by cause (years 100–200; all ages).**", "", "| cause | " + " | ".join(NAME[a] for a in ARMS) + " |",
          "|---|---|---|---|"]
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
