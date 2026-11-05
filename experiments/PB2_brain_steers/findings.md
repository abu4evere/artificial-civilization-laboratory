# PB2 findings: the episodic brain helps choose (a test in a copy of v13)

**Status: not final until the blind recompute** (`recompute_pb2.md`, to be written from the models' real replies).
Every number below is from `results.md` (analyse_pb2.py, frozen before data) on run 41985849249: 160 worlds
(5 arms × 32 seeds, 23201–23232), 170 years, the brain on from year 100. Measured over adults aged 16–49 in years
130–170. Zero checks All: PASS (local record, accepted by the cloud; fingerprint 3bcb2c07…).

## The answer in one line
**Letting each person's own memory guide their choices makes them finish about six times more of the "gather, then
make" chains they start, and the worlds hold about 28% more people.** A self-chosen goal on top adds **nothing**
measurable, and neither does a random goal.

## The frozen questions, answered
1. **The validity check (arm c's read-only memory): passes.**
   - Over 12,451,910 scored weeks, the memory's estimate r̂ predicted the week's learning signal r far better than
     the habit table's q.
   - Mean squared error: 0.0027 against 0.8021; difference +0.7995 [0.7759, 0.8215].
   - The correlation with r (described, and scale-free) gives the same verdict: 0.902 against 0.588; difference
     +0.314 [0.305, 0.324].
   - The squared-error gap is inflated by scale. q estimates a discounted sum that includes a look-ahead, so it is
     not on r's scale. The correlation is the fairer reading, and it agrees.
2. **Guards: none raised.** Living-weeks against v13:
   - P 1.283 [1.236, 1.335];
   - G 1.263 [1.211, 1.320];
   - G0 1.295 [1.246, 1.350];
   - sham 0.957 [0.848, 1.081].

   No world died out in any arm.
3. **Primary, M3 (ends-directed chains): the frozen reading is "not shown".** The goal does not help people finish
   what they start beyond steering alone, nor beyond a random goal:
   - G − P: −0.0007 [−0.0020, +0.0005];
   - G − G0: +0.0002 [−0.0009, +0.0013].
4. **The steering effect (P − c, reported with its interval as frozen): +0.0176 [0.0157, 0.0194].**
   - M3 rises from 0.0034 in v13 to 0.0210 with the memory steering.
   - Chains: 299,407 gather chains and 2,781,678 matched chains in v13; 270,255 and 3,842,688 in P.
   - The sham against v13: +0.0000 [−0.0004, +0.0005].
   - **The known limit, stated before data:** P − c mixes "a better predictor" with "no look-ahead", because q looks
     one step ahead and r̂ does not.
5. **Co-primary, R (lineage remaking): near zero in every arm, as predicted.** Kinds remade within 5 years:
   - v13 0 of 1,192;
   - P 5 of 2,214;
   - G 1 of 2,161;
   - G0 2 of 2,299;
   - sham 2 of 1,294.

   Every remake was by the inventor. With so few events, intent tests 1–3 cannot carry a reading:
   - test 1 (inventors against others): positive in P, but on 6 remakes;
   - test 2 (preparation): 5 of 6 in P;
   - test 3 (M5) moves with M3: P − c +0.0174 [0.0155, 0.0191].
   - G − P on R is −0.0018 [−0.0035, −0.0004]. This rests on 1 against 5 remakes and is not a meaningful
     difference in behaviour.

## Described (no frozen prediction; population beside each)
- **Making:** makes per adult-year rise from 0.061 in v13 to 0.254 in P, about 4 times. World-new kinds per world in
  years 130–165 rise from 37 to 69.
- **PB0's warning, partly confirmed:**
  - acts aimed at a person rise from 18.4% to 23.2% in P (+0.049 [0.043, 0.053]): care ×6, courting ×3, talk and give
    up;
  - gathering falls from 23.6% to 18.9%, and putting things down from 11.3% to 8.7%;
  - making and play rise.
- **Population:** living-weeks are +28% with the brain, and the share of adult weeks lived by people born after year
  100 is a little higher. More courting and care is a plausible route; it is not tested here.
- **Food:** edible food per adult at year end is slightly lower: P −0.29 [−0.65, +0.08]; G −0.33 [−0.66, −0.004].
  There are more people on the same land.
- **M2** (structure in consecutive actions) falls: P −0.038 [−0.044, −0.033]. Lives guided by memory are less
  repetitive.
- **Goals:**
  - in G, about 47% of adult weeks have a goal. Adoptions favour health + (44,683), affection + (22,006), materials
    + (22,192) and things held + (21,905). Goals are held about 25 weeks on average.
  - in G0 the goals are spread evenly, as designed.
  - the goal bonus (the curiosity pull's size) does not change M3, R or survival measurably.
- **People born after the brain came on:** M3 moves in the same way (P − c +0.0177 [0.0158, 0.0195]).
- **Fallbacks to q:** under 1% of decisions.

## Against the assistant's prior (questions.md)
| prior | result |
|---|---|
| 1. the validity check passes | **yes** |
| 2. P shifts toward social acts, and M3 changes little | social acts rose (yes), but **M3 rose about 6-fold (no)** |
| 3. G − P > 0 on M3, but G − G0 unclear | **G − P is null (no)**; G − G0 is null |
| 4. R stays near 0 in every arm | **yes** |
| 5. no guard is raised | **yes**, and populations grew |

## What it means (the assistant's reading, for the council and the creator)
- **The habit trap can be broken without losing survival.** AM2 found that habits keep people alive but hold back
  "gather, then make" chains: removing habits gave about 7.7 times the chains, with −21% living-weeks and 3 worlds
  extinct. Here, a memory of one's own weeks (plus what one saw others do, used for the goal outputs) gives about 6
  times the chains, with +28% living-weeks and no extinctions.
- **Goals did not add anything here.** A single seasonal goal with a curiosity-sized pull may be too weak, or
  learning progress on these seven outputs may not point at chains. Steering alone already explains the change.
- **Remaking on purpose (R) is still absent.** More people make more new kinds, but almost nobody makes a new kind
  again. Bob's "builds on what was learned" is not yet here.
- **Not yet a candidate for adoption.**
  - The goal part failed its frozen test.
  - The steering effect (P − c) is reported, not a frozen success criterion, and it carries the look-ahead mix.
  - Adopting "memory steering" into live nature would need its own frozen test, with P against v13 as the primary,
    then a confirmatory run on new seeds and the safe path (CLAUDE.md).

## Implementation notes (all before data)
- Memories end with their owner: nothing reads a dead person's memory. Recorded in WORKLOG at 01:06 on 5 November;
  the zero checks were re-run on that code.
- R uses AF1's lineage rule (a `make` action of the kind's own recipe within 5 years).
- Intent test 1 also reports "others who knew the recipe". In every arm none of them held the inputs, so that column
  is empty (nan).
