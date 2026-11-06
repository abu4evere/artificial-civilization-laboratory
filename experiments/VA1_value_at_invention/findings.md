# VA1 findings: is a new invention valued before it is lost? (read-only on v13)

**Status: final.** The blind recompute (`recompute_va1.md`, 5 November 2026, 21:34) matches. GPT and Gemini ran
code; DeepSeek, with no code tool, wrote a script blind, and the assistant ran it. All three give the same numbers and
the same readings.

Every number is from `results.md` (analyse_va1.py, frozen before data, with amendment 1 made before data) on run
42141156581:
- 32 worlds of nature v13, seeds 23701–23732, 170 years;
- 1,194 world-new kinds first made in play in years 130–165, each followed 5 years in its inventor's weeks;
- zero checks All: PASS on the cloud (`zero_cloud.log`; `code_v13` fingerprint f8b793bf…);
- one world died out (seed 23703).

## The answer in one line
**Value is not the bottleneck.** New kinds are used, found useful, and kept in memory. What stops remaking is that
inventors almost never have the inputs in hand again.

## The frozen questions, answered
1. **Primary 1, used before lost: 0.824 [0.788, 0.858].** Most new kinds are used by their inventor before their
   recipe is gone. The frozen reading "unvalued at birth dominates" is **not shown**.
   - Within 5 years, 95.6% are used at all (1,141 of 1,194).
   - The median first use comes in the week of invention.
2. **Primary 2, counterfactual survival of the 12-recipe cap:** survival is already high. 87.1% [83.5%, 90.5%]
   still hold the recipe at the first week's end, because the cap was full at invention for only 155 of 1,194 kinds.
   - With the first use's felt value as the starting value, 99.8% would survive.
   - The v_sim row (1.000) carries no reading, by amendment 1.
3. **Primary 3, is similar experience informative? Yes, modestly.**
   - The correlation of v_sim with the first use's felt value is 0.297 [0.245, 0.350], on 1,135 kinds. Its interval
     lies wholly above 0.2.
   - It is above the plain mean's 0.267, so the reading is "similar experience is informative".
   - The margin over the plain mean is small (0.03). Most of the signal is the person, not the similarity.

**What follows, decided before data:** because "unvalued at birth" is not shown, **the next target is opportunity or
intention: getting the inputs again**.

## Described
- **Stages** (LD1's funnel; it repeats LD1 on new seeds):
  - 0, never held the recipe at a week's end: 0.129;
  - **1, held the recipe but never its inputs: 0.869**;
  - 2–5: about 0.001 each;
  - remade: 0.
- **First uses:** felt value above 0.05 in 903 of 1,141. v_first clears the make-offer threshold (0.05) for those 903;
  v_sim clears it for 533 of 1,188.
- **Losses:** the median week of loss is 0, but only 193 of 1,194 kinds were lost within the 5 years.

## Against the assistant's prior (questions.md)
| prior | result |
|---|---|
| 1. "unvalued at birth dominates" | **no:** 82% are used before loss, and 96% are used at all |
| 2. v_first keeps most used kinds; v_sim fewer | v_first 99.8%, but the actual survival is already 87% (the cap is rarely full) |
| 3. "similar experience is informative" about 50% | **yes, modestly** (0.297, and only 0.03 above the plain mean) |

## What it means (the assistant's reading, for the council)
- **The chain breaks at gathering.** On live v13:
  - new kinds are made, used, felt useful, and remembered;
  - but their inventors hardly ever gather what it would take to make them again.

  The four views from round 65 narrow to one: **opportunity or intention** (GPT's "an intention to reproduce a past
  success"; DeepSeek's "retrieval and targeting"). Not value, and not, in v13, the memory cap.
- **IQ1's link:** this is the gap that Sahih al-Bukhari 1 inspired as a candidate law in
  `docs/research/iq1_intention_foresight_2026-11-05.md`: an aim toward a state one's own experience valued, held across
  weeks and steering the steps toward it, here gathering its inputs.
- **Next:**
  - first check, in the code and read-only, why gathering is not offered for the inputs of a valued new kind. It may
    be a plain gap in which materials the gather option considers, and that would be a fault, not a missing law;
  - then the council on an intention law.

## Appended 5 November 2026, 21:36: what a full recipe memory does (described, from `va1_kinds.csv`; no reading)
DeepSeek's reasoning noticed that "held at the first week's end" is 0 almost exactly when the memory was full.
Checked on the CSV:
- **With room (1,039 kinds): all 1,039 were kept.**
- **With a full memory (155 kinds): 154 were gone by the first week's end.** All 155 were still used later (the made
  thing stays in hand after the recipe is gone), and 130 of their first uses felt above 0.05.
- **130 of the 155 were ties at value 0**, and 129 of those were lost. `knowhow.remember_recipe` drops
  `min(p.recipes, key=(value, name))`, so a tie is settled by the recipe's name in alphabetical order.
- **Made kinds are named `(a+b)#binder`, so a more nested (more complex) kind starts with more "(" and sorts first.**
  On a tie, the more complex kind is the one forgotten.

This is not a fault by the written rule ("the least valued is dropped", `docs/ODD_v11.md`): the rule says nothing about
ties. But it is an arbitrary tie-break that leans against complexity. It goes to the council as a candidate general
fix (for example, on a tie the longest-unused recipe is forgotten), never adopted without the safe path. It touches
about 11% of new kinds here (130 of 1,194).
