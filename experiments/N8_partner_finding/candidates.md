# N8 — Finding partners: candidate designs

**Asked by the creator (October 2026), after MC1.** Candidates only: **no code, no experiment, no choice.** Next, for
whichever candidates the creator picks: evidence review (rule 17), feasibility (rule 12), design for sign-off.

## What constrains the candidates (the record)

| study | what it established |
|---|---|
| F1 | a third of control worlds die out; pairing happens mostly among the founders; single women in small worlds almost never have an eligible man within sight (98%), though one usually exists elsewhere |
| F2 | perfect partner finding (a diagnostic, not a mechanism) cut extinction from 22 to 7 of 64: **finding partners is the main lever**; the smallest worlds still ran out of eligible partners |
| N5 | real foragers find spouses in networks of hundreds, outside the local group; adults know hundreds of people in a lifetime (Hill et al. 2014); random movement fails to keep contact at low density (Pearce 2014); in small groups the rarer sex disperses outward to find partners (Kramer et al. 2017); most marriages are arranged by kin (culture) |
| C1, MC1 | couples' proximity limits births, not survival |
| T1, HB1, MC1 | a slight change flips 18–20 of 64 worlds by chance; 64 worlds detect only large effects |

**The code today** (`mind.py`): a single adult courts only someone within sight (4 tiles), walks toward an eligible
single within 6, or otherwise takes a random exploratory step. People **remember others** (affection, trust,
familiarity, when they last met) **but not where** they saw them.

**Lessons the design must respect:** nature, not culture (no arranged marriage, no gatherings, no rule about which sex
moves); no tuning toward survival (a wider radius chosen until worlds live would be tuning); a sham arm, a paired test,
the hunger ledger; and **enough worlds to see the effect** (below).

## The candidates

| | candidate | what changes | nature? | anchor (to be checked) | main risk |
|---|---|---|---|---|---|
| **P0** | keep as is | nothing | – | F1 | baseline stays fragile |
| **P1** | **seek the people you know** | people remember where they last saw each person they know; a single adult with no eligible partner in sight walks toward where they last saw an eligible single they know, instead of a random step | nature: memory of people and places | Hill et al. 2014 (hundreds of people known); Pearce 2014 (random movement fails); F2 (the lever) | needs a new memory (where someone was seen), which must be bounded like ACL's other memories; people move, so the memory goes stale |
| **P2** | **leave when there is no one** | a single adult whose own group holds no eligible partner (none within sight for some weeks) travels outward, away from where they have been, until they meet others | nature: a drive acting on local scarcity | Kramer et al. 2017 (dispersal outside the group when partners are scarce); Hill et al. 2011 (either sex may disperse) | "some weeks" is a number to anchor, not tune; leaving costs food and safety |
| **P3** | **see or search further** | a larger perception or joining radius for mate search | doubtful | none: ACL has no scale, so any radius would be chosen | **tuning** (rule 17): listed only to be rejected |
| **P4** | **hear of eligible people** | stories carry who is unpartnered and where | borderline | stories already exist in ACL; no evidence read on this | risks writing a cultural practice (matchmaking talk) |
| **P5** | **more founders** (N5's M1) | a larger founding population | world setting | White 2017 (viable ~75–150) | changes every baseline; does not address search |
| — | arranged marriage, aggregation, bride exchange, "the woman/man moves" | — | **culture: not to be written** | Walker et al. 2011, Pearce 2014 (to watch for) | — |

## How the candidates differ

- **P1** is the closest realistic counterpart to F2's diagnostic: F2 let everyone find any eligible partner at once; P1
  lets people find only those they have met, at the place they last saw them, at walking pace. It adds one bounded
  memory and changes where singles go when no one is in sight.
- **P2** answers a different failure: the one the smallest worlds had in F2, when no eligible partner existed anywhere
  near. It moves people toward unknown others rather than known ones.
- **P1 and P2 could be tested separately, then together** (as T1 → HB1 → MC1), so each one's effect is measured.
- **P3** is tuning; **P4** is borderline culture; **P5** is a different question (size).

## Power: how many worlds (a lesson from T1, HB1, MC1)

F2's upper bound saved 17 of 22 dying worlds; a realistic mechanism will save fewer. With 64 worlds, chance alone flips
18–20 worlds' fates (shams), and only effects of roughly ten or more net worlds reach p < 0.05. **Before freezing any
design, the number of worlds should be set from the sham data already in hand**, so that an effect of, say, half of F2's
would be detectable. If that needs more worlds than F1's 64, new seeds (with their own control runs) are added.

## Assistant's view (the creator decides)

Take **P1** to evidence first (memory of known people and where they are; how foragers locate known people across a
landscape), then **P2** (when and how far the unpartnered disperse). Record P3–P5. And before any design is frozen, a
**power calculation** from the existing sham runs, to choose how many worlds the experiment needs.
