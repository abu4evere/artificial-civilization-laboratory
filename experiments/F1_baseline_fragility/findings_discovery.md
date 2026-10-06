# F1 — Baseline fragility: discovery findings (40 control worlds; holdout not yet run)

Read-only. Frozen questions: `questions.md` (`F1-questions`). Full generated tables: `results_discovery.md`. All 40 replays
reproduce their saved populations exactly; the observer is read-only; the code was unchanged. **Population beside every
measure:** 12 of 40 worlds died out (years 53–105); peak population median 27.5 (extinct) vs 42 (survivors).

Parts marked **exploratory** were read after the frozen analysis, from the same recorded data (nothing re-run); they
are leads for the holdout, not findings.

## Answers to the five questions (frozen measures)

**1. Why do control worlds die out?** Because **births stop decades before the end**. In every extinct world the last
birth came 40–61 years before the last death (median ≈ 52). In the 30 years before extinction there were **no births at
all**, while deaths ran at 0.06 a person-year rising to 0.14. The people who remain simply grow old: mean age 34 over
the whole life of an extinct world, 54 in its last decade (survivors: 22), and old age is about half of the deaths in
the last 20 years. The worlds do not fall; they **stop renewing and age out**.

**2. The most common path:** **reproductive failure, then ageing out: 10 of 12.** The other 2 were classified "crash"
by the frozen rule, but on 2 and 3 deaths in their last decade; in both, births had stopped 41 and 54 years earlier, so
they also aged out (the label follows the rule; the reading is noted here).

**3. Which candidate?**

| candidate | verdict | evidence (extinct vs surviving worlds) |
|---|---|---|
| starvation | **not the cause of extinction** | share of person-weeks starving the same (0.033 vs 0.037); starvation does kill children (below) |
| fertility collapse | **yes, as the proximate cause** | births per woman-year 0 for the last 30+ years |
| aging | **the end stage, not the cause** | old age dominates deaths only after births stop |
| child mortality | **a contributor, early** | child deaths per birth 0.37 vs 0.17 over the whole run; 0.39 vs 0.25 already in years 0–9 |
| lack of carers | **no** | children under 6 without a carer: 0.000 of person-weeks in every group; neglect a few % of deaths |
| resource depletion | **no** | autumn food per land tile the same or higher in failing worlds (25.4 vs 24.4 at year 40) |
| **something else: no partner** | **yes, the mechanism of the fertility collapse** | women 16–45 in extinct worlds spent 67% of their weeks with no partner (survivors 55%), and **100%** in the 30 years before extinction |

**4. Can extinct worlds be identified decades before collapse?** **Yes, in discovery** (to be confirmed in the holdout):

| year | indicator | AUC separation |
|---|---|---|
| 20 (33–85 years before extinction) | population | 0.85 |
| 30 | population; women 16–45; share of women unpartnered | 0.95; 0.91; **0.98** |
| 40 | population; women 16–45; births per woman-year; share unpartnered | 0.97; 0.94; 1.00; 0.96 |

Food, starvation, sex imbalance, mate shortage in the world and group count do **not** separate them (0.51–0.67).

**5. Shared signatures** (≥ 2/3 of extinct, ≤ 1/3 of survivors), first 30 years: **G1 population below the 20 founders
at year 30** (11 of 12 vs 2 of 28) and **G7 at most three women of childbearing age at year 30** (9 of 12 vs 3 of 28).
Not shared: sex imbalance, starvation, early fertility, isolation, mate shortage in the world.

## The mechanism (exploratory: from the recorded data and the code, read-only)

1. **Pairing happens almost only among the founders.** Pairings per person-year: 0.035 in years 0–9 in both kinds of
   world, then about 0.005 everywhere afterwards. The first generation pairs where it starts; later generations rarely
   do.
2. **Mates are found only within sight.** In the code, a single adult courts only people within perception (4 tiles);
   with no one eligible in reach, they "join" someone within 6 tiles, or else take a random step of a few tiles
   (`mind.py`, `seeking`). The world is 40 × 40 (1,600 tiles) on a torus.
3. **Single women almost never have an eligible man within sight**, in any world: 3,125 of 3,601 single-woman-years in
   survivors' first 40 years, 1,547 of 1,587 in extinct worlds. Yet an eligible man (unpartnered adult, not kin, within
   15 years of age) **exists somewhere in the world** in most of those years (no eligible man anywhere in only 402 and
   304 of them). The shortage is **local, not global**: the partners exist but are not met.
4. **What tips a world:** extinct worlds lose more children early (child deaths per birth 0.39 vs 0.25 in years 0–9,
   mostly starvation and thirst) and so raise a smaller next generation (population at year 20: 17 vs 28). Fertility per
   woman is the same in the first decade (0.21 vs 0.22). A small cohort, scattered over a large world and searching only
   within sight, mostly never pairs; when the founders' pairs age past 45 births end, and the world ages out over the
   next half-century, with fertile women still alive and single for decades (e.g. seed 817: 168 woman-years after the
   last birth, 166 of them single).
   **Correction (found by the leads check, before any holdout data):** point 3 first said this held "in any world".
   It does not. Over all years, single women had no eligible man within sight in 97% of single-woman-years in extinct
   worlds (median population 10), 87% in survivors' first 40 years (median 27), but **44%** in survivors' years 40–119
   (median 34). Mates come within sight once a world is large enough; the claim is about small worlds. Lead L2 in
   `leads_check.py` was written with the wrong all-world threshold and fails on discovery itself (59%); it is kept
   unchanged and reported as failed, not re-tuned.
5. **Survivors are not better at pairing;** they are larger, so more of their few pairings happen, and their children
   pair into a bigger pool. The same search rule operates in every world; size decides whether it is enough.

**Sentence, held until the holdout:** ACL's control worlds die out because, in a sparse world, the generations after the
founders rarely find partners within sight; worlds that lose more children early fall below the size at which chance
encounters keep pairing going, births stop, and the population ages out over about fifty years. Starvation, food and
carers are not the cause.

## Next, frozen order

Holdout seeds 1101–1124 (`run_f1.py holdout`, then `analyse_f1.py holdout`). Recurring only if: Q4 indicators AUC ≥ 0.70;
signatures G1 and G7 again ≥ 2/3 of extinct and ≤ 1/3 of survivors; and (exploratory leads, tested descriptively) births
stopping ≥ 15 years before extinction in most extinct worlds, and single women mostly without an eligible man within
sight while one exists in the world. No fixes are proposed here; that is the creator's decision after the holdout.

**Traceability (rule 16, added after the rule was adopted):** the exploratory numbers in "The mechanism" were first read
with one-off snippets; they are now reproduced by `explore_f1.py` (output `explore_discovery.md`), and match. Lead tests:
`leads_check.py`.
