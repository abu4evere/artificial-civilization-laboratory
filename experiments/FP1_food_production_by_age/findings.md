# FP1 findings: food production by age in nature v15, against forager evidence

**Status: final.** The blind recompute (`recompute_fp1.md`, 7 November 2026, 02:39) matches. GPT and Gemini each
used code, and every point estimate agrees. DeepSeek, which has no code tool, gave a script and no numbers.

Every number is from `results.md` (analyse_fp1.py, frozen before data) on cloud run 42337207529:
- 32 worlds, seeds 24301–24332, on `code_v15`, read-only; 200 years, years 100–200 counted;
- zero checks All: PASS (`zero_local.log`; read-only; 0 conservation breaches; reload exact);
- **0 conservation breaches in every person-week of every world.**

It is a table beside the evidence. No pass/fail band was frozen (round 72).

## The answer in one line
**Three things are off against real foragers:**
1. **Children feed themselves far too early.** They reach their need at 8–11; real foragers do so in the mid-to-late
   teens.
2. **Women out-produce men.** That is the reverse of the evidence.
3. **Nobody hunts.** The hunted share of production is 0.000 against 26–78%.

**Foraging is not "too generous" over all weeks:** grown men produce about 1.10 of their need, women 1.31–1.33. The
generous part is **the yield per active week** (about 3 × need), paired with **children foraging at adult rates for
their need**.

## 1. Production ÷ need by age (all weeks; the same for both sexes until 16)
- **0–2: 0.000.** **3–7: 0.442.** **8–11: 1.207** (the crossover). **12–15: 1.101.**
- **Women:** 16–29 1.192; 30–39 **1.333 [1.323, 1.341]**; 40–49 1.312; 50+ 1.053.
- **Men:** 16–29 1.098; 30–39 **1.105 [1.103, 1.107]**; 40–49 1.097; 50+ 1.054.
- **Evidence (Kaplan et al. 2000, read in full):** "no children in any forager society produced as much as they
  consumed until they reached their mid- to late teens"; grown men produce 1.37–3.22 times per-capita intake, women
  0.39–1.64 (the assistant's arithmetic from Tables 2 and 3).
- **Two caveats:** ACL's need is a fixed requirement, and Kaplan's per-capita intake counts children as full consumers.
  So only the shape and direction compare, not the level. **The shape is wrong in two places:**
  - the crossover comes about 6 years early;
  - the sexes are reversed. ACL has no division of labour.

## 2. Prime adults: all weeks against active weeks
| band, sex | all weeks | per active week | share of weeks active |
|---|---|---|---|
| 30–39 women | 1.333 | 2.931 | 0.453 |
| 40–49 women | 1.312 | 2.962 | 0.442 |
| 30–39 men | 1.105 | 3.010 | 0.367 |
| 40–49 men | 1.097 | 3.018 | 0.363 |

- **Per active week, both sexes gather about 3 times their weekly need. Women are simply active more often.**
- Grown people spend their other weeks gathering materials (24%), setting things down (12%), talking (10%), giving
  (8%) and joining others (6%).

## 3. Hunting
- **Hunted share of production: 0.000** (to 3 decimals).
- Hunting was chosen in **1,880 of 17,174,461 grown weeks** (about 1 in 9,100), though offered in 234,520.
- **2,092 hunts:** every one solo, 99 successful.
- Forage was offered in 12,414,127 grown weeks and chosen in 6,759,339.

## 4. Losses, and where children's food comes from
- **Rot:** about 7.5% of production, at every age.
- **Unmet need:** 0.8–3.1% of need, highest at 0–2 (3.1%).
- **Children under 16 get 67.6% of their food from their own foraging,** 22.4% from being fed by carers, and 10.0%
  from gifts.
- **Evidence:** by 15, forager children had eaten over 25% of their lifetime food but gathered under 5% of it (Kaplan
  et al. 2000).

## Against the assistant's prior (questions.md)
| prior | result |
|---|---|
| prime adults' production ÷ need about 1–2 | yes (1.10–1.33) |
| no sex difference | **no**: women 1.31–1.33, men 1.10, because women are active more weeks |
| about 3 per active forage-week | **yes** (2.93–3.02) |
| children produce little | **no**: 3–7 already 0.44; 8–11 above need |
| hunted share under 1% | yes (0.000) |
| reading most likely "hunting the gap" | partly: hunting is the largest gap, but children's early self-sufficiency is a second, separate one |

## What it suggests for HR1 (for the council; nothing decided)
- **Hunting is the largest gap.** The decision almost never picks it (1 in about 9,100 grown weeks), and when picked it
  pays little (HN1).
- **A second gap: children's foraging.**
  - Children forage at 0.4 of the adult rate, and teens at 0.8 (`mind.forage_rate`).
  - A child's need is 4 a week against an adult's 7, so a child's foraging week still covers about two weeks of
    need. Children also forage often, so 8–11-year-olds pass their need.
  - Real children gather far less relative to what they eat: smaller bodies, less skill (Koster: skill rises
    through adolescence), more play.
  - Whether the 0.4 and 0.8 factors, or the child need, are off is a calibration of existing physics against
    evidence, not a new law.
- Foraging per active week (3 × need) may also be high. But over all weeks the grown produce only 1.1–1.3 × need,
  because they do many other things. So "foraging too generous" is **not** clearly the problem for adults.
