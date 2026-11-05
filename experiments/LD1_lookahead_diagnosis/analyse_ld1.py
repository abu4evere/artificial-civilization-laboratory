"""LD1 analysis (questions.md, frozen as `LD1-frozen`); written before any data.

Part A: the expected make share of adult decisions in v13 under three score versions (actual, scale, none; amendment 1)
against the actual share in the paired c0 worlds; recovery f = (version - actual) / (c0 - actual); the reading.
Part B: the stage each world-new kind reached on its way to being remade, by arm; the stage where most stop.
Paired world bootstrap: 10,000 replicates, NumPy seed 20261116; shares pooled over worlds (sum / sum).

  python experiments/LD1_lookahead_diagnosis/analyse_ld1.py                      # writes results.md
  python experiments/LD1_lookahead_diagnosis/analyse_ld1.py --smoke --dir <folder>
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
import run_ld1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261116)
ARMS = ("c", "c0")
NAME = {"c": "v13", "c0": "v13, discount 0"}
CLS = ("make", "gather", "forage", "play", "person")
STAGE = {0: "never held the recipe at a week's end", 1: "held the recipe, never with its inputs",
         2: "held both, never while free and valuing it", 3: "free and valuing it, never offered",
         4: "offered, never chosen", 5: "remade"}
TARGET = {0: "recipe memory (rules review R1)", 1: "opportunity, or an intention to gather for a past success",
          2: "the 'already holding one' and value rules", 3: "the single-offer make rule (rules review R3)",
          4: "valuation at choice"}


def pct(x):
    x = x[np.isfinite(x)]
    return (float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))) if len(x) else (float("nan"),) * 2


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
    L = ["# LD1: why the habit look-ahead locks choices, and where remaking fails (results)", "",
         "Frozen as `LD1-frozen`. run_ld1.py, analyse_ld1.py (written before data). Read-only on v13; adults 16–49, "
         "years 130–170.", "", "## Validity", "",
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

    def sm(key):
        return lambda r: r["sums"].get(key, 0)

    dec = {a: col(a, sm("decisions")) for a in ARMS}

    def share(a, v, k):
        nu = col(a, sm(f"sh_{v}_{k}"))
        with np.errstate(invalid="ignore", divide="ignore"):
            return nu.sum() / dec[a].sum(), (W @ nu) / (W @ dec[a])

    # --- Part A
    sh = {(a, v, k): share(a, v, k) for a in ARMS for v in R.VERSIONS for k in CLS}
    L += ["## Part A: the look-ahead", "",
          "Expected share of adult decisions (softmax probabilities of all scored options) under three score versions (amendment 1). "
          "v13's decisions; c0's own decisions for comparison.", "",
          "| class | v13 actual | v13 scale | v13 none | c0 actual |", "|---|---|---|---|---|"]
    for k in CLS:
        L.append(f"| {k} | " + " | ".join(f"{sh[('c', v, k)][0]:.4f}" for v in R.VERSIONS) +
                 f" | {sh[('c0', 'actual', k)][0]:.4f} |")
    a0, c0v = sh[("c", "actual", "make")], sh[("c0", "actual", "make")]
    rec = {}
    for v in ("scale", "none"):
        x = sh[("c", v, "make")]
        with np.errstate(invalid="ignore", divide="ignore"):
            rec[v] = ((x[0] - a0[0]) / (c0v[0] - a0[0]), (x[1] - a0[1]) / (c0v[1] - a0[1]))
    L += ["", "**Recovery of the make share** f = (version − actual) ÷ (c0 − actual):", ""]
    for v in ("scale", "none"):
        lo, hi = pct(rec[v][1])
        L.append(f"- {v}: {rec[v][0]:.3f} [{lo:.3f}, {hi:.3f}]")
    fs, fn = rec["scale"][0], rec["none"][0]
    if fn >= 0.5:
        reading = "direction" + (" (the scale version also recovers)" if fs >= 0.5 else "")
    elif fs >= 0.5:
        reading = "scale"
    else:
        reading = "dynamics"
    label = ""
    L += ["", "Rule (amendment 1): \"direction\" if f_none >= 0.5; \"scale\" if f_none < 0.5 and f_scale >= 0.5; "
          "\"dynamics\" if both are below 0.5 (the lock lies in the states people reach).", "",
          f"**Primary A reading: {reading}{label}.**", ""]

    def ratio(a, num, den):
        nu, de = col(a, num), col(a, den)
        with np.errstate(invalid="ignore", divide="ignore"):
            return (nu.sum() / de.sum() if de.sum() else float("nan")), (W @ nu) / (W @ de)
    rows = [("q entries at the clamp (|q| ≥ 1.49), adults' year ends", sm("census_clamp"), sm("census_entries")),
            ("mean |q|", sm("census_absq"), sm("census_entries")),
            ("decisions whose top option changes without the habit term", sm("top_changes"), sm("decisions")),
            ("mean |habit term| ÷ mean |rest of the score|", sm("abs_h"), sm("abs_rest")),
            ("approximation gap mean |q − (q_r + q_f)|", sm("gap_sum"), sm("gap_n")),
            ("at make offers: 0.6 × (q_f of make − mean q_f of the options)", sm("mk_qf_diff"), sm("mk_n")),
            ("at make offers: 0.6 × (q_r of make − mean q_r of the options)", sm("mk_qr_diff"), sm("mk_n"))]
    L += ["**Described.**", "", "| measure | v13 | c0 |", "|---|---|---|"]
    for label_, num, den in rows:
        L.append(f"| {label_} | " + " | ".join(f"{ratio(a, num, den)[0]:.4f}" for a in ARMS) + " |")
    acts = sorted({k[3:-2] for a in ARMS for s in seeds for k in runs[a][s]["sums"] if k.startswith("la_")
                   and k.endswith("_n") and not k.startswith("la_band")})
    L += ["", "The look-ahead term at learning, 0.8 × max next q (v13; c0's is 0 by construction), by action learned "
          "and by the next week's food band:", "", "| action | mean term | updates |", "|---|---|---|"]
    for a_ in acts:
        v_, _ = ratio("c", sm(f"la_{a_}_sum"), sm(f"la_{a_}_n"))
        L.append(f"| {a_} | {v_:+.4f} | {int(col('c', sm(f'la_{a_}_n')).sum()):,} |")
    for b in range(4):
        v_, _ = ratio("c", sm(f"la_band{b}_sum"), sm(f"la_band{b}_n"))
        L.append(f"| next food band {b} | {v_:+.4f} | {int(col('c', sm(f'la_band{b}_n')).sum()):,} |")
    ex = {a: (sum(runs[a][s]["exact"][0] for s in seeds), sum(runs[a][s]["exact"][1] for s in seeds)) for a in ARMS}
    L += ["", "Exactness at each world's end (clean entries, q = q_r + q_f to 1e-9): " +
          "; ".join(f"{NAME[a]} {ex[a][1]:,} wrong of {ex[a][0]:,}" for a in ARMS) + ".", ""]

    # --- Part B
    L += ["## Part B: where remaking fails", "",
          "World-new kinds made in play in years 130–165, followed 5 years in their inventor's weeks; the furthest "
          "stage reached.", "", "| stage | " + " | ".join(NAME[a] for a in ARMS) + " |", "|---|---|---|"]
    K = {a: col(a, lambda r: r["n_kinds"]) for a in ARMS}
    stg = {}
    for st in range(6):
        for a in ARMS:
            nu = col(a, lambda r, st=st: r["stages"].get(str(st), 0))
            with np.errstate(invalid="ignore", divide="ignore"):
                stg[(a, st)] = (nu.sum() / K[a].sum() if K[a].sum() else float("nan"), (W @ nu) / (W @ K[a]))
        L.append(f"| {st}. {STAGE[st]} | " + " | ".join(
            "{:.3f} [{:.3f}, {:.3f}]".format(stg[(a, st)][0], *pct(stg[(a, st)][1])) for a in ARMS) + " |")
    L.append(f"| kinds | " + " | ".join(f"{int(K[a].sum()):,}" for a in ARMS) + " |")
    for a in ARMS:
        top = max(range(5), key=lambda st: stg[(a, st)][0])
        L += ["", f"**Primary B, {NAME[a]}: most kinds stop at stage {top} ({STAGE[top]}): "
                  f"{stg[(a, top)][0]:.3f}. The first R target decided before data: {TARGET[top]}.**"]
    L += ["", "**Described.**", ""]
    for a in ARMS:
        fl = sum(runs[a][s]["first_week_lost"] for s in seeds)
        dl = sum(runs[a][s]["died_lost"] for s in seeds)
        sp = sum(runs[a][s]["spread"] for s in seeds)
        lw = sorted(x for s in seeds for x in runs[a][s]["lost_weeks"])
        med = lw[len(lw) // 2] if lw else float("nan")
        kk = int(K[a].sum())
        L.append(f"- {NAME[a]}: recipe gone by the first week's end {fl:,} of {kk:,}; lost because the inventor died "
                 f"{dl:,}; learned by anyone else {sp:,}; median weeks until lost {med} (of {len(lw):,} lost).")
    L += ["", "## Population (beside every measure)", "", "| world | living-weeks | adult-weeks (16–49) | extinct worlds |",
          "|---|---|---|---|"]
    for a in ARMS:
        L.append(f"| {NAME[a]} | {int(col(a, sm('living_weeks')).sum()):,} | {int(col(a, sm('adult_weeks')).sum()):,} | "
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
