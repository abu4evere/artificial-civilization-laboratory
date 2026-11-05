# PB2 draft: let the episodic brain help choose — in a copy of the world (5 November 2026; the brain road, step 3)

**What this is:** a draft for council round 61. Nothing is frozen or built.
- **This is the first nature-change test of the brain road.** It is a test **in a copy** (`code_pb2` = `code_v13` +
  settings; 0 = v13). It goes live only by the safe path.
- **The basis:**
  - PB0 (foresight has room, but steering by today's reward makes people social, not inventive);
  - PB1 and PB1b (final): an **episodic memory that also learns from watching others (E-obs)** predicts the effects of
    actions better than the habit table, most of all in new combinations;
  - rounds 55–60;
  - the brain design (`docs/brain_design_draft_2026-11-03.md`).

## What changes in the copy (general abilities only; no named goal, invention or reward)
1. **Each person carries an episodic memory (E-obs, exactly as frozen in PB1b).** It stores their own weeks and the
   visible weeks of those they see. It predicts the 9 observable changes of an option.
2. **The memory also stores each week's learning signal r** (reward + 2 × mood change, the quantity habits learn
   from). From it, the memory predicts **r for an option**, by the same rule: the exact cell's mean, else similar
   weeks. This is the person's own experience of what felt good, not a value we write.
3. **Steering (arm P):** in `mind.decide`, the habit term `learned_weight × q[situation, action]` is replaced by
   `learned_weight × r̂(option)`, the memory's predicted r for that option's action and target.
   - Everything else is unchanged: the written pulls, curiosity, the softmax and its temperature.
   - **Where the memory has no entry** for the action, q is used as now.
4. **A learning-progress goal (arm G = P + goal):**
   - **The goal:** each person tracks, for each of the 9 outputs, how fast the memory's prediction error for that
     output is falling (learning progress, LP; Colas et al. 2022). Once a season they adopt as a goal the observable
     change with the highest LP, for example "materials held go up" or "a new kind made".
   - **Holding it:** options whose predicted change in that output is positive get a bonus. The bonus is the same
     size as the curiosity pull already in v9 (0.3 × curiosity gene × (1 − hunger)), so no new weight is invented.
   - **Dropping it:** the goal lasts until LP on it falls to 0, or for 1 year at most. Then a new goal is chosen.
   - **The rule (round 58):** goals are **states of observable outputs, never named things**, and nothing rewards
     making or remaking directly.

## Arms (paired seeds, LP worlds, 200 years)
| arm | memory | steering | goal |
|---|---|---|---|
| **v13** (c) | — | habits (q) | — |
| **P** | E-obs | predicted r replaces q | — |
| **G** | E-obs | predicted r replaces q | learning-progress goal |
| **G0** (ablation) | E-obs | as G | the goal is chosen **at random** each season, not by LP |
| **sham** | — | habits | — |

## Measures
**Guards first:** living-weeks and extinctions against v13 (FF's rule). A brain that kills people is not progress.

**Primary (to choose in round 61; candidates):**
- **(a) Remaking on purpose:** AF1's lineage measure R (new kinds remade within 5 years), against v13, with the first
  tests of intent: above chance against matched non-inventors, and preparation (gathering the inputs first);
- **(b) Ends-directed chains:** AM's M3/M5 (gather-then-make), which the habit trap suppressed;
- **(c) M2:** sequence structure beyond a time-shuffle (the one autonomy measure that held twice).

**Described:**
- PB0's warning (the shift to social acts);
- making and kinds;
- food and survival;
- **G against G0**, which separates learning progress from merely having some goal.

## Open questions for the council
1. **Steering:** is replacing q by the memory's predicted r right, or should r̂ be added beside q (and with what weight,
   fixed how)?
2. **The goal:** is "the observable output with the highest learning progress" a general law, or a disguised target?
   Is borrowing the curiosity pull's size for the bonus principled?
3. **The primary:** which of (a), (b) and (c), and the tests of intent to freeze now?
4. **Cost:** memories in every adult of every world for 200 years. Should a smaller window be used (for example,
   brains switched on at year 100 and measured to year 150)?
