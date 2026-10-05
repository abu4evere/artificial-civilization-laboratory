# E8.1 — Value autopsy · Results

Read-only replays of the E7 code, seeds 301–304, 120 years, adults sampled every 4th week. The probe changed
nothing (state hash, 20 years) and all four replays matched their saved runs. Predictions frozen in
E8_1_value_autopsy.md (tag `E8.1-frozen`) before the run. Data: `output_e81/`.

## By generation (pooled over seeds)

| generation | adult-weeks | things held per adult | mean worth of held things | held things worth ≤ 0 | best worth among known recipes | weeks a make was possible | "make" weighed | "make" chosen | chosen score ÷ make's largest pull (median of seeds) |
|---|---|---|---|---|---|---|---|---|---|
| 0 (founders) | 18,544 | 0.71 | 0.133 | 8% | 0.164 | 61% | 10.6% | 1.0% | 7.1–8.8 |
| 1 | 36,700 | 0.61 | 0.119 | 18% | 0.215 | 86% | 4.4% | 0.5% | 8.1–11.7 |
| 2 | 40,428 | 0.37 | 0.053 | 43% | 0.192 | 86% | 1.3% | 0.1% | 12.7–13.5 |
| 3+ | 58,487 | 0.19 | 0.056 | 48% | 0.175 | 87% | 0.6% | 0.1% | 12.8–15.8 |

What was chosen instead of making, generation 3+: forage 45%, talk 17%, join 14%, give 13%, gather 6%, put 2%.
Mean worth of held things by seed, generations 0 / 1 / 2 / 3+: 301: 0.128 / 0.109 / 0.065 / 0.038;
302: 0.100 / 0.115 / 0.044 / 0.062; 303: 0.137 / 0.085 / 0.047 / 0.056; 304: 0.184 / 0.173 / 0.060 / 0.112.

## Frozen predictions, scored

1. **wrong** — generation 3+ held worth below half the founders' in 2 of 4 seeds (301, 303), not in 302 or 304.
2. **confirmed** — 48% of generation 3+ held things are worth zero or less (founders 8%).
3. **confirmed** — "make" weighed in 0.6% of generation 3+ weeks when a make was possible.
4. **confirmed** — forage, talk, join and give: 89% of what was chosen instead.
5. **confirmed** — chosen action's score 12.8–15.8× the largest pull "make" could have had from worth alone.

Caveat on 5: the probe estimates hunger from food on hand, not with the mind's own formula, and counts only
the pull from worth (not puzzles, place beliefs or parts wanted), so the ratio is approximate.

## What this says

- **Making was never competitive.** Even founders weighed "make" in only 11% of the weeks they could have made
  something, and chose it in 1%. The pull of making is an order of magnitude below the pull of daily life,
  from the first generation on. The things people make are worth too little to them to compete with eating,
  company and care.
- **It then gets worse.** Later generations hold far fewer things (0.71 → 0.19 per adult), half of what they hold
  is worth nothing to them, and "make" is weighed 18 times less often. The best worth among recipes they know
  does not fall (about 0.17–0.22), so knowledge is not what is missing; reasons to act on it are.
- **Consequences for E8.** Apprenticeship, memory protection and larger populations all act after someone has
  chosen to make. On this evidence that choice almost never happens, so those arms would have little to work
  on. The open question moves to the economics of making: do the things people make actually help them enough
  to be worth making? That is the "innovations without leverage" suspect, now with numbers.
