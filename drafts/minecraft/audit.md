# ACL in Minecraft: what transfers? (read-only audit of the live code, nature v2; 17 October 2026)

**Asked by the creator** ("yes do the audit now"). Nothing built, installed or decided. Plan context: ACL's people (minds
and lives unchanged) in a Minecraft world edited to ACL's rules (`memory: acl-minecraft-idea`). Method: every place the
mind, body and world processes read or change the world (`world.*` accesses per module, tile properties used), checked
against what Minecraft has.

**A correction first.** I said ACL's people have no notion of building. Wrong: the `put` action sets materials down on a
tile, and the heap's physics (`matter.pile_shape`) gives **enclosure** (wood, stone, bone) and **cover** (hide, fibre,
wood); together they give warmth and room. Nobody scripted a shelter; since E1, heaps the historian names shelters have
appeared, and in two E1 worlds a scratched mark meant "shelter" for 33 and 38 years. So building maps well onto Minecraft.

## 1. What the mind reads (perception)

| ACL input | where in ACL | Minecraft equivalent | verdict |
|---|---|---|---|
| own body: hunger, food held, thirst, cold, health, items | person | food bar, health, inventory; **no thirst, little cold** | bridge keeps ACL's body (§3) |
| the 32 situations: food on hand (4) × company (2) × season (4) | `mind.context_index` | food in inventory; others nearby; **no seasons** | transfers if the bridge supplies a season |
| people within sight (4 tiles) and reach (3): who, kin, relations | `world.people_near`, `kinship` | other bots' positions | transfers (distances in blocks: a mapping choice) |
| tiles within sight: plant food, wood, stone, flint, fibre, clay, fire, heaps, stores, marks, traces, water, biome, temperature | `world.tile` | blocks and biomes; no fibre, no wild plant food to speak of | partly (§2, §4) |
| animals nearby | `fauna.near`, herds | passive mobs (cows, pigs, sheep, chickens, rabbits, fish) | transfers |
| sky, weather, season | `world.sky`, `season` | day/night, rain, snow; **no seasons** | season needs a plugin |
| islands (which land is connected) | `world.island_of` | continents, rivers, oceans | bridge computes it |
| walking, water blocks the way without a float (Rule 3) | `step_toward_land`, `walk`, `passable` | real pathfinding; swimming exists | **a real difference**: Minecraft people can swim |

## 2. The 19 actions

| action | Minecraft | verdict |
|---|---|---|
| rest | stand / lie still | easy |
| forage (wild plant food) | sweet berries (taiga), apples (rare, from leaves), glow berries (caves); carrots and potatoes only in villages, which are removed | **mismatch: almost no plant food** — needs an edit (§5) |
| hunt | kill passive animals by hand; meat, leather | easy; much easier than ACL's party hunts |
| gather (wood, stone, flint, fibre, clay, hide, bone) | logs by hand; **stone needs a pickaxe**; flint from gravel; clay by hand; leather from cows; **no plant fibre** (string comes from spiders); bone from skeletons, removed | mixed: **tools gate stone**, the opposite of ACL's generous earth |
| put / take | place / break blocks; drop / pick up items | easy; **warmth from real walls and roof** (bridge measures enclosure around a person) |
| make (tie, strike, shape, heat by properties) | crafting grid with fixed recipes | **the big decision** (A: keep recipes, hidden, found by trial; B: ACL's property physics as a mod) |
| heat (hold in fire) | campfire or furnace, both crafted; **fire itself needs flint and steel (iron)** | **mismatch: no fire early** — ACL strikes flint for sparks; needs an edit |
| fill (a vessel with water) | buckets need iron; bottles need glass | mismatch: no vessels early |
| play, explore, join, flee | movement with a pathfinder | easy (pathfinding is fiddly, not hard) |
| give | toss an item to someone | easy |
| care (feed, carry a child) | bridge-mediated | bridge |
| talk, court (gossip, stories, where things are, how to make, affection) | mind to mind through the bridge; chat only shows it | transfers **unchanged** |
| steal | take from another's inventory: not possible in Minecraft | bridge-mediated transfer |
| attack | hit (real damage) | easy |

## 3. The body (ACL's biology, kept in the bridge)

Hunger (linked to the food bar), **thirst** (new for Minecraft), **cold** (biome temperature, snow, rain, night, against
warmth from worn things, fire and walls), illness, injury, ageing (ACL's Gompertz, paused anchor noted), pregnancy,
**birth** (spawn a child bot; children follow their carer), death. All exist in ACL's code (`biology.py`); they need a
reader for Minecraft's state, not new rules.

## 4. What transfers unchanged

The whole mind: temperament, drives, habits (the 608-value table and its learning), memories, beliefs, relationships,
know-how, talk, stories, gossip, marks as symbols (if the bridge keeps marks on blocks), kinship, partner choice, the
historian outside. These touch the world only through perception and actions.

## 5. What Minecraft lacks, and edits it would need (each a condition, written down first)

| missing | why it matters for ACL | possible edit |
|---|---|---|
| seasons | the 32 situations, winter, storage, sowing | a server plugin (Java) changing growth and snow by season |
| wild plant food | ACL's main food; without it, people are hunters only | forageable yield from grass, leaves, bushes by biome (plugin) |
| plant fibre | binding (tying) is how ACL makes composites | fibre from tall grass (plugin), or accept the gap |
| fire without iron | warmth, heat, cooking, fired clay | striking flint on stone makes sparks (plugin or bridge) |
| thirst | water drives where people go | in the bridge (ACL's rule) |
| marks scratched on things | symbols (E1's marks lasted decades) | the bridge records marks on blocks |

## 6. What Minecraft adds (and ACL has never tested)

Tools that matter (stone and ores need pickaxes); 3-D land, caves, cliffs; **falls, lava, drowning, suffocation**;
swimming; real animal behaviour (Minecraft's own mob AI); fixed recipes. Several are exactly what the council suspected
ACL lacks (tools that matter: Gemma's "force-to-open food").

## 7. The two hard problems

1. **The mind reads ACL's world directly** (about 60 `world.*` calls in `mind.py` alone). It needs one adapter, a
   "world view" that answers the same questions (`tile`, `people_near`, `season`, `island_of`, `walk`, `passable`, …)
   from Minecraft's state. The rules stay; only who answers changes. This is most of the engineering.
2. **Time.** ACL decides once a week; generations need decades. If one ACL week is one Minecraft day (20 minutes), a year
   is 17 hours and a century 72 days: too slow. Minecraft's `/tick sprint` (Java 1.20.3+) can run the world faster;
   bots still need real ticks to walk. Realistic guess: **a century in several days of running, for one world at a time.**
   So: case studies of a few worlds, not ACL's 256-world statistics.

Also a choice with no anchor (as N10 found for ACL's tile): how many blocks a tile is (sight 4 tiles = 64 blocks if a
tile is a 16-block chunk).

## 8. Verdict

**Transfers unchanged:** the mind and the social life (the most important part). **Reimplemented in the bridge from ACL's
own rules:** the body. **Needs edits to Minecraft:** seasons, plant food, fibre, fire from flint (the four that most
change what life is like). **New, untested:** tools that gate stone, 3-D hazards, swimming. **Hard:** the world-view
adapter and time.

**Suggested first milestone (when unparked):** the adapter plus one person, no edits beyond the server settings, on a
flat test map, living one Minecraft day per ACL week: does the mind act sensibly through the bridge (forage, hunt, rest,
put, flee)? That checks problem 1 before any world-editing is built.
