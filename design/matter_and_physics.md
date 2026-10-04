# Matter & Physics: design note (draft for the creator's approval)

**Status:** nothing built, and all code is frozen. Before any code, the creator must approve three things:
1. how to read v8.1's "discrete core" rule (§7);
2. which processes go into the first version (§4; core or second);
3. E6's predictions (§8), frozen before any run.

Bible: v8.1 Chapter 3 (Matter, Physics & Chemistry) of the first-stage architecture, and Laws 4, 105–120 of the
law ledger.

---

## 1. The problem, from evidence

E5 (8 worlds × 1000 years): every kind of tool any world ever had appeared in the first 11 years, and nothing new
appeared in the 990 years after. Spears and warm wrappings were lost and never came back. A 1000-year world and a
20-year world were almost the same world.

The cause is in the code, not the agents:

- **Making:** 6 materials (stone, flint, bone, wood, fibre, hide), 2 ways to work them (strike, bind), 6
  properties (edge, reach, hard, contain, warm, float).
- **What a thing does:** `matter.factor(item, use)` multiplies one of about 9 fixed efforts (forage, hunt, wood,
  stone, fibre, fight, carry, cold) and float lets a person cross water. No invention creates a new resource, a
  new action, a new place to live or a new problem. The best possible spear only makes hunting a bit easier.
- **Depth:** every result is one or two steps from raw materials. Play tries every combination within a decade.

The one invention with a consequence beyond a multiplier, the raft, opened new land. It was also the one that
changed history (crossings, isolation, E4's band fates).

So two things are missing:
- **Consequence:** a thing should be able to change *what is possible*, not only how fast something goes.
- **Depth:** some results should need the products of earlier results, plus conditions that are rare or found only
  in some places. Then discovery spreads over centuries and differs from island to island.

## 2. Principles: every piece must pass all seven

| | Principle | Test |
|---|---|---|
| P1 | **Properties, never products.** No human invention is named in the code. | Search the code: no `pot`, `oven`, `kiln`, `bow`, `house`, `bridge`, `cook`, `pottery`, `boil`, `smoke` as code paths. |
| P2 | **One rule, many consequences.** Each process is a general rule over properties. | A rule that opens only one human invention is a recipe in disguise: reject it. Each rule must open at least 2 unrelated possibilities. |
| P3 | **Outputs are states, not new kinds.** A process changes the property values of the same stuff. | Wet clay, dry clay and fired clay are one material in three states. The observer may name results; the code never does. |
| P4 | **Consequences are physical, not bonuses.** What a thing does comes from how its properties meet the world. | Water stays in a container only if the container is tight enough; a heavy thing needs more hands. No new multiplier is added to `factor`. |
| P5 | **Depth and place.** Some inputs exist only in some places; some states need products of other processes. | No step is gated by a flag or an unlock. The only gates are physics and geography. |
| P6 | **Agents learn everything.** Nothing is innate (Law 44); usefulness is discovered (Law 109). | Agents meet properties only through outcomes, as now. |
| P7 | **Responses before pressures** (the creator, 2026-10-03). | This chapter adds no new way to die except what its physics implies (e.g. fire spreading). Disease and parasites come with biology, after. |

## 3. Properties: what exists, what is proposed

| Property | Now | Proposed |
|---|---|---|
| weight | none (carry limits on totals) | **mass** per material and item; a person carries up to a limit; heavier things need several people at once, or water to float them |
| temperature | places are hot or cold; things are not | **heat** of a thing: raised by fire, lost over time |
| hardness | `hard` | unchanged; heat and moisture can change it |
| flexibility | a yes/no list (`fiber`, `hide`) | a value per material; heat and moisture change it |
| buoyancy | `float` | unchanged |
| combustion | fire burns wood and fibre, by name | **fuel** per material, and what burning leaves behind (ash, charred remains with high fuel) |
| durability | `uses` | unchanged; moisture and heat change it |
| moisture | none | **wetness** of things and heaps; rain and rivers wet, sun and fire dry; wetness changes weight, rot, burning, warmth, flexibility |
| *tightness* (new) | none | how well a thing holds liquid; needed for containers of water |
| *plasticity* (new) | none | whether a thing takes and keeps a shape when wet; high for clay, about 0 for everything now in the world |

The 2 new properties follow from the creator's list: containers need tightness, and shaping needs plasticity.

## 4. Processes: general rules

**Core** (the first version, if approved):

- **4.1 Heat.** A fire heats what is in or next to it. Every material responds by its own data, as changes in its
  properties only:
  - moisture leaves;
  - things with fuel burn down to ash or charred remains;
  - plastic things that are dry harden and become tight;
  - wood hardens a little;
  - hide stiffens;
  - **food changes state:** it keeps longer and goes further.

  This replaces today's flat `cooking_saving` (fed 15% more when a fire burns on the tile) with a change in the
  food itself. Changed food can then be carried and stored, not only eaten at the fire.

  *Opens, without naming any of it:* food that keeps, hardened points, fired clay, carried embers, charred fuel.
- **4.2 Wetting and drying.** Rain, floods and rivers wet things; sun, wind and fire dry them.
  - Wet things are heavier, burn badly, rot faster and keep out less cold.
  - Wet plastic things can be shaped.

  *Opens:* seasonal timing of work, dry storage, shaping, and the reason to keep things covered.
- **4.3 Containers hold substances.** A held thing can contain water, food, seeds or embers, if its properties
  allow. Water needs tightness, embers need resistance to heat, and how much fits comes from `contain`.

  *Opens:*
  - water carried away from any spring, so dry land and long voyages become livable;
  - food kept from rot and animals;
  - fire carried to wherever one goes.

  It also gives today's `contain` property a physical meaning beyond "carry more food".
- **4.4 New raw stuff, by place.** Clay, found only at wet ground by rivers and lakes. Plus the outputs of
  processes (ash, charred remains). Nothing else new in the first version.

**Second** (can follow in a later version, or be cut):

- **4.5 Mass and moving together.** Everything has mass. A thing heavier than one person's limit moves only when
  several people move it in the same week, or when it floats. Coordination (Law 97) then comes from physics,
  with no coordination feature.
- **4.6 Placed things change places, by properties, not names.**
  - Generalise today's heaps (`pile_shape` uses wood, stone and bone for walls and hide and fibre for cover, by
    name) to properties: enclosure from hard, long things; cover from flat, flexible things.
  - Add two more: **barrier** (animals cannot pass a hard, tall heap) and **span** (a long, rigid thing laid
    across one tile of water can be walked).
  - The rules would be tuned so today's materials give today's results.

