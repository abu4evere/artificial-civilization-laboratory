# How long do ACL people live under nature v9? (read-only count, 30 October 2026)

**Descriptive, not a frozen study.** 6 throwaway seeds (30001–30006), LS2's own world (LP: 80 founders, 80 × 80,
`code_v9` with v9's settings), 150 years each, every death event recorded by a wrapper on `world.emit` (read-only).
Script: `acl_lifespan_v9/lifespan_v9.py`; full output: `acl_lifespan_v9/summary.txt`. Asked for by the creator's ageing
idea ("humans used to live longer ... we should do same with acl", 30 October), and by the SA1 evidence note's "measure
first" step (`experiments/SA1_sensitivity/evidence_mortality.md`).

**Population:** all 6 worlds alive at year 150. The cohort: world-born people born in years 0–50, **1,314 people, all
followed to death** (none still alive at year 150).

## Results
- **Mean age at death (= life expectancy at birth for this cohort): 33.4 years;** median 35.2.
- Died before 1: 0.052; before 5: 0.134; **before 16: 0.235.**
- **Of those who reached 16 (1,005): mean age at death 42.0, median 43.0; oldest 75.1.** Share of adult deaths at 45+:
  0.451; at 60+: **0.113**; at 70+: **0.010**; none at 80+.
- Causes of adult (16+) deaths: illness 0.38, old age 0.32, starvation 0.18, thirst 0.09, childbirth 0.02, killed 0.01.
  Under 16: starvation 0.46, thirst 0.27, illness 0.13, neglect 0.12, killed 0.02.
- Period check: all world-born deaths in years 100–150 (all 6 worlds): 1,357, mean age 38.2, median 40.8.

**Deaths per person-year by age (all causes), the cohort:**

| age | deaths / person-years | rate | forager total (SA1 note) |
|---|---|---|---|
| 0–1 | 68 / 1,280 | 0.053 | |
| 1–5 | 108 / 4,743 | 0.023 | |
| 5–15 | 123 / 10,699 | 0.012 | |
| 15–30 | 268 / 13,358 | 0.020 | |
| 30–45 | 294 / 9,105 | 0.032 | 0.018 at 40 |
| 45–60 | 339 / 4,196 | 0.081 | 0.039 at 60 |
| 60–70 | 104 / 475 | 0.219 | |
| 70+ | 10 / 27 | 0.366 | |

## Reading
1. **ACL's adults die far too early.** From 30 on, ACL's death rates run from about 1.8 times the forager total (ages
   30–45 against foragers at 40) to more than 5 times (ages 60–70 against foragers at 60); only 11% of adult deaths
   come at 60 or later, and almost nobody reaches 70.
2. **ACL's children die less than the adults' excess would suggest:** 23.5% die before 16. (The forager comparison for
   children needs the full Siler fits; not done here.)
3. **Ageing causes most adult deaths:** "illness" and "old age" together 0.70 of adult deaths. (In the code, "illness"
   mixes the ageing draw before the elder stage with sickness that runs health down; both rise with age through the
   ageing draw, frailty and falling maximum health.)
4. **What it bears on:** LS1 and LS2 find 98% of lost knowledge is lost at death. If adults die about 20 years too
   early, holders of skill and know-how die before they can pass it on.

**Not data for any study's question.** A frozen study (the ageing anchor) would measure this on fresh seeds.
