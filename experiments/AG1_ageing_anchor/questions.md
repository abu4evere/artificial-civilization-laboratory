# AG1 — Ageing anchored to forager evidence: does it make ACL's adult deaths realistic, safely? (frozen plan)

**A nature-change study (a calibration).** No new code: `code_v9` (live nature v9) unchanged; each arm changes one
existing setting, `mortality_base`. Adoption is the creator's decision, after a confirmatory run.

**Why.** The creator (30 October 2026): "humans used to live longer before and i think we should do same with acl";
"we are not gonna make grow their ages unrealisticly but slightly"; "just discuss with gpt and gemini and solve this
aging problem". The SA1 evidence note (14 October) found ACL's ageing hazard anchored in its rate (doubling every 8.0
years; foragers 8.1) but **5.3 times the forager average in scale** (Gurven & Kaplan 2007, Table 2; read in full text
then). A read-only count today on 6 throwaway v9 worlds (`docs/research/acl_lifespan_v9_2026-10-30.md`; not this
study's data) found adults dying at a mean age of 42, with death rates 1.8 to 5 times the forager total from age 30 on.
LS2: 98% of lost knowledge is lost at death. Debate round 33 (`docs/gpt_view_ageing_2026-10-30.md`): GPT and Gemini
both accept this four-arm design (90% each).

## Design
- **Code:** `experiments/NV9_nature_v9/code_v9` (fingerprint 8f88ec33…), with nature v9's settings passed explicitly
  (as LS2: v8's settings + `ground_items` 1 + `curiosity_pull` 1).
- **World:** LP (80 founders, 80 × 80), **1,000 years**, **20 new paired seeds (20501–20520)**, the same seeds in every
  arm. 80 worlds; 4 per cloud job, so no job nears GitHub's time limit.
- **Arms** (one existing setting each; the rate `mortality_rate` 0.0866 unchanged; the other ageing routes, maximum
  health after 50 and elders' doubled illness chance, unchanged):
  - **v** — nature v9 as it is (`mortality_base` 1.5 × 10⁻⁵ a week).
  - **b** — the smaller step, matched to the !Kung at age 40: 1.5 × 10⁻⁵ × 0.0072 / 0.0249 = **4.3373 × 10⁻⁶**
    (SA1 note's table: !Kung 0.0072 and ACL 0.0249 a year at age 40).
  - **a** — the forager average: 1.47 × 10⁻⁴ / 52 = **2.8269 × 10⁻⁶** (SA1 note: average a3 1.47 × 10⁻⁴ a year).
  - **x** — sham: v9 with `sham_draw` 1 (one extra random draw in week one; changes no rule).
- **Observer (read-only):** reads each week's events and the living; records every death's age and cause, the
  person-weeks lived in each age band, and LC1's yearly census (living, adults, making events, made things held by
  adults, world-born adults aged 20–40 and their summed crafting skill), plus the number of living people aged 60+.

## The primary: calibration distance
- **Age-specific, all-cause death rates** (GPT's and Gemini's changes): in each band 30–45, 45–60 and 60–70 (age in
  years at death, or while alive), rate = deaths in the band ÷ person-years lived in the band, **years 100–999**,
  pooled as a ratio of sums over the worlds (a died-out world contributes what it lived).
- **The reference, frozen:** the forager average total hazard h(x) = 0.013 + 1.47 × 10⁻⁴ × exp(0.086 x) (a2 and the
  senescent part from the SA1 note; it reproduces the note's 0.018 at 40 and 0.039 at 60), at the band midpoints:
  **37.5 → 0.01670; 52.5 → 0.02643; 65 → 0.05236** (computed by script; rounded to 5 decimals, the analysis uses the formula).
- **Distance D** = the mean over the three bands, **equal weights (frozen)**, of |ln(ACL rate ÷ reference)|.
- **Paired world bootstrap:** 10,000 replicates over the 20 seeds (the same resampled seeds in every arm), generator
  seed 20261030; 95% percentile intervals. A replicate where a band has no person-years is dropped (reported).

## The decision rule (frozen)
For each of **a** and **b** separately:
- **"More realistic"** if the upper bound of D(arm) − D(v) is below 0 **and** below the lower bound of D(x) − D(v)
  (beyond the sham's band).
- **Flags (harm), LC1's:** (1) the arm has 3 or more extinct worlds by year 1,000 than v; (2) living person-years in
  years 800–999 (a died-out world counts 0) are below 0.90 × v's. A flag is reported beside the reading; with 20 pairs
  it is a **safety warning**, not proof of harm (GPT).
- **If both are more realistic:** the arm with the lower D is the better anchor; if their intervals of D(arm) − D(v)
  overlap, both are reported as calibrating, and the choice is left to the creator. **The choice is made by
  calibration and safety, never by which arm raises skill or knowledge** (GPT, round 33b).
- **Exploratory (GPT):** 20 seeds. Adoption as a nature version needs a **confirmatory run** on new seeds (the frozen
  rule unchanged) and the creator's decision.

## Described (secondary; not part of the rule)
- Mean adult (16+) age at death, years 100–999; the share of adult deaths at 60+ and at 70+; the share of the living
  aged 60+.
- Population per century; extinct worlds.
- LC1's measure: world-born adults' (20–40) crafting skill in years 800–999 (arm − v, with its interval; LC1's ±0.012
  margin shown for scale only); making events per adult-year; made things held per adult.
- Adult causes of death (shares); child (under 16) deaths per child-year from starvation and thirst (a cost signal,
  Gemini's "elders' drag on food").

## Validity (hard stops)
Zero checks before data: the observer is read-only (state and random numbers identical with and without it, arms v
and a, 20 and 60 years); arms a and b act (differ from v by 60 years); the sham acts; reload exact (arm a); the
observer's death count equals the world's dead in each check. All 80 worlds present under one fingerprint (`code_v9`).
The independent recompute (GPT and Gemini, fresh chats, from raw per-world counts, without the analysis script) of the
primary (each arm's band rates and D, and D(arm) − D(v) with intervals) and the flags, before the findings are final.

## The assistant's prior
1. Both a and b are "more realistic" (the excess is large: D(v) about 1.07 in the read-only count).
2. a is closer to the reference than b, but ACL's other deaths (starvation, thirst, illness) keep both above it.
3. No flags; population rises somewhat in both; skill and making change little (described).

## What would follow
- **An arm more realistic, no flags:** a confirmatory run on new seeds; then the creator decides adoption (nature
  v10), by the usual path.
- **More realistic with a flag:** look at why (food, crowding) in a read-only follow-up before any adoption.
- **Neither more realistic:** the excess lies in the other ageing routes or in non-ageing deaths; a read-only look at
  causes by age comes next.

## Sign-off (30 October 2026)
**Signed off by the assistant under the creator's delegation** ("just discuss with gpt and gemini and solve this aging
problem") **and sleep-mode autonomy** (estimate 80%; GPT 90%, Gemini 90%; `docs/autonomous_decisions.md`). Frozen as
`AG1-frozen` before any code or data.
