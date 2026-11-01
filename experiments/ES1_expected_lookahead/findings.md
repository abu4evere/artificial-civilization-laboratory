# ES1 — Do minds learn more accurately with an expected look-ahead? Findings (final: recomputed blind by GPT and Gemini; see the end)

**A nature-change test in a copy (`code_es1` = `code_v11` + `expected_lookahead`), not an adoption.** Frozen as
`ES1-frozen` (operational note 1, which recorded a smoke observation before any data). Signed off by the assistant
(GPT 75%, Gemini 88%; debate round 38). Run on GitHub Actions (run 41256219936, `skip_zero=local`). 96 worlds: v11,
e (expected look-ahead) and a sham, on 32 paired seeds (21401–21432); LP (80 founders, 80 × 80), 200 years. Every number
comes from `analyse_es1.py`, written before data and tested on smoke worlds; full tables are in `results.md`.

**Validity:**
- zero checks pass;
- all 96 worlds are present under one fingerprint;
- every habit update replays exactly under its arm's own rule (mismatches 0; about 21–25 million updates closed per
  arm).

**Population beside it:** extinctions were v11 2, e 2, sham 2. Mean living population, e ÷ v11, was **1.205** [1.034,
1.392]; the sham's was 0.956.

## The answer

**Not supported by the frozen rule.** The expected look-ahead does **not** make habit values more accurate: their error
against what really happens grows slightly. **But it changes behaviour a great deal:** five times more making, four times
more food from tools, and larger populations, with no guard flag.

### Primary — calibration error across all actions (mean |q − G|, years 100–200)
| arm | mean abs(q − G) |
|---|---|
| v11 | 0.3919 |
| e | 0.4230 |
| sham | 0.3859 |

- **e − v11: +0.031** [+0.022, +0.040]. Worse, not better. The sham's difference is −0.006 [−0.015, +0.003].
- **The frozen decision: NOT SUPPORTED** (it needed e − v11 < 0, with its upper bound < 0).

### Secondary (described; making was declared "reported, not decisive" before the run)
- **The signed bias q − G flips sign for the common actions.** Under v11, foraging, gathering, giving and putting
  things down are over-valued (+0.30 to +0.41) and making is under-valued (−0.51). Under e, **every action is
  under-valued, at similar levels** (−0.36 to −0.67; making −0.52).
  - Operational note 1 had recorded this pattern in a smoke world **before any data**, with its likely reason: the
    expectation weighs only the habit part of a future choice, not its instinct terms.
- **Making per adult-year: 0.070 → 0.362,** ×5.2 [4.7, 5.5].
- **Tools' share of foraged food: 1.40% → 5.58%,** ×4.0 [3.7, 4.3].
- **Foraged food per adult-year:** ×1.024 [1.018, 1.031].
- **Guards: none raised.**
  - Population ×1.205 [1.034, 1.392].
  - Adult deaths +0.96 per 1,000 adult-years [−0.05, +1.89].
  - Extinctions +0.

## Against the prior (the assistant's, frozen)
1. "Supported: the error falls": **wrong** (it rises by 0.031).
2. "Making rises a little (under +20%)": **wrong in size** (×5.2).
3. "No guard flag": **right.**

## What it means (descriptive; nothing here overrides the frozen rule)
- **This form of the law makes minds less accurate, not more,** so by both models' own principle it is not adopted:
  "ACL should test whether its minds learn more accurately, not whether changing their minds makes them craft more"
  (GPT, round 38).
- **Yet it shows how strongly the max look-ahead holds making back.**
  - The max inflates the actions people do all the time, by about +0.4. Making, rarely done, stays low.
  - Remove that **uneven** inflation, even at the cost of a uniform under-valuation, and making rises fivefold.
  - Tools then reach a 5.6% share of food: about a quarter of TR1's 20% headroom.
  - **This is the strongest evidence yet that the choice gap is a learning-rule gap** (CO2's 0.87, now shown by
    intervention, not only by accounting).
- **What follows** (for debate with GPT and Gemini, and the creator's view; not decided here):
  - **(a) A second frozen test** of an expected look-ahead taken over the **whole** choice (instinct terms included,
    as operational note 1 suggested before data), closer to the monkey dopamine evidence (Morris et al. 2006;
    `docs/research/dopamine_max_or_expected_2026-10-31.md`). Primary: calibration again, with making secondary.
  - **(b) Whether "accuracy" should be absolute or relative** (do the rankings of actions match the rankings of their
    returns?). That would be a new question for a new frozen study, **never a change to this one's reading.**
- **No change to nature** follows from this study.

## Independent recompute (31 October 2026)
GPT and Gemini, each in a fresh chat, from per-seed sums of the raw output only (`recompute_es1.md`). **All three agree:**
M 0.3919 / 0.4230 / 0.3859; e − v11 +0.0311 [+0.0218, +0.0398]; sham −0.0060; not supported.

**Final: not supported. Not adopted.**
