# HC1 — Habit copying in talk: whole table or only the situation at hand? (frozen plan)

**A nature-change study: one law, frozen, with a matched control and a sham.** Chosen in sleep mode
(`docs/autonomous_decisions.md`, 27 October 2026). Both GPT (70%) and Gemini (90%) chose it after CL1 (debate round 13,
`docs/debate_after_cl1_2026-10-27.md`).

Proposed in the debate as "CC1". That name was already taken (`CC1_cumulative_proof`), so it is **HC1**.

**Adoption is not decided here.** As with MO1, any adoption is left to the creator. GPT also said the thresholds below
are "proposed practical margins" whose relevance the creator should accept. The assistant signs them off under sleep-mode
autonomy and flags them for the creator's review.

## The evidence (CL1 and VC1, final)
- In years 100–200 the common actions' habit values over-value what actually follows by +0.418.
- That over-valuation splits exactly:
  - own experience −0.069;
  - **copying in talk +0.391 (0.93);**
  - carers +0.089.
- Copied values are never checked against the learner's own returns.

## The law tested (`code_hc1` = `code_v7` + one setting, `talk_copy`, default `"whole"` = v7 exactly)

**`talk_copy = "situation"`:** when a learner copies a model in talk (`actions._imitate`), only the 19 habit values of
the **model's current situation** move towards the model's. Everything else is unchanged:
- the same conditions (respect ≥ 0.2, or the model seeming happier by 0.1);
- the same rate, 0.05 × (0.5 + curiosity) × (0.5 + respect).

The law is TC1's arm S, on v7. It is a condition on what can be seen, not a change of strength: people learn what
others do in the situation they are in, not values for the 31 situations not at hand.

## Arms (32 paired seeds, 19201–19232; LP: 80 founders, 80×80; 200 years; run on GitHub)

| arm | setting |
|---|---|
| **w** | v7 (`talk_copy` "whole") |
| **s** | `talk_copy` "situation" |
| **x** | sham: v7 with `sham_draw` 1. It is the yardstick for how far worlds drift from any small change |

## Logged (read-only observer, as VC1: a wrapper on `biology._learn` that replays each update exactly and follows the realised return)

- **For every adult TD update:** q before; the realised discounted return G (VC1's definition); by action and era.
- **A yearly census:** living population, and extinction.

## Questions and the frozen decision rule (GPT's proposed rule, adopted)

- **P (primary: calibration).** The common actions' (forage, give, talk, gather) bias q − G in years 100–200, w against
  s. Paired by seed; world bootstrap, 10,000 replicates. **Supports** if the improvement (bias_w − bias_s) is at least
  0.10 **and** its 95% interval's lower bound is above 0.
- **H (no harm: realised return).** The mean realised return G over all adult updates, years 100–200, s against w.
  **No harm** if the lower 95% bound of (s − w) is above −0.05.
- **F (flags, reported, not gates).** Survival: extinctions in s against w, and the mean population in years 100–200,
  s ÷ w. Flagged if s has 3 or more extinct worlds beyond w, or population below 0.90 × w. A flag blocks any
  recommendation to adopt. It does not change "supported" (GPT: "don't claim equivalence from nonsignificance").
- **D (described, GPT's addition).** Make's calibration bias in s against w, and per-action biases. Also:
  - whether the s bias lies inside ±0.10 (reported; not a gate, so as not to repeat MO1's over-demanding threshold);
  - making per adult-year;
  - the sham's differences from w beside every measure.

**The change is supported** if P supports and H shows no harm. Then GPT and Gemini recompute blind and are consulted. **Adoption is
left to the creator.** Making and culture are not criteria.

## What would follow (stated now)
- **Supported, no flags:** a candidate for v8 (the copying law), for the creator's decision, on calibration grounds.
- **P fails:** restricting what is copied does not correct the over-valuation. Copied values arrive through the
  situations people are actually in, or carers take over. Described.
- **Harm (H) or flags:** the restriction costs people real returns or survival. Not recommended.

## The assistant's prior
1. P supports: the bias falls from about +0.42 to under +0.20 (improvement ≥ 0.2).
2. H: no harm. G changes by less than 0.02.
3. No flags.
4. Make's bias changes little (its copied part was only +0.03).

## Validity (hard stops)
- **Zero checks:**
  - `code_hc1` with "whole" equals `code_v7` (state and random numbers, 20 and 60 years);
  - the observer is read-only in arm s;
  - the setting acts;
  - the sham acts;
  - reload is exact in arm s.
- The TD replay is exact in every arm (mismatch 0).
- All 96 worlds are present under one fingerprint.
- An independent recompute by GPT and Gemini (fresh chats, raw files, no analysis script) of P and H before the findings
  are final. A recompute is recorded only from numbers read from the reply.

## Sign-off (27 October 2026)
The assistant, under the creator's sleep-mode autonomy (CLAUDE.md, Sleep mode). Both models support it (GPT 70%, Gemini
90%); the assistant's estimate is 70%, above the 40% threshold. The decision rule is GPT's, chosen over Gemini's stricter
one (a 60% reduction) to avoid MO1's threshold mistake. Logged in `docs/autonomous_decisions.md`. Frozen as `HC1-frozen`
before any code or data.
