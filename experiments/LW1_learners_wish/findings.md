# LW1 findings: a learner's wish for the part they could not follow

**Status: final.**

The blind recompute (`recompute_lw1.md`, 7 November 2026, 12:37) matches every point estimate: GPT and Gemini with
code, and DeepSeek in its points (it had no code tool; its intervals are not counted). Only the co-primary's lower
bound differs: the study −0.0001, GPT +0.0002, Gemini +0.0001. So GPT and Gemini read "supported" with their own
random draws. **The cause is the bootstrap's random draws**, not a difference in the data or the method
(`recompute/mc_check_lw1.py`, written after data):
- across 50 other random seeds, the lower bound runs from −0.00016 to +0.00012;
- with 200,000 draws it is −0.00001.

The frozen random seed (20261109) was fixed before data, so the frozen reading stands. **The effect sits exactly on
the line.**

Every number is from `results.md` (analyse_lw1.py, frozen before data) on cloud run 42387280021:
- 3 arms × 32 paired worlds (seeds 24601–24632), on `code_lw1` = `code_v15` + `learn_wish`; LP, 200 years, years
  100–200 counted;
- zero checks All: PASS (`zero_local.log`: `code_lw1` at 0 = v15; read-only; LW and the sham act; reload exact with
  wishes; the unit checks: 864 wishes formed by the rule, 818 wish lessons valid, endings correct, no double lessons);
- all 96 worlds present under one fingerprint.

## The answer in one line
**The frozen reading: no harm, no effect.**
- **The wish does what it says.** Learners whose lesson failed on a missing part now learn a missing part within 5 years
  about **2.8 times as often**: 0.0165 against 0.0059, LW − v15 **+0.0107 [+0.0072, +0.0146]** (243 of 14,698 pairs
  against 76 of 12,991).
- **It does not carry through to the whole kind.** The co-primary, new kinds learned by someone other than the inventor
  within 5 years, rose from **0.0121 to 0.0191** (37 of 3,053 against 63 of 3,297). The difference is **+0.0070
  [−0.0001, +0.0140]**. Its lower bound touches 0, so by the frozen rule it is not supported.
- **Making by others stays at zero.** New kinds made by a non-inventor within 5 years: v15 1 of 3,053; LW 0 of 3,297
  (−0.0003 [−0.0011, +0.0000]).

## The guards (LW against v15): none raised
| guard | LW | v15 | ratio or difference [95%] |
|---|---|---|---|
| starvation deaths per 1,000 living-years | 4.546 | 4.978 | ratio 0.913 [0.788, 1.063] |
| killing deaths per 1,000 living-years | 0.012 | 0.000 | +0.012 [+0.003, +0.023] (threshold 0.05) |
| adult health | 93.08 | 93.04 | +0.04 [−0.81, +0.90] |
| living-weeks | 22,123,261 | 21,644,745 | ratio 1.022 [0.942, 1.115] |
| extinct worlds | 0 | 1 | −1 |
| child deaths per 1,000 child-years | 8.97 | 9.52 | ratio 0.942 [0.817, 1.090] |
| child starvation deaths per 1,000 child-years | 5.01 | 6.16 | ratio 0.814 [0.701, 0.949] |
| food gifts to kin's children per 1,000 adult-weeks | 5.09 | 5.11 | ratio 0.995 [0.907, 1.090] |

Notes:
- **Killing:** v15 had no killings at all in these 32 worlds, and LW had a few. The rise is a fifth of the frozen
  threshold, so the guard is not raised; it is recorded here, not hidden.
- **Child starvation** fell (ratio 0.81, interval below 1). This is not a gate, and one world fewer went extinct in LW.
  Read it as no harm, not as a benefit claimed.

## The sham
- Co-primary 0.0099 against v15 0.0121: −0.0022 [−0.0076, +0.0032]; no guard raised.
- So the run's noise in the co-primary is about ±0.005, and LW's +0.0070 sits just at its edge.

## The wish at work (described, LW only)
- **15,644 wishes formed.**
- **17,888 lessons were shown for a wish.** This is more than the wishes formed, because a wish stays until it ends and
  can be met again after a declined lesson.
- **2,784 wishes ended with the part known; 9,000 expired** after 52 weeks.
- **Time use did not change.** The grown spent 0.393 of weeks foraging and 0.094 talking, against v15's 0.395 and 0.098.

## What it means
- **PC1 found the blocker, and LW1 shows that steering lessons to it works.** Part learning nearly triples, with no
  harm. The wish is a general ability, and it costs nothing in time.
- **It is not enough on its own.** Most wishes expire, and most lessons are still declined: PC1 found acceptance about
  21%. Chains are deep (56% are 3+ levels), so a learner climbs one level and stalls. More kinds are learned (+58% in
  relative terms), but the interval touches 0.
- **The wall for Bob is unchanged: knowing is not making.** Even when a kind is learned, no one but its inventor makes
  it (0 of 3,297). RF1 found that pursuit fails on getting the pieces again. So after the lesson step, the next
  blockers are the inputs and the will to make.
- **Not adopted.** The frozen reading is not "supported", so it does not go to a confirmatory run by the rule. It is a knife-edge: the lower bound is 0 to within the bootstrap's noise. The assistant's prior was "supported"
  about 35% and "no harm" about 85%.
- **For the council:** whether to try LW again with acceptance (the trust gate) as the joint question, or turn to making
  by others (the inputs).
