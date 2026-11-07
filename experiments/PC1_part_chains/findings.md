# PC1 findings: the part chains of new kinds: why lessons fail on a missing part

**Status: final.** The blind recompute (`recompute_pc1.md`, 7 November 2026, 07:40) matches. GPT and Gemini each
used code, and every point estimate and the reading agree. DeepSeek was still working by hand, and nothing from it is
counted.

Every number is from `results.md` (analyse_pc1.py, frozen before data) on cloud run 42366219425:
- 32 worlds, seeds 24501–24532, on `code_v15`, read-only; invented kinds born in years 100–190, followed to year 200;
- zero checks All: PASS (`zero_local.log`; read-only; 0 tree mismatches; every taken part lesson matched a learn
  event; reload exact);
- in the study run, 0 tree and part-lesson mismatches in every world.

## The answer in one line
**The frozen reading: a deeper, learner-driven part lesson could help.**
- **New kinds sit on deep chains.** In 56% of failed lessons the missing chain is 3 or more levels deep.
- **The teacher knows every missing part in 93% of failed lessons.**
- **The one-level part lesson never helps:** 0 of 4,359 led to learning. It almost always shows a part the learner
  lacks (99%), but the learner declines it (78%), or it fails on a still deeper missing part (21%).

## 1. The trees (2,784 invented kinds)
**The longest chain of made parts:**
| depth | share |
|---|---|
| 0 | 0.004 |
| 1 | 0.129 |
| 2 | 0.390 [0.372, 0.407] |
| **3 or more** | **0.477 [0.453, 0.499]** |

## 2. The failed lessons (4,625 top-level lessons that failed on a missing part)
- **Missing made parts:** usually one (0.965); two in 0.035; never three or more.
- **The deepest missing chain beneath:**

  | levels | share |
  |---|---|
  | 1 | 0.093 |
  | 2 | 0.350 |
  | **3 or more** | **0.557 [0.514, 0.598]** |

- **The teacher knows the missing parts:**

  | | share |
  |---|---|
  | all | **0.926 [0.899, 0.952]** |
  | some | 0.009 |
  | none | 0.064 [0.038, 0.091] |

## 3. The one-level part lesson (NV3's parts-first)
- **It followed 94.2% of failed lessons** (4,359).
- **The part shown was one the learner lacked in 99.0%.** "The first part in the recipe's order" is almost never
  wasted (1.1% already known).
- **Its outcome:**
  - declined at the learner's draw: **0.780**;
  - failed on a deeper missing part: **0.209**;
  - **taken: 0.000 (0 of 4,359).**
- **Not helpful: 1.000.**

## 4. Afterwards (3,369 learner-kind pairs, within 5 years of the first failure)
- learned a missing part: 0.006;
- learned the kind: 0.001 (2 pairs);
- made it: 0.

## Against the prior (questions.md)
| prior | result |
|---|---|
| most trees 1–2 deep | **no**: 48% are 3 or more deep |
| usually a single part missing | yes (0.965) |
| the teacher knows it, about 70% | **more**: 0.926 |
| the one-level lesson often wasted, about 40% | **no**: 1.1% wasted. It fails by being declined, or on a deeper missing part |
| reading "could help", about 60% | **yes** |

## What it means for (b), learner-driven deeper part lessons (for the council; nothing decided)
1. **The knowledge is within the teacher's reach** (93%). The one-level lesson aims at the right part. So the
   chain is not blocked by missing knowledge in the world.
2. **But two walls compound:**
   - **Depth:** a chain of 3 or more levels needs 3 or more successful part lessons in a row. Today's lesson stops
     at one, and every accepted part lesson then failed on a deeper part.
   - **Acceptance:** each part lesson must pass the learner's draw. Here 0.211 passed (911 of the 4,309 part lessons
     that reached the draw). Three in a row would pass 0.0094 of the time, the assistant's arithmetic by script.
   - So (b) alone may open little unless the chain can be taught across several talks, bottom-up, so that each part
     is learned on its own before the next. That is how a learner-driven version would work (DeepSeek's trigger: "the
     learner failed on a missing part this time"), with a budget.
3. **The council should weigh (b) against (c), the acceptance draw**, which multiplies at every level of a chain.
