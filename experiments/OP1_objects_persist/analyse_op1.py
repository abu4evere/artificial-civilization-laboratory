"""OP1 analysis, written before any data (questions.md, frozen as `OP1-frozen`; operational note 1).

  python experiments/OP1_objects_persist/analyse_op1.py            # writes results.md
  python experiments/OP1_objects_persist/analyse_op1.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_op1 import ARMS, SEEDS  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261027)


def cnt(r, k):
    return r["counts"].get(k, 0.0)


def census(r, y0, y1, num, den):
    F = r["census_fields"]
    rows = [row for row in r["census"] if y0 <= row[0] < y1]
    if den is None:
        return sum(row[F.index(num)] for row in rows), len(rows)
    return sum(row[F.index(num)] for row in rows), sum(row[F.index(den)] for row in rows)


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
    L = ["# OP1 — Objects in the world. Results", "",
         "Frozen as `OP1-frozen` (operational note 1). run_op1.py, analyse_op1.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({sum(len(runs[a]) for a in ARMS)} of {len(SEEDS) * len(ARMS)}): **{'yes' if present else 'NO'}**",
         f"- One fingerprint (`code_op1`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- Every overflow dropped and dropped = picked up + on the ground (mismatches 0): "
         f"**{'yes' if mism == 0 else f'NO ({mism})'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    seeds = sorted(set(runs["c"]) & set(runs["o"]) & set(runs["x"]))
    n = len(seeds)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))])
    o = [runs["o"][s] for s in seeds]
    # M
    over_worlds = [r for r in o if cnt(r, "keep_overflow") > 0]
    m_ok = all(cnt(r, "drops") > 0 for r in over_worlds) and sum(cnt(r, "deleted_at_limit") for r in o) == 0
    c_del = sum(cnt(runs["c"][s], "deleted_at_limit") for s in seeds)
    L += [f"## M — manipulation", "",
          f"Arm o: {sum(cnt(r, 'keep_overflow') for r in o):.0f} carry-limit overflows from making, "
          f"{sum(cnt(r, 'drops') for r in o):.0f} drops (with inheritance), {sum(cnt(r, 'deleted_at_limit') for r in o):.0f} "
          f"deleted; every world with an overflow has drops: {all(cnt(r, 'drops') > 0 for r in over_worlds)}. "
          f"Arm c: {c_del:.0f} made things deleted at the limit. **M {'passes' if m_ok else 'FAILS'}.**", ""]
    # P
    drops = np.array([cnt(r, "drops") for r in o])
    picks = np.array([cnt(r, "pickups") for r in o])
    other = np.array([cnt(r, "pickups_by_other") for r in o])
    p = picks.sum() / drops.sum() if drops.sum() else float("nan")
    with np.errstate(divide="ignore", invalid="ignore"):
        reps = (W @ picks) / (W @ drops)
    reps = reps[np.isfinite(reps)]
    lo, hi = np.percentile(reps, [2.5, 97.5])
    p_ok = p >= 0.05 and lo > 0
    oth = other.sum() / picks.sum() if picks.sum() else float("nan")
    meds = [r["pickup_weeks_median"] for r in o if r["pickup_weeks_median"] is not None]
    L += ["## P — primary: of the things dropped, the share later picked up by a living person (arm o)", "",
          f"Dropped {drops.sum():.0f}; picked up {picks.sum():.0f}: **{p:.4f} [{lo:.4f}, {hi:.4f}]**; by someone other than "
          f"the one who dropped it {oth:.3f} of pick-ups; on the ground at the end {sum(cnt(r, 'ground_end') for r in o):.0f}; "
          f"median weeks on the ground (median of world medians) {np.median(meds) if meds else float('nan'):.1f}.",
          f"**P {'supports' if p_ok else 'does not support'}** (at least 0.05 with the lower bound above 0).", ""]
    # H flags
    def popmean(arm):
        s_ = [census(runs[arm][s], 100, 200, "living", None) for s in seeds]
        return sum(a for a, _ in s_) / max(sum(b for _, b in s_), 1)
    pc, po, px = popmean("c"), popmean("o"), popmean("x")
    ext = {a: sum(1 for s in seeds if runs[a][s]["extinct"]) for a in ARMS}
    flag_pop = po < 0.90 * pc
    flag_ext = ext["o"] - ext["c"] >= 3
    L += ["## H — flags", "",
          f"Mean population, years 100-200: c {pc:.1f}, o {po:.1f} (ratio {po / pc if pc else float("nan"):.3f}), sham {px:.1f} "
          f"({'FLAG' if flag_pop else 'no flag'}). Extinct: c {ext['c']}, o {ext['o']}, sham {ext['x']} "
          f"({'FLAG' if flag_ext else 'no flag'}).", ""]
    # D
    def ratio(arm, num, den, y0=50, y1=200):
        s_ = [census(runs[arm][s], y0, y1, num, den) for s in seeds]
        return sum(a for a, _ in s_) / max(sum(b for _, b in s_), 1)
    L += ["## D — described (years 50-200)", "", "| measure | c | o | sham |", "|---|---|---|---|",
          f"| made things held per adult | {ratio('c', 'items_adults', 'adults'):.3f} | {ratio('o', 'items_adults', 'adults'):.3f} | "
          f"{ratio('x', 'items_adults', 'adults'):.3f} |",
          f"| making events per adult-year | {ratio('c', 'makes', 'adults'):.3f} | {ratio('o', 'makes', 'adults'):.3f} | "
          f"{ratio('x', 'makes', 'adults'):.3f} |", ""]
    L += [f"**{'The change is supported' if (m_ok and p_ok) else 'The change is not supported'} by the frozen rule"
          f"{'; flagged, so adoption is not recommended' if (flag_pop or flag_ext) else ''}.** Adoption is left to the creator.", ""]
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
