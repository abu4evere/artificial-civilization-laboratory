# CA3 — Opportunity or availability: why most inventions never reach a lesson (DRAFT, 19 October 2026; not frozen, nothing run)

**Why.** CA2 (`../CA2_teaching_gates/findings.md`, `CA2-done`) found that for **46%** of useful inventions never passed
on, the inventor never once took part in a talk where teaching could happen while knowing it (G1), and for another
36–39% never valued it enough to offer it (G2). It also found the narrowest gate: composites can almost never be
followed by a learner who cannot make their parts (G7). GPT's review (19 October 2026, under the creator's delegation;
a review, not a sign-off) advised this read-only audit **before** any evidence review or change: "Proceed with the
read-only audit first. No changes to ACL's teaching, learning, or recipe rules yet." **Read-only: nothing in ACL changes.**

## Questions

1. For inventions that stopped at G1: was it **availability** (the inventor lost the know-how soon: died, forgot it, or
   had it pushed out of their 12) or **opportunity** (they kept it, but no teaching talk happened)?
2. For composites: how often could the inventor's actual talk partners have followed it (did they know the parts)?
3. What separates inventions that spread from those that never did (inventor's age, holding time, talks, value)?

## Design (the assistant's recommendation; decisions marked)

- **Instrument:** `code_ca3` = `code_ca2` (CA2's logging copy) + one more logged field: in each teaching-possible talk,
  the **learner's** recipes at that moment (for question 2). Logging only; shown to change nothing (state hash equal to
  `code_v2`, seeds 501 and 601, 20 years); every replay must end in CA1's saved state.
- **Worlds:** CA1's seeds again, **discovery 6301–6316, holdout 6317–6332** (Decision 1; or new seeds).
- **Measured per useful invention** (GPT's list): time from invention to the first teaching-possible talk, to the first
  offer, and to loss; **how it was lost** (the inventor died, forgot it as useless, pushed out by the 12-recipe limit,
  or held to the end); how many such talks and with how many different people while held; the inventor's age when they
  invented it; for composites, the share of talk partners who knew how to make every made part.
- **Computer:** two spare workers, about 3 hours.

## The frozen reading (proposed)

- **Question 1:** each G1-stopped invention is **availability-limited** if its inventor held it for under 13 weeks (one
  season), else **opportunity-limited** (Decision 2: 13 weeks, or 52). The reading is whichever is larger, counted only
  if the same in discovery and holdout; otherwise "both". Reported beside: how it was lost.
- **Questions 2 and 3:** described, with denominators, discovery and holdout apart; recorded causes kept apart from
  inferred explanations (GPT's point).
- Population beside every measure (rule 18). It cannot show that changing anything would help: GPT: "Don't assume G7 is
  the root cause simply because it has the lowest pass rate."

## The assistant's prior (to be frozen at sign-off; held loosely)

**Availability:** most G1-stopped inventions are made in play and dropped within weeks (forgotten as useless or pushed
out of the 12), before any talk. Composites: under 5% of talk partners know the parts. (My last three priors on this
question were wrong.)

## Afterwards (not part of CA3)

GPT's step (b): an evidence review of how real people teach multi-step crafts (apprenticeship, teaching parts in
sequence, learning without every prerequisite; living societies apart from archaeological inference), then a Law 126
proposal that can tell the **opportunity** and **prerequisite** explanations apart, with controls and frozen predictions.
GPT's warning, kept: "The danger is building a teaching system that secretly manufactures cumulative culture."

## Decisions for the creator

1. Worlds: **CA1's seeds** (recommended), or new.
2. The availability line: **13 weeks** (recommended), or 52.
3. Order: **now, on two spare workers** (recommended), or later.
4. Then the evidence review (b): **yes, after CA3** (recommended), or not yet.
