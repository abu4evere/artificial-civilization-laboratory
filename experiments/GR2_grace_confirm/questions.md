# GR2 — Does first-season grace hold up on new worlds, and is it safe for population? (SIGNED OFF 22 October 2026; frozen as `GR2-frozen` before any data)

**Why.** GR1 (frozen as G1) met its frozen adoption rule narrowly: passing on +0.0043 [−0.0000, +0.0085],
p = 0.037; survival no different. Population ran lower with grace (exploratory: lower in 107 seeds, higher in 80,
p = 0.057). GPT advised confirming before adoption, with population as a frozen safety check
(`../G1_first_season_grace/gpt_review_gr1_results.md`). The creator chose this (option a: 512 worlds pairs, 5% margin).

## Design

- **Code and runner:** GR1's, unchanged (`code_g1`, `run_g1.py`). Arms C (v3) and G (`first_season_grace` 1).
- **Seeds: 512 new, 10001–10512**; 20 founders, 120 years; 1,024 worlds on GitHub.
- **Power (estimated before freezing, from GR1's paired differences, sd 0.0347):** about 80% to detect +0.0043 at
  p < 0.05 with 512 pairs.
- **Zero checks:** GR1's, rerun here (hard stop).
- **Manipulation check (hard stop):** as GR1.
- **Primary (transmission):** as GR1: link 3, G − C paired; Wilcoxon; mean difference with a 95% bootstrap interval
  (10,000, random.Random(2026)). "changes transmission" (p < 0.05), "no meaningful effect" (interval inside ±0.02),
  otherwise "not shown".
- **Population safety (new, frozen):** each world's **time-averaged population**, the mean of its 12 ten-yearly
  counts (end of years 10, 20, … 120; 0 after dying out). Relative difference R = (mean over seeds of G) / (mean over
  seeds of C) − 1, with a 95% bootstrap interval over paired seeds (resampling seeds, 10,000, random.Random(2026)).
  **Safe** if the interval's lower bound is above −0.05 (the creator's margin: no more than 5% lower). **Harmful** if
  the upper bound is below −0.05. Otherwise **inconclusive**.
- **Survival check:** as GR1 (sign test, bootstrap, yardstick ±0.117).
- **Described:** population at years 60 and 120; GR1's pathway, cost and other described measures.

## The adoption rule (fixed now, before any data)

First-season grace is **adopted into nature (v4)** only if all hold:
1. The manipulation check passes.
2. Transmission reads "changes transmission" with G higher.
3. Population safety reads **safe**.
4. Survival is not worse ("no meaningful effect", or fewer worlds dying out).

If transmission holds but population is inconclusive, grace **stays experimental** (not in nature). Otherwise it is
not adopted. (The creator's acceptance of the evidence is given now, by approving this rule.)

## The assistant's prior

- Transmission: a small rise again, about +0.4 points; p < 0.05 (about 80% likely by the power estimate).
- Population: lower by about 3–5%, so **inconclusive** is the most likely reading.

## Sign-off (22 October 2026)

The creator: "go with a, run both on github". So: GPT's design, 512 new seed pairs, the 5% margin, the rule above.
GPT's advice was recorded before this plan (`../G1_first_season_grace/gpt_review_gr1_results.md`).
