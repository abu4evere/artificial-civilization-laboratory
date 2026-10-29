"""CU1 analysis, written before any data (questions.md, frozen as `CU1-frozen`).

  python experiments/CU1_curiosity/analyse_cu1.py            # writes results.md
  python experiments/CU1_curiosity/analyse_cu1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_cu1  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
SEEDS = run_cu1.SMOKE_SEEDS if SMOKE else run_cu1.SEEDS
ARMS = run_cu1.ARMS
REPS = 10_000
RNG = np.random.default_rng(20261029)


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
    L = ["# CU1 — A curiosity law: does a pull towards the rarely tried break the practice trap? Results"
         + (" (SMOKE TEST, throwaway seeds)" if SMOKE else ""), "",
         "Frozen as `CU1-frozen`. run_cu1.py, analyse_cu1.py (written before data).", "", "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({sum(len(v) for v in runs.values())} of {len(ARMS) * len(SEEDS)}): "
         f"**{'yes' if present else 'NO'}**",
         f"- One fingerprint (`code_cu1`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- `tried` equals own updates in arm c (mismatches 0): **{'yes' if mism == 0 else f'NO ({mism})'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    seeds = sorted(SEEDS)
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))])

    def sp(arm, key):
        return np.array([float(runs[arm][s]["spread"][key]) for s in seeds])

    def cen(arm, field):
        out = []
        for s in seeds:
            r = runs[arm][s]
            i = r["census_fields"].index(field)
            out.append(float(sum(row[i] for row in r["census"] if 100 <= row[0] < 200)))
        return np.array(out)

    def diff(get_a, get_b, num, den):
        Na, Da, Nb, Db = get_a(num), get_a(den), get_b(num), get_b(den)
        pa = Na.sum() / Da.sum() if Da.sum() else float("nan")
        pb = Nb.sum() / Db.sum() if Db.sum() else float("nan")
        with np.errstate(invalid="ignore", divide="ignore"):
            reps = (W @ Na) / (W @ Da) - (W @ Nb) / (W @ Db)
        reps = reps[np.isfinite(reps)]
        lo, hi = np.percentile(reps, [2.5, 97.5]) if len(reps) else (float("nan"),) * 2
        return pa, pb, pa - pb, lo, hi

    def f(t, d=4):
        return f"{t[2]:+.{d}f} [{t[3]:+.{d}f}, {t[4]:+.{d}f}]"

    ext = {a: sum(1 for s in seeds if runs[a][s]["extinct"]) for a in ARMS}
    pop = {a: cen(a, "living").sum() / max(1, sum(len([r for r in runs[a][s]["census"] if 100 <= r[0] < 200])
                                                   for s in seeds)) for a in ARMS}
    L += [f"Paired seeds: {n}. Extinct by year 200: v {ext['v']}, c {ext['c']}, x {ext['x']}. Mean population, years "
          f"100–200: v {pop['v']:.1f}, c {pop['c']:.1f}, x {pop['x']:.1f}.", ""]

    # Primary
    pc = diff(lambda k: sp("c", k), lambda k: sp("v", k), "practised", "offered")
    px = diff(lambda k: sp("x", k), lambda k: sp("v", k), "practised", "offered")
    supports = pc[3] > 0 and pc[3] > px[4]
    L += ["## P (primary) — the spread of real practice (adults, years 100–200)", "",
          "Share of the situation–action pairs a person was offered in which they had at least one own learning update.",
          "", "| arm | share | − v [95%] |", "|---|---|---|",
          f"| v (v8) | {pc[1]:.4f} | |", f"| c (curiosity) | {pc[0]:.4f} | {f(pc)} |",
          f"| x (sham) | {px[0]:.4f} | {f(px)} |", "",
          f"**The frozen rule:** lower bound of c − v ({pc[3]:+.4f}) above 0 and above the sham's upper bound "
          f"({px[4]:+.4f}): **{'supports' if supports else 'does not support'}**.", ""]
    flag_ext = ext["c"] - ext["v"] >= 3
    flag_pop = pop["c"] < 0.90 * pop["v"]
    L += ["## F (flags, not gates)", "",
          f"- Extinct c {ext['c']} vs v {ext['v']}: {'FLAG' if flag_ext else 'no flag'}.",
          f"- Population years 100–200 c ÷ v = {pop['c'] / pop['v'] if pop['v'] else float('nan'):.3f} (sham "
          f"{pop['x'] / pop['v'] if pop['v'] else float('nan'):.3f}): {'FLAG' if flag_pop else 'no flag'}.", "",
          f"**{'The change is supported' if supports else 'The change is not supported'} by the frozen rule"
          f"{'; flagged, so adoption is not recommended' if (flag_ext or flag_pop) else ''}.** Adoption is left to "
          f"the creator.", ""]
    # Secondary
    L += ["## Secondary (described; years 100–200)", "", "| measure | v | c − v [95%] | x − v [95%] |",
          "|---|---|---|---|"]
    rows = [("make pairs practised (share of make pairs offered)", lambda a: (lambda k: sp(a, k)), "make_practised",
             "make_offered"),
            ("making events per adult-year", lambda a: (lambda k: cen(a, k)), "makes", "adults"),
            ("made things held per adult", lambda a: (lambda k: cen(a, k)), "items_adults", "adults"),
            ("world-born adults' (20–40) crafting skill", lambda a: (lambda k: cen(a, k)), "wb_craft_sum_20_40",
             "wb_adults_20_40")]
    for name, g, num, den in rows:
        dc = diff(g("c"), g("v"), num, den)
        dx = diff(g("x"), g("v"), num, den)
        L.append(f"| {name} | {dc[1]:.4f} | {f(dc)} | {f(dx)} |")
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
