# PT1 — Does parts-first teaching work? Findings (final: recomputed blind by GPT and Gemini)

Frozen as `PT1-frozen` (operational note 1); decided and signed off in sleep mode (`docs/autonomous_decisions.md`).
Run on GitHub Actions (run 40470789434, `skip_zero=local`). 32 worlds on nature v7, LP (80 founders, 80×80), seeds
18801–18832, 200 years. Mean population 104.5 / 111.5 / 107.7 by era. Every number comes from `analyse_pt1.py`,
written before data; full tables are in `results.md`.

**Validity:**
- zero checks pass;
- all 32 worlds are present under one fingerprint (`code_v7`);
- every gate outcome, every parts-first selection and every memory eviction the observer predicted matches the code
  (mismatches 0).

## The answer

**Parts-first can reach only about a quarter of the lessons that fail at "cannot follow". Where it can, the chain
breaks at making, not at teaching. Separately, the memory limit deletes the new lesson itself in 71% of overflows, an
artefact of the order of two lines of code.**

### Q1 — Is the route reachable? (primary; 95,580 G4 failures of world-born useful kinds)

| class | share [95%] |
|---|---|
| (a) none: the teacher knows no made part | 0.098 [0.084, 0.110] |
| (b) wrong: the part shown is already held | 0.044 [0.039, 0.049] |
| **(c) deep: the part shown itself needs a missing part** | **0.579 [0.559, 0.604]** |
| (d) reachable | **0.278 [0.266, 0.290]** |

The reachable share rises across eras: 0.227, then 0.257, then 0.350.

**The completion funnel** covers 19,472 chains (one learner and one whole kind, ever reachable), followed until death
or the run's end:

| step | chains | conditional [95%] |
|---|---|---|
| part shown and taken | 6,092 | 0.313 [0.302, 0.325] |
| part kept | 3,900 | 0.640 [0.620, 0.661] |
| **part made** | **436** | **0.112 [0.099, 0.125]** |
| every missing part held | 346 | 0.794 [0.755, 0.833] |
| whole taken again | 215 | 0.621 [0.559, 0.678] |
| **whole made** | **12** | **0.056 [0.029, 0.088]** |

**The frozen rule names "whole made"** as the step with the largest loss (lowest conditional). The two making steps
(part made 0.11, whole made 0.06) lose the most. The first step loses the most chains in number: 13,380, mostly through
the part lesson's own belief draw (0.73 of part lessons stop at G3).

Of 19,472 reachable chains, **12** end with the whole made. Of all 59,990 world-born useful chains, 0.021 ever hold the
whole by any route and 0.001 make it.

### Q2 — The selection rule
- **The wrong-part rate is low:** 0.044. A teacher who knew a missing part but showed another: 0.025.
- **Teachers usually know a missing part** (0.88). What they show is mostly a part that is itself out of reach (deep).
- **Reachable part lessons:**
  - the outcome is G1 0.014, G3 0.734, taken 0.252;
  - mean p is 0.251, against 0.290 for the whole lesson;
  - kept, of taken: 0.605.

### Q3 — Memory (lesson-added recipes that overflow the 12-recipe memory)

| lessons | overflows | evicted is the new lesson [95%] | replay: the new lesson survives [95%] |
|---|---|---|---|
| whole, all kinds | 41,808 | **0.714 [0.691, 0.732]** | **0.957 [0.945, 0.971]** |
| whole, world-born useful | 9,865 | 0.784 | 0.957 |
| part, all kinds | 4,906 | 0.737 | 0.975 |
| part, world-born useful | 1,127 | 0.808 | 0.977 |

- **The evicted recipe's value is about 0.002**, and 0.65 of overflows are ties at the lowest value.
- **In the replay** (lesson value 0.070 set first), the recipe evicted instead has a mean value of 0.010.
- **Composites are evicted beyond their share:** 0.728 of evictions against 0.681 held (world-born useful: 0.819
  against 0.692). This is the signature-order tie-break.
- **Relearned:** 0.145 of evicted recipes, after a mean of 283 weeks.

### Q4 — Depth
- **0.681 of failures need two or more levels**, which one-level parts-first cannot complete in one chain:
  - one level: 0.319;
  - two levels: 0.323;
  - three or more: 0.358.
- On average 1.19 parts are missing directly, and 2.70 at all levels.
- **Chains became shallower over time:** two or more levels in 0.748 of failures early, against 0.597 late.

## Against the prior (the assistant's, frozen)
1. "The largest share is (b) wrong or (a) none; under 30% reachable": **wrong on the class** (deep is 0.58; wrong only
   0.04), **right on reachability** (0.278).
2. "Among reachable, the largest loss is the part not being made, after the second belief draw": **mostly right.**
   Making is where chains are lost: part made 0.11, whole made 0.06, with whole made the lowest. The second draw loses
   the most chains in number.
3. "Over 80% of overflows evict the new lesson; in the replay, over half survive": **first part wrong** (0.714, though
   0.784 for world-born useful), **second right** (0.957).
4. "Composites evicted beyond their held share": **right** (0.728 against 0.681).

**On record from the debate:**
- GPT predicted several independent bottlenecks: **supported.** Depth, the second draw, eviction and making all cut.
- Gemini predicted the blind teacher and the memory order as the main structural flaws:
  - the memory order is supported;
  - the blind teacher is not: the wrong-part rate is 0.044. The teacher is not blind so much as the parts are deep.

## Reading (interpretation, not tested here)
- **Teaching reaches the edge of what learners can follow, and making stops there.** Even when parts-first works (part
  taken, kept, every part held, whole taken again), the whole is made in 12 of 215 cases. This is MK1, CO1 and HL1's
  finding again, now at the end of a teaching chain: the choice to make loses to habits.
- **Most lessons are too deep for one-level teaching.** This is a structural limit of the route, not a failure of
  learners.
- **The memory order is an artefact.** A just-taught recipe is judged at value 0 before its lesson value is set, so it
  is deleted in 71% of overflows. With the two lines in the other order, 96% would survive, and what would go instead is
  worth about 0.01. Whether this is a bug or a law is the creator's question. Any change goes by the adoption path, as
  one law, frozen, with a matched control.

## What follows (from the frozen branches)
- **Mostly (c), deep:** "chains are deeper than one-level parts-first can reach. Described." Described here: 0.58 deep,
  and 0.68 need two or more levels.
- **Reachable but lost at a step:** the step is making (the choice: MK1, CO1, HL1), so the learning rule (HL1's branch)
  stays the main lever, with the second belief draw next.
- **Memory:** the replay shows most new lessons would survive with their value set first. **By the frozen text, the
  push-out is an order-of-operations artefact of the code, not a property of memory.** It is a candidate correction,
  judged by the same path as any nature change.

## Independent recompute (27 October 2026)
GPT and Gemini, each in a fresh chat, worked from the raw cells and chains only, without the analysis script
(`recompute_pt1.md`). **All three agree on every key number:**
- reach 0.278 [0.266, 0.290];
- the funnel 19,472 → 6,092 → 3,900 → 436 → 346 → 215 → 12;
- the lowest step is whole made;
- memory: 0.714 evicted new, 0.957 survive in the replay.

**Final.**
