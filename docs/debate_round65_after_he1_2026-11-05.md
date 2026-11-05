# Council round 65: after HE1, a look-ahead without the familiarity bias, and remaking (5 November 2026, 17:46)

**Opinions of GPT, Gemini and DeepSeek, not sign-off.**
- **The question:** `docs/debate_round65_question_2026-11-05.md` (the same text to all three).
- **The chats:** GPT, the main chat; Gemini 3.1 Pro, chat 87f468c684ee5839; DeepSeek, DeepThink, chat 2552dbba.
- **Recorded from the replies read in the chats.** The time in the title is from the clock.

## Answers
| | GPT | Gemini | DeepSeek |
|---|---|---|---|
| 1. which look-ahead | **Ranking C → A → D → B.** First: **(c) ES2's real-next-choice expectation, frozen unchanged against v13 and the sham, on new seeds, with starvation and killing as primary safety constraints.** It estimates what the person would actually do next rather than assuming the best. (a) is the preferred alternative (no bootstrap inflation, no max over poorly sampled acts), **but immediate experienced reward may not capture delayed consequences (hunger, retaliation) and could repeat discount 0's harms**. Include (a) as an exploratory arm if affordable. Not B or D: visit weighting does not remove the bias and invites tuning. "The objective is not to maximise inventions." | **(c)** an on-policy expected look-ahead (the expectation under the person's actual policy), with explicit starvation and harm guards as primary. The max's optimism in rare states creates the familiarity bias; removing the look-ahead destroys protection. | **(a)** the person's own mean experienced r in that situation: the mean, not the max; only experienced cells; no bootstrap, so no inflation. **Fallback (c)**, which follows (a) because ES2 previously failed one guard. (b) keeps the max bias; (d) invites tuning. |
| 2. remaking | **Run both, separately:** the look-ahead test, plus a **read-only value-at-invention audit** (consequences at creation, the first value and later valuation, survival of eviction, inputs later, whether a remake becomes a choice). Test whether observable outcomes give enough information for a first value. **No intention mechanism yet.** | A read-only value-at-invention audit in parallel; then pair it with the on-policy look-ahead. | **Look-ahead first; remaking audit in parallel, read-only**: how often is a new kind's value ever updated by its own use, and does that predict surviving the 12-cap? |
| 3. estimate | (not read as a single number in the part recorded) | 95% | about 80% |

## Checked (the assistant as council)
1. **The split on the first choice.** GPT and Gemini choose (c), DeepSeek (a) with (c) as its fallback. Both can be
   tested in one frozen study: v13 / (c) / (a) / sham, with **harm guards first for each arm** (starvation rate,
   killing, population, extinction, health) and making as the co-primary.
2. **GPT's concern about (a)** is checked against the code. (a) values next week by the mean r actually experienced in
   that situation. Hunger and harm show up only if being in that situation was itself experienced as bad, which is one
   step. The max look-ahead's recursion carried longer chains, so GPT's risk is real, and the guards will show it.
3. **(c) needs porting.** ES2's code is `code_es2` on nature v11. A version for v13 must be built and zero-checked:
   the expectation over the whole softmax choice, instinct terms included.
4. **Remaking:** a read-only value-at-invention audit, as all three ask. Per new kind, it records:
   - its use and value updates;
   - its value at eviction and whether it survived the cap;
   - whether its inputs were later held;
   - whether a make option was offered.

   It can extend LD1's funnel with `judge_item` hooks.

## Merged plan
1. **A frozen nature test in a copy:** v13 / ES2-style real-next-choice look-ahead / mean-experienced-situation-value /
   sham.
   - New seeds, 200 years.
   - Primary: harm guards per arm (starvation, killing, population, extinction, health).
   - Co-primary: making (M3 and makes).
   - Not adopted unless no harm, then a confirmatory run.
2. **In parallel:** a read-only value-at-invention audit on v13 (LD1's funnel plus value tracking).
3. **No intention mechanism yet** (GPT).
