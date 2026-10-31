# Debate round 38 (31 October 2026): after v11, the handing audit (A) or the learning rule (B)? (opinions, not sign-off)

**The same text to GPT (fresh chat `6ae6789f`) and Gemini (fresh chat `e75e6a2a7c71c85d`), about 19:10; Claude as
council. The creator: "alr keep working bro."**

**The options:**
- **(A)** a read-only study on v11: why handing stays rare, and where handed tools go.
- **(B)** a frozen nature-change test in a copy. Replace the max look-ahead in habit learning with an expected look-ahead
  under the person's own softmax choice (Expected Sarsa, van Seijen et al. 2009). The research note is
  `docs/research/learning_rule_sources_2026-10-30.md`.

## First answers
- **GPT: B first, 80%.** "HL1 and VC1 already identify a plausible general learning defect. B tests that mechanism
  directly, while A investigates a smaller downstream effect."
  - **Primary:** the reduction in out-of-sample calibration error across all actions.
  - **Secondary:** making, tool use, survival and population.
  - **Guard:** use the actual choice probabilities; freeze the temperature, the rewards and all other mechanics.
  - "Fix how minds learn before trying to make them produce more."
- **Gemini: A first, 85%.** Establish v11's handing baseline first, so tool sharing is not confounded with a change to
  how minds learn.
  - B is "a legitimate general law… zero domain knowledge".
  - **Primary:** making attempts per adult-year, with calibration error and survival as guards.

## The debate
- **To Gemini, with a fact checked:** B is paired on v11, with v11 as its own control arm and a sham. v11's handing is
  identical in every arm, so it cannot confound B, and A and B do not depend on each other.
  - **Gemini revised to B first, 88%:** "handing dynamics are perfectly controlled across seeds… Fix the evaluation
    engine first."
  - **And adopted GPT's primary:** "Freezing tool-making as the primary metric risks evaluating a general law based
    on a single favored behavior."
- **To GPT, Gemini's argument:**
  - **GPT kept B first, 75%** (down from 80%): "B's three arms all share frozen v11 mechanics. Handing cannot
    confound the randomized comparison."
  - **On the primary:** "ACL should test whether its minds learn more accurately, not whether changing their minds
    makes them craft more. More making is evidence of progress only if it emerges from a better general learning
    rule."

## Council
- **Agreed by both after the debate:**
  - B first;
  - **primary = calibration error across all actions;**
  - making, foraged food, survival and population as secondary or guards.
- **The assistant's estimate:** 70%. ES1 is drafted on this basis (`experiments/ES1_expected_lookahead/questions.md`).
- **A (the handing audit) follows later**, on unchanged v11.
