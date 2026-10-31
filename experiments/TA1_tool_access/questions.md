# TA1 — Why do tools not reach hands? (frozen plan)

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

## Design (32 worlds, seeds 21101–21132; LP: 80 founders, 80×80; 200 years; `code_v10`; one arm)
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
  - **The split** (GPT, Gemini):
    - (b), (c) and (d) are **mutually exclusive**; (b) counts only when making is possible now;
    - (a) and (e) are **overlapping flags**;
    - a strict priority partition is also reported (Gemini): (e) hands full, then (b), (c), (d).
  - **(a′) a tool within reach that could be received** (GPT): the holder is within 3 tiles **and** the forager has
    room (fewer than 3 items).
  - **"Empty hands" against "hands holding other things"** (Gemini): 0 items, against 1–3 non-forage items.
- **Q2: who holds forage tools.**
  - The share of people holding one, by age band.
  - **Including children's hands** (Gemini): an heir can be a child, so adult tools can sit in children's hands.
  - Among holders, the share who forage that week (tools in non-foragers' hands; Gemini).
- **Q3: how forage tools leave hands:** wear, the 3-item limit, death; and the mean weeks a forage tool is held.
- **Q4: how they enter:** made, picked up, inherited.
  - The share of forage-tool makes by people already holding one.
- **Q5** (described): the food that would be added if each bare-handed forager in (a′) held the nearest holder's
  actual tool. It is computed with the tool's real properties and TR1's arithmetic, including the carry room and the
  tile's plants (GPT).

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

- **The 50% thresholds are classifications, not causal proof** (GPT). Access and choice gaps can coexist.

## Validity (hard stops)
- **Zero checks:**
  - the wrappers are read-only (state and random numbers identical with and without them, at 20 and 120 years);
  - reload is exact.
- **Forage-tool accounting:** every forage tool's entry and exit is counted (GPT). Tools held at the end = entries −
  exits, per world (a mismatch counter).
- All worlds are present under one fingerprint (`code_v10`).
- **A blind recompute by GPT and Gemini** of Q1's (a) and (b) shares and the reading.

## The assistant's prior
1. **"Neither":** (a) is below 0.50 (people are spread out), and (b) is below 0.50 (materials are often lacking).
2. **"Hands holding other things" is common:** more than 30% of bare-handed weeks.
3. **Most forage tools leave by wear.**

## Review (debate round 36, `docs/debate_round35_after_tr1_2026-10-31.md`, second part)
- **GPT: yes, 90%.** Adopted:
  - exclusive (b)/(c)/(d);
  - (a′) feasible receipt;
  - Q5 with real properties and caps;
  - full entry and exit accounting;
  - thresholds as classifications.
- **Gemini: yes, 94%.** Adopted:
  - the priority partition;
  - empty against clogged hands;
  - children's hands.
- **Corrected:** Gemini wrote that ACL "children under 12 play and craft miniature tools (Lew-Levy et al.)". That is the
  forager evidence. **In ACL, children under 12 cannot make known things.**

## Sign-off (31 October 2026)
The assistant, under the creator's sleep-mode autonomy. It is read-only (the 40% rule). GPT estimates 90%, Gemini 94%
and the assistant 75%. Frozen as `TA1-frozen` before any code or data.

## Operational note 1 (31 October 2026, after freezing, before any data)

How the code (`run_ta1.py`, `analyse_ta1.py`) reads the text where it left a choice, found in smoke worlds (seed 9995,
25 and 110 years; not data):
1. **Zero checks run at 20 and 120 years** (stricter than 20 and 60, as TR1).
2. **"Bare-handed"** means no item in hand with forage factor > 1. "Within reach" is `world.people_near(loc, reach = 3)`.
   "Room to receive" means fewer than 3 items (`item_limit`).
3. **"Knows a helpful kind"** means a kind in the forager's recipes whose best item in living hands that week has forage
   factor > 1. "Could make it now" is the law's own `can_make` (materials and parts in hand).
4. **The accounting follows each forage tool weekly** in living hands, on the ground (v8) and on bodies (BD1).
   - **Entries:**
     - made (a new item, made or changed from another);
     - picked up (from the ground);
     - from a body;
     - passed (it was in another's hands, as by inheritance).
   - **Exits:**
     - worn (confirmed by the `matter.wear` wrapper);
     - dropped (onto the ground);
     - to a body;
     - passed;
     - lost at death;
     - used or changed (gone while the holder lives: used up as a part, or changed by heat).
   - The first smoke showed that a catch-all "worn" was wrong (3,464 against 943 confirmed wears), so "used or changed"
     was split out. The checks:
     - tools held at the end = entries − exits;
     - no worn tool is still in hand.
   Both are 0 in the smoke.
5. **"Makes by someone already holding one":** a forage tool newly in the maker's hands, with a `make` event of that
   kind that week, by someone who held a forage tool the week before.
6. **Q2's age bands:** 0–11, 12–15, 16–39, 40–59, 60+. "Holders who forage" are adult holders who chose forage that week.