## 5. Primitive actions (Law 106): from 17 to 20

| New action | Meaning | Works on |
|---|---|---|
| `heat` | put a held thing in or next to a fire, and take it out later | anything held (today only fuel and food go near fire, through `put`) |
| `shape` | press a wet, plastic thing into a form: hollow, long or flat | anything plastic (clay; maybe wet hide) |
| `fill` / `pour` | put a substance into a held container, or empty it | water at a source, food, seeds, embers |

The forms (hollow, long, flat) are geometry, not products. A small fixed set of forms is a mild limit on
open-endedness; see §7.

`play` may try any primitive with anything, as it does now. That is how the new rules get discovered.

## 6. What this must not script

- No code path named after a human invention: pot, oven, kiln, bow, house, bridge, cooking, boiling, smoking, pottery.
- No reward for using the new actions, no knowledge of them at birth, no new multiplier in `factor`.
- No guaranteed path. Clay plus shaping plus heat *permits* a fired, hollow, tight thing; whether any world ever
  makes one is a question for E6.
- The observer may name things after the fact (as `historian.classify` does now). That is measurement only and
  never feeds back into the world.

## 7. Law accounting (proposed)

**Implements or strengthens:**

| Laws | What changes |
|---|---|
| 4 | Things have state that changes. |
| 5 | Mass makes carrying cost something. |
| 6, 7 | Clay is a resource found only by water. |
| 8 | Weather wets and dries things. |
| 14 | Carrying water lets people live farther from fresh water. |
| 29, 31, 73, 112, 113, 116, 120 | Results become inputs to later processes, so discovery can cascade. |
| 97 | Heavy things need several people (second version). |
| 105, 107, 108, 118 | The world resolves everything from properties. |
| 109 | Uses are discovered. |
| 123 | Ash and charred remains are traces. |

