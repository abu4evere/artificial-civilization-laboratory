# FS1 — Is the erosion the founders' head start wearing off? (frozen plan)

**An initial-condition study on nature v8.** Laws do not change: only the founders' starting skills differ between
arms, through one setting in a study copy of the code (`code_fs1` = `code_v8` + `founder_skill`; its default is
today's founders exactly). Nothing is adopted into nature. Chosen in debate round 20
(`docs/debate_after_ic2_lr1_2026-10-28.md`): both GPT (85%) and Gemini (95%) put it before any learning-rule change.

**Why.** M1, LS1 and LR1 show every world eroding over centuries: making, tools held, skill and population fall. But
the worlds start unevenly. **Founders begin as adults (16–28) with every skill at 0.2–0.4** (`world.py`,
`_make_founders`), while **every newborn starts at 0**, and crafting skill grows only by making or play. 0.73 of the
useful know-how held in years 0–100 is founders' (LS1). So part of the "erosion" may be an unearned head start fading.
The question: **do world-born people end up in the same place whether or not the founders had a head start?**

## Arms (32 paired seeds, 19901–19932; LP: 80 founders, 80×80; 500 years; run on GitHub)

| arm | founders' starting skills |
|---|---|
| **t** (today) | foraging, hunting and crafting each 0.2–0.4 (v8 exactly) |
| **z** (zero start) | all three at 0, the world-born level |
| **c** (no crafting head start) | crafting at 0; foraging and hunting 0.2–0.4 as today |
| **x** (sham) | v8 with `sham_draw` 1: the yardstick for world-to-world drift |

**The random stream is kept identical:** in z and c the same random numbers are drawn for the founders' skills as in
t, and then the skill is set to 0. So each seed starts with the same land, people, genes and places in every arm; only
the skill values differ. Arm c exists because zero-start founders also lack foraging skill and might starve: c separates
"a head start in making" from "a head start in getting food".

## Measured (read-only observer; a yearly census and the law's `make` events)
Every year: the living; adults; **world-born adults aged 20–40 and their mean crafting skill**; all adults' mean
crafting skill; made things held per adult; making events; and, for world-born people alive in years 300–500, crafting
skill at ages 10, 20, 30 and 40 (GPT: skill by age, so that founders dying and a changing age mix are not mistaken for
learning or forgetting).

## Questions (paired by seed; world bootstrap, 10,000 replicates)

- **Primary (GPT): world-born adults' crafting skill in years 300–500,** as an **absolute difference**. The mean
  crafting skill of world-born adults aged 20–40 over all yearly censuses in years 300–500 (summed skill ÷ summed head
  count), compared as z − t and c − t, paired by seed; x − t is shown beside them as the yardstick. Ratios are reported
  as secondary (both models: a ratio is fragile when late skill may be near 0.05).
- **Survivor weighting, in the open (GPT):** this measure counts living adults, so it describes the worlds that are
  still alive. Beside every skill estimate: the number of contributing worlds and adult-years. Extinction is reported
  as its own outcome.
- **Key secondaries (Gemini):** making events per adult-year, and made things held per adult, in years 300–500.
- **Also:** mean living population in years 300–500 (extinct worlds count 0); worlds extinct by year 100 and by year
  500 (reported separately, as GPT asked); the skill-by-age curve; the same measures in years 0–100, to show the start.

## Frozen readings (for z and for c, each against t)
**The margin is ±0.012 in crafting skill, fixed from the code before any data:** it is the skill one making act gives a
person starting from zero (`skill_gain` 0.012). A difference smaller than one act of practice is treated as negligible;
at that size the quality of a struck tool changes by about 0.5% (`matter.strike`: quality ∝ 55 + 45 × skill).
- **"Converges":** the 95% interval of the difference lies inside [−0.012, +0.012]. The late state does not depend on
  the founders' head start: the decline is the head start fading towards today's laws' own low level, and that level
  is the target for later studies.
- **"Zero start higher":** the lower bound is above +0.012. Something about the head start holds later generations
  back.
- **"Zero start lower":** the upper bound is below −0.012. The head start leaves something that lasts.
- **Otherwise "not shown"** (inconclusive). 32 seeds are fixed now; no seeds are added after seeing results (GPT).
- **Collapse flag:** if z has 4 or more worlds extinct by year 100 beyond t's, z's primary is reported but marked
  "survivors only, after an early collapse" (GPT), and **c becomes the main test** of the head start in making
  (Gemini), since c keeps the founders' food skills.
- **Whatever the result,** this is not proof that the head start caused everything (GPT): both arms could settle low
  because today's laws block accumulation.

## The assistant's prior
1. z and c **converge** with t on world-born crafting skill in years 300–500 (the head start is gone by then).
2. z is **not** collapsing: fewer than 4 extra early extinctions.
3. Making per adult-year and things held per adult in years 300–500 converge too.

## Validity (hard stops)
- **Zero checks:**
  - `code_fs1` with `founder_skill` = today equals `code_v8` exactly (seeds 501 and 601 at 20 and 60 years);
  - z and c act: founders' skills are 0 as set, and the worlds differ from t;
  - **only the skills differ at the start (GPT):** at week 0, every founder's id, name, sex, age, genes, place,
    relations and food are identical in t, z and c, and the random state after the founders are made is identical;
  - the observer is read-only (state and random numbers identical with and without it);
  - reload is exact.
- All 128 worlds are present under one fingerprint (`code_fs1`).
- An independent recompute by GPT and Gemini (fresh chats, raw per-world numbers) of the primary and the collapse flag
  before the findings are final.

## Review (debate round 21, `docs/debate_after_ic2_lr1_2026-10-28.md`)
- **GPT: approve after two changes, 90%.** Adopted: an absolute-difference primary with a margin justified before data
  (ratios secondary); contributing worlds and adult-years beside every estimate, extinction separate; no seeds added
  after results; a check that zero-start changes nothing else at the start.
- **Gemini: 95%.** Adopted: an absolute margin (it suggested 0.008; the council fixed 0.012 from the code instead, one
  making act's skill gain); c becomes the main test if z collapses. Its claim that 32 seeds give "narrow" intervals is
  not assumed: an inconclusive result will be reported as such.

## Sign-off (28 October 2026)
**The creator: "yessir"** (to "Approve FS1 and run it on GitHub?"). Frozen as `FS1-frozen` before any code or data.

## Operational note 1 (28 October 2026, after freezing, before any data)
How the code (`run_fs1.py`, `analyse_fs1.py`) reads the text where it left a choice; checked on 12-year smoke worlds
(seeds 9960 and 9961, all arms; not data). Nothing in the plan, its margin or its readings was changed.
1. **The setting** is `founder_skill` ("all" = v8, "none" = arm z, "no_crafting" = arm c) in `code_fs1`
   (`v8_to_fs1.diff`). The founders' skills are drawn exactly as in v8 and then set to 0, so the random stream is the
   same.
2. **"World-born"** means generation above 0 (founders are generation 0). **"Aged 20–40"** means from the 20th birthday
   to just before the 41st, at each year-end census.
3. **The late window** is the censuses at the ends of years 300–499 (200 censuses); "years 0–100" is the first 100.
   A world that has died out adds nothing to skill sums and 0 to population.
4. **Making events** are the law's `make` events, summed per year; "per adult-year" divides by the summed yearly adult
   counts. "Things held per adult" is made things held by adults at each census, divided the same way.
5. **Paired bootstrap:** each replicate resamples seeds once and recomputes the pooled means of both arms on the same
   seeds; the difference and the ratio are read from those replicates.
6. **"Extinct by year 100"** means the world ended before week 5,200.
7. **The zero checks passed locally** (`zero_local.log`): `founder_skill` "all" equals `code_v8` at 20 and 60 years;
   z, c and the sham act; the observer is read-only in t and z; at week 0 only the founders' skills differ (everything
   else and the random state identical); reload exact in t and z; fingerprint 01b19e66.
