# Research note: is resting while starving worth something? (1 November 2026)

**For the open question:** ES2's frozen guard was raised by **rest**. An exploratory breakdown
(`experiments/ES2_realized_lookahead/explore_rest.md`) puts almost all of it in one situation: weak or nearly out of
food, with company. There, the realized look-ahead under-values resting (bias −0.107 → −0.368). **Is resting in a
food crisis truly worth more than the new rule thinks, or is the new rule seeing it more truly?** A source suggests; only
a frozen study decides.

## What was read (labels per CLAUDE.md)
1. **Smith, L. L. (2023).** "Similarities and differences regarding acute anorexia nervosa and semi-starvation: does
   behavioral thermoregulation play a central role?" *Frontiers in Behavioral Neuroscience* (2023). PMC10634530.
   - **Read:** the abstract, and the sections on the Minnesota study and on shallow torpor; **not** the full text.
   - **The Minnesota Study of Semi-Starvation** (Keys et al. 1950, as described by Smith): 36 healthy young men, 6
     months at about 50% of their earlier intake.
   - **Semi-starved people "select" a passive strategy, "shallow torpor":** "reduced activity, resulting in energy
     conservation", with "a listless mood and increased sleep".
   - **Shallow torpor** is described as "an evolved behavioral strategy to facilitate survival in response to food
     shortages" and "the most effective means for energy conservation" (Smith citing others).
   - **Keys et al. (1950) itself was not read.**

## Bearing on ACL
- **In human evidence, resting when food is critically short is adaptive:** it conserves energy.
- **In ACL's own worlds, G (what actually followed) says the same:** resting in a crisis returned more than the
  realized look-ahead valued it.
  - The rule's under-valuation there is **a distortion, not a truer picture.**
  - The frozen guard was right to stop ES2.
- **A candidate for a later, separately frozen study** (not proposed here): a look-ahead that keeps ES2's gain without
  this distortion. To debate with GPT and Gemini first:
  - Why is the next week's expected habit value so low after a crisis rest? Perhaps because the next choice's
    options are dominated by instinct terms (instinct share 0.96 in ES2), so habits carry little.
  - Would a longer view (more than one week) recover rest's worth?
- **ES2's reading stands as frozen:** not supported.

## Addendum (06:50): a longer view
**Sutton, R. S. (1988).** "Learning to predict by the methods of temporal differences." *Machine Learning* 3:9–44
(Springer, doi 10.1007/BF00115009). **Read: the abstract only.**
- **Temporal-difference methods** "assign credit by means of the difference between temporally successive
  predictions". ACL's one-step habit update is such a method.
- The paper's TD(λ) family blends one-step and longer looks ahead. That is described in its body, **which was not
  read here.** It is named only as a candidate to read before any proposal.
- **Bearing:**
  - ES2's distortion arises at one step: the next week's habit values carry little after a crisis rest.
  - A longer view might recover what resting in a crisis is worth.
  - This is a hypothesis for the council, not a proposal.

## Correction (1 November 2026, after UV1)
- **The analogy above does not fit most of ES2's crisis rest updates.** UV1's exploratory table
  (`experiments/UV1_undervaluation_by_experience/explore_crisis_by_age.md`) finds that **94% of them are by children
  aged 1–5**. Children hold almost no food, so they always count as "under half a week of food".
- For them, the "crisis" situation is not starvation. Semi-starved adults' shallow torpor (Minnesota) says nothing
  about toddlers resting.
- What stands:
  - in ACL's own worlds, the realized look-ahead values those rest weeks below what followed (a distortion against G);
  - ES2's frozen guard stands.
- What does not: the reading "resting when starving is adaptive, so the guard caught that".
