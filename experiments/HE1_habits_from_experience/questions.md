# HE1: Habits learn from experience — a law test in a copy (frozen plan)

**A nature-change test.**
- The candidate law uses an existing setting, so the test runs on `code_v13` with `discount` 0. No code copy is
  needed.
- Nothing goes live except by the safe path, in order:
  1. this frozen study, final and supporting the change;
  2. blind recomputes;
  3. a confirmatory run on new seeds;
  4. council on adoption;
  5. a new `code_v14` with zero checks;
  6. reference hashes and tests;
  7. a tag, a decisions line and a Telegram message.

**The candidate law: habits learn only from experienced outcomes.**
- Each habit value learns from the week's own learning signal, q ← q + 0.05 × (r − q), with no look-ahead to next
  week's best habit.
- Foresight is left to the systems that model the future: E9's anticipation of seasonal shortage, know-how beliefs
  and, later, the brain road's predictor.
- It is not a number chosen for an outcome. It separates the habit (model-free) system from foresight (model-based).
  Council round 64 (`docs/debate_round64_after_ld1_2026-11-05.md`) named this law, all three models alike.

**Why (all final, recomputed blind):**
- **PB3:** without the habit look-ahead, finished gather-then-make chains rise from 0.0035 to 0.0263, makes about 6.6
  times, world-new kinds about 9 times, and living-weeks are 1.166 [1.028, 1.321]. One extra extinct world, seed
  23311, also died out in the sham.
- **LD1:**
  - the look-ahead acts as a **familiarity bias**: it marks making down by 0.245 at offers, and values next week's
    best-fed situation least, because that situation is rarely visited;
  - the values are large (the habit term is 1.3 times all written pulls) but almost never clamped.

## Arms (32 new paired seeds **23501–23532**; LP: 80 founders, 80 × 80; 200 years)
| arm | settings |
|---|---|
| **c** | v13 |
| **h** | v13 with `discount` 0 (the law) |
| **x** | v13 with `sham_draw` 1 |

## Measures (adults 16–49 where stated; years 100–200, the later century; population beside every measure)
Pooled sums per world; a paired world bootstrap with 10,000 replicates and NumPy seed 20261117.

### 1. Primary: harm guards (h against c)
A guard is raised by:
- **population:** a living-weeks ratio below 0.90 with its upper bound below 1;
- **extinction:** 3+ extra extinct worlds. Each extinction is listed with the same seed's c and sham worlds;
- **hunger:** deaths from hunger per 1,000 living-years, ratio above 1.25 with its lower bound above 1;
- **health:** adults' mean health at year ends, a difference below −5 points with its upper bound below 0.

**"No harm"** if no guard is raised. A guard raised means "harm: investigate", and the law is not adopted.

### 2. Co-primary: the effect
- **M3** (AM1's ends-directed chains; adults): h − c with its interval wholly above 0.
- **Makes per adult-year:** a ratio h ÷ c with its lower bound above 1.

**"The law releases making"** if both hold.

### 3. The reading
The law is **"supported"** if there is no harm and it releases making. Only then does the confirmatory run follow.

### 4. Described
- living-weeks against the sham; the sham against v13;
- acts aimed at a person;
- world-new kinds;
- R (lineage remaking);
- food per adult;
- deaths by cause;
- M2 and M5;
- people born after year 100.

## Validity (hard stops)
- **Zero checks:**
  - the observers leave the world unchanged (c and h; 20 and 60 years);
  - h and the sham act;
  - with `discount` 0, every habit update equals q + 0.05 × (r − q), clamped. A unit check on 20 years, read-only.
- **All 3 × 32 worlds** are present under one `code_v13` fingerprint.
- **A smoke run** before the cloud.
- **A blind recompute** by GPT, Gemini and DeepSeek of the guards and the co-primary.

## Known limits
- The law is tested in v13 as it is. Other parts of nature were shaped while the look-ahead existed, so some settings
  may interact. This is reported, not tuned.
- Removing the look-ahead also removes its real one-week opportunity cost of making (PB3's P+). If people now make
  at a cost to food, the food and hunger guards will show it.

## The assistant's prior
1. **No harm:** living-weeks higher (about +15%), hunger deaths not higher.
2. **The law releases making:** M3 and makes clearly higher, as in PB3 and LD1.
3. **R stays near 0** (value at invention is the next step).

Overall "supported": about 75%.

## Sign-off (5 November 2026)
The assistant, under:
- the creator's 2 November permission to edit world rules (tests in a copy, the safe path);
- sleep-mode autonomy.

Council round 64: GPT 96% (the next audit), Gemini 95%, DeepSeek about 78%. All three name this law. The assistant
75% that HE1 is valid and supportive. Frozen as `HE1-frozen` before any code or data.
