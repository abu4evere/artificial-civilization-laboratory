# Autonomous decisions (sleep mode)

Since 27 October 2026 the creator has authorised the assistant to decide in their place in sleep mode ("you gotta work
autonomy decide without me … if its more than 40% just go ahead"; see CLAUDE.md, Sleep mode).

Every such decision is listed here with:
- the date;
- the decision;
- GPT's and Gemini's votes;
- the estimated chance of success;
- the reason.

| date | decision | GPT | Gemini | estimate | reason |
|---|---|---|---|---|---|
| 27 Oct 2026 | Next study after LA1: **PT1, the parts-first and memory audit** (renamed from PF1, a name already taken by the partner-finding study) (read-only on v7); frozen and signed off by the assistant | (A) first, 85% | (A) first, 95% | 80% (the assistant's own, taking the lower of the models' and allowing for observer complexity) | LA1: G4 "cannot follow" holds 0.85–0.88 of lessons back; the code's own route past it (parts-first) and the memory push-out were never audited; read-only, so no tuning risk. Both models' design notes adopted (`docs/debate_after_la1_2026-10-27.md`) |
| 27 Oct 2026 | After PT1: **MO1, the memory-order nature-change study** (c / o / sham, 32 paired seeds); frozen and signed off by the assistant. **Adoption deferred to the creator** | (A) first, 90%; "do not adopt v8 without the creator's explicit decision" | (A) first, 95% | 80% | PT1 (final): the new lesson is deleted in 71.4% of overflows because its value is set after the memory limit; 95.7% survive in the one-event replay. One law (learning event completes before memory decides), judged on retention with no-harm checks, not on making (`docs/debate_after_pt1_2026-10-27.md`) |
