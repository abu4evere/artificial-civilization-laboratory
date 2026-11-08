# PM1 findings: why are the parts of new kinds never made again?

**Status: final.** The blind recompute (`recompute_pm1.md`, 7 November 2026, 20:10) matches: GPT and Gemini agree in
every point estimate and in the reading.

Every number is from `results.md` (analyse_pm1.py, frozen before data) on cloud run 42427166476:
- 32 worlds, seeds 25001–25032, on `code_v16`, read-only; kinds born in years 100–190, followed 5 years;
- zero checks All: PASS (`zero_local.log`):
  - the observer is read-only;
  - the make option offered was predicted exactly at every look;
  - the event checks pass;
  - reload exact;
- in the study run: **45,071,900 decisions looked at, 0 make-option mismatches, 0 failed event checks.**

## The answer in one line
**The frozen reading: most kinds stop at P1, clearly.** For **0.710 [0.688, 0.729]** of the 3,929 new kinds that need a
made part, someone who knows the kind also knows the part's recipe, but **never has the part's inputs in hand.**
- The assistant's prior was wrong. It expected "never valued" (P2, about 45%); P2 is 0.047.

## The funnel (3,929 kinds)
| stage | | share [95%] |
|---|---|---|
| P0a | the part's recipe known by no one living | 0.101 [0.085, 0.118] |
| P0b | the knower lacks the part's recipe; someone else has it | 0.026 [0.020, 0.032] |
| **P1** | **known, never the inputs in hand** | **0.710 [0.688, 0.729]** |
| P2 | inputs in hand, never valued enough to make | 0.047 [0.041, 0.053] |
| P3 | eligible, never the make option offered | 0.010 [0.007, 0.012] |
| P4 | offered, never chosen | 0.051 [0.044, 0.058] |
| P5 | chosen, never made | 0.000 |
| P6 | made, never all parts held at once | 0.026 [0.022, 0.031] |
| P7 | all parts held at once | 0.030 [0.022, 0.039] |

**By depth:** P1 grows with depth.

| depth | kinds | P0a | P1 | P2 | P7 |
|---|---|---|---|---|---|
| 1 | 447 | 0.107 | **0.318** | 0.221 | 0.087 |
| 2 | 1,450 | 0.105 | **0.650** | 0.051 | 0.037 |
| 3 or more | 2,032 | 0.097 | **0.838** | 0.005 | 0.012 |

**Never-valued kinds** (0.145 of all, 570) stop mostly at P0a (0.653). A kind its inventor never values loses its parts'
recipes. Kinds that were valued stop mostly at P1 (0.783).

**Where the rest went:**
- When another recipe won the single make slot (P3 looks), it was an old recipe 0.908 of the time.
- When making the part was offered but not chosen (P4 looks), the choice was:
  - forage 0.498;
  - talk 0.229;
  - give 0.130.

## Why P1: what the code does (read for this record)
- **Making a part needs value and inputs.**
  - **Value.** A part is valued for making through the whole it goes into (`mind._wanted_parts`: 0.8 × the whole's
    value). This happens only when that whole is valued directly (`itemval` > 0), and only one level down.
  - **Inputs.** The inputs must already be in hand (`can_make`).
- **Raw materials are wanted only for things valued directly.** `mind._material_wants` wants a recipe's materials only
  when the person values that recipe directly (`itemval` > 0). The value a part gets from its whole never reaches the
  part's own materials.
- **Sub-parts are never wanted at all.** A part's own made sub-parts get no value either, because `_wanted_parts` does
  not look below one level.
- **So the chain breaks below the first level.** A person can want the part, but nothing makes them gather what the
  part is made of, or make what it needs. Deep kinds stall at P1 (0.838 at depth 3+).

## What it means
- **The making wall for Bob is a planning wall.** People can want a whole, and its direct parts, but the want does not
  flow down to what those parts need. This is goal decomposition, the "planning depth" of the curation evidence
  (`docs/research/curation_and_parts_2026-11-07.md`).
- **For the council, a general law candidate:** "what a valued whole needs is wanted". Value would flow down the recipe
  tree, from a whole to its parts, their sub-parts and their raw materials, discounted at each step (as `_wanted_parts`
  already does with 0.8).
  - It names no thing, plans no chain, and adds no reward.
  - It extends one existing rule to the materials rule and to deeper levels.
  - It would be tested in a copy with a sham, CI1's guards and a confirmatory run.
- **A second, smaller wall is memory.** 10% of kinds stop because no one living still knows a part's recipe (P0a),
  mostly kinds never valued by their inventor. The 12-recipe memory is a suspect
  (`docs/research/skills_per_person_2026-11-07.md`), for later.
