# E8 — The Crucible · Predictions (FROZEN)

**Written:** 2026-10-05, before any E8 code is written and before any run. Not to be edited after the results.
**Design:** 7 arms (Control, Making Freedom, Naturalistic Apprenticeship, Composite Memory Protection, Demographic Scale, The Crucible Triad, Full Synthesis) across 4 seeds (301–304) for 120 years.

---

## Known from the Code and Audits Before Running (Not Predictions)

- Crafting skill currently rises only through physical practice: each crafting act adds ~1.2% of the gap to 1.0 (x1.6 when focused).
- In E7.6, best living crafting skill collapsed from 0.73–0.98 at Year 25 to 0.34–0.61 at Year 100, and 0.05–0.11 at Year 1000.
- Deliberate making collapsed from ~3.1 per person-decade to ~0.05 by Year 1000.
- Watching produced only 7 copies in 1,770 observations in E7.7 because watching was only coded for boat landings and hunts.
- Composite recipes face a 5-fold higher eviction rate upon making (21% forgotten vs. 4% for simple items) due to `MAX_RECIPES = 12`.
- Direct Lamarckian inheritance is strictly forbidden: novices must earn motor skill with their own hands.

---

## Frozen Predictions

1. **Apprenticeship Preserves Skill (Arm 2):**
   In Arm 2, scaffolded practice efficiency will arrest skill degradation: the best living crafter at Year 100 will have crafting skill $\ge 0.60$ in all surviving worlds (vs. $\le 0.40$ in Control).
2. **Making Freedom Stimulates Deliberate Making (Arm 1):**
   In Arm 1, deliberate making in Years 50–100 will exceed 2.0 per person-decade in at least 3 of 4 seeds (a $\ge 2.5\times$ increase over Control). However, best skill at Year 100 will remain $< 0.50$ due to lack of scaffolded guidance.
3. **Memory Protection Preserves Composite Inventions (Arm 3):**
   In Arm 3, multi-component recipes will comprise $\ge 25\%$ of unique recipes held by the living at Year 100 (vs. $<12\%$ in Control).
4. **Demographic Scale Alone Fails to Stop Skill Decay (Arm 4):**
   In Arm 4 ($N_0 = 80$), best crafting skill at Year 100 will remain $< 0.45$ in all seeds, demonstrating that population scale without transmission fidelity cannot prevent de-skilling.
5. **Synergistic Triad (Arm 5):**
   In Arm 5, the combination of Making Freedom, Apprenticeship, and Memory Protection will achieve super-additive skill retention:
   $$\text{mean skill at Year 100 in Arm 5} > 0.35 \quad \text{and} \quad \text{best skill} \ge 0.75 \quad \text{in} \ge 3 \text{ seeds.}$$
6. **Watertight Vessels in The Crucible (Arms 5 and 6):**
   At least one world in Arm 5 or Arm 6 will craft $\ge 2$ watertight vessels and sustain them in regular use past Year 50.

---

## Kill Criteria (The Experiment Is Invalid If)

1. Any run crashes or raises an unhandled exception.
2. The probe touches simulation state (verified via 20-year SHA-256 state hash equality).
3. Any direct skill transfer / Lamarckian inheritance shortcut is introduced.
4. Any simulation code file changes during the active execution of an arm.
