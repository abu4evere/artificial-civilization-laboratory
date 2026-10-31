"""TR1 analysis, written before any data (questions.md, frozen as `TR1-frozen`; operational note 1).

  python experiments/TR1_tool_returns/analyse_tr1.py            # writes results.md
  python experiments/TR1_tool_returns/analyse_tr1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_tr1 import SEEDS  # noqa: E402

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
    L = ["# TR1 — What do tools really add? Results", "",
         "Frozen as `TR1-frozen` (operational note 1). run_tr1.py, analyse_tr1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({len(runs)} of {len(SEEDS)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint (`code_v10`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- Replayed forage yield = food actually got (mismatches 0): **{'yes' if mism == 0 else f'NO ({mism})'}**",
         "", f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    seeds = sorted(runs)
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))])

    def col(k):
        return np.array([float(runs[s]["sums"].get(k, 0.0)) for s in seeds])

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
    L += [f"Worlds: {n}; extinct {ext}. Mean living population {liv / yrs if yrs else float('nan'):.1f}; "
          f"adults in years 100-200: {np.mean([c[2] for c in late]) if late else float('nan'):.1f} per world-year.",
          f"Adult forage weeks, years 100-200: {col('weeks').sum():,.0f} (with a tool in hand: "
          f"{col('tool_weeks').sum():,.0f}); adult hunts: {col('hunts').sum():,.0f}.", ""]

    wi, wo, kn, wb = col("with"), col("without"), col("known"), col("world")
    q1 = boot(wi - wo, wi)
    ha = boot(kn - wi, wi)
    hb = boot(wb - wi, wi)
    L += ["## Q1 — Food added by tools (adults' foraging, years 100-200)", "",
          "| measure | share of foraged food [95%] |", "|---|---|",
          f"| **realized: (food got - food without a tool) / food got** | **{f3(q1)}** |",
          f"| headroom (a): with the best tool the person knows, more than got | {f3(ha)} |",
          f"| **headroom (b): with the best tool in anyone's hands, more than got** | **{f3(hb)}** |", ""]

    tw = col("tool_weeks")
    L += ["## Q2 — Where the tool's help goes (tool-aided adult forage weeks)", "",
          "| outcome | share [95%] |", "|---|---|"]
    for k, lab in (("zero", "added nothing (carry room or plants bound)"), ("partial", "partly capped"),
                   ("full", "fully realized")):
        L.append(f"| {lab} | {f3(boot(col('tw_' + k), tw))} |")
    L += ["", f"**Efficiency ratio** (realized food added / uncapped food added): {f3(boot(col('added'), col('uncapped')))}.", "",
          "## Q3 — Felt against real (per tool-aided week)", "",
          f"- Mean felt help (factor - 1): {f3(boot(col('felt'), tw))}",
          f"- Mean normalized realized gain ((with / without) - 1): {f3(boot(col('norm_gain'), col('norm_n')))} "
          f"(same weeks' felt help {f3(boot(col('felt_n'), col('norm_n')))})", ""]

    hw, hn, hwb = col("h_with"), col("h_without"), col("h_world")
    kills = np.array([runs[s]["kills_all"][0] for s in seeds], float)
    meat = np.array([runs[s]["kills_all"][1] for s in seeds], float)
    mpk = meat.sum() / kills.sum() if kills.sum() else float("nan")
    L += ["## Q4c — Hunting (adult hunts, years 100-200; expected kills, not food produced)", "",
          "| measure | value [95%] |", "|---|---|",
          f"| expected kills per hunt with the hunters' tools | {f3(boot(hw, col('hunts')))} |",
          f"| without tools | {f3(boot(hn, col('hunts')))} |",
          f"| with the best hunting tool in anyone's hands | {f3(boot(hwb, col('hunts')))} |",
          f"| **tools' share of expected kills: (with - without) / with** | **{f3(boot(hw - hn, hw))}** |",
          f"| headroom: (world best - with) / with | {f3(boot(hwb - hw, hw))} |", "",
          f"Mean meat per kill (all kills, whole run): {mpk:.2f}. Expected meat from tools in years 100-200: "
          f"{(hw - hn).sum() * mpk:,.1f}, against {wi.sum():,.0f} foraged by adults.", ""]

    meat_ad = col("hunt_meat_adults")
    L += ["## Q6 — For scale: where adults' food comes from (years 100-200)", "",
          f"- Foraged by adults: {wi.sum():,.0f}; hunted meat shared to adults (before the carry cap): "
          f"{meat_ad.sum():,.0f}. Hunting's share: {f3(boot(meat_ad, wi + meat_ad))}.", "",
          "## Q5 — By season (adults' foraging, years 100-200)", "",
          "| season | realized share | headroom (a) | headroom (b) |", "|---|---|---|---|"]
    seasons = sorted({k for s in seeds for k in runs[s]["season"]}, key=str)
    for se in seasons:
        a = np.array([runs[s]["season"].get(se, [0, 0, 0, 0]) for s in seeds], float)
        L.append(f"| {se} | {f3(boot(a[:, 0] - a[:, 1], a[:, 0]))} | {f3(boot(a[:, 2] - a[:, 0], a[:, 0]))} | "
                 f"{f3(boot(a[:, 3] - a[:, 0], a[:, 0]))} |")
    L.append("")

    if q1[0] < 0.05 and hb[0] < 0.10:
        reading, near = "knowing barely matters", q1[2] >= 0.05 or hb[2] >= 0.10
    elif hb[0] >= 0.10 and q1[0] < hb[0] / 2:
        reading, near = "knowing matters but is unused", hb[1] < 0.10 or q1[2] >= hb[0] / 2
    else:
        reading, near = "knowing matters and is used", (hb[1] < 0.10 <= hb[2]) or (q1[1] < 0.05 <= q1[2])
    L += ["## The frozen reading", "",
          f"- Realized share {q1[0]:.3f} [{q1[1]:.3f}, {q1[2]:.3f}] (< 0.05 for 'barely'); headroom (b) "
          f"{hb[0]:.3f} [{hb[1]:.3f}, {hb[2]:.3f}] (< 0.10 for 'barely'; >= 0.10 with realized < half of it for "
          "'unused').", "",
          f"**Reading: {reading.upper()}{' (near the line)' if near else ''}.**", ""]
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
