# LW1: a learner's wish for the part they could not follow (frozen plan)

**A test of one law in a copy of nature v15, with a sham.** Council round 74 chose it
(`docs/debate_round74_after_pc1_2026-11-07.md`; GPT 96%, DeepSeek about 75%; Gemini 95% for a wider design). PC1 found
that new kinds fail in lessons because a made part is missing. Chains run 3 or more deep in 56% of failures. The
teacher knows the missing parts in 93%, and today's one-level part lesson never led to learning (0 of 4,359). The law
gives learners **a general ability: remembering the part they could not follow, and being shown it first next time.**
It names no thing and plans no chain, and it adds no lesson and no time.

## The law (LW, `learn_wish` = 1; 0 = v15)
1. **A wish forms on a visible failure.** A lesson fails because the learner cannot follow it (`can_follow` False, after
   the acceptance draw passed). This includes a part lesson, or a lesson shown because of a wish. The learner then
   holds a wish for **the first made part of that recipe, in the recipe's own order, that they do not know**. It is the
   immediate blocker: the learner knows which part they could not make, not the whole chain.
2. **One wish at a time,** the most recent: a new blocker replaces it.
3. **The wish is met by anyone who knows the part.** In a later talk where the speaker knows the wished part, the
   lesson shown is that part (`information.show_how`), instead of the speaker's own pick among their top three.
   - The claim is the speaker's value for it × the usual 0.85–1.35 draw.
   - The lesson then runs exactly as today (`hear_how`): the copying error, the acceptance draw, `can_follow`, NV3's
     part lesson, memory.
   - **One lesson per talk, as now; no extra lesson and no extra time.**
4. **The wish ends** when the learner knows the part (by any route), or after **52 weeks** (one year: four seasons, ACL's
   own cycle, not tuned).
5. **No look-ahead.** The learner never sees the tree. The chain is climbed only through the learner's own failures: a
   wish lesson that fails on a deeper part forms the next wish.
6. **The wish is part of a person's saved state,** so reload is exact.

## Arms and seeds
- **v15 (c), LW (w), and the sham (x):** the standard sham, one extra draw from the world's generator in week one.
- **Seeds 24601–24632** (32 new paired seeds, used by no study). LP; 200 years; years 100–200 counted. `code_lw1` =
  `code_v15` + `learn_wish`.

## Frozen decision rule
- **Guards, LW against v15.** CI1's eight, exactly:
  - starvation deaths per 1,000 living-years: ratio above 1.25 with the lower bound above 1;
  - killings: difference above 0.05 per 1,000 living-years with the lower bound above 0;
  - adult health: difference below −5 with the upper bound below 0;
  - living-weeks: ratio below 0.90 with the upper bound below 1;
  - extinctions: 3 or more extra worlds;
  - child deaths: ratio above 1.25, the lower bound above 1, and a rise of 3 or more per 1,000 child-years;
  - child starvation: ratio above 1.25 with the lower bound above 1;
  - gifts to kin's children: ratio below 0.80 with the upper bound below 1.
- **Co-primary:** the share of invented kinds born in years 100–190 that a non-inventor learns within 5 years, by a
  lesson, watching or reading. LW − v15, paired world bootstrap (10,000 draws; random seed 20261109).
- **Readings:**
  - **supported:** no guard is raised, and the co-primary's lower bound is above 0;
  - **harm:** any guard is raised;
  - **no harm, no effect:** otherwise.
- A supported reading goes to a confirmatory run on new seeds before any adoption.

## Pre-registered secondary (not a gate)
- Invented kinds made by a non-inventor within 5 years, LW − v15.
- Among learner-kind pairs with a failed lesson, the share that learn a missing part within 5 years, LW − v15.

## Described (not decisive)
- **The wish funnel:** wishes formed; met (a lesson shown for a wish); that lesson's outcome (declined; deeper part
  missing; taken); ended by learning, or by expiry; never met.
- **The levels climbed:** for each learner, the chain of wishes, and how many links were learned.
- **The share of grown weeks spent foraging, and talking.** Starvation is the guard; this is the mechanism to read
  beside it.
- **CI1's context measures.**

## Validity (hard stops)
- **Zero checks:**
  - `code_lw1` at 0 = `code_v15` (20 and 60 years, world and random stream);
  - the observer is read-only;
  - LW and the sham act;
  - reload is exact, with wishes saved;
  - **unit checks** (an LW world, 30 years):
    - every wish forms only on a failure with `can_follow` False, on the first missing made part;
    - every lesson shown for a wish is the wished part, from a speaker who knows it;
    - a wish ends when the part is known, or at 52 weeks;
    - no talk has two lessons.
- **All 3 × 32 worlds** are present under one fingerprint.
- **A blind recompute** by GPT, Gemini and DeepSeek.

## The assistant's prior
- **Supported: about 35%.**
  - Wish lessons still pass acceptance only about 21% of the time (PC1), and chains are deep, so the co-primary may move
    little.
  - Learning parts should rise clearly (the secondary).
  - Making by non-inventors stays near 0.
- **No harm likely, about 85%.** Talks are not added, only redirected.

## Sign-off (7 November 2026)
The assistant, under the creator's 2 November permission (new general laws through council, a frozen test in a copy
with a sham, blind recompute, confirmation, the safe path), and their 7 November message: "you supposed to work
autonomous do not ask for permissions from me just go". Council round 74; the assistant's estimate that this study is
valid and informative is 85%. Frozen as `LW1-frozen` before any code or data.
