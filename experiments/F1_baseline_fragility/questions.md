# F1 — Baseline fragility: why do control worlds die out? (read-only; questions frozen before any data)

**Asked by the creator (October 2026), after U stopped at its pilot:** "Before introducing new weather systems,
ownership systems, or storage incentives, run a read-only investigation into baseline fragility. ... No fixes, no
tuning, no code changes. First identify the mechanism."

**Read-only.** No change to ACL's code or settings. An observer records what happens; it is shown not to change the
world (state hash with and without it). Replays must reproduce the saved populations exactly, or the study stops.

## The worlds

**Discovery set: the 40 control worlds already run** with the same code (`E13R_replication/code_e13r`, A2-full,
`anticipation_weight=1.0`, all other settings default, 120 years), whose populations per decade are saved:

| source | seeds | died out (saved) |
|---|---|---|
| E13R arm `zero` | 501–516 | 2 of 16 |
| L1 arm `c` | 601–616 | 6 of 16 |
| U pilot arm `c` (code_u at defaults, shown identical to E13R's code by U's zero check) | 811–818 | 4 of 8 |
| **all** | 40 | **12 of 40 (30%)** |

(The "half" that prompted F1 was the U pilot's 4 of 8; across all 40 controls it is 30%. Both are reported.)

**Holdout set: 24 new seeds, 1101–1124**, run only after the discovery analysis is written up and committed. Any
signature or early-warning sign found in discovery is called "recurring" only if it also holds in the holdout.

## Questions (the creator's, verbatim, with how each is answered)

1. **Why do control worlds die out?** Births fall short of deaths. Decompose: compare births per woman-year (16–45) and
   deaths per person-year, by cause and by stage, between worlds that die out and worlds that survive, over the whole
   run and in the decades before extinction.
2. **What is the most common path to extinction?** Each extinct world is classified by the rule below (fixed now).
3. **Is it starvation, fertility collapse, aging, child mortality, lack of carers, resource depletion, or something
   else?** Each candidate is measured as below; the answer is the one(s) the data show, including "something else".
4. **Can extinct worlds be identified decades before collapse?** At years 20, 30 and 40, for worlds alive then and,
   if they die, dying at least 20 years later: how well each pre-stated indicator separates future-extinct from
   surviving worlds (rank AUC: the chance a random future-extinct world scores worse than a random survivor).
   "Identifies" means AUC ≥ 0.80 in discovery **and** ≥ 0.70 in the holdout.
5. **Are there recurring signatures shared by most failed worlds?** A signature is "shared" if present in at least two
   thirds of extinct worlds and at most one third of survivors, in discovery, and "recurring" if that also holds in
   the holdout.

## What the observer records (each year unless stated)

- Population by stage (infant <1, child <12, teen <16, adult <50, elder) and sex.
- Births; deaths by recorded cause (starvation, thirst, cold, neglect, illness, old age, childbirth, killed, mauled,
  other) and stage of the dead; pairings.
- **Reproduction, every week, for each woman aged 16–45** (the code's own conditions for conception, re-evaluated
  without drawing any random number): pregnant; else the first blocking condition in the code's order: no partner;
  partner dead; apart (beyond camp radius); her health < 50; starving; partner under 12; nursing; else **eligible**.
- **Mate supply, yearly:** unpartnered women 16–45, and for each the number of unpartnered adult men within 15 years of
  her age and not kin by the code's rule (mate-eligible men), anywhere in the world and within perception range.
- Food: mid-autumn plant food per land tile and per person; share of person-weeks starving; mean health.
- Children under 6 without a caregiver (person-weeks); carers per dependant.
- Spread: number of separate groups (people within camp radius chained together) and mean distance to the nearest
  other adult.
- Mean genes of the living (drift).

## Candidates (Q3), each with its measure

| candidate | measure |
|---|---|
| starvation | share of deaths by starvation (and thirst, cold) |
| fertility collapse | births per woman-year 16–45; weekly breakdown of why women do not conceive |
| aging | share of deaths by old age; share of population over 50; mean age |
| child mortality | share of births dying before 12 |
| lack of carers | neglect deaths; caregiver-less child-weeks |
| resource depletion | mid-autumn food per land tile over time, in extinct vs surviving worlds |
| something else | mate supply (no partner / no eligible mate), spread, violence, sex ratio, drift |

## Path classification (Q2), fixed now

For each extinct world: **E** = last year anyone is alive; **B** = year of the last birth; **F** = last year with a
woman aged 16–45 alive.

- **Crash:** more than half of the deaths in the ten years before E are from starvation, thirst or cold.
- **Reproductive failure, then ageing out:** not a crash, and E − B ≥ 15. Sub-typed by the most common blocking
  condition among women 16–45 in the ten years before B (no partner / apart / health / starving / nursing / etc.), and
  by whether a woman 16–45 was alive with **no** mate-eligible man in the world for most of those years (mate shortage).
- **Attrition:** neither (births continue almost to the end while deaths outrun them).

## Pre-stated early-warning indicators (Q4)

Population; women 16–45; adult sex ratio (men ÷ women); births per woman-year in the past decade; share of person-weeks
starving in the past decade; mid-autumn food per land tile; share of women 16–45 unpartnered; share of unpartnered
women with no mate-eligible man in the world; number of groups. No other indicator is called a predictor; any found
later is labelled exploratory.

## Hard stops

- A replay does not reproduce its saved populations per decade: stop, report, no outcomes read.
- The observer changes the world (state hash differs with and without it over 20 years, two seeds): stop.
- The code fingerprint changes during runs: stop.
