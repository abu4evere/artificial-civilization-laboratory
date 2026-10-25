# GPT's review of the WM1 draft (25 October 2026). GPT's opinion, not sign-off.

Asked in a fresh ChatGPT chat (https://chatgpt.com/c/6ade52af-3288-83e8-8137-0f2e33d9aa57), with the draft attached.
**Verdict: major revisions before freezing.** "Observing when women die is not the same as establishing why they die."

1. **The load-state decomposition is useful but not causal.**
   - Selection into pregnancy: healthier women conceive.
   - Selection into caring: mothers are carers by rule; men become carers only by replacement.
   - Delayed effects: a woman harmed while caring may die after the load ends.
   - Overlapping states: a pregnant mother may also be feeding children.
   - Log independent, time-varying indicators (gestational week, weeks since delivery, dependants, food actually
     given, concurrent loads, recent deficits, prior illness, health at the start), not only one state per week.
   - Deficit and illness may be the pathway, so do not adjust them away.
2. **Rewrite Q2 as descriptive.** Equal hazards in unloaded weeks do not show that loads caused the gap. The diagnostic
   arms, not Q2, should decide whether removing a mechanism reduces the gap.
3. **Measures.**
   - Rates per 1,000 person-years. Define when state and age are measured.
   - A crude ratio for 16–54 depends on each sex's age structure. Use age-standardised measures with the same fixed
     weights, defined in advance.
   - Use 5-year bands where counts allow; 55+ descriptive only.
   - Primary: the age-standardised rate difference (female minus male) and the rate ratio; survival from 16 to 50,
     with censoring at week 6240 defined.
   - Bootstrap over worlds (10,000 replicates, method stated, zero denominators handled); paired by seed for the arms.
   - Drop [0.9, 1.1] as a decision rule. Keep it as a descriptive tolerance, or register a proper equivalence test.
4. **Make P0, B0 and K0 planned and primary, as counterfactual rule interventions**, plus at least a combined arm
   (a full 2×2×2 factorial if affordable).
   - B0 is the cleanest. P0 and K0 have system-wide effects; K0 may save mothers and cost children.
   - The outcome: Δ = G_arm − G_C, the change in the age-standardised female-minus-male rate difference, with paired
     intervals.
   - Report each sex's rate too, since a ratio can move because men die more.
   - Do not add up separate effects.
   - The arms are not proposals for nature.
5. **Missing pieces to add.**
   - Health trajectories after delivery and caring.
   - Concurrent loads.
   - Men's exposures (hunting, fights, travel, injuries) by sex.
   - Partner provisioning (transfers by giver and timing).
   - Founders reported separately.
   - Extinction and adult person-years by setting.
   - A feasibility or precision estimate.
   - Clear cause-of-death coding.
   - C20 and D80 are different regimes, not just two sample sizes.
6. **Evidence check.**
   - Hadza 35.5 / 30.8: cite Blurton Jones (2016). It is life expectancy at birth, not adult hazard.
   - Pumé 24.2 men / 22.5 women (male share 0.52): adults are defined as men 16–45 and women 14–36, and the figure
     varies a lot from year to year. Do not compare it with ACL's ratio at 50.
   - Hiwi 4.4 per 1,000 women of reproductive age per year: correct (Hill, Hurtado & Walker 2007, J. Hum. Evol. 52:
     443–454). This is about one maternal death per 55–75 pregnancies. State denominators.
   - Kramer, Schacht & Bell 2017 and Gurven & Kaplan 2007 (illness about 70% of deaths, violence and accidents about
     20%): correct.
   - Narrow the claim about men: some populations show a large male excess from violence (the Hiwi). Nothing should be
     added just to reproduce a human sex ratio.
7. **Validity.**
   - One fingerprint per arm, not one overall.
   - A zero check that the observer changes nothing, in each arm.
   - A test that each switch changes only its rule.
   - Seeds paired across arms.
   - Contributions can be negative: report signed rate differences first and percentages second.
8. **Structure.** Q1 the gap (primary); Q2 loads (primary, descriptive); Q3 cause and state (signed, descriptive); Q4
   the arms (primary, causal diagnostic); Q5 the combined arm. C20 is the main setting; D80 is for robustness. No
   change to nature v7 is justified by anything here.
