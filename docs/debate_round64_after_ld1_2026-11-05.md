# Council round 64: after LD1, a general law for the look-ahead, and the path to remaking (5 November 2026, 13:08)

**Opinions of GPT, Gemini and DeepSeek, not sign-off.**
- **The question:** `docs/debate_round64_question_2026-11-05.md` (the same text to all three).
- **The chats:** GPT, the main chat; Gemini 3.1 Pro, chat 87f468c684ee5839; DeepSeek, DeepThink, chat 2552dbba.
- **Recorded from the replies read in the chats.** The time in the title is from the clock.

## Answers
| | GPT | Gemini | DeepSeek |
|---|---|---|---|
| 1. the look-ahead | **A fault in the learning mechanism**, not evidence that foresight is harmful. Two problems: an estimation bias (the max over poorly sampled situations rewards familiarity) and a real opportunity cost (making costs a week of feeding; not a fault). **The general law: habits learn experienced consequences; a separate predictive system estimates the future when planning.** That makes discount 0 for habit learning a principled separation, "not a number chosen to increase inventions". Not a longer horizon (it amplifies the bias); visit-weighted or expected values do not fix the mixing of habit and planning. **Before live nature: a frozen harm-check of discount 0 against v13** (survival, food, social behaviour, extinction; scrutinise the extra extinction). | **A demonstrated mechanical fault** (the comment says prospects; it measures familiarity). **Removing the look-ahead from habits is the only clean general law**; foresight belongs to model-based systems. Discount 0 in habits "is not tuning; it removes a flawed model-free temporal approximation". | **A law to replace, not a fault-fix**: the change is broad, so it is tested in a copy as a nature change. **The law: habits learn only from experienced r; foresight is left to the predictor or episodic system** (model-free / model-based separation, not tuning). Expected values fix direction but not the scale inflation; "learned by visits" keeps the max bias; a longer horizon is worse. "So: remove look-ahead from habits." |
| 2. first R test | **Value at invention, then recipe memory.** A minimal general rule: when an agent creates or discovers something, its first value reflects the observable consequences of that experience, not 0. It applies to every new object, with no value for novelty or for making. **First a read-only counterfactual audit**, then a frozen intervention in a copy, with a control separating retention from valuation. Value alone cannot produce deliberate remaking; intention comes next. Do not just raise the cap. | **Value at invention:** a new recipe's first value anchored to the experienced outcome (r) of its discovery week, not 0. | **Value at invention, not the look-ahead:** a new kind's value set or updated from what it did when made, by the same value-learning rule as use. No named reward. Primary: the share of new kinds that survive week 1 and are later offered. Co-primary: R given the recipe is held and the inputs reachable. Then intention; then the cap. The look-ahead is a separate, broad law. |
| 3. estimate | 96% (a read-only value and retention audit); 75% that an outcome-grounded value would improve the opportunity to remake | 95% | about 78% |

## Checked (the assistant as council)
1. **All three name the same general law:** the habit system learns only from experienced outcomes, with no
   look-ahead in its update, and foresight is left to other systems.
   - It is implemented by the existing setting (`discount` 0) in the habit update.
   - They differ on the path: GPT and Gemini call the current look-ahead a fault; DeepSeek a law to replace by a full
     test.
   - **Decision:** take the stricter path, DeepSeek's and GPT's harm check. A frozen nature-change test in a copy
     with a sham and harm guards, then a confirmatory run on new seeds, then the safe-path adoption. Two earlier frozen
     studies (PB3, LD1) already show the effect on new seeds, but neither was framed as an adoption test.
2. **Foresight left to other systems:** v13 already keeps other forward-looking rules, such as E9's anticipation of
   seasonal shortage (`anticipation_weight`) and the know-how beliefs. The law does not remove foresight from people;
   it removes it from the habit table.
3. **Value at invention, checked in the code:**
   - A made thing's value is learned **only when it is used**: `knowhow.judge_item` (lines 49–58), called from the
     actions where a thing helps work, travel or warmth.
   - A new kind therefore has value 0 until used, and is often evicted before then.
   - "What it did when made" has no observable outcome in the code today (nothing is felt at making), so the design
     needs care, not a fixed number. Candidates for the next design round: the value of the person's most similar
     known kinds, which is generalisation from experience as in PB1b; or a first use as part of making.
   - GPT's read-only audit comes first.
4. **GPT's extinction point:**
   - PB3: c0 +1 extinct world, seed 23311, which also died out in the sham.
   - LD1: c0 2 extinct, v13 1; seed 23423 died out in both.

   The harm test will report each extinction with the matching v13 and sham worlds.

## Merged plan
1. **Now:** a frozen nature-change test of the law "habits learn only from experienced outcomes" in a copy.
   - Arms: v13, the law, sham. New seeds.
   - Primary: the harm guards: living-weeks, extinctions with paired worlds named, food, health.
   - Co-primary: M3 and makes.
   - Described: social acts, R.
   - Then a confirmatory run on new seeds, and the safe path.
2. **Then:** a read-only audit of value at invention (GPT), followed by a design round.
3. **Later:** intention to remake; recipe memory.
