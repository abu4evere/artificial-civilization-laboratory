# Research notes: the max look-ahead and inflated habits (for CO2's reading and a possible later study), 30 October 2026

Following the creator's "do research all the time". **What was read is labelled;** "abstract" means the abstract or
publisher summary as returned by a web search, not the full paper. A source suggests; only a frozen study decides.
Any change to ACL's learning rule is a nature change: **the creator's decision only.**

## Why these sources
ACL's habits are learned by one-step Q-learning (`biology._learn`):
`q ← q + lr × (r + γ × max_a' q(next, a') − q)`. ACL's own studies traced the trouble to it:
- **HL1:** the max look-ahead grew from 0.06 to 1.26 while rewards stayed flat.
- **VC1:** common actions were over-valued (+0.418), and making under-valued (−0.558).
- **CL1, EX1:** making's under-valuation comes from own experience, not from copying.

CO2 (running) asks whether habit still carries making's deficit under v9.

## 1. van Hasselt 2010, "Double Q-learning", NIPS 2010 (pp. 2613–2621)
https://proceedings.neurips.cc/paper/3964-double-q-learning.pdf — **read: abstract and search summary.**
- Q-learning uses the **maximum of the estimated action values** in place of the maximum expected value. This
  introduces a **positive (overestimation) bias**.
- Double Q-learning keeps two estimators: one picks the best next action, the other values it. It has no positive
  bias (it can underestimate).
- **For ACL:**
  - This is the textbook name for what HL1 measured.
  - Noisy, frequently updated values (forage, talk, gather) gain most from the max.
  - A rarely tried action (making) rarely benefits, which matches VC1's opposite signs.

## 2. van Seijen, van Hasselt, Whiteson & Wiering 2009, "A theoretical and empirical analysis of Expected Sarsa", IEEE ADPRL
https://www.cs.ox.ac.uk/people/shimon.whiteson/pubs/vanseijenadprl09.pdf — **read: abstract and search summary.**
- Expected Sarsa replaces the max with the **expected next value under the agent's own behaviour policy**.
- It converges under the same conditions as Sarsa, and its updates have lower variance than Sarsa's and
  Q-learning's.
- **For ACL:** ACL people choose by a softmax. With Expected Sarsa, a person would value next week by what they would
  actually do, on average, rather than by their single best-looking option. That is arguably closer to how a person
  forms expectations, and it removes the max's upward pull.

## What this would mean (only if CO2 finds "habit carries it", and only with the creator)
- **A candidate nature-change study:** v9 against v9 with an expected look-ahead (the softmax-weighted next value), with
  a sham arm.
  - **Primary:** making per adult-year, as in CU1 and AW1.
  - **Calibration check:** VC1's q − G.
- **Risks:**
  - it changes every habit, not only making's;
  - lower values everywhere could shift what people do in unexpected ways, so survival flags matter;
  - "no named recipes or outcomes" is kept, because the rule is general.
- **Not done here:** full texts; the human or animal evidence on whether people learn more like the max or like the
  expected value (to look for next).
