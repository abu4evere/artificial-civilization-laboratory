# Council round 58: the brain design, after PB0 (4 November 2026, about 17:30)

**Opinions of GPT, Gemini and DeepSeek, not sign-off.**
- **The question:** `docs/debate_round58_brain_design_question_2026-11-04.md`, with the brain design and the ethics
  draft attached.
- **The chats:** GPT, the main chat; Gemini `87f468c684ee5839`; DeepSeek `2552dbba-…`.
- **Recorded from the replies read in the chats.**

## Answers
| | GPT | Gemini | DeepSeek |
|---|---|---|---|
| first part | **the predictor, but not a reward-maximising planner**: learn consequences without choosing what is desirable; test its generalisation on its own **before** connecting it to decisions | **the goal memory first** (95%): without a way to value and hold a new material state, a predictor only serves today's pulls toward talking and giving | **the predictor first, but bundled with a learning-progress drive in its first test**. LP needs prediction error, so the predictor is its substrate. About 72% that predictor + LP is valid and informative; about 85% that a predictor alone is valid but uninformative for Bob |
| smallest form | a small shared-feature network (one hidden layer, 16–32 units), compared against a linear predictor; inputs: body, nearby people, objects and their properties, conditions, the candidate action; outputs: predicted **changes in observable state** (food, energy, health, relations, place, object properties); online learning with replay; no future outcomes, recipe names or oracle data as inputs | a small recurrent network (or a state table) for goals; inputs are raw features already computed in `mind.decide` (tile, hardness, edge, people near), with no names and no utilities | **linear over 20–30 perceived features**, predicting a **vector** of outcome parts (food, health, energy, materials, mood), **never a single scalar**; a few hundred weights; nonlinearity only if it underfits |
| data (about 2,000 choices) | personal experience plus replay; others' observed outcomes as extra data, weighted by reliability, not a fixed ratio | social learning by watching (`knowhow.watch`) to bootstrap | an inherited structure and learning rate (never weights); learning from others' observed outcomes; replay or "dreams" |
| goals as valued states | a general law only if values are not disguised invention targets. Learn value from consequences, body, social feedback and progress in understanding. Learning progress drives exploration, but **a separate mechanism must decide what deserves lasting commitment**. Freeze the value rule first. **Never reward remaking, improvement or transmission directly** | general if states are physical properties, not labels; a state becomes a goal when reaching it reliably reduces the agent's own prediction error | general only if "valued" is learned. The danger is *which* dimensions count: naming "holding a cutting thing" is naming. Value is estimated from which predicted states preceded high outcome or high learning progress; goals are few, decay and compete |
| tests of intent | add targeted interventions with matched sham removals; behaviour must survive changed conditions; report false positives from agents with goal memory off; passing is not proof of consciousness | flexibility must use a substitute never met during the discovery | add a **no-goal ablation arm**, a **sham-removal** control, an **abandonment test** (goals dropped when unreachable), and observer blinding |
| ethics | keep cognitive sophistication separate from sentience and moral status; if credible welfare concerns arise, stopping or copying needs **documented independent ethical review, not only the creator's discretion**; pause criteria before the threshold | define a threshold for a "Bob-like mind" (for example passing 4 of 5 intent tests, or a goal held across generations) above which deletion needs explicit sign-off | add a floor of care at every level; a cooling-off period and a recorded reason before any irreversible erasure; the rights and consent of copies; population guards never silently override individual welfare |

## Checked (the assistant as council)
- **Gemini's "goal memory first" conflicts with its own mechanism.** It says a state becomes a goal when reaching it
  reduces the agent's prediction error, which needs a predictor. DeepSeek makes the same point the other way round
  ("the predictor is its substrate"). This survives: the predictor must exist first, even if it does not yet steer.
- **GPT's "test the predictor before connecting it"** matches Gemini's round-56 "shadow brain" and costs nothing to
  nature. It survives.
- **DeepSeek's vector outputs** (never one scalar) and GPT's "observable changes" agree. A predictor that outputs one
  "goodness" number would build the reward in. This survives.
- **GPT's "never reward remaking or improvement directly"** is ACL's hard rule (no rewards in nature). It survives
  and goes into the plan.
- **`knowhow.watch`** exists in v13 (watching another's use of a made thing and its outcome), so Gemini's reference is
  right. It covers made things only.

## The merged plan (the assistant's; for the creator)
1. **PB1, read-only:** a "shadow" predictor learns beside v13's people from their own and observed experience. It
   predicts the vector of observable changes and steers nothing. The question: does it predict well, and does it
   generalise to unfamiliar situations and materials (linear against a small network)?
2. **PB2, a test in a copy:**
   - **the arms:** v13; predictor steering by today's reward ("PB0's warning" arm); predictor + a learning-progress
     goal memory; the same brain with the goal memory off (ablation); and a sham;
   - **the judges:** the five tests of intent plus DeepSeek's abandonment test and a sham removal; observers blind to
     the arm;
   - **the rule:** value is learned, goals are few and decay, and nothing rewards remaking directly.
3. **Ethics:** the amendments go to the creator. GPT's "independent ethical review, not only the creator" is a real
   difference from principle 5, and it is the creator's to decide.
