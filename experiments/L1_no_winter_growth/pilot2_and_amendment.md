# L1 — Redesigned pilot (same-seed controls) and Amendment 1 (FROZEN)

**Status:** signed off by the creator and frozen, both parts together, as `L1-pilot2-frozen`, before the new pilot ran.
Written after the first pilot's stop (2 of 4 died out) and the declared post-pilot diagnostic (`pilot_diagnostic.md`). No
main-experiment data exists: seeds 601–616 have never been run. The creator approved eight seeds, the excess-extinction
limit, population beside every measure and the paired-world verdict, and changed one threshold (both arms alive in at
least five of eight seeds, not six).

## Why redesign

The first pilot changed the winter in four worlds without watching the same worlds unchanged, so it could not separate
L1's effect from seed fragility. The diagnostic showed both were present: one world (702) died in the unchanged world
too; one (704) died only under L1; every surviving L1 world ended much smaller (31 against 44; 32 against 94). The
question a pilot should answer is: **does L1 reduce survival relative to the world those exact seeds would otherwise
have had, by so much that the main experiment could not be read?**

## Part 1 — The redesigned pilot

- **Seeds:** eight new pilot seeds, **711–718**: none used before (not the first pilot's 701–704, which have now been
  seen; not the experiment's 601–616). Eight is enough for the pilot's binary question.
- **Arms:** both, on every seed: C (unchanged) and L (no winter growth). Same code, same people as the frozen design.
- **Read only:** population every ten years, and whether the world died out. Nothing else.
- **Stop rule, against the control (all must hold for the main experiment to run):**
  1. **Excess extinction:** worlds that die out under L, minus worlds that die out under C on the same seeds, is at most
     **one** of eight.
  2. **No collapse of the comparison:** in at least **five** of eight seeds, both arms are still alive at year 120, so
     that the main experiment would have enough worlds where both arms can be compared. (The creator: the pilot is to
     prevent an uninterpretable experiment, not one that reveals the world became harder.)
- **Shrinkage is not a stop reason.** Smaller populations under L are expected (the diagnostic) and are themselves a
  finding; Amendment 1 handles them in the main analysis.

## Part 2 — Amendment 1 to the frozen L1 pre-registration (the population confound)

The frozen design (`preregistration.md`) is unchanged except for these additions, made before any main data:

1. **Population reported beside every measure.** For each arm: population at each ten-year sample, final population,
   and worlds that died out, reported next to the manipulation check, the frozen test and the descriptive measures.
2. **The frozen test is computed on worlds where both arms are alive at year 120** (paired seeds), as well as pooled
   over all seeds; both are reported. **The frozen verdict uses the paired worlds**, because extinction would otherwise
   change the composition of the sample; pooled results are reported for completeness.
3. **Per-person and per-household forms only.** The three frozen criteria are already per household or per person
   (household stock ÷ need; share of carers stashing; share of weeks foraging), so they need no change; descriptive
   measures (food given, going short, deaths, seed sown) are reported per person or per adult-week, never as totals.
4. **A sentence added to the reading of any result (frozen):** "L1 worlds are smaller than control worlds. Smaller
   populations have fewer people to share with, learn from and sow beside; differences between the arms may come from
   the leaner winter directly, or through the smaller population it produces. L1 cannot separate the two."

## Order after sign-off

1. Freeze Part 1 and Part 2 together; tag `L1-pilot2-frozen`.
2. Run the redesigned pilot (both arms, seeds 711–718); report survival and population only.
3. If its stop rule passes: run the main experiment as frozen with Amendment 1. If it fails: L1 is too disruptive to be
   read as a test of delayed return; the design returns to the creator (L6 is the fallback named in the roadmap).
