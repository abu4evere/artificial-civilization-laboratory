# PL1 — How much do ACL's children play, against forager children? Findings (final: recomputed blind by GPT and Gemini; see the end)

Frozen as `PL1-frozen` (operational note 1); decided and signed off in sleep mode (`docs/autonomous_decisions.md`).
Read-only on nature v8. Run on GitHub Actions (run 40818054966, `skip_zero=local`). 32 worlds (seeds 20101–20132; LP,
80 founders, 80×80), 200 years. Every number comes from `analyse_pl1.py`, written before data; full tables are in
`results.md`.

**Validity:** zero checks pass; all 32 worlds present under one fingerprint (`code_v8`); wrapper counts match the law
(play carried out = play chosen; mismatches 0).

**Population beside it:** 2 of 32 worlds died out; mean living population 107.3.

## The answer

**ACL's young children play less than forager children, and not for lack of things to play with: they choose other
things.** Play is where nearly all of a child's crafting skill comes from.

| ages | play share of weeks [95%] | play available | chosen when available |
|---|---|---|---|
| 1–2 | 0.0000 | 0.000 | – |
| **3–6** | **0.0684 [0.0655, 0.0716]** | 0.942 | 0.0725 |
| 7–12 | 0.0121 [0.0110, 0.0134] | 0.999 | 0.0121 |
| 13–18 | 0.0032 [0.0030, 0.0035] | 0.987 | 0.0033 |

**The frozen readings:**
- **Ages 3–6 against the human range** (9–58%; Lew-Levy et al. 2022, 12 forager societies): 0.068, upper bound 0.072:
  **below the human range.** (Approximate: one action per week in ACL against shares of daytime observations; a warning,
  not proof.)
- **Decline with age: yes** (0.068 → 0.012 → 0.003), as in forager children.
- **The bottleneck at ages 3–6: choice.** Of weeks without play, 0.938 had play available and something else was chosen;
  only 0.062 had nothing to play with.
- Children who lived through each band play the same (0.068, 0.012, 0.003): deaths do not distort the trend.

**Where children's crafting skill comes from:** ages 3–6, all of it from play (1.000); ages 7–12, 0.977; ages 13–18,
0.680 (the rest from making). Children aged 1–2 never have play available (they hold nothing).

## Against the prior (the assistant's, frozen)
1. "Below the human range": **right.**
2. "The bottleneck is choice": **right.**
3. "Play declines with age": **right.**
4. "Most of children's crafting skill comes from play": **right.**

**A correction to what the creator was told:** before the run, the assistant reported a smoke-world hint (about 12%, inside
the range). The smoke world was 20 years from founding, not data; the real 200-year worlds give 6.8%, below the range.

## What follows
- **The play instinct, at its current strength, makes young children play less than the evidence suggests,** while play
  is the main way children gain crafting skill. Practice starvation starts in childhood.
- **For CU1 (the curiosity law, frozen before PL1's data was read):** CU1 borrows the play instinct's strength
  (0.3 × curiosity × (1 − hunger)). PL1 suggests that strength is, if anything, on the weak side for children. As GPT
  required, CU1's strength is **not** adjusted after seeing PL1. Whether a stronger, evidence-anchored play or curiosity
  drive is justified is a later question for the creator.

## Independent recompute
Pending: GPT and Gemini, fresh chats, raw per-world counts (ages 3–6). Recorded only from their actual replies.

## Independent recompute (29 October 2026)
GPT and Gemini, each in a fresh chat, worked from raw per-world counts only, without the analysis script
(`recompute_pl1.md`). **All three agree:** ages 3–6 play 0.0684 [0.0655, 0.0716] (below the human range); declining with
age; bottleneck choice (0.0619 unavailable).

**Final.**
