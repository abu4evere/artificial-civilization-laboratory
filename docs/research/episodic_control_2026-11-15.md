# Episodic control: a fast memory that acts (research note, 15 November 2026, heartbeat)

**Why now:**
- W3 (drives only) failed: the hunger link never learned to point at food from sparse reward in 2,000,000 steps.
- WF showed that a fast store of "what just worked" relearns at once when it acts (WSLS, about 1.00). Replayed at night,
  it also teaches the slow network (0.45–0.51).
- The proposed W3b would give the drives brain such a store. These two works are the direct precedent.
- They are not in `mindlab_sources_2026-11-15.md` (that note covers McClelland et al. 1995 and Oh et al. 2018).

**What was read:** abstracts only, from the publishers' and arXiv pages. Nothing below goes beyond the abstracts.

## 1. Lengyel, M., & Dayan, P. (2007). Hippocampal contributions to control: the third way. *NIPS 20*, 889–896.
- **Claim:** beside planning with a model (prefrontal) and habits (striatum), there is a third control system, based
  on episodic memory (hippocampus).
- **It is most useful at the very start of learning,** before habits form, and in complex, noisy settings.
- **Control later passes from the episodic system to habits.**
- **Bearing on Mind Lab:**
  - this is the pattern WF found: the store acts at once (WSLS), while replay slowly builds the habit (RP);
  - W3's brains are always "early" in a hard world with sparse food, which is where the paper says episodic control
    pays most.

## 2. Blundell, C., Uria, B., Pritzel, A., Li, Y., Ruderman, A., Leibo, J. Z., Rae, J., Wierstra, D., & Hassabis, D. (2016). Model-free episodic control. arXiv:1606.04460.
- **Claim:** a simple model of hippocampal episodic control learns sequential tasks much faster than the deep reinforcement learning of the time,
  and reaches higher reward on some hard tasks.
- **How it works (from memory, not in the abstract; to be checked in the full text):** it stores the best return seen
  after each state and action, and acts on the best remembered return.
- **Bearing on W3b:**
  - the first food found by chance is exactly the kind of rare, rewarding discovery such a store keeps and reuses at
    once;
  - in W3, nothing kept it.
  - The author list above was checked on the arXiv abstract page (nine authors).

## What these sources suggest (a source suggests; only a frozen study decides)
- **For W3b:** a fast store keyed by place ("food was found here, after this much hunger"), which can act at once when
  the same need returns, plus night replay into the slow planner.
- **This matches WF's design,** moved from boxes to places. It needs the creator's OK and a council before any
  freeze.

## Sources
- [Lengyel & Dayan 2007, NeurIPS proceedings](https://papers.nips.cc/paper/3311-hippocampal-contributions-to-control-the-third-way)
- [Blundell et al. 2016, arXiv:1606.04460](https://arxiv.org/abs/1606.04460) ·
  [Semantic Scholar record](https://www.semanticscholar.org/paper/Model-Free-Episodic-Control-Blundell-Uria/ba378579fb44007db9f02699889721dcd2b5b3a0)
