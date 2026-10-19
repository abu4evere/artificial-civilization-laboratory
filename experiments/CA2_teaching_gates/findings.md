# CA2 — Why does teaching pass on so little? Findings

Frozen as `CA2-frozen` (signed off by the creator, all recommendations; GPT's six refinements part of the design).
Read-only: a logging copy of nature v2, shown to change nothing; CA1's 32 worlds replayed, **every replay ending in
CA1's saved state**. Table: `results.md`, from `analyse_ca2.py`. **Valid:** zero check, all 32 worlds, replays exact, one
fingerprint, 0 unmatched log records (2.5 million records).

## The gates, for useful inventions never passed on (5,138 discovery / 4,853 holdout)

| gate | pass rate, discovery | holdout | stopped here for good, discovery | holdout |
|---|---|---|---|---|
| **G1 meets** (the inventor teaches-talks with anyone while knowing it) | 0.539 | 0.541 | **2,370 (46%)** | **2,229 (46%)** |
| G2 valued (above 0.15 to the inventor) | 0.326 | 0.283 | 1,866 (36%) | 1,882 (39%) |
| G3 offered (top three) | 0.905 | 0.930 | 86 | 52 |
| G4 chosen | 0.958 | 0.946 | 34 | 37 |
| G5 new to the learner | 1.000 | 1.000 | 0 | 0 |
| G6 believed | 0.848 | 0.855 | 119 | 95 |
| **G7 followable** (the learner can make its made parts) | **0.012** | **0.005** | 655 (13%) | 555 (11%) |

## The frozen reading

**Most stopped at G1, "meets", in both sets; the lowest pass rate was elsewhere: G7, "followable", in both sets.** By the
rule fixed before data, that is not "one bottleneck": the largest loss and the narrowest gate are different gates, and
both repeat.

1. **The largest loss is before any teaching (G1–G2):** for 46% of the useful inventions never passed on, the inventor
   never took part, as teacher, in a talk where teaching could happen while knowing it; for another 36–39%, they did,
   but never valued it enough to offer it (above 0.15). Together, **over four in five losses happen before anything is
   shown.**
2. **The narrowest gate is G7:** of the inventions that were offered, chosen, new and believed, **only 1 in 80
   (discovery) and 1 in 200 (holdout) could be followed**, because they need a made part the learner cannot make. A
   composite can be taught only to someone who already knows how to make its parts, and almost no one does.
3. **Teaching itself, once a thing is shown, mostly works:** offered 91–93%, chosen 95–96%, believed 85%.

## The assistant's prior, against the result

| prior (frozen) | result |
|---|---|
| blocking gate G3, offered | **wrong**: G3 passes 91–93% |
| second guess G6, believed | **wrong**: 85% pass |
| question 2: most building on (over half) is the inventor's own work | **wrong as stated**: the inventor 42–43%; but a learner who had learned the part only 4–5% |

The third wrong prior in a row in this line (CA1, CA2 twice); kept as wrong.

## Described

- **Who built on what (CA1's link-5 pairs):** the inventor **42% / 43%**; a learner who had learned the part **4% /
  4%**; unclear (the builder had the part but no record of learning it, for example given or found as a thing) **54% /
  54%**. Passed on afterwards: 8% / 6% overall. **Building on something learned from someone else is rare**, the
  missing step of cumulative culture.
- **Kept a year (G8):** 97% of learners kept what they learned for a year (died 2%; pushed out by the 12-recipe limit
  1%). Retention after learning is not the problem.
- **Watching, for the same inventions:** in 65% / 72% of watching chances the person watched did not know the recipe
  themselves (they held the thing, not the know-how); in 33% / 26% the small chance of noticing failed.
- Population (rule 18): median 24–42 (discovery) and 21–29 (holdout) living people per decade.

## Caveats

1. G1 counts talks in which teaching could happen (learner aged 4 or more); an inventor who knew a thing only briefly
   (pushed out of their own 12, or died soon) has few chances. How long inventors held their inventions was not
   measured.
2. G2's 0.15 is the code's threshold on the inventor's own felt value; what makes that value low was not measured.
3. The gates are sequential; a later gate's pass rate is among the few that reached it (G7: 663 and 558 inventions).
4. As GPT put it: "identifying a gate associated with failure does not prove that changing it would increase cumulative
   culture." That needs a separate, frozen intervention.

## What it suggests (for the creator; nothing changed)

Two separate obstacles, one large and one narrow:

- **Large: most inventions never reach a lesson** (inventors meet no one to teach while knowing it, or do not value it).
  A read-only next step: how long inventors hold their inventions, and how often an inventor and a possible learner meet.
- **Narrow, and structural: composites cannot be taught to someone who cannot make the parts.** This is the step where
  culture would build on itself, and it almost never passes. A candidate for a frozen study under Law 126: whether a
  lesson can include the parts (teaching the chain, not just the last step), as real apprenticeship does. Evidence on
  how real people teach multi-step crafts would come first.
