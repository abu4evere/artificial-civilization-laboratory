# Debate round 44 (1 November 2026, the creator present): KL1's design (opinions, not sign-off)

**The same text to GPT (fresh chat `6ae7fa2b`) and Gemini (fresh chat `17bcc08091baa56c`); Claude as council.**
- **The origin:** IQ1's first report ranked "know-how that outlives its holders" first (H3, step 1). It was inspired
  (inspiration only) by Q 96:4 and Sahih Muslim 1631.
- **Proposed:** a read-only audit on v11.
  - When a recipe kind is lost to everyone, classify the loss as by death, by forgetting, or mixed.
  - When it comes back, record the path: made, heated or read; teaching and copying need a living knower.
  - **Primary:** D, the share of losses by death; R, the share of revivals through marks.

## Answers
- **GPT: accept with one change, 91%.**
  - "Make event-level provenance the authoritative basis for classifying loss and revival, rather than weekly
    snapshots." A knower "might forget and die within the same week."
  - Separate a kind that is *re-invented* from preserved knowledge.
  - Report R for mark-encodable kinds separately.
  - "D ≥ 0.5 is a reasonable descriptive majority threshold, but R ≥ 0.10 is arbitrary." Report intervals.
  - Measure exposure: readable marks left at extinction.
- **Gemini: accept with one change, 75%.**
  - "Restrict the primary revival metric R specifically to markable recipe kinds", since rock marks only carry "strike"
    know-how. Log mark coverage.
  - Benchmark 'read' against spontaneous re-invention ('made', 'heated').
  - The fixed cut-off of 100 revivals is "overly sensitive to total extinction frequency".

## Council
**Both changes adopted.** They do not conflict.
- Losses are classified from events: the code has exactly three ways a recipe leaves a mind (`acl/knowhow.py`):
  - the 12-recipe cap pushing it out;
  - dropping it as useless;
  - death, which erases all know-how (`acl/biology.py`: "A person's memories, habits and know-how end with them").
- R is computed on markable ("strike") kinds, beside the made and heated baselines.
- The revival floor is lowered to 30 markable revivals; below it, the reading is "too few to judge".
- GPT's mark-exposure measure is **not adopted**. A mark does not name a recipe kind (a reader picks the tool), so
  "marks for a kind" cannot be counted cleanly. `read` events are reported instead.
- **The assistant's estimate:** 80%.
