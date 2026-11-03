"""HN1 analysis, written before any data (questions.md, frozen as `HN1-frozen`).

  python experiments/HN1_hunting_funnel/analyse_hn1.py                      # writes results.md
  python experiments/HN1_hunting_funnel/analyse_hn1.py --smoke --dir <folder>
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
import run_hn1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261109)
TABLE = {"rabbit": 0.40, "deer": 0.16, "bison": 0.10, "fish": 0.25}     # fauna.SPECIES "catch" (unused, F7)


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
    m = re.search(r"code_v11 fingerprint: ([0-9a-f]{64})", zero)
    zero_ok = "All: PASS" in zero and m is not None and m.group(1) == fp_now
    seeds = sorted(runs) if SMOKE else sorted(R.SEEDS)
    present = len(seeds) > 0 if SMOKE else sorted(runs) == seeds
    fps = {r["code_hash"] for r in runs.values()} | {r["code_hash_after"] for r in runs.values()}
    ok = bool(zero_ok and present and fps == {fp_now})
    L = ["# HN1: Where do v11's hunts fail? (results)", "",
         "Frozen as `HN1-frozen`. run_hn1.py, analyse_hn1.py (written before data).", "", "## Validity", "",
         f"- Zero checks (All: PASS, same `code_v11` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({len(runs)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_v11`'s: **{'yes' if fps == {fp_now} else 'NO'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
        print("\n".join(L))
        return
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def col(key):
        return np.array([float(runs[s]["sums"].get(key, 0)) for s in seeds])

    def ratio(num, den):
        a, b = col(num), col(den)
        with np.errstate(invalid="ignore", divide="ignore"):
            return (a.sum() / b.sum() if b.sum() else float("nan")), (W @ a) / (W @ b)

    # --- the routing rule: F = no prey / failed
    a, b = col("no_prey"), col("roll_failed")
    with np.errstate(invalid="ignore", divide="ignore"):
        F = a.sum() / (a.sum() + b.sum()) if (a.sum() + b.sum()) else float("nan")
        Frep = (W @ a) / (W @ a + W @ b)
    Flo, Fhi = pct(Frep)
    route = "prey encounter (density)" if F > 0.5 else "the base chance (hunt_base_chance)"
    straddle = Flo <= 0.5 <= Fhi
    L += ["## The routing rule for HR1 (frozen)", "",
          f"- F = failed hunts with no prey on the tile ÷ all failed hunts = **{F:.4f} [{Flo:.4f}, {Fhi:.4f}]** "
          f"({int(a.sum()):,} with no prey, {int(b.sum()):,} with a failed roll).",
          f"- **HR1 calibrates {route}.**" + (" The interval straddles 0.5: the council is asked before HR1 is frozen."
                                               if straddle else ""), ""]

    # --- the return ratio (pooled)
    hk, hw = col("kept_sum"), col("hunter_weeks")
    fk, fw = col("forage_sum"), col("forage_weeks")
    with np.errstate(invalid="ignore", divide="ignore"):
        Rp = (hk.sum() / hw.sum()) / (fk.sum() / fw.sum())
        Rrep = ((W @ hk) / (W @ hw)) / ((W @ fk) / (W @ fw))
    Rlo, Rhi = pct(Rrep)
    # matched: each hunter-week against the same person's forage-weeks in the same season, year and plant band
    num_m, den_m, used, dropped = np.zeros(n), np.zeros(n), 0, 0
    for j, s in enumerate(seeds):
        fm = {(x[0], x[1], x[2], x[3]): (x[4], x[5]) for x in runs[s]["forage_match"]}
        for h in runs[s]["hunts"]:
            g = fm.get((h[0], h[1], h[2], h[3]))
            if g is None or not g[1]:
                dropped += 1
                continue
            used += 1
            num_m[j] += h[8]
            den_m[j] += g[0] / g[1]
    with np.errstate(invalid="ignore", divide="ignore"):
        Rm = num_m.sum() / den_m.sum() if den_m.sum() else float("nan")
        Rmrep = (W @ num_m) / (W @ den_m)
    Rmlo, Rmhi = pct(Rmrep)
    L += ["## The return ratio (HR1's target: the Aché's about 1.1; accepted range 0.5–1.5)", "",
          f"- **Pooled:** food kept per adult hunter-week ÷ food per adult forage-week = **{Rp:.4f} [{Rlo:.4f}, {Rhi:.4f}]** "
          f"({int(hw.sum()):,} hunter-weeks, {int(fw.sum()):,} forage-weeks).",
          f"- **Matched** (same person, season, year and plant-stock band): **{Rm:.4f} [{Rmlo:.4f}, {Rmhi:.4f}]** "
          f"({used:,} hunter-weeks matched, {dropped:,} without a match, dropped).", ""]

    # --- the funnel, armed and bare-handed
    L += ["## The failure funnel (shares of adult hunter-weeks)", "",
          "| hunters | hunter-weeks | (a) no prey | (b) roll failed | (c) success | food kept per hunter-week |",
          "|---|---|---|---|---|---|"]
    for k, lab in (("", "all"), ("_armed", "armed"), ("_bare", "bare-handed")):
        tot = col("hunter_weeks" + k).sum()
        if not tot:
            L.append(f"| {lab} | 0 | - | - | - | - |")
            continue
        L.append(f"| {lab} | {int(tot):,} | {col('no_prey' + k).sum() / tot:.4f} | {col('roll_failed' + k).sum() / tot:.4f} | "
                 f"{col('success' + k).sum() / tot:.4f} | {col('kept_sum' + k).sum() / tot:.3f} |")
    sh, ks, ex, sc = col("share_sum").sum(), col("kept_sum_success").sum(), col("expected_sum").sum(), col("success").sum()
    L += ["", f"- **Meat lost to carrying room** (successes): {(1 - ks / sh) if sh else float('nan'):.4f} of the meat "
              "share.",
          f"- **F8, expected against realized:** the decision's expected share per success averages "
          f"{(ex / sc) if sc else float('nan'):.2f}; the meat share actually taken averages {(sh / sc) if sc else float('nan'):.2f} "
          f"and the meat kept {(ks / sc) if sc else float('nan'):.2f} (successes {int(sc):,}).",
          f"- **Population beside it:** {int(col('living_weeks').sum()):,} living-weeks, {int(col('adult_weeks').sum()):,} "
          f"adult-weeks (16–49); extinct worlds {sum(1 for s in seeds if runs[s]['extinct'])}.", ""]

    # --- F7: success by species on single-species tiles
    L += ["## F7: success by species (tiles with a single prey species), against the unused table rates", "",
          "| species | attempts | successes | rate | table rate (unused) |", "|---|---|---|---|---|"]
    for sp in ("rabbit", "deer", "bison", "fish"):
        t = sum(runs[s]["species_try"].get(sp, 0) for s in seeds)
        h = sum(runs[s]["species_hit"].get(sp, 0) for s in seeds)
        L.append(f"| {sp} | {t:,} | {h:,} | {(h / t) if t else float('nan'):.4f} | {TABLE[sp]:.2f} |")
    L.append("")
    text = "\n".join(L) + "\n"
    if SMOKE:
        print(text)
        return
    (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
