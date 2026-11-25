# Curiosity for Body v1's consequence model (25 Nov 2026)

The Body v1 round-table agreed on a count-based consequence model with "a bonus for untried actions" and a pain-gated
poke (`D:\mindlab\body\roundtable_body_v1_2026-11-25.md`). Which bonus? **What was read: ABSTRACTS and search-result
summaries only.** A source suggests; only a frozen study decides.

| Source (read) | What it says | For Body v1 |
|---|---|---|
| Bellemare, Srinivasan, Ostrovski, Schaul, Saxton, Munos 2016, "Unifying Count-Based Exploration and Intrinsic Motivation" (NeurIPS; arXiv 1606.01868; abstract) | turns visit counts (pseudo-counts from a density model when states are too many to count) into an intrinsic reward; strong exploration gains on hard Atari games such as Montezuma's Revenge | our tables are already counts (kind x consequence; action x change): a 1/sqrt(n) bonus for rarely tried pairs is the simplest honest "untried bonus" |
| Oudeyer, Kaplan, Hafner 2007, "Intrinsic Motivation Systems for Autonomous Mental Development", *IEEE Trans. Evol. Comp.* 11(2): 265-286 (search summary of the abstract) | "Intelligent Adaptive Curiosity": a robot seeks situations where its LEARNING PROGRESS is greatest, which avoids both the already-known and the unlearnable | a better curiosity for Bob than novelty alone: prefer kinds and actions whose predictions are still improving; give up on noise (a pain-gated poke is a special case: stop where touching only hurts) |

## What follows (proposals, for the Body v1 freeze)
1. Step 1 (the frozen brain through the body) needs no curiosity change.
2. The consequence model's first bonus: count-based (1/sqrt(n+1)) per (kind, action) and per operation number; simple,
   general, no learned parameters.
3. A later study: learning-progress curiosity (Oudeyer) against the count bonus, in the Mind Lab crafting world.
