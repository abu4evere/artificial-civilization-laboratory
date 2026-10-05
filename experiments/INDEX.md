# Experiments — index

Every experiment in ACL, in order: the question, the answer, and where its record lives. Each one froze its
predictions before running; "scorecard" is predictions confirmed out of predictions made. The story of how they
connect is told in the book (`book/source/the_world_that_nobody_wrote.md`).

| # | Question | Answer | Scorecard | Record |
|---|---|---|---|---|
| E0 | Does the agent architecture produce non-trivial behaviour? | Predictions kept; no scored report survives. | – | `E0/` |
| E1 | Over 200 years, does culture appear without scripting? | Yes: symbols, myths, techniques passed across generations, fire. Trust follows food, not truth. Rafts invented in year 0 and almost never used. | 10 / 19 | `E1/report.md`, `E1/investigations.md` |
| E2 | Do four changes (reputation by record, more testing, records that teach, floating made felt) work? | Each works; population falls 40%. | 5 / 10 | `E2/results.md` |
| E3 | Why did births fall in E2? | Inconclusive with 8 worlds. | – | `E3_births/report.md` |
| E4 | Is E2's population drop real, and why? | Real (18 of 24 worlds): isolated founding bands die out. | 2 / 6 | `E4_replication/results.md` |
| E5 | What happens over 1,000 years? | Long traditions, one people per world, two peoples who never met (seed 301), and the freeze: no new kind of thing after year 11. | 6 / 7 | `E5_millennium/results.md` |
| E6 | Does richer matter (clay, heat, filling) unfreeze novelty? | No: bottleneck remains. One lump of clay fired in 8,000 world-years. | 2 / 6 | `E6_novelty/results.md` |
| E6.5 | Where does the chain of discovery break? | At interaction: Reibik held a watertight vessel at fresh water for 102 weeks and never filled it. | – | `E6_novelty/autopsy.md` |
| E6.6 | Can people learn from delayed rewards? | Yes, through things held and places; the first try is what never happens. | – | `E6_novelty/horizon.md` |
| E7 | If the world does the first step itself (rain fills, fire hardens), does novelty continue? | No: fire hardens clay 647 times, water almost never; bottleneck remains. | 3 / 7 | `E7_passive/results.md` |
| E7.5 | What was seed 301's year-115 novelty? | A duller flint flake made by unskilled people; the novelty measure counted a loss as new. | – | `E7_passive/autopsy_301.md` |
| E7.6 | Do expertise, recipes and making last? | They decay: best skill ~0.9 → ~0.08, deliberate making ÷40, recipes ÷4–8; vessels almost never exist. | 3 / 6 | `E7_6_expertise/results.md` |
| E7.7 | Does living with useful things lead to making them? | Teaching spreads recipes; watching almost never does; 78% who knew fired clay never made it; composite inventions forgotten 5× as often. | 1 / 6 | `E7_7_imitation/results.md` |
| E8 Arm 1 | Does freeing people to remake what they hold restore practice? | No evidence: making collapses as before. | 0 / 6 | `E8_crucible/results_arm1.md`, `amendment_1.md` |
| E8.1 | How do people value what they hold, by generation? | Making was never competitive, even for founders; by generation 3 it is weighed in 0.6% of possible weeks. | 4 / 5 | `E8_crucible/E8_1_results.md` |
| E8.2 | Do tools pay? | Barely: at most 2% of food foraged; most made things never repay their cost. | 3 / 4 | `E8_crucible/E8_2_results.md` |
| E8.3 | Who starves, when? | 88% in winter or early spring; nothing laid by; not one carried a container. | 3 / 4 | `E8_crucible/E8_3_results.md` |
| E8.4 | Could they have prepared for winter? | Yes: median autumn surplus 163; median adult enters winter with 13. | 5 / 5 | `E8_crucible/E8_4_results.md` |
| E9 | Does anticipating a season one has gone short in make people prepare? | Faintly: leak test passed, central test failed; for the first time some people fill their hands before winter, and those few store six times the food. | 2 / 6 | `E9_anticipation/results.md` |
| E9.1 | Whom does anticipation reach? | Nearly everyone, faintly; only those with a strong lesson store. | 1 / 3 | `E9_anticipation/E9_1_results.md` |
| E9.2 | Does a carer's store protect children through winter? | Yes: a few weeks' more food in the carer's hands cuts a child's winter starvation five-fold; such carers are rare (0.2%), and anticipation makes them nine times commoner. | 3 / 3 | `E9_anticipation/E9_2_results.md` |
| E10 | Does losing a child (O2) or witnessing a death (O3, at 0.25 and 0.50) teach preparation? | Bereaved forage 1.2× next autumn, witnesses barely; no change in how anyone enters winter. Differences in child deaths go in no consistent direction and nothing upstream explains them. | 2 / 7 | `E10_loss/results.md` |
| E9.3 | Who were the first winter planners, and what did they do? | Ordinary people with a hard lesson; they gave 30% away; no child in their care starved; 1 of 113 planned again. The lesson undoes itself. | 3 / 3 | `E9_anticipation/E9_3_results.md` |

## The chain so far

Winter is when people starve (E8.3), though autumn offers enough to see them through (E8.4). Nobody lays food by,
because nothing in them reaches beyond two weeks of hunger; a faithful copy of the thirst mechanism gives them a
season-ahead feeling, but a faint one (E9, E9.1). With no store to fill, a carrier's one real use is never lived
through, so tools seem worth almost nothing (E8.2), so nobody chooses to make them (E8.1), so skill and recipes decay
generation by generation (E7.6), and nothing new is built on what was found in the first decades (E5–E7).

## Method, in one paragraph

Predictions and a kill criterion are frozen in a file, committed and tagged before any code or run. Every probe is
proved read-only (the world's state hash is the same with and without it). Every replay is checked against the saved
run. Code is fingerprinted at the start and end of each run. Wrong predictions are kept as wrong. Designs are reviewed
against the code before running, and amended in the open, never silently.
