# Morning report: sleep mode, night of 27 October 2026

Everything below was done under your sleep-mode autonomy (CLAUDE.md). Every decision is in
`docs/autonomous_decisions.md`; every step is in `WORKLOG.md`.

## 1. LA1 is finished and final
Why are lessons refused? The study is read-only, with 32 worlds, and was recomputed blind by GPT and Gemini (all three
agree).

- **Lessons for world-born kinds fail mostly because the learner cannot follow them.** 85–88% need a part the learner
  cannot make. Removing that gate in replay gives 8.1 times more takes; restoring belief to its early level gives only
  1.06.
- **Per lesson, acceptance does not fall after year 50** (0.0236 → 0.0248). NA1's fall was counted differently (per kind
  and person, by when the kind was first made).
- **Half of early takes are pushed out at once** by the full 12-recipe memory.
- The prior was wrong on all four points.

## 2. The council's choice, made for you: PT1 (the parts-first and memory audit)
- **GPT:** (A), 85%. **Gemini:** (A), 95%. **Mine:** 80%. Above the 40% rule, so I went ahead.
- **Two facts in the code** that I found and gave both models:
  1. **Parts-first shows the first part the teacher knows**, not the part the learner lacks. It needs a second belief
     draw, and it goes only one level deep.
  2. **A taught recipe meets the memory limit at value 0**, before its lesson value is set. So it is usually the one
     deleted.
- **Gemini cited E7.7 wrongly** (it was about watching). Its point about composite recipes losing ties is right, and is
  measured.
- **Frozen as `PT1-frozen`.** It was first drafted as PF1, a name already taken by the partner-finding study, and renamed
  openly.
- **A smoke world (not data) hints:**
  - most failures are "deep": the part shown itself needs a missing part;
  - "wrong part" is rare;
  - with the lesson value set first, every new lesson would have survived the memory limit.

## 3. Status
See the end of `WORKLOG.md` for where PT1's run stands.

## For you to review (nothing needs you urgently)
- The PT1 decision itself.
- Whether either code fact deserves a frozen nature-change study later, one law at a time, by the adoption path:
  - a parts-first rule that shows a part the learner lacks;
  - setting a lesson's value before the memory limit.
- The hourly heartbeat expires about 3 November. Say anything after that and I'll renew it.
