# UV2 — Does the habit floor come from unpractised choices further ahead? Findings (not final until GPT and Gemini recompute)

**Read-only: no change to nature.** Frozen as `UV2-frozen`. Signed off by the assistant (GPT 91%, Gemini 98%, the
assistant 75%; debate round 41). Run on GitHub Actions (run 41341318088, `skip_zero=local`). 32 worlds: ES2's r arm
replayed on its 32 seeds (21501–21532) with a wider observer. Every number comes from `analyse_uv2.py`, written before
data and tested on a smoke world. Full tables are in `results.md`.

**Validity:**
- zero checks pass;
- all 32 worlds are present under ES2's fingerprint;
- every update replays exactly, and every completed update had its exposure measure;
- **every world matches ES2's r file exactly** (hash, n and Σ|q − G|);
- every update is binned once, and no Dn falls outside [0, 1];
- **the primary pooled over all Dn equals UV1's B_high to 4 decimals.**

**Operational note 1:** one validity flag was a NumPy true/false that failed an `is True` test. It was fixed by a cast
before any outcome was computed or read (`questions.md`).

**Population beside it:** ES2's r worlds, unchanged. Mean living population, r ÷ v11, 1.160 [1.029, 1.289] (ES2).

## The answer
**Not propagation, by the frozen rule.** Practised habits (k ≥ 80, ages 16–44, not death-closed) are under-valued just
as much when the person's discounted future choices are almost all well practised:

| cell | B [95%] | n | worlds |
|---|---|---|---|
| **Dn < 0.1** | **−0.111 [−0.115, −0.106]** | 362,963 | 32 |
| all Dn | −0.108 [−0.111, −0.105] | 1,376,008 | 32 |

So unpractised choices further ahead do not explain the floor.

### Secondary (described, not decisive)
- **No dose-response.** B by Dn bin (k ≥ 80, ages 16–44):

  | Dn | 0–0.05 | 0.05–0.1 | 0.1–0.2 | 0.2–0.4 | 0.4–1 |
  |---|---|---|---|---|---|
  | B | −0.084 | −0.128 | −0.132 | −0.101 | −0.052 |

  Propagation predicts the bias shrinks as Dn falls. Instead the most-exposed bin is the *least* under-valued. The
  one-step U shows no trend either (−0.108, −0.122, −0.112, −0.090).
- **A clear trend over time.** B for k ≥ 80, ages 16–44, by quarter:

  | years | 100–124 | 125–149 | 150–174 | 175–199 |
  |---|---|---|---|---|
  | B | −0.146 [−0.149, −0.143] | −0.119 | −0.095 | −0.075 [−0.078, −0.071] |

  The floor roughly halves across the 100 years. The share of updates with Dn < 0.1 rises a little: 0.244 → 0.278.
- **Children:** almost all children's updates have Dn 0.4–1 (their future choices are mostly unpractised), at
  B −0.38 to −0.39 (ages 1–11).

## Against the prior (the assistant's, frozen)
1. "Mixed": **wrong** (not propagation).
2. "The dose-response falls toward 0 as Dn falls": **wrong.** It does not fall; the most exposed are the least biased.
3. "Year quarters show little trend": **wrong.** It is the clearest pattern in the study.

None of the three was right.

## What it means
- **Propagation through the look-ahead is not what keeps practised habits low.**
- **Time is the strongest clue.** The floor shrinks steadily from year 100 to year 200. Two readings fit, both
  untested:
  - **Circumstances improving:** under r, making triples and tools spread, so returns may rise over time and learned
    values lag behind them.
  - **A slow, generations-long convergence:** each generation starts at half its parents' values, and the parents'
    values themselves rise slowly, so the whole population climbs over centuries.

  These can be told apart: the first predicts the floor tracks how fast returns are rising; the second predicts it
  tracks how many generations have passed.
- **For Bob:** a lasting part of each mind's error is not in its own learning but in its starting point and its
  world. Minds inherit their parents' values halved and are pulled toward their carers'. If the world improves faster
  than values are passed on, every generation starts behind. **Cumulative culture needs the passing-on to keep up.**
- **No change to nature** follows from this study.

## Independent recompute
Pending: GPT and Gemini, each in a fresh chat, from `recompute/uv2_one_file.csv`. Recorded only from their actual
replies.
