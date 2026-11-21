# Learned eyes for planning brains (research notes, 20 November 2026)

Why: W3o ("raw eyes") tests whether the living brain (W3n's DriveVIN, a value-iteration network on a map memory) still
works when its world is not sorted into wall, food and shelter layers. GPT and Gemini both expect the "colours that
change" arm to fail, because the brain's eye is one linear 3 × 3 layer. These notes look for how others gave a planning
network its own learned perception. A source suggests; only a frozen study decides.

## What was read
| source | read | what it says (in my words) | bearing on Mind Lab |
|---|---|---|---|
| Tamar, Wu, Thomas, Levine, Abbeel, *Value Iteration Networks*, NeurIPS 2016 (arXiv 1602.02867) | search-result excerpts only | The planning step is a convolution repeated K times, trained end to end; the network learns to map observations to a planning computation. In their image experiment, a planner fed with an obstacle map from a separately trained classifier succeeded about 90% of the time: seeing obstacles in raw images is the hard part. | Our brain is this design. Its "eye" today is a single linear layer on hand-sorted layers. |
| Gupta, Tolani, Davidson, Levine, Sukthankar, Malik, *Cognitive Mapping and Planning for Visual Navigation*, CVPR 2017 (arXiv 1702.03920) | abstract (and search excerpts) | A learned mapper builds a top-down map from first-person images and a differentiable value-iteration planner uses it; the mapper is trained by the planner's needs, end to end. The learned mapper did better than a hand-made (analytic) one, and planning mattered most with raw images. | The strongest precedent: let the planner's error teach the eye (and later the memory writer) what to see, instead of the designer's labels. Our memory writer is still fixed. |
| Ishida, Henriques, *Towards real-world navigation with deep differentiable planners*, CVPR 2022 (arXiv 2108.05713) | abstract | Differentiable planners fail at long horizons because nothing forces a big enough penalty on every collision. They add a structural constraint to learn impossible moves explicitly, and a memory-efficient map for limited cameras; it then worked on real robot images. | When walls no longer have their own layer (RV), the brain may lose its sense of "can't go there". A learned "blocked here" output could help. |

## Ideas for the step after W3o (for the creator; not a plan)
1. **A small learned eye:** replace the brain's linear first layer with a tiny non-linear one (for example 3 × 3
   convolution, a rectifier, then a 1 × 1 mix), trained by the planner's error as in Gupta et al. It can learn
   combinations and shapes (a 2 × 2 patch, a line), which a single linear layer cannot.
2. **A learned "blocked" map** (Ishida and Henriques): the eye also outputs where moves are impossible, used to stop the
   planner passing value through walls.
3. **Later, a learned memory writer:** the map memory stores what the eye saw (features), not the designer's labels.
   This is the deeper version of "raw eyes", and the one closest to a baby learning what things are.
4. Each is one change at a time, judged on W3's lands against the current brain, with the bare (no-reflex) reading,
   as W3o does.
