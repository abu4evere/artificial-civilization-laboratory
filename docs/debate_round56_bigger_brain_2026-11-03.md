# Council round 56: does Bob need a bigger brain, and should ACL commit now? (3 November 2026, about 14:55–15:10)

**Opinions of GPT, Gemini and DeepSeek, not sign-off.**
- **The question:** `docs/debate_round56_question_2026-11-03.md`, the same file to all three. It was asked at the
  creator's request: "If Bob eventually needs this type of bigger brain we should go with that option but ask other ai
  about this."
- **The chats:** GPT, the main chat; Gemini, the fresh chat `87f468c684ee5839` (round 55's); DeepSeek, `2552dbba-…`.
- **Recorded from the replies read in the chats.**

## Answers
| | GPT | Gemini | DeepSeek |
|---|---|---|---|
| does Bob need it? | **yes, about 95%**, for generalisation, prediction and persistent goals. It disagrees that a richer table *cannot*: "A sufficiently expressive structured system could implement these abilities without neural networks." | **yes, 99%.** A table only memorises, and open actions would make it blow up. | **yes:** about 85% for a generalising predictor, about 95% for goal-holding state. "A 'richer table plus open actions' is not a third road — it is the same road with a worse approximator." |
| commit now? | commit to the programme now, but run the cheap upper-bound test first. "A negative result would not eliminate the case": the fixed actions might hide prediction's value. Keep hunting calibration going independently. | not yet: run the cheap test first, because of the 10–100× cost | **commit now to the road; do not build before the gate.** Freeze the brain as a planned line, with the upper bound as the first frozen study and a written go/no-go rule |
| the data problem | 1. structured, sample-efficient learning (relations between actions, objects, properties and consequences); 2. social learning, weighted as indirect evidence; 3. evolved learning predispositions (not knowledge); 4. finer time steps **only** if real action timescales justify them | an evolved readiness to learn (structure, not knowledge) plus social learning as a data multiplier; no finer time steps | **not** finer time steps (they break the week-anchored biology: ageing, food needs, gestation). In order: learn from **observed** outcomes, not only chosen ones; an inherited readiness to learn (the Baldwin route); social learning |
| smallest brain | three parts: a compact predictive model (perceived properties + conditions + action → consequences), a goal memory with priorities that change through experience, and a short-horizon planner | a small recurrent state-space model (memory to hold goals, a forward model to imagine) | a compact feature-based predictor (a linear model or small network over body state, visible objects' properties and recent actions), a goal register (a few held intentions that decay and resume), and a 1–2-step look-ahead. "No deep RL, no LLM." |
| first study | **PB0, a prediction-opportunity audit:** read-only on v12, 32 paired worlds. Compare the habit's choice with the choice preferred under independently estimated outcome predictions; record disagreement, outcome differences and availability. A shuffled-prediction control and blind recompute. | **a read-only "shadow brain":** a recurrent model watches the tabular people and predicts the next state and need; a sham gets scrambled time; the metric is prediction accuracy, and whether it learns the use of marks, piles and stashes | the round-55 upper-bound replay as the gate. If it passes, a frozen copy-test at matched compute against v12's table, with a sham, guards, primary option-shift rate, goal resumption and survival |

## What survived checking (the assistant as council)
- **All three say yes:** Bob needs generalisation, prediction and goals held over time.
  - GPT's caution stands: it need not be a neural network. It must be a learned, structured predictor.
  - The assistant agrees: "the smallest mechanism" was already the round's premise.
- **All three agree on order:** commit to the road, but a cheap **read-only** test comes first. All three designs are
  read-only on v12, so no nature changes at step one.
- **All three reject finer time steps** as the answer to the data problem, unless evidence on action timescales
  justifies them. DeepSeek's reason holds against the code: ACL's biology is anchored per week.
- **The shared answer to the data problem:**
  - learn from more than one's own choices (observed outcomes, others);
  - an evolved readiness to learn, inherited as structure and never as knowledge.
- **The brain all three describe** is the same in substance: a small predictor, a goal memory, and a short planner.

## The decision on the road (the creator's, given above, now supported by all three)
**ACL commits to the brain road as a planned line of frozen studies.** Hunting calibration continues alongside it.
- **Step 1 (read-only, allowed under the 40% rule):** **PB0**, merging GPT's prediction-opportunity audit with
  DeepSeek's gate. On v12's own decisions, how often would an option's predicted outcome change the choice? It has a
  written go/no-go rule, a shuffled control, 32 new seeds, and a blind recompute.
- **Later, only through frozen nature-change tests in a copy:** the small brain (predictor + goal memory + short
  planner); learning from observed outcomes; an inherited readiness to learn. Each goes through council and the safe
  path.
- **Numbering:** HR1's council round becomes round 57.

**Correction (14:46):** the times in the title were estimated, not read from the clock. Commit times: round 55 recorded at 14:25, round 56 at 14:38 (both 3 November, New York).
