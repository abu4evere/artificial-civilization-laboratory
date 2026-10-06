# F1 — Baseline fragility: findings (discovery confirmed on the holdout)

Read-only. Questions frozen as `F1-questions`. Discovery: the 40 saved control worlds (`results_discovery.md`,
`findings_discovery.md`, all 40 replays reproduce their saved populations). Holdout: 24 new seeds 1101–1124
(`results_holdout.md`), run after the discovery write-up was committed. Observer read-only, code unchanged, in both.
Leads: `leads_discovery.md`, `leads_holdout.md`; exploratory numbers: `explore_discovery.md`, `explore_holdout.md`.

**Population beside every measure (rules 14, 18):** died out 12 of 40 (discovery), 10 of 24 (holdout), **22 of 64
(34%)** overall, between years 53 and 116. Peak population, extinct vs surviving worlds (median): 27.5 vs 42 (discovery),
25.5 vs 47 (holdout).

## The five questions, confirmed

**1. Why do control worlds die out?** **Births stop decades before the end, and the people left grow old.** The last
birth came 40–65 years before extinction in all 22 extinct worlds (median about 52 in both sets). In the 30 years before
extinction there were no births at all. Mean age in the last decade: 54 (discovery), 52 (holdout), against about 22 in
survivors. Old age is about half of the deaths in the last 20 years.

**2. The most common path:** **reproductive failure, then ageing out: 18 of 22** (10 of 12; 8 of 10). The other four
were labelled "crash" by the frozen rule, on 1–3 deaths in their last decade; in every one, births had already stopped
41–54 years earlier. **In substance, all 22 aged out after births stopped.** (The labels stand as the rule gave them;
this reading is noted beside them.)

**3. Which candidate?**

| candidate | verdict | discovery | holdout |
|---|---|---|---|
| starvation | **not the cause** | starving share 0.033 extinct vs 0.037 survivors | 0.030 vs 0.037 |
| resource depletion | **no** | autumn food per tile at year 40: 25.4 vs 24.4 | 25.4 vs 23.9 |
| lack of carers | **no** | children under 6 without a carer: 0.000 of person-weeks | 0.000 |
| aging | **the end stage, not the cause** | old age 48–56% of deaths only after births stop | 50–60% |
| child mortality | **a contributor, early** | child deaths per birth 0.37 vs 0.17 (whole run) | 0.34 vs 0.20 |
| fertility collapse | **the proximate cause** | births 0 for the last 30+ years | the same |
| **no partner** | **the mechanism of the fertility collapse** | women 16–45 with no partner: 67% of weeks vs 55%; **100%** in the 30 years before extinction | 71% vs 51%; **100%** |

**4. Early warning (frozen rule: AUC separation ≥ 0.80 in discovery and ≥ 0.70 in the holdout):**

| year | indicator | discovery | holdout | identifies? |
|---|---|---|---|---|
| 20 | population | 0.85 | 0.91 | **yes** |
| 20 | women 16–45 | 0.78 | 0.96 | no (discovery below 0.80) |
| 30 | population | 0.95 | 0.94 | **yes** |
| 30 | women 16–45 | 0.91 | 0.92 | **yes** |
| 30 | share of women 16–45 unpartnered | 0.98 | 0.91 | **yes** |
| 40 | population; women 16–45 | 0.97; 0.94 | 0.97; 0.93 | **yes** |
| 40 | births per woman-year, past decade | 1.00 | 0.81 | **yes** |
| 40 | share of women 16–45 unpartnered | 0.96 | 0.82 | **yes** |

Food, starvation, mate shortage in the world as a whole and group count do not identify them in both sets. **Yes:
extinct worlds can be identified decades before collapse**, already at year 20 by population alone (33 to 96 years
before extinction).

