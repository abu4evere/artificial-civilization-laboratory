"""AW1 analysis, written before any data (questions.md, frozen as `AW1-frozen`).

  python experiments/AW1_watch_and_teach/analyse_aw1.py            # writes results.md
  python experiments/AW1_watch_and_teach/analyse_aw1.py --smoke --dir <folder> [--window A B]
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_aw1  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
SEEDS = run_aw1.SMOKE_SEEDS if SMOKE else run_aw1.SEEDS
ARMS = tuple(run_aw1.ARMS)
REPS = 10_000
RNG = np.random.default_rng(20261031)
WIN = (int(sys.argv[sys.argv.index("--window") + 1]), int(sys.argv[sys.argv.index("--window") + 2])) \
    if "--window" in sys.argv else (100, 200)                  # frozen: years 100-200


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
    kinds_ok = all(
        (r["passed_total"].get("watched", 0) == 0 or a == "w") and (r["passed_total"].get("shown", 0) == 0 or a == "t")
        for a in ARMS for r in runs[a].values())
    ok = "All: PASS" in zero and present and len(fps) == 1 and kinds_ok
    L = ["# AW1 — Learning a craft from others: results" + (" (SMOKE TEST, throwaway seeds)" if SMOKE else ""), "",
         "Frozen as `AW1-frozen`. run_aw1.py, analyse_aw1.py (written before data).", "", "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({sum(len(v) for v in runs.values())} of {len(ARMS) * len(SEEDS)}): "
         f"**{'yes' if present else 'NO'}**",
         f"- One fingerprint (`code_aw1`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- Each arm passed only its own kind of step (v and x none): **{'yes' if kinds_ok else 'NO'}**", "",
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

    def pooled(arm, num, den, win=WIN):
        N, D = cen(arm, num, *win), cen(arm, den, *win)
        with np.errstate(invalid="ignore", divide="ignore"):
            return (N.sum() / D.sum() if D.sum() else float("nan")), (W @ N) / (W @ D)

    def ci(x):
        x = x[np.isfinite(x)]
        return np.percentile(x, [2.5, 97.5]) if len(x) else (float("nan"),) * 2

    ext = {a: sum(1 for s in seeds if runs[a][s]["extinct"]) for a in ARMS}
    pop = {a: cen(a, "living", *WIN).sum() for a in ARMS}
    L += [f"Paired seeds: {n}; years {WIN[0]}–{WIN[1]}. Extinct by year 200: " +
          ", ".join(f"{a} {ext[a]}" for a in ARMS) + ". Mean living in the window: " +
          ", ".join(f"{a} {pop[a] / (n * (WIN[1] - WIN[0])):.1f}" for a in ARMS) + ".", ""]

    # primary
    pv, rv = pooled("v", "makes", "adults")
    res = {}
    for a in ("w", "t", "x"):
        pa, ra = pooled(a, "makes", "adults")
        lo, hi = ci(ra - rv)
        res[a] = (pa, pa - pv, lo, hi)
    L += [f"## Primary — making events per adult-year, years {WIN[0]}–{WIN[1]}", "",
          "| arm | making per adult-year | − v [95%] |", "|---|---|---|", f"| v (v9) | {pv:.4f} | |"]
    for a, name in (("w", "w (watching)"), ("t", "t (being shown)"), ("x", "x (sham)")):
        L.append(f"| {name} | {res[a][0]:.4f} | {res[a][1]:+.4f} [{res[a][2]:+.4f}, {res[a][3]:+.4f}] |")
    L += ["", "## The frozen rule", ""]
    for a in ("w", "t"):
        sup = res[a][2] > 0 and res[a][2] > res["x"][3]
        f1 = ext[a] - ext["v"] >= 3
        f2 = pop[a] < 0.90 * pop["v"]
        L.append(f"- **{a}:** lower bound {res[a][2]:+.4f} above 0 and above the sham's upper bound "
                 f"{res['x'][3]:+.4f}: **{'supports' if sup else 'not supported'}**. Flags: extinct {ext[a]} vs v "
                 f"{ext['v']} ({'FLAG' if f1 else 'no flag'}); population {a} ÷ v = "
                 f"{pop[a] / pop['v'] if pop['v'] else float('nan'):.3f} ({'FLAG' if f2 else 'no flag'}).")

    # secondaries
    L += ["", f"## Secondaries (described; years {WIN[0]}–{WIN[1]})", "",
          "| measure | v | w − v [95%] | t − v [95%] | x − v [95%] |", "|---|---|---|---|---|"]
    for name, num, den in (("world-born adults' (20–40) crafting skill", "wb_craft_sum_20_40", "wb_adults_20_40"),
                           ("children's (6–11) crafting skill", "kids_craft_sum_6_11", "kids_6_11"),
                           ("teens' (12–15) making per teen-year", "teen_makes", "teens_12_15"),
                           ("made things held per adult", "items_adults", "adults"),
                           ("steps passed by watching, per living person-year", "passed_watched", "living"),
                           ("steps passed by being shown, per living person-year", "passed_shown", "living")):
        p0, r0 = pooled("v", num, den)
        cells = []
        for a in ("w", "t", "x"):
            p1, r1 = pooled(a, num, den)
            lo, hi = ci(r1 - r0)
            cells.append(f"{p1 - p0:+.4f} [{lo:+.4f}, {hi:+.4f}]")
        L.append(f"| {name} | {p0:.4f} | " + " | ".join(cells) + " |")
    L += ["", "Whole-run steps passed (sum over worlds): " + "; ".join(
        f"{a}: watched {sum(r['passed_total'].get('watched', 0) for r in runs[a].values())}, shown "
        f"{sum(r['passed_total'].get('shown', 0) for r in runs[a].values())}" for a in ARMS) + "."]
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
