"""VA1 analysis (questions.md, frozen as `VA1-frozen`); written before any data.

Primary 1: the share of kinds used by their inventor before the recipe was lost ("unvalued at birth dominates" if
below 0.5 with the upper bound below 0.5). Primary 2: counterfactual survival of the 12-cap at invention under v_first
(the first use's felt value, among used kinds) and v_sim (similarity value), against the share actually holding the
recipe at the first week's end. Primary 3: the correlation of v_sim with the first felt value among kinds used and
with a v_sim ("similar experience is informative" if the 95% interval lies wholly above 0.2). World bootstrap: 10,000
replicates, NumPy seed 20261119; shares pooled over worlds.

  python experiments/VA1_value_at_invention/analyse_va1.py                      # writes results.md
  python experiments/VA1_value_at_invention/analyse_va1.py --smoke --dir <folder>
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
import run_va1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261119)
F = {k: i for i, k in enumerate(["full", "minval", "vsim", "used_before_loss", "n_uses", "first_felt",
                                 "first_use_week", "lost_week", "held_first_week", "stage", "vmean"])}


def pct(x):
    x = np.asarray(x, float)
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
    m = re.search(r"code_v13 fingerprint: ([0-9a-f]{64})", zero)
    zero_ok = "All: PASS" in zero and m is not None and m.group(1) == fp_now
    seeds = sorted(runs) if SMOKE else sorted(R.SEEDS)
    present = len(seeds) > 0 if SMOKE else sorted(runs) == seeds
    fps = {r["code_hash"] for r in runs.values()} | {r["code_hash_after"] for r in runs.values()}
    ok = bool(zero_ok and present and fps == {fp_now})
    L = ["# VA1: is a new invention valued before it is lost? (results)", "",
         "Frozen as `VA1-frozen`. run_va1.py, analyse_va1.py (written before data). Read-only on v13; kinds first made "
         "in years 130–165, followed 5 years.", "", "## Validity", "",
         f"- Zero checks (All: PASS, same `code_v13` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({len(runs)} of {len(R.SEEDS)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_v13`'s: **{'yes' if fps == {fp_now} else 'NO'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
        print("\n".join(L))
        return
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)
    K = [runs[s]["kinds"] for s in seeds]

    def per_world(fn):
        """Per world (numerator, denominator) for a pooled share."""
        nu = np.array([sum(1 for k in ks if fn(k) == 1) for ks in K], float)
        de = np.array([sum(1 for k in ks if fn(k) is not None) for ks in K], float)
        with np.errstate(invalid="ignore", divide="ignore"):
            return nu.sum() / de.sum() if de.sum() else float("nan"), (W @ nu) / (W @ de), int(de.sum())

    def g(k, f):
        return k[F[f]]

    # --- primary 1
    p1 = per_world(lambda k: g(k, "used_before_loss"))
    lo1, hi1 = pct(p1[1])
    unvalued = p1[0] < 0.5 and hi1 < 0.5
    L += ["## Primary 1: used before lost", "",
          f"Share of kinds used by their inventor at least once before the recipe was gone: **{p1[0]:.3f} "
          f"[{lo1:.3f}, {hi1:.3f}]** (kinds {p1[2]:,}).", "",
          f"**Reading: {'unvalued at birth dominates' if unvalued else 'not shown (most kinds are used before loss, or the interval reaches 0.5)'}.**",
          ""]

    # --- primary 2
    def survives(k, v):
        if v is None:
            return None
        if not g(k, "full"):
            return 1
        return int(v > g(k, "minval"))
    actual = per_world(lambda k: g(k, "held_first_week") if g(k, "held_first_week") is not None else None)
    s_first = per_world(lambda k: survives(k, g(k, "first_felt")) if g(k, "n_uses") > 0 else None)
    s_sim = per_world(lambda k: survives(k, g(k, "vsim")))
    L += ["## Primary 2: counterfactual survival of the 12-recipe cap at invention", "",
          "| first value | survives the cap | 95% | kinds |", "|---|---|---|---|",
          "| actual (value 0; held at the first week's end) | {:.3f} | [{:.3f}, {:.3f}] | {:,} |".format(
              actual[0], *pct(actual[1]), actual[2]),
          "| v_first (the first use's felt value; used kinds) | {:.3f} | [{:.3f}, {:.3f}] | {:,} |".format(
              s_first[0], *pct(s_first[1]), s_first[2]),
          "| v_sim (similar known kinds' values) | {:.3f} | [{:.3f}, {:.3f}] | {:,} |".format(
              s_sim[0], *pct(s_sim[1]), s_sim[2]), "",
          "Amendment 1: the v_sim row is close to 1 by construction (a mean of the person's values is almost always "
          "above their lowest) and carries no reading.", ""]

    # --- primary 3
    xs = [[(g(k, "vsim"), g(k, "first_felt")) for k in ks if g(k, "vsim") is not None and g(k, "n_uses") > 0]
          for ks in K]

    def corr(pairs):
        if len(pairs) < 3:
            return float("nan")
        a = np.array(pairs, float)
        if a[:, 0].std() == 0 or a[:, 1].std() == 0:
            return float("nan")
        return float(np.corrcoef(a[:, 0], a[:, 1])[0, 1])
    point = corr([p for w_ in xs for p in w_])
    reps = []
    for row in W[:2000] if SMOKE else W:
        pairs = [p for wi, w_ in zip(row, xs) for _ in range(int(wi)) for p in w_]
        reps.append(corr(pairs))
    lo3, hi3 = pct(reps)
    npairs = sum(len(w_) for w_ in xs)
    xm = [[(g(k, "vmean"), g(k, "first_felt")) for k in ks if g(k, "vmean") is not None and g(k, "n_uses") > 0]
          for ks in K]
    point_m = corr([p for w_ in xm for p in w_])
    informative = lo3 > 0.2 and point > point_m          # amendment 1
    L += ["## Primary 3: does experience with similar things predict a new kind's usefulness?", "",
          f"Correlation of v_sim with the first use's felt value: **{point:.3f} [{lo3:.3f}, {hi3:.3f}]** "
          f"(kinds used and with a v_sim: {npairs:,}).",
          f"Amendment 1: the plain mean value's correlation with the first felt value: {point_m:.3f}. \"Similar experience "
          "is informative\" requires v_sim's interval wholly above 0.2 and v_sim's correlation above the plain mean's.", "",
          f"**Reading: {'similar experience is informative' if informative else ('experience is informative, but not its similarity' if lo3 > 0.2 else 'not shown (the interval does not lie wholly above 0.2)')}.**",
          ""]
    follow = ("a nature test of 'a new kind's first value comes from similar known kinds' (council first)"
              if (unvalued and informative) else "the next target is opportunity or intention (getting the inputs again)")
    L += [f"**What follows (decided before data): {follow}.**", ""]

    # --- described
    allk = [k for ks in K for k in ks]
    stages = np.bincount([g(k, "stage") for k in allk], minlength=6) / max(1, len(allk))
    used = [k for k in allk if g(k, "n_uses") > 0]
    fu = sorted(g(k, "first_use_week") for k in used)
    lw = sorted(g(k, "lost_week") for k in allk if g(k, "lost_week") is not None)
    pos = sum(1 for k in used if g(k, "first_felt") > 0.05)
    clear_first = sum(1 for k in used if g(k, "first_felt") > 0.05)
    vs = [g(k, "vsim") for k in allk if g(k, "vsim") is not None]
    L += ["## Described", "",
          f"- Kinds {len(allk):,}; ever used by the inventor within 5 years {len(used):,} ({len(used) / max(1, len(allk)):.3f}).",
          "- Stage shares (LD1's funnel): " + ", ".join(f"{i}: {v:.3f}" for i, v in enumerate(stages)),
          f"- Weeks to first use (median): {fu[len(fu) // 2] if fu else 'nan'}; weeks to loss (median): "
          f"{lw[len(lw) // 2] if lw else 'nan'} (of {len(lw):,} lost)",
          f"- First uses with felt > 0.05: {pos:,} of {len(used):,}; v_first clears the 0.05 offer threshold: "
          f"{clear_first:,}; v_sim clears it: {sum(1 for v in vs if v > 0.05):,} of {len(vs):,}",
          f"- Cap full at invention: {sum(1 for k in allk if g(k, 'full')):,} of {len(allk):,}", ""]
    L += ["## Population", "", f"- Worlds {len(seeds)}; extinct {sum(1 for s in seeds if runs[s]['extinct'])}", ""]
    text = "\n".join(L) + "\n"
    if SMOKE:
        print(text)
        return
    (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
