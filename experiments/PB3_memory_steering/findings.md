# PB3 findings: memory steering as a candidate law — prediction or myopia?

**Status: final.** Blind recompute by GPT and Gemini (fresh chats, with code) matches every number and both readings (`recompute_pb3.md`); DeepSeek's reply is appended there when it ends.

Every number is from `results.md` (analyse_pb3.py, frozen before data) on run 42020737135:
- 160 worlds: 5 arms × 32 seeds, 23301–23332;
- 170 years, the brain on from year 100;
- measured over adults aged 16–49 in years 130–170;
- zero checks All: PASS (local record, accepted by the cloud; fingerprint 9f3701dd…).

## The answer in one line
**The habit table's one-week look-ahead is what held people back. Switching it off alone raises finished
"gather, then make" chains about 7.5-fold, more than the memory does.** PB2's memory effect replicates on new seeds,
but its cause is that the memory does not look ahead. It is not better prediction.

## The frozen questions, answered
1. **Guards: none raised.** Living-weeks against v13:
   - v13 with discount 0 (c0): 1.166 [1.028, 1.321], with 1 extra extinct world;
   - P: 1.276 [1.231, 1.325];
   - P+: 1.306 [1.260, 1.357];
   - the sham: 1.016 [0.892, 1.154], with 1 extra extinct world.

   Seed 23311 died out in both c0 (year 167) and the sham (year 153), so it is a fragile world, not an effect of
   c0.
2. **Primary, the attribution: "myopia, not prediction".**
   - P − c0 on M3 is **−0.0059 [−0.0076, −0.0044]**: the memory does *worse* than the habit table without
     look-ahead.
   - c0 − v13 is **+0.0228 [+0.0211, +0.0245]**.
   - M3 by arm:
     - v13 0.0035 (284,503 gather chains, 2,659,469 matched);
     - c0 0.0263 (380,653; 3,640,739);
     - P 0.0203 (258,999; 3,634,964);
     - P+ 0.0149 (293,961; 3,865,287);
     - the sham 0.0034.
3. **Co-primary, the replication: "PB2's steering effect replicates".**
   - P − v13 on M3: +0.0169 [+0.0146, +0.0193]. PB2 found +0.0176.
   - P / v13 living-weeks: 1.276 [1.231, 1.325]. PB2 found 1.283.

## Described (no frozen prediction; population beside each)
- **Adding a look-ahead to the memory (P+) brings part of the trap back.**
  - P+ − P on M3: −0.0055 [−0.0067, −0.0042].
  - P+ − c0: −0.0114 [−0.0128, −0.0100].
  - The 2 × 2 is consistent: in both systems, looking ahead lowers chains.
- **Without look-ahead (c0), people make far more:**
  - makes per adult-year: v13 0.061, c0 0.406 (about 6.6×), P 0.255;
  - world-new kinds per world in years 130–165: v13 40, c0 355 (about 9×), P 71.
- **R is still near zero everywhere.** Kinds remade within 5 years:
  - v13 1 of 1,284;
  - c0 0 of 11,348;
  - P 1 of 2,260;
  - P+ 2 of 2,082;
  - the sham 0.

  In c0, inventors held their new kind's inputs in 456 weeks and never still knew the recipe: they invent many more
  kinds and forget them all.
- **Living-weeks:** every arm without the habit look-ahead holds more people. P against c0 is 1.095 [0.968, 1.239],
  not distinguishable.
- **Acts aimed at a person:** c0 has fewer than v13 (−0.025 [−0.033, −0.018]). P has more (+0.052 vs v13;
  +0.077 vs c0). The social shift seen in PB2 comes from the memory itself, not from the missing look-ahead.
- **Food per adult** is not distinguishable from v13 in c0: −0.33 [−0.80, +0.16].
- **M2** is lower in c0 (−0.039), as in P. People born after year 100 show the same pattern.

## Against the assistant's prior (questions.md)
| prior | result |
|---|---|
| 1. c0 − c > 0 | **yes**, and larger than expected: +0.0228 |
| 2. P − c0 > 0 but smaller than P − c ("better prediction" about 55%) | **no: P − c0 < 0**, so "myopia, not prediction" |
| 3. PB2 replicates (about 85%) | **yes** |
| 4. P+ ≤ P on M3 | **yes** |
| 5. R stays near 0 | **yes** |
| 6. no guard | **yes** |

## What it means (the assistant's reading, for the council and the creator)
- **The "habit trap" (AM1, AM2) has a precise cause:** the one-week look-ahead in the habit update,
  q ← q + rate × (r + 0.8 × max next q − q).
  - With it, people finish almost no gather-then-make chains.
  - Without it, they finish about 7.5 times as many, make 6.6 times as much and invent 9 times as many new kinds,
    and the population is larger.
- **Memory steering is not, by this test, a better law than simply not looking ahead through the habit table.**
  - It does carry a different social pattern: more care, courting, talk and giving.
- **Why would a look-ahead suppress chains?**
  - A plausible mechanism, not tested here: the max over next week's habit values is dominated by the most valuable
    habitual act (often foraging). That inflates the values of acts that lead back to it, and flattens the
    differences that would favour finishing a chain.
  - The max is also known to overestimate (the classic bias of max-based learning).
  - This needs its own read-only diagnosis before anything is changed.
- **What follows (frozen before data):** "The next question becomes the look-ahead rule itself: a fault, or a law to
  test." The look-ahead does what its comment says ("how much next week's prospects count toward this week's
  choice"), so it is **not** a plain fault. Changing it is a nature change. It needs:
  - a council;
  - a frozen test with a sham;
  - a blind recompute;
  - a confirmatory run on new seeds;
  - the safe path;
  - and an argument that the new rule is a general law, not a tuned number.
- **R (remaking) is untouched by all of this.** With nine times the inventions, still nothing is made again. The cause
  of R lies elsewhere: memory for new recipes (rules review R1) and opportunity or intention.
