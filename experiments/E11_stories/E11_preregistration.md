# E11 — Stories that carry a hard season (S1): pre-registration (FROZEN)

**Status:** signed off by the creator on 2026-10-06 (S1 only; two strengths; built on E10's code; leak test a hard
fail; repeat planning a headline outcome) and frozen as `E11-frozen` before any E11 code was written. Not to be
edited after the results.

## 1. Why

E9.4 measured a self-erasing lesson: preparing removes the hunger that taught it, and the lesson falls below the
threshold (about 0.4) at which anyone prepares. A lesson that lasts must outlast the experience. The O4 pilot found
that stories of starvation deaths already reach a median of 26 people each and are told for decades, but carry
neither cause nor season. S1 lets them carry both. The creator's question: can the channel that preserves social
memory preserve ecological memory?

## 2. The mechanism, exactly

Built on the E10 code (O2 on, O3 off). Two additions:

**(a) The cause and season of a death are known with its story.** When anyone dies, the world records, under the
death's event id, its cause and the season it happened in. Stories already carry that id, so whoever hears a story of
a death learns, exactly, what it was of and when. (Nothing about how stories are chosen, retold, believed or changed
in the telling is altered; no new random draws are made, so with S1 switched off the world is exactly E10's.)

**(b) A story of a death from hunger leaves a lesson.** Whenever a listener hears such a story and does not doubt or
reject it (it is accepted as new, or it is one they already knew), their lesson for that season is raised to at least

```
STORY × (their credence in the teller) × (the story's strength as told)
```

using E10's `expect["loss@s"]`, which fades at grief's rate (0.985 a week) and is felt a season early only in the pull
to get food. Hearing the story again renews it, whether or not anyone is hungry now.

The story says only what happened. Nothing tells anyone to store food, make anything, or that winter will come.

## 3. Arms and numbers

| arm | code | O2 (own child lost) | STORY |
|---|---|---|---|
| 0 | E7 code (control) | – | – |
| S1-low | E11 code, loss weight 1.0 | on | 0.25 |
| S1-high | E11 code, loss weight 1.0 | on | 0.50 |

STORY has no precedent in the code, so (the creator's E10 rule) it is tested at two values rather than guessed once.
**The O2-only comparison** is E10's O2 arm: the E11 code with STORY = 0 must reproduce it exactly (section 5). No other
values will be tried in E11. Seeds 301–304, 120 years.

## 4. Scripting review

| question | answer |
|---|---|
| Storing, putting, carriers, containers or heaps mentioned? | No. |
| Anything fires because it is autumn? | No. A lesson for a season is felt one season ahead, in every season. |
| A fact about winter not lived, seen or heard? | No. Only the cause and season of a real death, told by someone. |
| An instruction carried by a story? | No. Stories carry who died, of what, when. |
| Changes how anything is valued, or stealing? | No. |

## 5. Validity (kill criteria)

- The probe changes nothing (state hash, 20 years, both codes).
- **Zero-story check:** the E11 code with STORY = 0 (loss weight 1.0) reproduces E10's O2 arm population at every
  10-year sample (seed 304), and so E10's O2 runs stand as the O2-only comparison.
- Arm 0 reproduces the saved runs; code unchanged during the runs; no crashes.
- **Leak test (hard fail):** adults who never lost a child to starvation and never heard (accepted or knew) a story
  of a death from hunger forage in autumn within ±10% of the same group in Arm 0, pooled.

## 6. Order of reading (binding: the creator's chain)

1. hunger deaths occur; 2. their stories spread; 3. stories are accepted; 4. autumn foraging rises in people who never
lost a child; 5. more people prepare (hold 80+ in autumn); 6. **some prepare in successive years**; 7. only then,
winter outcomes. A change at step 7 without steps 1–6 is treated as noise.

## 7. Predictions

1. **Stories move people (S1-high).** Adults who heard a hunger story in the past year and never lost a child forage in
   at least 1.2× as many autumn weeks as the same group in Arm 0, pooled.
2. **More planners (S1-high).** At least 1% of adult-autumns reach 80 food in hand (Arm 0 in E10: 0 of 11,832).
3. **Preparation survives success (headline, S1-high).** At least 10% of planner-autumns are followed by planning in
   the next autumn (E9.3: 1 of 113), with at least 20 planner-autumns in all.
4. **Dose response.** Steps 4 and 5 are both larger in S1-high than in S1-low, pooled.
5. **Better-stocked carers (S1-high).** The share of child-winters whose carer holds 20+ food is at least 5 points
   above Arm 0's, pooled.
6. **Children saved (S1-high), read only if 1, 2 and 5 hold.** Children's winter starvation per child-winter is at
   least 20% lower than Arm 0's, pooled.
7. **No leak** in either S1 arm.

**What the result would decide:**
- 1 fails: stories of hunger, even renewed for decades, do not move behaviour through this machinery; the cultural
  memory route fails in this form.
- 1–2 hold, 3 fails: stories raise preparation but it still does not survive success; the lesson is erased even with
  stories, and something more durable than a told memory (a custom, a kept store) is the next question.
- 1–3 hold: the first lesson in ACL that outlives the people who suffered it. Then steps 5–7, and the 300-year
  follow-up with carrier and novelty predictions frozen first.
