# WP1 — Want propagation: findings (final: recomputed blind by GPT and Gemini; see the end)

**A nature-change test in a copy (`code_wp1` = `code_v11` + `want_propagation`). Live nature stays v11.**
- **Frozen** as `WP1-frozen`. Signed off by the assistant under sleep-mode autonomy (GPT 95%, Gemini 94%, the
  assistant 60%; debate round 49).
- **The creator** wrote on Telegram at 10:05: "Yes go ahead".
- **Its origin:** UP1 found that new inventions die at "cannot make". An exploratory check found the missing part
  usually cannot be made either, and nothing pulls a person to gather the part's inputs.

**The run:**
- GitHub Actions run 41476346903; the zero checks ran locally (`zero_local.log`).
- 128 worlds: v11 / A1 / A2 / sham × 32 paired seeds (22201–22232). LP, 200 years.
- Every number comes from `analyse_wp1.py`, written before data. Full tables are in `results.md`.

**Validity:**
- **The zero checks pass:**
  - with setting 0 the copy equals v11, at 20 and 60 years;
  - A1, A2 and the sham each act, and A1 and A2 differ;
  - the observer is read-only;
  - a saved and reloaded A2 world continues exactly.
- **All 128 worlds** are present under one `code_wp1` fingerprint.

## The answer
**Inconclusive for both A1 and A2. Want propagation does not let late inventions be made again. No guard was
raised.**

| arm | R: kinds invented in years 100–195 made again within 5 years | kinds | remade |
|---|---|---|---|
| v11 | 0.0000 | 3,575 | 0 |
| A1 (one level) | 0.0003 | 3,564 | 1 |
| A2 (the whole chain) | 0.0000 | 3,760 | 0 |
| sham | 0.0003 | 3,621 | 1 |

| contrast | difference [95%] |
|---|---|
| A1 − v11 | +0.0003 [+0.0000, +0.0009] |
| A2 − v11 | +0.0000 [+0.0000, +0.0000] |
| A2 − A1 | −0.0003 [−0.0009, +0.0000] |
| sham − v11 | +0.0003 [+0.0000, +0.0009] |
| A1 − sham | +0.0000 [−0.0009, +0.0008] |
| A2 − sham | −0.0003 [−0.0009, +0.0000] |

- **The rule needed** a gain of at least 0.01 over both v11 and the sham. The largest gain was 0.0003: one remade kind
  in about 3,600.
- **Guards (none raised):**

  | arm | population ÷ v11 | extinctions beyond v11's |
  |---|---|---|
  | A1 | 1.068 [0.971, 1.184] | 0 |
  | A2 | 1.120 [0.995, 1.261] | 0 |

### Secondary (described, not decisive)
| arm | gathers per adult-year | makes per adult-year | nested makes per adult-year | recipes per adult | kinds per 100 adult-years |
|---|---|---|---|---|---|
| v11 | 12.78 | 0.064 | 0.0026 | 10.1 | 1.12 |
| A1 | 11.91 | 0.063 | 0.0025 | 10.2 | 1.05 |
| A2 | 12.41 | 0.060 | 0.0028 | 9.9 | 1.06 |
| sham | 12.51 | 0.068 | 0.0028 | 10.2 | 1.06 |

Making, and the making of nested things, hardly change. The two remakes (A1 and the sham, one each) were by the
inventor, after about 64 weeks.

## Against the prior (the assistant's, frozen)
1. **"A1 inconclusive": right.**
2. **"A2 positive": wrong.** A2 changed nothing measurable in remaking.
3. **"No guard raised": right.**

## What it means
- **Missing "wanting" is not the block.** Even when value flows from the whole down to every part and material, people
  do not rebuild their late inventions.
- **The chain fails somewhere else.** From UP1 and its exploratory follow-ups, the remaining candidates are:
  1. **parts are used up and only 3 made things can be carried,** so a person seldom holds all the parts at once;
  2. **there is no goal held across weeks:** each week's choice is fresh, and the make choice offers only one recipe
     that can be made **now**, usually an old proven kind (UP1: every step-4 winner was an old kind);
  3. **deep chains:** each extra level multiplies the chances of a missing input.
- **What this rules out is useful.** The cheapest general repair, propagating value, is now tested and shown not to be
  enough. The candidates left are larger changes: a goal kept across weeks, or more carrying room. **Those are for the
  creator to choose.** Each would be a frozen test in a copy first.

## Blind recompute (`recompute_wp1.md`)
GPT (chat `6ae8d65a`) and Gemini 3.1 Pro (chat `8a14af5997ab7e3f`; Flash had returned an error) recomputed WP1 from the
per-world counts, blind, with the prompt written before the data. **Both match every point value, reading and guard.**
**WP1 is final.**

## Addendum (2 November 2026, about 20:30): where new kinds stop under A2 (exploratory; outside the frozen plan)
`explore/funnel_under_a2.py` (`explore/funnel_under_a2.json`) runs one A2 world of the copy (seed 22201) to year 130 with
UP1's make-choice funnel. The observer's reproduction of the make choice matched the copy's at every decision
(mismatches 0). **One world, 23 new kinds from years 100–125, described only:**

| step | new kinds under A2 (6,766 cases) | new kinds under v11 (UP1, 32 worlds) |
|---|---|---|
| value floor | 24.2% | 13.2% |
| **cannot make** | **75.9%** | **86.7%** |
| any later step (4, 5, made) | 0 | 0.05% |

- **Even when value flows down the whole chain, new kinds stop at "cannot make".** No case reached the make option.
- **So the missing piece is not wanting.** The inputs do not come together in the hand.
- **The candidates left are logistic:**
  - parts are used up, and only 3 made things can be carried;
  - each extra level needs its own inputs;
  - there is no persistence: nothing keeps the parts gathered for the goal.

  A goal kept across weeks would add persistence. The carrying limit would still stand.

**A lead for the creator's decision, not a finding.**
