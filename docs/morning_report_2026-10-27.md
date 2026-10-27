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

## 3. PT1 is finished and final
Recomputed blind by GPT and Gemini, all three agreeing; Gemini's first try hit a tool error and it redid it.

- **Parts-first can reach only 28% of "cannot follow" failures.** Most are too deep: the part shown itself needs
  another missing part (58%). Showing the wrong part is rare (4%).
- **Where it can reach, making is where chains die.** Of 19,472 reachable chains, 12 ended with the whole made:
  - part made 0.11;
  - whole made 0.06.

  This is MK1, CO1 and HL1's choice problem again.
- **The memory order is an artefact.** In 71% of overflows the new lesson itself is deleted, because its value is set
  just after the 12-recipe limit is applied. With the value set first, 96% would survive.

## 4. Next: MO1, a frozen nature-change study of the memory order (decided for you; not adopted)
- **Votes:** GPT (A) at 90%; Gemini (A) at 95%; mine 80%.
- **GPT's caution:** "do not adopt v8 without the creator's explicit decision". I am following it. **Nothing becomes
  live nature without you.**
- **One law:** a recipe learned from someone (taught, or copied by watching, where the same defect sits) is given its
  learned value before memory decides what to keep.
- **Arms:** c = v7, o = the setting, s = sham; 32 paired seeds.
- **Judged on:**
  - retention;
  - no loss of useful knowledge;
  - no rise in bad lessons.

  It is **not** judged on making or culture.
- **Status:** `code_mo1` is built (`v7_to_mo1.diff`: three small edits behind one setting). A smoke world shows survival
  at overflow going from 0.36 to 0.98. The zero checks pass (with the setting off it equals v7 exactly), and it is running on GitHub (run 40480396086, 96 worlds). See the end of `WORKLOG.md`.

## 5. MO1 is finished and final: NOT supported (recomputed blind by GPT and Gemini, all three agree)
- **The manipulation check failed.** With the value set first, new lessons survive an overflow 84% of the time, below
  the frozen 90% (v7: 30%). PT1's one-event replay (96%) overestimated: memories fill with lesson-valued recipes, which
  then compete.
- **Everything else passed:**
  - lessons still held a year later: +24 points;
  - useful knowledge −2%, within the limit;
  - no bad lessons;
  - making unchanged.
- By the frozen rule there is **no v8 candidate. v7 stays live.** I did not re-read the rule after the data.

## 6. Next: VC1, the value-calibration audit (read-only; decided for you)
- **Votes:** GPT (B) at 75%; Gemini (B) at 95%; mine 65%.
- **The question:** do habit values match the returns people actually go on to get? Action by action, it compares q
  with the realised discounted reward afterwards, and measures the optimism of the max look-ahead separately (GPT's
  correction).
- **Why it matters:** this decides whether any learning-rule change is justified on calibration grounds, not on making.
- **Status:** the code is built; the zero checks are running, then the cloud run. See the end of `WORKLOG.md`.

## For you to review (nothing needs you urgently)
- The PT1 decision itself.
- **MO1:** whether to re-test the memory order under a new frozen plan whose threshold allows for memories filling up, or to leave it (not supported as frozen).
- Whether teaching deeper parts (PT1: 68% of failures need two or more levels) deserves its own frozen study later.
- The hourly heartbeat expires about 3 November. Say anything after that and I'll renew it.
