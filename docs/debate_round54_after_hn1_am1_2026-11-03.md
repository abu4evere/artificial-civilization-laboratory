# Council round 54: after HN1 and AM1, what next? (3 November 2026)

**Opinions of GPT, Gemini and DeepSeek, not sign-off.**
- **The question:** `docs/debate_round54_question_2026-11-03.md`, the same file to all three, with a one-paragraph
  summary. It was sent by an earlier session (about 04:00 New York) that did not save this record.
  - This record was written at about 11:45 from the replies **read in the three chats** (GPT, the main chat; Gemini
    3.1 Pro, `d5ecc8b87be7ae89`; DeepSeek, `2552dbba-6c74-4cc4-b613-2228b137c47f`).
  - The "Code facts" section of the question file was added at 11:30, after the round, so the models did not see it.
    The earlier session's follow-up made the same provenance point.

## First answers
| | GPT | Gemini | DeepSeek |
|---|---|---|---|
| ranking | **B**, D, A, C | **B**, A, D, C | **B**, A, D, C |
| estimate for B | 93% ("that FF2-hunt can validly answer its fault-correction question ... not that it will improve hunting or cumulative culture") | 98% | about 90% |
| F7 | "Probably, but conditional on the species table being authoritative"; if the rates were unused design candidates, using them is a rule change needing ecological justification | "definitive fault" | fault, conditionally: if the table values are "arbitrary placeholders never evidence-anchored", using them is calibration; check provenance before freezing |
| F8 | "Stronger case for a genuine fault"; but tell a mistaken hard-coded expectation apart from an imperfect learned belief, and do not give exact foresight | fault ("the decision engine hallucinates an expected return") | fault, "not a calibration question" |
| AM1 habit/ends | not enough evidence to call it a fault; calibration, architecture (no persistent goals) or an adaptive trade-off all remain plausible; leans architecture; "an eightfold increase in M3/M5 under habit removal does not establish greater autonomy"; a read-only mechanism analysis before C | a real trade-off, made worse by calibration: habits learn what pays now; once hunting and tools pay, habits will reinforce longer sequences | a real trade-off, not a fault; perhaps calibration (VC1), but not shown harmful; do not fix now; C only after D and re-validated M3/M5 |
| checks GPT asks for in FF2 | v12 behaviour unchanged when the fixes are off; species probabilities, decision expectations, random-number consistency, food conservation; combined and separate arms, a sham, paired seeds, harm guards | | |

**Checked against the code** (live `acl/`, v12; the assistant, 3 November 11:25):
- **F7:** the `catch` field in `fauna.SPECIES` has been there since the first commit (`87a46dcc`), and no code has
  ever read it. The table's comment explains every other field, but not `catch`. The success roll is the flat
  `hunt_chance`, and the species is chosen only **after** success (`fauna.take_prey`).
  - So the provenance is unknown. Under GPT's and DeepSeek's own test, F7 is a **calibration choice, not a fault.**
  - Gemini's "definitive fault" does not survive this check.
- **F8:** `hunt_prey_base` 25 and `hunt_prey_per_hunter` 12 (first commit) are read only in `mind.decide`. What a kill
  gives is the species' meat (`take_prey`).
  - The decision's model of the hunt is stale: a hard-coded expectation, not a learned belief.
  - It is a fault under the 2 November rule ("a rule that does not do what its own comment or plan says": the option's
    utility is meant to weigh the food a hunt brings).

## The merged plan (sent to all three by the earlier session)
1. **FF2:** a harm-only fault-fix check on v12, like FF1.
   - **F8 only, for hunting.** The hunt option's expected meat becomes the meat of the prey the person sees on that
     tile: the same perception the option already uses to require prey. It is not exact foresight (GPT's caution).
   - **The other plain faults already drafted:**
     - F4: materials past the 20-unit limit go onto the tile's pile instead of being kept;
     - F5: only a thing that can hold water saves the walk to water.
   - Separate settings and arms per fix, a sham, and the FF1 rule.
2. **F7 moves into HR1.** HR1 becomes a calibration study of two existing things against evidence (per-species success
   and meat per kill). It is frozen after FF2 and chosen on calibration distance and safety only.
3. **D:** AM1's identical battery on v12, read-only, run in parallel with FF2.
4. **F6** (mark scale and wear) stays a separate calibration item.

## Follow-up answers (all support)
- **GPT:** "Yes, I support the merged plan; my confidence rises from 93% to 97%." The conditions: each fix passes
  "explicit conservation, perception, and regression checks".
- **Gemini:** supports; 98% → **99%**.
- **DeepSeek:** "Support: yes"; about 90% → **about 92%**, "because the F7 reassignment removes the provenance risk
  that could have invalidated FF2".

## What survived checking, and the decision
- **All three rank B first.** All three agree that F8 is a fault. F7's status turns on provenance, and the code record
  settles it as calibration.
- **AM1:**
  - No model calls habit suppression a fault.
  - Two call it a trade-off; GPT leans to a missing architecture (no persistent goals) and wants a read-only mechanism
    analysis before any change.
  - So C waits for D (the v12 baseline) and that analysis.
- **Decision** (the assistant, under the creator's standing autonomy, 3 November 2026; `docs/autonomous_decisions.md`):
  - Adopt the merged plan: **FF2** (F8 for hunting, F4, F5; separate arms; sham; GPT's checks) and **AM2** (AM1's
    battery on v12, read-only) in parallel; then **HR1** with F7 as a calibration item.
  - Estimate of success: **90%** (the lowest model's figure, rounded down; a harm-only check of plain faults has worked
    once already, in FF1).
