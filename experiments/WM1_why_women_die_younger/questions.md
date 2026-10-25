# WM1 — Why do women die younger than men? Adult mortality by sex on nature v7 (DRAFT, Revision 1, 25 October 2026; not frozen; waiting for the creator)

**Why.** In TW1 (`../TW1_twins_sex_ratio/results.md`), the control arm C (v6, an even sex draw at birth) had 98 boys
per 100 girls among those reaching 16, but 110 men per 100 women reaching 30 and 141 reaching 50. Arm T (v7) had
109 / 126 / 166. Counts of survivors are shaped by the birth ratio, cohorts and age structure as well as by deaths, so
this is a pattern, not yet a measured hazard. TW1 did not log deaths by sex. GPT asked for this before v7
(`../TW1_twins_sex_ratio/gpt_view_tw1.md`).

**The evidence** (from search results and abstracts, checked by GPT, `gpt_review_wm1.md`; not yet read in full by the
assistant):
- Among foragers, women often live as long as men or longer. Hadza life expectancy at birth: 35.5 years for women,
  30.8 for men (Blurton Jones 2016). This is life expectancy at birth, not the adult hazard.
- Savannah Pumé: 24.2 men to 22.5 women on average, a male share of 0.52 (Kramer, Schacht & Bell 2017, Phil. Trans. R.
  Soc. B 372: 20160316). Adults there are men 16–45 and women 14–36, and the figure varies widely year to year; it is
  not comparable with ACL's ratio at 50.
- Childbirth is a real cost. Among the Hiwi, about 4.4 maternal deaths per 1,000 women of reproductive age per year,
  about one per 55–75 pregnancies (Hill, Hurtado & Walker 2007, J. Hum. Evol. 52: 443–454). ACL's 1% per delivery is
  inside this range.
- Illness causes about 70% of forager deaths, violence and accidents about 20% (Gurven & Kaplan 2007, Popul. Dev. Rev.
  33: 321–365). Some populations show a large male excess from violence (the Hiwi).

**The purpose** is to learn what makes women die faster *inside ACL*, not to make ACL match a human sex ratio. This
study changes nothing in nature. Its diagnostic arms are measuring tools, never candidates for nature.

## What in v7 treats the sexes differently (from the code)

1. **Pregnancy:** +1.5 food per week for 39 weeks (`person.need`; an adult needs 7).
2. **Childbirth:** a 1% chance of death per delivery (`birth_death_chance`).
3. **Caring:** the mother is every newborn's carer (`child.caregiver = mother.id`). A carer feeds dependants from her
   own food first, weighted by her `care` gene (`biology`, "Parents feed the young first"). A new carer is chosen only
   when the carer dies (family first: father, older siblings, grandparents; then a kind stranger).
4. **Nothing else** in the body or the choices reads sex, except courting (a partner must be of the other sex). No risk
   applies only to men: hunting, fighting and travel are the same for both sexes.

## Design

**Part A (read-only).** Live v7 plus a logging observer, which changes nothing (zero check). Two settings, 120 years.
They are different regimes, not two sample sizes:
- **C20** (main): 20 founders on 40 × 40, today's standard world.
- **D80** (robustness): 80 founders on 40 × 40.

**Part B (diagnostic arms, C20 only).** `code_wm1` = v7 plus three switches (each 0 = v7 exactly). Run as a full
2 × 2 × 2 design: eight arms including v7 itself (arm C).
- **P0:** pregnancy needs no extra food.
- **B0:** no childbirth deaths.
- **K0:** a carer meets her own need before feeding dependants. Dependants get only what is left.

These are counterfactual rule changes that measure system-wide effects. K0 may save mothers and cost children. B0 can
save a woman who then dies of something else.

