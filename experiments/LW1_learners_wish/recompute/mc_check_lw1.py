"""LW1: how much the co-primary's lower bound moves with the bootstrap's own random draws. Written AFTER data
(7 November 2026), when GPT's and Gemini's blind recomputes matched every point estimate but put the lower bound at
+0.0002 and +0.0001 against the frozen analysis's -0.0001 (random seed 20261109). It changes nothing in the frozen
reading; it only shows the cause of the disagreement.

The method is analyse_lw1.py's, unchanged: paired world bootstrap, the same drawn seeds for every arm, pooled sums,
numpy percentiles 2.5 and 97.5. Only the random seed and the number of draws vary.

  python experiments/LW1_learners_wish/recompute/mc_check_lw1.py
"""
import csv
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
rows = list(csv.DictReader(open(HERE / "lw1_counts.csv")))
seeds = sorted({int(r["seed"]) for r in rows})
get = {(r["arm"], int(r["seed"])): r for r in rows}


def col(a, k):
    return np.array([float(get[(a, s)][k]) for s in seeds])


lc, kc, lw, kw = col("c", "lw_learned"), col("c", "lw_kinds"), col("w", "lw_learned"), col("w", "lw_kinds")
n = len(seeds)
print(f"point estimate w - c: {lw.sum() / kw.sum() - lc.sum() / kc.sum():+.5f} ({int(lw.sum())}/{int(kw.sum())} "
      f"against {int(lc.sum())}/{int(kc.sum())})")


def lower(rng_seed, reps):
    rng = np.random.default_rng(rng_seed)
    W = np.stack([np.bincount(row, minlength=n) for row in rng.integers(0, n, size=(reps, n))]).astype(float)
    d = (W @ lw) / (W @ kw) - (W @ lc) / (W @ kc)
    return float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5)), float((d <= 0).mean())


lo, hi, p0 = lower(20261109, 10_000)
print(f"frozen random seed 20261109, 10,000 draws: [{lo:+.5f}, {hi:+.5f}]; share of draws <= 0: {p0:.4f}")
los = [lower(s, 10_000)[0] for s in range(1, 51)]
above = sum(1 for v in los if v > 0)
print(f"50 other random seeds (1-50), 10,000 draws each: lower bound min {min(los):+.5f}, median "
      f"{float(np.median(los)):+.5f}, max {max(los):+.5f}; above 0 in {above} of 50")
lo, hi, p0 = lower(7, 200_000)
print(f"random seed 7, 200,000 draws: [{lo:+.5f}, {hi:+.5f}]; share of draws <= 0: {p0:.4f}")
