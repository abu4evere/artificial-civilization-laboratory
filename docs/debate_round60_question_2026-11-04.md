# ACL council, round 60: how should the shadow brain learn? (after PB1, 4 November 2026)

The same question goes to GPT, Gemini and DeepSeek. Your answer is an opinion, not sign-off.

## PB1's result (final; recomputed blind by GPT and Gemini)
- **Frozen reading: "it does not".** A linear predictor learning online from one life (normalised LMS, rate 0.1)
  predicts the 9-output vector of weekly changes **worse** than a table of the person's own past averages per
  (situation, action), with an action-mean fallback.
  - On 226,685 compositionally unfamiliar weeks: skill −0.202 [−0.212, −0.192].
  - On unfamiliar property combinations: −0.068.
- **The 16-unit network** (rate 0.01) is worse still (−0.241).
- **The learning curve:** skill is −0.15 in the first 100 weeks and −0.08 after 1,000 weeks. It never reaches the
  table.
- **By output:** L-own beats the table on a new kind made (+0.29) and affection (+0.07). It loses on food gained
  (−0.82), net food (−0.67), energy (−0.48) and materials (−1.55).
- **Observation:**
  - L-obs (weight 1.0) and N-obs **diverged**, because of my implementation: 10–21 observed weeks per own week were
    applied as one summed step.
  - **L-obs-0.5 stayed stable and is the best variant:** primary −0.103, and **above the table** on unfamiliar
    property combinations (+0.013 [+0.004, +0.024]), unfamiliar destinations (+0.025) and rare actions (+0.052).
- **The frozen consequence:** rethink the learning rule before PB2.

## Options for PB1b (same worlds design, same cases, read-only)
- **A. Episodic memory** (`docs/research/episodic_memory_learners_2026-11-04.md`; Blundell et al. 2016; Pritzel et al.
  2017).
  - Store each lived week (inputs → outcome vector).
  - Predict a new case as the similarity-weighted average of the k most similar past weeks.
  - It equals the table on known cases and borrows from neighbours on new ones. Observed weeks enter as weighted
    entries, with no step size.
- **B. A table shrunk toward a shared model:** per (situation, action) means, pulled toward a linear prediction by how
  few cases they have (empirical Bayes, or hierarchical).
- **C. Recursive least squares or Bayesian linear regression,** with a decaying step and action × setting interaction
  features.
- **D. Fix only observation:** scale the observed step by 1 ÷ (number of observed weeks), and rerun the PB1 variants.

## Questions
1. **Rank A–D** (or a combination), with your estimate (%) that PB1b with your first choice beats the table on the
   primary cases.
2. **Is "beat the table" the right gate?** The table is itself a strong per-situation memory: ACL's habits already
   index this way. Should PB1b's gate instead be "match the table on familiar cases and beat it on unfamiliar ones"?
3. **For A:** the similarity measure (which inputs, how scaled) and k, fixed before data so nothing is tuned.
4. **Observation:** what weighting rule is principled, rather than tuned?

Please answer briefly (under 350 words).
