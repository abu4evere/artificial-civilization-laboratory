"""PC1 analysis, written before any data (questions.md, frozen as `PC1-frozen`). Descriptive, with the frozen reading.

  python experiments/PC1_part_chains/analyse_pc1.py                      # writes results.md
  python experiments/PC1_part_chains/analyse_pc1.py --smoke --dir <folder>
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
import run_pc1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261108)
PART_OUT = ("knew", "declined", "missing_part", "taken", "distrust")


def pct(x):
    x = x[np.isfinite(x)]
    return (float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))) if len(x) else (float("nan"),) * 2


def per_world(r):
    """Per-world counts (the same as the recompute file)."""
    c = Counter()
    for t0, d, n, u, cyc in r["kinds"]:
        c["kinds"] += 1
        c[f"depth{min(d, 3)}"] += 1
    for nm, ntk, tk_all, nalive, deep, shown, pout, pmiss in r["rows"]:
        c["failed"] += 1
        c[f"miss{min(nm, 3)}"] += 1
        c[f"deep{min(deep, 3)}"] += 1
        c["tk_all" if (nm and ntk == nm) else ("tk_none" if ntk == 0 else "tk_some")] += 1
        if shown:
            c["part_shown"] += 1
            c[f"part_{pout}"] += 1
            c["part_was_missing"] += pmiss
    for k, v in r["later"].items():
        c[k] += v
    return c


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
    checks = all(r["tree_mismatch"] == 0 and r["part_taken_mismatch"] == 0 for r in runs.values())
    ok = bool(zero_ok and present and fps == {fp_now} and checks)
    L = ["# PC1: the part chains of new kinds (results)", "",
         "Frozen as `PC1-frozen`. run_pc1.py, analyse_pc1.py (written before data).", "", "## Validity", "",
         f"- Zero checks (All: PASS, `code_v15` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({len(runs)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_v15`'s: **{'yes' if fps == {fp_now} else 'NO'}**",
         f"- Tree checks and part-lesson event checks in every world (mismatches "
         f"{sum(r['tree_mismatch'] + r['part_taken_mismatch'] for r in runs.values())}): **{'yes' if checks else 'NO'}**",
         "", f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        finish(L)
        return
    seeds = [s for s in seeds if s in runs]
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)
    C = {s: per_world(runs[s]) for s in seeds}

    def col(k):
        return np.array([float(C[s].get(k, 0)) for s in seeds])

    def share(num, den):
        nu = sum(col(k) for k in num) if isinstance(num, tuple) else col(num)
        de = sum(col(k) for k in den) if isinstance(den, tuple) else col(den)
        with np.errstate(invalid="ignore", divide="ignore"):
            return (nu.sum() / de.sum() if de.sum() else float("nan")), (W @ nu) / (W @ de), int(nu.sum()), int(de.sum())

    def fmt(t):
        lo, hi = pct(t[1])
        return f"{t[0]:.3f} [{lo:.3f}, {hi:.3f}] ({t[2]:,} of {t[3]:,})"

    tot = Counter()
    for c in C.values():
        tot.update(c)
    L += ["## 1. Trees of the followed kinds (depth = the longest chain of made parts)", "",
          "| depth | kinds | share |", "|---|---|---|"]
    for d in range(4):
        L.append(f"| {d if d < 3 else '3+'} | {tot[f'depth{d}']:,} | {fmt(share(f'depth{d}', 'kinds'))} |")
    L += ["", "## 2. Lessons that failed on a missing part", "",
          f"Failed-on-part top-level lessons of followed kinds: {tot['failed']:,}.", "",
          "| missing made parts | share |", "|---|---|"]
    for k in range(1, 4):
        L.append(f"| {k if k < 3 else '3+'} | {fmt(share(f'miss{k}', 'failed'))} |")
    L += ["", "| deepest missing chain | share |", "|---|---|"]
    for k in range(1, 4):
        L.append(f"| {k if k < 3 else '3+'} | {fmt(share(f'deep{k}', 'failed'))} |")
    tk_all, tk_none, tk_some = share("tk_all", "failed"), share("tk_none", "failed"), share("tk_some", "failed")
    L += ["", "**Does the teacher know the missing parts?**", "",
          f"- all of them: **{fmt(tk_all)}**", f"- some: {fmt(tk_some)}", f"- none: **{fmt(tk_none)}**", ""]
    shown = share("part_shown", "failed")
    L += ["## 3. The one-level part lesson (NV3's parts-first)", "", f"- A part lesson followed: {fmt(shown)}."]
    for o in PART_OUT:
        L.append(f"- of those, {('wasted (the learner knew the part)' if o == 'knew' else o)}: "
                 f"{fmt(share(f'part_{o}', 'part_shown'))}")
    L.append(f"- the part shown was one the learner was missing: {fmt(share('part_was_missing', 'part_shown'))}")
    unhelp = share(("part_knew", "part_declined", "part_missing_part", "part_distrust"), "part_shown")
    L += [f"- **not helpful** (wasted, declined, nested failure or distrust): **{fmt(unhelp)}**", ""]
    L += ["## 4. Within 5 years, per learner and kind (after the first failed lesson)", "",
          f"- learned a missing part: {fmt(share('got_part', 'pairs'))}",
          f"- learned the kind itself: {fmt(share('got_K', 'pairs'))}",
          f"- made the kind: {fmt(share('made_K', 'pairs'))}", ""]

    # frozen reading
    def crosses(t):
        lo, hi = pct(t[1])
        return lo <= 0.5 <= hi
    if tk_all[0] > 0.5 and unhelp[0] > 0.5:
        reading = "a deeper, learner-driven part lesson could help"
    elif tk_none[0] > 0.5:
        reading = "it could not: the knowledge is not within the teacher's reach"
    else:
        reading = "mixed"
    cross = [name for name, t in (("teacher knows all", tk_all), ("teacher knows none", tk_none),
                                  ("part lesson not helpful", unhelp)) if crosses(t)]
    L += ["## Reading (frozen)", "", f"**{reading}.**" + (f" Intervals crossing 0.5: {', '.join(cross)}." if cross else ""),
          "", "Rule: \"could help\" if the teacher knows every missing part in more than half of failed lessons and the "
          "one-level part lesson is not helpful in more than half of those shown; \"could not\" if the teacher knows none "
          "in more than half; \"mixed\" otherwise.", ""]
    finish(L)


def finish(L):
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
