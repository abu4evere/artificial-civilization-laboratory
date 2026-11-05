"""PB2 analysis (questions.md, frozen as `PB2-frozen`); written before any data.

Order: validity (zero checks, all worlds, one fingerprint) -> guards (P, G, G0 each against c) -> the validity check
(arm c: r-hat against q as predictors of r) -> primary M3 (G - P, G - G0; P - c as the steering effect) -> co-primary
R with intent tests 1-3 -> described. Paired world bootstrap: 10,000 replicates, NumPy seed 20261114; every ratio is
pooled over worlds (sum of numerators / sum of denominators), as in AM1 and AF1.

  python experiments/PB2_brain_steers/analyse_pb2.py                      # writes results.md
  python experiments/PB2_brain_steers/analyse_pb2.py --smoke --dir <folder>
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
import run_pb2 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261114)
ARMS = ("c", "P", "G", "G0", "x")
NAME = {"c": "v13 (shadow)", "P": "P (steering)", "G": "G (LP goal)", "G0": "G0 (random goal)", "x": "sham"}
GOAL_NAMES = ("food gained", "net food", "health", "energy", "materials held", "things held", "affection")
PERSON_ACTS = ("give", "care", "talk", "court", "steal", "attack")


def pct(x):
    x = x[np.isfinite(x)]
    return (float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))) if len(x) else (float("nan"),) * 2


def fmt(pt, lo, hi):
    return f"{pt:+.4f} [{lo:+.4f}, {hi:+.4f}]"


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
    m = re.search(r"code_pb2 fingerprint: ([0-9a-f]{64})", zero)
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
    L = ["# PB2: the episodic brain helps choose, in a copy of nature (results)", "",
         "Frozen as `PB2-frozen`. run_pb2.py, analyse_pb2.py (written before data). Adults 16–49, years 130–170.", "",
         "## Validity", "",
         f"- Zero checks (All: PASS, same `code_pb2` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({sum(len(runs[a]) for a in ARMS)} of {len(ARMS) * len(R.SEEDS)}): "
         f"**{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_pb2`'s: **{'yes' if fps == {fp_now} else 'NO'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
        print("\n".join(L))
        return
    arms = [a for a in ARMS if all(s in runs[a] for s in seeds)]
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def col(a, f):
        return np.array([float(f(runs[a][s])) for s in seeds])

    def am(key):
        return lambda r: r["am1"]["sums"].get(key, 0)

    def pb(key):
        return lambda r: r["pb2"]["sums"].get(key, 0)

    def ratio(a, num, den):
        nu, de = col(a, num), col(a, den)
        with np.errstate(invalid="ignore", divide="ignore"):
            return (nu.sum() / de.sum() if de.sum() else float("nan")), (W @ nu) / (W @ de)

    def diff(va, vb):
        return va[0] - vb[0], *pct(va[1] - vb[1])

    # --- guards first (G, P and G0 each against c)
    L += ["## Guards (each brain arm against v13)", ""]
    guards = {}
    for a in ("P", "G", "G0", "x"):
        if a not in arms:
            continue
        lw_a, lw_c = col(a, am("living_weeks")), col("c", am("living_weeks"))
        with np.errstate(invalid="ignore", divide="ignore"):
            pop = (lw_a.sum() / lw_c.sum(), *pct((W @ lw_a) / (W @ lw_c)))
        ext = sum(1 for s in seeds if runs[a][s]["extinct"]) - sum(1 for s in seeds if runs["c"][s]["extinct"])
        g = (["population"] if pop[0] < 0.90 and pop[2] < 1.0 else []) + (["extinctions"] if ext >= 3 else [])
        guards[a] = g
        L.append(f"- {NAME[a]}: living-weeks ratio {pop[0]:.3f} [{pop[1]:.3f}, {pop[2]:.3f}]; extinct worlds beyond "
                 f"v13's {ext:+d}" + (f" — **guard raised: {', '.join(g)} (harm: investigate)**" if g else
                                      " — no guard raised"))
    L += ["", "Rule: a guard is raised if the living-weeks ratio is below 0.90 with its upper bound below 1, or 3+ extra "
          "extinct worlds. An arm with a guard raised is not read as a success.", ""]

    # --- the validity check (arm c's shadow memory)
    vd = {k: col("c", (lambda i: lambda r: (r["pb2"]["valid"] or [0.0] * 11)[i])(i))
          for i, k in enumerate(("se_rhat", "se_q", "n", "r", "r2", "rhat", "rhat2", "q", "q2", "r_rhat", "r_q"))}
    with np.errstate(invalid="ignore", divide="ignore"):
        mse_r, mse_q = vd["se_rhat"].sum() / vd["n"].sum(), vd["se_q"].sum() / vd["n"].sum()
        rep_v = (W @ vd["se_q"] - W @ vd["se_rhat"]) / (W @ vd["n"])

        def corr(xs, xx, xy, w=None):
            S = (lambda v: v.sum()) if w is None else (lambda v: w @ v)
            N = S(vd["n"])
            mr, mx = S(vd["r"]) / N, S(vd[xs]) / N
            cov = S(vd[xy]) / N - mr * mx
            return cov / np.sqrt((S(vd["r2"]) / N - mr ** 2) * (S(vd[xx]) / N - mx ** 2))
        cr, cq = corr("rhat", "rhat2", "r_rhat"), corr("q", "q2", "r_q")
        crep = corr("rhat", "rhat2", "r_rhat", W) - corr("q", "q2", "r_q", W)
    lo, hi = pct(rep_v)
    valid_pass = bool(lo > 0)
    L += ["## The validity check (arm c: a read-only memory scores r-hat against the habit's q as predictors of r)", "",
          f"- Weeks scored (own r-hat available): {int(vd['n'].sum()):,}",
          f"- Mean squared error: r-hat {mse_r:.4f}, q {mse_q:.4f}; q − r-hat: {fmt(mse_q - mse_r, lo, hi)}",
          f"- Described: correlation with r: r-hat {cr:.4f}, q {cq:.4f}; difference {fmt(cr - cq, *pct(crep))}", "",
          f"**r-hat predicts r better than q: {'yes' if valid_pass else 'NO'}.**" +
          ("" if valid_pass else " P and G are therefore reported as **not a test of predictive steering**, and their "
           "effects are described only."), ""]

    # --- primary: M3 (and M5), pooled per world
    def chains(a, pre):
        gc, gm, mc, mm = (col(a, am(f"{pre}_{k}")) for k in ("g_chains", "g_made", "m_chains", "m_made"))
        with np.errstate(invalid="ignore", divide="ignore"):
            v = gm.sum() / gc.sum() - mm.sum() / mc.sum() if gc.sum() and mc.sum() else float("nan")
            return (v, (W @ gm) / (W @ gc) - (W @ mm) / (W @ mc)), int(gc.sum()), int(mc.sum())
    M3 = {a: chains(a, "m3") for a in arms}
    M5 = {a: chains(a, "m5") for a in arms}
    L += ["## Primary: M3, ends-directed chains", "",
          "P(made a recipe using m within 8 weeks | gathered m, a needed input of a valued recipe, holding < 1) − "
          "P(made | an opportunity-matched week).", "", "| arm | M3 | gather chains | matched chains |",
          "|---|---|---|---|"]
    for a in arms:
        L.append(f"| {NAME[a]} | {M3[a][0][0]:.4f} | {M3[a][1]:,} | {M3[a][2]:,} |")
    con = [("G", "P"), ("G", "G0"), ("P", "c"), ("G", "c"), ("G0", "c"), ("x", "c")]
    D3 = {(a, b): diff(M3[a][0], M3[b][0]) for a, b in con if a in arms and b in arms}
    L += ["", "| contrast | difference [95%] |", "|---|---|"]
    for (a, b), v in D3.items():
        tag = " (primary)" if (a, b) in (("G", "P"), ("G", "G0")) else (" (the steering effect)" if (a, b) == ("P", "c")
                                                                       else "")
        L.append(f"| {NAME[a]} − {NAME[b]}{tag} | {fmt(*v)} |")
    both = all((k in D3 and D3[k][1] > 0) for k in (("G", "P"), ("G", "G0")))
    if guards.get("G"):
        reading = "not read as a success: a guard is raised for G"
    elif not valid_pass:
        reading = "described only (r-hat did not predict r better than q)"
    elif both:
        reading = "a self-chosen goal helps people finish what they start"
    else:
        reading = "not shown: G − P and G − G0 do not both lie wholly above 0"
    L += ["", "Rule: \"a self-chosen goal helps people finish what they start\" if both G − P and G − G0 lie wholly "
          "above 0 (guards first; the validity check must pass). P − c is the steering effect (it mixes a better "
          "predictor with no look-ahead; questions.md, the known limit).", "", f"**M3 reading: {reading}.**", ""]

    # --- co-primary: R with intent tests
    K = {a: col(a, lambda r: r["pb2"]["n_kinds"]) for a in arms}
    M = {a: col(a, lambda r: r["pb2"]["n_remade"]) for a in arms}
    with np.errstate(invalid="ignore", divide="ignore"):
        Rv = {a: (M[a].sum() / K[a].sum() if K[a].sum() else float("nan"), (W @ M[a]) / (W @ K[a])) for a in arms}
    L += ["## Co-primary: R, lineage remaking", "",
          "The share of world-new kinds first made in years 130–165 whose own recipe is made again (a `make` action) "
          "within 5 years.", "", "| arm | R | kinds | remade | remade by the inventor |", "|---|---|---|---|---|"]
    for a in arms:
        L.append(f"| {NAME[a]} | {Rv[a][0]:.4f} | {int(K[a].sum()):,} | {int(M[a].sum()):,} | "
                 f"{int(col(a, lambda r: r['pb2']['n_remade_by_inventor']).sum()):,} |")
    L += ["", "| contrast | difference [95%] |", "|---|---|"]
    for a, b in con:
        if a in arms and b in arms:
            L.append(f"| {NAME[a]} − {NAME[b]} | {fmt(*diff(Rv[a], Rv[b]))} |")

    def opp(key):
        return lambda r: r["pb2"]["opp"].get(key, 0)

    def rem(key):
        return lambda r: r["pb2"]["rem"].get(key, 0)
    L += ["", "**Intent test 1 (above chance):** remakes per adult week holding the kind's inputs, the inventor "
          "against non-inventors who held them (all; and those who also knew the recipe, described).", "",
          "| arm | inventor | others | inventor − others [95%] | others who knew it | inventor − those [95%] |",
          "|---|---|---|---|---|---|"]
    for a in arms:
        vi, vo, vk = ratio(a, rem("inv"), opp("inv")), ratio(a, rem("oth"), opp("oth")), \
            ratio(a, rem("oth"), opp("oth_knows"))
        L.append(f"| {NAME[a]} | {vi[0]:.5f} | {vo[0]:.5f} | {fmt(*diff(vi, vo))} | {vk[0]:.5f} | "
                 f"{fmt(*diff(vi, vk))} |")
    L += ["", f"(holding-weeks: inventors {int(sum(col(a, opp('inv')).sum() for a in arms)):,}, others "
          f"{int(sum(col(a, opp('oth')).sum() for a in arms)):,}, all arms together)", "",
          "**Intent test 2 (preparation):** the share of remakes preceded within 8 weeks by the maker gathering one of "
          "the recipe's materials.", "", "| arm | prepared | remakes |", "|---|---|---|"]
    PR = {a: ratio(a, pb("remakes_prepared"), pb("remakes")) for a in arms}
    for a in arms:
        L.append(f"| {NAME[a]} | {PR[a][0]:.4f} | {int(col(a, pb('remakes')).sum()):,} |")
    L += ["", "| contrast | difference [95%] |", "|---|---|"]
    for a, b in con:
        if a in arms and b in arms:
            L.append(f"| {NAME[a]} − {NAME[b]} | {fmt(*diff(PR[a], PR[b]))} |")
    L += ["", "**Intent test 3 (persistence): M5**, chains whose next decision was a food action.", "",
          "| arm | M5 | gather chains | matched chains |", "|---|---|---|---|"]
    for a in arms:
        L.append(f"| {NAME[a]} | {M5[a][0][0]:.4f} | {M5[a][1]:,} | {M5[a][2]:,} |")
    L += ["", "| contrast | difference [95%] |", "|---|---|"]
    for a, b in con:
        if a in arms and b in arms:
            L.append(f"| {NAME[a]} − {NAME[b]} | {fmt(*diff(M5[a][0], M5[b][0]))} |")
    L += ["", "\"M3 up, R null\" is a real finding, not a failure (questions.md).", ""]

    # --- described
    L += ["## Described (no frozen prediction)", ""]

    def acts(a):
        return [runs[a][s]["pb2"]["actions"] for s in seeds]
    kinds_all = sorted({k for a in arms for d in acts(a) for k in d})
    tot = {a: np.array([sum(d.values()) for d in acts(a)], float) for a in arms}
    L += ["**Action shares (adults, years 130–170; PB0's warning: a shift to social acts).**", "",
          "| action | " + " | ".join(NAME[a] for a in arms) + " |", "|---|" + "---|" * len(arms)]
    for k in kinds_all:
        L.append(f"| {k} | " + " | ".join(
            f"{sum(d.get(k, 0) for d in acts(a)) / tot[a].sum():.4f}" if tot[a].sum() else "-" for a in arms) + " |")
    soc = {}
    for a in arms:
        nu = np.array([sum(d.get(k, 0) for k in PERSON_ACTS) for d in acts(a)], float)
        with np.errstate(invalid="ignore", divide="ignore"):
            soc[a] = (nu.sum() / tot[a].sum() if tot[a].sum() else float("nan"), (W @ nu) / (W @ tot[a]))
    L += ["", "Share of acts aimed at a person (" + ", ".join(PERSON_ACTS) + "): " +
          "; ".join(f"{NAME[a]} {soc[a][0]:.4f}" for a in arms) + ". " +
          "; ".join(f"{NAME[a]} − v13 {fmt(*diff(soc[a], soc['c']))}" for a in ("P", "G", "G0", "x") if a in arms) +
          ".", ""]
    rows = [("M2 (bits beyond shuffle, per adult-year)", am("m2_mi_sum"), am("m2_person_years")),
            ("M3 among people born after year 100: gather chains made",
             am("b_m3_g_made"), am("b_m3_g_chains")),
            ("  matched chains made (born after year 100)", am("b_m3_m_made"), am("b_m3_m_chains")),
            ("makes per adult-year", lambda r: r["pb2"]["actions"].get("make", 0) * R.WPY,
             pb("adult_weeks_win")),
            ("world-new kinds per world (years 130–165)", lambda r: r["pb2"]["n_kinds"], lambda r: 1),
            ("edible food per adult (year-end census)", pb("census_food"), pb("census_adults")),
            ("goal weeks per adult week", lambda r: r["pb2"]["sums"].get("goal_weeks", sum(r["pb2"]["goals"].values())),
             pb("adult_weeks_win")),
            ("decisions falling back to q (share)", lambda r: r["pb2"]["fallback"],
             lambda r: r["pb2"]["fallback"] + r["pb2"]["steered"]),
            ("adult weeks of people born after year 100 (share)", pb("adult_weeks_born_after"), pb("adult_weeks_win"))]
    L += ["| measure | " + " | ".join(NAME[a] for a in arms) + " | P − v13 [95%] | G − v13 [95%] |",
          "|---|" + "---|" * (len(arms) + 2)]
    for label, num, den in rows:
        vals = {a: ratio(a, num, den) for a in arms}
        cells = " | ".join(f"{vals[a][0]:.4f}" for a in arms)
        dd = [fmt(*diff(vals[b], vals["c"])) if b in vals else "-" for b in ("P", "G")]
        L.append(f"| {label} | {cells} | {dd[0]} | {dd[1]} |")
    L.append("")
    for a in ("G", "G0"):
        if a not in arms:
            continue
        ad = [x for s in seeds for x in runs[a][s]["pb2"]["adopt"]]
        kept = {}
        for s in seeds:
            for k, v in runs[a][s]["pb2"]["kept"].items():
                kept[k] = kept.get(k, 0) + v
        L += [f"**Goals in {NAME[a]}:** {len(ad):,} adoptions.", "",
              "| output | direction | adoptions | mean LP at adoption | finished goals | mean weeks held |",
              "|---|---|---|---|---|---|"]
        for j, nm in enumerate(GOAL_NAMES):
            for d in (1, -1):
                sel = [x for x in ad if x[2] == j and x[3] == d]
                lps = [x[4] for x in sel if x[4] is not None]
                nk, wk = kept.get(f"{j}:{d}:n", 0), kept.get(f"{j}:{d}:weeks", 0)
                if sel or nk:
                    L.append(f"| {nm} | {'+' if d > 0 else '−'} | {len(sel):,} | "
                             f"{(sum(lps) / len(lps)) if lps else float('nan'):.4f} | {nk:,} | "
                             f"{(wk / nk) if nk else float('nan'):.1f} |")
        L.append("")
    L += ["## Population (beside every measure)", "",
          "| arm | living-weeks | adult-weeks (16–49) | extinct worlds |", "|---|---|---|---|"]
    for a in arms:
        L.append(f"| {NAME[a]} | {int(col(a, am('living_weeks')).sum()):,} | {int(col(a, am('adult_weeks')).sum()):,} "
                 f"| {sum(1 for s in seeds if runs[a][s]['extinct'])} |")
    L.append("")
    text = "\n".join(L) + "\n"
    if SMOKE:
        print(text)
        return
    (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
