"""LR1 analysis, written before any data (questions.md, frozen as `LR1-frozen`; operational note 1).

  python experiments/LR1_long_run_v8/analyse_lr1.py            # writes results.md
  python experiments/LR1_long_run_v8/analyse_lr1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_lr1 import ARMS, SEEDS, YEARS  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261028)
NAME = {"c": "v7", "o": "v8", "x": "sham"}


def series(r, field, years):
    """Value of a census field per year (worlds that died out count 0 after their last year)."""
    F = r["census_fields"]
    by = {row[0]: row[F.index(field)] for row in r["census"]}
    return np.array([by.get(y, 0.0) for y in range(years)], float)


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
    L = ["# LR1 — Does nature v8 stay healthy over 1,000 years? Results", "",
         "Frozen as `LR1-frozen` (operational note 1). run_lr1.py, analyse_lr1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({sum(len(runs[a]) for a in ARMS)} of {len(SEEDS) * len(ARMS)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint (`code_v8`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- Drops = pick-ups + on the ground every year (mismatches 0): **{'yes' if mism == 0 else f'NO ({mism})'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    seeds = sorted(set(runs["c"]) & set(runs["o"]) & set(runs["x"]))
    n = len(seeds)
    years = YEARS if not SMOKE else max(row[0] for a in ARMS for r in runs[a].values() for row in r["census"]) + 1
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))])
    S = {a: {f: np.stack([series(runs[a][s], f, years) for s in seeds]) for f in
             ("living", "adults", "items_adults", "ground", "ground_max_tile", "drops", "pickups", "pickups_other")}
         for a in ARMS}
    ext = {a: sum(1 for s in seeds if runs[a][s]["extinct"]) for a in ARMS}
    L += [f"Paired seeds: {n}; {years} years. Extinct: v7 {ext['c']}, v8 {ext['o']}, sham {ext['x']}.", ""]
    marks = [y for y in (200, 400, 600, 800, 1000) if y <= years]
    # Q1
    L += ["## Q1 — Accumulation: things lying on the ground (mean per world)", "",
          "| year | v8 | sham | v8: most on one tile (max over worlds) | v8: pick-ups ÷ drops in the century before |",
          "|---|---|---|---|---|"]
    for y in marks:
        i = y - 1
        lo = max(0, y - 100)
        d = S["o"]["drops"][:, lo:y].sum()
        p = S["o"]["pickups"][:, lo:y].sum()
        L.append(f"| {y} | {S['o']['ground'][:, i].mean():.1f} | {S['x']['ground'][:, i].mean():.1f} | "
                 f"{S['o']['ground_max_tile'][:, i].max():.0f} | {p / d if d else float('nan'):.3f} |")
    L.append("")
    flag_a = False
    if years >= 1000:
        t = np.arange(800, 1000)
        slopes = np.array([np.polyfit(t, S["o"]["ground"][k, 800:1000], 1)[0] for k in range(n)])
        reps = (W @ slopes) / n
        lo, hi = np.percentile(reps, [2.5, 97.5])
        g200, g1000 = S["o"]["ground"][:, 199].mean(), S["o"]["ground"][:, 999].mean()
        flag_a = g1000 > 5 * g200 and lo > 0
        L += [f"Slope of things on the ground, years 800-1,000 (mean over worlds): {slopes.mean():+.3f} per year "
              f"[{lo:+.3f}, {hi:+.3f}]. Year 1,000 ÷ year 200: {g1000 / g200 if g200 else float('nan'):.2f}.", "",
              f"**Flag A (accumulation): {'RAISED' if flag_a else 'not raised'}** (> 5× year 200 and still growing).", ""]
    # Q2
    L += ["## Q2 — Demography (mean living per world; extinct worlds count 0)", "",
          "| years | v7 | v8 | sham | v8 ÷ v7 | sham ÷ v7 |", "|---|---|---|---|---|---|"]
    for y0 in range(0, years, 100):
        y1 = min(y0 + 100, years)
        c, o, x = (S[a]["living"][:, y0:y1].mean() for a in ("c", "o", "x"))
        L.append(f"| {y0}-{y1} | {c:.1f} | {o:.1f} | {x:.1f} | {o / c if c else float('nan'):.3f} | {x / c if c else float('nan'):.3f} |")
    L.append("")
    flag_b = False
    if years >= 1000:
        def late(a):
            return S[a]["living"][:, 800:1000].sum(axis=1)
        ro = (W @ late("o")) / (W @ late("c"))
        rx = (W @ late("x")) / (W @ late("c"))
        po = late("o").sum() / late("c").sum()
        px = late("x").sum() / late("c").sum()
        lo, hi = np.percentile(ro, [2.5, 97.5])
        lx, hx = np.percentile(rx, [2.5, 97.5])
        flag_b = (po < 0.90 and hi < 1.0) or (ext["o"] - ext["c"] >= 3)
        L += [f"Population, years 800-1,000: v8 ÷ v7 **{po:.3f} [{lo:.3f}, {hi:.3f}]**; sham ÷ v7 {px:.3f} [{lx:.3f}, {hx:.3f}].", "",
              f"**Flag B (demography): {'RAISED' if flag_b else 'not raised'}** (below 0.90 with the upper bound under 1, "
              f"or 3+ more extinct worlds).", ""]
    # Q3
    L += ["## Q3 — Made things held per adult", "", "| years | v7 | v8 | sham |", "|---|---|---|---|"]
    for y0 in range(0, years, 100):
        y1 = min(y0 + 100, years)
        row = []
        for a in ("c", "o", "x"):
            ad = S[a]["adults"][:, y0:y1].sum()
            row.append(S[a]["items_adults"][:, y0:y1].sum() / ad if ad else float("nan"))
        L.append(f"| {y0}-{y1} | {row[0]:.3f} | {row[1]:.3f} | {row[2]:.3f} |")
    po_ = S["o"]["pickups"].sum()
    L += ["", f"v8: pick-ups by someone other than the dropper: {S['o']['pickups_other'].sum() / po_ if po_ else float('nan'):.3f} "
              f"of {po_:.0f} pick-ups.", ""]
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
