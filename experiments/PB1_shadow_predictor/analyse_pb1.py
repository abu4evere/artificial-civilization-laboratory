"""PB1 analysis, written before any study data (questions.md, frozen as `PB1-frozen`, with amendment 1).

  python experiments/PB1_shadow_predictor/analyse_pb1.py                      # writes results.md
  python experiments/PB1_shadow_predictor/analyse_pb1.py --smoke --dir <folder>
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
import run_pb1 as R  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261112)
OUTPUTS = ("food gained", "net food", "health", "energy", "materials", "things held", "distance", "new kind",
           "affection")
NAME = {"B": "B (table)", "L": "L-own", "N": "N-own", "LO": "L-obs", "LO5": "L-obs-0.5", "NO": "N-obs"}


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
    m = re.search(r"code_v13 fingerprint: ([0-9a-f]{64})", zero)
    zero_ok = "All: PASS" in zero and m is not None and m.group(1) == fp_now
    seeds = sorted(runs) if SMOKE else sorted(R.SEEDS)
    present = bool(seeds) and all(s in runs for s in seeds)
    fps = {runs[s]["code_hash"] for s in runs} | {runs[s]["code_hash_after"] for s in runs}
    ok = bool(zero_ok and present and fps == {fp_now})
    L = ["# PB1: A shadow brain — can a small predictor learn what ACL's actions do? (results)", "",
         "Frozen as `PB1-frozen` (with amendment 1). run_pb1.py, analyse_pb1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks (All: PASS, same `code_v13` fingerprint): **{'yes' if zero_ok else 'NO'}**",
         f"- All worlds present ({len(runs)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint, `code_v13`'s: **{'yes' if fps == {fp_now} else 'NO'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
        print("\n".join(L))
        return
    seeds = [s for s in seeds if s in runs]
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))]).astype(float)

    def sse(v, case):              # per world, summed over the 9 outputs
        return np.array([sum(runs[s]["sse"][v][case]) for s in seeds])

    def skill(v, case):
        a, b = sse(v, case), sse("B", case)
        with np.errstate(invalid="ignore", divide="ignore"):
            pt = 1.0 - a.sum() / b.sum() if b.sum() else float("nan")
            rep = 1.0 - (W @ a) / (W @ b)
        return pt, *pct(rep)

    def cnt(case):
        return sum(runs[s]["counts"].get(case, 0) for s in seeds)

    # --- Primary (frozen): L-own against B on compositionally unfamiliar common-action weeks
    p = skill("L", "u_pair")
    holds = p[1] > 0
    L += ["## Primary (frozen): L-own against B on compositionally unfamiliar weeks", "",
          "| cases | skill of L-own [95%] | reading |", "|---|---|---|",
          f"| {cnt('u_pair'):,} unfamiliar (situation, action) weeks of common actions | {p[0]:+.4f} [{p[1]:+.4f}, "
          f"{p[2]:+.4f}] | **{'the predictor learns and generalises' if holds else 'it does not'}** |", "",
          "Skill = 1 − (squared standardised error of the variant ÷ that of B). Rule: the predictor learns and "
          "generalises if the 95% interval lies wholly above 0.", ""]
    s2 = skill("L", "u_prop")
    L += ["## Mandatory secondary: unfamiliar property combinations", "",
          f"L-own against B on {cnt('u_prop'):,} weeks: **{s2[0]:+.4f} [{s2[1]:+.4f}, {s2[2]:+.4f}]**.", ""]
    # --- every variant, every case
    cases = ("u_pair", "u_prop", "all", "rare", "u_place", "w0", "w1", "w2", "w3")
    label = {"u_pair": "unfamiliar pairs (primary)", "u_prop": "unfamiliar property combinations", "all": "all own weeks",
             "rare": "rare actions", "u_place": "unfamiliar destination", "w0": "first 100 weeks lived",
             "w1": "100-500 weeks", "w2": "500-1,000 weeks", "w3": "over 1,000 weeks"}
    L += ["## Every variant against B (described; no multiplicity claim)", "",
          "| cases | weeks | " + " | ".join(NAME[v] for v in R.VARIANTS if v != "B") + " |",
          "|---|---|" + "---|" * (len(R.VARIANTS) - 1)]
    for c in cases:
        cells = []
        for v in R.VARIANTS:
            if v == "B":
                continue
            s = skill(v, c)
            cells.append(f"{s[0]:+.3f} [{s[1]:+.3f}, {s[2]:+.3f}]")
        L.append(f"| {label[c]} | {cnt(c):,} | " + " | ".join(cells) + " |")
    # PB2 preferences (frozen rules)
    def diff(v1, v2, case="u_pair"):
        a1, a2 = sse(v1, case), sse(v2, case)
        b = sse("B", case)
        with np.errstate(invalid="ignore", divide="ignore"):
            pt = (a2.sum() - a1.sum()) / b.sum()
            rep = ((W @ a2) - (W @ a1)) / (W @ b)
        return pt, *pct(rep)
    dn, do = diff("N", "L"), diff("LO", "L")
    L += ["", "## For PB2 (frozen preference rules, on the primary cases)", "",
          f"- N-own over L-own (skill difference): {dn[0]:+.4f} [{dn[1]:+.4f}, {dn[2]:+.4f}] → "
          f"**{'a network is preferred' if dn[1] > 0 else 'linear is kept'}**.",
          f"- L-obs over L-own: {do[0]:+.4f} [{do[1]:+.4f}, {do[2]:+.4f}] → "
          f"**{'observation is preferred' if do[1] > 0 else 'own experience only'}**.", ""]
    # by output
    L += ["## By output: L-own and L-obs against B, all own weeks (described)", "",
          "| output | L-own | L-obs | B's mean squared standardised error (headroom) |", "|---|---|---|---|"]
    for k, o in enumerate(OUTPUTS):
        def sk(v):
            a = sum(runs[s]["sse"][v]["all"][k] for s in seeds)
            b = sum(runs[s]["sse"]["B"]["all"][k] for s in seeds)
            return 1 - a / b if b else float("nan")
        bmse = sum(runs[s]["sse"]["B"]["all"][k] for s in seeds) / max(1, cnt("all"))
        L.append(f"| {o} | {sk('L'):+.3f} | {sk('LO'):+.3f} | {bmse:.3f} |")
    su = lambda key: sum(runs[s]["sums"].get(key, 0) for s in seeds)  # noqa: E731
    L += ["", "## Population and sample (beside every measure)", "",
          f"Followed adults {su('followed_people'):,}; their own prequential weeks {su('own_weeks'):,}; observed examples "
          f"{su('observed'):,}; living-weeks {su('living_weeks'):,}; extinct worlds "
          f"{sum(1 for s in seeds if runs[s]['extinct'])}.", ""]
    text = "\n".join(L) + "\n"
    if SMOKE:
        print(text)
        return
    (HERE / "results.md").write_text(text, encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
