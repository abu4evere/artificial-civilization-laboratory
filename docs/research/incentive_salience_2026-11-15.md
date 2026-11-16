# Incentive salience: a need that changes what a cue is worth (research note, 15 November 2026, heartbeat)

**Why now:**
- Mind Lab W3c (running) adds a "need gate": a strong need turns down the parts of the reward map not about it.
- W3b had found hunger drowned at about 0.009 against 0.9 for the base map.
- Its first test-only result: the gate added at test time to W3's D3i did not rescue it (survival 0), but the trained
  arms are still running.
- This note looks for the biology behind "a need takes over".

**What was read:** the abstract of the paper below, through the journal's page (summarised by a fetch tool).
Nothing from the full text.

## Zhang, J., Berridge, K. C., Tindell, A. J., Smith, K. S., & Aldridge, J. W. (2009). A neural computational model of incentive salience. *PLoS Computational Biology* 5(7): e1000437.
**What the abstract says:**
- A change in the body's state (hunger, salt appetite, drugs) can at once change how much a learned cue is "wanted",
  with no new learning about the reward.
- The model combines cached values learned earlier with the current body state, through a gain on the learned value:
  multiplicative for shifts in strength, additive for reversals.
- **The shift is specific to the need:** salt appetite raises the pull of salt cues, not others.
- **The example:** rats taught that an intense salt taste was unpleasant showed strongly raised firing, and approached
  the cue linked to it, once sodium-deprived, without tasting the salt again in the new state.

## Bearing on Mind Lab (a source suggests; only a frozen study decides)
- **W3's map already has the multiplicative part:** hunger s multiplies the learned food link (s·W_s).
- **The abstract describes need-specific gain on the relevant cue, not a damping of everything else** (W3c's gate).
  So W3c tests a stronger, broader form than this model states.
- **The instant revaluation in the abstract happens in the valuation.** W3c's step 0c changed the valuation at test time
  in a brain whose downstream planner and hand were trained without it, and it did not help.
  - That fits a reading in which the rest of the brain must have learned with state-dependent values in place, which
    is what the trained arms (G, Gi, GYFR) test.
  - This is an interpretation, not something the paper states.
- **A possible later variant (needs the creator):** a need-specific gain (raise the food channel's weight with hunger,
  more steeply than linearly) instead of damping the base map. The two forms could be compared.

## Source
- [Zhang et al. 2009, PLoS Computational Biology](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000437)
  · [Semantic Scholar record](https://www.semanticscholar.org/paper/A-Neural-Computational-Model-of-Incentive-Salience-Zhang-Berridge/45291637057c4efe558de38c81ed562569119351)
