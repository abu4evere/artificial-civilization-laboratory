# LA1 — Why are lessons refused? The lesson-acceptance audit (frozen plan)

**Read-only on nature v7. No change to nature.** From debate round 8 (`docs/debate_after_hl1_2026-10-27.md`): both
GPT and Gemini chose this study first, and the design is GPT's. Background:
- NA1 (final): only 0.020 of offered lessons for useful world-born kinds are taken, falling from 0.031 (years 0–50) to
  0.004 and 0.003 later.
- LU1 (earlier): the main reason was "not open".

The aim is to find out whether acceptance is malfunctioning, not to assume that more acceptance is better.

## How a lesson is decided in `code_v7` (`information.hear_how`, read from the code)

A lesson shows a recipe as the learner takes it in (it can come across wrong). The learner then meets these gates, in
order:

| gate | rejected when |
|---|---|
| **G1, known** | the recipe as shown is already in the learner's memory (including a variant they hold) |
| **G2, tried and found bad** | the learner's own worth for it is below −0.1 and they were never told of it |
| **G3, not taken up** | a random draw ≥ p = credence × openness |
| **G4, cannot follow** | it needs a part the learner cannot make. Then a lesson for that part is shown instead (parts-first, v3) |

If it passes all four, it is taken.

**The parts of p:**
- **openness** = 0.35 × (0.5 + curiosity), doubled if the teacher is the learner's parent;
- **credence** = goodwill (trust and respect), weighted against the record of how the teacher's word has held up as
  that record grows;
- +0.2 for a child listening to an adult;
- + the teacher's visible health;
- +0.15 if the teacher holds the thing.

## Logged (read-only: a wrapper on `information.hear_how` that reads state before and calls the original unchanged)

For every lesson offered (useful kinds, as NA1; all kinds described), the observer records, before the decision:
- the learner, teacher, kind meant and kind as shown (exact, or a variant);
- every condition, overlapping: known; tried-and-bad; can follow;
- **p**, and its parts: openness, the parent doubling, credence, goodwill, the record's weight and estimate, the child
  bonus, the health term, the evidence term;
- the outcome: rejected at which gate, part lesson shown, or taken;
- the learner's age band, relation (parent, carer, other kin, other), the kind's origin (founder or world-born), and
  the era (years 0–50, 50–100, 100–200).

## Questions (primary: world-born useful kinds; adults and children apart; population beside every measure)

**Q1. The rejection funnel.** By era: the share of offered lessons rejected at each gate in order (G1, G2, G3, G4),
part lessons shown, and taken. Also the overlapping conditions (the share known, tried-and-bad, cannot follow,
regardless of order).

**Q2. Threshold margins.** By era: the distribution of p (mean, quartiles; the share under 0.05, 0.1, 0.2) for lessons
reaching G3, and the mean of each part of p. How far are refusals from being taken?

**Q3. By kind and relationship.** Acceptance and mean p by:
- the kind's origin (founder or world-born) and whether it is useful;
- relation (parent, carer, kin, other);
- learner age (child under 12, teen, adult);
- era.

**Q4. Why acceptance falls after year 50 (primary).** The expected acceptance of an offered lesson splits exactly:

P(taken) = P(passes G1) × P(passes G2 | G1) × E[p | reached G3] × P(passes G4 | passed G3)

using p's expectation, not the random draw. From years 0–50 to years 100–200, Δ ln P(taken) is the sum of the four
terms' Δ ln. **The term carrying the largest share of the fall is named.** Then E[p] is split by its parts (credence
against openness; within credence: goodwill, record, the child bonus, health, evidence), by an exact difference
decomposition written before data. World bootstrap (10,000 replicates).

**Q5. Counterfactual gate replay (diagnostic; nothing in the world changes).** For the lessons actually offered in
years 100–200, the expected number taken if one thing alone were set back:
- **(a)** p set to its years 0–50 mean for the same relation and learner age, within the world;
- **(b)** credence set back alone;
- **(c)** openness set back alone;
- **(d)** G1 (known) removed;
- **(e)** G4 (cannot follow) removed.

