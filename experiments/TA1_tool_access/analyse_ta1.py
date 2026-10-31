"""TA1 analysis, written before any data (questions.md, frozen as `TA1-frozen`; operational note 1).

  python experiments/TA1_tool_access/analyse_ta1.py            # writes results.md
  python experiments/TA1_tool_access/analyse_ta1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_ta1 import SEEDS  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261031)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {}
    for f in sorted(glob.glob(str(OUTDIR / "lp_seed_*.json"))):
        r = json.load(open(f))
        runs[r["seed"]] = r
    zero = (OUTDIR / "zero.txt").read_text(encoding="utf-8") if (OUTDIR / "zero.txt").exists() else ""
    present = sorted(runs) == sorted(SEEDS)
    fps = {r["code_hash"] for r in runs.values()} | {r["code_hash_after"] for r in runs.values()}
    mism = sum(sum(r["mismatch"].values()) for r in runs.values())
    ok = "All: PASS" in zero and present and len(fps) == 1 and mism == 0
    L = ["# TA1 — Why do tools not reach hands? Results", "",
         "Frozen as `TA1-frozen` (operational note 1). run_ta1.py, analyse_ta1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({len(runs)} of {len(SEEDS)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint (`code_v10`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- Forage-tool accounting exact; no worn tool still in hand (mismatches 0): "
         f"**{'yes' if mism == 0 else f'NO ({mism})'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    seeds = sorted(runs)
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))])

    def col(k, part="q1"):
        return np.array([float(runs[s][part].get(k, 0)) for s in seeds])

    def boot(num, den):
        point = num.sum() / den.sum() if den.sum() else float("nan")
        with np.errstate(invalid="ignore", divide="ignore"):
            reps = (W @ num) / (W @ den)
        lo, hi = np.nanpercentile(reps, [2.5, 97.5])
        return point, lo, hi

    def f3(t):
        return f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"

    liv = sum(sum(c[1] for c in runs[s]["census"]) for s in seeds)
    yrs = sum(len(runs[s]["census"]) for s in seeds)
    late = [c for s in seeds for c in runs[s]["census"] if 100 <= c[0] < 200]
    ext = sum(1 for s in seeds if runs[s]["extinct"])
    bare = col("bare")
    tih = col("tool_in_hand")
    L += [f"Worlds: {n}; extinct {ext}. Mean living population {liv / yrs if yrs else float('nan'):.1f}; adults in "
          f"years 100-200: {np.mean([c[2] for c in late]) if late else float('nan'):.1f} per world-year; forage tools "
          f"in hand at year ends (years 100-200): {np.mean([c[3] for c in late]) if late else float('nan'):.1f} per world.",
          f"Adult forage weeks, years 100-200: {bare.sum() + tih.sum():,.0f}; bare-handed {bare.sum():,.0f} "
          f"({f3(boot(bare, bare + tih))}).", ""]

    a = boot(col("a"), bare)
    b = boot(col("b"), bare)
    L += ["## Q1 — Why is a forager bare-handed? (share of bare-handed adult forage weeks)", "",
          "| flag | share [95%] |", "|---|---|",
          f"| **(a) a forage tool in someone's hands within 3 tiles** | **{f3(a)}** |",
          f"| (a') the same, and the forager has room to receive it | {f3(boot(col('a_feasible'), bare))} |",
          f"| **(b) knows a helpful kind and could make it now** | **{f3(b)}** |",
          f"| (c) knows a helpful kind but lacks the materials | {f3(boot(col('c'), bare))} |",
          f"| (d) knows no helpful kind | {f3(boot(col('d'), bare))} |",
          f"| (e) hands full (3 items, none for foraging) | {f3(boot(col('e'), bare))} |",
          f"| empty hands (0 items) | {f3(boot(col('empty'), bare))} |",
          f"| hands holding other things (1-3 non-forage items) | {f3(boot(col('clogged'), bare))} |", "",
          "Priority partition (Gemini): " + "; ".join(f"{k} {boot(col('prio_' + k), bare)[0]:.3f}"
                                                       for k in ("e", "b", "c", "d")) + ".", ""]
    q5w = np.array([runs[s]["q5"][0] for s in seeds])
    q5o = np.array([runs[s]["q5"][1] for s in seeds])
    L += [f"**Q5** (described): in the (a') weeks, the nearest holder's actual tool would add "
          f"{f3(boot(q5w - q5o, q5o))} to those forages' food (TR1's arithmetic, with the carry room and plants).", ""]

    hold = {}
    for s in seeds:
        for k, v in runs[s]["hold"].items():
            hold[k] = hold.get(k, 0) + v
    L += ["## Q2 — Who holds forage tools (person-weeks, years 100-200)", "",
          "| age | person-weeks | share holding a forage tool |", "|---|---|---|"]
    for bd in ("0-11", "12-15", "16-39", "40-59", "60+"):
        h, no = hold.get(f"{bd}|1", 0), hold.get(f"{bd}|0", 0)
        L.append(f"| {bd} | {h + no:,} | {h / (h + no) if h + no else float('nan'):.3f} |")
    hf = {}
    for s in seeds:
        for k, v in runs[s]["hold_forage"].items():
            hf[k] = hf.get(k, 0) + v
    tot = hf.get("1", 0) + hf.get("0", 0)
    L += ["", f"Adult holders who foraged that week: {hf.get('1', 0) / tot if tot else float('nan'):.3f} of {tot:,} "
              "holder-weeks.", ""]

    def tally(part):
        t = {}
        for s in seeds:
            for k, v in runs[s][part].items():
                t[k] = t.get(k, 0) + v
        return t
    en, ex, mk = tally("enter"), tally("exit"), tally("makes")
    hw = sum(runs[s]["held_weeks"][0] for s in seeds)
    hn = sum(runs[s]["held_weeks"][1] for s in seeds)
    L += ["## Q3 and Q4 — How forage tools enter and leave hands (all ages, whole run)", "",
          "| enter | count | share |", "|---|---|---|"]
    te = sum(en.values())
    for k, v in sorted(en.items(), key=lambda x: -x[1]):
        L.append(f"| {k} | {v:,} | {v / te:.3f} |")
    L += ["", "| leave | count | share |", "|---|---|---|"]
    tx = sum(ex.values())
    for k, v in sorted(ex.items(), key=lambda x: -x[1]):
        L.append(f"| {k} | {v:,} | {v / tx:.3f} |")
    tm = sum(mk.values())
    L += ["", f"Mean weeks a forage tool stays in one hand: {hw / hn if hn else float('nan'):.1f} ({hn:,} exits).",
          f"Forage-tool makes by someone already holding one: {mk.get('by_holder', 0) / tm if tm else float('nan'):.3f} "
          f"of {tm:,}.", ""]

    access, choice = a[0] >= 0.50, b[0] >= 0.50
    reading = "both" if access and choice else "access gap" if access else "choice gap" if choice else "neither"
    L += ["## The frozen reading", "",
          f"- (a) {a[0]:.3f} [{a[1]:.3f}, {a[2]:.3f}] (>= 0.50 for 'access gap'); (b) {b[0]:.3f} [{b[1]:.3f}, "
          f"{b[2]:.3f}] (>= 0.50 for 'choice gap').", "",
          f"**Reading: {reading.upper()}.** (A classification, not causal proof; GPT.)", ""]
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
