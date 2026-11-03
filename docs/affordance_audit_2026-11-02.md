# What can made things do in ACL, and what stops them? An audit of nature v11 (2 November 2026)

**Why:** the creator, 2 November 2026: "we should give them all possibilities … you gotta check all other inventions if
its restricted in some way of usage or not". UP1 and WP1 showed new inventions are never remade. The creator suspects
the world itself gives too few possibilities.

**What it is:** a read-only reading of the code (`acl/`, nature v11), with file and function names. It changes
nothing. Every limit below is a **written law**; none was found by running worlds.

## A. What a made thing can do today
A made thing is described only by 10 properties: edge, reach, hard, contain, warm, float, tight, plastic, fuel, flex.

| use | which properties count | where |
|---|---|---|
| foraging | edge, contain | `matter.factor` "forage" |
| hunting, fishing | edge × reach, hard × reach | "hunt" |
| fighting | edge × reach, hard × reach | "fight" |
| gathering wood | edge × hard | "wood" |
| gathering stone, flint, clay, char, and digging | hard | "stone" etc.; `actions._dig` |
| gathering fiber | edge | "fiber" |
| carrying **food and seeds**; easier trips to far water | contain | `matter.carry_capacity`; `weather.drink` |
| keeping warm (worn) | warm (less when wet) | `matter.worn_warmth` |
| crossing water | float | `matter.best_float` |
| holding **water** | contain ≥ 40 and tight ≥ 50 | `matter.can_hold` |
| holding **embers** | contain ≥ 30, fuel ≤ 20, hard ≥ 40 | `matter.can_hold` |
| scratching marks | hard, edge | `marks.tool_of` |
| a part in another thing | any | bind (two parts), heat (one part) |
| handing to another person | — | `actions._hand` (v11) |

## B. Fixed limits that no invention can change
1. **3 made things per person** (`config.item_limit`).
   - Picking up a 4th drops the least valued on the ground (`actions._keep`).
   - A container does **not** raise it.
2. **20 raw materials per person** (`config.material_limit`). A container does not raise it either.
3. **Only food, seeds and water trips** benefit from a container.
   - The carry factor `1 + contain` multiplies the food limit (`matter.carry_capacity`).
   - It also lowers the effort of walking to water further away (`weather.drink`).
   - It does nothing for made things or materials.
4. **Only one thing counts per use.** `matter.best_item` takes the single best item. Two tools never help together, and
   two warm things worn never add up.
5. **Containers hold only water or embers** (`matter.can_hold` returns 0 for anything else). Food, seeds, materials and
   made things cannot be put **into** a container.
6. **Nothing made can go into a heap.** The things that can be set down (`person.PLACEABLE`) are seeds, food and raw
   materials only.
   - So a shelter (`matter.pile_shape`) is built only from raw wood, stone, bone, hide and fiber, never from made
     things.
   - Made things cannot be stored in a cache.
7. **No carrying for someone else, and no making together.** People can hand a made thing over (v11), but there is no
   joint work on one thing.

## C. Limits on how things are made
8. **A recipe is exact.** To make a thing again, a person needs the **same kind** of each made part (`mind.can_make`
   checks the part's exact name) and the **same binder**. A part with nearly the same properties does not count. This
   is the creator's "alternatives" point, and UP1's "cannot make".
9. **Binders must be raw:** fiber or hide (`matter.FLEXIBLE`). A made cord, for example bound fibres, can never tie
   things.
10. **Striking uses only raw materials** (`actions.STRIKABLE`, `actions.HARD`). A made hammer or a hafted stone can
    never be used to flake anything.
11. **Shaping uses only raw soft material** (clay), into three forms (hollow, long, point; `matter.FORMS`).
12. **Binding joins exactly two parts.** More complex things must nest, two at a time, one level per making.
13. **Only five ways to make:** strike, bind, shape, heat, fill.
14. **Made things only wear out.** There is no repairing and no reworking. A worn thing disappears (`matter.wear`).

## D. Properties that do little
- **flex** matters only for raw binders. A flexible **made** thing has no use for its flexibility.
- **tight** matters only for holding water.
- **fuel** matters only for raw fuel in fires. A made thing's fuel value is never used.
- **plastic** matters only before shaping.
- **reach** matters only in hunting and fighting. A long thing cannot reach fruit, cross a gap or carry a load.

## E. What this means (the assistant's reading; for the creator and the council)
- **The creator is right that the world limits invention.**
  - New things can be **made**, but most of what they could **do** is closed off by fixed laws: the 3-thing limit, one
    tool at a time, containers that hold only food or water, heaps of raw things only, exact recipes, raw-only binders
    and hammers.
  - In UP1's terms, a new kind has few uses, so it is rarely worth much. When it is, it cannot be rebuilt from
    alternatives.
- **None of these needs an invention named to fix it.** Each is a law that could be made general, following the
  physics already written (properties). For example:
  1. **make by what it does:** a part close enough in its properties can stand in (C8);
  2. **any part, any binder:** a made thing can be a binder if it is flexible enough, or a hammer if it is hard enough
     (C9, C10);
  3. **containers contain:** a thing's `contain` lets it carry made things and materials, not only food and water (B1,
     B2, B3, B5);
  4. **heaps of anything:** made things can be set down and built with, judged by their properties (B6);
  5. **tools together:** more than one item can help in one use, with less from each extra (B4).
- **Each would be a frozen test in a copy** first, one at a time or in a small set of arms, with a sham and no target
  outcome. **The creator chooses which to try**; GPT and Gemini are consulted on the design.
- **A risk to name: "give them all possibilities" must not become "give them the answer".** Each rule above opens a
  possibility through properties; none adds a recipe, a reward or a named thing.