Each is reported against the actual expectation. It says nothing about later effects.

## What would follow (stated now; not exclusive)

- **G3 carries it, through credence:** learners believe teachers less as time goes on. Next: which part (the record of
  told things failing, fewer children, less goodwill), and whether that is rational distrust (told things that did
  not work) or a malfunction. Only then, any candidate law, decided by the creator.
- **Through openness:** a temperament effect (curiosity). Described.
- **G1 carries it:** lessons come to learners who already hold the thing, or a variant. Then teaching offers the wrong
  things, a teacher-side question.
- **G4 carries it:** lessons need parts the learner lacks. Parts-first teaching is the existing route.
- **Acceptance is rational** (low credence where the record shows told things failing): then the refusals are not a
  malfunction. Making and use (MK1, CO1, HL1) remain the leak.

## The assistant's prior (separate predictions)

1. G3 (the chance draw) rejects most lessons (over 80% of offered), and G1 rejects most of the rest.
2. Mean p for lessons reaching G3 is low (about 0.1 early) and lower late.
3. **The late fall is carried mainly by E[p], through credence:** the record of how teachers' words held up falls, and
   fewer learners are children (the child bonus). It is not carried by G1.
4. Setting p back to its early level (Q5 a) at least triples the expected number taken late.

## Validity (hard stops)

- **Zero checks:**
  - the observer is read-only: state and random numbers identical with and without it, at 20 and 60 years;
  - reload is exact.
- **The replay of p:** the observer's p equals the code's credence × openness for every lesson reaching G3 (a mismatch
  counter that must be 0). Every outcome is consistent with its recorded conditions (taken only if not known, not
  tried-and-bad, and able to follow; a mismatch counter that must be 0).
- All 32 worlds are present under one fingerprint (`code_v7`).
- **An independent recompute by GPT and Gemini** (fresh chats, raw files, no analysis script) of Q4's split and its
  largest term, and Q1's gate shares, before the findings are final. A recompute is recorded only from numbers read
  from the reply.

## Setting

Nature v7, LP (80 founders, 80×80), 32 new seeds (18701–18732), 200 years, run on GitHub.

## Sign-off (27 October 2026)

The creator: "yea draft it, approve and freeze", on this plan (debate round 8: both models' first choice, GPT's design).
Frozen as `LA1-frozen` before any code or data. How the code reads choices the text leaves open goes in operational
notes, appended before any data.

## Operational note 1 (27 October 2026, after freezing, before any data)

How the code (`run_la1.py`, `analyse_la1.py`) reads the text where it left a choice, found in a 20-year smoke world
(seed 9949, not data):
1. **The random draw** at G3 is read from a copy of the world's generator state, without consuming it, so the gate
   actually reached is known exactly. The zero checks confirm this changes nothing.
2. **Taken, then pushed out.** A lesson can be taken (`hear_how` returns True) while the learner's 12-recipe memory is
   full, and the new recipe can then be pushed out at once as the least valued. It counts as taken, and is reported
   separately as "taken, then pushed out of a full memory". (In the smoke world: 62 of 237 taken.)
3. **At G4 the code returns the part lesson's result** (parts-first). The outcome check therefore compares the gate with
   the code's answer at G1, G2, G3 and taken only. The part lesson is logged as its own call, flagged as a part lesson,
   and kept out of the primary funnel.
4. **Origin:** a kind is a founder kind if it was first made in the world by a founder (founders start with no recipes).
   "Useful" is LS1's definition, from the meant kind.
5. **Q4's T4** is the p-weighted share of lessons reaching G3 that the learner can follow, so T1 × T2 × T3 × T4 equals
   the expected share taken exactly. **Q5's (a)–(c)** compare, over the same lessons, the actual expectation with the
   early-mean replacement. (d) and (e) are over all of the era's lessons.
6. **Seeds** 18701–18732.
