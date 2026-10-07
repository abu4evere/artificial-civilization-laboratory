"""T1 — exact two-sided sign test on the paired worlds that changed fate (exploratory; after the frozen analysis).

  python experiments/T1_threshold_align/paired_test.py
"""
from math import comb

saved, lost = 7, 12          # from results.md (paired with F1)
n = saved + lost
k = min(saved, lost)
p = min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)
print(f"discordant worlds {n} (saved {saved}, lost {lost}); exact two-sided sign test p = {p:.3f}")
