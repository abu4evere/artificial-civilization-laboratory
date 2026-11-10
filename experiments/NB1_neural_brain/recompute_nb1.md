# NB1: independent blind recompute (10 November 2026)

- **Input:** `recompute/nb1_worlds.csv`, `nb1_gens.csv`, `nb1_g.csv` and `nb1_garden.csv`, built by
  `recompute/build_nb1_counts.py` (written before data): 48 worlds, 1,113 generation rows, 86 garden worlds.
- **The exact text sent:** `recompute/prompt.txt`, written and committed before the data existed. The four CSVs were
  attached as files.
- **Who** (each a fresh chat; none saw the analysis script or any earlier result):
  - GPT (Thinking, medium), chat `6af32c0d`: Python, 10,000 draws (its own seed 20261110);
  - Gemini 3.1 Pro (High), chat `d039a5c40af5db6d`: it ran code ("Show code"), 10,000 draws. Two earlier Gemini
    chats failed: `c2e7dd83d6e89477` stalled after loading the files (about 40 minutes), and a second disappeared
    without answering. The third was sent the same prompt plus one sentence for speed ("each world's slopes do not
    depend on the draw, so compute them once and resample the per-world values"), which does not change the method;
  - DeepSeek, chat `30594b2b`: **it had no code tool**. It computed the point values by hand. **Its own reasoning says it
    would make up plausible slope values and approximate the intervals** ("invent slopes but plausible"), so its
    slopes and its intervals are **not counted**. Only its hand-summed point values are recorded.
- **Recorded only from their actual replies.**

| quantity | analyse_nb1.py | GPT | Gemini | DeepSeek (hand point values only) |
|---|---|---|---|---|
| extinct worlds c / n / e | 1 / 3 / 3 | 1 / 3 / 3 | 1 / 3 / 3 | 1 / 3 / 3 |
| population n/c | 1.1677 [0.8825, 1.4587] | 1.16772 [0.88485, 1.46021] | 1.16772 [0.88915, 1.45876] | 1.16773 (sums 48,323,491 / 41,382,598) |
| population e/c | 1.4489 [1.1482, 1.7251] | 1.44894 [1.15507, 1.72453] | 1.44894 [1.15591, 1.73380] | 1.44894 |
| n slope, survival to 16 | +0.00371 [+0.00190, +0.00562] | +0.00371 [+0.00193, +0.00559] | 0.00371 [0.00191, 0.00561] | not counted (made up) |
| n slope, adult lifespan | +0.17941 [+0.10077, +0.25417] | +0.17941 [+0.10267, +0.25415] | 0.17941 [0.10195, 0.25360] | not counted |
| e slope, survival to 16 | +0.01255 [+0.00305, +0.03117] | +0.01255 [+0.00309, +0.03070] | 0.01255 [0.00307, 0.03115] | not counted |
| e slope, adult lifespan | +0.05680 [−0.04427, +0.14046] | +0.05680 [−0.04401, +0.14047] | 0.05680 [−0.04736, 0.14206] | not counted |
| mean g, n, years 1…600 | 1.001, 1.007, 1.022, 1.091, 1.109, 1.141, 1.190, 1.229 | 1.00103, 1.00687, 1.02241, 1.09079, 1.10910, 1.14057, 1.18956, 1.22939 | 1.00103, 1.00687, 1.02241, 1.09079, 1.10910, 1.14057, 1.18956, 1.22939 | 1.00103, 1.00687, 1.02241, 1.09079, 1.10910, 1.14057, 1.18956, 1.22939 |
| mean g, e, years 1…600 | 0.999, 0.993, 0.993, 1.038, 1.095, 1.178, 1.222, 1.272 | 0.99859, 0.99256, 0.99289, 1.03798, 1.09488, 1.17752, 1.22236, 1.27180 | 0.99859, 0.99256, 0.99289, 1.03798, 1.09488, 1.17752, 1.22236, 1.27180 | 0.99859, 0.99256, 0.99289, 1.03798, 1.09488, 1.17752, 1.22236, 1.27180 |
| g18N − g1N (13 sources) | +0.00537 [−0.03104, +0.04412] | +0.00537 [−0.03278, +0.04510] | 0.00537 [−0.03175, 0.04421] | +0.00537 |
| learning on − off, pooled (43) | −0.04504 [−0.06538, −0.02444] | −0.04504 [−0.06534, −0.02642] | −0.04504 [−0.06580, −0.02677] | −0.04611 (see note) |
| reading | decorative | decorative | decorative | decorative |

- **DeepSeek's pooled value:** it summed all 43 pairs (16 + 14 + 13; sum −1.93671) but divided by 42. Divided by 43 it
  is −0.04504, the same as the analysis. Recorded as its arithmetic slip, not as a disagreement.
- **GPT and Gemini agree with the analysis** on every point value and on the reading; their interval ends differ from the
  analysis by at most 0.003 (slopes and garden) and 0.009 (population).
- **GPT's note:** "Positive generational slopes coexist with increasing g". It added that this is "a classification under
  NB1's predefined criteria, not proof that the neural network contributed nothing to behavior."

**All agree: decorative. NB1 is final.**
