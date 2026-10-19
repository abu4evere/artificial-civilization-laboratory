# CA3 — Opportunity or availability: findings

Frozen as `CA3-frozen` (signed off by the creator, all recommendations). Read-only: a logging copy of nature v2, shown
to change nothing; CA1's 32 worlds replayed, **every replay ending in CA1's saved state**. Table: `results.md`, from
`analyse_ca3.py`. **Valid:** zero check, all 32 worlds, replays exact, one fingerprint.

## Question 1: why most inventions never reach a teaching talk

| | discovery | holdout |
|---|---|---|
| useful inventions never passed on that stopped at G1 (CA2's largest loss) | 2,370 | 2,229 |
| **availability-limited** (the inventor held it under 13 weeks) | **2,350 (99%)** | **2,207 (99%)** |
| opportunity-limited (held 13 weeks or more, never in a teaching talk) | 20 (1%) | 22 (1%) |
| how it was lost: **pushed out by the 12-recipe limit** | **2,346 (99%)** | **2,204 (99%)** |
| how it was lost: the inventor died | 24 (1%) | 25 (1%) |

**The frozen reading: availability, in both sets.** CA2's biggest loss was not that inventors never met anyone to
teach. Almost every invention that never reached a lesson was gone from its inventor's memory within a season, pushed
out by the 12-recipe limit before any teaching talk could happen.

## The assistant's prior, against the result

| prior (frozen) | result |
|---|---|
| availability: most G1-stopped inventions are dropped within weeks (forgotten as useless or pushed out of the 12) | **right**: 99%, and almost all by the 12-recipe limit, not by forgetting |
| composites: under 5% of talk partners know the parts | **wrong**: 7.6% / 8.4% (still low) |

The first right prior in this line (CA1 and CA2's were wrong).

## Described

- **Question 2 (composites).** In more than 500,000 (discovery) and 440,000 (holdout) teaching-possible talks in which
  an inventor held a useful composite that was never passed on, the learner knew how to make every made part in
  **7.6% / 8.4%**. Even when the right person was there, about eleven times in twelve they could not have followed it.
- **Question 3 (what separates inventions that spread), medians weighted by inventions:**

| | inventions | weeks held | teaching talks while held | different learners met | inventor a child (under 16) | ever valued enough to offer |
|---|---|---|---|---|---|---|
| passed on, discovery / holdout | 659 / 526 | 851 / 954 | 83 / 72 | 11 / 11 | 45% / 43% | 43% / 44% |
| never passed on | 5,138 / 4,853 | 155 / 204 | 21 / 30 | 5 / 5 | **80% / 80%** | 18% / 15% |

  Inventions that spread were held five times as long and shown to about twice as many people; four in five that
  never spread were made by children.
- Population (rule 18): median 24–42 (discovery) and 21–29 (holdout) living people per decade.

## Caveats

1. The 13-week line was fixed before data; with 99% on one side, the reading does not depend on it.
2. "Pushed out" is the code's 12-recipe limit acting on a brand-new recipe valued at zero, with ties broken by name so
   that composite names sort first: the accident already listed among the book's known compromises ("a memory that
   discards composite inventions"). CA3 measures its size; it does not show what removing it would do.
3. Question 3 is described, not tested; children invent most in play, so "child" and "pushed out" overlap.
4. Recorded causes only: what the log saw. Why children's inventions are valued at zero is a rule of the code, not
   observed behaviour.

## What it suggests (for the creator; nothing changed)

CA1 found the chain breaks at the first hand-over; CA2 that most losses come before any lesson, and that composites can
almost never be followed; CA3 that the "before any lesson" loss is almost entirely **memory**: new inventions are
pushed out of a 12-place memory within weeks. Two candidate places for a Law 126 decision, each needing evidence before
any design:

- **The memory limit and how it chooses what to drop.** Twelve recipes is not anchored to anything about real people,
  and the tie-break that drops composites first is a bookkeeping accident. A question for evidence: how many distinct
  techniques do real foragers know, and how do people forget them?
- **Learning parts before wholes** (the teaching review, `evidence_teaching.md`): real learners meet parts and simpler
  versions first; ACL's lesson needs every part already known (CA3: about 1 talk in 12).

GPT's boundary stands: a gate associated with failure does not prove that changing it would build culture.
