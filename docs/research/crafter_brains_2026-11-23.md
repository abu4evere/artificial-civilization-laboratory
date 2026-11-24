# How the top Crafter brains work: first reading (23 Nov 2026, for the Outside Exam)

What was read: the arXiv ABSTRACT pages only (through a page fetch) of Curious Replay (2306.15934), Achievement
Distillation (2307.03486), DreamerV3 (2301.04104), Plan2Explore (2005.05960); the Crafter paper (2109.06780) in full
text. Everything below marked "to check" comes from the assistant's background knowledge, not yet from the papers, and
must be checked in the full texts before it is used in any plan.

| Brain | Crafter score | Core idea (from the abstract) |
|---|---|---|
| Curious Replay | 19.4 | DreamerV3 + prioritized replay with a curiosity-based priority signal |
| Achievement Distillation | 21.8 (uses knowledge of the reward structure) | PPO (ResNet) + contrastive learning that "strengthens the agent's ability to predict the next achievement" |
| DreamerV3 | 14.5 | learns a model of the world and improves behaviour by imagining futures; one fixed configuration across domains |
| Plan2Explore | 2.1 (no reward) | plans to seek EXPECTED future novelty, instead of scoring novelty after reaching it; adapts zero/few-shot to tasks later |

## Candidate ideas to borrow (hypotheses only; any one is built and tested in Mind Lab first)
1. **A model of consequences** (Dreamer's world model): learn what each action does to the world and the body
   ("do at a tree -> wood"). MBb plans with fixed body physics for moves only; it has no learned "what happens if".
   This is the same gap BX1's school showed in ACL. (To check: Dreamer's RSSM details.)
2. **Curiosity about surprise, not staleness** (Plan2Explore; Curious Replay): MBb's curiosity is "how long since I
   looked there". These brains are curious about what their own model cannot yet predict (to check: Plan2Explore uses
   ensemble disagreement). That would make a brain try "do" on new things.
3. **Learn more from surprising memories** (Curious Replay): replay the moments the model got wrong more often; a
   possible analogue of sleep and dreaming.
4. **Predict what comes next** (Achievement Distillation): AD uses achievement labels, which our rules forbid (no named
   rewards); a body-only analogue would be "predict the next change in my own inventory and body".
5. Not allowed: SPRING (an LLM reading the paper). No LLMs inside our minds.

Next: read the full texts of DreamerV3, Plan2Explore and Curious Replay (methods sections) and label them.
