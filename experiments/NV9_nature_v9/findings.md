# NV9 — Nature version 9: the curiosity pull (adopted by the creator)

**Decision:** the creator, 29 October 2026: **"yes make it v9"**, after CU1 and LC1. Both models consulted (debate round
29, `docs/debate_after_ic2_lr1_2026-10-28.md`): GPT yes, 95% (conditional on the build checks and LC1's blind
recompute, both done); Gemini yes, 98%.

## What changed (one law; `v8_to_v9.diff`)
**A pull towards what has rarely been tried.** Each person remembers how often they have learned from each action in
each situation (`tried`, counted at their own learning step). When the mind weighs an option, an action rarely tried in
the current situation gets the play instinct's own curiosity pull, **0.3 × curiosity × (1 − hunger) ÷ (1 + times tried
there)**. The same for every action; only options already offered get it; the strength is borrowed from the play
instinct and was never adjusted after any result. `tried` is saved with a person only when held.

`code_v9` = CU1's `code_cu1` with `curiosity_pull` on by default. The live package (`acl/`) now runs v9. v8 is kept in
`experiments/NV8_nature_v8/code_v8`, so the change can be undone.

## The evidence
- **CU1** (final; recomputed blind by GPT and Gemini): supported by its frozen rule. The spread of real practice +0.018
  [+0.016, +0.021] (sham −0.004); making × 1.57; world-born adults' crafting skill × 1.18; no flags (population × 1.025).
- **LC1** (final; recomputed blind by GPT and Gemini), 1,000 years: "curiosity holds skill higher" (years 800–999,
  +0.033 [+0.023, +0.043]); making × 2; extinct 7 against 12 of 32; population higher. **Limit (recorded at GPT's
  request): curiosity does not stop the erosion.** Skill falls by the same absolute amount from century 2 to century 10
  (−0.185 against −0.184); curiosity raises the floor, it does not make knowledge build up.

## Checks (all pass; `zero.txt`)
- `code_v9` with `curiosity_pull` 0 equals `code_v8` (seed 11 and 501 at 5 years; 501 and 601 at 20 years).
- v9 equals CU1's arm c (seeds 501 and 601, 20 years).
- The live package with its own defaults equals v9 (seeds 501 and 601, 20 years).
- The setting acts (v9 differs from v8).
- Reload is exact with `tried` held (seed 501, saved at year 10, continued to year 15).
- State hashes include the random-number state (GPT's point on exact equivalence).
- Reference hashes: the live package regenerated (= v9); a v9 set added; v8 and earlier kept. **64 tests pass.**

Tag: `nature-v9`.
