# CI1-C findings: children may make again (LG), confirmed on new seeds

**Status: final.** The blind recompute (`recompute_ci1c.md`, 6 November 2026, 19:29) matches. GPT and Gemini each
used code; every point estimate agrees to 4 decimals, with the same reading. DeepSeek, which has no code tool, was
still working by hand; its reply will be appended.

Every number is from `results.md` (analyse_ci1c.py on CI1's frozen analysis, both written before data) on cloud run
42298530869:
- 3 arms (v14, LG, sham) × 32 new paired seeds 24101–24132, 200 years, years 100–200 counted;
- zero checks All: PASS (`zero_cloud.log`, run through CI1-C's runner so its observer was checked; `code_ci1`
  fingerprint e0ccbf07…);
- 96 of 96 worlds present under one fingerprint.

## The answer in one line
**Confirmed.** On new worlds, letting children make again what they know raises the share of new inventions whose
inventor gathers the full set of pieces from 0.0041 to 0.0262, about six times. No harm guard was raised. LG now
goes the safe path to nature v15.

## The frozen rule (all three must hold)
| condition | value | holds |
|---|---|---|
| 1. no CI1 guard raised for LG against v14 | none raised | yes |
| 2. LG − v14 in the co-primary, lower bound above 0 | 107/4,077 against 16/3,873: **+0.0221 [+0.0166, +0.0283]** | yes |
| 3. LG − sham in the co-primary, lower bound above 0 | against 16/3,583: **+0.0218 [+0.0169, +0.0278]** | yes |

The sham against v14 is +0.0003 [−0.0029, +0.0035]: no movement, as a sham should show.

## The guards (LG against v14)
**Every guard moved toward less harm, or stayed level.**
- **Starvation:** 0.9942 [0.8759, 1.1290].
- **Killings:** 0 against 0.0021 per 1,000 living-years.
- **Adult health:** −0.08 [−0.67, +0.55].
- **Living-weeks:** 0.9733 [0.8581, 1.0911].
- **Child deaths:** 0.9259 [0.8097, 1.0697].
- **Child starvation:** 0.9447 [0.8054, 1.1058].
- **Gifts to kin's children:** 1.0221 [0.9339, 1.1305].
- **Extinctions:** LG 0, v14 2.

CI1's nearest approaches to a line were in LG+IN, which was not carried forward. They do not recur in LG alone.

## Pre-registered secondary (not a gate): making again
**Kinds remade by their inventor within 5 years:** v14 2 of 3,873, the sham 0 of 3,583, **LG 32 of 4,077**.
LG − v14: **+0.0073 [+0.0044, +0.0107]**.
- Of LG's 32, 31 were remade by inventors who were children.
- Among kinds that reached a complete set, LG made 32 of 107 again, against v14's 2 of 16.
- This repeats CI1, where LG remade 22 against v14's 0. Twice now, on 64 different worlds, **children's inventions
  are made again** only when children may make.

## Described
- **Children make:** 4.464 makes per 1,000 child-weeks in LG, against 0 in v14. Adults' makes per adult-year are 0.0886
  against 0.0767.
- **Child makes beside child risk:**
  - child starvation deaths per 1,000 child-years: LG 4.83, v14 5.11, the sham 5.43;
  - child deaths: LG 7.68, v14 8.30, the sham 8.64.
  - More making by children came with no rise in risk to children.
- **Nobody else ever made a new kind: 0 kinds made by another person within 5 years**, in every arm (0 of 3,873,
  0 of 4,077, 0 of 3,583).
  - The measure works: in the 12-year smoke run it counted 20, 26 and 18 kinds made by others, mostly in the
    founders' first years.
  - In years 100–200, no new invention reached a second maker within 5 years, in any world or arm.
  - **This is the next wall for a cumulative mind (Bob):** an invention now stays with its inventor, child or grown,
    and is remade by them, but it does not spread.

## Against the assistant's prior (questions.md)
| prior | result |
|---|---|
| confirmed, about 80% | **yes** |
| remaking stays rare but above v14's | **yes**: 32 against 2 (0.8% of kinds) |
| making by others stays rare | **more than rare: none** |

## What follows
The safe path (`CLAUDE.md`), in order:
1. The blind recompute, by GPT, Gemini and DeepSeek in fresh chats.
2. The council on adoption.
3. `code_v15` = `code_v14` + the child_make law at default 1. The held_aim code is not carried.
4. Zero checks: v15 with child_make 0 = v14, and v15 = CI1-C's LG arm.
5. The reference hashes regenerated and the tests passing.
6. A tag `nature-v15` and a Telegram message.

**Then, for the brain and culture road:** why does no new invention reach a second person? That question is the
first lead, from this study's described count.
