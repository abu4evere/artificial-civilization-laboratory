# Debate round 39 (31 October 2026, sleep mode): after ES1, which learning rule next? (opinions, not sign-off)

**The same text to GPT (fresh chat `6ae6b587`) and Gemini (fresh chat `49f1810cfa701570`); Claude as council.**

**The candidates** (each a nature-change test in a copy; primary calibration across all actions):
- **(i) Deferred Expected Sarsa over the real next choice:** hold last week's update until the next decision, then use
  the expected value under the actual softmax over options, instinct terms included.
- **(ii) Deferred plain SARSA.**
- **(iii) Double Q-learning.**

## Answers
- **GPT: (i), 85%.** "It learns from the actual policy, including instinct and habit, rather than pretending agents
  choose by habit alone. Plain SARSA is valid but noisier; Double Q addresses maximization bias without correcting the
  mismatch between learning and real decisions."
  - Freeze exactly when the deferred update happens, and how deaths are handled.
  - **Keep absolute calibration as the sole primary,** and ranking accuracy as a frozen secondary: "changing the
    success criterion now risks confusing behavioral gains with more accurate minds."
  - **Guards:**
    - no well-sampled action's calibration may deteriorate substantially;
    - uncompleted deferred updates must stay negligible and comparable across arms.
- **Gemini: (i), 72%.**
  - Add ranking accuracy (Kendall or Spearman) as a **co-primary**.
  - **Guards:** an instinct-dominance check (the variance of instinct against 0.6 × q); deferred updates dropped
    cleanly at death.

## The debate
- **To Gemini, GPT's argument, and the council's note:** G exists only for actions actually taken. A ranking would
  compare average returns of different actions across people and weeks, and adding a primary right after ES1's
  secondary result could look like moving the goalposts.
- **Gemini revised (80%):** "Yes. I accept absolute calibration as the sole primary metric, with relative ranking
  accuracy placed strictly as a frozen secondary… Elevating relative ranking to a co-primary immediately after
  observing ES1's secondary behavioral split risks post-hoc goalpost shifting."

## Council
- **Agreed:** design (i); absolute calibration the sole primary; ranking a frozen secondary.
- **Guards from both:** per-action calibration, uncompleted updates, deaths dropping the deferred update cleanly, and
  an instinct-dominance description.
- **The assistant's estimate:** 70%. ES2 is frozen on this basis.
