# AW1 — Learning a craft from others: does watching, or being shown, pass technique and bring making back? (frozen plan)

**A nature-change study.** `code_aw1` would be `code_v9` + one setting, `skill_pass` (0 = v9 exactly). Adoption is the
creator's decision.

**Why.** The creator's order (30 October 2026): ageing (AG1, running), then apprenticeship, then talent. LS2 (final):
98% of knowledge is lost at death; making collapses at the choice; each generation takes up about a quarter of its
carers' recipes; of recipes got from others only 0.03–0.05 are ever made; crafting skill at 30 falls from 0.52 to 0.08
over the cohorts. Today **skill never passes between people**: everyone builds it alone, by making or playing. Evidence
(abstracts; `docs/research/skill_learning_sources_2026-10-30.md`): forager children learn by play, observation and
joining in, and adults teach complex tool making in adolescence (Lew-Levy et al. 2017); in experiments, being taught
passed stone-tool skill, while imitation alone did not (Morgan et al. 2015). Debate round 34
(`docs/gpt_view_apprenticeship_2026-10-30.md`): both models want W and T as separate arms and making as the primary.

## The laws (each reuses nature's existing chance and skill step; no new number)
- **W, watching:** when someone successfully makes a thing, each person aged 6+ within sight (`perception`, 4 tiles;
  the crossing rule's age and radius) who notices it (the existing chance 0.04 × (0.5 + curiosity), one draw per
  eligible onlooker, the age checked before the draw) gets **one ordinary crafting practice step** (`_gain_skill`:
  0.012 × (1 − skill), × 1.6 when focused). The hook sits in `_make`'s success branch, not in `_craft` (so play and
  failed attempts do not count).
- **T, being shown:** when a teacher shows a recipe in talk (`information.show_how`, a recipe offer), the learner gets
  **one ordinary crafting practice step**, whether or not they take the recipe. No random draw is added.
- Nothing else changes: no recipe passes by W; T's recipe passing is unchanged; no habit values, `tried` counts, item
  values or memories change; with the setting at 0, no draw, no state change.

## Design
- **Arms:** v (v9), w (`skill_pass` 1), t (`skill_pass` 2), x (sham: v9 with `sham_draw` 1).
- **World:** LP (80 founders, 80 × 80), **200 years**, **32 new paired seeds (20601–20632)**. 128 worlds. (CU1's pattern: 200 years
  first; a 1,000-year check only if supported.)

## Primary
**Making events per adult-year, years 100–200** (CU1's and LC1's measure: adults 16+, survivor-weighted, ratio of
sums over worlds). Paired world bootstrap (10,000 replicates; generator seed 20261031; 95% percentile intervals).
**Rule (CU1's):** an arm **supports** if the lower bound of (arm − v) is above 0 and above the upper bound of
(x − v). **Flags (CU1's):** 3 or more extinct worlds than v; population in years 100–200 below 0.90 × v.

## Secondaries (described)
- World-born adults' (20–40) crafting skill, years 100–200 (the mechanism check), and children's (6–11) crafting
  skill; teens' (12–15) making.
- Made things held per adult; the number of practice steps given by the law (it acts, and how often).
- Population and extinctions.

## The assistant's prior
1. Both arms raise skill (the mechanism works), T more than W (lessons are frequent: 0.3–3.6 offered per person-year
   in LS2; the noticing chance is small).
2. Making rises little: the pull to make reads the thing's worth, diligence and hunger, not skill (`mind.py`); skill
   reaches it only through better strikes and gathering. GPT gives 40% that making rises meaningfully.
3. No flags.

## What would follow
- **Making rises (supports):** a 1,000-year check, then the creator decides adoption.
- **Skill rises, making does not:** technique is not the bottleneck; the choice is. Next: why the choice falls (the
  worth of made things, LS2's "what won": foraging 0.67), read-only first.
- **Neither:** the passed steps are too few to matter; report how many were given.

## Settled at freezing
- **T applies to every recipe shown in talk**, whether or not the teacher can make it at that moment: being told is
  part of being shown (Morgan et al. 2015: verbal teaching passed the most), and the existing copying-error rule
  already rewards showing with the things in hand. No new condition is added.

## Sign-off (30 October 2026)
**The creator: "yea go ahead with AW1 run it after AG1".** Frozen as `AW1-frozen` before any code or data. It runs on
GitHub after AG1 finishes.
