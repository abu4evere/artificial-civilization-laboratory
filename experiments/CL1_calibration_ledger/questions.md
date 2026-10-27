# CL1 — Which route carries the miscalibration? The calibration ledger (frozen plan)

**Read-only on nature v7. No change to nature.** Chosen in sleep mode (`docs/autonomous_decisions.md`, 27 October 2026),
after VC1. Both GPT (80%) and Gemini (95%) chose it first (debate round 12, `docs/debate_after_vc1_2026-10-27.md`).

**VC1 (final), years 100–200:**
- habit values over-value the common actions (q − G = +0.418) and under-value making (−0.558);
- the max look-ahead's optimism is only 0.35 of the over-valuation.

**HL1 (final):** every habit value is an exact sum of components by the route it arrived through:

q = C_TD + C_talk + C_carer + C_birth + C_paid.

This study joins the two.

## The exact split (written before data)

At every adult TD update, with q read before the update and G the realised discounted return that follows (VC1's
definition):

**q − G = (C_TD − G) + C_talk + C_carer + C_birth + C_paid**

- **C_TD − G:** own experience's value minus what actually followed;
- **the social and inherited parts:** what arrived from others.

It is exact accounting of how the value arrived, **not causal attribution** (GPT's caveat). Copied values also feed
later TD targets through the look-ahead, so removing a route's component does not say what would happen without that
route.

Beside C_TD − G, the max gap (VC1) is reported.

## Questions (primary: adults, years 100–200; population beside every measure; world bootstrap, 10,000 replicates)

**Q1 (primary).** For the common actions pooled (forage, give, talk, gather): the mean of each term of the split.
**Named: the term carrying the largest share of the over-valuation (+q − G).**

**Q2.** For make: the same split. Is making's under-valuation carried by a small own-experience value (C_TD far below
G: practice starvation) with social parts near 0?

**Q3.** By era (0–50, 50–100, 100–200) and per action (make, forage, give, talk, gather): every term, and the max gap.

## What would follow (stated now; not exclusive)
- **Copying in talk carries the largest share:** a copying-rule study (F) is the targeted next nature-change
  candidate, on calibration grounds.
- **Own TD carries it** (C_TD above G): the learning rule. The max gap shows how much an Expected-SARSA change (C)
  could address.
- **Carers or birth carry it:** inherited values. A developmental question.
- **Make's under-valuation is C_TD far below G with tiny social parts:** practice starvation confirmed at the level of
  calibration. Exploration (E) is the next read-only question.

## The assistant's prior
1. For the common actions, copying in talk carries the largest share of the over-valuation, above own TD.
2. C_TD − G for the common actions is positive but smaller than C_talk.
3. For make, C_TD is far below G (−0.5 or less) and every social part is under 0.05.

**GPT's prediction (on record):** "copying amplifies common-action overvaluation while sparse experience sustains
making's underestimation".

## Validity (hard stops)
- **Zero checks:**
  - the observer and wrappers are read-only: state and random numbers identical with and without them, at 20 and 60
    years;
  - reload is exact.
- **The TD replay is exact,** and at every update the ledger's components add up to q (mismatch counters that must be
  0). So does HL1's decade closure.
- All 32 worlds are present under one fingerprint (`code_v7`).
- **An independent recompute by GPT and Gemini** (fresh chats, raw files, no analysis script) of Q1's split and the
  largest term, and make's split, before the findings are final. A recompute is recorded only from numbers read from
  the reply.

## Setting
Nature v7, LP (80 founders, 80×80), 32 new seeds (19101–19132), 200 years, run on GitHub.

## Sign-off (27 October 2026)
The assistant, under the creator's sleep-mode autonomy (CLAUDE.md, Sleep mode). Both models chose this study (GPT 80%,
Gemini 95%); the assistant's estimate is 80%, above the 40% threshold. Logged in `docs/autonomous_decisions.md`. Frozen
as `CL1-frozen` before any code or data. How the code reads choices the text leaves open goes in operational notes,
appended before any data.
