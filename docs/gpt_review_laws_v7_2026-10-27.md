# Review of all 38 laws of nature v7 (GPT's and Gemini's opinions, not sign-off)

**The creator's request (27 October 2026):** "lets work on laws then … Send whole laws to both gpt and gemini to check".
The same request and `docs/laws_of_nature_v7.md` went to both (GPT as a file, Gemini as text); Claude was council.

## GPT, in short
- **Keep most laws.** The strongest is law 12 (making by real properties, no named inventions).
- **The world is sometimes too restrictive:**
  - made objects cannot persist anywhere but in hands or on a body (law 15);
  - extra objects vanish (law 13);
  - watching is very narrow (law 30);
  - tools cannot be given (law 37).
- **The mind is "too generous and too limited at the same time":**
  - it copies or inherits large tables without experience (laws 25, 27);
  - yet it learns poorly from real observation, values delayed consequences badly, and rarely explores (laws 16–18);
  - the 32 situations may be too coarse (law 17: "state confusion", e.g. a person with a working tool and an injured
    empty-handed person are in the same situation).
- **Possible built-in answers:** law 21 (seasonal anticipation), law 27 (newborns inherit habit values), law 28,
  law 34 (marks with predefined meaning). Also: the care cut-off at exactly 12, and the arbitrary link between
  overthinking and lower trust.
- **Its order:**
  1. finish HC1;
  2. law 15, letting made objects exist on the ground;
  3. law 13, dropping instead of deleting;
  4. laws 30 and 37 separately (watching someone make; handing tools over);
  5. then cognition (laws 17–19, 28).
- "Give Bob a world where things can happen, and a mind that can learn why they happen. Don't give him the answers, and
  don't make success inevitable."

## Gemini, in short
- **Wrong or against the mission:**
  - law 25 ("telepathic" whole-table copying);
  - law 13 (silent deletion: "violates conservation of matter");
  - law 29 (memory order);
  - law 28 (shallow parts-first);
  - laws 11 and 15 (material piles cannot be gathered back).
- **Missing:** objects lying on tiles; handing tools to the living; learning by watching someone make or use a thing;
  teaching more than one level deep.
- **Its order:** HC1, then law 29 (memory order), then laws 13 and 15 (drop onto the ground).
- **Arbitrary settings:** the care cut-off at 12, the 12-recipe memory, the 3-item limit, the 0.05 learning rate, the
  0.2 temperature.

## Council checks (against the code)
| claim | who | check | result |
|---|---|---|---|
| Made things cannot be set down (law 15) | GPT | `_put` handles food, seeds and raw materials only | **right**; the document was wrong; corrected |
| The limit is 3 made things in total, not per kind (law 13) | GPT | `item_limit` 3; `_keep` deletes the extra | **right**; corrected |
| Watching happens only on joint hunts and floats (law 30) | GPT | `knowhow.watch` is called only from `resolve_hunts` and `_over_water` | **right**; corrected |
| Material piles cannot be gathered back (law 15) | GPT, Gemini | `_gather` reads `Tile.material`, not the pile | **right**; corrected |
| Tools cannot be given to the living (law 37) | both | `_give` moves food, then seeds; never items | **right** |
| "TF1: 12% of new tools and 99% of new invention types are deleted the week they are made" | Gemini | TF1: 12.4% of things made in **play** vanished the same week, and 98.8% **of those** were new kinds (4.1% of things made deliberately) | **partly right; wording corrected** |
| Fix the memory order next (law 29) | Gemini | MO1 was **not supported** by its frozen rule; a re-test is the creator's decision | **not adopted by the council**; left to the creator |

## Where they agree
- Finish HC1 first.
- Then **objects in the world**: let made things exist on the ground and be dropped, not deleted.
- **Teaching deeper** and **learning by watching** are missing abilities.
- Several settings (12 recipes, 3 items, age 12, 0.05, 0.2) are arbitrary assumptions, not discovered limits.
