# PT1 — Does parts-first teaching work? The parts-first and memory audit (frozen plan)

**Read-only on nature v7. No change to nature.** Chosen in sleep mode (`docs/autonomous_decisions.md`, 27 October
2026). Both GPT and Gemini chose this study first, after LA1 (GPT 85%, Gemini 95%). The design adds both models' design
notes (debate round 9, `docs/debate_after_la1_2026-10-27.md`).

**LA1 (final pending recompute):**
- 0.85–0.88 of offered lessons for world-born useful kinds need a part the learner cannot make (G4, "cannot follow");
- removing G4 in replay gives 8.1 times the expected takes;
- 0.56 (early) and 0.37 (late) of taken lessons are pushed out at once by the full 12-recipe memory.

The code's intended route past G4 is **parts-first** (NV3): when a lesson cannot be followed, the teacher shows a part
instead.

## How it works in `code_v7` (read from the code)

**Parts-first** (`information.hear_how`), when a whole lesson passes G1–G3 but fails G4:
- the code takes the recipe's made parts (not raw materials) in order;
- it shows **the first one the teacher knows**, as the learner takes it in (it can come across garbled);
- it does **not** check whether the learner already knows that part, or whether it is the part they lack;
- the part lesson meets the same gates G1–G4, **with its own belief draw**;
- it goes **one level deep**: a part lesson that itself fails G4 shows nothing further.

**Memory** (`knowhow.remember_recipe`):
- a taken recipe is added with its existing value, or 0;
- if over 12, the lowest-valued recipe is deleted (on ties, the first by signature order; composite signatures begin
  with "(", which sorts first);
- **only then** does `hear_how` give the new recipe its lesson value, max(own, 0.5 × claim × credence).

## Logged (read-only wrappers on `information.hear_how` and `knowhow.remember_recipe`; weekly events; nothing changes)

**For every whole lesson that reaches G4 and fails it** (a "G4 failure"; it gets a chain id):
- the learner, teacher, kind meant, time, era, origin (founder or world-born), useful (LS1), relation and age (as LA1);
- **the full set of missing parts**: made parts the learner lacks, found recursively through the teacher's recipes (or
  the world's record of each part), with the minimum depth;
- every made part the teacher knows;
- **the part selected** by the code's rule, and its kind:
  - (a) none: the teacher knows no made part;
  - (b) wrong: the selected part is already held by the learner;
  - (c) deep: the selected part is missing but itself needs a missing part;
  - (d) reachable: the selected part is missing, and the learner could follow it;
- the part lesson's outcome: the gate where it stops (G1 / G2 / G3 / G4 / taken), its p, and whether it was shown
  garbled.

**After the call:**
- whether the taken part is still held (kept, or pushed out at once).

**Followed until the learner dies or the run ends (censoring recorded):**
- the learner first makes the part;
- the learner first holds every missing part, by any route;
- the whole is offered again and taken;
- the learner first holds the whole, by any route;
- the learner first makes the whole.

The time between steps is recorded. "Made" is a `make` or `play` event by the learner with that kind.

**For every recipe added through a lesson (`taught`) that overflows the 12-recipe memory:**
- the whole memory before the deletion: values and signatures;
- the evicted recipe: its value, and whether it is the new lesson;
- how many recipes tied at the lowest value;
- whether the evicted recipe is a composite;
- **the replay:** which recipe would be evicted had the lesson value been set first (one-event mechanical
  counterfactual only);
- whether each evicted recipe is held again later (relearned), and how.

## Questions (primary: G4 failures of world-born useful kinds; population beside every measure; world bootstrap, 10,000 replicates)

**Q1. Is the parts-first route reachable (primary).** The shares of G4 failures in (a) none, (b) wrong, (c) deep and
(d) reachable, by era. **Then, among reachable failures only, the completion funnel:**
- part shown and taken;
- part kept;
- part made;
- every missing part held;
- whole taken again;
- whole made.

The conditional probability at each step, with censoring (death, run end), and the median time between steps.
**Named: the share of G4 failures that parts-first can reach at all, and the step with the largest loss among reachable
ones.**

**Q2. The selection rule.** How often the part shown is a part the learner already holds, while a different part is
missing (the wrong-part rate). How often the teacher knew a missing part but showed another. For the reachable cases:
the part lesson's gate outcome and p, against the whole lesson's p.

**Q3. Memory.** For lesson-added recipes that overflow memory:
- how often the evicted one is the new lesson;
- the evicted recipe's value;
- the tie count;
- whether composites are evicted more often than their share of held recipes;
- **in the replay**, how often the new lesson would have survived had its value been set first, and the value of what
  would have been evicted instead.

Separately for whole lessons and part lessons. Whether evicted recipes are relearned, and the time until then.

**Q4. Depth.** The distribution of the number of missing parts and of the minimum depth across all G4 failures, and
the share needing two or more levels (which one-level parts-first cannot complete in one lesson chain).

