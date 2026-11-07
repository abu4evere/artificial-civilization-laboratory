# SP1 findings: where does the spreading of new kinds stop?

**Status: final.** The blind recompute (`recompute_sp1.md`, 7 November 2026, 04:39) matches. GPT and Gemini each
used code, and every total and point estimate agrees. DeepSeek was still working by hand, and nothing from it is counted.

Every number is from `results.md` (analyse_sp1.py, written before data by the Telegram session) on cloud run
42352592253:
- 32 worlds, seeds 24401–24432, on `code_v15`, read-only; kinds born in years 100–190, followed to year 200;
- zero checks All: PASS (`zero_local.log`; read-only; 0 offer replica misses; every taken lesson matched a learn
  event);
- in the study run, 865,204 top-level lessons with 0 offer misses, and 58,788 lessons taken with 0 mismatches;
- 32 of 32 worlds under one fingerprint; 1 extinct.

## The answer in one line
**Spreading stops at the lesson,** and the wall that is particular to new kinds is **a missing part**.
- Of 3,597 new inventions, 35% are ever offered and nearly all of those are shown.
- **Only 6.2% are ever taken up by anyone.**
- **80% of lessons are declined,** by a draw on trust and openness. That draw applies to every lesson, old or new: about
  6.8% of all lessons end in learning (58,788 taken, part lessons included, per 865,204 top-level lessons).
- **For new kinds, a lesson that passes that draw then fails on a missing part 97.6% of the time** (5,547 of 5,686,
  a script on the outcome counts). The new kind needs a made part the learner cannot make.
- The few who learn almost never have the pieces in hand, and making the thing is almost never among their top choices.

**Language is not the missing piece here.** A lesson passes the recipe whole, with no words. It fails because the
learner cannot yet make what the new thing is built from.

## The funnel (frozen; each invented kind counted once per stage; world bootstrap 95%)
| step | rate | kinds |
|---|---|---|
| offered ∣ born | 0.3461 [0.3299, 0.3625] | 1,245 of 3,597 |
| shown ∣ offered | 0.9606 [0.9502, 0.9708] | 1,196 of 1,245 |
| **learned through a lesson ∣ shown** | **0.0619 [0.0452, 0.0805]**, the lowest (the frozen rule) | 74 of 1,196 |
| the learner had the parts ∣ learned | 0.1081 [0.0429, 0.1795] | 8 of 74 |
| made by that learner ∣ had the parts | 0.1250 [0.0000, 0.3333] | 1 of 8 |

The lowest step's interval overlaps the last two. Those rest on 74 and 8 kinds, so they are named too, by the frozen
rule. **In all, 1 of 3,597 new kinds was made by someone who had learned it.**

## Why lessons fail (the lessons of invented kinds, n = 28,897)
| outcome | share |
|---|---|
| **declined** (the learner's trust × openness draw failed) | **0.797** |
| missing part (the learner cannot make a part it needs) | 0.192 |
| already known | 0.006 |
| taken as meant | 0.003 |
| taken with a copying error | 0.002 |
| distrust (tried it, found it bad) | 0.000 |

## After learning
- **Non-inventors who know a new kind** (479,208 knower-weeks):
  - they value it above 0.05 in 75.2% of weeks;
  - **they have the parts in hand in 0.9%;**
  - **making it is among their top 4 options in 0.01%;**
  - they chose to make it in 7 weeks.
- **Inventors** have the parts in hand in only 0.09% of their knower-weeks, and made their kind again in 1.1% of kinds.
- **Copying by watching:** 0 of 3,597 kinds.
- **A non-inventor came to know the kind on their own** (the same recipe found independently, or heated) for 5.5%.
- **70.2% of new kinds were lost** (no one alive knows them) by year 200.
- **Offered ∣ born is low because inventors seldom value their own invention above 0.15** (the offer threshold): only
  39.2% ever do. Yet 92.0% of inventors teach something while knowing the kind.

## Against the prior (questions.md, written by the Telegram session)
| prior | result |
|---|---|
| offered ∣ born the lowest step (about 60%) | **no**: 0.346, but not the lowest |
| next most likely: the learner never gets the parts (about 25%) | partly: 0.108, overlapping the lowest |
| made by a non-inventor who learned it near 0 | **yes**: 1 of 3,597 |

## What it suggests (for the council; nothing decided)
1. **New kinds are built on parts the learner cannot make.**
   - Of lessons that pass the acceptance draw, 97.6% fail there.
   - `hear_how` then offers a part lesson (NV3's parts-first). That part lesson must itself pass the same draw, and the
     learner must be able to follow it.
   - The question for a next study: does learning stall because a nested new kind needs several unknown parts in a
     row? This is the same "missing made parts" RF1 found for inventors.
2. **The acceptance draw:** credence × openness. Openness is 0.35 × (0.5 + curiosity), doubled from a parent, so about 1 in 5 lessons passes for an average non-parent. Real children learn mostly from other children (about 75% of observed teaching among Hadza and BaYaka children; `docs/research/children_innovation_2026-11-06.md`). Whether this draw is too strict is a calibration question, not settled here.
3. **Even learners almost never hold the pieces,** and making the thing almost never enters their top choices. The
   pursuit gap RF1 found for inventors holds for learners too.
4. **The creator's language idea:** the code passes a recipe without words, so words alone would not open the lesson
   step. A shared way to *show that something works* might. That is a design question for the council, not a finding.
