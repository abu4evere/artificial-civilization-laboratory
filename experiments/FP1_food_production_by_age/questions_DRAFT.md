# FP1: food production by age in nature v15, against forager evidence (DRAFT for council round 72; not frozen)

**A read-only study,** HR1's step 0 (`docs/research/forager_production_2026-11-06.md`). It asks which side is off:
foraging, hunting, or the weekly action budget. It comes before any hunting calibration. Nothing in nature changes.

## Question
In v15, how much food does a person acquire per week, by age band, sex and source, against what they need? How do
the grown spend their weeks? How do these compare with forager net-production curves (Kaplan et al. 2000) and the
hunted share of forager energy (about 60%)?

## Design
- **Code:** `code_v15`, unchanged; one arm, no sham (nothing is changed). LP; **32 new seeds 24301–24332**; 200 years;
  years 100–200 counted.
- **A read-only observer.** Every person-week, by age band (0–2, 3–7, 8–11, 12–15, 16–29, 30–49, 50+) and sex, it
  records:
  - food acquired by source: forage (`got`), hunt (meat ÷ party size), taken from one's own stash, taken from
    another's stash, stolen, received as a gift, inherited;
  - food given away;
  - need (`Person.need`);
  - the week's action (`p.doing`).
- **The zero checks:** the observer is read-only (hashes with and without it); the sum of sources equals an independent
  count from the events; reload is exact.

## Measures (all with population beside them)
1. **Net production by age band:** (forage + hunt) − need, per person-week, and the ratio (forage + hunt) ÷ need, by
   sex. This is the curve Kaplan et al. draw.
2. **Prime adults (30–49):** production ÷ need over all weeks, by sex.
3. **The hunted share** of all food acquired.
4. **The action budget** of the grown: the share of weeks per action (forage, hunt, make, rest, talk, …).
5. **Per active week:** food per forage-week and per hunt-week (as HN1), by age.

## Reading (to be fixed at the freeze, from evidence read in full)
FP1 describes; it does not decide a law. Its frozen output is a table beside the evidence. The council then decides
HR1's calibration target:
- **foraging too generous:** prime adults' production ÷ need well above the forager range;
- **hunting the gap:** production is in range, but the hunted share is near 0;
- **the action budget:** returns per active week are in range, but the time spent is not.

The evidence bands are fixed from sources read in full before the freeze. Kaplan et al. 2000 is so far known only
from search summaries; its PDF is a file download, and the creator has been asked.

## Prior (the assistant)
Prime adults' production ÷ need over all weeks is about 1–2. Foraging per active week is high, but people forage few
weeks. Hunting's share is under 1%. The gap is mostly hunting, about 70%.
