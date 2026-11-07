# CI1 findings: children may make again (LG), and a held aim that keeps its pieces (IN)

**Status: final.** The blind recompute (`recompute_ci1.md`, 6 November 2026, 16:29) matches. GPT and Gemini each
used code, and every point estimate agrees to 4 decimals, with the same readings. DeepSeek, which has no code tool,
declined to give intervals it could not compute.

Every number is from `results.md` (analyse_ci1.py, frozen before data) on cloud run 42249052146:
- 5 arms × 32 paired seeds 24001–24032, 200 years, years 100–200 counted;
- zero checks All: PASS (`zero_cloud.log`; `code_ci1` fingerprint e0ccbf07…);
- 160 of 160 worlds present under one fingerprint (one cloud chunk was lost and re-run; the 152 worlds fetched
  before it were identical).
Where a number is not in `results.md`, the line names the script that gave it.

## The answer in one line
**Letting children make again what they know works.** The share of new inventions whose inventor gathers the full
set of pieces rises about five times (0.0042 → 0.0225), and no harm guard is raised. **Keeping the pieces for a held
aim, alone, does nothing measurable.** Both together are supported, but no better than LG alone. By the frozen rule,
nothing is adopted yet: a supported arm goes first to a confirmatory run on new seeds.

## The frozen decision (each arm against v14)
| arm | complete-set share | arm − v14 [95%] | guards raised | reading |
|---|---|---|---|---|
| v14 | 12 of 2,839 = 0.0042 | | | |
| LG | 70 of 3,114 = 0.0225 | **+0.0183 [+0.0125, +0.0239]** | none | **supported** |
| IN | 27 of 3,601 = 0.0075 | +0.0033 [−0.0004, +0.0068] | none | no harm, no effect |
| LG+IN | 86 of 3,669 = 0.0234 | **+0.0192 [+0.0139, +0.0251]** | none | **supported** |
| sham | 7 of 2,980 = 0.0023 | −0.0019 [−0.0047, +0.0011] | (none) | (the sham moves the share the other way) |

## The harm guards, where they came closest
- **LG alone sits close to v14 on every guard.** Starvation 0.9486 [0.7925, 1.1245]; child deaths 1.0005
  [0.8183, 1.2137]; child starvation 0.9378 [0.7130, 1.2223]; adult health +0.52 [−0.20, +1.31]; population
  (living-weeks) 1.0553 [0.9414, 1.1924].
- **LG+IN came nearest to a line, and did not cross it.**
  - Starvation 1.1331 [0.9396, 1.3550]: the line is above 1.25 with the lower bound above 1.
  - Child deaths 1.1029 [0.9042, 1.3631]: the line is above 1.25.
  - Adult health −0.73 [−1.61, +0.20]: the line is below −5.
  - Its population rose: living-weeks 1.1270 [1.0218, 1.2535].
- **Food gifts to kin's children rose in every arm** (LG 1.1073 [1.0292, 1.2016]; IN 1.0852; LG+IN 1.0912). The sham
  rose too: 5.0888 per 1,000 adult-weeks against v14's 4.7916, a ratio of about 1.06 (a script on
  `recompute/ci1_counts.csv`; the frozen analysis gives no guard values for the sham). So this rise is mostly noise
  between runs. The guard looks for a fall, and there is none.
- **Extinctions: one world in each of LG, IN and LG+IN, and none in v14.** That is +1, under the line of 3.
  - In all three arms it is **the same world, seed 24017**. In v14 that world was the smallest of the 32: 72,865
    living-weeks.
  - The sham lost two other worlds (24004 and 24020) and kept 24017 alive.
  - These counts are from a script on `recompute/ci1_counts.csv`. They describe the deaths; they are not part of the
    decision.

## What the laws did (described, not decided)
- **Making again rose from nothing.** Kinds made again by their inventor within 5 years:
  - v14: 0 of 2,839;
  - LG: **22 of 3,114**, all by inventors who were children;
  - LG+IN: 13 of 3,669 (12 by child inventors);
  - IN: 4; the sham: 3 (both by grown inventors).
  - This is still rare, but it is the first time in ACL that **children's inventions are made again**.
- **Children's inventions are where the gain is.**
  - In v14, 2,631 of 2,839 new kinds are invented by children, and 11 of those 2,631 reach a complete set.
  - In LG, 69 of 2,827 reach one.
  - Children made 4.153 things per 1,000 child-weeks in LG, against 0 in v14.
  - Adults' making did not change (0.0664 makes per adult-year against 0.0685).
- **IN was very busy and changed little.**
  - It formed 70,853 aims, and 59,030 of them ended complete.
  - It kept 12.7 million set-downs, 146,454 hand-overs, 6.0 million makes and 30,822 play trials off the kept pieces.
  - Yet the co-primary moved only +0.0033. Grown inventors' complete sets rose from 1 to 6, against 208 v14 kinds and
    205 IN kinds.
  - A likely reason, read from the code (`aim_week`) but not measured here: an aim forms only on a recipe whose thing
    the person values above 0.05, and a newly invented kind starts with no value. So aims seldom point at the new kinds
    that the co-primary counts.
  - The known limit stands: IN keeps pieces but does not order the steps (making a part before the whole).

## Against the assistant's prior (questions.md)
| prior | result |
|---|---|
| LG supported, about 45% | **yes**, with no guard raised |
| IN supported, about 30%; a hunger guard possible | **no**: no effect; no guard (starvation 1.0898 [0.9353, 1.2440]) |
| LG+IN gives the most complete sets | yes, barely: 0.0234 against LG's 0.0225 |
| making again stays rare in every arm | yes, but LG made it rise from 0 to 22 |

## What follows (the frozen rule)
"A supported arm goes to a confirmatory run on new seeds before any adoption." LG and LG+IN are supported, and IN is
not. LG+IN adds nothing measurable over LG, and it came closest to the starvation and child-death lines. Which arm goes
to confirmation is the council's choice on this frozen data (round 69).

## Limits
- The co-primary counts holding the **complete set**, not making again. Making again is described, because it is rare.
- Seeds 24001–24032 are used here only. The confirmation must use new seeds.
- Heat crafts stay out of children's reach (they need the grown block); a possible LG2.

## Correction (6 November 2026, 21:15): heat recipes were within children's reach
The "Limits" line above says heat crafts stay out of children's reach. **That is wrong.**
- The make option offers a heat-verb recipe to anyone at a fire (`mind.decide`), and `actions._make` crafts it by
  holding the part in the fire.
- So under LG, children aged 3 and over at a fire could make heat recipes. What stayed for the grown is the separate
  option of holding *food* in the fire (`_heat_food`), along with put and fill.
- The claim came from council round 68 and the plan's "Known limits", unchecked against the code.
- **No result changes:** the study tested the code as it is. Found during round 71
  (`docs/debate_round71_adoption_v15_2026-11-06.md`).
