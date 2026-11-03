# HN1: independent blind recompute (3 November 2026)

- **Input:** `recompute/hn1_counts.csv` (32 rows). Per world: the funnel counts, the food from hunting and foraging,
  living weeks and extinction. It was built by `recompute/build_hn1_counts.py`, written before data.
- **The exact text sent:** `recompute/prompt.txt`, written and committed before the data existed. The CSV was attached
  as a file.
- **Who** (each a fresh chat; none saw the analysis script or any earlier result):
  - GPT, chat `6ae99e3b`: Python, 10,000 draws;
  - Gemini 3.1 Pro (High), chat `a43e31c647c81a4e`: it ran code;
  - DeepSeek, chat `c685650b`: by hand. Its sums are exact (870.0 food from 1,831 hunter-weeks; 115,979,160.584 food
    from 5,583,050 forage-weeks).
- **Recorded only from their actual replies.**

| quantity | analyse_hn1.py | GPT | Gemini | DeepSeek |
|---|---|---|---|---|
| F | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | 0 [0.0000, 0.0000] |
| routing | base chance (no straddle) | base chance (no straddle) | base chance (no straddle) | base chance (no straddle) |
| R (pooled) | 0.0229 [0.0186, 0.0272] | 0.0229 [0.0185, 0.0271] | 0.0229 [0.0187, 0.0273] | ≈0.0229 [0.0190, 0.0275] |
| shares: no prey / roll failed / success | 0.0000 / 0.9459 / 0.0541 | the same | the same | the same |
| R inside 0.5–1.5? | no | no | no | no (see below) |

- **The range answer:** DeepSeek's reply was cut short on the page at "(5) Is R inside 0.5…", so its range answer was
  not read. It follows from its R of 0.0229.
- **GPT's note:** the result "identifies the failed-success-roll stage as the observed bottleneck, but does not
  establish that changing the base chance alone will improve overall outcomes". This agrees with the ceiling in the
  findings.
- **All three agree with the analysis** on every value, the routing and the shares. Interval ends differ by at most
  0.0004.

**HN1 is final.** All three tabs were closed.
