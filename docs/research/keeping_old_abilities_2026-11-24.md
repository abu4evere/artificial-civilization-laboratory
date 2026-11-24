# Keeping old abilities while learning new ones (24 Nov 2026; for the creator's principle)

The creator, 24 Nov 2026: "Bob must retain his previous abilities while acquiring new ones. Otherwise, we're just
building increasingly complicated specialized agents rather than a general mind."

**What was read: ABSTRACTS only** (arXiv abstract pages, through a page fetch); no full texts. A source suggests; only
a frozen study decides.

| Source | What the abstract says | Bearing on Bob |
|---|---|---|
| Kirkpatrick et al. 2017, "Overcoming catastrophic forgetting in neural networks" (arXiv 1612.00796; EWC) | keeps old tasks by "selectively slowing down learning on the weights important for those tasks" | Mind Lab's W3j tried slowing ALL adult learning (CK − C −136: no help). EWC slows only the weights that mattered for earlier skills: a different, untested idea for MoveVIN (236 numbers, so the importance of each is cheap to compute). |
| Abbas et al. 2023, "Loss of Plasticity in Continual Deep RL" (arXiv 2303.07507) | agents cycling through Atari games lose the ability to learn; activations grow sparse, gradients shrink; Concatenated ReLUs help | Mind Lab's W3i-W3k saw "every brain peaks soon after childhood and then declines"; the kept copy (W3k) works around it. Whether MoveVIN's decline is forgetting or lost plasticity is untested. |
| Khetarpal, Riemer, Rish, Precup 2022, "Towards Continual RL: A Review and Perspectives" (JAIR 75; arXiv 2012.13490) | a review: taxonomy of non-stationarity, methods, benchmarks and metrics; links to neuroscience under-developed | the map of the field, to read in full when a continual-learning study is drafted. |

## What follows for our work (proposals, not decisions)
1. **Measure first:** every new brain takes the Bob Profile beside its own study (now a rule; W3r amendment 5), so a
   lost ability shows as a regression.
2. **A later study, if a regression appears:** EWC-style protection of the weights that mattered for the earlier
   abilities, against W3j's uniform slowing, as a frozen test.
3. **The decline after childhood** (W3i-W3k) may be forgetting or lost plasticity: a probe could tell them apart
   (re-learn an old skill from scratch: fast = forgetting, slow = lost plasticity).
