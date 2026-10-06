# U1 — Why is there no surplus to store? (E8.4 revisited) Questions (written before any data)

**Read-only. No new mechanic, no rule touched.** The creator's question after P1: not why people don't stash (S1 mapped
that), but why they don't generate enough surplus for stashing to matter at all. S1 found food above the stashing line
in only 13% of adult-weeks, 2.7% in autumn. E8.4 had found a median autumn surplus of 163 per adult on the land.

**Worlds:** E13R's control (Arm A), seeds 501–516, replayed with a read-only probe (state hash, 20 years; every replay
equal to the saved E13R run).

## From the code, before any data

- One week of foraging gathers `(12 + 14 × foraging skill) × stage factor × tool`, at most what the person's tile holds
  and what they can still carry (100 food and seed). An adult gathers 12 to 26 a week and eats 7.
- Wild plant food on a tile is capped at 64 (× fertility) and regrows 14 a week (× fertility × season: spring 1.3,
  summer 1.0, autumn 0.5, winter 0.15).
- So a winter's food for one adult (91) is about four to seven weeks of foraging; for a carer with two children (195),
  beyond what one person can carry.

## The questions

1. **How much food is there and never gathered?** In autumn: the plant food on land within reach of adults (tiles
   within three of any adult), per adult, at the start and end of autumn, and how much adults gathered.
2. **How do people spend autumn?** Adults' chosen actions by season.
3. **Do they reach the carrying limit?** Share of adult autumn-weeks holding 90% or more of what they can carry.
4. **Do they move too much?** Distance moved per week, by season; and food gathered per forage week, against the
   most the formula allows, by season (are tiles near people stripped?).
5. **Do they stop when fed?** The share of autumn weeks in which adults forage, by the food they hold (in weeks of
   their own and their dependents' need).
6. **How much surplus could there have been?** For every adult autumn-week spent not foraging: what one week of
   foraging would have gathered there, from the same formula, capped by the food on their tile and their room to carry.
   Summed per adult per autumn: an upper bound (it ignores that each week's gathering changes the next week's land and
   room, that others forage the same land, and rot).

## Reading rule

Descriptive; nothing scored. U1 changes nothing in any world.
