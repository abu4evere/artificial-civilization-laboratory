# SA1-F — The sensitive settings at proper power, and the evidence for sight and range (DRAFT for the creator's sign-off)

**The creator (14 October 2026):** "Run 256 seeds and review the evidence for sight and range. Record uncertainty and
compare results against the existing baseline." SA1's sign-off already allowed "a 256-seed follow-up only for settings
that turn out sensitive or near the line".

## Part A: the 256-seed runs

**Which arms** (from SA1's results, chosen by its own rule, not by preference):

| arm | SA1 (64 worlds) | why it is in |
|---|---|---|
| `perception` × 0.5 (2 tiles) | 49 died out (C 22); sensitive | sensitive |
| `perception` × 2 (8) | 8; sensitive | sensitive |
| `reach` × 2 (6) | 36; sensitive | sensitive |
| `mortality_base` × 2 | 34; sensitive | sensitive |
| `forage_base` × 0.5 (6) | 34; sensitive, not after Holm | near the line |
| `conception_chance` × 0.5 | 31; p = 0.078 | near the line |
| `reach` × 0.5 (2) | 31; p = 0.078 | near the line |

Plus the **control** and a **sham**: 9 arms × 256 = 2,304 worlds.

- **Seeds:** 256 **new** seeds (fixed now: 4301–4556), so the result is a replication on fresh worlds, not a re-read of SA1's.
- **Code, observers, thresholds and tests:** exactly SA1's (same scripts, same frozen reading: "sensitive" if p < 0.05
  and |effect| > half of F2's effect measured on these seeds; Holm over the seven; the sham must be quiet).
- **What it adds:** with 256 worlds the interval is about ±0.06, so a "no sign" can now be read as "no effect larger than
  half of F2's" (the first time robustness, not only sensitivity, can be shown).
- **Uncertainty recorded:** every arm's effect with its interval, beside SA1's on the 64 worlds; agreement or not between
  the two is reported for each arm.
- **Cost:** about 30 hours on four workers (worlds that die early are cheaper; `perception` × 0.5 mostly dies). **Decision 1:**
  all seven arms (recommended), or only the four sensitive ones (about 17 hours).

## Part B: the evidence reviews (read-only; rule 17)

1. **Sight (`perception`, 4 tiles).** The obstacle is known (N10): an ACL tile has **no measured size**, so "4 tiles" cannot
   be compared with any distance in metres. The review asks two things that do not need a tile size: (a) what share of a
   band's members a forager is typically within sight or earshot of during a day (camp layouts, daily foraging parties:
   Hadza, BaYaka, Agta GPS studies); (b) the ratio of what a person can see to how far they travel in a day, compared with
   ACL's 4 ÷ 3. If neither can be anchored, `perception` is recorded as **unanchorable without a tile scale**, and every
   finding keeps its caveat.
2. **Range (`reach`, 3 tiles a week of action).** The same obstacle; the review looks for the ratio of daily foraging
   radius to camp-move distance (Binford 1980; Kelly; Venkataraman et al. 2017), which ACL could match as a ratio.

Both reviews are written as evidence notes (sources labelled full text / abstract / record), checked by Claude; outside
sources (Perplexity, the council) only for leads.

## The assistant's prior (to be frozen)

`perception` both ways and `mortality_base` × 2 stay sensitive; `reach` × 2 stays sensitive but smaller; of the
near-the-line arms, `forage_base` × 0.5 becomes sensitive, the other two do not.

## Decisions for the creator

1. All seven arms (about 30 hours) or the four sensitive ones (about 17 hours).
2. Order: after TC1 and before nature v2's comparison (recommended: it is on v1, like SA1, so it should finish before
   studies move to v2), or later.
