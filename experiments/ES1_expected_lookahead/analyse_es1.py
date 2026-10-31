"""ES1 analysis, written before any data (questions.md, frozen as `ES1-frozen`; operational note 1).

  python experiments/ES1_expected_lookahead/analyse_es1.py            # writes results.md
  python experiments/ES1_expected_lookahead/analyse_es1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_es1 import ARMS, SEEDS, WPY  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261031)
NAME = {"c": "v11", "e": "e (expected look-ahead)", "x": "sham"}
SHOW = ("forage", "gather", "talk", "give", "rest", "explore", "play", "make", "hunt", "care", "put", "take")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {a: {} for a in ARMS}
    for f in sorted(glob.glob(str(OUTDIR / "*_seed_*.json"))):
        r = json.load(open(f))
        runs[r["arm"]][r["seed"]] = r
    zero = (OUTDIR / "zero.txt").read_text(encoding="utf-8") if (OUTDIR / "zero.txt").exists() else ""
    present = all(sorted(runs[a]) == sorted(SEEDS) for a in ARMS)
    fps = {r["code_hash"] for a in ARMS for r in runs[a].values()} | \
          {r["code_hash_after"] for a in ARMS for r in runs[a].values()}
    mism = sum(sum(r["mismatch"].values()) for a in ARMS for r in runs[a].values())
    ok = "All: PASS" in zero and present and len(fps) == 1 and mism == 0
    L = ["# ES1 — Do minds learn more accurately with an expected look-ahead? Results", "",
         "Frozen as `ES1-frozen` (operational note 1). run_es1.py, analyse_es1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({sum(len(runs[a]) for a in ARMS)} of {len(SEEDS) * len(ARMS)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint (`code_es1`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- Every habit update replays under its arm's rule (mismatches 0): **{'yes' if mism == 0 else f'NO ({mism})'}**",
         "", f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    seeds = sorted(set(runs["c"]) & set(runs["e"]) & set(runs["x"]))
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))])

    def cal(a, field, act=None):
        j = ["n", "sum_abs", "sum_signed", "censored"].index(field)
        return np.array([float(sum(v[j] for k, v in runs[a][s]["cal"].items() if act is None or k == act))
                         for s in seeds])

    def col(a, k):
        return np.array([float(runs[a][s]["sums"].get(k, 0.0)) for s in seeds])

    def ratio(num, den):
        point = num.sum() / den.sum() if den.sum() else float("nan")
        with np.errstate(invalid="ignore", divide="ignore"):
            reps = (W @ num) / (W @ den)
        return point, reps

    def diff(num, den, a, b="c"):
        pa, ra = ratio(num[a], den[a])
        pb, rb = ratio(num[b], den[b])
        lo, hi = np.nanpercentile(ra - rb, [2.5, 97.5])
        return pa - pb, lo, hi

    def rat(num, den, a, b="c"):
        pa, ra = ratio(num[a], den[a])
        pb, rb = ratio(num[b], den[b])
        with np.errstate(invalid="ignore", divide="ignore"):
            lo, hi = np.nanpercentile(ra / rb, [2.5, 97.5])
        return pa / pb if pb else float("nan"), lo, hi

    ext = {a: sum(1 for s in seeds if runs[a][s]["extinct"]) for a in ARMS}
    L += [f"Paired seeds: {n}. Extinct: v11 {ext['c']}, e {ext['e']}, sham {ext['x']}.", ""]

    # primary
    ABS = {a: cal(a, "sum_abs") for a in ARMS}
    NN = {a: cal(a, "n") for a in ARMS}
    de, dx = diff(ABS, NN, "e"), diff(ABS, NN, "x")
    L += ["## Primary — calibration error across all actions: mean |q - G| (habit updates started in years 100-200)", "",
          "| arm | mean abs(q - G) | updates closed | censored at death |", "|---|---|---|---|"]
    for a in ARMS:
        L.append(f"| {NAME[a]} | {ratio(ABS[a], NN[a])[0]:.4f} | {NN[a].sum():,.0f} | {cal(a, 'censored').sum():,.0f} |")
    L += ["", f"**e - v11: {de[0]:+.4f} [{de[1]:+.4f}, {de[2]:+.4f}]**; sham - v11: {dx[0]:+.4f} [{dx[1]:+.4f}, {dx[2]:+.4f}].", ""]

    # secondary: signed bias by action
    L += ["## Secondary — signed bias q - G by action (years 100-200)", "", "| action | v11 | e | sham |", "|---|---|---|---|"]
    for act in SHOW:
        cells = []
        for a in ARMS:
            nn, ss = cal(a, "n", act), cal(a, "sum_signed", act)
            cells.append(f"{ss.sum() / nn.sum():+.3f}" if nn.sum() else "-")
        L.append(f"| {act} | " + " | ".join(cells) + " |")
    L.append("")
    ay = {a: col(a, "adult_weeks") / WPY for a in ARMS}
    mk = {a: col(a, "adult_makes") for a in ARMS}
    fw = {a: col(a, "food_with") for a in ARMS}
    tool = {a: col(a, "food_with") - col(a, "food_without") for a in ARMS}
    L += ["| secondary (years 100-200) | v11 | e | sham | e ÷ v11 [95%] |", "|---|---|---|---|---|"]
    for label, num, den, d in (("makes per adult-year", mk, ay, 3), ("foraged food per adult-year", fw, ay, 1),
                               ("tools' share of foraged food", tool, fw, 4)):
        r = rat(num, den, "e")
        L.append(f"| {label} | " + " | ".join(f"{ratio(num[a], den[a])[0]:.{d}f}" for a in ARMS) +
                 f" | {r[0]:.3f} [{r[1]:.3f}, {r[2]:.3f}] |")
    L.append("")

    # guards
    pop = {a: col(a, "living_weeks") for a in ARMS}
    span = {a: np.full(n, 100.0 * WPY) for a in ARMS}
    ad = {a: col(a, "adult_deaths") * 1000.0 for a in ARMS}
    flags = {}
    rp, rpx = rat(pop, span, "e"), rat(pop, span, "x")
    flags["population"] = rp[0] < 0.90 and rp[2] < 1.0
    dd, ddx = diff(ad, ay, "e"), diff(ad, ay, "x")
    base = ratio(ad["c"], ay["c"])[0]
    flags["adult deaths"] = dd[0] > 0 and dd[1] > 0 and dd[0] > 0.10 * base
    flags["extinctions"] = ext["e"] - ext["c"] >= 3
    L += ["## Guards", "", "| guard | e against v11 [95%] | sham against v11 | raised |", "|---|---|---|---|",
          f"| population (e ÷ v11 < 0.90, upper < 1) | {rp[0]:.3f} [{rp[1]:.3f}, {rp[2]:.3f}] | {rpx[0]:.3f} | "
          f"{'**RAISED**' if flags['population'] else 'no'} |",
          f"| adult deaths per 1,000 adult-years (e − v11 > 0, lower > 0, > 10% of v11's {base:.1f}) | "
          f"{dd[0]:+.2f} [{dd[1]:+.2f}, {dd[2]:+.2f}] | {ddx[0]:+.2f} | {'**RAISED**' if flags['adult deaths'] else 'no'} |",
          f"| extinctions (e − v11 ≥ 3) | {ext['e'] - ext['c']:+d} | {ext['x'] - ext['c']:+d} | "
          f"{'**RAISED**' if flags['extinctions'] else 'no'} |", ""]

    supported = de[0] < 0 and de[2] < 0 and de[0] < dx[0] and not any(flags.values())
    L += ["## The frozen decision", "",
          f"- e - v11 {de[0]:+.4f} [{de[1]:+.4f}, {de[2]:+.4f}] (< 0 with upper < 0); sham - v11 {dx[0]:+.4f} (e must be "
          f"below it); guard flags: {', '.join(k for k, v in flags.items() if v) or 'none'}.", "",
          f"**{'SUPPORTED' if supported else 'NOT SUPPORTED'}.** (A test in a copy; making is reported, not decisive; "
          "adoption only by the safe path in CLAUDE.md, with a confirmatory run.)", ""]
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
