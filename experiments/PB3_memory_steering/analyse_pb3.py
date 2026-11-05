"""PB3 analysis (questions.md, frozen as `PB3-frozen`); written before any data.

Order: validity (zero checks, all worlds, one fingerprint) -> guards (c0, P, P+ each against c) -> primary P - c0 on
M3 (attribution) -> co-primary P - c on M3 and P / c living-weeks (replication of PB2) -> described. Paired world
bootstrap: 10,000 replicates, NumPy seed 20261115; every ratio pooled over worlds (sum / sum), as in AM1 and PB2.

  python experiments/PB3_memory_steering/analyse_pb3.py                      # writes results.md
  python experiments/PB3_memory_steering/analyse_pb3.py --smoke --dir <folder>
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
import run_pb3 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261115)
ARMS = ("c", "c0", "P", "Pp", "x")
NAME = {"c": "v13", "c0": "v13, discount 0", "P": "P (memory)", "Pp": "P+ (memory, two-week return)", "x": "sham"}
MIN_GAIN = 0.005
GEMINI = 0.015
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
    m = re.search(r"code_pb3 fingerprint: ([0-9a-f]{64})", zero)
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
    L = ["# PB3: memory steering as a candidate law — prediction or myopia? (results)", "",
         "Frozen as `PB3-frozen`. run_pb3.py, analyse_pb3.py (written before data). Adults 16–49, years 130–170.", "",
         "## Validity", "",
         f"- Zero checks (All: PASS, same `code_pb3` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({sum(len(runs[a]) for a in ARMS)} of {len(ARMS) * len(R.SEEDS)}): "
         f"**{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_pb3`'s: **{'yes' if fps == {fp_now} else 'NO'}**", "",
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

    lw = {a: col(a, am("living_weeks")) for a in arms}

    def lw_ratio(a, b):
        with np.errstate(invalid="ignore", divide="ignore"):
            return lw[a].sum() / lw[b].sum(), *pct((W @ lw[a]) / (W @ lw[b]))

    # --- guards first
    L += ["## Guards (each arm against v13)", ""]
    guards = {}
    for a in ("c0", "P", "Pp", "x"):
        if a not in arms:
            continue
        pop = lw_ratio(a, "c")
        ext = sum(1 for s in seeds if runs[a][s]["extinct"]) - sum(1 for s in seeds if runs["c"][s]["extinct"])
        g = (["population"] if pop[0] < 0.90 and pop[2] < 1.0 else []) + (["extinctions"] if ext >= 3 else [])
        guards[a] = g
        L.append(f"- {NAME[a]}: living-weeks ratio {pop[0]:.3f} [{pop[1]:.3f}, {pop[2]:.3f}]; extinct worlds beyond "
                 f"v13's {ext:+d}" + (f" — **guard raised: {', '.join(g)} (harm: investigate)**" if g else
                                      " — no guard raised"))
    L += ["", "Rule: a guard is raised if the living-weeks ratio is below 0.90 with its upper bound below 1, or 3+ extra "
          "extinct worlds. An arm with a guard raised is not read as a success.", ""]

    # --- M3 and M5 per arm
    def chains(a, pre):
        gc, gm, mc, mm = (col(a, am(f"{pre}_{k}")) for k in ("g_chains", "g_made", "m_chains", "m_made"))
        with np.errstate(invalid="ignore", divide="ignore"):
            v = gm.sum() / gc.sum() - mm.sum() / mc.sum() if gc.sum() and mc.sum() else float("nan")
            return (v, (W @ gm) / (W @ gc) - (W @ mm) / (W @ mc)), int(gc.sum()), int(mc.sum())
    M3 = {a: chains(a, "m3") for a in arms}
    M5 = {a: chains(a, "m5") for a in arms}
    L += ["## M3, ends-directed chains", "",
          "P(made a recipe using m within 8 weeks | gathered m, a needed input of a valued recipe, holding < 1) − "
          "P(made | an opportunity-matched week).", "", "| arm | M3 | gather chains | matched chains |",
          "|---|---|---|---|"]
    for a in arms:
        L.append(f"| {NAME[a]} | {M3[a][0][0]:.4f} | {M3[a][1]:,} | {M3[a][2]:,} |")
    pairs = [("P", "c0"), ("P", "c"), ("c0", "c"), ("Pp", "P"), ("Pp", "c0"), ("Pp", "c"), ("x", "c")]
    D3 = {(a, b): diff(M3[a][0], M3[b][0]) for a, b in pairs if a in arms and b in arms}
    L += ["", "| contrast | M3 difference [95%] |", "|---|---|"]
    for (a, b), v in D3.items():
        tag = {("P", "c0"): " (primary)", ("P", "c"): " (co-primary)"}.get((a, b), "")
        L.append(f"| {NAME[a]} − {NAME[b]}{tag} | {fmt(*v)} |")
    L.append("")

    # --- primary: attribution
    pc0, c0c = D3.get(("P", "c0")), D3.get(("c0", "c"))
    if guards.get("P"):
        primary = "not read as a success: a guard is raised for P"
    elif pc0 and pc0[1] > 0 and pc0[0] >= MIN_GAIN:
        primary = "better prediction"
    elif pc0 and not pc0[1] > 0 and c0c and c0c[1] > 0:
        primary = "myopia, not prediction"
    else:
        primary = "unclear"
    L += ["## Primary: attribution (P − c0 on M3)", "",
          f"Rule: \"better prediction\" if the 95% interval of P − c0 lies wholly above 0 and its point is at least "
          f"+{MIN_GAIN}; \"myopia, not prediction\" if it does not lie wholly above 0 while c0 − c lies wholly above "
          "0; otherwise \"unclear\" (guards first).", "", f"**Primary reading: {primary}.**", "",
          f"Described: Gemini's stricter check, P − c0 ≥ +{GEMINI}: "
          f"{'yes' if pc0 and pc0[0] >= GEMINI else 'no'}.", ""]

    # --- co-primary: replication of PB2
    pc = D3.get(("P", "c"))
    lwp = lw_ratio("P", "c") if "P" in arms else (float("nan"),) * 3
    rep = bool(pc and pc[1] > 0 and lwp[1] > 1.0 and not guards.get("P"))
    L += ["## Co-primary: replication of PB2 (P − c on M3, P / c living-weeks)", "",
          f"- P − c on M3: {fmt(*pc) if pc else '-'}",
          f"- P / c living-weeks: {lwp[0]:.3f} [{lwp[1]:.3f}, {lwp[2]:.3f}]", "",
          "Rule: \"PB2's steering effect replicates\" if the M3 interval lies wholly above 0 and the living-weeks "
          "interval wholly above 1.", "",
          f"**Co-primary reading: {'PB2s steering effect replicates' if rep else 'not replicated'}.**".replace(
              "PB2s", "PB2's"), ""]

    # --- described
    L += ["## Described (no frozen prediction)", "", "**Living-weeks ratios.**", ""]
    for a, b in (("c0", "c"), ("Pp", "P"), ("Pp", "c0"), ("P", "c0")):
        if a in arms and b in arms:
            v = lw_ratio(a, b)
            L.append(f"- {NAME[a]} / {NAME[b]}: {v[0]:.3f} [{v[1]:.3f}, {v[2]:.3f}]")
    L += ["", "**M5 (chains whose next decision was a food action).**", "", "| arm | M5 |", "|---|---|"]
    for a in arms:
        L.append(f"| {NAME[a]} | {M5[a][0][0]:.4f} |")
    L += ["", "| contrast | M5 difference [95%] |", "|---|---|"]
    for a, b in pairs:
        if a in arms and b in arms:
            L.append(f"| {NAME[a]} − {NAME[b]} | {fmt(*diff(M5[a][0], M5[b][0]))} |")
    K = {a: col(a, lambda r: r["pb2"]["n_kinds"]) for a in arms}
    Mr = {a: col(a, lambda r: r["pb2"]["n_remade"]) for a in arms}
    L += ["", "**R (lineage remaking, as in PB2) and inventors' opportunities.**", "",
          "| arm | R | kinds | remade | inventor weeks holding the inputs | of which still knew the recipe | others "
          "holding |", "|---|---|---|---|---|---|---|"]
    for a in arms:
        inv = col(a, lambda r: r["pb2"]["opp"].get("inv", 0)).sum()
        know = col(a, lambda r: r["pb2"]["opp"].get("inv_knows", 0)).sum()
        oth = col(a, lambda r: r["pb2"]["opp"].get("oth", 0)).sum()
        L.append(f"| {NAME[a]} | {(Mr[a].sum() / K[a].sum()) if K[a].sum() else float('nan'):.4f} | "
                 f"{int(K[a].sum()):,} | {int(Mr[a].sum()):,} | {int(inv):,} | "
                 f"{(know / inv) if inv else float('nan'):.3f} | {int(oth):,} |")

    def acts(a):
        return [runs[a][s]["pb2"]["actions"] for s in seeds]
    kinds_all = sorted({k for a in arms for d in acts(a) for k in d})
    tot = {a: np.array([sum(d.values()) for d in acts(a)], float) for a in arms}
    L += ["", "**Action shares (adults, years 130–170).**", "",
          "| action | " + " | ".join(NAME[a] for a in arms) + " |", "|---|" + "---|" * len(arms)]
    for k in kinds_all:
        L.append(f"| {k} | " + " | ".join(
            f"{sum(d.get(k, 0) for d in acts(a)) / tot[a].sum():.4f}" if tot[a].sum() else "-" for a in arms) + " |")
    soc = {}
    for a in arms:
        nu = np.array([sum(d.get(k, 0) for k in PERSON_ACTS) for d in acts(a)], float)
        with np.errstate(invalid="ignore", divide="ignore"):
            soc[a] = (nu.sum() / tot[a].sum() if tot[a].sum() else float("nan"), (W @ nu) / (W @ tot[a]))
    L += ["", "Share of acts aimed at a person: " + "; ".join(f"{NAME[a]} {soc[a][0]:.4f}" for a in arms) + ". " +
          "; ".join(f"{NAME[a]} − {NAME[b]} {fmt(*diff(soc[a], soc[b]))}" for a, b in (("P", "c0"), ("P", "c"),
                                                                                    ("c0", "c"))
                    if a in arms and b in arms) + ".", ""]
    rows = [("M2 (bits beyond shuffle, per adult-year)", am("m2_mi_sum"), am("m2_person_years")),
            ("M3 among people born after year 100: gather chains made", am("b_m3_g_made"), am("b_m3_g_chains")),
            ("  matched chains made (born after year 100)", am("b_m3_m_made"), am("b_m3_m_chains")),
            ("makes per adult-year", lambda r: r["pb2"]["actions"].get("make", 0) * R.WPY, pb("adult_weeks_win")),
            ("world-new kinds per world (years 130–165)", lambda r: r["pb2"]["n_kinds"], lambda r: 1),
            ("edible food per adult (year-end census)", pb("census_food"), pb("census_adults")),
            ("decisions falling back to q (share)", lambda r: r["pb2"]["fallback"],
             lambda r: r["pb2"]["fallback"] + r["pb2"]["steered"]),
            ("adult weeks of people born after year 100 (share)", pb("adult_weeks_born_after"), pb("adult_weeks_win"))]
    L += ["| measure | " + " | ".join(NAME[a] for a in arms) + " | P − c0 [95%] | c0 − c [95%] |",
          "|---|" + "---|" * (len(arms) + 2)]
    for label, num, den in rows:
        vals = {a: ratio(a, num, den) for a in arms}
        cells = " | ".join(f"{vals[a][0]:.4f}" for a in arms)
        dd = [fmt(*diff(vals[x], vals[y])) if x in vals and y in vals else "-" for x, y in (("P", "c0"), ("c0", "c"))]
        L.append(f"| {label} | {cells} | {dd[0]} | {dd[1]} |")
    L += ["", "## Population (beside every measure)", "",
          "| arm | living-weeks | adult-weeks (16–49) | extinct worlds |", "|---|---|---|---|"]
    for a in arms:
        L.append(f"| {NAME[a]} | {int(lw[a].sum()):,} | {int(col(a, am('adult_weeks')).sum()):,} | "
                 f"{sum(1 for s in seeds if runs[a][s]['extinct'])} |")
    L.append("")
    text = "\n".join(L) + "\n"
    if SMOKE:
        print(text)
        return
    (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
