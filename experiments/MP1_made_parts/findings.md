# MP1 findings: where do the made parts of new kinds go?

**Status: final.** The blind recompute (`recompute_mp1.md`, 7 November 2026, 17:35) matches. GPT and Gemini each used
code, and every point estimate and the reading agree.

Every number is from `results.md` (analyse_mp1.py, frozen before data) on cloud run 42412372759:
- 32 worlds, seeds 24901–24932, on `code_v15`, read-only; kinds born in years 100–190, each followed for 5 years;
- zero checks All: PASS (`zero_local.log`):
  - the observer is read-only;
  - every tracked part has exactly one fate, and none is gone unexplained;
  - the stage checks pass;
  - reload exact;
- in the study run: 441 tracked parts, 0 unexplained, 0 failed stage checks.

## The answer in one line
**The frozen reading: most new kinds stop at A, clearly.** For **0.902 [0.891, 0.914]** of the 3,690 new kinds that
need a made part, **no one who knows the recipe ever holds even one of its made parts** in the 5 years after its
invention.
- The wall is not carrying, and not assembling. **The parts are never made again in the first place.**
- The assistant's prior ("A or B, often dropped at the carry limit") was right about A and wrong about the carry
  limit.

## The funnel (3,690 kinds)
| stage | | share [95%] |
|---|---|---|
| **A** | no knower holds any of its made parts | **0.902 [0.891, 0.914]** |
| B | some parts held, never all at once | 0.056 [0.047, 0.067] |
| C | all parts held, but cannot make it | 0.010 [0.007, 0.014] |
| D | could make it, never made again | 0.017 [0.014, 0.020] |
| E | made again | 0.014 [0.010, 0.019] |

**By depth** (the longest chain of made parts): stage A rises with depth.

| depth | kinds | A | E |
|---|---|---|---|
| 1 | 437 | 0.684 | 0.023 |
| 2 | 1,402 | 0.887 | 0.024 |
| 3 or more | 1,851 | 0.965 | 0.005 |

**The inventor alone** looks almost the same as all knowers together (A 0.908; E 0.008). This is because almost no one
else knows the recipe (LW1, SP1).

## The parts that were made (441 in all 32 worlds)
Only **441 parts** of followed kinds were ever made in a knower's hands, against 3,690 kinds: about one part for every
eight kinds. Their first fates:

| first fate | share [95%] |
|---|---|
| **handed to another** | **0.497 [0.430, 0.555]** |
| worn out in use | 0.138 [0.104, 0.179] |
| used in another thing | 0.129 [0.087, 0.172] |
| worn out by the cold | 0.091 [0.064, 0.125] |
| used in its own kind | 0.073 [0.053, 0.096] |
| still held at the window's end | 0.048 [0.029, 0.070] |
| dropped at the carry limit | 0.025 [0.005, 0.053] |

- **The carry limit is not the wall.**
  - Knowers spend only 0.037 of their weeks at the 3-thing limit (32,770 of 878,365).
  - Only 11 tracked parts were dropped there, and all 11 were picked up by someone else.
- **Half of the few parts made are given away.** A part made for a whole is more often handed to another person than
  used in that whole (0.497 against 0.073).

## What it means
- **Bob's making wall sits at the very first step: making the parts again.**
  - LW1 showed that knowing the recipe is not enough. MP1 shows the gap starts earlier than holding or keeping parts:
    after an invention, its parts are almost never remade.
  - The deeper the kind, the more certain this is (A 0.965 at depth 3+).
- **The evidence on carrying** (`docs/research/carrying_and_toolkits_2026-11-02.md`; one real kit held 29 pieces)
  stays relevant to the world's realism. **It is not what blocks new kinds now.**
- **For the council:** why are parts not remade? Earlier studies point to candidates:
  - **the inputs** (VA1: 87% stop at "held the recipe, never the inputs");
  - **the value a part gets from the whole it goes into** (`_wanted_parts`), and whether the make option for a part is
    ever offered;
  - **the habit look-ahead** that marks making down (LD1).

  A read-only step-by-step look at the knowers of stage-A kinds would settle it. It would cover:
  - whether they know each part's recipe;
  - whether they have its inputs;
  - whether the part is valued;
  - whether making it is offered, and whether it is chosen.
- **Handing parts away** fits the givers' rule (`hand_pick`): it chooses what to hand without regard to what the giver
  is building. This is a candidate for the "choose what to give" ability (PLAY1, rounds 75–76), not a fault.
