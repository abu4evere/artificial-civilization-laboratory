# Learning a meaning within one life: sources (22 Nov 2026, sleep-mode research)

**The open question (from W3o, `D:\mindlab\workbench\W3o\findings.md`):** the brain learns fixed colour meanings over
training, but when colours are dealt anew on each land it cannot work out within a life which colour is food. What
kind of mechanism lets a small brain learn "here, this colour means food" from its own few meals?

## What was read
- **Miconi, Clune and Stanley (2018), "Differentiable plasticity: training plastic neural networks with
  backpropagation"** (ICML; arXiv 1804.02464). *Abstract read; the search summary added detail.* Each connection has a
  fixed weight learned slowly plus a Hebbian trace that changes within a life; how much each connection is plastic (α)
  and how fast the trace moves (η) are learned by gradient descent. Plastic networks beat fixed ones on memorising new
  images, on one-shot learning, and in a maze exploration task.
  - Bearing on W3o: a plastic link from the eyes' colour layers to the feelings (reward) map, with a trace written at
    each meal ("the colour under me when I ate"), is the smallest version of "learn a meaning within one life". The slow
    training would learn how plastic that link should be, not the meaning itself.
- **Ba et al. (2016), "Using fast weights to attend to the recent past"**: *record only (named in the search summary).*
  Recurrent networks with fast-changing Hebbian weights; the forerunner of the same idea.
- **Wang et al. (2016), "Learning to reinforcement learn"** (arXiv 1611.05763). *Abstract-level (search summary).* A
  recurrent network trained by ordinary RL across many tasks comes to run its own fast learning inside each episode
  ("meta-RL"); the slow learner learns the task family, the recurrent state does the fast learning.
  - Bearing: the alternative to plasticity. Mind Lab found earlier that a learned recurrent memory did not learn
    (W2) while a short window did (Cradle C1); plasticity is the smaller, more direct step.
- **Miconi et al. (2023), Hebbian plasticity in recurrent networks; "fast weight programming" reviews (2025)**:
  *record only (search results).*

## What it suggests (a source suggests; only a frozen study decides)
- A study in RV's world (colours dealt per land): DriveVIN plus a plastic colour-to-value link whose trace is written by
  the brain's own meals and reset at birth; the slow training learns the plasticity's size and speed (Miconi's α, η).
- Controls: the same brain with the trace frozen at zero (no within-life learning), and the trace written at random
  (a sham); the probe of W3o (toward food when hungry) on fresh colour deals.
- Named limit to state in the plan: the trace's rule (Hebbian, written at meals) is designer-given; what it learns is
  the world's.

Sources: [Miconi et al. 2018, arXiv](https://arxiv.org/abs/1804.02464) ·
[PMLR PDF](http://proceedings.mlr.press/v80/miconi18a/miconi18a.pdf) ·
[Wang et al. 2016](https://arxiv.org/abs/1611.05763) · [Hebbian and gradient plasticity in RNNs (2023)](https://arxiv.org/pdf/2302.03235) ·
[Fast weight programming review (2025)](https://arxiv.org/pdf/2508.08435)
