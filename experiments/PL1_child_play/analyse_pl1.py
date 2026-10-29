"""PL1 analysis, written before any data (questions.md, frozen as `PL1-frozen`).

  python experiments/PL1_child_play/analyse_pl1.py            # writes results.md
  python experiments/PL1_child_play/analyse_pl1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_pl1  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
SEEDS = run_pl1.SMOKE_SEEDS if SMOKE else run_pl1.SEEDS
WPY = run_pl1.WPY
BANDS = [f"{lo}-{hi}" for lo, hi in run_pl1.BANDS]
REPS = 10_000
RNG = np.random.default_rng(20261029)
LOW, HIGH = 0.09, 0.58         # Lew-Levy et al. 2022: play at ages 3-6 across 12 forager societies


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    runs = {}
    for f in sorted(glob.glob(str(OUTDIR / "o_seed_*.json"))):
        r = json.load(open(f))
        runs[r["seed"]] = r
    zero = (OUTDIR / "zero.txt").read_text(encoding="utf-8") if (OUTDIR / "zero.txt").exists() else ""
    present = sorted(runs) == sorted(SEEDS)
    fps = {r["code_hash"] for r in runs.values()} | {r["code_hash_after"] for r in runs.values()}
    mism = sum(sum(r["mismatch"].values()) for r in runs.values())
    ok = "All: PASS" in zero and present and len(fps) == 1 and mism == 0
    L = ["# PL1 — How much do ACL's children play, against forager children? Results"
         + (" (SMOKE TEST, throwaway seeds)" if SMOKE else ""), "",
         "Frozen as `PL1-frozen`. run_pl1.py, analyse_pl1.py (written before data).", "", "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({len(runs)} of {len(SEEDS)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint (`code_v8`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- Wrapper counts match the law (mismatches 0): **{'yes' if mism == 0 else f'NO ({mism})'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    seeds = sorted(runs)
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))])

    def col(key, src="counts"):
        return np.array([float(runs[s][src].get(key, 0)) for s in seeds])

    def ratio(num, den):
        point = num.sum() / den.sum() if den.sum() else float("nan")
        with np.errstate(invalid="ignore", divide="ignore"):
            reps = (W @ num) / (W @ den)
        reps = reps[np.isfinite(reps)]
        lo, hi = np.percentile(reps, [2.5, 97.5]) if len(reps) else (float("nan"),) * 2
        return point, lo, hi

    def fmt(t, d=4):
        return f"{t[0]:.{d}f} [{t[1]:.{d}f}, {t[2]:.{d}f}]"

    living = sum(sum(row[1] for row in runs[s]["census"]) for s in seeds)
    years = sum(len(runs[s]["census"]) for s in seeds)
    ext = sum(1 for s in seeds if runs[s]["extinct"])
    L += [f"Worlds: {n}; extinct {ext}. Mean living population {living / max(years, 1):.1f}.", ""]

    L += ["## Q1–Q2 — Play share, availability and choice, by age band (person-weeks)", "",
          "| ages | weeks | **play share** | play available | chosen when available | no-play weeks: unavailable / "
          "available |", "|---|---|---|---|---|---|"]
    share = {}
    for b in BANDS:
        wk = col(f"{b}|weeks")
        ps = ratio(col(f"{b}|play"), wk)
        av = ratio(col(f"{b}|avail"), wk)
        ca = ratio(col(f"{b}|play_when_avail"), col(f"{b}|avail"))
        nu, na = col(f"{b}|noplay_unavail").sum(), col(f"{b}|noplay_avail").sum()
        share[b] = ps
        L.append(f"| {b} | {wk.sum():,.0f} | **{fmt(ps)}** | {fmt(av, 3)} | {fmt(ca)} | "
                 f"{nu / max(nu + na, 1):.3f} / {na / max(nu + na, 1):.3f} |")
    L.append("")

    # Frozen readings
    s36 = share["3-6"]
    if s36[2] < LOW:
        read = "below the human range"
    elif LOW <= s36[1] and s36[2] <= HIGH:
        read = "within the human range"
    elif s36[1] > HIGH:
        read = "above the human range"
    else:
        read = "overlaps the edge of the human range"
    decline = share["3-6"][0] > share["7-12"][0] > share["13-18"][0]
    nu, na = col("3-6|noplay_unavail").sum(), col("3-6|noplay_avail").sum()
    neck = "availability" if nu > na else "choice"
    L += ["## The frozen readings (descriptive; the human range is context, not an equivalence test)", "",
          f"- **Ages 3–6 against the human range ({LOW:.2f}–{HIGH:.2f}; Lew-Levy et al. 2022):** play share "
          f"{fmt(s36)}: **{read}**.",
          f"- **Decline with age** (3–6 > 7–12 > 13–18): **{'yes' if decline else 'no'}** "
          f"({share['3-6'][0]:.4f}, {share['7-12'][0]:.4f}, {share['13-18'][0]:.4f}).",
          f"- **The bottleneck at ages 3–6:** of weeks without play, {nu / max(nu + na, 1):.3f} had no play available "
          f"and {na / max(nu + na, 1):.3f} had it available but chose something else: **{neck}**.",
          "- Caveat: one action per week in ACL against shares of daytime observations in the human data.", ""]

    L += ["## Q3 — Where children's crafting skill comes from (summed skill gained)", "",
          "| ages | in play | in making | otherwise | share from play |", "|---|---|---|---|---|"]
    for b in BANDS + ["other_ages"]:
        p_, m_, o_ = (col(f"{b}|craft_{k}").sum() for k in ("play", "make", "other"))
        tot = p_ + m_ + o_
        L.append(f"| {b if b != 'other_ages' else 'infants and 19+'} | {p_:.2f} | {m_:.2f} | {o_:.2f} | "
                 f"{p_ / tot if tot else float('nan'):.3f} |")
    L += ["", "## Q4 — Play share among children who lived through the whole band", "",
          "| ages | children | weeks | play share |", "|---|---|---|---|"]
    for b in BANDS:
        sw = col(f"{b}|weeks", "survivors")
        sp = col(f"{b}|play", "survivors")
        L.append(f"| {b} | {col(f'{b}|children', 'survivors').sum():,.0f} | {sw.sum():,.0f} | {fmt(ratio(sp, sw))} |")
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
