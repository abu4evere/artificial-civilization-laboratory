# LC1 — Does curiosity slow the erosion over 1,000 years? (frozen plan)

**No change to live nature.** A long comparison on CU1's code (`code_cu1`, unchanged): arms v (v8), c (the curiosity
pull), x (sham). Chosen in debate round 28 (`docs/debate_after_ic2_lr1_2026-10-28.md`) as the safe step that informs the
creator's decision on nature v9, while the creator sleeps. GPT 90%, Gemini 95%.

**Why.** CU1 (final) supports the curiosity pull over 200 years (practice spreads; making × 1.57; crafting skill × 1.18;
no harm). But FS1 showed that every world's skill falls century by century (world-born adults 0.43 → 0.08 by years
400–500). The question that matters for Bob: **does curiosity hold skill up over centuries, or only delay the fall?**

## Design (32 new paired seeds, 20301–20332; LP: 80 founders, 80×80; 1,000 years; run on GitHub)
The runner is CU1's (`run_cu1.py`, its observer and census unchanged), with 1,000 years and new seeds. Arms as CU1:
v (`curiosity_pull` 0 = v8), c (`curiosity_pull` 1), x (sham).

## Questions
- **Primary:** world-born adults' (20–40) crafting skill in years 800–999 (pooled over yearly censuses: summed skill ÷
  summed head count), c − v, paired by seed; world bootstrap, 10,000 replicates. **Readings (FS1's margin, ±0.012 = one
  making act's skill gain from zero):** "curiosity holds skill higher" if the lower bound is above +0.012; "no lasting
  difference" if the interval lies inside ±0.012; otherwise "not shown". The sham's x − v beside it.
- **Survivor weighting (GPT):** the number of worlds and adult-years contributing in years 800–999 per arm; extinction
  reported as its own outcome.
- **Slower erosion or a parallel shift (GPT, Gemini):** for each arm, the change in that skill from years 100–199 to
  years 800–999, and c − v of that change; and, described, the century-by-century log-skill slope per arm (Gemini).
- **Secondaries:** making per adult-year by century; made things held per adult; population by century.
- **Flags (CU1's):** c has 3 or more extinct worlds beyond v by year 1,000, or mean population in years 800–999 below
  0.90 × v.

## The assistant's prior
1. "Not shown" or "curiosity holds skill higher" with a small gap: the gap persists, but both arms erode.
2. No flags.
3. Erosion slows somewhat in c (a smaller fall from years 100–199 to 800–999).
(GPT: 55% that curiosity meets the lasting-improvement threshold.)

## Validity (hard stops)
- **Zero checks** (as CU1, re-run for this runner): `code_cu1` with 0 equals `code_v8`; the setting and the sham act;
  the observer is read-only; `tried` equals own updates; reload exact.
- All 96 worlds present under one fingerprint.
- An independent recompute by GPT and Gemini (fresh chats, raw per-world numbers) of the primary and the flags.

## Sign-off (29 October 2026)
The assistant, under the creator's sleep-mode autonomy (CLAUDE.md, Sleep mode). GPT 90%, Gemini 95%; the assistant's
estimate is 80%. No change to live nature; adoption of v9 stays the creator's decision. Logged in
`docs/autonomous_decisions.md`.

## Operational note 1 (29 October 2026, after freezing, before any data)
1. **The runner** (`run_lc1.py`) imports CU1's runner unchanged and sets only the years (1,000), seeds, smoke seeds,
   jobs and output folder. The code and observer are CU1's (fingerprint 12bdc869, the same as CU1).
2. **Windows:** "years 100–199" and "years 800–999" are the yearly censuses at the ends of those years; a world that has
   died out adds nothing to skill sums and 0 to population.
3. **The log-skill slope** is a least-squares line through each arm's pooled skill per century (centuries with data),
   in log units per century; described only.
4. **The zero checks passed locally** (`zero_local.log`), re-run for this runner. Smoke worlds (15 years, seed 9993)
   showed the analysis runs; they were not data.
