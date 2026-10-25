# M1 — A thousand years on nature v6: findings (recomputed independently; final)

Frozen as `M1-frozen` (Revision 1); run on GitHub Actions (run 40214835191). 192 worlds (arms LP, D80, C20; 64 seeds
each, 16801–16864), 1,000 years. Every number comes from `analyse_m1.py` (written before data); full tables are in
`results.md`. Validity: zero checks pass, all worlds present, one fingerprint (`code_v6`).

## The answer

**Over a thousand years, what people know and use does not build up. In every world that survived, it wore away.**
The frozen trajectory rule puts every surviving world in **erosion**: LP 45 of 45, D80 24 of 24, C20 16 of 16. None
was classed as maintenance, rediscovery or improvement.

**Co-primary outcomes (LP, primary arm; 45 worlds alive at year 1,000; population early 120, late 108):**
- **A4, food owed to tools per adult forage-week:** early 0.917, late 0.049. Late is 0.054 of early [0.046, 0.063]:
  **declines** (about 95% less).
- **B-retained, useful kinds still known 25 years after their maker's death:** early 0.137, late 0. **Declines.** The
  late value is 0 in all 18 worlds where late kinds could be followed. In the other worlds no useful kind made in years
  900–950 had a maker who died and was followed for 25 years.

**Secondary, LP:**
- Crafting skill falls to a tenth (mean adult 0.54 to 0.05).
- Unique recipes known fall to an eighth (278 to 37).
- Deliberate making falls 96% (1.92 to 0.07 per person-decade).
- The best tool held falls by a quarter (1.95 to 1.44).
- Tools still cover all eight uses early and 7.4 late (unclear).
- **The ladder for new kinds after year 100:** 12,655 candidates. None was made by three people within ten years.
  None lasted, was adopted, outlived its maker or was improved.
- **Traditions:** 4,290 found, but only 181 began after year 100.
- **Shared marks** per world: 102 early, 1.2 late.

**The cohort test (born at the start vs born in years 900–950, at age 30):**
- Late-born people know a fifth as many useful recipes (11.4 to 2.4) and have a tenth of the crafting skill. Their
  best tool is worse (1.17 to 1.04).
- **Only one measure builds:** the share of a 30-year-old's useful recipes learned from others, 0.29 to 0.40 (ratio
  1.38 [1.26, 1.51]).
- That is more learning from others, but of far less. Read with the fall in total, it is a larger share of a shrinking
  stock, not a growing one.

**D80 and C20** (secondary, described) show the same picture.
- Survival: D80 24 of 64 alive at year 1,000; C20 16 of 64.
- A4 falls about 96% in both.
- B-retained late is 0 in both.
- Every surviving world is erosion.

## Against the prior (written before data)

The assistant expected LP to "hold" on A4, B-retained, A1 and the cohort test, and to decline only on skill and
making. **The prior was wrong in the pessimistic direction:** both co-primary outcomes decline, and so does almost
everything else. Only the zero lasting novelties after year 100 matched.

## What follows (frozen)

"If LP declines: a study of loss (where retention breaks, with CA1–CA3's methods), not a longer run." So a 10,000-year
run is not justified now. The next study should trace where and when knowledge is lost across the centuries, and why
skill and deliberate making fall even while populations stay alive. The creator decides.

## For the mission

This is the clearest answer yet for level 4 ("knowledge outlives its maker and builds up"): **on nature v6, it does
not.** In ACL's worlds, the early generations' knowledge decays rather than accumulates, the opposite of human history.
A finding about this nature, not a failure of the project: it says the ratchet is missing, and the loss study looks
for where.

Limits: v6, not v7, as frozen. Survivorship: "late" describes worlds alive at year 1,000.

## Independent recompute (25 October 2026)

GPT recomputed the co-primary outcomes from the raw files without the script; every number matches (`recompute_m1.md`). Caveat recorded: the late B-retained zero rests on 35 late kinds in all (25 in LP), all lost.
