# NV14 — Nature v14: memory ties no longer settled by name (adopted 6 November 2026)

**Adopted by the assistant under the creator's permission to edit world rules.** The creator, 2 November 2026: "I give
you permission to edit world rules. Take a look and check all rules. If you find something fix it or add any new
rules. From now on keep working without me". The path is the one `CLAUDE.md` gives for a plain fault ("Editing the
world's rules"), FF3's frozen plan, and NV13's precedent.
1. **A frozen study whose result supports the change:** FF3, final. It found no harm: f / v13 living-weeks 0.9636
   [0.8506, 1.0867] (the sham 0.9576); extinctions 2 against 1. Two flags were explained read-only: fewer ties per
   recipe eviction (the fix's own mechanism) and remade kinds 1 → 0 (single events).
2. **An independent blind recompute:** GPT (with code) matches every number. DeepSeek matches every point estimate; its
   intervals are approximate, as it said. Gemini 3.1 Pro failed to answer three times (stalled, or the page reset with
   no reply); if it answers, its reply is appended to `experiments/FF3_name_ties/recompute_ff3.md`.
3. **No confirmatory run:** a fault fix restores what the rule already says ("the least valued is dropped"). This was
   frozen in FF3's plan, as in FF1 and FF2.
4. **The council on adoption:**
   - round 66 (all three call the name order a fault);
   - round 67 ("FF3 first … then adoption as v14 by the fault-fix path"; GPT 97%, Gemini 95%, DeepSeek about 90%);
   - the assistant 88%.
5. **`code_v14`**, with zero checks (`zero.txt`).
6. **Reference hashes** regenerated, and the tests passing.
7. **A tag `nature-v14`,** a line in `docs/autonomous_decisions.md`, and a Telegram message.

## What changed (six files; FF3's `v13_to_ff3.diff` with the default set to 1)
- **F9, ties at a full memory** (`fix_name_ties` = 1; helper `util.tie_pick`).
  - **Before:** when a full memory dropped its least valued item and several shared that value, the item's text
    decided. That was the recipe's name (more nested kinds lost), the mark's shape, the source's id, or the puzzle's
    key.
  - **Now:** one of the tied items is drawn evenly from a stream of its own, seeded from the world's seed, the week, the
    person, the memory and its size. It never touches the world's generator.
  - **Where:** recipes (`knowhow.remember_recipe`), known marks (`marks._link`), records of sources
    (`information._note`), puzzles (`inquiry.notice`).
- **Unchanged:** known places (they never tied) and the trimming of a mark's links (`marks._link`'s sorted links, also
  settled by text; noted for a later round). The read-only logging hooks FF3 used (`ff3log`) act only when a runner sets
  them.

## Checks
- **Zero checks** (`zero.txt`, 6 November 2026, from 04:00): all pass.
  - v14's code with the fix 0 = `code_v13` (4 runs);
  - v14 = FF3's arm f (2 seeds);
  - the live package's defaults = v14 (2 seeds);
  - the fix acts;
  - reload is exact.
- **Tests:** 69 pass (68 plus v14's replay test), run at 04:05. The live reference hashes were regenerated (= v14);
  v14's set was added; v13's is kept.
- **Fingerprints:** live `acl/` `0e69752c…`; `code_v14` `84b54237…`.

## What it does (FF3, 32 paired worlds; described)
- **Population and extinctions:** no harm (above).
- **A new recipe entering a full memory is kept at birth 39% of the time instead of 30%.** It no longer loses every tie.
- **Ties per recipe eviction** fall from 64% to 48%.
- **Unchanged within their intervals:** world-new kinds, makes, and the other memories' eviction rates.
- **Remaking** stays at the floor (RF1: pursuit fails, and most inventors are children).

## For studies
New studies use `code_v14`; v13 findings stay v13's. v13 stays in `experiments/NV13_nature_v13/code_v13`, so the change
can always be undone.
