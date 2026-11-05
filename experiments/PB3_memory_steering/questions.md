# PB3: Memory steering as a candidate law — prediction or myopia? (frozen plan; the brain road, step 4)

**A nature-change test in a copy:**
- `code_pb3` = `code_pb2` + one setting, `brain_lookahead`. With `brain` 0 it is v13 exactly; with `brain_lookahead`
  0 it is `code_pb2` exactly.
- Nothing goes live except by the safe path: a final supported study, recomputes, a confirmatory run on new seeds,
  council, zero checks, tests.

**Why:**
- PB2 (final, recomputed blind) found that when each adult's own memory guides choices in the habit table's place
  (arm P), M3 rises from 0.0034 to 0.0210 (P − v13 +0.0176 [0.0157, 0.0194]) and living-weeks rise by 28%, with no
  extinction.
- But this was PB2's reported steering effect, not its frozen primary, and it carries a confound stated before data:
  - the habit value q looks one week ahead (`discount` 0.8 on next week's best habit);
  - the memory's estimate r̂ does not.

  So P − v13 mixes "a better predictor" with "no look-ahead".
- Council round 62 (`docs/debate_round62_after_pb2_2026-11-05.md`): all three models put this test first. GPT 94%,
  Gemini 95%, DeepSeek about 80%.

**What it asks:**
1. Does memory steering raise ends-directed chains **beyond what removing the look-ahead alone does**?
2. Does PB2's total effect replicate on new seeds?

## The brain (as in PB2; general abilities only)
- From year 100, each adult keeps PB2's memory (empty at the start):
  - own weeks with the week's learning signal r = reward + 2 × mood change;
  - the visible weeks of others, without r;
  - memories end with their owner.
- **P** (`brain` 1): in `mind.decide`, the habit term `learned_weight × q` becomes `learned_weight × r̂ₛ`. r̂ is the
  mean r of the exact lived (situation, action) cell, else of the 8 most similar own weeks with that action. r̂ₛ is
  r̂ put on q's running scale. Where there is no r̂, q is used.
- **P+** (`brain` 1, `brain_lookahead` 1): as P, but each own week's value is its **two-week return**,
  r(t) + discount × r(t+1).
  - r(t+1) is the r of the person's next own week, entered when that week is lived; `discount` is v13's 0.8.
  - A week whose next own week is not yet lived is not used for r̂ until it is.
  - This is a look-ahead through memory of the same horizon as q's.

## Arms (32 new paired seeds **23301–23332**; LP: 80 founders, 80 × 80; 170 years)
| arm | settings | |
|---|---|---|
| **c** | v13 | the habit table with its one-week look-ahead |
| **c0** | v13 with `discount` 0 | the habit table without look-ahead (an existing setting) |
| **P** | `brain` 1 (from year 100) | memory steering, no look-ahead |
| **P+** | `brain` 1, `brain_lookahead` 1 | memory steering with a one-week look-ahead through memory |
| **sham** | v13 with `sham_draw` 1 | |

The arms form a 2 × 2: {habit, memory} × {look-ahead, none}, plus the sham.

## Measures (adults 16–49, years 130–170; population beside every measure)
M3 as in AM1 and PB2: P(made a recipe using material m within 8 weeks | gathered m, a needed input of a valued
recipe, holding < 1) − P(made | an opportunity-matched week). Pooled sums per world; a paired world bootstrap with
10,000 replicates and NumPy seed 20261115.

1. **Guards first** (c0, P, P+ each against c). A guard is raised by:
   - a living-weeks ratio below 0.90 with its upper bound below 1;
   - or 3+ extra extinct worlds.

   A guard raised means "harm: investigate", and the arm is not read as a success.
2. **Primary — attribution: P − c0 on M3.**
   - **"Better prediction"** if its 95% interval lies wholly above 0 **and** its point is at least **+0.005**.
   - **"Myopia, not prediction"** if the interval does not lie wholly above 0 while c0 − c lies wholly above 0.
     Removing the look-ahead then explains the effect. This is a real finding, pre-registered as one.
   - Otherwise: **"unclear"**.
3. **Co-primary — replication: P − c on M3** (95% interval wholly above 0) **and P / c living-weeks** (95% interval
   wholly above 1). **"PB2's steering effect replicates"** if both hold.
4. **Described:**
   - c0 − c (the look-ahead's own effect);
   - P+ − P and P+ − c0 on M3 and living-weeks;
   - Gemini's stricter check, whether P − c0 ≥ +0.015;
   - R (lineage remaking, as in PB2);
   - inventors' weeks holding their kind's inputs, and the share in which they still knew the recipe;
   - makes per adult-year, world-new kinds, action shares, food per adult, M2, M5;
   - fallbacks to q;
   - people born after year 100 apart from the others.

## What follows from the readings (decided before data)
- **"Better prediction" + "replicates" + no guard:** memory steering becomes a candidate law. Adoption still needs a
  **confirmatory run on new seeds** (P against c and c0), blind recomputes, council and the rest of the safe path. PB3
  alone never changes live nature.
- **"Myopia, not prediction":** the habit table's one-week look-ahead, not the memory, holds chains back. The next
  question becomes the look-ahead rule itself: a fault, or a law to test.
- **Either way:** the next step for R is the recipe-memory rule. A new recipe enters at value 0 and can be evicted at
  once (`acl/knowhow.py` lines 78–82; round 62). It gets its own frozen check.

## Validity (hard stops)
- **Zero checks:**
  - `code_pb3` with `brain` 0 = `code_v13` (20 and 60 years);
  - `code_pb3` with `brain` 1 and `brain_lookahead` 0 = `code_pb2`'s P (the same world, the same memories);
  - c0, P, P+ and the sham act;
  - reload is exact in P+, with memories and two-week returns saved;
  - **unit check:** in P+, every used two-week return equals r(t) + 0.8 × r(t+1) from the person's next own week, and
    no week waiting for its next week is used.
- **All 5 × 32 worlds** are present under one `code_pb3` fingerprint.
- **A timed smoke run** before the cloud.
- **A blind recompute** by GPT and Gemini (DeepSeek too) of the primary, the co-primary and the guards.

## Known limits (stated before data)
- P+'s look-ahead is **on-policy**: the next week actually lived. q's is a **max** over next week's habits. P+ is a
  look-ahead of the same horizon, not the same rule.
- c0 changes the habit table everywhere, including in the fallback, so c0 − c is the look-ahead's effect on the habit
  system as a whole.

## The assistant's prior
1. **c0 − c > 0:** removing the look-ahead alone raises chains somewhat.
2. **P − c0 > 0 but smaller than P − c.** "Better prediction" passes: about 55%.
3. **PB2's effect replicates** (P − c and living-weeks): about 85%.
4. **P+ ≤ P on M3:** a look-ahead partly brings back the habit trap.
5. **R stays near 0** in every arm.
6. **No guard is raised.**

## Sign-off (5 November 2026)
The assistant, under:
- the creator's direction (the brain first);
- the 2 November permission to edit world rules (tests in a copy);
- sleep-mode autonomy.

Council round 62: GPT 94%, Gemini 95%, DeepSeek about 80%; the assistant 70% that the study is valid and
informative. Frozen as `PB3-frozen` before any code or data.
