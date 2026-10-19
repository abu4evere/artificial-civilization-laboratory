# NS1 — The name shuffle: do the names in ACL's code carry any hidden meaning? (PARKED, 20 October 2026: the creator: "we do not have to prove if its scripted or not to anybody rn"; draft kept, nothing built or run)

**Why.** ACL's founding claim is that nothing cultural is written in: no recipe, no list of inventions, no reward for
being useful. Several tests already guard it (no invention names where people think; a read-only historian; rewards
only from nature; leak tests). But a sceptic can still ask: do the *names* in the code (`stone`, `flint`, `wood`,
`forage`, `deer`, `forest` …) quietly steer anything? If people "make rafts from wood" only because something somewhere
treats the word `wood` specially, that would be a script. The creator asked how ACL could prove it is not scripted
(20 October 2026); this study is one direct test. **Nothing in ACL's nature changes; the study runs on renamed copies.**

## Question

If every name a person's world is built from is replaced by meaningless tokens, does anything about what happens change?

## What the code already tells us (read 20 October 2026)

- The named things: 8 materials (`matter.MATERIALS`, with their physical properties in `matter.RAW`), 19 actions
  (`person.ACTIONS`), animal species (`fauna.SPECIES`), biomes (`geo.BIOMES`), skills, and the names recipes are built
  from (a recipe's signature is spelled from material names, e.g. `flint/stone`).
- Names can still matter in one known, meaning-free way: **order**. Some choices break ties by sorting names (the
  12-recipe tie-break that drops composites first, because `(` sorts before letters, is the known example; about 25
  places sort or take a minimum or maximum by key). Renaming can change alphabetical order and so change which of two
  equal options is taken. That is a bookkeeping effect, not meaning, and the design separates it.

## Design (the assistant's recommendation; decisions marked)

A script makes renamed copies of the package by changing **only string literals from a fixed vocabulary**, every
occurrence in every file, consistently, with Python's own tokenizer (so no code, comment or number is touched). The
vocabulary is listed in full and frozen before any run.

**Test 1, exact (hard proof):** an **order-preserving** renaming: gibberish tokens chosen so that every list sorts in
the same order as before (e.g. `stone` → `q71m` only if all relative orders hold). Prediction, which the design
requires: **every world is identical, week by week**, once the saved state's names are translated back (state hash
equal, seeds 11, 501, 601 for 20 years, and 16 full 120-year worlds). Any difference means some name carries meaning,
and it would be found and reported.

**Test 2, statistical (Decision 1):** a **random** renaming (orders change), on 256 new worlds against the original
code, paired by seed. Because ties may now break differently, histories diverge, so the test is whether the
**distribution** of outcomes is the same: extinction (sign test), population at years 60 and 119, CA1's chain pass rates,
food sources (FX1's measure), what kinds of things get made (by their properties, not their names). Reading: "no
meaningful difference" if every interval sits inside a yardstick fixed beforehand (extinction ±0.117, as every study);
any difference is traced to a specific sort before it is called anything.

**Also recorded:** a list of every place in the code where the order of names decides something (from Test 2's
differences and a code read), so the book's known compromises can be updated.

## What it can and cannot show

It can show that the words in ACL's code carry no meaning that steers its people: if Test 1 is identical, the names are
just labels. It cannot show that nothing else is scripted: the physics (which material floats, which is sharp) is
chosen by the creator, as nature, and must stand on its own evidence (a further test could swap physical properties
between materials, the "change the physics" test, as a later study).

## The assistant's prior (to be frozen at sign-off; held loosely)

Test 1: identical in every world. Test 2: no meaningful difference in any outcome, with individual histories diverging
from the first tie that sorts differently.

## Decisions for the creator

1. Tests: **both, Test 1 first** (recommended), or Test 1 only.
2. Worlds for Test 2: **256 new seeds** (recommended), or 64.
3. Order: **Test 1 now** (it is short: about an hour on two spare workers), Test 2 after the queued runs.
4. Later: draft the "change the physics" test (swap floating and hardness between materials) as NS2, or not.
