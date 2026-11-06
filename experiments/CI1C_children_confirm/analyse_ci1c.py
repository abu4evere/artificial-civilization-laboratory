"""CI1-C analysis, written before any data (questions.md, frozen as `CI1C-frozen`).

CI1's frozen analysis (`../CI1_children_and_aims/analyse_ci1.py`, unchanged) is run on this study's seeds, arms (v14,
LG, sham) and output: validity, the eight guards and LG − v14 in the co-primary (CI1's "supported"). This script adds
the rest of the frozen CI1-C rule and measures:
  condition 3   LG − sham in the co-primary (the per-kind complete-set share), lower bound above 0
  secondary     the share of world-new kinds remade by their inventor within 5 years, LG − v14 (not a gate)
  described     kinds made by a person other than their inventor within 5 years; child makes beside child starvation
Its bootstrap: 10,000 paired-world resamples, random seed 20261124 (CI1's analysis keeps its own, 20261122).

  python experiments/CI1C_children_confirm/analyse_ci1c.py                    # writes results.md here
  python experiments/CI1C_children_confirm/analyse_ci1c.py --smoke --dir <folder>
"""
from __future__ import annotations

import contextlib
import glob
import io
import json
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_ci1c  # noqa: E402  (sets CI1's runner to these seeds, arms and folder)

sys.path.insert(0, str(HERE.parent / "CI1_children_and_aims"))
import analyse_ci1 as A  # noqa: E402

A.ARMS = ("c", "g", "x")
A.HERE = HERE
if "--dir" not in sys.argv:
    A.OUTDIR = HERE / "output"
SMOKE = A.SMOKE
REPS = 10_000
RNG = np.random.default_rng(20261124)
WPY = run_ci1c.WPY
TITLE_CI1 = "# CI1: Children may make again, and a held aim that keeps the pieces (results)"
TITLE = ("# CI1-C: children may make again (LG), confirmatory run on new seeds (results)\n\n"
         "CI1's frozen analysis on seeds 24101-24132, arms v14 / LG / sham (frozen as `CI1C-frozen`); the CI1-C rule "
         "and measures follow it (analyse_ci1c.py, written before data).")


class _Text(io.StringIO):
    def reconfigure(self, **k):          # CI1's analysis sets the console's encoding; here its text is kept instead
        pass


def main():
    buf = _Text()
    with contextlib.redirect_stdout(buf):
        A.main()
    sys.stdout.reconfigure(encoding="utf-8")
    text = buf.getvalue().rstrip("\n").replace(TITLE_CI1, TITLE, 1)
    L = [text, ""]
    valid = "**Valid.**" in text
    if not valid and not SMOKE:
        L += ["## The CI1-C rule", "", "**No reading: the study is not valid.**"]
        return finish(L)

    runs = {a: {} for a in A.ARMS}
    for f in sorted(glob.glob(str(A.OUTDIR / "*_seed_*.json"))):
        r = json.load(open(f))
        if r["arm"] in runs:
            runs[r["arm"]][r["seed"]] = r
    if SMOKE:
        seeds = sorted(set.intersection(*[set(runs[a]) for a in A.ARMS if runs[a]]))
    else:
        seeds = sorted(run_ci1c.SEEDS)
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def arr(a, key):
        return np.array([float(runs[a][s].get(key, 0)) for s in seeds])

    def share(a, num):
        K, C = arr(a, "n_kinds"), arr(a, num)
        with np.errstate(invalid="ignore", divide="ignore"):
            return (C.sum() / K.sum() if K.sum() else float("nan")), (W @ C) / (W @ K), int(K.sum()), int(C.sum())

    # conditions 1 and 2: CI1's reading of LG ("supported" = no guard and LG − v14 lower bound above 0)
    m = re.search(r"- \*\*LG: ([^*]+?)\.\*\* Guards raised: ([^.]+)\. Complete-set share [0-9.]+ against v14's "
                  r"[0-9.]+: ([+-][0-9.]+) \[([+-][0-9.]+), ([+-][0-9.]+)\]\.", text)
    reading, guards = (m.group(1), m.group(2)) if m else ("?", "?")
    c1 = guards == "none"
    c2 = m is not None and float(m.group(4)) > 0
    # condition 3: LG − sham
    sg, sx = share("g", "n_complete"), share("x", "n_complete")
    d3 = sg[0] - sx[0]
    lo3, hi3 = A.pct(sg[1] - sx[1])
    c3 = lo3 > 0
    confirmed = c1 and c2 and c3
    yn = lambda b: "yes" if b else "no"  # noqa: E731
    L += ["## The CI1-C rule (frozen)", "",
          "| condition | value | holds |", "|---|---|---|",
          f"| 1. no CI1 guard raised for LG against v14 | guards raised: {guards} | {yn(c1)} |",
          f"| 2. LG − v14, co-primary, lower bound above 0 | "
          f"{m.group(3) + ' [' + m.group(4) + ', ' + m.group(5) + ']' if m else '?'} (CI1's analysis: {reading}) | "
          f"{yn(c2)} |",
          f"| 3. LG − sham, co-primary, lower bound above 0 | {d3:+.4f} [{lo3:+.4f}, {hi3:+.4f}] "
          f"(LG {sg[3]:,} of {sg[2]:,}; sham {sx[3]:,} of {sx[2]:,}) | {yn(c3)} |", "",
          f"**{'CONFIRMED' if confirmed else 'NOT CONFIRMED'}.** Confirmed only if all three hold; then the blind "
          "recompute and the safe path to v15. Otherwise LG is not adopted.", ""]

    # secondary: remaking by the inventor, LG − v14 (not a gate)
    rg, rc = share("g", "n_remade"), share("c", "n_remade")
    lo, hi = A.pct(rg[1] - rc[1])
    L += ["## Pre-registered secondary (not a gate): kinds remade by their inventor within 5 years", "",
          "| arm | kinds | remade | share |", "|---|---|---|---|"]
    for a in A.ARMS:
        s = share(a, "n_remade")
        L.append(f"| {A.NAME[a]} | {s[2]:,} | {s[3]:,} | {s[0]:.4f} |")
    L += ["", f"LG − v14: {rg[0] - rc[0]:+.4f} [{lo:+.4f}, {hi:+.4f}].", ""]

    # described: making by others; child makes beside child starvation
    L += ["## Described (not decisive)", "",
          "| arm | kinds made by another person within 5 years | share | child makes per 1,000 child-weeks | child "
          "starvation deaths per 1,000 child-years | child deaths per 1,000 child-years |", "|---|---|---|---|---|---|"]
    for a in A.ARMS:
        s = share(a, "n_others")
        su = lambda k: sum(float(runs[a][x]["sums"].get(k, 0)) for x in seeds)  # noqa: E731
        cw = su("child_weeks") or 1
        L.append(f"| {A.NAME[a]} | {s[3]:,} of {s[2]:,} | {s[0]:.4f} | {1000 * su('makes_child') / cw:.3f} | "
                 f"{1000 * WPY * su('child_death_starvation') / cw:.4f} | {1000 * WPY * su('child_deaths') / cw:.4f} |")
    L.append("")
    return finish(L)


def finish(L):
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
