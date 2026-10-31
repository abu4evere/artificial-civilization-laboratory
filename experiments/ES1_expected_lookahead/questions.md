# ES1 — Do minds learn more accurately with an expected look-ahead? A nature-change test in a copy (frozen plan)

**A test in a copy (`code_es1` = `code_v11` + `expected_lookahead`; 0 = v11 exactly), not an adoption.** Live nature
stays v11. Adoption would follow only the safe path in `CLAUDE.md` (a confirmatory run first).

## Why
- **ACL's habits** are one-step Q-learning (`biology._learn`): q ← q + 0.05 × (r + 0.8 × max_a′ q(next, a′) − q).
  - **The max look-ahead is known to over-estimate** (van Hasselt 2010; `docs/research/learning_rule_sources_2026-10-30.md`).
  - **HL1:** the max term grew from 0.06 to 1.26 while rewards stayed flat.
  - **VC1:** common actions were over-valued (+0.42), and making under-valued (−0.56).
  - **CO2:** habit inflation carries 0.87 of making's decline over the centuries.
- **Debate round 38** (`docs/debate_round38_learning_rule_2026-10-31.md`): both models chose this test (GPT 75%, Gemini
  88%), with the primary as calibration across **all** actions. "ACL should test whether its minds learn more
  accurately, not whether changing their minds makes them craft more" (GPT).

## The law (one setting, `expected_lookahead`; 0 = v11)
- **When 1,** the look-ahead in `_learn` is the **expected** value of the next situation under the person's own way of
  choosing, instead of the maximum:
  - future = Σ_a π(a) · q(next, a);
  - π(a) ∝ exp(learned_weight × q(next, a) ÷ choice_temperature), over all actions;
  - the same learned weight (0.6) and temperature (0.2) the choice already uses.
- **This is the habit part of the choice.** The instinct terms of a future choice are not known when learning, so they
  are not used. Nothing else changes: rewards, rates, discount, the choice itself, all other laws.
- **It is general.** Every action's value is learned the same way. No action is favoured.

## Arms (32 paired seeds 21401–21432; LP: 80 founders, 80×80; 200 years)
| arm | setting |
|---|---|
| **v11** | `expected_lookahead` 0 (= `code_v11`, shown by the zero checks) |
| **e** | `expected_lookahead` 1 |
| **x** | sham: v11 with `sham_draw` 1 |

## Measures (paired world bootstrap, 10,000 replicates)
- **Primary: calibration error across all actions,** years 100–200. VC1's method (`experiments/VC1_value_calibration/questions.md`):
  - at each habit update (all ages), the value q before the update against the realized return
    G = Σ_k 0.8^k r_{t+k} over the person's next updates;
  - G is closed when 0.8^k falls below 0.001 (31 updates) or at death (censored, and reported);
  - **the error is the mean |q − G|** over all updates.
  - **Primary contrast: e − v11** (negative = more accurate).
- **Secondary:**
  - the signed bias q − G by action (VC1's +0.42 for common actions, −0.56 for making);
  - making per adult-year;
  - foraged food per adult-year;
  - tools' share of foraged food (TR1's R).
- **Guards:**
  - population (mean living, years 100–200);
  - adult deaths per 1,000 adult-years;
  - extinctions.

## Frozen decision rule
- **Supported:** e − v11 in mean |q − G| < 0 with its upper bound < 0, **and** more negative than the sham's own
  difference, **and** no guard flag.
- **Guard flags:**
  - population e ÷ v11 < 0.90 with the upper bound < 1;
  - adult deaths per 1,000 adult-years e − v11 > 0 with the lower bound > 0, and above 10% of v11's rate;
  - extinctions +3 or more.
- **Making is reported, not decisive.** A supported rule with no change in making would say that accuracy alone does
  not bring making back.

## Validity (hard stops)
- **Zero checks:**
  - `code_es1` with the setting 0 = `code_v11` (state and random numbers, 20 and 60 years);
  - e acts;
  - the sham acts;
  - the observer is read-only in arm e;
  - reload is exact.
- **The observer replays every habit update** (the update formula under the arm's rule) and must match the stored q
  (mismatch 0).
- All 96 worlds are present under one fingerprint.
- **A blind recompute by GPT and Gemini** of the primary contrast, its interval and the sham's.

## The assistant's prior
1. **Supported:** the error falls, most for frequent actions.
2. **Making per adult-year rises** a little (under +20%).
3. **No guard flag.**

## Sign-off (31 October 2026)
The assistant, under the creator's standing instruction to keep working (a nature-change test in a copy, allowed as a
frozen study under the 40% rule; adoption only by the safe path). GPT estimates 75%, Gemini 88% and the assistant 70%.
Frozen as `ES1-frozen` before any code or data.
