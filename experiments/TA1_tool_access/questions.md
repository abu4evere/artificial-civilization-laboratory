# TA1 — Why do tools not reach hands? (DRAFT for debate; not frozen)

**Read-only on nature v10. No change to nature.** It follows TR1 (final, `experiments/TR1_tool_returns/findings.md`):
tools add 1.0% of adults' foraged food, but the best tool already in anyone's hands would add 20%. About nine forage
weeks in ten are bare-handed. Debate round 35 (`docs/debate_round35_after_tr1_2026-10-31.md`): both models chose this
read-only audit first (GPT 95%, Gemini 95%), before any handing law (B).

## How tools move today (code, v10)
- **Into hands:**
  - making (`_make`, `make` event, with the item's properties);
  - pick-up from the ground (`pickup` event, v8);
  - inheritance at death (`inherit`).
- **Out of hands:**
  - wear (`matter.wear`, which removes an item at 0 uses; no event);
  - the 3-item limit (`drop` event, v8);
  - death.
- **No living person can hand a made thing to another.** Children under 12 cannot make known things.

## Design (32 worlds, seeds to be set; LP: 80 founders, 80×80; 200 years; `code_v10`; one arm)
**Read-only:**
- a wrapper on the forage action (as TR1) notes, before the action, the forager's hands, recipes and materials, and
  who is within reach (3 tiles, `world.people_near`);
- a wrapper on `matter.wear` notes tools that wear out;
- one on `actions.drop_on_ground` notes tools pushed out of hand;
- events (`make`, `pickup`, `inherit`, `death`);
- a weekly note of who holds a forage tool (factor > 1).

## Questions (adults, years 100–200; world bootstrap)
- **Q1** (primary): **why is a forager bare-handed?** For each bare-handed adult forage week (no item with forage
  factor > 1 in hand):
  - **(a) a tool within reach:** someone within 3 tiles holds a forage tool;
  - **(b) could have made one:** the forager knows a kind whose existing items have forage factor > 1, and has the
    materials to make it now (`can_make`);
  - **(c) knows one but lacks materials;**
  - **(d) knows none;**
  - **(e) hands full:** 3 items, none for foraging.
  Shares, which may overlap; (b), (c) and (d) are exclusive.
- **Q2: who holds forage tools.**
  - The share of people holding one, by age band.
  - Among holders, the share who forage that week (tools in non-foragers' hands; Gemini).
- **Q3: how forage tools leave hands:** wear, the 3-item limit, death; and the mean weeks a forage tool is held.
- **Q4: how they enter:** made, picked up, inherited.
  - The share of forage-tool makes by people already holding one.
- **Q5:** for scale, the food TR1-style headroom would add if every bare-handed forager in (a) had the nearest
  holder's tool (described).

## Frozen reading (Q1)
- **"Access gap":** (a) ≥ 0.50 of bare-handed weeks. A tool is usually within reach, so a handing law (B) can be tested
  meaningfully.
- **"Choice gap":** (b) ≥ 0.50. The forager could make one now and does not, so the bottleneck is the choice (CO2,
  IW1).
- **"Both"** if both; **"neither"** if neither.
  - Then (c), (d) and (e) say where the gap is: materials, knowledge or hands.

## What would follow
- **"Access gap":** draft B (handing a made thing), with both models' guards (`docs/debate_round35_after_tr1_2026-10-31.md`).
- **"Choice gap":** the choice to make. A learning-rule study (the creator's open item) or the worth of tools against
  food.
- **"Neither":** materials, knowledge or hands, by the split.

## Status
A draft for a design check by GPT and Gemini (debate round 36). Seeds, priors and sign-off follow the check.
