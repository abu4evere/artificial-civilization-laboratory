# RF1: Why do the inputs never come together? A read-only remaking funnel (frozen plan)

**Read-only on nature v13.**
- The runner only watches, through wrappers as in VA1.
- Zero checks prove the world is unchanged.

**Why:**
- VA1 (final) and its exploratory follow-up showed that the made thing wears out (98.7% within 5 years, median 32
  weeks), so a second one is needed.
- But when the recipe is still known and valued and the thing is gone (261 cases), the inputs came together only
  twice.
- LH1 (final): even with 16,089 and 25,279 new kinds, remakes were 2 and 2.
- Council round 66 (`docs/debate_round66_after_lh1_2026-11-05.md`): all three models ask for a read-only funnel of
  where the sequence breaks before any intention law (GPT 98%, Gemini 95%, DeepSeek about 90%). GPT: "Distinguish
  inability from failure to pursue an available sequence."

**What it asks:** when a person knows, values and lacks a new kind they invented, does remaking fail because:
- the inputs cannot be had;
- no option toward them is offered;
- the option is offered but loses to other acts;
- or the person starts gathering but never completes the set?

## Worlds
- v13 only, 32 new seeds **23801–23832**; LP (80 founders, 80 × 80); 170 years.
- Kinds followed are the world-new kinds first made in play in years 130–165 (VA1's rule), each for 5 years in its
  inventor's weeks.

## The "wanting" week
A kind's inventor is **wanting** it in a week when all of these hold at their decision:
- they are alive and grown;
- the recipe is still known;
- its value (`itemval`, or the value as a part of a valued thing, as the make option computes it) is above 0.05;
- they do not hold a fresh one (`_holding` with worn_ok False, the make option's own test).

## What is recorded in each wanting week (at the decision; nothing is changed)
- **The missing inputs**, from the recipe exactly as `can_make` reads it, each with its type:
  - raw (a material or the binder, short of the amount needed);
  - part (a made thing not held);
  - wet (a shape recipe whose material is held but not damp enough);
  - fire (a heat recipe away from a fire).
- **For each missing raw input:**
  - whether it is obtainable: a tile within reach (`cfg.reach`) holds at least 1 of it, and there is room under the
    carry limit;
  - whether it is wanted (`_material_wants` > 0).
- **For each missing part:** whether its recipe is known.
- **Offered:**
  - whether the gather option offered is for a missing raw input (the gather option names one material);
  - whether a make option is for a missing part.
- **Chosen:** the act chosen. It is read from the choice's own index; the random draw is untouched.
- **Completed:** whether a chosen gather of a missing input added to the person's stock of it.
- **Context:** the carried material total against the limit, hunger, and what was chosen instead.
- **At each week's end:** whether all the inputs are in hand (`can_make`) while the recipe is known.

## The funnel (per kind with at least one wanting week; the farthest stage reached in 5 years)
| stage | name | meaning |
|---|---|---|
| 1 | cannot obtain | in no wanting week was any missing input obtainable (raw within reach with room, or a part whose recipe is known) |
| 2 | not offered | obtainable at least once, but no option toward a missing input was ever offered |
| 3 | out-competed | offered at least once, never chosen |
| 4 | started, never complete | chosen at least once, but all the inputs were never in hand together |
| 5 | complete | all the inputs in hand at a week's end while the recipe was known (then VA1's later stages: make offered, remade) |

Kinds with no wanting week are counted and reported apart; they are not in the funnel's denominator.

## Measures
A world bootstrap: 10,000 replicates, NumPy seed 20261120; shares pooled over worlds.

1. **Primary: the funnel shares** of the 5 stages, each with its 95% interval and the number of kinds.
2. **The reading (frozen):**
   - **"Inability dominates"** if stages 1 + 2 together are above 0.5, with the lower bound above 0.5. Next: the
     option generation and the inputs' availability, read in the code (a possible fault), not an intention law.
   - **"Pursuit fails"** if stages 3 + 4 together are above 0.5, with the lower bound above 0.5. Next: the council on an
     intention law (a held aim toward a state one's own experience valued).
   - **"Mixed"** otherwise. Next: the council, with the shares.
3. **Described:**
   - per wanting week, the type of the missing inputs (raw, part, wet, fire);
   - the share of wanting weeks at the carry limit;
   - what is chosen instead, the top acts with their shares;
   - for stage-4 kinds, whether a gathered input was later lost before the set was complete (stock lower at a later
     wanting week without the kind being made);
   - the number of wanting weeks per kind.

## Validity (hard stops)
- **Zero checks:**
  - the observers leave the world unchanged (seeds 501 for 20 years and 601 for 60 years, with and without the
    observer: the same world hash and random state);
  - **a unit check:** in every wanting week, the observer's list of missing inputs is empty exactly when `can_make` is
    True for that recipe (wrong 0);
  - at least one wanting week is recorded.
- **All 32 worlds** are present under one `code_v13` fingerprint.
- **A smoke run** before the cloud.
- **A blind recompute** by GPT, Gemini and DeepSeek of the funnel shares and the reading.

## Known limits
- "Obtainable" looks only within reach of where the person stands. Inputs farther away are not counted, which favours
  "cannot obtain". The reach is the decision's own.
- The gather option names one material per decision, so "not offered" can mean that another material won the gather
  slot. The material that won is recorded.
- Five years per kind, in its inventor's weeks.

## The assistant's prior
- **"Pursuit fails"** (stages 3 + 4 above 0.5): about 45%.
- **"Inability dominates"**: about 30%.
- **Mixed**: about 25%.
- The single largest stage is likely "out-competed" (3): gathering a binder or a stone loses to foraging.

## Sign-off (5 November 2026)
The assistant, under the creator's standing autonomy ("keep working", 5 November 2026) and the safe path. Read-only.
Council round 66: all three models ask for this funnel first. The assistant estimates 85% that it is valid and
informative. Frozen as `RF1-frozen` before any code or data.

## Amendment 1 (5 November 2026, 23:30; before any data): why most kinds have no wanting week
The smoke run (2 worlds, 40 years; not data) showed that only 13 of 270 kinds ever had a wanting week. The plan already
reports such kinds apart.
- **Added (described only):** for each of the inventor's decision weeks that is not a wanting week, the first condition
  that fails, in this order: not grown; recipe forgotten; valued at or below 0.05; still holding a fresh one.
- Each kind with no wanting week is reported by the reason seen most often (or "no decision week" if the inventor
  died).
- **Nothing else changes:** not the primary, the stages, the reading or the seeds.

The zero checks run again on the amended runner.
