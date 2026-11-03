# Council round 55: other ways to build ACL toward Bob (3 November 2026, about 14:10–14:45)

**Opinions of GPT, Gemini and DeepSeek, not sign-off.**
- **The question:** `docs/debate_round55_question_2026-11-03.md`, the same file to all three. It was asked at the
  creator's request ("yea ask gpt gemini and deepseek about it").
- **The chats:** GPT, the main chat; DeepSeek, `2552dbba-…`; Gemini, a fresh chat (`87f468c684ee5839`), because the old
  Gemini chat froze twice and lost the reply. The fresh chat got one paragraph of ACL context in addition.

## Answers
| | GPT | Gemini | DeepSeek |
|---|---|---|---|
| is ACL's road right? | "Yes, as a research approach—not as a proven route to Bob." Separate drive, autonomy and cognition. The risk: assuming survival behaviour will by itself grow an independent motivational system. | Yes, "conceptually correct": drive comes from bodily needs meeting friction. But tabular Q-learning optimises handed-down rewards, and a forgiving world removes the pressure. | Yes, "the only principled one." Two pieces are missing: a mechanism that **builds** goals (today the mind only selects), and open actions. |
| ranking | 3 open actions, 1 predictive brain, 2 evolving brains, 4 fewer scripted feelings, 5 signals, 6 scale | 3, 1, 4, 5, 2, 6 | 3 and 1 together (3 first as the testable change; tabular Q over an open action space is hopeless), then 4 (as a gradient, keeping a bodily core), 2, 5, 6 |
| the bottleneck | "primarily the action architecture, followed closely by the mind" | the mind and the actions together | the actions, jointly with the mind that learns over them; "World: not" |
| missing option | **learned goal generation**: persistent goals formed from prediction errors, discovered opportunities and competence gains, without naming which goals | **stigmergy**: leaving lasting changes in the world (marks, caches) to hold memory past death | a **goal/intention layer** (propose, hold across weeks, break into steps) and **composition** (routines built from primitives) |
| smallest first study | **PB1** in a copy of v12: arms C (v12), P (a small predictive model of immediate food and energy change, learned from each person's own experience and used in choice), S (the same model and workload, its predictions disconnected from choice). Primary: held-out prediction accuracy over a simple baseline. Then behaviour. "I would not replace tabular habits with neural networks yet." | A frozen study with a delayed-reward task (e.g., gather a thing to pass a barrier to rich food). Arms: tabular, predictive network, sham network fed noise. Metric: completed gather-then-make chains. | First a **read-only upper bound**: replay v12's decisions, give each a perfect one-step predictor of every option's outcome, and count how often the top choice would change. If about 0, stop cheaply. If not, a copy test at matched compute with a sham, guards, blind recompute. |

## Checked against the code and records
- **Gemini's "missing option" already exists in ACL.** Marks on surfaces (`marks.py`), piles and food stashes on
  tiles (`tile.pile`, `tile.stash`) and traces are all in nature. KL1 measured know-how revived through marks.
  Stigmergy is not missing; what is unknown is why it does not stop the knowledge leak. Gemini should be told.
- **Gemini's barrier task** would be a designed puzzle with a prize. It comes close to the hard rule against recipe
  chains and rewards in nature. GPT's and DeepSeek's designs keep nature as it is.
- **All three put open actions (3) first or joint first.** This matches the 2 November action and affordance audits
  (`docs/action_audit_2026-11-02.md`, `docs/affordance_audit_2026-11-02.md`).
- **GPT and DeepSeek both name the same missing piece:** goals that are built, not only selected. That is the
  creator's "own drive" in working form.

## The assistant's merged reading (for the creator; nothing frozen)
1. **The road stays.** All three agree that drive must come from being alive in a world.
2. **The wall is the action menu together with a mind that can only choose from it.** A better brain over the same
   menu would only choose better among the same things (DeepSeek).
3. **A possible order:**
   - (a) DeepSeek's cheap read-only upper bound ("would prediction change the choice?");
   - (b) GPT's PB1 if (a) shows room;
   - (c) open actions and composition as their own frozen nature-change line;
   - (d) a goal-formation layer, built on (b) and (c).
4. **Not yet run past the models:** the follow-up round, which would send this merged order to all three, with the
   correction to Gemini. It is for the creator to say whether to go on.

**Correction (14:46):** the times in the title were estimated, not read from the clock. Commit times: round 55 recorded at 14:31, round 56 at 14:40 (both 3 November, New York).
