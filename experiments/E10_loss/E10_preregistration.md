# E10 — The lesson of a lost child (O2) and of a death witnessed (O3): pre-registration (FROZEN)

**Status:** signed off by the creator on 2026-10-06, with one change (O3 tested at two witness strengths instead of
one, so its value is a dose-response test rather than a single guess), and frozen as `E10-frozen` before any E10 code
was written. Not to be edited after the results.

**Chosen by the creator (2026-10-06):** O2 first, then O2 + O3, from `../E9_anticipation/next_options.md`.

## 1. Why

E9.2: a carer's food at the start of winter cuts their children's starvation five-fold, so the reward for laying
food by falls on the children, not on the person who does the work. E9.1: one's own hunger teaches it only faintly.
O2 asks whether losing a child to a season teaches it strongly; O3 whether seeing someone starve teaches it to more
people.

## 2. Pilots (read-only, recorded before this design)

- **O2** (`../E9_anticipation/run_o2_pilot.py`): in four control worlds over 120 years, 81 children starved (57 in
  winter, 23 in spring), in the care of 54 carers; 42 of them were alive the next autumn and still caring for
  children. A strong lesson, about ten times per world per 120 years.
- **O3** (`run_o3_pilot.py`): each of the 195 starvation deaths was within sight (4 tiles) of a median of 10 adults;
  206 different adults witnessed one; 555 witness-autumns followed in which the witness was caring for children.

## 3. The mechanism, exactly

Built on the E7 code alone (not on E9's A2). A new expectation per season, `expect["loss@s"]`.

**(a) Learning, where a death from starvation happens (`biology.py`, beside the death):**
- **O2:** if the dead person was under 12, their carer (`caregiver`, else `mother`), if alive, gets
  `expect["loss@s"] = 1.0`, where s is the season of the death.
- **O3 (O2+O3 arms only):** every adult (16+) within sight (`cfg.perception`) of anyone who dies of starvation,
  other than an O2 carer, gets `expect["loss@s"] = max(expect["loss@s"], WITNESS)`.

**(b) Fading, every week, for everyone alive (`biology.py`):** every `loss@s` is multiplied by 0.985, the rate at
which grief already fades in the code. A loss in winter still weighs about 0.6 the next autumn and 0.27 the one after.

**(c) Feeling it a season early (`mind.py` and `thought.py`), exactly as in E9:**
```
ahead = WEIGHT * p.expect.get(f"loss@{(world.season + 1) % 4}", 0.0)
food_hunger = max(hunger, ahead)
```
`food_hunger` replaces `hunger` only in the utility of foraging, the utility of hunting, and the "hunger" thought's
pull. Stealing, taking, giving, play and everything else keep today's hunger.

## 4. Arms and numbers

| arm | mechanism | WEIGHT | WITNESS |
|---|---|---|---|
| 0 | E7 code (control) | – | – |
| O2 | (a) O2, (b), (c) | 1.0 | – |
| O2+O3-low | (a) O2 and O3, (b), (c) | 1.0 | 0.25 |
| O2+O3-high | (a) O2 and O3, (b), (c) | 1.0 | 0.50 |

Reasons, fixed now: **WEIGHT 1.0** because E9 showed the weaker dose (0.375) inert and the strength of this lesson
lies in the lesson itself. **WITNESS** has no precedent in the code for how much less a stranger's death weighs than
one's own child's, so it is not a single guess but a dose-response test, set by the creator: **0.25** (conservative,
unlikely to overpower O2) and **0.50** (half of a direct loss). **0.985 per week** is grief's own fading rate. No
other values will be tried in E10.

Seeds 301–304, 120 years, probed every 10 years and every autumn and winter.

## 5. Scripting review

| question | answer |
|---|---|
| Storing, putting, carriers, containers or heaps mentioned? | No. |
| Anything fires because it is autumn? | No. The same rule runs every season, one season ahead of a loss. A loss in spring is felt in winter. |
| A fact about winter the person has not lived or seen? | No. Only a death they suffered (O2) or saw (O3). |
| Inherited or told? | No. (Stories are O4, not part of E10.) |

**Planned after E10, whatever its result (creator's request):** a read-only autopsy of the 112 adult-autumns in
E9 A2-full that reached the carrying limit: the first naturally occurring winter planners in ACL.
| Changes how anything is valued? | No. |
| Could it make people steal? | No: stealing keeps today's hunger. |

## 6. Validity (kill criteria)

- The probe changes nothing (state hash, 20 years, both codes).
- **Zero-weight check:** the E10 code with WEIGHT = 0 reproduces Arm 0's population at every 10-year sample for
  120 years (seed 304).
- Arm 0 reproduces the saved runs; code unchanged during the runs; no crashes.
- **Leak test (hard fail):** adults who never lost a child to starvation and (in O2+O3) never witnessed a starvation
  death forage in autumn within ±10% of Arm 0's comparable adults, pooled. If not, E10 is declared failed.

## 7. Order of analysis (binding, as in E9)

Validity and the leak test first. Then the causal links: autumn foraging of lesson-holders; their food entering
winter; the share of child-winters whose carer holds 20+ food; carrying-limit hits; carriers made. Only then deaths:
children's winter starvation, all starvation, population.

## 8. Predictions

1. **The lesson moves the bereaved (O2).** In the first autumn after losing a child, bereaved carers forage in at least
   1.3× as many autumn weeks as bereaved carers in Arm 0, pooled over seeds.
2. **The witnessed lesson moves witnesses (O2+O3-high).** In the first autumn after witnessing a starvation death,
   witnesses caring for children forage in at least 1.2× as many autumn weeks as comparable witnesses in Arm 0,
   pooled.
3. **Dose response.** Witnesses' autumn foraging, relative to Arm 0, rises less in O2+O3-low than in O2+O3-high;
   and the share of child-winters whose carer holds 20+ food is lower in O2+O3-low than in O2+O3-high, pooled.
4. **Better-stocked carers (O2+O3-high).** The share of child-winters whose carer holds 20 or more food at the first
   week of winter is at least 5 percentage points higher than in Arm 0, pooled.
5. **Children saved (O2+O3-high).** Children's winter starvation per child-winter is at least 20% lower than in
   Arm 0, pooled.
6. **O2 alone is too rare to change the world.** In O2, children's winter starvation per child-winter is within ±20%
   of Arm 0's, pooled.
7. **No leak.** The leak test (section 6) passes in all three mechanism arms.

**What the result would decide:**
- 1 fails: even losing a child, felt a season early at full strength, does not move people; the anticipation route is
  closed in this form.
- 1 holds, 2 fails: own loss teaches, witnessing does not; next is whether stories (O4) can carry it.
- 2 holds, 3 fails: witnessing moves people, but not in proportion to its weight; read the two O3 arms with care.
- 1–3 hold, 4 fails: lessons spread and carers stock more, but it does not save children; measure where the food goes.
- 1–4 hold: the first lesson in ACL that spreads, prepares people for winter and saves lives, learned only from what
  people lived through or saw. Run the 300-year follow-up, with novelty and carrier predictions frozen first.
