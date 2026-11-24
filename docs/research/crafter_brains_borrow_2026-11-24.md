# What to borrow from the top Crafter brains (24 Nov 2026; the creator: "learn it and if there are things we should take, take it use in ours")

Follows `crafter_brains_2026-11-23.md` (abstracts only). **Read now, in full text (arXiv PDFs, text extracted
locally), the method sections of:** Plan2Explore (Sekar et al. 2020, arXiv 2005.05960, sec. 3.1, 5); Curious Replay
(Kauvar et al. 2023, arXiv 2306.15934, sec. 3.3-3.5, 4.4); Achievement Distillation (Moon et al. 2023, arXiv 2307.03486,
sec. 3-4); DreamerV3 (Hafner et al. 2023, arXiv 2301.04104, sec. 2-3, appendix hyperparameters). Results sections were
skimmed, not studied. A source suggests; only a frozen study decides.

## What each brain does (from the method sections)
| Brain | The mechanism, in plain words | Read |
|---|---|---|
| Plan2Explore | Five small one-step predictors guess the next state from (state, action). Where they **disagree** (variance of their guesses), the brain does not yet know what happens, and that disagreement is its curiosity reward. As it learns a place, the predictors agree and the place becomes boring. It plans in imagination toward expected disagreement. Ensemble of 5 (sec. 3.1, 4). | full method |
| Curious Replay | When the brain re-learns from memory, it replays more often the moments it **predicted badly** and the ones it has **replayed least**: priority p = c·β^v + (\|L\| + ε)^α (eq. 1; v = times replayed, L = the world model's error). Added to DreamerV3: Crafter 19.4. | full method |
| Achievement Distillation | Plain PPO, made bigger (channels 64-128-128, hidden 1024) with layer and value normalization, already beats DreamerV3 (15.6 vs 14.8, sec. 3.1). Then: the brain learns to **predict the next "unlock"** (a big change, represented as the change between two consecutive states) from where it is, and **remembers its last unlock** as part of its state (sec. 4.1-4.3). It uses WHEN an unlock happened (from the reward), not its name. | full method |
| DreamerV3 | Learns a world model (what my action does next) and practises in imagination 15 steps ahead; symlog squashing and return normalization make one setting work everywhere (sec. 2-3; H = 15). | method skimmed |

## What our brain lacks, in their terms
MBb (MoveVIN, 236 numbers) plans with **fixed body physics** and a **learned reward map from fixed eye layers**. It has:
- no learned model of consequences ("if I step here / do this, what happens to my body?"): the gap BX1's ACL school
  showed (it learned how a week felt, not which choice caused it), and Mind Lab's own open gap since W3o ("I ate where
  it was this colour, so here this colour is food": learning a meaning within one life);
- curiosity by staleness ("how long since I looked"), not by not-knowing;
- no memory of its last big change.

## Borrow list, ranked by fit with our rules (no LLMs; no named rewards; the body and feelings only)
1. **A consequence model with disagreement-curiosity (Plan2Explore), first.** A small ensemble (5, as in the paper)
   learns within one life to predict the body's change when entering a cell from what the cell looks like (its
   colours). Its mean prediction is the cell's learned meaning (feeds the reward map where the sorted "food" layer is
   now); its disagreement is the curiosity (replaces staleness). Directly targets W3o's RV gap. Fits the rules: the
   target is the body's own change, not a named outcome.
2. **Replay the surprises (Curious Replay)** as the brain's learning-from-memory, e.g. in rest/sleep (W3m's reflex
   already rests it): replay moments with high consequence error and few replays. A second arm or the next study.
3. **Remember the last big change (Achievement Distillation's memory)**: "what changed in my body/hands last" as an
   input, body-only (no labels). Later, for Crafter-like chains (wood -> table -> pickaxe).
4. **Bigger and normalized (AD's PPO lesson)**: size and normalization matter more than cleverness. Our 236 numbers are
   tiny; a scale test belongs in the Bob Profile work. Later.
5. **Not allowed:** SPRING (an LLM reads the paper) and any achievement-labelled reward.

## Next
Draft W3r (borrow 1) in `D:\mindlab\workbench\W3r\questions_draft.md`, then council (GPT, Gemini, DeepSeek), frozen
plan, checks, the creator's sign-off.
