# HD1 — Can a person hand a made thing to another? A nature-change test in a copy (frozen plan)

**A nature-change test in a copy (`code_hd1`), not an adoption.** Live nature stays v10. Adoption would follow only
the safe path in `CLAUDE.md`:
1. this study supported and final, with a matching GPT and Gemini blind recompute;
2. a confirmatory run on new seeds;
3. both models consulted;
4. `code_v11` with zero checks;
5. hashes and tests;
6. a tag, and a Telegram message.

## Why
- **TA1** (final): in 82% of bare-handed adult forage weeks a forage tool is in someone's hands within 3 tiles, but
  **no living person can hand a made thing to another**.
- **TR1** (final): the best tool in anyone's hands would add 20% to foraged food; tools add 1% today.
- **Debate round 37** (`docs/debate_round37_handing_2026-10-31.md`): both models chose this test first (GPT 88%,
  Gemini 85%). Handing a thing is a physical ability, not a custom: whether and when people do it is left to the existing
  choice machinery.

## The law (one setting, `hand_items`; 0 = v10 exactly)
- **The existing `give` action is generalized,** following GPT: a person may hand **one made thing they hold** to a
  person within reach, instead of food.
  - Same action, same habit entry, same cost (5).
  - **The receiver must have room** (fewer than 3 items).
- **What can be handed:** the item with the highest **net use**. Net use = the receiver's gain − the giver's loss.
  - **The receiver's gain:** for any use (forage, hunt, wood, stone, fiber, fight, carry, cold), how much the item's
    `matter.factor` exceeds the receiver's own best for that use.
  - **The giver's loss:** how much the giver's own best for any use falls without the item.
  - It is offered only if net use > 0.
- **How it is chosen:** with give's own social weights. Score = net use × (0.25 × kindness + 0.6 × affection + 0.6 ×
  kin + 0.6 if partner + give's own payback term).
  - Food giving needs the giver's surplus and the receiver's hunger; **handing needs neither.**
  - For each nearby person, the `give` option carries the larger of the food score and the handing score. When handing
    is larger, `_give` hands the item instead of food. This is decided by a transient note, cleared each week and never
    saved.
- **No reward, no relation change, no kin preference beyond give's existing weights, no forced transfers.** Objects
  are conserved: the item moves from one hand to the other.

## Arms (32 paired seeds 21201–21232; LP: 80 founders, 80×80; 200 years)
| arm | setting |
|---|---|
| **v10** | `hand_items` 0 (= `code_v10`, shown by the zero checks) |
| **h** | `hand_items` 1 |
| **x** | sham: v10 with `sham_draw` 1 |

## Measures (adults, years 100–200; paired world bootstrap, 10,000 replicates)
- **Primary** (GPT): the realized share of adults' foraged food added by tools, R = (food with − food without) ÷ food
  with (TR1's own measure and wrapper), **h − v10**.
- **Mechanism checks:**
  - handings per adult-year;
  - the share of adult forage weeks with a tool in hand;
  - recipients' later tool-use weeks;
  - reversals (the same item handed back to its giver within 4 weeks);
  - food gifts per adult-year.
- **Described:** tools in children's hands; items handed by kind of use.

## Frozen decision rule
- **Supported:** h − v10 > 0 with a lower bound > 0, **and** h − v10 > (x − v10), the sham's own difference, **and** no
  flag.
- **Not supported:** otherwise. If handings are rare (< 0.1 per adult-year), the reading says so: a null with few
  handings points to choice, not to access being irrelevant (GPT).

## No-harm flags (raised against v10, paired)
- **Extinctions:** h has 3 or more more extinct worlds than v10.
- **Population** (mean living, years 100–200), or **food per adult:** h ÷ v10 < 0.90, with the upper bound < 1.
- **Knowledge kept:** recipes held per adult, h ÷ v10 < 0.90, with the upper bound < 1.
- **Food gifts** (Gemini): food gifts per adult-year, h ÷ v10 < 0.95, with the upper bound < 1.
- **Children** (Gemini): child (0–11) deaths per 1,000 child-years, h − v10 > 0, with the lower bound > 0.
- **Ping-pong** (Gemini, GPT): reversals > 10% of handings.

## Validity (hard stops)
- **Zero checks:**
  - `code_hd1` with `hand_items` 0 = `code_v10` (state and random numbers, 20 and 60 years, two seeds);
  - h acts (differs);
  - the sham acts;
  - the TR1-style wrapper is read-only in arm h;
  - reload is exact.
- **Conservation:** items handed = items received (a mismatch counter).
- All 96 worlds are present under one fingerprint.
- **A blind recompute by GPT and Gemini** of the primary difference, its interval, the sham's and the flags.

## The assistant's prior
1. **Supported:** R rises from about 1% to 3–6%.
2. **Handings are frequent** (more than 1 per adult-year), mostly to partners and kin.
3. **No flags.**

## Sign-off (31 October 2026)
The assistant, under the creator's sleep-mode autonomy (a nature-change test in a copy; CLAUDE.md allows it as a
frozen study under the 40% rule). GPT estimates 88%, Gemini 85% and the assistant 70%. Frozen as `HD1-frozen` before
any code or data. **Adoption is not part of this study.**
