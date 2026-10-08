# N7 — Evidence: K2 (a camp that goes where the couple goes) and K1 (co-residence at the scale of a week)

**Written:** October 2026. Questions and anchor criteria: `questions.md` (committed before any search). **No code, no
experiment, no choice.** "Abstract read" = the abstract read in full (OpenAlex); "summary read" = full text read through a
page-summary tool; "record only" = bibliographic record and secondary snippets.

## Sources

**Camps move, and why**
- **Kelly, R. L. (1983).** Hunter-gatherer mobility strategies. *Journal of Anthropological Research* 39(3)
  ([doi](https://doi.org/10.1086/jar.39.3.3629672); **abstract read**). Whether a group emphasises residential moves
  (the whole camp) or logistical ones (task groups out from a base) is closely related to the structure of resources in
  its environment. (Secondary report, **record only**: the tropical Punan made 45 residential moves a year, 8.5 km each.)
- **Binford, L. R. (1980).** Willow smoke and dogs' tails. *American Antiquity* 45 ([doi](https://doi.org/10.2307/279653);
  **abstract read**). Two organisations: "mapping-on" (moving the residence to the resources) and "logistics" (task groups
  from a base), each answering different environmental problems.
- **Venkataraman, V. V., Kraft, T. S., Dominy, N. J. and Endicott, K. M. (2017).** Hunter-gatherer residential mobility
  and the marginal value of rainforest patches. *PNAS* 114 ([doi](https://doi.org/10.1073/pnas.1617542114); **abstract
  read**, opening truncated in the record): Batek foragers of Malaysia over 93 days and 11 residential camps; **camp
  residence times conformed to the marginal value theorem**: camps were left as local returns fell, "communal
  perceptions of resource depletion are closely linked to collective movement decisions."
- **Hamilton, M. J. et al. (2016).** The ecological and evolutionary energetics of hunter-gatherer residential mobility.
  *Evolutionary Anthropology* 25 ([PMC5094510](https://pmc.ncbi.nlm.nih.gov/articles/PMC5094510/); **summary read**):
  residential moves are driven by local patches becoming depleted; average residential distance about 158–174 km a year
  across ethnographic samples; mobility is a large part of the energy budget.

**Returning to the camp each day**
- **Garg, K. et al. (2021).** *Royal Society Open Science* 8 (**abstract read**; carried from N6): central-place foraging,
  returning to a central location, is a key feature of hunter-gatherer social organisation; foragers forage near home or
  move home to new areas.
- **Kelly, R. L. (2013).** *The Lifeways of Hunter-Gatherers* (**record only**, secondary summaries): daily movement out
  for food and back to camp before dark, as distinct from moving camp.
- **Wood, B. M., Harris, J. A., Raichlen, D. A. and Pontzer, H. (2021).** Gendered movement ecology and landscape use in
  Hadza hunter-gatherers. *Nature Human Behaviour* 5 ([doi](https://doi.org/10.1038/s41562-020-01002-7); **abstract
  read**): 2,078 person-days of GPS tracks; men walked further per day, explored more land and were more often alone.
  (That people occasionally stayed out overnight, to hunt at night or visit another camp, is **record only**, from a
  search snippet.)

## Answers

1. **Camps move**, many times a year in most foraging societies, more often where resources are spread and accessible
   (Kelly 1983; Binford 1980); one record gives 45 moves a year (record only).
2. **Daily foraging is out from camp and back.** Men range further and more often alone than women (Wood et al. 2021).
   No source read gives a ratio of daily range to camp-move distance that could be carried into ACL, which has no scale.
3. **Camps move when local returns fall:** shown directly for the Batek (Venkataraman et al. 2017: marginal value
   theorem) and stated as the general driver (Hamilton et al. 2016). This is the piece HB1 lacked.
4. **Spouses who forage apart by day sleep in the same camp** as the general pattern of central-place foraging (Garg et
   al. 2021; Kelly 2013, record only).
5. **Overnight separations** exist (night hunts, visits) and are occasional; **no rate was read**.
6. **No scale-free relation** was found that maps "a day's range" onto ACL's tiles. ACL's `reach` (3 tiles a week) is
   the code's own travel unit, not a value the evidence supplies.
7. **Nature or culture:** returning to a central place and moving it when returns fall are species-typical foraging
   behaviour (central-place foraging; marginal value); *how* a camp decides to move (Batek deliberation and argument) is
   social, and is not to be written.

## Against the anchor criteria (written before the search)

| | criterion | verdict |
|---|---|---|
| **K2** | foragers return to a central place most nights **and** the central place moves with foraging, in a range of societies | **anchored**: return to a central place (Garg 2021; Kelly 2013, record only); camps move as local returns fall (Venkataraman 2017; Hamilton 2016; Kelly 1983; Binford 1980) |
| **K1** | partners foraging within a day's range share a camp at night as a general pattern, **so that the weekly co-residence rule follows from the evidence rather than from births** | **not anchored**: the pattern (spouses share a camp at night) is general, but nothing in the evidence turns "a day's range" into a number of ACL tiles; counting partners within 3 tiles as co-resident would rest on choosing a threshold, and that choice would act directly on births. **K1 is dropped.** |

## What this means for K2's design (for the creator; nothing chosen)

- K2's core is supported: **couples end each week together, at a place that moves with their foraging.** HB1's failure
  is consistent with the evidence: a central place that does not move when returns fall is not what real foragers have.
- **A feasibility fact already in the record (C1, read-only):** in the control worlds, couples are beyond `reach` (more
  than 3 tiles apart) in 29.0% of couple-weeks in C1's discovery and 27.6% in its holdout (computed from C1's saved
  counts).
  A K2 that reunites only partners within `reach` could bring together at most the other ~71%.
- Open design questions for sign-off: where the couple meets (one partner's position, the midpoint, the better-fed
  tile), with no random draw; whether the meeting also uses the evidence that camps move as returns fall (it does by
  construction, since the camp is wherever they foraged); and, from T1 and HB1, a sham arm, a paired test, and HF4's
  ledger measured from the start.
