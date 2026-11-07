"""FP1 analysis, written before any data (questions.md, frozen as `FP1-frozen`). A table beside the evidence; no pass/fail.

  python experiments/FP1_food_production_by_age/analyse_fp1.py                      # writes results.md
  python experiments/FP1_food_production_by_age/analyse_fp1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_fp1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261107)
BANDS = [b[2] for b in R.BANDS]
GROWN = ("16-29", "30-39", "40-49", "50+")
CHILD = ("0-2", "3-7", "8-11", "12-15")
TRANSFER_IN = ("fed_in", "by:give", "act:take", "act:steal", "death:inherited")


def pct(x):
    x = x[np.isfinite(x)]
    return (float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))) if len(x) else (float("nan"),) * 2


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {}
    for f in sorted(glob.glob(str(OUTDIR / "c_seed_*.json"))):
        r = json.load(open(f))
        runs[r["seed"]] = r
    zero = ""
    for name in ("zero_cloud.log", "zero_local.log"):
        if (HERE / name).exists():
            zero = (HERE / name).read_text(encoding="utf-8", errors="replace")
            break
    R.base.setup(R.CODE)
    fp_now = R.base.fingerprint(R.CODE)
    m = re.search(r"code_v15 fingerprint: ([0-9a-f]{64})", zero)
    zero_ok = "All: PASS" in zero and m is not None and m.group(1) == fp_now
    seeds = sorted(runs) if SMOKE else sorted(R.SEEDS)
    present = SMOKE or sorted(runs) == seeds
    fps = {r["code_hash"] for r in runs.values()} | {r["code_hash_after"] for r in runs.values()}
    cons = all(r["n_residual"] == 0 for r in runs.values())
    ok = bool(zero_ok and present and fps == {fp_now} and cons)
    L = ["# FP1: food production by age in nature v15, against forager evidence (results)", "",
         "Frozen as `FP1-frozen`. run_fp1.py, analyse_fp1.py (written before data). A table beside the evidence; no "
         "pass/fail.", "", "## Validity", "",
         f"- Zero checks (All: PASS, `code_v15` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({len(runs)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_v15`'s: **{'yes' if fps == {fp_now} else 'NO'}**",
         f"- Every person-week in every world conserves held food (breaches: "
         f"{sum(r['n_residual'] for r in runs.values())}): **{'yes' if cons else 'NO'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        finish(L)
        return
    seeds = [s for s in seeds if s in runs]
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)
    sexes = sorted({k.split("|")[1] for r in runs.values() for k in r["sums"]})

    def col(keys, field):
        return np.array([sum(float(runs[s]["sums"].get(k, {}).get(field, 0.0)) for k in keys) for s in seeds])

    def ratio(keys, num, den):
        nu = col(keys, num) if isinstance(num, str) else sum(col(keys, f) for f in num)
        de = col(keys, den)
        with np.errstate(invalid="ignore", divide="ignore"):
            return (nu.sum() / de.sum() if de.sum() else float("nan")), (W @ nu) / (W @ de)

    def fmt(t):
        lo, hi = pct(t[1])
        return f"{t[0]:.3f} [{lo:.3f}, {hi:.3f}]"

    # 1. net production by age band and sex
    L += ["## 1. Production ÷ need by age band and sex (forage + hunt, over all weeks) [95%, worlds resampled]", "",
          "| band | sex | person-weeks | production per person-week | need per person-week | production ÷ need |",
          "|---|---|---|---|---|---|"]
    cross = {}
    for sx in sexes:
        for b in BANDS:
            k = [f"{b}|{sx}"]
            pw = col(k, "person_weeks").sum()
            if not pw:
                continue
            r = ratio(k, "production", "need")
            L.append(f"| {b} | {sx} | {int(pw):,} | {col(k, 'production').sum() / pw:.3f} | {col(k, 'need').sum() / pw:.3f} "
                     f"| {fmt(r)} |")
            if sx not in cross and r[0] >= 1.0:
                cross[sx] = b
    L += ["", "Crossover (the first band whose production ÷ need is at least 1): " +
          "; ".join(f"{sx}: {cross.get(sx, 'none')}" for sx in sexes) +
          ". Evidence (Kaplan et al. 2000): no forager child produced as much as consumed until the mid-to-late teens.", ""]

    # 2. prime adults
    L += ["## 2. Prime adults: production ÷ need, over all weeks and per active week (forage or hunt)", "",
          "| band | sex | all weeks | per active week | share of weeks active |", "|---|---|---|---|---|"]
    for sx in sexes:
        for b in ("30-39", "40-49"):
            k = [f"{b}|{sx}"]
            if not col(k, "person_weeks").sum():
                continue
            L.append(f"| {b} | {sx} | {fmt(ratio(k, 'production', 'need'))} | "
                     f"{fmt(ratio(k, 'active_production', 'active_need'))} | {fmt(ratio(k, 'active_weeks', 'person_weeks'))} |")
    L += ["", "Evidence (Kaplan et al. 2000, Table 2 ÷ Table 3, the assistant's arithmetic): grown men's production ÷ "
          "per-capita intake 1.37–3.22 (eight societies), women's 0.39–1.64. Per-capita intake counts children as full "
          "consumers, and ACL's need is a fixed requirement: shape and direction, not level.", ""]

    # 3. hunted share
    allk = [f"{b}|{sx}" for b in BANDS for sx in sexes]
    acq = col(allk, "production") + sum(np.clip(col(allk, f), 0, None) for f in TRANSFER_IN)
    hs = ratio(allk, "hunt", "production")
    L += ["## 3. The hunted share", "", f"- Of production (forage + hunt): **{fmt(hs)}**.",
          f"- Hunt per person-week: {col(allk, 'hunt').sum() / col(allk, 'person_weeks').sum():.4f}; of all food "
          f"acquired (production + transfers in): {col(allk, 'hunt').sum() / acq.sum():.4f}.",
          "- Evidence (Kaplan et al. 2000, Table 3): 26–78% of the diet hunted over ten societies, median 68.7%.", ""]

    # 4. action budget of the grown
    acts = Counter()
    offer = Counter()
    for s in seeds:
        for k, v in runs[s]["acts"].items():
            if k.split("|")[0] in GROWN:
                acts.update(v)
        for k, v in runs[s]["offer"].items():
            if k.split("|")[0] in GROWN:
                offer.update(v)
    tot = sum(acts.values()) or 1
    L += ["## 4. The action budget of the grown (16 and over): share of person-weeks", "",
          "| action | weeks | share |", "|---|---|---|"]
    for a, v in acts.most_common():
        L.append(f"| {a} | {v:,} | {v / tot:.4f} |")
    L += ["", f"Forage offered in {offer['forage_offered']:,} of {tot:,} grown weeks, chosen {offer['forage_chosen']:,}; "
          f"hunt offered {offer['hunt_offered']:,}, chosen {offer['hunt_chosen']:,}.", ""]
    hunts = Counter()
    for s in seeds:
        hunts.update(runs[s]["hunts"])
    sizes = sorted({int(k.split("_")[0]) for k in hunts})
    L += ["Hunts by party size (tried, succeeded): " +
          "; ".join(f"{z}: {hunts[f'{z}_tried']:,}, {hunts[f'{z}_succeeded']:,}" for z in sizes) + ".", ""]

    # 5. losses
    L += ["## 5. Losses and unmet need", "", "| band | rot ÷ production | unmet ÷ need |", "|---|---|---|"]
    for b in BANDS:
        k = [f"{b}|{sx}" for sx in sexes]
        pr, nd = col(k, "production").sum(), col(k, "need").sum()
        L.append(f"| {b} | {(-col(k, 'rot').sum()) / pr if pr else float('nan'):.4f} | "
                 f"{col(k, 'unmet').sum() / nd if nd else float('nan'):.4f} |")
    L.append("")

    # 6. what children receive
    ck = [f"{b}|{sx}" for b in CHILD for sx in sexes]
    parts = {f: np.clip(col(ck, f), 0, None).sum() for f in TRANSFER_IN}
    own = col(ck, "production").sum()
    total = sum(parts.values()) + own
    L += ["## 6. Where children's food comes from (under 16)", "",
          "| source | share |", "|---|---|", f"| their own production | {own / total if total else float('nan'):.4f} |"]
    for f, v in parts.items():
        L.append(f"| {f} | {v / total if total else float('nan'):.4f} |")
    L.append("")
    finish(L)


def finish(L):
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
