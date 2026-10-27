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
- **Status:** the code is built; the zero checks pass and it is running on GitHub (run 40491681638). See the end of `WORKLOG.md`.

## 7. VC1 is finished and final: habits are miscalibrated (recomputed blind by GPT and Gemini, exact match)
- **Late on, habits over-value the common actions** (forage, give, talk, gather) by +0.42 compared with what people
  actually go on to get.
- **They under-value making** by −0.56.
- **Making's real returns are within 0.01 of the alternatives'**, yet the habits put it about 1.1 below.
- **The max look-ahead explains only a third** of the over-valuation.
- **This is the first case against the learning or copying rules that rests on calibration, not on wanting more
  making.**

## 8. Next: CL1, the calibration ledger (read-only; decided for you)
- **Votes:** GPT (G) at 80%; Gemini (G) at 95%; mine 80%.
- **The question:** joining HL1's exact route ledger with VC1's realised returns, which route carries the
  over-valuation: own learning, copying in talk, carers or birth? So that any later nature change targets the right
  law.
- **Status:** the code is built and the split adds up exactly in a smoke world. The zero checks pass and it is
  running on GitHub (run 40499977145). See the end of `WORKLOG.md`.

## 9. CL1 is finished and final: the over-valuation comes from copying in talk (recomputed blind by GPT and Gemini, exact match)
- **The common actions' over-valuation (+0.42) splits exactly:**
  - own experience **−0.07** (own learning never over-values them);
  - **copying habits in talk +0.39 (93%)**;
  - carers +0.09.
- **Making's under-valuation (−0.57) is own experience alone.** Its own value is about 0, against a real return of
  0.62, because it is almost never practised. Copying adds 0.03.
- **GPT predicted exactly this.** Expected SARSA is not the target. How habits are copied is.

## 10. Next: HC1, a frozen nature-change study of habit copying (decided for you; NOT adopted)
- **Votes:** GPT yes at 70%; Gemini yes at 90%; mine 70%.
- **The law:** in talk, a learner copies only the habit values for the situation the model is in (19 values), not the
  whole table (608 values). The rate and the conditions are unchanged.
- **Arms:** v7 / situation-only / sham; 32 paired seeds.
- **Judged on calibration, with GPT's rule:**
  - the common actions' over-valuation must fall by at least 0.10 (interval above 0);
  - realised returns must not fall by more than 0.05;
  - extinction and population are flags.

  Not judged on making. I did not take Gemini's stricter 60% gate, because of the MO1 lesson.
- **⚠ GPT said you should accept these thresholds before freezing.** I signed them off under sleep mode; please review
  them. Nothing becomes live nature without you.
- **Status:** `code_hc1` is built (`v7_to_hc1.diff`: one small edit behind one setting). The zero checks pass, and it is
  running on GitHub (run 40528434282).

## 11. HC1 is finished: the copying fix did not work (checked by GPT and Gemini, exact match)
- Copying only the situation at hand did not make values more accurate (+0.42 → +0.44).
- No harm either. The world stays v7.
- **Lesson:** the problem is copying *without checking against your own experience*, not *how much* is copied.

## 12. All 38 laws written down and reviewed by GPT and Gemini
- The list is in `docs/laws_of_nature_v7.md`. GPT caught 3 mistakes in my list, which I checked and fixed.
- **Both want, most of all, things to be able to exist in the world:** tools that can lie on the ground and be picked
  up, instead of vanishing.

## 13. Next: OP1, objects in the world (a nature-change study; decided for you; NOT adopted)
- **Votes:** GPT 80%, Gemini 95%, mine 75%.
- **The law:**
  - when someone has more than 3 made things, the extra one **drops on the ground** instead of vanishing;
  - anyone 12+ standing there with room in their hands picks it up.
  - Things on the ground don't rot, the same as tools on a body today.
- **No new numbers** are invented: it reuses existing rules.
- **Judged on:** do people actually pick up dropped things (at least 5%)? Not on making.
- **A test world hints:** 82% of dropped things were picked up, almost all by *other* people, within about 4 weeks.
  Tools start passing between people.
- **Status:** the zero checks are running, then the cloud run.

## For you to review (nothing needs you urgently)
- The PT1 decision itself.
- **MO1:** whether to re-test the memory order under a new frozen plan whose threshold allows for memories filling up, or to leave it (not supported as frozen).
- **If OP1 supports it:** whether to make "things drop instead of vanishing" a real law (nature v8). I will not adopt any nature change without you.
- Whether teaching deeper parts (PT1: 68% of failures need two or more levels) deserves its own frozen study later.
- The hourly heartbeat expires about 3 November. Say anything after that and I'll renew it.
