# C1 — Why couples drift apart: discovery findings (16 worlds, 40 years; holdout not yet run)

Read-only. Questions frozen as `C1-questions`. Generated tables: `results_discovery.md`. Valid: observer read-only
(seeds 501, 1101), all 16 replays reproduce F1's populations for years 10–40, code unchanged. **Population beside every
measure:** worlds of 3 to 64 people at year 40 (median about 27; table in `results_discovery.md`).

## First, a correction to F2 (found here, before any holdout data; rule 19)

F2's findings (point 4), the index, the roadmap and the book (Chapter 55) said that once couples were brought together,
the share of women's weeks with the partner out of reach "rose from 20% to 46%", and read this as couples drifting
apart more. **Those figures were shares of all woman-weeks, including women with no partner.** Re-expressed per couple
(`reconcile.py`, `reconcile.md`): partners were out of reach in **57.8%** of partnered, non-pregnant woman-weeks in the
control worlds (F1) and **65.1%** under perfect finding (F2). Most of F2's jump came from far more women having partners
(45% → 89% of woman-weeks), not from couples drifting further. **Couples in ACL were already apart about half the time
before F2.** The earlier statements stay as written, with this correction beside them.

## Answers (frozen questions; discovery only)

**Q1. How far, how long.** Couples were apart in **49.2%** of couple-weeks (105,892 couple-weeks; years 0–39). Of apart
weeks, **41.1% were at exactly 3 tiles** (the gap: too far to conceive, too near to feel any pull), 43.8% at 4–6, 15.1%
at 7 or more. Spells are short (median 2 weeks; 44% last one week); spells longer than 13 weeks are 2.4% of spells but
20.4% of apart weeks.

**Q2. Who moves away, doing what.** Both partners moved in 51% of splits (the man alone 27%, the woman alone 22%). The
moves that split couples were **foraging in 58.5%**, joining someone or somewhere else 18.5%, talking to or giving to
someone else 17.4%.

**Q3. Beyond reach.** In 75.2% of partner-weeks beyond 3 tiles, a "join" option was among the four top-scored; it was
**chosen in 16.3%**. **Foraging won 55.7%.** Affection for the partner was high (mean 0.77) and hunger moderate (0.40):
the pull is there, and food outbids it.

**Q4. Coming back.** Rejoins were made by "join" in 36.5% of moves, by **foraging in 29.8%** (chance: a forage move that
happened to land near the partner), and by giving or talking to someone 28.7%.

**Q5. Who is apart more.** Winter (57.0%) more than summer (43.4%); couples with low affection (83.1%) more than high
(46.1%), though most couple-weeks are high-affection; women with a child under 6 slightly less (48.3%) than without
(53.2%); years together make little difference (46.8–51.0%).

## Reading (discovery; to be checked on the holdout)

ACL's couples are apart because **nothing in nature keeps them together while they forage**. Each partner chooses their
own foraging tile; within 3 tiles there is no pull toward the partner at all, and conception stops beyond 2, so a
couple at 3 tiles (two in five apart weeks) is neither together nor drawn together. Beyond 3, the pull exists but loses
to food most weeks. Couples come back together as often by chance as by intent. Apart weeks are mostly short drifts,
with a long tail of long separations.

## Next, frozen order

Holdout seeds 1101–1116 (`run_c1.py holdout`, `analyse_c1.py holdout`). The reading is confirmed if, on the holdout:
couples are apart in at least 35% of couple-weeks; at least a quarter of apart weeks are at exactly 3 tiles; foraging is
the most common action in splits; and when beyond reach, "join" is among the top options at least half the time but
chosen in under a third. These thresholds are written now, before the holdout data.