## What would follow (stated now; not exclusive)

- **Mostly (a), none:** teachers rarely know the parts of what they teach. Then teaching offers kinds whose parts are
  not taught. That is a teacher-side question (what is offered).
- **Mostly (b), wrong:** the selection rule shows the wrong part. A candidate condition-level nature change (show a part
  the learner lacks) is the creator's to decide, or the sleep-mode adoption path. It would be one law, frozen, with a
  matched control.
- **Mostly (c), deep:** chains are deeper than one-level parts-first can reach. Described.
- **Reachable, but lost at a step:** that step is the next target:
  - the part's belief draw;
  - memory push-out (Q3);
  - the part not made (the choice: MK1, CO1, HL1);
  - the whole not offered again.
- **Memory:** if the replay shows most new lessons would survive with their value set first, the push-out is an
  order-of-operations artefact of the code, not a property of memory. That is a candidate correction, judged by the same
  path as any nature change.

## The assistant's prior (separate predictions)

1. The largest share of G4 failures is (b), wrong part, or (a), none. Under 30% are reachable.
2. Among reachable failures, the largest loss is the part not being made (the choice), after the second belief draw.
3. Over 80% of lesson-added recipes that overflow memory evict the new lesson itself. In the replay, over half would
   survive.
4. Composite recipes are evicted at more than their held share.

**On record from the debate:**
- GPT predicts several independent bottlenecks, not one;
- Gemini predicts the blind teacher and the memory order as the main structural flaws.

## Validity (hard stops)

- **Zero checks:**
  - the wrappers and observer are read-only: state and random numbers identical with and without them, at 20 and 60
    years;
  - reload is exact.
- **Replays match the code:**
  - the observer's predicted part selection equals the part the code actually showed (a mismatch counter that must
    be 0);
  - the observer's predicted eviction (on the actual order) equals the recipe actually deleted (must be 0).
- All 32 worlds are present under one fingerprint (`code_v7`).
- **An independent recompute by GPT and Gemini** (fresh chats, raw files, no analysis script) of Q1's shares (a)–(d)
  and the reachable funnel, and Q3's share of evictions that are the new lesson and its replay, before the findings are
  final. A recompute is recorded only from numbers read from the reply.

## Setting

Nature v7, LP (80 founders, 80×80), 32 new seeds (18801–18832), 200 years, run on GitHub.

## Sign-off (27 October 2026)

The assistant, under the creator's sleep-mode autonomy (CLAUDE.md, Sleep mode). Both models chose this study, and its
estimated success is 85% (above the 40% threshold). Logged in `docs/autonomous_decisions.md`. Frozen as `PT1-frozen`
before any code or data. How the code reads choices the text leaves open goes in operational notes, appended before any
data.

## Operational note 1 (27 October 2026, after freezing, before any data)

How the code (`run_pt1.py`, `analyse_pt1.py`) reads the text where it left a choice, found in a 20-year smoke world
(seed 9949, not data):
1. **Name.** The study was drafted as PF1. That name already belonged to the partner-finding study, so it is PT1, frozen
   as `PT1-frozen` (the earlier commit shows the rename).
2. **A G4 failure** is a whole lesson that passes G1–G3 and fails G4, judged as LA1 judges it (the copied-generator
   draw).
3. **The four classes follow the code's own selection rule:** the first made part, in the recipe's order, that the
   teacher knows. The class uses the teacher's true recipe for that part; the part lesson itself may still come across
   garbled, which is recorded.
4. **"Missing parts"** are the made parts the learner lacks, found recursively through the teacher's recipes (or the
   world's record when the teacher lacks one), with a guard against cycles. **"Levels needed"** is 1 when every
   missing part can itself be followed, and is counted up to "3 or more".
5. **Chains** are one learner and one whole kind, counted from the learner's first G4 failure for that kind. Later
   failures add to the same chain. **"Reachable" chains** are those with at least one reachable failure.
6. **The funnel's steps** are counted in order. A chain reaches a step only if it reached every earlier step. The
   steps are:
   - "part made": the reachable part, by a `make` or `play` event of the learner;
   - "every missing part held": every direct missing part was held at some time after the failure, by any route;
   - "whole taken again": a later lesson for that kind was taken;
   - "whole made": a `make` or `play` event of that kind.

   Times are measured from the first G4 failure, because holding every missing part can come before making the part.
7. **The memory replay** sets the new lesson's value to max(its existing value, 0.5 × claim × credence) before the
   12-recipe limit, with every other value unchanged. The composite share held counts the 13 recipes at the moment of
   overflow.
8. **Relearning** counts the evicted recipe entering the learner's memory again, by any route.
9. **Population** is the number of living people, sampled once a year.
10. **Bootstraps** resample whole worlds (10,000 replicates) and pool ratios over them.
11. **Seeds:** 18801–18832.
