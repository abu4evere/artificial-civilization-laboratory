# PB1 — A shadow brain: can a small predictor learn what ACL's actions do? Findings (final: recomputed blind by GPT and Gemini)

Frozen as `PB1-frozen`, with amendments 1 (numerical safeguards) and 2 (the zero check's 20-year world), both made
before any study data. Read-only on `code_v13`.
- **The run:** GitHub Actions run 41947447573.
  - The zero checks ran on the cloud (`zero_cloud.log`: All: PASS): read-only, L-own the same alone, prediction
    before update.
  - Two earlier launches failed before any world ran: numpy was missing on the cloud (fixed in `cloud-run.yml`), and
    the zero check needed amendment 2.
- **The sample:** 32 seeds 23001–23032; v13, LP; to year 120. 3,502 followed adults, with 3,742,401 own prequential
  weeks and 53.4 million observed examples. No world died out.
- **Every number** comes from `analyse_pb1.py`, written before data, except where marked "diagnosis".

## The answer (frozen rule): it does not
| cases | skill of L-own against the table B [95%] | reading |
|---|---|---|
| 226,685 compositionally unfamiliar weeks (common actions) | **−0.202 [−0.212, −0.192]** | **it does not** |
| mandatory secondary: 81,801 weeks with an unfamiliar property combination | −0.068 [−0.079, −0.056] | |

**A small linear predictor, learning from one life at the frozen rate, predicts the effects of a person's actions
worse than a simple table of their past averages, even in situations they have never met.** The 16-unit network
(N-own) does worse still (−0.241 [−0.253, −0.231]), so by the frozen rule linear is kept.

## Where it stands (described)
- **It improves with life, but never catches up:** skill is −0.147 in the first 100 weeks, −0.192 at 100–500,
  −0.121 at 500–1,000, and −0.076 beyond 1,000 weeks.
- **By output (all own weeks):**
  - L-own is better than the table for **a new kind made** (+0.29), **affection** (+0.07) and things held (+0.01);
  - it is worse for food gained (−0.82), net food (−0.67), energy (−0.48) and materials (−1.55).
  - So the table's exact averages win where outcomes depend on the precise situation and action, as food does.
- **Rare actions:** about even (+0.016 [−0.008, +0.040]).
- **Unfamiliar destinations:** −0.055.

## An implementation flaw in two observation variants (diagnosis; it does not touch the primary)
- **What happened:** L-obs (weight 1.0) and N-obs **diverged** in some worlds. N-obs gave NaN in 7 of 32 worlds;
  L-obs reached 44 and 70 times B's error in two worlds.
- **The cause** (read from the output files): a followed adult sees 10–21 others' weeks per own week. The code applied
  them as **one batched update that sums their steps**, so the effective step at weight 1.0 was far too large.
- **The consequence:** these two variants measure the batching flaw, not the value of learning by watching. The
  frozen preference line "own experience only" is therefore not a valid conclusion and is not used.
- **L-obs-0.5** (half the step) stayed stable, and it is **the best variant**:
  - primary −0.103 [−0.114, −0.094];
  - it is the only one **above the table** on unfamiliar property combinations (+0.013 [+0.004, +0.024]), unfamiliar
    destinations (+0.025) and rare actions (+0.052).
- **The hint (described, not a finding):** watching others can help generalisation, but only if it is weighted
  properly.

## What it means for the brain road
1. **The frozen consequence:** the brain road stops to rethink inputs or learning before PB2. A predictor that steers
   choices would, as built here, steer by worse guesses than the habit table's averages.
2. **What looks wrong is the learning rule, not the idea of prediction:**
   - a fixed-step online learner keeps chasing noise, while the table averages exactly;
   - a linear model cannot represent the interactions (this action on this tile in this season) that food depends on;
   - observation needs a step that scales with how many examples arrive.
3. **What a rethink could try (for the council, not decided):**
   - a learner that averages like the table but shares strength across similar situations, for example a table
     smoothed toward a linear prediction, or a Bayesian or recursive-least-squares update with a decaying step;
   - features that include action × setting interactions;
   - observation weighted by the number of examples.
4. **The table baseline is itself a lesson:** ACL's people already store per-situation averages in their habits. The
   wall AM1, AM2 and PB0 found is less "they cannot predict" than "their choices are pulled away from what they would
   predict" (PB0: the best option lies outside the top 6 in 66% of decisions).

## Against the assistant's frozen prior
1. "The predictor learns and generalises": **wrong.**
2. "Observation helps": **not testable as run.** L-obs at full weight diverged; at half weight it was the best variant.
3. "The network does not beat linear": **right.**
4. "Skill best for food and distance, worst for affection and new kinds": **wrong.** It was the reverse: L-own does
   best on new kinds and affection, and worst on food.

## Independent recompute (4 November 2026)
GPT and Gemini 3.1 Pro (fresh chats, code) worked from `recompute/pb1_sums.csv` without the analysis script
(`recompute_pb1.md`). Both match: primary −0.2017 (GPT [−0.2123, −0.1916], Gemini [−0.2119, −0.1917]), "it does
not"; secondary −0.0676.

**Final.**
