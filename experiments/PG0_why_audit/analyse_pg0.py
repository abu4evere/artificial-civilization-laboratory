"""PG0 analysis, written before any data (questions.md, frozen as `PG0-frozen`; operational note 1).

  python experiments/PG0_why_audit/analyse_pg0.py            # writes results.md
  python experiments/PG0_why_audit/analyse_pg0.py --smoke --dir <folder>
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from run_pg0 import SEEDS  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUTDIR = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else HERE / "output"
REPS = 10_000
RNG = np.random.default_rng(20261027)


def cnt(r, k):
    return r["counts"].get(k, 0.0)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rs = [json.load(open(f)) for f in sorted(glob.glob(str(OUTDIR / "*_seed_*.json")))]
    zero = (OUTDIR / "zero.txt").read_text(encoding="utf-8") if (OUTDIR / "zero.txt").exists() else ""
    fps = {r["code_hash"] for r in rs} | {r["code_hash_after"] for r in rs}
    mism = sum(sum(r["mismatch"].values()) for r in rs)
    seeds_ok = sorted(r["seed"] for r in rs) == sorted(SEEDS)
    ok = "All: PASS" in zero and seeds_ok and len(fps) == 1 and mism == 0
    L = ["# PG0 — The \"why\" audit. Results", "",
         "Frozen as `PG0-frozen` (operational note 1). run_pg0.py, analyse_pg0.py (written before data).", "",
         "## Validity", "",
         f"- Zero checks: **{'yes' if 'All: PASS' in zero else 'NO'}**",
         f"- All worlds present ({len(rs)} of {len(SEEDS)}): **{'yes' if seeds_ok else 'NO'}**",
         f"- One fingerprint (`code_v7`): **{'yes' if len(fps) == 1 else 'NO'}**",
         f"- Mismatches 0: **{'yes' if mism == 0 else f'NO ({mism})'}**", "",
         f"**{'Valid.' if ok else 'NOT VALID: no reading is drawn.'}**", ""]
    if not ok and not SMOKE:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    n = len(rs)
    W = np.stack([np.bincount(row, minlength=n) for row in RNG.integers(0, n, size=(REPS, n))])

    def v(k):
        return np.array([cnt(r, k) for r in rs], float)

    def ratio(num, den):
        a, b = v(num), v(den)
        with np.errstate(divide="ignore", invalid="ignore"):
            reps = (W @ a) / (W @ b)
        reps = reps[np.isfinite(reps)]
        lo, hi = np.percentile(reps, [2.5, 97.5]) if len(reps) else (np.nan, np.nan)
        return (a.sum() / b.sum() if b.sum() else float("nan")), lo, hi, a.sum(), b.sum()

    def fmt(t):
        return f"{t[0]:.4f} [{t[1]:.4f}, {t[2]:.4f}] ({t[3]:.0f} / {t[4]:.0f})"

    pop = sum(sum(row[1] for row in r["census"]) for r in rs) / max(sum(len(r["census"]) for r in rs), 1)
    L += [f"{n} worlds; mean living population over all years {pop:.1f}.", ""]
    # Q1
    plays = v("play:led") + v("play:free")
    L += ["## Q1 — Curiosity: does puzzle-led play find useful new kinds?", "",
          f"Puzzle-led play: {v('play:led').sum():.0f} of {plays.sum():.0f} plays "
          f"({v('play:led').sum() / plays.sum():.4f}).", "",
          "| play | plays | new-to-world kinds per play | of those, useful | of the useful, remade later |",
          "|---|---|---|---|---|"]
    for tag in ("led", "free"):
        a = ratio(f"newworld:{tag}", f"play:{tag}")
        b = ratio(f"newworld_useful:{tag}", f"newworld:{tag}")
        c = ratio(f"newworld_useful_remade:{tag}", f"newworld_useful:{tag}")
        L.append(f"| {tag} | {v(f'play:{tag}').sum():.0f} | {fmt(a)} | {fmt(b)} | {fmt(c)} |")
    led_rate = ratio("newworld_useful:led", "play:led")[0]
    free_rate = ratio("newworld_useful:free", "play:free")[0]
    led_n = v("newworld_useful:led")
    free_n = v("newworld_useful:free")
    with np.errstate(divide="ignore", invalid="ignore"):
        dreps = (W @ led_n) / (W @ v("play:led")) - (W @ free_n) / (W @ v("play:free"))
    dreps = dreps[np.isfinite(dreps)]
    lo, hi = np.percentile(dreps, [2.5, 97.5]) if len(dreps) else (np.nan, np.nan)
    L += ["", f"**Useful new-to-world kinds per play, puzzle-led minus other: {led_rate - free_rate:+.4f} [{lo:+.4f}, {hi:+.4f}].** "
              "(Described, not causal.)", ""]
    # Q2
    used = v("new_useful_used_by_maker").sum()
    gone = v("new_useful_lost_gone").sum()
    dead = v("new_useful_lost_dead").sum()
    tot = used + gone + dead
    L += ["## Q2 — The zero start", "",
          f"- At first use of a kind: mean |felt − worth before| = {fmt(ratio('first_err_before:all', 'first:all'))}.",
          f"- New useful kinds made in play: used by their maker {used:.0f}; lost before use: gone from hand {gone:.0f}, "
          f"maker died {dead:.0f}; share lost before use **{(gone + dead) / tot if tot else float('nan'):.4f}** "
          f"(of {tot:.0f}; {v('new_useful_pending_end').sum():.0f} still pending at the end).",
          f"- Uses until worth is within 0.1 of the felt value: mean {v('uses_to_learn').sum() / max(v('learned').sum(), 1):.2f} "
          f"({v('learned').sum():.0f} person-kinds learned).", ""]
    # Q3
    L += ["## Q3 — Is information available? Prediction error at first use of a new kind (own past uses only)", "",
          "| predictor | mean absolute error [95%] |", "|---|---|"]
    for name, k in (("own-experience property neighbours (k = 5)", "pred_err_knn:all"),
                    ("shuffled properties (control)", "pred_err_shuf:all"),
                    ("zero start (today)", "pred_err_zero:all")):
        L.append(f"| {name} | {fmt(ratio(k, 'pred_n:all'))} |")
    a, b, d = v("pred_err_knn:all"), v("pred_err_shuf:all"), v("pred_n:all")
    with np.errstate(divide="ignore", invalid="ignore"):
        reps = (W @ b - W @ a) / (W @ d)
    reps = reps[np.isfinite(reps)]
    lo, hi = np.percentile(reps, [2.5, 97.5])
    gain = (b.sum() - a.sum()) / d.sum()
    L += ["", f"First uses with at least 5 past uses for the same purpose: {d.sum():.0f}; without: {v('pred_nohist:all').sum():.0f}.", "",
          f"**Shuffled minus property error: {gain:+.4f} [{lo:+.4f}, {hi:+.4f}]: information "
          f"{'IS' if lo > 0 else 'is NOT shown to be'} available in a person's own past experience.**", ""]
    text = "\n".join(L) + "\n"
    if not SMOKE:
        (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
