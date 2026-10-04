# E5 — A thousand years · Predictions (FROZEN)

**Question:** Can this world produce distinct peoples and cultures that survive for centuries?

**Design:** 8 new seeds (301–308), never run before, 1000 years each, under the current code (world 0.3,
agent 0.3), with every feature frozen. Observers: historian, Lab, and a read-only Divergence recorder that, every
10 years, measures each populated island (5+ people):
- **genes:** trait means, spread within the island, and the share of variation lying between islands;
- **culture:** techniques held, practices believed, what marks are read as, shared remembered events, habits;
- **identity:** trust and affection toward people of one's own island against people of other islands.

Snapshots every 100 years.

**Written:** 2026-10-02, before any E5 run. Not to be edited after results.

## Definitions (fixed in advance)

- **A distinct people:** two populated islands at the same moment whose trait means differ by more than the typical
  spread of that trait within an island, for at least 3 of the 8 traits, sustained for at least 100 years.
- **A distinct culture:** two populated islands whose techniques, practices or mark readings overlap by less than
  half (Jaccard distance > 0.5), sustained for at least 100 years.
- **A surviving tradition:** a technique, practice belief or mark reading held by 3+ people continuously for 300+
  years, outliving everyone alive when it began.
- **Rival identity:** trust toward people of other islands lower than toward people of one's own island by 0.2 or
  more, sustained for 100 years.

## Predictions

The creator's: most worlds become one mixed population or die; the experiment may well confirm the bottleneck.

Claude's:
1. At least 3 of the 8 worlds die out within 1000 years.
2. Of the worlds that survive, most hold one population for most of the time; two or more populated islands at
   once for less than 25% of the time.
3. **No distinct people** (as defined) appears in any world. Island trait gaps stay at or below the founders'
   (about 0.12).
4. Within-island trait spread stays at the inheritance floor (about 0.10-0.11 standard deviation).
5. At least one **distinct culture** appears for 100+ years in at least one world: culture diverges faster than
   genes.
6. At least one **surviving tradition** (300+ years) appears in at least half the surviving worlds. The likely
   candidates are simple techniques (the basket, striking stone on stone) and building beliefs.
7. **No rival identity** appears: trust between islands is set by gifts and contact, not by origin.

## Kill criterion (the experiment is invalid if…)

- any run crashes, or the code is changed during the experiment;
- fewer than 6 worlds complete (by reaching year 1000 or dying out).
