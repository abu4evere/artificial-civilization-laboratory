"""LC1 analysis, written before any data (questions.md, frozen as `LC1-frozen`).

  python experiments/LC1_long_curiosity/analyse_lc1.py            # writes results.md
  python experiments/LC1_long_curiosity/analyse_lc1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_lc1  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
SEEDS = run_lc1.SMOKE_SEEDS if SMOKE else run_lc1.SEEDS
ARMS = run_lc1.ARMS
REPS = 10_000
RNG = np.random.default_rng(20261029)
MARGIN = 0.012              # FS1's margin: one making act's skill gain from zero
EARLY, LATE = (100, 200), (800, 1000)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {a: {} for a in ARMS}
    for f in glob.glob(str(OUTDIR / "*_seed_*.json")):
        r = json.load(open(f))
        if r["arm"] in runs:
            runs[r["arm"]][r["seed"]] = r
    zero = (OUTDIR / "zero.txt").read_text(encoding="utf-8") if (OUTDIR / "zero.txt").exists() else ""
    present = all(sorted(runs[a]) == sorted(SEEDS) for a in ARMS)
    fps = {r["code_hash"] for a in ARMS for r in runs[a].values()} | \
          {r["code_hash_after"] for a in ARMS for r in runs[a].values()}
    mism = sum(sum(r["mismatch"].values()) for a in ARMS for r in runs[a].values())
    ok = "All: PASS" in zero and present and len(fps) == 1 and mism == 0
    L = ["# LC1 — Does curiosity slow the erosion over 1,000 years? Results"
         + (" (SMOKE TEST, throwaway seeds)" if SMOKE else ""), "",
         "Frozen as `LC1-frozen`. run_lc1.py (CU1's runner), analyse_lc1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({sum(len(v) for v in runs.values())} of {len(ARMS) * len(SEEDS)}): "
         f"**{'yes' if present else 'NO'}**",
         f"- One fingerprint (`code_cu1`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- `tried` equals own updates (mismatches 0): **{'yes' if mism == 0 else f'NO ({mism})'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    seeds = sorted(SEEDS)
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))])

    def cen(arm, field, lo, hi):
        out = []
        for s in seeds:
            r = runs[arm][s]
            i = r["census_fields"].index(field)
            out.append(float(sum(row[i] for row in r["census"] if lo <= row[0] < hi)))
        return np.array(out)

    def pooled(arm, num, den, win):
        N, D = cen(arm, num, *win), cen(arm, den, *win)
        p = N.sum() / D.sum() if D.sum() else float("nan")
        with np.errstate(invalid="ignore", divide="ignore"):
            reps = (W @ N) / (W @ D)
        return p, reps

    def ci(reps):
        reps = reps[np.isfinite(reps)]
        return np.percentile(reps, [2.5, 97.5]) if len(reps) else (float("nan"),) * 2

    skill = ("wb_craft_sum_20_40", "wb_adults_20_40")
    ext = {a: sum(1 for s in seeds if runs[a][s]["extinct"]) for a in ARMS}
    L += [f"Paired seeds: {n}; 1,000 years. Extinct by year 1,000: v {ext['v']}, c {ext['c']}, x {ext['x']}.", ""]

    # Primary
    pv, rv = pooled("v", *skill, LATE)
    rows = []
    res = {}
    for a in ("c", "x"):
        pa, ra = pooled(a, *skill, LATE)
        lo, hi = ci(ra - rv)
        res[a] = (pa, pa - pv, lo, hi)
    d = res["c"]
    if d[2] > MARGIN:
        read = "curiosity holds skill higher"
    elif -MARGIN < d[2] and d[3] < MARGIN:
        read = "no lasting difference"
    else:
        read = "not shown"
    contrib = {a: (int((cen(a, "wb_adults_20_40", *LATE) > 0).sum()), cen(a, "wb_adults_20_40", *LATE).sum())
               for a in ARMS}
    L += ["## Primary — world-born adults' (20–40) crafting skill, years 800–999", "",
          f"Margin ±{MARGIN} (FS1). Survivor-weighted: only living adults in worlds still alive count.", "",
          "| arm | skill | worlds / adult-years | − v [95%] |", "|---|---|---|---|",
          f"| v (v8) | {pv:.4f} | {contrib['v'][0]} / {contrib['v'][1]:,.0f} | |",
          f"| c (curiosity) | {res['c'][0]:.4f} | {contrib['c'][0]} / {contrib['c'][1]:,.0f} | "
          f"**{res['c'][1]:+.4f} [{res['c'][2]:+.4f}, {res['c'][3]:+.4f}]** |",
          f"| x (sham) | {res['x'][0]:.4f} | {contrib['x'][0]} / {contrib['x'][1]:,.0f} | "
          f"{res['x'][1]:+.4f} [{res['x'][2]:+.4f}, {res['x'][3]:+.4f}] |", "",
          f"**Reading: {read}.**", ""]

    # Slower erosion or a parallel shift
    L += ["## Slower erosion or a parallel shift?", "",
          "| arm | skill years 100–199 | skill years 800–999 | change |", "|---|---|---|---|"]
    chg = {}
    for a in ARMS:
        pe, re_ = pooled(a, *skill, EARLY)
        pl, rl = pooled(a, *skill, LATE)
        chg[a] = (pl - pe, rl - re_)
        L.append(f"| {a} | {pe:.4f} | {pl:.4f} | {pl - pe:+.4f} |")
    lo, hi = ci(chg["c"][1] - chg["v"][1])
    L += ["", f"Change in c minus change in v: {chg['c'][0] - chg['v'][0]:+.4f} [{lo:+.4f}, {hi:+.4f}] (positive = c "
              f"falls less).", ""]
    L += ["Century-by-century (world-born adults' crafting skill; mean living; making per adult-year):", "",
          "| years | " + " | ".join(ARMS) + " |", "|---|" + "---|" * len(ARMS)]
    slopes = {a: [] for a in ARMS}
    for lo_ in range(0, 1000, 100):
        cells = []
        for a in ARMS:
            sk = pooled(a, *skill, (lo_, lo_ + 100))[0]
            liv = cen(a, "living", lo_, lo_ + 100).sum() / (n * 100)
            mk = pooled(a, "makes", "adults", (lo_, lo_ + 100))[0]
            cells.append(f"{sk:.4f} / {liv:.1f} / {mk:.4f}")
            if sk and np.isfinite(sk) and sk > 0:
                slopes[a].append((lo_ + 50, math.log(sk)))
        L.append(f"| {lo_}–{lo_ + 100} | " + " | ".join(cells) + " |")
    L += ["", "Log-skill slope per century (least squares over the centuries with data; described):", ""]
    for a in ARMS:
        pts = slopes[a]
        if len(pts) >= 2:
            x = np.array([p[0] for p in pts]) / 100.0
            y = np.array([p[1] for p in pts])
            L.append(f"- {a}: {np.polyfit(x, y, 1)[0]:+.4f} per century")
    # Flags and secondaries
    popv = cen("v", "living", *LATE).sum()
    popc = cen("c", "living", *LATE).sum()
    flag_ext = ext["c"] - ext["v"] >= 3
    flag_pop = popc < 0.90 * popv
    L += ["", "## Flags (CU1's)", "",
          f"- Extinct c {ext['c']} vs v {ext['v']}: {'FLAG' if flag_ext else 'no flag'}.",
          f"- Population years 800–999 c ÷ v = {popc / popv if popv else float('nan'):.3f}: "
          f"{'FLAG' if flag_pop else 'no flag'}.", ""]
    L += ["## Secondaries (years 800–999, per adult-year)", "", "| measure | v | c − v [95%] |", "|---|---|---|"]
    for name, num in (("making events", "makes"), ("made things held", "items_adults")):
        p0, r0 = pooled("v", num, "adults", LATE)
        p1, r1 = pooled("c", num, "adults", LATE)
        lo, hi = ci(r1 - r0)
        L.append(f"| {name} | {p0:.4f} | {p1 - p0:+.4f} [{lo:+.4f}, {hi:+.4f}] |")
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
