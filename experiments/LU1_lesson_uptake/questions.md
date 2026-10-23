# LU1 — Why are offered lessons not taken up? (SIGNED OFF 22 October 2026; frozen as `LU1-frozen` before any data; read-only)

**Why.** GR1 (frozen as G1) moved the bottleneck. With first-season grace, many more useful inventions were valued
enough to teach (19% → 44%) and offered in a lesson (20% → 32%), but hardly more were learned (11.4% → 11.7%).
GPT advised measuring the offer-to-learning step read-only before choosing any change
(`../G1_first_season_grace/gpt_review_gr1_results.md`). The creator: "run both on github".

## What is measured (nothing in the world changes)

`code_lu1` = `code_v3` + logging inside `hear_how`, where a learner decides on a lesson (`v3_to_lu1.diff`). Every
lesson about a way of making something ends in exactly one of:
- **known:** the learner already holds that recipe (as they understood it);
- **own_bad:** the learner tried it and found it no good;
- **not_open:** the learner did not take it up because the chance draw failed (chance = credence in the teacher ×
  openness; openness = 0.35 × (0.5 + curiosity), doubled for a parent);
- **part_shown:** the learner could not follow it, so a part was shown instead (logged again as its own lesson);
- **cannot_follow:** it needs a part the learner cannot make, and no part was shown;
- **taken:** learned.

## Design

- v3, one arm, **256 new seeds 10601–10856**, 20 founders, 120 years, on GitHub.
- **Zero checks (hard stops):** `code_lu1` equals `code_v3` with and without the logging and observers (seeds 11 and
  501 at 5 years, 501 and 601 at 20); reload is exact.

## Questions (described; no test, no adoption)

1. For lessons about **useful** inventions: the share ending in each outcome, pooled over worlds, and the median
   share per world.
2. The same split by teacher (parent or not; the inventor or not) and by learner (child under 16, or adult).
3. Among "not_open": the distribution of the chance of taking it (in tenths), mean credence and mean openness.
4. Among "taken" useful lessons: the share whose learner later made the thing.

## The reading rule (fixed now)

The failure outcome with the largest pooled share among useful lessons is **the main reason lessons fail**, if it is
at least 40% of the useful lessons not taken; otherwise "no single main reason".

## The assistant's prior

**not_open is the main reason** (over half of failed useful lessons): chances are low (credence about 0.4 ×
openness about 0.35), so most lessons are simply not taken. "known" second. "cannot_follow" small, now that
parts-first is in nature.
