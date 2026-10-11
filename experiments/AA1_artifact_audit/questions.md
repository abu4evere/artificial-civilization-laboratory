# AA1 — Do ACL's people exploit flaws in the simulation? (questions, DRAFT for the creator's sign-off; nothing run)

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

## Questions

1. **How often does each shortcut happen** in control worlds (per person-year)?
2. **How much behaviour rests on it:** what share of all water crossings are corner crossings (A1); what share of
   crossings are over the wrapping edge (A2); what share of food eaten from wild plants came from the dead (A3)?
3. **Which earlier findings could it touch?** For each shortcut that matters, a read-only list of the studies whose
   measures could include it (for example A1 and GF1's group fluidity, F1's partner supply, E-series contact between
   islands).

## Reading rule (draft; the threshold is an operational choice, labelled as such)

A shortcut is **material** if it accounts for at least **5%** of the behaviour it touches (crossings, or food eaten),
in discovery **and** holdout. A material shortcut is reported to the creator with the list of findings it could touch;
**fixing it is a separate decision** (a fix changes ACL's world and every baseline, so it would need its own sign-off and
re-checks of the findings it touches).

## Worlds (rule 15)

Discovery: F1's seeds 501–516; holdout: 601–616. 120 years, control code, a read-only observer verified by state hash.

## Decisions for the creator

1. The **5%** threshold for "material" (or another figure).
2. Add any shortcut you have noticed yourself to the list before it is frozen.
3. Run after WS1 and ID1 (recommended), or before ID1.

## Assistant's prior (written before any run; not a prediction to test)

A1 (corner crossing) happens, perhaps often, because diagonal moves are common and many channels are narrow; A2 is rare
(the generator puts sea around the edges); A3 is small. Held loosely.
