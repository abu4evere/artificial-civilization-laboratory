# CI1-C: children may make again (LG), confirmatory run on new seeds (frozen plan)

**The safe path's confirmatory step** (`CLAUDE.md`) for CI1's LG arm. CI1 is final and LG supported
(`experiments/CI1_children_and_aims/findings.md`). This is a test in a copy, not an adoption.
Council round 69 chose LG alone (`docs/debate_round69_after_ci1_2026-11-06.md`).

## Design: CI1's LG arm exactly, on new seeds
- **The same code:** `experiments/CI1_children_and_aims/code_ci1`, fingerprint e0ccbf07…, unchanged.
- **The same set-up, guards and co-primary:** CI1's runner and frozen analysis (`run_ci1.py`, `analyse_ci1.py`). Thin
  wrappers set the seeds, arms and folder.
- **Arms:** v14 (c: child_make 0, held_aim 0), LG (g: child_make 1, held_aim 0) and the sham (x). IN is set aside.
- **Seeds 24101–24132:** 32 new paired seeds, used by no study. LP; 200 years; years 100–200 counted.
- **One read-only addition to CI1's observer:** for each world-new kind, whether a person other than its inventor
  made it within 5 years. It is described only, and the zero checks' read-only test covers it.

## Frozen decision rule
**Confirmed** only if all three hold:
1. **No CI1 guard is raised for LG against v14.** The guards, exactly as in CI1:
   - starvation deaths per 1,000 living-years: ratio above 1.25 with the lower bound above 1;
   - killing per 1,000 living-years: difference above 0.05 with the lower bound above 0;
   - adult health: difference below −5 with the upper bound below 0;
   - living-weeks: ratio below 0.90 with the upper bound below 1;
   - extinctions: 3 or more extra worlds;
   - child deaths per 1,000 child-years: ratio above 1.25, the lower bound above 1, and a rise of 3 or more;
   - child starvation per 1,000 child-years: ratio above 1.25 with the lower bound above 1;
   - food gifts to kin's children per 1,000 adult-weeks: ratio below 0.80 with the upper bound below 1.
2. **LG − v14** in the co-primary (the per-kind complete-set share) has its paired-bootstrap lower bound above 0.
   This is CI1's "supported".
3. **LG − sham** in the co-primary has its paired-bootstrap lower bound above 0.

**Not confirmed:** otherwise. Then LG is not adopted. The bootstrap uses 10,000 paired-world resamples; CI1's analysis
keeps its own random seed (20261122), and the wrapper's additions use 20261124.

## Pre-registered secondary (reported with its interval; not a gate)
- **Remaking:** the share of world-new kinds made again by their inventor within 5 years, LG − v14.

## Described (not decisive)
- Kinds made by a person other than their inventor within 5 years, per arm.
- CI1's described tables: inventors by age (child, grown), child makes per 1,000 child-weeks, makes per adult-year,
  care, food per adult, adult-weeks at the carry limit, and child health.
- Child makes and child starvation side by side.

## Validity (hard stops)
- **Zero checks**, CI1's (re-run for this study):
  - `code_ci1` at 0 = `code_v14`;
  - the observer is read-only (now with the addition);
  - each arm acts;
  - reload is exact;
  - the unit checks pass.
- **All 3 × 32 worlds** are present under one `code_ci1` fingerprint.
- **A blind recompute** by GPT, Gemini and DeepSeek of the three conditions and the secondary.

## What follows
**If confirmed:**
1. the blind recompute;
2. GPT, Gemini and DeepSeek consulted on adoption as nature v15, with the assistant's estimate at 40% or more;
3. `code_v15` = `code_v14` + the child_make law at default 1 (the held_aim code is not carried);
4. zero checks: v15 with child_make 0 = v14, and v15 = CI1-C's LG arm;
5. reference hashes regenerated and the tests passing;
6. a tag `nature-v15` and a Telegram message.

**Not confirmed:** CI1's gain is recorded as not repeating; nothing is adopted.

## The assistant's prior
- **Confirmed: about 80%.** Round 69: GPT 85%, Gemini 95%, DeepSeek about 92%.
- Remaking stays rare but above v14's 0.
- Making by others stays rare.

## Sign-off (6 November 2026)
The assistant, under the creator's 2 November permission (tests of new laws in a copy, the safe path) and their
6 November message ("check everything and learn first then keep working"; on Telegram: "Today whole day you can work
on pc fully"). This is the frozen next step of a supported study. Council round 69 was unanimous on LG alone. Frozen
as `CI1C-frozen` before any code or data.
