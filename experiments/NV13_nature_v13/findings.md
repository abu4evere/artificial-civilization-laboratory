# NV13 — Nature v13: three more faults fixed (adopted 3 November 2026)

**Adopted by the assistant under the creator's permission to edit world rules.** The creator, 2 November 2026: "I give
you permission to edit world rules. Take a look and check all rules. If you find something fix it or add any new
rules. From now on keep working without me". The path is the one `CLAUDE.md` gives for a plain fault ("Editing the
world's rules"), and FF2's frozen plan.
1. **A frozen study whose result supports the change:** FF2, final. It found no harm: f / v12 living-weeks 1.0008
   [0.8893, 1.1203]; extinctions 0 against 0. One flag was explained (fewer hunts, caused by F8's honest expectation).
2. **An independent blind recompute:** GPT, Gemini and DeepSeek all match
   (`experiments/FF2_fault_fixes_2/recompute_ff2.md`).
3. **No confirmatory run:** a fault fix restores what the rule already says. This was frozen in FF2's plan, as in FF1.
4. **The council on adoption:** round 54's merged plan, "a harm-only fault-fix check on v12 like FF1 … the FF1 rule"
   (no harm → adoption). GPT 97%, Gemini 99%, DeepSeek about 92%; the assistant 90%.
5. **`code_v13`** with zero checks (`zero.txt`).
6. **Reference hashes** regenerated, and the tests passing.
7. **A tag `nature-v13`,** a line in `docs/autonomous_decisions.md`, and a Telegram message.

## What changed (seven files; FF2's `v12_to_ff2.diff` with the three defaults set to 1)
- **F8, the hunt decision's meat** (`fix_hunt_expect` = 1, `mind.decide`; helper `fauna.expected_take`).
  - **Before:** a success was weighed as (25 + 12 × n) ÷ n food per hunter, from the first commit and read nowhere
    else.
  - **Now:** it is weighed as the meat of the prey the person sees on that tile (the mean over `take_prey`'s choices),
    ÷ n.
- **F4, materials past the 20-unit limit** (`fix_mat_limit` = 1, `matter.receive`, used by `actions.resolve_hunts` and
  `biology.die`). What does not fit is left on the tile's pile instead of being kept past the limit.
- **F5, water walks** (`fix_water_holder` = 1, `weather.drink`). Only a thing that can hold water shortens the daily
  walk to water.
- **Unchanged:** the read-only logging hooks FF2 used (`ff2log`). They act only when a runner sets them.

## Checks
- **Zero checks** (`zero.txt`): all pass.
  - v13's code with the three fixes 0 = `code_v12` (4 runs);
  - v13 = FF2's arm f (2 seeds);
  - the live package's defaults = v13;
  - the fixes act;
  - reload is exact.
- **Tests:** 68 pass (67 plus v13's replay test). The live reference hashes were regenerated (= v13); v13's set was
  added; v12's is kept.
- **Fingerprints:** live `acl/` `0251e516…`; `code_v13` `f8b793bf…`.

## What it does (FF2, 32 paired worlds; described)
- **Population and extinctions:** unchanged.
- **Hunting:** about 21% fewer hunter-weeks. The option now expects about 8.6 food per success instead of 35.5.
- **Inheritance:** about 4,400 material units a century past the limit (all 32 worlds) now go to the pile.
- **Water walks:** about 9% of adults' water-walk weeks no longer get a walk shortened by a leaky carry thing.

## For studies
New studies use `code_v13`; v12 findings stay v12's. v12 stays in `experiments/NV12_nature_v12/code_v12`, so the change
can always be undone.
