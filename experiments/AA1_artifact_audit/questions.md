# AA1 — Do ACL's people exploit flaws in the simulation? (SIGNED OFF and frozen as `AA1-frozen`)

**Signed off by the creator (October 2026):** keep the 5% threshold but report absolute counts and uncertainty, and never
dismiss a near-threshold shortcut automatically; add an audit of **information people should not have**, limited to what
the code actually permits; classify every shortcut against the world's intended rules before calling it a flaw; fix
nothing because it looks unrealistic; any fix is a new version compared against the original baseline, which is kept;
run after WS1 and **before ID1**, because its findings may change how ID1 is read. Nothing has been run.

**Asked by the creator (October 2026),** as the honest version of "can a civilization discover it is simulated?". ACL's
people cannot reason about their universe, but they can learn, without knowing it, to rely on shortcuts in the code that
have no counterpart in nature. That happened once already: in E1, 92% of crossings between islands used a gap in the
movement rules that let people jump channels up to three tiles wide (book, "The Raft"). A finding built on such a
shortcut would be an artefact, not a discovery. **AA1 is a validity audit: read-only, no change to ACL.**

## Candidate shortcuts (from a read-only reading of the code; more may be added before freezing, none after)

| | candidate | where | why it could matter |
|---|---|---|---|
| **A1** | **corner crossing:** a diagonal step from land to land between two water tiles that touch only at a corner, crossing a channel without anything that floats | `world.walk` steps one tile at a time and diagonal steps are allowed; only the destination tile is checked | islands meant to be separate may be joined; contact, partners and spread of knowledge between islands would be inflated |
| **A2** | **the wrapping edge:** walking off one side of the map and arriving on the other | every distance and step is on a torus (`util.torus_delta`) | if the edges are land in some worlds, people far apart on the map are near in fact |
| **A3** | **food of the dead becomes wild plants:** food carried by someone who dies with no heir nearby is added to the tile's wild plants, above the tile's cap | `biology.py` (noted in HF1's correction) | foraging on death sites would be a food source with no natural counterpart |
| **A4** | others found in a full read-only review of movement, foraging, giving and storage code before freezing | — | — |
| **A5** | **knowing where absent loved ones are now:** a person whose partner, parent, child or best friend is out of reach walks toward that person's **current** location, anywhere in the world | `mind._far_people` reads `q.loc` with no limit of sight or memory | added at sign-off (information audit): couples and families may stay together more than people could manage without such knowledge (C1, GF1); N8 recorded that people remember others but not where |
| **A6** | further information shortcuts: any place where a person's choice reads another person's private state (habits, temperament, food held), a tile's contents beyond sight, or the random stream's future | to be listed in the read-only review before freezing the observer | added at sign-off; only cases the code actually permits |

## Questions

1. **How often does each shortcut happen** in control worlds (per person-year)?
2. **How much behaviour rests on it:** what share of all water crossings are corner crossings (A1); what share of
   crossings are over the wrapping edge (A2); what share of food eaten from wild plants came from the dead (A3)?
3. **Which earlier findings could it touch?** For each shortcut that matters, a read-only list of the studies whose
   measures could include it (for example A1 and GF1's group fluidity, F1's partner supply, E-series contact between
   islands).

## Is it a flaw? (checked against the world's intended rules, before any measure is read)

| | intended? | source |
|---|---|---|
| A1 corner crossing | **no**: water is meant to stop anyone without something that floats | `world.walk` docstring; DESIGN.md (Rule 3) |
| A2 wrapping edge | **yes**: intended world physics | DESIGN.md: "The map wraps." |
| A3 food of the dead | **unclear**: DESIGN.md says food is "left on the ground where they died"; the code adds it to the tile's wild plants, above the tile's cap | DESIGN.md, "Things left on the ground"; `biology.py` |
| A5 knowing where loved ones are | **not stated**; N8 found no evidence that people track where acquaintances are | `mind._far_people`; N8 evidence |

A shortcut that matches an intended rule is reported as a property of ACL's world, not a flaw. Only an unintended
shortcut that is also material is put to the creator as a candidate for a fix.

## Reading rule (the threshold is an operational choice, labelled as such)

A shortcut is **material** if it accounts for at least **5%** of the behaviour it touches (crossings, food eaten, or
"go to" moves toward someone out of sight), in discovery **and** holdout. Every share is reported with its **absolute
counts** and a **95% interval** (percentile bootstrap over worlds, 10,000 resamples, `random.Random(2026)`). A share whose
interval reaches 5% but whose estimate is below it is reported as **borderline**, never dismissed as harmless. For A3,
also the share of all food eaten that came from the dead; for A5, the share of all "go to" moves aimed at an out-of-sight
loved one, and the distance walked toward them. A material shortcut is reported to the creator with the list of findings it could touch;
**fixing it is a separate decision**: a fix would be a **new version** of the world, compared against the original,
which is kept as the baseline; it would need its own sign-off and re-checks of the findings it touches. Nothing is fixed
because it looks unrealistic.

## Worlds (rule 15)

Discovery: F1's seeds 501–516; holdout: 601–616. 120 years, control code, a read-only observer verified by state hash.

## Decisions (taken by the creator at sign-off: 5% with counts and intervals; information audit added; intent check; no fix
without measure; after WS1, before ID1)

1. The **5%** threshold for "material" (or another figure).
2. Add any shortcut you have noticed yourself to the list before it is frozen.
3. Run after WS1 and ID1 (recommended), or before ID1.

## Assistant's prior (written before any run; not a prediction to test)

A1 (corner crossing) happens, perhaps often, because diagonal moves are common and many channels are narrow; A2 is rare
(the generator puts sea around the edges); A3 is small. Held loosely.

## Code review for A4 and A6 (read-only; written before the observer is written, as the frozen plan requires)

A full read of `mind.py` (where choices are made) found these further cases. Each is measured with the same rules as
the others (shares with absolute counts and 95% intervals; 5% material; borderline band), and each is classified against
the world's intended rules before being called a flaw.

| | what a person "knows" | where | measured as |
|---|---|---|---|
| **A6a** | the **exact food** a nearby person holds (`q.edible()`), when judging their hunger to give | `mind.decide`, give option | every gift decision uses it; reported: gifts per person-year and gifted food as a share of all food eaten |
| **A6b** | **exactly how much food** a nearby person carries (`q.food`), when deciding to steal | `mind.decide`, steal option | every theft decision uses it; reported: thefts per person-year and stolen food as a share of all food eaten |
| **A6c** | **eligible singles up to 2 tiles beyond sight**: partner search scans `perception + 2` tiles; sight is `perception` | `mind.decide`, partner search | share of partner-search "go to" moves aimed at someone beyond sight |
| **A6d** | **water up to 7 tiles away** when judging whether a place is dry (water within sight of the *place*, not of the person) | `mind.decide`, `dry_seen` | share of dryness judgements that rested on water beyond the person's own sight |

No case was found of a choice reading another person's habits or temperament, a tile's contents beyond sight other than
A6d, or the random stream's future. Movement, foraging and storage gave no further non-information shortcut beyond A1–A3
(A4: none added).
