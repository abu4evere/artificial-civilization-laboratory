# PB1b — A shadow brain with episodic memory: findings (final: recomputed blind by GPT and Gemini)

Frozen as `PB1b-frozen`. Read-only on `code_v13`.
- **The run:** GitHub Actions run 41957772921, with the zero checks on the cloud (`zero_cloud.log`: All: PASS). The
  checks were: read-only; E-own the same alone; E-own equal to the table on lived cells; reload exact.
- **The sample:** 32 seeds 23101–23132; v13, LP; to year 120. 3,976 followed adults, with 4,102,980 own prequential
  weeks and 58.8 million observed weeks. No world died out.
- **Every number** comes from `analyse_pb1b.py`, written before data.

## The answer (frozen gate): GO to PB2 with an episodic memory
| gate part | cases | skill of E-own against the table [95%] | holds |
|---|---|---|---|
| 1. unfamiliar (situation, action) pairs | 255,389 | **+0.0092 [+0.0081, +0.0103]** | yes |
| 2. familiar pairs | 3,826,129 | +0.0000 (equal by construction) | yes |

**A memory that uses the exact average where it has lived a situation, and the most similar past weeks where it has
not, predicts new situations better than the table, and never worse on familiar ones.** The gain from one's own
memory alone is small (+0.9%).

## The big result (described; its preference rule is frozen): learning from others' weeks
| | unfamiliar pairs | familiar pairs | unfamiliar property combinations | rare actions |
|---|---|---|---|---|
| **E-obs** (own + observed, each observed week weighted 1 ÷ the number seen that week) | **+0.084 [+0.077, +0.090]** | **+0.032 [+0.031, +0.033]** | **+0.252 [+0.240, +0.264]** | +0.142 |
| E-obs-0.5 | +0.099 [+0.092, +0.105] | +0.041 | +0.269 | +0.190 |
| L-obs-0.5 (PB1's best, rerun) | −0.091 | −0.018 | +0.017 | +0.057 |

- **E-obs passes the gate** (both parts), and it beats E-own on unfamiliar pairs by **+0.075 [+0.068, +0.081]**. By
  the frozen rule, **observation is preferred for PB2.**
- **Watching others makes the memory about 9 times as useful** in new situations, and it also helps in familiar ones.
- **The largest gain is in combinations of properties never held before: +25%.** Others' experiences cover what one's
  own life has not.
- **By output** (E-obs, all own weeks):
  - **gains:** a new kind made **+0.28**, materials +0.13, food gained +0.11, things held +0.11, distance +0.08. These
    are all outcomes others can see;
  - **slight losses:** health, energy, affection and net food (−0.003 to −0.020). Observed weeks carry nothing about
    those hidden outputs, so diluting the person's own cell with observed entries costs a little there.
- **The learning curve:** E-obs helps most early in life (+0.09 in the first 100 weeks) and still helps after 20
  years (+0.02). A young person learns most from watching.
- **The linear learner, rerun,** loses again on unfamiliar pairs (−0.091), confirming PB1.

## What it means for the brain road
1. **A predictor that works exists:** an **episodic memory** that learns from one's own life **and from what one sees
   others do**. It is a general ability (remember, compare, watch). It names no goal, invention or outcome.
2. **Learning by watching is the strongest single ingredient found so far.** This is cultural learning in its
   simplest form. It helps most exactly where the brain road needs it: things never done before (+25%), new kinds,
   materials.
3. **For PB2:** connect **E-obs** to choices, as the predictor in round 58's plan. Arms: v13; E-obs steering by today's
   reward; E-obs + a learning-progress goal memory; the same with the goal memory off; a sham. The judges are the tests
   of intent.
   - **PB0's warning still applies:** steering by today's reward alone may make people more social, not more
     inventive. That is why the goal-memory arm matters.

## Against the assistant's frozen prior
1. "GO: E-own beats B on unfamiliar cases": **right** (small, +0.009).
2. "E-obs better still, and non-inferior on familiar": **right.** It is much better (+0.084), and better on familiar
   cases too (+0.032).
3. "The gain is largest for food and materials": **partly.** The largest is for a new kind made (+0.28), then
   materials (+0.13) and food gained (+0.11).

## Independent recompute (4 November 2026)
GPT and Gemini 3.1 Pro (fresh chats, code) worked from `recompute/pb1b_sums.csv` without the analysis script
(`recompute_pb1b.md`). Both match every number: E-own +0.0092 [0.0081, 0.0103], both readings GO, E-obs +0.0839 and
+0.0319, and E-obs − E-own +0.0747.

**Final.**
