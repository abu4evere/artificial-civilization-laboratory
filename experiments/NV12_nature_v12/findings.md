# NV12 — Nature v12: three faults fixed (adopted 3 November 2026)

**Adopted by the assistant under the creator's permission to edit world rules.** The creator, 2 November 2026: "I give
you permission to edit world rules. Take a look and check all rules. If you find something fix it or add any new
rules. From now on keep working without me". The path is the one `CLAUDE.md` gives for a plain fault ("Editing the
world's rules"), and FF1's frozen plan.
1. **A frozen study whose result supports the change:** FF1, final. It found no harm (f / v11 living-weeks 1.0003
   [0.8926, 1.1301]; extinctions 1 against 1) and nothing to flag. FF1 was frozen as "FX1" (folder `FX1_fault_fixes`).
2. **An independent blind recompute:** GPT, Gemini and DeepSeek all match
   (`experiments/FX1_fault_fixes/recompute_ff1.md`).
3. **No confirmatory run:** a fault fix restores what the rule already says and is not a new law. This was frozen in
   FF1's plan, with all three advisors agreeing in council round 51.
4. **The council on adoption:** round 51 asked about "no harm → nature v12" itself. GPT 97%, Gemini 99%, DeepSeek about
   95%; the assistant 85%.
5. **`code_v12`** with zero checks (`zero.txt`).
6. **Reference hashes** regenerated, and the tests passing (67).
7. **A tag `nature-v12`,** a line in `docs/autonomous_decisions.md`, and a Telegram message.

## What changed (three files; `v11_to_v12.diff`, 98 lines)
- **F1, the make choice** (`fix_make_choice` = 1, `mind.decide`).
  - **Before:** a recipe was skipped when its unscaled value was at or below the best so far's *scaled* utility, so
    recipes learned later were held back.
  - **Now:** the offered recipe is the one with the highest utility above the same floors.
- **F2, an heir's things** (`fix_overflow` = 1, `biology.die`).
  - **Before:** things beyond the 3-thing limit were deleted, the heir's first-held thing first.
  - **Now:** the least valued is left on the ground, as v8's law and `_keep` already say.
- **F3, things from a body** (`fix_overflow`, `biology.bodies_week`). The least valued goes to the ground, not the first
  held.
- **Unchanged:** the read-only logging hooks FF1 used (`fx1log`) stay in the code. They act only when a runner sets
  them, as earlier logging hooks do.

## Checks
- **Zero checks** (`zero.txt`): all pass.
  - v12's code with both fixes 0 = `code_v11` (4 runs);
  - v12 = FF1's arm f (2 seeds);
  - the live package's defaults = v12;
  - the fixes act;
  - reload is exact.
- **Tests:** 67 pass. The live reference hashes were regenerated (= v12); v12's set was added; v11's is kept.

## What it does (FF1, 32 paired worlds; described)
- **The make choice:** the old and new rules differ in 8.6% of adult make decisions. On the same decisions, the newest
  recipe is offered more often (0.106 against 0.090).
- **Inheritance:** 63 things deleted at inheritances in v11 become 73 left on the ground.
- **No change** to population, making, remaking or held things beyond chance.

## For studies
New studies use `code_v12`; v11 findings stay v11's. v11 stays in `experiments/NV11_nature_v11/code_v11`, so the change
can always be undone.
