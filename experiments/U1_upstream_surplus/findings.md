# U1 — Why is there no surplus to store? (E8.4 revisited): findings

Read-only replays of E13R's control (Arm A), seeds 501–516; probe read-only (state hash, 20 years); all 16 replays
equal to the saved runs. Questions in `questions.md` (food bands taken at decision time, fixed before any data after a
smoke test); tables in `findings_tables.md`. Descriptive.

1. **The food is there.** Plant food on land within reach of adults: a median 281 per adult at the start of autumn,
   and still 266 at its end. Adults gathered a median 104 each over autumn. The land is barely touched.
2. **Autumn is spent like any season.** Adults forage in 43% of autumn weeks, the same as every season (spring 46%,
   winter 43%). The rest of autumn goes to talking, joining and giving (34%) and gathering materials (13%).
3. **Not the carrying limit.** Adults held 90% or more of what they can carry in 0.09% of autumn weeks.
4. **Not too much moving, not stripped land.** About 1.2 tiles moved a week in autumn; a forage week yields 77% of the
   most the formula allows, as in spring and summer.
5. **They stop when fed, at two weeks.** The share of autumn weeks spent foraging, by food held when choosing (weeks of
   their own and their dependents' need): under half a week 86%; half to one 80%; one to two 40%; **two to four 6%**.
6. **There could have been a surplus.** Foraging in the autumn weeks they did not forage would have gathered up to a
   median 84 more per adult (an upper bound: it ignores depletion, others on the same land, and rot). With it, 99% of
   adult-autumns would have reached an adult's winter (91) and 53% a carer-with-two-children's (195); but a person can
   carry 100, so beyond that it would have to be stashed.

## Why they stop: read from the code

Hunger is `1 − weeks of food ÷ 2` (counting dependents' need and the person's own nearby stashes): it reaches zero at
exactly two weeks of food. The pull to forage is `0.25 + 1.6 × hunger` (× how much the land offers), so at two weeks it
falls from its full strength to its floor, and talking, joining and giving outscore it. The stash becomes possible at
exactly the same line: food above two weeks' need. **People stop gathering at the very point where storing could begin.**

E9's anticipation (A2) works by raising this hunger a season early for those who have gone short; that is why the
planners it produced gathered past the line.

## Reading

The problem starts upstream, as the creator suspected, and it is not the land, the time, the carrying limit or moving
about. It is when people stop: a person in ACL feels no hunger at two weeks of food, so gathering stops there, so
almost no one ever holds the surplus that stashing needs. The surplus E8.4 found on the land is real, and it stays on
the land.