**5. Recurring signatures (≥ 2/3 of extinct and ≤ 1/3 of survivors, in both sets):**
- **G1 population below the 20 founders at year 30:** 11 of 12 vs 2 of 28; 8 of 10 vs 1 of 14. **Recurring.**
- **G7 at most three women of childbearing age at year 30:** 9 of 12 vs 3 of 28; 7 of 10 vs 0 of 14. **Recurring.**
- G5 (low births per woman-year in years 0–29) held in the holdout only (8 of 10 vs 4 of 14; discovery 7 of 12 vs
  13 of 28): **not recurring.** Sex imbalance, starvation, isolation, mate shortage in the world: not shared.

## The leads (written before the holdout data; rule 15)

| lead | discovery | holdout | status |
|---|---|---|---|
| L1 births stop ≥ 15 years before extinction in ≥ 2/3 of extinct worlds | 12 of 12 | 10 of 10 | **confirmed** |
| L2 (as written) ≥ 80% of all single-woman-years with no eligible man in sight, < 25% none in world | 59%, 13% | 62%, 13% | **failed in both, as written** |
| L3 more child deaths per birth in years 0–9 in extinct worlds | 0.385 vs 0.252 | 0.298 vs 0.212 | **confirmed** |
| L4 pairing collapses after the founders' decade in both kinds of world | 0.035 → 0.008 / 0.003 | 0.037 → 0.009 / 0.003 | **confirmed** |

L2 failed because it was written for all worlds; the corrected reading (`findings_discovery.md`, correction) is about
small worlds, and the holdout repeats it closely (`explore_holdout.md`): single women had no eligible man within sight
in **98%** of single-woman-years in extinct worlds (discovery 97%), **86%** in survivors' first 40 years (87%), and
**42%** in survivors' later years (44%). An eligible man existed somewhere in the world in most of those years (none
anywhere in 19% (discovery) and 32% (holdout) of extinct worlds' single-woman-years, 8–13% in survivors'). That corrected reading was formed after
discovery and repeated in the holdout, but it was not a pre-written lead: it is **reported as consistent, not
confirmed** (rule 15).

## Mechanism (confirmed parts in bold; the rest consistent but not separately confirmed)

1. **Pairing happens mostly in the founders' first decade** (about 0.035 pairings per person-year), then falls to a
   quarter or less in every world (L4).
2. In the code, a single adult courts only people within sight (4 tiles), joins someone within 6, or else takes a random
   step of a few tiles, on a 40 × 40 world (`mind.py`, `seeking`). In small worlds, single women almost never have an
   eligible man within sight, though one usually exists elsewhere (consistent in both sets).
3. **Worlds that die lose more children early** (L3), and are already **smaller at year 20** (Q4), with **few women of
   childbearing age by year 30** (G1, G7).
4. **Births then stop, 40–65 years before extinction, and the world ages out** (L1, Q1, Q2), with fertile women still
   alive, single, for decades.
5. Starvation, food on the land and care of children do **not** distinguish dying worlds (Q3, both sets).

**In one sentence:** ACL's control worlds die out not from hunger but from failed pairing: after the founders, people
rarely find a partner, because in a small and scattered population a partner is almost never within sight; worlds that
lose more children early fall below the size where chance meetings keep pairing going, births stop, and the people age
out over half a century.

## Limits

- 64 worlds, one code, one map size, founders 20, 120 years. Other sizes untested.
- The blocking conditions are re-evaluated at the end of each week, not at the moment the code checks them.
- "Within sight" uses perception (4 tiles); the code's join radius is 6. The early-warning AUCs are on 22 extinct worlds.
- Read-only: this shows what happens and where in the code it comes from, not what would happen if it were changed.

## What follows (no fix proposed; the creator decides; rules 12 and 17 apply)

The mechanism lies in nature (how far people search for partners, and the world's size against its founders), not in
culture. Any change must be anchored to evidence on how real foragers find partners (rule 17) and checked for feasibility
read-only first (rule 12), not widened until worlds survive. Every experiment that reads surviving worlds should report
that about a third of controls die out (rule 14).
