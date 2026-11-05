# Learning from few experiences: episodic memory (4 November 2026; the brain road, after PB1)

**Why:**
- PB1 (final): a fixed-step linear predictor and a small network both predicted worse than the habit-style table
  (−0.20 on unfamiliar weeks).
- The table averages exactly. The online learners kept chasing noise and could not represent combinations such as
  this action, on this tile, in this season.
- Round 60 asks how the brain should learn instead.

**A source suggests; only a frozen study decides.**

## Sources
1. **Blundell, Uria, Pritzel, Li, Ruderman, Leibo, Rae, Wierstra & Hassabis 2016,** "Model-Free Episodic Control",
   arXiv 1606.04460.
   - **Read:** the abstract only.
   - **What it says:** deep reinforcement learning needs millions of interactions, while people exploit a rewarding
     nuance "upon first discovery". In the brain this fast learning is thought to depend on the hippocampus and
     episodic memory. A simple model of hippocampal episodic control learned a highly rewarding strategy
     significantly faster than the deep methods, and did better on some harder tasks.
2. **Pritzel, Uria, Srinivasan, Puigdomènech, Vinyals, Hassabis, Wierstra & Blundell 2017,** "Neural Episodic Control",
   arXiv 1703.01988.
   - **Read:** the abstract only.
   - **What it says:** a "semi-tabular" value function: a buffer of past experience with slowly changing state
     representations and rapidly updated value estimates. Neighbours are looked up and weighted by similarity. It
     learns significantly faster than other general-purpose deep agents.

## What it suggests for ACL (the assistant's reading)
1. **This is the learner PB1's failure points to.**
   - **The table won** because it remembers exact cases and averages them.
   - **What it lacks is sharing:** an unfamiliar case gets only the action's mean.
   - **An episodic memory does both:** it stores each lived week (inputs → outcome vector). For a new case it predicts
     the **similarity-weighted average of the most similar past weeks**. A known case returns its own average, as the
     table does; a new case borrows from its nearest neighbours.
2. **It fits the brain design:** it is "memory that acts" (capability 2) and a predictor (capability 3) at once. It
   is biologically motivated (the hippocampus), and it learns from few experiences, which is ACL's data problem
   (about 2,000 choices a life).
3. **Observation fits naturally:** others' visible weeks go into the memory as their own entries, weighted. It has no
   step size, so PB1's batching flaw cannot recur.
4. **A test (for round 60):** PB1b, read-only like PB1, with the same cases. An episodic predictor (k nearest weeks,
   similarity-weighted, own and own + observed) is tested against the same table baseline and against L-obs-0.5.
5. **The cost:** memory grows with life. That is about 2,000 entries a person, which is small.

## Not read (to find next)
- The full texts (memory size, the kernel, how similarity is learned).
- Gershman & Daw 2017, on episodic memory in reinforcement learning (a review), for the biology.
