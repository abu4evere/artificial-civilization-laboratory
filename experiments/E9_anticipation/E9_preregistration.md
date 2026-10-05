# E9 — Anticipation (A2): pre-registration (FROZEN)

**Status:** signed off by the creator on 2026-10-05 and frozen (tag `E9-frozen`) before any E9 code was written.
Not to be edited after the results. Only the three arms below will run; no other mechanism is part of E9.

**Chosen mechanism:** A2, seasonal anticipation of going short, chosen by the creator from `candidates.md`.

## 1. The pilot, and what it changed (read-only, recorded before this design)

`run_pilot.py` replayed the four control worlds (E7 code, seeds 301–304, 120 years) with a probe that changed
nothing and matched every saved run. It computed A2's expectation in the shadow, two ways.

- **Learned from hunger level** (`mind.hunger_of`, how few weeks of food a person holds): nearly everyone comes to
  expect winter hunger, but the expectation raises the pull to forage in about half of all weeks in every season
  (about 0.09 all year, 0.16 in autumn). "Hunger" here measures low stock, which everyone has all year, so this
  version is not seasonal. It is A1 under another name. **Rejected.**
- **Learned from going short** (the weeks a person is actually starving): the expectation forms for the people who
  really went short in winter (winter expectation over 0.1 for 38–70% of people; over 0.3 for 13–43%), and it raises
  the pull almost only in autumn (median raise 0.02–0.05), with about zero elsewhere. Seasonal and specific, but weak
  at the thirst mechanism's weight. **Adopted**, at two doses (section 3).

This is also the faithful copy of the precedent: thirst's expectation is learned from actually going short of water
(`p.thirst`), not from how much water a person holds.

## 2. The mechanism, exactly

Two additions to the E7 code, and nothing else.

**(a) Learning, in `biology.body_phase`, beside the thirst update, every week, for everyone but infants:**

```
s = world.season
short = 1.0 if p.starving else 0.0                 # this week, did they actually go short of food?
key = f"short@{s}"
p.expect[key] = round(p.expect.get(key, 0.0) + 0.1 * (short - p.expect.get(key, 0.0)), 3)
```

The rate 0.1 is the thirst mechanism's. A person who has never gone short in a season has expectation 0 for it.
Newborns start empty. Nothing is inherited, told or copied.

**(b) Feeling it a season early, in `mind.decide`, and only in the pull toward getting food:**

```
ahead = WEIGHT * p.expect.get(f"short@{(world.season + 1) % 4}", 0.0)
food_hunger = max(hunger, ahead)
```

`food_hunger` replaces `hunger` in exactly three places: the utility of foraging, the utility of hunting, and the
"hunger" thought's pull (`thought.candidates`, `1.1 * hunger`). Everywhere else (stealing, taking, giving, play,
curiosity, courting, exploring, putting things down, making) keeps today's `hunger`. The same rule applies in every
season, always to the next season; no season is treated specially.

## 3. Arms and doses

Seeds 301–304, 120 years, sampled every 10 years; the 300-year follow-up only for an arm that passes.

| arm | code | WEIGHT | why this number |
|---|---|---|---|
| 0 | E7 code (control) | none | |
| A2-low | E7 + (a) + (b) | 0.375 | the thirst mechanism's ratio of expected to felt hardship (0.3 / 0.8) |
| A2-full | E7 + (a) + (b) | 1.0 | expected shortage felt as strongly as present hunger, the most a season-ahead feeling can be without exceeding the real thing |

Both numbers are fixed here, with their reasons, before any result exists. No other value will be tried in E9.

## 4. Scripting review (step 4)

Checked against the rule in `candidates.md`:

