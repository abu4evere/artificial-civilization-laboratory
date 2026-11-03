# AM2 — AM1's autonomy battery, unchanged, on nature v12: findings (final: recomputed blind by GPT and Gemini)

Frozen as `AM2-frozen`. Read-only on `code_v12`. Run on GitHub Actions, run 41676999711, with the zero checks on the
cloud (`zero_cloud.log`: All: PASS, `code_v12` fingerprint `52ec206d…`). 32 paired seeds 22801–22832; 5 arms; LP
(80 founders, 80 × 80); 200 years, with years 100–200 counted. Every number comes from `analyse_am2.py` (AM1's analysis,
written before data; `am1_to_am2.diff`). Full tables are in `results.md`.

**Validity:** zero checks pass; all 160 worlds are present under one fingerprint; the sanity check passes (arm a, fewer
acts, completes no chain).

**Population beside it** (living-weeks, years 100–200):

| arm | living-weeks | extinct worlds |
|---|---|---|
| v12 | 23,176,597 | 0 |
| no habits | 18,243,321 (−21%) | 3 |
| more chance | 21,224,492 (−8%) | 2 |
| sham | 23,134,685 | 0 |

## The readings (frozen rule)
| measure | v12 | no habits (v12 − h) | more chance (v12 − t) | reading | AM1 on v11 |
|---|---|---|---|---|---|
| M1, self-prediction gain | 0.0804 | 0.0875 (−0.0071 [−0.0174, +0.0025]) | 0.0770 (+0.0034 [−0.0052, +0.0112]) | **not validated** | partly validated (by more chance) |
| M3, gather-then-make chains | 0.0036 | 0.0276 (−0.0240 [−0.0257, −0.0224]) | 0.0076 (−0.0040 [−0.0045, −0.0035]) | **not validated** (both controls higher) | the same |
| M5, the same after a food action | 0.0037 | 0.0305 | 0.0080 | **not validated** (both controls higher) | the same |

The sham is stable for all three: no "unstable" mark.

## What it means
1. **AM1's reversal holds on v12.** Without habits steering choice, people complete gather-then-make chains about
   **7.7 times** as often (0.0276 against 0.0036). With more chance in choice, about twice as often.
   - Both controls survive less: no habits −21% living-weeks with 3 extinct worlds; more chance −8% with 2.
   - FF1's fix of the make choice (nature v12) did not change this. **The habits that keep people alive are the habits
     that pull them away from finishing what they start.**
   - This is the trade-off rounds 54–56 discussed. It now stands on two independent sets of 32 worlds.
2. **M1 does not replicate.** On v11 it was partly validated by more chance, with an interval that only just cleared 0
   ([−0.0812, −0.0047]). On v12 neither control lowers it. M1 is therefore **not a reliable measure of autonomy** as
   defined. It should not judge any redesign.
3. **M2 (sequence structure beyond a time-shuffle), described only, falls in both controls again:**
   - v12 − no habits +0.0299 [+0.0243, +0.0353];
   - v12 − more chance +0.0226 [+0.0187, +0.0269];
   - the same direction as on v11.

   M2 is the one candidate that behaves as a measure of self-driven structure should, in both studies. It is a
   candidate for a frozen prediction in a later battery.
4. **v12 against v11 (arm c, different seeds, described):** no measure differs; every interval includes 0. FF1 changed
   none of these behaviours.
5. **For the brain road:** today's mind holds habits that help survival but cannot hold an end. That is the gap a goal
   memory is meant to fill (round 56). PB0 asks first whether foresight alone would change choices.

## Against the assistant's frozen prior
1. "M1 partly validated again (by t)": **wrong.** It is not validated.
2. "M3 and M5 still not validated, with h above c": **right.**
3. "The sanity check passes; the sham is stable": **right.**

## A label slip in the frozen analysis (noted, not changed)
The rule line printed under the table reads "Unstable if the sham − v11 interval …". The word "v11" was left over from
AM1 in that one sentence of text. The computation uses arm c (v12) throughout. Only the printed label is wrong.

## Independent recompute (3 November 2026)
GPT and Gemini 3.1 Pro, each in a fresh chat, worked from `recompute/am2_counts.csv` without the analysis script
(`recompute_am2.md`). Both match every number: M3 and M5 per arm, the four differences and their intervals, the
readings, the sanity count and the living-weeks. DeepSeek worked by hand and stopped before a final answer; its working
notes show the same differences.

**Final.**
