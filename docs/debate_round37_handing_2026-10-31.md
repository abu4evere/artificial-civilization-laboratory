# Debate round 37 (31 October 2026, sleep mode): after TA1, the handing law (B) or the choice to make (C)? (opinions, not sign-off)

**The same text to GPT (fresh chat `6ae6247a`) and Gemini (fresh chat `3f8c5fd79d00dc1e`), about 12:45; Claude as
council.**

## Answers
- **GPT: B first, 88%.** "TA1 shows physical access is abundant, but transfer is impossible. Test that missing
  affordance before changing learning rules."
  - **Mechanism:** (i), simplified. "Generalize give into voluntary food-or-tool transfer."
    - Tool transfer must not require food surplus.
    - Reuse the existing social weights.
    - Score the receiver's marginal tool benefit minus the giver's perceived loss.
    - Require proximity and room in the receiver's hands.
    - "Never automatically bundle tools with food as in (ii): that scripts a gifting custom."
  - **Primary:** the paired difference in the realized forage-tool contribution, R = (food with − food without) ÷ food
    with, handing minus v10, with a 95% paired world-bootstrap interval. It needs a positive lower bound, and the sham
    must not reproduce it.
  - **Mechanism checks:** actual transfers, recipients' tool-use weeks, adult tool use, and transfer reversals.
  - **No-harm flags:**
    - more extinctions;
    - population, or food per adult, down more than 10%;
    - knowledge retention down more than 10%;
    - excessive cycling of transfers.
  - "A null result with few transfers would point toward motivation or choice rules, not prove that physical access is
    irrelevant."
- **Gemini: B first, 85%.** "Physical affordances of nature must be established before testing cognitive learning
  rules."
  - **Mechanism:** (i). (ii) "creates an artificial coupling" to hunger and food surplus. Keep give's social weights,
    and replace the food-need ratio with the item's marginal use to the receiver.
  - **Primary:** the food added by tools, and the share of adult forage weeks holding a good tool.
  - **No-harm flags:**
    - food gifts must not fall by more than 5%;
    - child mortality and children's holding must not suffer;
    - no ping-pong (the same item handed back and forth in consecutive weeks).

## Council (checked against the code)
- **Adding a new action would change every person's habit table** (`person.N_ACTIONS`, the curiosity `tried` array).
  So "off" would not equal v10. **Following GPT ("generalize give")**, handing is built as a variant of the existing
  `give` action:
  - **mind:** when the setting is on, for each nearby person, the giver also scores handing their most useful
    transferable item. Score = give's own social weights × (the receiver's gain − the giver's loss).
  - If that beats giving food to the same person, the `give` option carries that score, and a transient note (cleared
    each week, never saved) tells `_give` to hand the item instead of food.
  - **Same action, same habit entry, same cost** (5; Gemini's parity). Room in the receiver's hands is required.
  - **No reward, and no relation change** for handing. Food giving's own bumps are unchanged.
- **With the setting off, nothing runs and nothing is stored,** so `code_hd1` off = `code_v10` exactly (to be shown by
  the zero checks).
- **All flags from both models are adopted.**
