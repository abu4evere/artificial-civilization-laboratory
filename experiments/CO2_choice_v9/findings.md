# CO2 — What makes the other options beat making under nature v9? Findings (final: recomputed blind by GPT and Gemini; see the end)

Frozen as `CO2-frozen` (operational notes 1 and 2); signed off by the assistant under sleep-mode autonomy (read-only;
Gemini 95%; GPT could not be reached tonight). CO1's design re-run on `code_v9`, plus an exact curiosity split. Run on
GitHub Actions (run 41138990924, `skip_zero=local`). 32 worlds (seeds 20701–20732), LP (80 founders, 80 × 80), 200
years. Every number comes from `analyse_co2.py` (CO1's analysis + Q5, written before data); full tables are in
`results.md`.

**Validity:** zero checks pass; all 32 worlds present under one fingerprint (`code_v9`); the identity holds in every
logged week (family, identity and Q5 mismatches 0).

**Population beside it:** all 32 worlds alive at year 100; adults had 7.2 people within reach in years 0–5 and 14.8 in
years 100–200. Offered weeks (adults, making offered): 8,452,691 in years 100–200. Making was chosen in 3.5% of offered
weeks in years 0–5, and in 0.20% in years 100–200.

## The answer

**Two different things, both measured exactly:**
1. **Why making loses at any moment (the level, Q5): the built-in pull carries most of it.** In years 100–200 the
   others' combined score beats making's by 1.643 a week. The **built-in and thought pull** gives **0.562** of that gap
   [0.554, 0.571]: what foraging, gathering and putting things down are worth right now, against what a made thing is
   worth. **Habit** gives **0.351** [0.346, 0.356], multiplicity and spread 0.138, and **curiosity −0.051**
   [−0.053, −0.049]. Curiosity favours making, a little.
   **Frozen reading: "built-in pull carries it"; "curiosity works against the gap".**
2. **Why making's chance falls over time (the change, Q2): habit carries it, as on v7.** From years 0–10 to 100–200,
   the others' soft score rose by +0.639 [0.633, 0.646]. **Habit carries 0.87** of the rise (+0.559 [0.55, 0.569]);
   the per-entry score 0.20; multiplicity 0.02; spread −0.09. Setting habits back to their early values undoes **0.90**
   of the fall in making's log-odds (Q3). CO1 on v7: 0.86 and 0.86.

**Both are true at once.** Making was already a long shot in years 0–10, chosen in about 3% of offered weeks, because
food and gathering simply pull harder. Over the centuries the others' habits then grow tens to hundreds of times (forage
0.04 → 0.64, give 0.02 → 0.78, talk 0.01 → 0.52), while making's stays near 0 (habit 0.04 late). The long shot
becomes a much longer one: 0.20% of offered weeks.

## Against the prior (the assistant's, frozen)
1. "Habit still carries most of the gap (above 0.5)": **wrong for the level** (0.351); **right for the change** (Q2's
   0.87).
2. "Curiosity's part is negative and small": **right** (−0.051).
3. "Setting habits back undoes most of making's fall": **right** (0.90).

## What it means
- **Curiosity (nature v9) is not enough.** It gives making a small push (+0.09 a week against the others' 0.008). That
  is 5% of a gap whose other 95% comes from built-in worth and inflated habits.
- **The decline is a learning-rule story,** as on v7. Other actions' habits inflate (HL1: the max look-ahead; van
  Hasselt 2010's overestimation bias, `docs/research/learning_rule_sources_2026-10-30.md`); making's never does,
  because it is rarely tried.
- **The level is a worth story.** Even with honest habits, a made thing's built-in pull is low against food today. The
  per-entry scores of gathering and putting things down rose (gather 0.31 → 1.03, put 0.28 → 0.68), which shows they
  became more useful as things accumulated.
- **What follows (frozen branch for the reading "built-in pull carries it"):** a read-only look at how the worth of
  made things forms and decays: `itemval` and its updates, and how often made things actually help. Because Q2 repeats
  CO1, the learning-rule question stays open, **for the creator**: a frozen nature-change study of an expected
  look-ahead (Expected Sarsa) instead of the max.
- **No change to nature** follows from this study by itself.

## Independent recompute
Pending: Gemini (fresh chat), and GPT when ChatGPT works on this PC again. From raw per-world sums
(`recompute/co2_one_file.csv`). Recorded only from their actual replies.

## Independent recompute (31 October 2026)
GPT and Gemini, each in a fresh chat, worked from raw per-world sums only, without the analysis script
(`recompute_co2.md`). **All three agree:** Q5's shares (built-in 0.5619, habit 0.3513, curiosity −0.0509, multiplicity
and spread 0.1377; reading "built-in pull carries it"); Q2's rise +0.6394 with habit +0.5592 (share 0.8747).

**Final.**
