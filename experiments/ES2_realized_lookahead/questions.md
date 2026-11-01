# ES2 — Do minds learn more accurately when they look ahead by their real next choice? A nature-change test in a copy (frozen plan)

**A test in a copy (`code_es2` = `code_v11` + `realized_lookahead`; 0 = v11 exactly), not an adoption.** Live nature
stays v11. Adoption would follow only the safe path in `CLAUDE.md`.

## Why
- **ES1** (final, not supported): an expected look-ahead over the **habit part** of the choice made habits less
  accurate (mean |q − G| 0.392 → 0.423). Every action became under-valued, likely because it ignored the instinct
  terms of the real choice (recorded before data).
- **Yet** making rose fivefold, tools' share of food fourfold, and population a fifth, with no harm.
- **Debate round 39** (`docs/debate_round39_es2_2026-10-31.md`): both models chose an expected look-ahead over the
  **real** next choice (GPT 85%, Gemini 80% after revising), with absolute calibration the sole primary.

## The law (one setting, `realized_lookahead`; 0 = v11)
- **When 1,** last week's habit update is **held** at the end of the week (`_learn` stores the action's index and that
  week's reward r) and **applied at the person's next decision**, before they choose.
- **The look-ahead** is the expected habit value of that decision under its actual choice:
  - future = Σ_o π(o) · q(s′, action(o)), over the decision's options o, after every filter the choice uses;
  - π(o) is the choice's own softmax over the options' scores at the choice temperature (the same scores and
    temperature `softmax_pick` uses, computed without drawing a random number);
  - s′ is the situation of that decision.
- **Then** q ← clip(q + 0.05 × (r + 0.8 × future − q), −1.5, 1.5), as today. The choice itself is unchanged and uses
  the scores already computed.
- **A held update is dropped, not applied,** if the person dies before their next decision (counted).
- **Nothing else changes:** rewards, rates, discount, the choice, all other laws. It is general; no action is favoured.

## Arms (32 paired seeds 21501–21532; LP: 80 founders, 80×80; 200 years)
| arm | setting |
|---|---|
| **v11** | `realized_lookahead` 0 (= `code_v11`, shown by the zero checks) |
| **r** | `realized_lookahead` 1 |
| **x** | sham: v11 with `sham_draw` 1 |

## Measures (paired world bootstrap, 10,000 replicates)
- **Primary** (sole): **calibration error across all actions,** mean |q − G| (ES1's and VC1's method).
  - q is the value just before each update is applied (all ages; updates started in years 100–200).
  - G = Σ_k 0.8^k r over the person's next updates. It is closed when 0.8^k < 0.001, or at death (censored).
  - **Primary contrast: r − v11.**
- **Frozen secondary:**
  - **Ranking accuracy:** within each of the 32 situations, the Spearman correlation between actions' mean q and
    their mean realized G (actions with at least 100 closed updates in that situation and arm). It is averaged over
    situations, per world, then compared paired.
  - **The signed bias q − G** by action.
  - **Making per adult-year; foraged food per adult-year;** tools' share of foraged food.
- **Guards:**
  - **Calibration by action** (GPT): no action with at least 10,000 closed updates per arm may see its mean |q − G|
    rise by more than 0.10 against v11.
  - **Uncompleted updates** (GPT, Gemini): held updates dropped at death, below 1% of updates in every arm.
  - **Population:** r ÷ v11 < 0.90 with the upper bound < 1.
  - **Adult deaths:** up by more than 10% of v11's rate, with the lower bound > 0.
  - **Extinctions:** +3 or more.
- **Described** (Gemini): the instinct-dominance ratio, Var(score − 0.6 × q) ÷ Var(score) over the options of sampled
  decisions.

## Frozen decision rule
- **Supported:** r − v11 in mean |q − G| < 0 with its upper bound < 0, **and** more negative than the sham's own
  difference, **and** no guard flag.
- **Otherwise not supported.**
- **Making and ranking are reported, not decisive.**

## Validity (hard stops)
- **Zero checks:**
  - `code_es2` with the setting 0 = `code_v11` (state and random numbers, 20 and 60 years);
  - r acts;
  - the sham acts;
  - the observer is read-only in arm r;
  - reload is exact (a held update is saved with the person, and saved only when held);
  - every applied update replays exactly (mismatch 0).
- All 96 worlds are present under one fingerprint.
- **A blind recompute by GPT and Gemini** of the primary contrast, its interval and the sham's.

## The assistant's prior
1. **Supported:** the error falls (the expectation now includes the instinct terms that ES1 left out).
2. **Making rises,** but less than in ES1.
3. **No guard flag.**

## Sign-off (31 October 2026)
The assistant, under the creator's standing instruction to keep working (a nature-change test in a copy under the 40%
rule; adoption only by the safe path). GPT estimates 85%, Gemini 80% and the assistant 70%. Frozen as `ES2-frozen`
before any code or data.
