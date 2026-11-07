# EG1 findings: when someone is starving, does the energy rule stand between them and food?

**Status: final.** The blind recompute (`recompute_eg1.md`, 7 November 2026, 13:54) matches. GPT and Gemini each used
code, and every point estimate and the reading agree. DeepSeek's points agree, but it had no code tool, so its
intervals are not counted.

Every number is from `results.md` (analyse_eg1.py, frozen before data) on cloud run 42396536712:
- 32 worlds, seeds 24701–24732, on `code_eg1` = `code_v15` + logging only; LP, 200 years, years 100–200 counted;
  people aged 6+;
- zero checks All: PASS (`zero_local.log`):
  - `code_eg1` with and without the log = `code_v15`;
  - the hook check matched the options offered in 122,823 person-weeks;
  - reload exact;
- in the study run, **the hook check matched in all 40,327,088 logged person-weeks (0 mismatches)**, and no world went
  extinct.

## The answer in one line
**The frozen reading: energy is a minor contributor.**
- **P = 0.0628 [0.0540, 0.0713].** In 37,276 of 593,814 starving person-weeks, food was there (food at the best forage
  tile, or prey), but no food option was offered because energy was below its cost.
- **Energy is not why most starving weeks stay hungry.** In 88% of them a food option was offered and taken. Hunger in
  ACL comes mostly from what a week of food-getting yields against need, not from the gate.
- The assistant's prior (P about 0.25, "binds" about 55%) was wrong.

## The starving weeks, split (593,814)
| part | share [95%] |
|---|---|
| a. a food option offered and chosen | 0.8794 [0.8676, 0.8912] |
| b. offered, something else chosen | 0.0578 [0.0525, 0.0644] |
| **c. blocked by energy alone** | **0.0628 [0.0540, 0.0713]** |
| d. no food feasible | 0.0001 [0.0000, 0.0001] |

**By age and sex** (the share blocked by energy alone):
| ages | women | men | starving weeks (women / men) |
|---|---|---|---|
| 6–11 | 0.000 | 0.003 | 858 / 969 |
| 12–15 | 0.050 | 0.049 | 22,856 / 23,472 |
| 16–29 | 0.076 | 0.056 | 101,367 / 96,570 |
| **30–49** | **0.119** | **0.054** | 106,476 / 115,378 |
| 50+ | 0.022 | 0.023 | 48,003 / 77,865 |

**Women aged 30–49 are blocked twice as often as men of their age.** This is the age of the most dependents, and PLAY1
saw a mother lose her forage option in the same way. Why it falls on women is not measured here.

## Where the gate does bite
- **The dying.** Of 1,519 starvation deaths at 6+, **532 (0.350 [0.302, 0.396]) had a blocked starving week among their
  last 4 decisions.** This is an association, not a cause: the dying are both hungry and tired.
- **Rest.** Of the grown's rest weeks (143,879), **0.328** came when food was blocked by energy alone; 0.672 were chosen
  with food on offer.
- **How long.** Runs of blocked starving weeks: 27,980 runs, mean 1.34 weeks, 0.277 lasting 2 weeks or more, the longest
  7. Mostly one week, as one rest week restores 52.5.
- **What they did instead** (37,276 weeks):
  - rest 0.655;
  - put 0.171;
  - join 0.088;
  - talk 0.029;
  - care 0.025;
  - the rest under 0.02 each.
- **Energy at decision:** a mean of 77.5 in starving weeks, against 86.4 in non-starving ones.
- **Non-starving weeks** are blocked far less: 0.0065 [0.0057, 0.0073] of 21,398,700.

## The best-tile quirk (found in council round 75)
`decide` weighs forage at the single best tile it looks at, chosen without regard to energy. If that tile is
unaffordable, forage is not offered at all.
- **Starving weeks:** in **0.429 [0.420, 0.437]** of the blocked ones, a tile looked at had food **and was affordable**
  (about 16,000 weeks). In 0.546, even one's own tile (cost 25) was unaffordable.
- **Non-starving weeks:** in 0.926 of the blocked ones, an affordable tile had food.

So **about four in ten blocked starving weeks are the quirk, not tiredness:** the person could have foraged nearer.
- Whether this is a fault is the council's question. The code has no comment saying the forage target must be the best
  tile regardless of cost.
- A general reading of the rule is "weigh what you can do", which would mean the best **affordable** tile.

## What it means
- **The weekly energy gate is not what keeps ACL hungry.** Most starving weeks are spent getting food. The thin margin
  play mode felt is in the yield of a week's food-getting against a family's need (FP1, HR1's question), not in
  fatigue.
- **Two narrow faults or laws remain, for the council:**
  1. **The best-tile quirk.** Weighing forage at the best affordable tile would give a food option in about 43% of the
     blocked starving weeks. It is a narrow change, a candidate for the fault-fix path with a harm check, if the council
     agrees that it is a fault.
  2. **The gap between prime-age women and men,** to be understood before anything changes: is it dependents' need,
     carrying, or the way food is shared?
- **Kraft et al. 2021** (`docs/research/forager_time_energy_2026-11-07.md`): foragers eat while foraging, and that funds
  further effort. The cases where ACL's gate bites (starving, low energy, offered only rest) are the ones this would
  touch. EG1 shows they are 6% of starving weeks, but sit before a third of starvation deaths.
