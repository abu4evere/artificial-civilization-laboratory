# CA1 — The chain audit: findings

Frozen as `CA1-frozen` (signed off by the creator, all recommendations). Read-only: nature v2 (`code_v2` and its four
settings), unchanged; one observer, shown to leave the world unchanged. Discovery 6301–6316, holdout 6317–6332, 120
years; 4 long worlds 6401–6404, 300 years. Table: `results.md`, from `analyse_ca1.py`. **Valid:** zero check, all 36
worlds, one fingerprint.

## The chain (pass rate = share of the link before)

| link | discovery | holdout | long worlds (beside) |
|---|---|---|---|
| 1 invented (kinds of thing) | 6,263 | 5,746 | 1,655 |
| 2 useful (helps some job ≥ 5%) | 0.926 | 0.936 | 0.939 |
| **3 transmitted (anyone else learned it)** | **0.114** | **0.098** | **0.092** |
| 4 retained (outlived its first knower) | 0.880 | 0.902 | 0.923 |
| 5 built on (part of a better kind) | 0.812 | 0.824 | 0.817 |
| 6 retransmitted (that better kind passed on and outlived its maker) | 0.264 | 0.237 | 0.243 |

Population (rule 18): median living people per decade 24–42 (discovery) and 21–29 (holdout); the long worlds fell from
28 to 7 by year 120.

## The frozen reading

**The bottleneck is link 3, transmission**, the lowest pass rate in both sets (and in the long worlds): about **nine in
ten useful inventions are never learned by anyone but their inventor.** Once something is passed on, it mostly survives
its inventor (88–90%) and is mostly used as a part of something better (81–82%). The next weakest link is the same
step again, one level up: only a quarter of the better things are themselves passed on and outlive their maker.

## The assistant's prior, against the result

| prior (frozen) | result |
|---|---|
| bottleneck at link 5, built on | **wrong**: link 5 passes 81–82%; the bottleneck is link 3 |
| second guess: link 4, retained | **wrong**: link 4 passes 88–92% |

## Described (not part of the frozen reading)

- **How things are passed on:** first transmissions were by **teaching** in 806 of 889 (discovery) and 643 of 709
  (holdout); read from a mark 51 and 40; heated (worked out at a fire) 26 and 22; **copied by watching 6 and 4**. Watching
  almost never passes anything on, as E7.7 found.
- **Steps of cumulative culture do occur, in the measured sense:** 121 (discovery) and 90 (holdout) kinds reached link
  6. The longest chain of ever-better kinds in a world was 5–6 (median), at most 7; a recipe passed through at most 5
  generations of teaching.

## Caveats (what the measure counts, stated before reading meaning into it)

1. **"Built on" does not require a second person.** A kind counts as built on if *anyone* later made a better thing with
   it as a part, including its own inventor. The audit did not save who first made each kind, so it cannot say how many
   of the 81% are one person building on their own work. That matters for "cumulative" and is the first thing to check.
2. **"Better" compares the best use of each thing,** which may be a different use (a part best for cutting wood, a
   composite best for hunting).
3. **"Kinds" are fine-grained:** each recipe variant is its own kind (about 380 per world), including 478 and 384 that
   arose as changed copies. Counts are of variants, not of distinct ideas.
4. 466 and 367 kinds had no recorded properties and were counted as not shown useful (as fixed before data).
5. The audit locates where the chain breaks; it does not show why.

## What it suggests (for the creator; nothing changed)

The obstacle is not that people cannot improve things, nor that what is passed on is lost: it is that **almost nothing
is passed on in the first place**, and what is passed on goes nearly only by teaching. Two read-only checks would come
before any design:

- **Why teaching passes on so little:** what decides which recipe a teacher shows (`information.show_how`), how often a
  person who knows something useful meets anyone to teach, and whether the learner keeps it.
- **Caveat 1:** re-read the same worlds (exact replays) saving who first made each kind, to separate building on one's
  own work from building on someone else's.

Any change to nature that follows would be a Law 126 decision, one rule at a time, frozen.
