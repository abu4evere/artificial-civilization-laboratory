# AG1 — Ageing anchored to forager evidence: does it make ACL's adult deaths realistic, safely? Findings (not final until recomputed; see the end)

Frozen as `AG1-frozen` (operational notes 1 and 2); signed off by the assistant **under the creator's delegation**
("just discuss with gpt and gemini and solve this aging problem") and sleep-mode autonomy. A calibration study: `code_v9`
unchanged; each arm changes one existing setting, `mortality_base`. 80 worlds on 20 paired seeds (20501–20520), LP (80
founders, 80 × 80), 1,000 years:
- 75 worlds were run on GitHub Actions (run 41042869183);
- the 5 worlds lost to the cloud's time limit were run on the creator's PC with the same code and Python, after a
  cross-machine identity check (operational note 2).

Every number comes from `analyse_ag1.py`, written before data; full tables are in `results.md`.

**Validity:** zero checks pass; all 80 worlds present under one fingerprint (`code_v9`); the observer's deaths equal
the world's dead in every world.

**Population beside it** (mean living per century, worlds alive or 0): v 94–141, b 105–163, a 81–157, sham 86–130.
Died out by year 1,000: v 2, b 1, a 5, sham 3 (of 20).

## The answer

**Yes. Both forager anchors make ACL's adult deaths far more realistic. The smaller step (b, matched to the !Kung)
fits best and shows no harm; the forager average (a) overshoots and carries two warning flags.**

### Primary — calibration distance (all-cause death rates per person-year, years 100–999)
| arm | ages 30–45 (ref 0.0167) | 45–60 (ref 0.0264) | 60–70 (ref 0.0524) | D | D − D(v) [95%] |
|---|---|---|---|---|---|
| v (v9) | 0.0298 | 0.0762 | 0.2015 | 0.995 | |
| **b (!Kung step)** | **0.0166** | 0.0284 | 0.0705 | **0.125** | **−0.871 [−0.880, −0.823]** |
| a (forager average) | 0.0134 | 0.0209 | 0.0492 | 0.172 | −0.823 [−0.906, −0.746] |
| x (sham) | 0.0304 | 0.0760 | 0.2038 | 1.005 | +0.009 [−0.017, +0.036] |

**The frozen rule:** an arm is "more realistic" if the upper bound of D(arm) − D(v) is below 0 and below the sham's lower
bound (−0.017). **b: more realistic. a: more realistic.** Their intervals overlap, so by the frozen rule **both
calibrate, and the choice is the creator's.**

- b sits almost exactly on the forager total at ages 30–45 (0.0166 against 0.0167) and somewhat above it at older
  ages.
- a sits **below** the reference in every band: ACL adults would then die less often than foragers do. ACL's other
  causes of death (starvation, thirst) did not make up the difference, as the assistant's prior had expected.

### Flags (LC1's; with 20 pairs, a safety warning, not proof of harm)
- **b: none.** Extinct 1 against v's 2; living person-years in years 800–999 b ÷ v = 1.034.
- **a: both flags.** Extinct 5 against v's 2 (a difference of 3); living person-years in years 800–999 a ÷ v = **0.774**.

### Described (not part of the rule)
| | v | b | a | sham |
|---|---|---|---|---|
| mean adult (16+) age at death | 45.1 | **54.3** | 58.5 | 44.8 |
| adult deaths at 60+ | 0.147 | **0.443** | 0.541 | 0.143 |
| adult deaths at 70+ | 0.014 | **0.212** | 0.326 | 0.013 |
| living aged 60+ (share, years 800–999) | 0.013 | 0.078 | 0.108 | 0.013 |
| adult deaths from "old age" / "illness" | 0.38 / 0.43 | 0.54 / 0.19 | 0.57 / 0.17 | 0.37 / 0.43 |
| adult deaths from starvation | 0.12 | 0.17 | 0.18 | 0.13 |

**Knowledge did not improve** (years 800–999). World-born adults' crafting skill: b − v −0.004 [−0.018, +0.008];
a − v −0.010 [−0.021, −0.000]. Making per adult-year: b − v −0.004 [−0.012, +0.004]; a − v −0.007 [−0.012, −0.002].
Longer lives alone do not make knowledge build up, which fits LS2, AW1 and CO2: the bottleneck is the choice to make.

## Against the prior (the assistant's, frozen)
1. "Both a and b are more realistic": **right.**
2. "a is closer to the reference than b, but ACL's other deaths keep both above it": **wrong.** b is closer
   (D 0.125 against 0.172); a falls below the reference.
3. "No flags; population rises somewhat in both; skill and making change little": **right for b**
   (population +3%, no flags); **wrong for a** (two flags; population −23% late on). Skill and making change little in
   both, slightly down in a.

## What it means
- **The creator's idea holds, in its realistic form.** ACL people can live realistic forager lives. With the !Kung
  step, the mean adult age at death goes from 45 to 54, and 44% of adult deaths come at 60 or later (against 15%).
- **"Slightly" was the right instinct.** The smaller, harsher-forager anchor (b) fits the evidence best and is safe.
  The larger one (a) overshoots, and its worlds are smaller and die out more often. A plausible reason, not yet
  shown: more elders who eat but no longer bear children.
- **Not a knowledge fix.** Longer lives keep skilled people alive longer, but people still rarely choose to make.
- **What follows (frozen):**
  - **b: "an arm more realistic, no flags"**, so **a confirmatory run on new seeds, then the creator decides
    adoption** (nature v10).
  - **a: "more realistic with a flag"**, so a read-only look at why its population falls, before any thought of
    adoption.
- **Adoption is never autonomous.**

## Independent recompute
Pending: GPT and Gemini, fresh chats, from raw per-world counts (`recompute/ag1_one_file.csv`). Recorded only from
their actual replies.
