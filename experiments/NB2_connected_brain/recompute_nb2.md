# NB2: independent blind recompute (11 November 2026)

- **Input:** `recompute/nb2_worlds.csv` (80 worlds), `nb2_g.csv` and `nb2_garden.csv` (25 garden worlds with results),
  built by `recompute/build_nb2_counts.py`. The builder and `recompute/prompt.txt` were committed before the data
  existed. The CSVs were attached as files.
- **Who** (each a fresh chat; neither saw the analysis script or any earlier result):
  - GPT (Thinking, medium), chat `6af3d6a2`: Python, 10,000 draws;
  - Gemini 3.6 Flash (High), chat `5a4c4d96571f61e8`. A first Gemini chat (`a415d9d5d4d9eb14`) broke off midway, said
    its code tool was unavailable and returned a script instead. It is not counted, though its extinction counts and
    population ratios matched.
- **Recorded only from their actual replies.**

| quantity | analyse_nb2.py | GPT | Gemini |
|---|---|---|---|
| extinct c / s / o / l / n | 4 / 9 / 15 / 11 / 13 | 4 / 9 / 15 / 11 / 13 | 4 / 9 / 15 / 11 / 13 |
| population s / o / l / n against c | 0.2705 [0.1290, 0.4498] / 0.0458 / 0.2177 / 0.1769 [0.0515, 0.3406] | the same, to the digit | 0.2705 / 0.0458 / 0.2177 / 0.1769 [0.0991, 0.2641] |
| survival c / s / o / l / n | 0.8696 / 0.8110 / 0.7707 / 0.8148 / 0.7926 | the same | the same |
| n − s (primary) | −0.0184 [−0.0581, +0.0077] | −0.0184 [−0.0581, 0.0077] | −0.0184 [−0.0384, 0.0019] |
| o − s, l − o, n − l | −0.0403, +0.0441, −0.0222 | the same, with the same intervals | the same points |
| s − c, n − c | −0.0586 [−0.1165, +0.0090], −0.0770 [−0.1174, −0.0352] | the same | the same points; narrower intervals |
| g18Z − g1Z | no known births in any garden world with g = 0 | undefined (0/0 in every source) | 0.0000 (it read 0/0 as 0) |
| g18L − g18N | +0.0327 [−0.0490, +0.0754] (3 sources) | +0.0327 (per source +0.0716, +0.0754, −0.0490) | +0.0327 [−0.0490, 0.0754] |
| reading | not viable | not viable | not viable |

- **GPT** matches every point value and interval, and the reading.
  - It noted that arm o has only one surviving world, so in 1,182 of its 10,000 draws o had no births. o's interval
    uses the 8,818 draws where it is defined.
  - It reported o's g from year 300 on as one world's value, "not evidence of precise estimation".
- **Gemini** matches every point value that decides the reading, and the reading.
  - Its intervals are narrower than the analysis's and GPT's (for example n − s [−0.0384, 0.0019]). Its means of g
    differ at some years (for example s at year 600: 1.32 against 1.23). This points to a different resampling or
    averaging in its code. Neither changes the reading, which rests on the extinction counts and the population
    ratio's upper bound (0.26 or 0.34, both far below 0.80).
  - It read the gardens' 0/0 as 0; GPT, rightly, as undefined.

**All three agree: not viable. NB2 is final.**