| question | answer |
|---|---|
| Does anything mention storing, putting, carriers, containers or heaps? | No. |
| Does anything fire because it is autumn? | No. The same rule runs in every season, toward the next one. It acts in autumn only if the person went short in winter. |
| Does anyone learn a fact about winter they have not lived? | No. The expectation comes only from their own weeks of going short. |
| Is anything inherited, told or copied? | No. (Witnessing and stories are candidates A3 and A4, not part of E9.) |
| Does it change how anything is valued? | No. Item worth, beliefs and recipes are untouched. |
| Could it make people steal or hoard from others? | No. Stealing and taking keep today's hunger. |
| What does it give people that they lacked? | Only this: a season they have gone short in feels a little closer, one season early, in the pull to get food. |

**Known compromise, carried over, not added:** people in ACL already key beliefs to the season they are in
(`fiber@3`), and the material choices already look one season ahead. A2 uses that existing ability.

## 4a. Validity checks (kill criteria)

- The probe changes nothing (state hash with and without it, 20 years, both codes).
- **Zero-weight check:** the A2 code with WEIGHT = 0 reproduces Arm 0's population at every 10-year sample for
  120 years (seed 304). This proves the new code changes behaviour only through anticipation.
- Arm 0 reproduces the saved E7 runs; code fingerprints unchanged during the runs; no crashes.
- **Leak test (hard fail):** if prediction 6 fails, E9 is declared failed whatever its other results, because the
  mechanism would be acting on people who have nothing to anticipate.

## 5. Measures

- **Manipulation check:** adults who went short in the previous winter forage in a larger share of their autumn
  weeks than in Arm 0.
- **Preparation:** food in hand, seeds and stores at the first week of winter (as E8.4).
- **Survival:** winter starvation deaths; infant deaths; population at 60, 90, 120.
- **The chain:** share of adult-autumns reaching 80 food in hand (the carrying limit); carriers made per decade
  (things the historian would call a carrier); mean worth of carriers to those who know them; later-born adults'
  crafting skill; recipes held.
- **Cost:** plant food left on tiles at the end of autumn; starvation outside winter.
- **Leak test:** among adults with no recorded short week in any winter (expectation for winter exactly 0), autumn
  foraging share must not differ from Arm 0 beyond ordinary variation. By construction their decisions are
  unchanged; the test confirms it in the running code.

## 6. Predictions (to be frozen with this file)

1. **Manipulation check (A2-full).** In at least 3 of 4 seeds, adults who went short in the previous winter forage
   in at least 1.3× as many of their autumn weeks as comparable adults in Arm 0.
2. **Dose response.** The autumn foraging rise in A2-low is smaller than in A2-full, in at least 3 of 4 seeds.
3. **Preparation.** In A2-full, median food entering winter is at least twice Arm 0's, in at least 3 of 4 seeds.
4. **Survival.** In A2-full, winter starvation deaths over 120 years are at least 20% fewer than Arm 0's, pooled.
5. **The chain begins.** In A2-full, at least 1% of adult-autumns reach 80 food in hand (Arm 0: 0.0%), pooled.
6. **No leak.** In both arms, adults whose winter expectation is 0 show autumn foraging within ±10% of Arm 0's.

## 7. Order of analysis (binding, set by the creator)

Validity first. Then the causal links, in this order, before anything about survival is looked at:
autumn food held; food entering winter; carrying-limit hits; carrier making and carrier worth. Only then
deaths, infant deaths and population.

**What the result would decide:**
- 1 fails in A2-full: anticipating a lived hardship a season early does not change behaviour here, even at full
  strength. The capacity is not the bottleneck; look elsewhere (for example, why going short is so rare an
  experience for adults, or A3/A4).
- 1 holds, 3–4 fail: people forage more but it does not carry them through winter (eaten, given away, or rotted);
  measure where the food goes.
- 1, 3, 4 hold, 5 fails: preparation without needing tools; storage happens in hand and in heaps but never reaches
  the carrying limit, so carriers still do not matter.
- 1, 3, 4, 5 hold: the first link from a capacity to a reason for tools. Run the 300-year follow-up with novelty
  predictions.
