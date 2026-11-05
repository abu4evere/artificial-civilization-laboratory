# LD1 findings: why the habit look-ahead locks choices, and where remaking fails (read-only on v13)

**Status: final.** Blind recompute by GPT and Gemini (fresh chats, with code) matches every number and all readings (`recompute_ld1.md`); DeepSeek's reply is appended there when it ends.

Every number is from `results.md` (analyse_ld1.py, frozen before data, with amendment 1 made before data) on run
42068513736:
- 64 worlds: v13 and v13 with discount 0 (c0), 32 paired seeds 23401–23432, 170 years;
- adults aged 16–49 in years 130–170;
- zero checks All: PASS (local record, accepted by the cloud; `code_v13` fingerprint f8b793bf…);
- population: v13 8,889,569 living-weeks and c0 10,000,198. Extinct worlds: v13 1 (seed 23423, year 73); c0 2
  (23423 in year 130, 23416 in year 145).

## The answers in two lines
1. **The look-ahead locks choices mainly by direction.** At the moments when making is possible, it scores making
   about 0.24 below the average option. Removing the look-ahead's differences between actions recovers about three
   quarters of the no-look-ahead make share, within single choices. The habit values are also oversized: about 1.3
   times all the written pulls together, against 0.23 without the look-ahead.
2. **New kinds are lost before any chance to remake them.**
   - In v13, 88% of new kinds stop at "held the recipe, but never with its inputs in hand".
   - Without the look-ahead, people invent 11 times as many kinds, and 64% are forgotten by the end of the very first
     week (the 12-recipe cap).
   - In both, almost no kind ever reaches a moment of being free, valuing it, and having the inputs.

## Part A, primary: "direction (the scale version also recovers)"
Expected make share of adult decisions (softmax probabilities of all scored options):
- v13 actual 0.0011;
- v13 with the habit term shrunk to the no-look-ahead scale ("scale") 0.0074;
- v13 with the look-ahead's differences removed ("none") 0.0064;
- c0 actual 0.0080.

Recovery of c0's make share, f = (version − actual) ÷ (c0 − actual):
- **none: 0.770 [0.706, 0.836]**, so the reading is "direction" (f_none ≥ 0.5);
- scale: 0.912 [0.842, 0.987]. The scale version also recovers, as reported under the amended rule.

**Described:**
- **The direction is measured directly.** At decisions where a make option is offered, the look-ahead part of the
  habit term for making is **−0.245** against the mean of the options; the part learned from r is −0.107.
  - The look-ahead term at learning, 0.8 × max next q, is lowest after make (+0.876), play (+0.870), explore
    (+0.808) and hunt (+0.814).
  - It is highest after talk (+1.038), give (+1.037), care (+1.001) and forage (+0.991).
- **Being well fed next week is valued least:** +0.262 for the next week's top food band, against +0.93 to +1.04 for
  the others.
  - Few weeks are spent there (30,529 updates of 4.66 million), so its habit values stay near their start.
  - The max over a little-visited situation is small, so the look-ahead favours acts that lead back to familiar
    situations, not to better-fed ones.
  - This is a plausible part of the mechanism, not tested as such here.
- **Scale:**
  - mean |q| 0.098 in v13 against 0.018 in c0;
  - the habit term against the rest of the score, 1.30 against 0.23;
  - the top option changes without the habit term in 16.1% of decisions in v13 and 6.6% in c0;
  - **saturation is rare:** 0.06% of q entries at the clamp. The clamp is not the mechanism.
- The shadow tables are exact on clean entries: 0 wrong of 943,417 (v13) and of 1,102,705 (c0). The approximation gap
  over all entries is mean 0.019 (v13).
- Other shares under "none" against actual: forage 0.354 vs 0.402; person-aimed acts 0.155 vs 0.193; play 0.0067 vs
  0.0011.

## Part B, primary: where remaking fails
Stage reached, as a share of kinds:

| stage | v13 (1,039 kinds) | c0 (11,357 kinds) |
|---|---|---|
| 0. never held the recipe at a week's end | 0.116 [0.074, 0.169] | **0.642** [0.613, 0.667] |
| 1. held the recipe, never with its inputs | **0.882** [0.830, 0.923] | 0.357 [0.332, 0.386] |
| 2. held both, never while free and valuing it | 0.000 | 0.000 [0.000, 0.001] |
| 3. free and valuing it, never offered | 0.002 [0.000, 0.007] | 0.000 [0.000, 0.001] |
| 4. offered, never chosen | 0.000 | 0.000 |
| 5. remade | 0.000 | 0.000 [0.000, 0.001] |

**Frozen readings and their pre-decided first R targets:**
- **v13: stage 1.** The first R target is opportunity, or an intention to gather for a past success.
- **c0: stage 0.** The first R target is recipe memory (rules review R1).

**Described:**
- the recipe was gone by the first week's end in 121 of 1,039 kinds (v13) and 7,291 of 11,357 (c0);
- the median number of weeks until lost is 0 in both;
- loss through the inventor's death is rare (16 and 107);
- **almost nobody else ever learns a new kind:** 20 of 1,039 (v13) and 161 of 11,357 (c0).

## Against the assistant's prior (questions.md)
| prior | result |
|---|---|
| 1. saturation common in v13 (a third or more at the clamp) | **no: 0.06%.** The values are large, but not clamped |
| 2. reading "both", scale stronger | **"direction (scale also recovers)"**. Scale recovers more (0.91 vs 0.77), as expected |
| 3. stage 0 or 1 dominates; stage 0 in v13, 1 or 2 in c0 | stage 0 or 1, yes, **but the other way round**: stage 1 in v13, stage 0 in c0 |

## What it means (the assistant's reading, for the council)
- **The look-ahead's bias is a familiarity bias, not "foresight".**
  - Next week's value is the best habit value of the situation people will be in. Habit values grow only where people
    have often been.
  - So acts leading to common situations (foraging, company) gain, while making, playing and exploring lose.
  - Even being well fed next week is valued least, because people are rarely well fed.
  - This looks less like a deliberate rule and more like a side-effect of a bootstrapped value on a coarse, sparsely
    learned table. That makes it a candidate for a **general law fix** (for example, a situation's value counted only
    as far as it has been learned), not for tuning the discount.
- **Two R bottlenecks, one in each world:**
  - in live v13, inventors almost never again hold their kind's inputs together: opportunity or intention;
  - when people make more (c0), the 12-recipe memory forgets new kinds at once.

  Fixing one alone will likely expose the other. Both point at the same gap: nothing keeps a new kind in mind, and
  nothing makes people gather for it.
- **No change to nature follows from a read-only study.** The next step goes to the council.
