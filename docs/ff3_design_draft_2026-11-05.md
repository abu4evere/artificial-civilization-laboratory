# FF3 design draft: memory ties settled by name (5 November 2026; a draft, not frozen)

**Status:** a draft for the next fault-fix round, after RF1 (which may add faults in how the inputs for remaking are
sought). Nothing here is frozen or run.

## The fault found (F9)
`knowhow.remember_recipe` (lines 80–82): when the 12-recipe memory overflows, it drops
`min(p.recipes, key=lambda s: (value, name))`.
- On a tie in value, the recipe's **name** decides, in alphabetical order.
- Made kinds are named `(a+b)#binder` (`matter.py` line 125), so a more nested, more complex kind starts with more "("
  and sorts first.
- **Measured (VA1, `findings.md`, appended note):** 130 of the 155 new kinds invented with a full memory were ties at
  value 0, and 129 of those were lost. The written rule ("the least valued is dropped", `docs/ODD_v11.md`) says nothing
  about ties.
- **Council round 66:** all three models call it a fault. **GPT's split is adopted:**
  - the fault fix is a name-free tie-break with its own random stream;
  - "the longest-unused is forgotten" is a separate law (recency), tested later against the corrected baseline.

## The same pattern elsewhere (found by reading the code, 5 November 2026)
Each of these drops the minimum with the key's text as the tie-break:

| place | what is dropped | key | how often ties happen (to be counted) |
|---|---|---|---|
| `knowhow.remember_recipe` line 81 | a recipe (12) | the kind's name | often: new and untried recipes sit at exactly 0 |
| `inquiry` line 58 | a puzzle | "m:" or "f:" + the kind's name | rare (sizes are continuous, rounded to 3 decimals); the same lean against complex kinds |
| `information._note` line 97 | a record of a source | a person's id | rare (sums of rounded numbers); leans against older people (lower ids) |
| `knowhow` line 207 | a known place | "x,y" | rare (values decay continuously) |
| `marks` line 222 | a known mark | the shape | to be counted |

Items (`actions.py` line 487, `biology.py` lines 615 and 769) break ties by position (the order acquired), not by
name, and are not part of this.

## The proposed fix (to be frozen as FF3, a fault-fix check in a copy, as FF2)
- **A setting**, `fix_name_ties` (0 = v13 exactly). With 1, a tie at the minimum is settled by a draw from a
  **dedicated random stream**, so no other random draw in the world shifts.
  - The stream is seeded from the world's seed, the tick, the person's id number, and which memory it is (integers
    only, never Python's string hash).
- **Which memories:** first a cheap read-only count of how often each of the five ties actually happens. Then fix
  those where ties occur, or all five for consistency. That choice is for the council.
- **Arms** as in FF2: v13, the fix, the sham. Harm guards for population and extinction. Paired seeds; 200 years.
- **Adoption** by the fault-fix path in CLAUDE.md: zero checks, the tests, a recorded check showing the fault, and the
  harm check. Then `code_v14`, reference hashes, a tag, a Telegram message to the creator.

## Later, a law, not a fault
"The longest-unused recipe is forgotten" (recency; Anderson & Schooler 1991,
`docs/research/memory_recency_forgetting_2026-11-05.md`). This would be a frozen law test against the corrected
baseline, with a sham. It is not part of FF3.

## Appended 6 November 2026, 00:04: how often each tie happens (exploratory, `experiments/FF3_name_ties/explore_ties.py`)
Seed 9812, 60 years, nature v13, each call site counted apart (`explore_ties_9812.json`). A tie means the minimum
value is shared, so the second part of the key decides.

| memory (call site) | evictions | settled by the tie-break | tied candidates in all |
|---|---|---|---|
| recipes (`knowhow` 81), by name | 4,142 | **2,656 (64%)** | 11,005 |
| known marks (`marks` 222), by shape | 51,618 | **17,387 (34%)** | 49,275 |
| source records (`information` 97), by person id | 1,429 | **210 (15%)** | 2,367 |
| puzzles (`inquiry` 58), by name | 14,373 | **1,341 (9%)** | 2,906 |
| known places (`knowhow` 207), by "x,y" | 171,922 | 0 | 0 |
| marks on a tile (`marks` 142), by position | 1 | 0 | 0 |

The first pass (seeds 9811 and 9812 together, call sites merged) is kept in `experiments/FF3_name_ties/v1/`.
- **So the name decides most of the recipe forgetting, and a third of the mark forgetting.**
- Places never tie, so they can be left out of FF3.
- These are counts from one world, exploratory, not a frozen measure.
