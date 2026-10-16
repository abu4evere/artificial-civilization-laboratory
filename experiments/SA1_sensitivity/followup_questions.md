# SA1-F — The sensitive settings at proper power, and the evidence for sight and range (SIGNED OFF 14 October 2026; frozen as `SA1F-frozen`)

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

## Sign-off (14 October 2026)

The creator: "**SA1: run all seven settings on 256 seeds. For the sight and range evidence reviews, use comparable
ratios. Report the four sensitive settings and the three near-the-line settings separately.**" Order: third, after TC1
and the nature v2 comparison ("TC1 first, Nature v2 validation second, SA1 follow-up third"). Decision 1: **all seven
arms**. Decision 2: **after nature v2's comparison** (it runs on v1's control code, exactly as SA1; v2's sign-off does not
change it). Frozen as `SA1F-frozen` (16 October 2026), after NV2 and before any SA1-F code or data.

## Operational details (fixed at freezing, before any run)

- **Code:** SA1's, unchanged: the control code `code_e13r` (`anticipation_weight = 1.0`) for every arm but the sham, which
  runs in `code_p2` with `sham_draw = 1`. Observers: F1's probe and E8.2's probe. 20 founders, 40 × 40, 120 years.
- **Arms (9):** `c`; `perception_lo` (2), `perception_hi` (8), `reach_hi` (6), `mortality_hi` (3.0e-5) — **the four
  sensitive**; `forage_lo` (6.0), `conception_lo` (0.02), `reach_lo` (2) — **the three near the line**; `s` (sham). Values
  exactly SA1's. **Seeds 4301–4556.** 2,304 worlds; `run_sa1f.py` (SA1's functions, imported unchanged, with these seeds and
  the folder `output_f/`).
- **Hard stops:** SA1's zero check re-run into `output_f/` (observers leave the world unchanged; `code_p2` with every
  setting off equals the control code; seeds 501 and 601, 20 years). SA1's second check (the control re-run reproduces
  F1's saved populations) **cannot apply to new seeds** and is dropped; in its place, every world's code fingerprint must
  be unchanged and single per code copy (as SA1).
- **Primary, per arm against `c`, paired by seed:** exact two-sided sign test; effect = C's extinction share minus the
  arm's, 95% bootstrap interval (10,000 resamples, `random.Random(2026)`); **Holm over the seven**. The yardstick is SA1's,
  unchanged: **half of F2's effect on F1's seeds, 0.117** (F2 has not been run on the new seeds; the number is not
  re-estimated). Readings:
  - p < 0.05 and |effect| > 0.117: "**sensitive**";
  - p < 0.05 and |effect| ≤ 0.117: "**moves survival**";
  - p ≥ 0.05 and the interval inside ±0.117: "**no meaningful effect**" (robustness, new at this sample);
  - otherwise "**no sign at this sample**". A reading with p < 0.05 that does not survive Holm is marked.
- **Reported in two tables:** the four sensitive settings, then the three near the line (the creator's instruction).
- **Against SA1's baseline (64 worlds):** each arm's SA1 effect and interval beside the new one; "**agrees**" if SA1's
  point effect lies inside the new 95% interval, otherwise "**differs**". Reported for every arm, whatever it shows.
- **Sham:** must be quiet (p ≥ 0.05); if not, every reading carries the caveat.
- **Described (rule 18):** median population at year 119, births per woman-year, decisions blocked for want of a partner,
  tools' share of foraged food (SA1's table).
- **The analysis shows no outcome if the run is not valid** (lesson of ID1).
- **Part B (the evidence reviews)** is read-only and runs alongside, as ratios that need no tile size (the creator's
  instruction); written as `evidence_perception.md` and `evidence_reach.md`.
