# CI1 design draft: children may make again, and a held aim (6 November 2026; a draft, not frozen)

**Status:** a draft for the study council round 67 asked for after FF3
(`docs/debate_round67_after_rf1_2026-11-06.md`). It runs on nature v14 if FF3 is adopted. Nothing here is frozen or
run. The name CI1 ("children and intention") is provisional.

## Arms (as round 67): v14, LG, IN, LG+IN, sham

## LG: children may make again what they know
- **Today (v13):** the make option sits inside `if grown:` (`mind.decide`, line 288). Children aged 3 to 12 play and
  invent (`actions._play` records the recipe as "made"), but are never offered "make again".
- **The law:** the make option is offered to children past toddlerhood (3 and over), exactly as to the grown.
  - It uses the same value floor, the same `can_make`, and the same pull, with their own diligence and hunger.
  - The rest of the grown block (put, heat, fill) stays for the grown, so that only the one ability changes.
- **The evidence:** Lew-Levy et al. 2017 (`docs/research/children_tool_making_2026-11-06.md`; read as a summary, to
  be checked): children make their own simple tools by about 4–5.

## IN: a held aim (revised by round 67)
**A fact found while drafting, which changes the design:** the pull toward a valued thing's missing pieces **already
exists in v13**.
- `_material_wants` (`mind.py` lines 670–691) wants each missing raw material of a valued recipe whose thing is not
  held, at that recipe's value.
- `_wanted_parts` (lines 631–642) values each missing made part at 0.8 × the value of what it goes into.
- RF1 agrees: every one of the 53 kinds started was seen gathering a missing input.

So part (b) of round 67's law is not new. **The new part is keeping the pieces.** In 45 of 53 kinds a gathered piece
was later gone before the set was complete.

How held pieces leave a person in v13 (found in the code):

| how | where |
|---|---|
| used in another make | `actions` lines 414–458 |
| set down (put) | `actions` line 300; "put" was chosen in 0.117 of wanting weeks |
| burnt to light a fire, or under tipped embers | `actions` lines 545 and 661 |
| baked at a fire (soft earth) | `biology` line 304 |
| a made part given away, or worn out | gifts; `matter.wear` |

**The law, minimal:**
- **The aim forms** when a recipe is known, valued above the existing floor (0.05), and its thing is not held fresh
  (`_holding`). One aim at a time: the most valued such recipe. It is saved with the person.
- **While it is held:**
  - a piece it needs, up to the number needed, is not set down, not given, and not used in another make of lower
    value. A make of higher value interrupts the aim (DeepSeek: "interrupted, not violated");
  - **survival uses stay open:** lighting a fire and tipping embers (warmth) are never blocked. The aim yields to
    need, as all three models asked;
  - nothing else changes: the existing pulls already lead to the missing pieces.
- **The aim ends** when:
  - the inputs are in hand (the make option then appears as now);
  - the value falls to 0.05 or below;
  - the recipe is forgotten;
  - or a higher-valued make is chosen (interruption).
- **Not included:** a new pull or a new weight (GPT's caution), a time limit, a named recipe.

## Measures (to be frozen)
- **Harm guards per arm, against v14:**
  - starvation per 1,000 living-years (ratio above 1.25 with the lower bound above 1);
  - killing (difference above 0.05 per 1,000 living-years);
  - adult health (below −5);
  - living-weeks (ratio below 0.90);
  - extinctions (3 or more extra);
  - **child deaths** per 1,000 child-years, and **gifts to kin's children** (both proposed by the council).
- **Co-primary, remaking:** kinds made again by their inventor within 5 years (AF1's rule), per new kind, with RF1's
  funnel as described.
- **Described:**
  - RF1's stages per arm;
  - the share of wanting weeks with a piece lost;
  - the carry limit;
  - theft;
  - held materials.

## Open points for the freeze
- Whether LG should also open the rest of the grown block (put, heat, fill). The draft says no, so that one ability
  changes at a time.
- A power check: IN's own primary depends on how many kinds reach a wanting week (69 in RF1). LG may add many.