**Risks and departures:**

- **Laws 105/107: per-material heat responses could become hidden recipes.** Guards: P2 and P3. Responses are
  property changes only, never named outputs, and every rule must open 2+ unrelated possibilities.
- **v8.1's first-stage rule:** "runtime core state should remain deterministic and discrete where practical."
  This chapter adds new quantities (mass, wetness, heat).
  - **This is the one decision that changes how the code is written, so it is needed before any code.**
  - If the creator reads "discrete" literally, the new properties should be small whole-number levels (e.g.
    0–4) from the start. That is far cheaper now than converting later.
  - If the concern is reproducibility, decimals with the existing determinism checks are enough.
- **Law 106:** a fixed set of forms for `shape` (hollow, long, flat). This is acceptable as geometry, but noted.
- **Comparability:** replacing `cooking_saving` changes the existing world, so E5 and E6 are different worlds.
  That is expected. They are compared on the same novelty measure (§8), not on population.
- **Left for later on purpose:** disease, injuries, organs, parasites (biology, Ch. 5), and better genetics (Ch. 6).

## 8. E6: the experiment (draft; to be frozen before any run)

**Question** (the creator's): *Can the world still create genuinely new behaviours after year 100?*
Population, survival and births are not the measure.

**Measure.** A new read-only recorder, proved by state hash not to change the world. It defines novelty without
human names:

- **New kind of thing:** a property profile (each property in 5 bands) that never existed before in that world,
  made 3+ times.
- **New behaviour:** a combination of (action, kind of thing used, kind of thing acted on) never seen before in that
  world, done by 3+ people within 10 years.
- **New consequence:** the first time something physically new happens because of a thing. The list is derived
  from the physics, not from inventions:
  - water carried 5+ tiles from any source;
  - fire burning where no lightning or sparks started it;
  - food eaten after its natural rot time;
  - a tile crossed or blocked because of what was placed there;
  - a heavy thing moved by several people.
- **New tradition:** a technique, practice or behaviour that first appeared after year 100 and was held by 3+
  people for 100+ years.

**Baseline.** Re-run E5's 8 seeds with the recorder on the current code. This is deterministic and read-only, so
it gives the novelty curve of today's world without changing anything.

**Design.** E6 uses the same 8 seeds (301–308; the same maps and founders) under the new physics, for 1000 years,
compared pair by pair.

**Claude's draft predictions** (the creator adds theirs before freezing):
1. Baseline: fewer than 10% of all novelty events in E5 happen after year 100.
2. E6: at least 25% of new kinds and new behaviours appear after year 100, in at least 5 of 8 worlds.
3. E6: at least one new tradition that began after year 100, in at least half of the surviving worlds.
4. E6: worlds whose people live near clay make different things from those that don't (place shapes culture).
5. E6: no more worlds die out than in E5 (3 of 8 or fewer). This chapter adds responses, not just deaths.

**Kill criterion:**
- The design failed to add depth if E6's share of novelty after year 100 is not higher than the baseline's in at
  least 6 of the 8 seed pairs, or is under 10% overall.
- As always, the experiment is void if any run crashes, the code changes during it, or fewer than 6 worlds
  complete.

## 9. Order of work, if approved

1. The creator decides the "discrete core" question and cuts or keeps each process (§4).
2. Write the novelty recorder and run the baseline on the current code. No world rule changes.
3. Freeze E6's predictions.
4. Build the approved processes, with law tests:
   - no human-invention names in the code;
   - each process opens 2+ consequences;
   - all existing tests still pass.
5. Report the feature with law accounting, then run E6.
6. If E6 bears it out, propose a candidate law for the next Bible version, roughly "Creation must be able to
   change what is possible, not only how well". Evidence comes first, so it is not drafted now.

---

## As built (2026-10-03; in `experiments/E6_novelty/code_e6/`, not yet in the main code)

**Creator's decisions:** core processes only; whole numbers from day one; main measure is latest first appearance.

**Built:**
- **Properties:** 10 lasting properties, whole numbers 0–100 (see the scale note below). Wetness and fire heat
  are passing states on 0–10. New materials: clay, on river banks and lake shores, regrowing slowly; and char,
  left by a fire that has burned hot for a while.
- **Heat** (`matter.heat`). The same rule for everything:
  - it dries what is wet;
  - something dry that burns well catches and is gone, feeding the fire;
  - something plastic sets hard and tight if dry, harder and tighter in a hotter fire, and cracks if still wet.

  A fire burns as hot as the best dry fuel in it: fibre 5, wood 6, char 8.
- **Food held in a fire** (action `heat`). It rots at a quarter of the usual rate and goes 15% further, wherever it
  is eaten. That includes stashed food. Eating beside a fire still counts as before.
- **Wetting and drying** (`biology._wet_and_dry`):
  - a rainy week in the open soaks carried things to 5 of 10, and going into water soaks them to 10;
  - a dry week dries them by 4 (6 in summer), and a fire dries them completely.

  Clay can be shaped at wetness 4 or more. Fuel above 3 burns weaker and no hotter. Tinder that is soaked (above
  5) will not catch. Wet coverings keep out less cold. Soaked embers go out.
- **Containers hold substances** (action `fill`).
  - Water needs holding 40+ and tightness 50+.
  - Embers need holding 30+, hardness 40+ and fuel 20 or less.
  - Carried water is drunk where none can be found.
  - Carried embers tipped onto dry fuel light a fire.
  - The seam where two coverings are bound together keeps liquid in only as well as the binding: hide tied with
    hide holds water, hide tied with fibre does not.
- **New steps for play and make:** `shape` (soft stuff into hollow, long or point) and `heat` (hold a material or
  thing in the fire). Primitive actions went from 17 to 19: `heat` (food) and `fill` (fill, or tip out). Shaping and
  heating things are steps inside play and make, as striking and binding already are.
- **Means to ends:** a made thing that goes into something a person values counts as worth making, so chains
  of steps can be repeated. This extends the existing pull toward materials for valued things to made parts.
- **Tests:** 8 new physics tests (P1 and P2 among them) plus the 47 existing law tests, all passing. The P1 test
  checks every name and key in the code for human inventions. It caught one already in the old code,
  `cooking_saving`, which is now `heated_food_saving`.

**Calibration problems found and fixed before any E6 run (development seeds only):**
- Wetting at +3 per rainy week and −2 per dry week left carried things wet almost all the time, since it rains
  about 45% of weeks, and fire-making collapsed. Replaced with the soak/dry rule above.
- On a 0–10 scale, small strikes rounded to nothing. Sharpening a stick on a stone and flaking stone on stone
  then always failed. Hence the 0–100 scale, and strikes round to the nearest step.

**Found, not changed (a condition of the world, not a bug):** fire is rare and brief. In a development world
adults stood at a burning fire for 33 weeks in a century. Fires come from sparks, last a week or two, and are
seldom fed. Every consequence of heat is gated behind that.

**Law accounting for what was built:**

| | Laws |
|---|---|
| Implements | 4, 5, 6, 7, 8, 14, 29, 31, 73, 105, 107, 108, 109, 112, 113, 116, 118, 120, 123 (shards and ash are traces) |
| Partly | 106: shaping and heating are steps inside play/make (as before), not separate actions; holding food in a fire and fill/tip are separate actions |
| Departure | v8.1's first-stage rule: matter is discrete now, but the rest of the core (minds, bodies, genes) still uses decimals |
| Departure | `heat`'s food rule, `can_hold`'s thresholds and the soak/dry numbers are tuned by hand, not derived from a physical model (as all of `config.py` is) |
