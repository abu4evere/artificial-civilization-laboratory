# PB1 draft: a "shadow brain" — can a small predictor learn what ACL's actions do? (4 November 2026; the brain road, step 2)

**What this is:** a draft for council round 59, before a frozen plan. Nothing is frozen or built.
- **The basis:**
  - PB0 (final: GO);
  - round 58 (`docs/debate_round58_brain_design_2026-11-04.md`): the predictor first, tested on its own before it
    steers anything (GPT); vector outputs, never one "goodness" number (DeepSeek); a read-only "shadow" (Gemini, round
    56).

## The question
Can a small predictor, learning **only from what a person lives through and sees**, learn what the person's actions do
to their world? Can it do so better than a habit-table-like baseline, and also in **situations it has never met**?

## Read-only: it steers nothing
The predictors live beside v13's people (`code_v13`), in the observer. They read each week's state before and after,
and they never touch the world. Because they steer nothing, **several variants can learn in the same worlds at the
same time**: a paired comparison at no extra cost.

## What a predictor sees (inputs, all perceived now; no names, no outcomes, no recipes)
- **Body:** food in weeks of need (edible ÷ need), health, energy, thirst, age band, sex.
- **Season.** Whether anyone is in reach, and how many.
- **The tile:** plants, water within sight, fire, and how much of each raw material lies there.
- **Held things:** the best edge, reach, hardness and containment among things in hand (0–1 properties), and how many
  things are held.
- **The action taken that week** (one of the 19 kinds, as a one-hot code).

## What it predicts (outputs: a vector of observable changes over that week)
Change in edible food; in health; in energy; in raw materials held; in things held; distance moved; whether a new kind
of thing was made; the change in summed affection towards others.

**Never one combined "goodness" score.** Mood and reward are not predicted, so no value is built in.

## Variants (all learning at once, each person their own copy of weights; nothing inherited)
| variant | form | data |
|---|---|---|
| **B (baseline)** | a table: the running mean change for (situation index, action), as the habit table indexes | own weeks |
| **L-own** | linear | own weeks |
| **L-obs** | linear | own weeks + the weeks of people in sight (their state, action and change), each counted as one example |
| **N-own** | one hidden layer (16 units) | own weeks |
| **N-obs** | one hidden layer (16 units) | own + observed |

All learn online with one update per example (learning rates fixed in the plan, never tuned on data).

## Measures (prequential: each week is predicted **before** it is learned from)
- **Skill against the baseline:** 1 − (squared error of the variant ÷ squared error of B). Outputs are standardised
  first (by v13's own spread), and errors are summed over outputs.
- **Primary: skill on unfamiliar cases.** These are weeks whose (situation index, action) the person has never lived
  before; there B falls back to the person's overall mean. They are the generalisation test.
- **Secondary:**
  - skill on all weeks;
  - skill when the held things include a property level the person never held before;
  - how fast skill grows with the weeks lived (the data question: about 2,000 choices).

## Reading (to be frozen; numbers for the council)
- **The predictor road holds** if the best variant's skill on unfamiliar cases has a world-bootstrap 95% interval
  wholly above 0.
- **Which form and data** go into PB2: the best variant. A network is used only if it beats linear (DeepSeek: "nonlinearity
  only if it underfits").
- **If no variant beats B on unfamiliar cases:** the inputs or the learning are the problem, and the brain road
  stops to rethink before PB2.

## Worlds and cost
- **Worlds:** 32 new seeds, v13, LP, run to year 110.
- **Who is followed:** adults born after year 70 are followed from their first adult week, so whole learning lives fit
  in the window.
- **Cost:** small weights per person, a few multiply-adds a week. Much cheaper than PB0, so the cloud should manage it
  in well under the limit.

## Open questions for the council
1. Are the inputs fair: nothing that smuggles in an outcome, and enough to make generalisation possible?
2. Is "unfamiliar (situation, action)" the right generalisation test, or should unfamiliar materials and places be
   primary?
3. Observed examples: should they count fully, or be down-weighted, and by what rule set in advance?
4. Should the observed variants also see others' failures, or only what is visible? Today what is visible is the
   other's action and its result for them.