**Seeds:** 17001–17128.
- Part A: C20 and D80, 256 worlds.
- Part B: the same 128 seeds in each of the eight arms (arm C is Part A's C20 worlds), 896 new worlds.
- Seeds are paired across arms.

**Feasibility** (from TW1's results, C20-sized v7 worlds): about 0.9 childbirth deaths and about 90 deaths of all
ages per world, so roughly 115 childbirth deaths per arm. Before freezing, the assistant will count adult deaths by sex
in a throwaway 8-world pilot. Pilot data are not used for any result. If adult female deaths in C20 are under 2,000
per arm, the seeds go up to 256 (decided before any data).

**Who is counted:** world-born people from their 16th birthday until death, or censoring at week 6240 (year 120).
Founders are reported separately. Worlds that die out contribute until their last person dies. Extinctions and adult
person-years are reported per setting and arm.

## Logged (by a read-only observer, in every arm)

- **Person-weeks from 16**, summed into cells: sex × 5-year age band (16–19, 20–24, …, 50–54; 55+ descriptive only) ×
  each of these independent indicators:
  - pregnant (and the week of pregnancy);
  - weeks since last delivery (0–12, 13–52, 53–104, over 104, never);
  - dependants fed this week (0, 1, 2, 3+), and whether pregnant at the same time;
  - food given to dependants as a share of own need (0, under 25%, 25–50%, over 50%);
  - food deficit over the past 13 weeks (four bands);
  - sick now, and weeks sick in the past year;
  - health at the start of the week (four bands).
- **Per cell:** deaths by recorded cause.
- **The state is measured at the start of each week**, before anything happens; a death in that week is counted in
  that cell.
- **Every death from 16:** sex, age, recorded cause, all the indicators above, partner (alive, within 2 tiles), and
  over the last 13 weeks: food given out, food received (from whom: partner, kin, other), deficit and illness.
- **Men's and women's exposures by sex:** weeks spent hunting, fights joined, injuries, and tiles travelled.
- **Provisioning:** food given to pregnant women, carers and dependants, by the giver's relation (partner, kin,
  other) and timing.
- **Health after a load:** health and illness in the 52 weeks after a delivery, and after caring ends.

## Measures

- **Rates** are deaths per 1,000 person-years (person-weeks ÷ 52), by sex and age band.
- **Age-standardised** with **fixed equal weights** over the 5-year bands 16–19 to 50–54 (8 bands), the same for both
  sexes, both settings and all arms. Fixed now, so no arm sets its own weights.
- **Intervals:** world bootstrap, 10,000 replicates, percentile 95% intervals, resampling worlds within a setting.
  For Part B, seeds are resampled with all eight arms together (paired). A band with no person-weeks in a replicate
  is dropped from that replicate's standardisation for both sexes, and the number of such replicates is reported.
- **Survival from 16 to 50:** a pooled life table built from the band rates, with world-bootstrap intervals; also by
  birth cohort (born before year 40, 40–69).

## Questions

**Q1 — The gap (primary; C20 and D80).**
- G = the age-standardised female-minus-male death rate, 16–54, per 1,000 person-years.
- R = the female-to-male ratio of age-standardised rates.
- Survival 16–50 by sex.
- Each sex's band rates are shown, so it is clear whether women die more or men die less.

**Q2 — Loads and their aftermath (primary, descriptive; C20 and D80).** For women and men, age-standardised rates
across:
- each indicator, including concurrent pregnancy and caring;
- the weeks after a delivery and after caring ends;
- recent deficit and illness.

These are associations, not causes. Similar rates in unloaded weeks would not show that loads caused the gap.
[0.9, 1.1] is used only as a descriptive tolerance ("within 10%"), never as a decision.

**Q3 — Cause and state (primary, descriptive).**
- G split by recorded cause of death (childbirth, starvation, illness, thirst, killed, old age, other) and by load
  state at death.
- Shown as signed age-standardised rate differences with intervals: a negative share is a real offset. Percentages
  second, never forced to sum to 100.
- "Cause" means the cause the engine records. Hunger or caring may lie behind a recorded illness.

**Q4 — The diagnostic arms (primary, causal diagnostic; C20).**
- For each arm j: Δj = G_j − G_C, with paired intervals. Negative means the female disadvantage shrinks.
- Main effects and interactions of P0, B0 and K0 come from the full 2 × 2 × 2 design.
- Also each sex's age-standardised rate, child survival to 5, births per woman, and population.
- A mechanism "**reduces the gap**" if its main effect's interval lies below 0. It "**does not**" if the interval
  lies above −1 death per 1,000 person-years. Otherwise: unclear.
- **Q5, the all-three arm (P0 + B0 + K0):** the share of G that remains, with its interval. If G stays clearly above 0,
  the gap has another source (to be looked for next, not guessed now).

## Validity (hard stops)

- **Zero checks:**
  - the observer is read-only in every arm (state and random numbers identical with and without it);
  - `code_wm1` with all switches at 0 equals v7 exactly;
  - each switch changes only its own rule (a unit test per switch) and changes the world;
  - reload is exact.
- One fingerprint per code (`code_v7` for Part A, `code_wm1` for Part B), recorded.
- All worlds are present.
- An independent recompute of Q1 and Q4's main effects from the raw files before the findings are final (CLAUDE.md).

## What would follow (stated now)

- **One or more loads reduce the gap:** an evidence review of how forager women are supported while pregnant and
  caring (food from partners, grandmothers, others), and what ACL lacks. Any change to nature comes after that review,
  frozen on its own.
- **The gap remains with all three removed:** look for its source (lasting damage, behaviour) in the logs.
- **The lack of men-only risks** stays an evidence question. Nothing is added to make numbers match.

## The assistant's prior

- In C20, R is 1.3–1.6, and G is clearly above 0.
- K0 reduces the gap most, then P0. B0's effect is small: under 15% of G.
- With all three removed, G is close to 0.
- In Q2, most of the excess comes in caring weeks (starvation and illness while feeding dependants).

## Revision 1 (25 October 2026, before any code or data)

After GPT's review (`gpt_review_wm1.md`):
- Q2 is descriptive.
- The diagnostic arms are primary, in a full 2 × 2 × 2 design.
- G (rate difference) and R (ratio) are age-standardised with fixed equal weights in 5-year bands.
- Indicators are independent, with lagged and concurrent loads.
- Men's exposures, provisioning and health after a load are added.
- Contributions are signed.
- There is one fingerprint per code, and a test per switch.
- The evidence wording is corrected (Blurton Jones 2016; Pumé age bands; denominators; a narrower claim about men).
- A feasibility pilot is added (8 throwaway worlds; seeds raised to 256 if needed).
- The independent recompute is added.
