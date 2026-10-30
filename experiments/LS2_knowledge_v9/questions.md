# LS2 — Where does knowledge go under nature v9? (frozen plan)

**Read-only on nature v9. No change to nature.** The creator: "yea draft it and run on github" (29 October 2026), after
debate round 30 (`docs/debate_after_ic2_lr1_2026-10-28.md`): both models chose this audit first (GPT 90%, Gemini 95%),
before any apprenticeship law.

**Why.** LS1 (final, v7) traced where knowledge goes over 1,000 years: copies and kinds are lost with the dead (0.98),
inflow by invention falls to near 0, and making collapses at the choice. Nature v9 (the curiosity pull) changed
practice: LC1 shows more skill, making and people over 1,000 years, but the same absolute fall in skill. **Is the leak
still the same under v9, and where does it sit now?** The answer shapes the next law (GPT: watching someone make a thing
could teach a technique, a recipe, or both; the ledger should say which matters).

## Design: LS1's frozen design, unchanged, on v9
- **The observer, ledger, questions (Q1–Q5), decompositions, survivorship rules, validity checks and "what would follow"
  are LS1's** (`../LS1_where_knowledge_goes/questions.md`), applied to `code_v9` (the live nature) by a thin runner
  (`run_ls2.py`) that reuses LS1's code unchanged, and an analysis that is LS1's (`analyse_ls2.py`).
- **LP only:** 80 founders on 80 × 80, 1,000 years, **40 new seeds (20401–20440)**. LS1's secondary D80 arm is dropped
  so that each cloud chunk stays within GitHub's job limit (LC1's longest chunk reached it).
- **Comparison with LS1 (v7)** is described, not tested: different seeds, the same design.

## The questions (LS1's, read on v9)
1. **Q1:** the dominant copy-loss channel and kind-extinction channel after year 100; when net flow turns negative.
2. **Q2:** transmission and persistence of useful kinds, founder against world-born, by era.
3. **Q3:** the making funnel (feasible, weighed, chosen) and the decline decomposition from years 0–10 to 100–200.
4. **Q4:** the fall in food owed to tools, split exactly.
5. **Q5:** per birth cohort, the inheritance rate, use, onward passing and survival of what each generation acquires.
**Added (GPT, debate round 30), described:** knowing a recipe kept apart from the practical skill to use it: LS1's Q3
and Q5 already report making by those who know (use) and crafting skill at 16 and 30; both are read side by side by
cohort.

## The assistant's prior
1. Death is still the dominant channel of copy loss and kind extinction after year 100.
2. Making's decline is still carried mostly by the choice gate, but less than on v7 (curiosity raises "chosen").
3. The inheritance rate is low and falls over cohorts, as on v7.

## Validity (hard stops)
LS1's: the observer is read-only (state and random numbers identical with and without it, at 20 and 100 years); reload
exact; the ledger balances exactly in every world (holdings, kind counts, living people's recipes; mismatches 0); all
40 worlds present under one fingerprint (`code_v9`); an independent recompute by GPT and Gemini of Q1's dominant
channels, Q3's decomposition and Q5's inheritance rate before the findings are final.

## Sign-off (29 October 2026)
**The creator: "yea draft it and run on github".** Frozen as `LS2-frozen` before any code or data.
