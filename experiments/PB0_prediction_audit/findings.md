# PB0 — Would knowing what happens next change people's choices? Findings (final: recomputed blind by GPT and Gemini)

Frozen as `PB0-frozen`. Read-only on `code_v12`.
- **The run:** GitHub Actions run 41751443724, with the zero checks on the cloud (`zero_cloud.log`: All: PASS,
  including the copy and forced-pick checks).
  - 30 worlds were run on the cloud.
  - 2 (22901 and 22923) were run on the creator's PC because their cloud jobs hit the 340-minute limit.
  - A cross-machine check (world 22918) is identical in every field (`identity_check.md`).
- **The sample:** 32 seeds 22901–22932; v12, LP; 104 sampled adult decisions per world in years 100–110 (3,328 in
  all; none skipped).
- **Every number** comes from `analyse_pb0.py`, written before data, except where marked "post-hoc".

**Validity:** zero checks pass; all 32 worlds are present under one fingerprint (`code_v12`); no world died out.

## The answer (frozen rule): GO
| decisions | G, held-out gain over the top-scored option, 4 weeks [95%] | A | G / A | reading |
|---|---|---|---|---|
| 3,328 | **+0.1592 [+0.1512, +0.1672]** | 0.5074 | 0.314 | **GO** |

**Knowing each option's outcome would change people's choices often, and gain them about 31% of a typical month's
learning signal.**
- 56% of decisions have a held-out gain above the outcome noise.
- The gain holds against the softmax's actual pick (+0.152) and at longer horizons (13 weeks +0.159; 26 weeks +0.160,
  on 416 decisions each).
- In the all-options sample, the best option lies **outside the person's top 6 in 551 of 832 decisions (66%)**. So the
  scores rank badly what actually pays.

## What the gain is made of (described; the second half is post-hoc)
- **Almost all of it comes from reward, not mood** (+0.148 against +0.012). It is not the scripted-mood artefact
  Gemini and DeepSeek warned of.
- **But it does not show in survival terms.** At 4 weeks the winner and the top option leave people equally alive
  (0.9986 against 0.9982), with the same food (12.53 against 12.56) and nearly the same health (91.7 against 92.1).
- **Post-hoc** (a read-only count after the frozen analysis; not part of the reading):
  - **the top-scored option is mostly food work:** forage 1,404, gather 852, put 406;
  - **the oracle's winner is mostly social:** talk 1,331, give 897, forage 393, join 168, care 99, court 86;
  - **the most common switches** are forage → talk (618), gather → give (358) and gather → talk (348);
  - **make wins in only 40 of 3,328 decisions.**

## What it means
1. **Foresight has room** (the frozen GO). Today's choice (written pulls + habits) often fails to pick what will
   bring the person the most of their own learning signal over the next weeks, so a predictor has something to fix.
2. **What foresight would chase is set by the reward signal.** With today's rewards and today's forgiving world (food
   is plentiful; HN1 and TR1), a perfect predictor would make people **more social**, not more inventive. Skipping a
   week of foraging costs nothing within a month, while talking and giving pay in reward now.
3. **For the brain road:** a predictor alone (PB1) would most likely shift time toward social life, not toward
   discovery and making. Bob also needs goals that are not just the present reward signal, such as a goal memory
   driven by learning progress (`docs/research/autotelic_goals_2026-11-03.md`). These are questions for the council
   (round 58), not a reading of PB0.
4. **The habit trap, seen from another side:** people spend much of their time on food work that their own reward
   signal says they could cut back. AM1 and AM2 found that habits pull toward common actions; PB0 shows those actions
   are not even the ones that pay the person most.

## Against the assistant's frozen prior
1. "NO-GO, narrowly": **wrong.** It is GO, with G / A = 0.31.
2. "Where gains appear, they come mostly from mood": **wrong.** They come from reward.
3. "The full-menu winner lies outside the top 6 in under 10% of decisions": **wrong.** It is 66%.

## Independent recompute (4 November 2026)
GPT and Gemini 3.1 Pro, each in a fresh chat with code, worked from `recompute/pb0_outcomes.csv` without the analysis
script, picking the winners themselves (`recompute_pb0.md`). Both match: G 0.1592 (GPT [0.1513, 0.1672], Gemini
[0.1513, 0.1671]); A 0.5074; G / A 0.314; GO; winner differs from the top option in 85.4%.

**Final.**
