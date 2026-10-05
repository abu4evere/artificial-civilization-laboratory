# E7.7 — Exposure and reproduction audit · Predictions (FROZEN)

**Written:** 2026-10-04, before any E7.7 run. Not to be edited after the results.
**Type:** read-only. Replays of the eight E7 worlds (E7 code, seeds 301–308), first 300 years, each checked
against the saved E7 run's population at every 10-year sample.

**Question:** when a person carries, inherits, or lives beside a useful thing, how often do they go on to
learn how to make it, and how often do they actually make one?

## Known from the code before running (not predictions)

- A person can come to know how to make something in five ways: finding it in play; being taught; reading a
  mark; copying by watching; and (E7 only) having a fire harden clay they carry.
- Copying by watching happens in only two situations: seeing someone arrive on new land with a raft, and
  hunting alongside someone using a tool. Its chance is 4% × (0.5 + curiosity) each time, and only if the
  person watched knows the recipe.
- Inheriting or carrying a thing teaches nothing about how it was made.
- A deliberate make needs a known recipe; making in play is random.
- Each person remembers at most 12 recipes. A new one beyond that pushes out the least valued, ties broken by
  name. A new recipe is valued at 0, and composite things (tied from other things) have names starting with
  `(`, which sorts first, so among equally valued recipes a composite one is always the one dropped.
  (Found while testing this probe, before any E7.7 run.)

## Families of things

The historian's names by properties (blade, spear, club, carrier, wrap, boat), plus fired clay (a thing whose
name holds `clay` and the heated mark `^`) and watertight (tight ≥ 50 and contain ≥ 40). A thing can be in
more than one family.

## Measures, per family

- objects that ever existed; people who carried one, and how they got it (made it, inherited it, fire-hardened
  it, other);
- people who lived beside one (on the same tile as someone carrying it) without carrying one;
- of people exposed (carried or beside) before knowing any recipe of that family: how many later learned one
  (and how), how many later made one, how many never learned;
- of everyone who ever knew a recipe of the family: how many made one at least once;
- kept after making: of things made in play, how often the maker still knows how to make it at the end of
  that week, split by simple things and composite things;
- watching: how often someone watched a thing of the family being used, how often the person watched knew the
  recipe, and how many copies resulted.

## Predictions

1. **Exposure rarely leads to reproduction.** For every family except carrier and boat, fewer than 20% of
   people exposed without a recipe later make one themselves.
2. **Inheritance is a dead end.** Of people whose first contact with a family is inheriting a thing of it,
   fewer than 10% ever make one, pooled over families.
3. **Fired clay never spreads by contact.** Of people who lived beside fired clay without carrying it, under
   5% later know how to make it.
4. **Teaching does more than watching.** Pooled over families, more recipes are learned by being taught than by
   copying, by at least a factor of 5.
5. **Knowing is not making.** Pooled over families, at least 40% of people who ever knew a recipe never made
   that family of thing.

6. **Composite inventions are forgotten as they are made.** Of things made in play, composite things are kept
   (the maker still knows the recipe at the end of the week) less often than simple things, by at least 20
   percentage points, pooled over worlds.

## Kill criterion

The audit is invalid if any replay does not match its saved run, if the probe changes the world (state hash
with and without it, 20 years), or if code changes during the runs.
