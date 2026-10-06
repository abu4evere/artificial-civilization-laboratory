# N1 — Which candidate changes the least while addressing U1?

**Written:** October 2026, after `evidence.md`, at the creator's request. **No code, no experiment, no choice made.**

## What "addressing U1" means

U1 found that people stop gathering at two weeks of food, because hunger (`1 − weeks ÷ 2`) reaches zero there and the
pull to forage (`0.25 + 1.6 × hunger`) falls to its floor; and that stashing becomes possible at the same line. A
candidate addresses U1 if it plausibly lets a person keep gathering past two weeks of food, for reasons of their own.

## What "changes the least" means, measured from the code

Read from the E13R code before writing this:

- General `hunger` is used **26 times** in `mind.py`: in the pulls to forage, rest, talk, court, steal, give, care and
  more. Changing it changes nearly every choice a person makes.
- E9 introduced a narrow channel, **`food_hunger`**, used in only **three** places: the pull to forage, the pull to hunt,
  and the "I'm hungry" thought. E9's anticipation acted only through it, and its zero check and leak test both worked.
- The habit learner looks about five weeks ahead (`discount` 0.8 a week; E6.6) and counts against instinct at
  `learned_weight` 0.6. Changing it changes every habit of every action.
- The forage reward that teaches the habit is scaled by hunger too (`0.3 + 0.7 × hunger`).

So "least change" is judged on five things: how much code; **how many choices it reaches**; how many new numbers it
needs (each a dial that could be tuned toward the answer); who it touches (leak); and whether it keeps earlier results
valid (a zero check that can reproduce the existing worlds exactly).

## The four candidates, measured

### C3 — Smooth satiety, **scoped to `food_hunger` only**

- **Code:** one expression, in the one place `food_hunger` is set. The general `hunger` is untouched.
- **Reach:** three uses (forage, hunt, the hunger thought). Talking, giving, courting, stealing and resting are
  unchanged.
- **New numbers:** one (how slowly the pull fades past two weeks). It must be fixed by an argument written before any
  result.
- **Who:** everyone (a leak), but only in the pull to get food.
- **Zero check:** yes, as for E9 (with the new number set to reproduce the old curve).
- **Addresses U1:** **directly.** The pull to forage no longer hits its floor at two weeks.
- **Evidence:** moderate and general (`evidence.md`).

### C4 — Insecurity learned from one's own swings (a generalised A2)

- **Code:** small; one new learned value per person, beside E9's existing expectations, acting through `food_hunger`.
- **Reach:** three uses, as C3.
- **New numbers:** two (how fast it is learned, how strongly it weighs), unless E9's are reused.
- **Who:** **nobody who has never gone short**: the only satiety candidate with no leak by design.
- **Zero check:** yes.
- **Addresses U1:** **only for those who have lived through swings**, and E9 showed such lessons are strong but rare
  and erase themselves after a good winter (E9.3, E9.4). Likely partial.
- **Evidence:** moderate, mixed in direction (scarcity can also narrow people to the present).

### C11 — The body as a store

- **Code:** large. A new body reserve for every person, rules for filling and burning it, and a hunger redefined around
  it.
- **Reach:** wide. Eating, health, starvation, the pull to forage, and anything that reads hunger.
- **New numbers:** several (how much food becomes reserve, how large it can grow, how fast it burns).
- **Who:** everyone.
- **Zero check:** only by switching the whole reserve off.
- **Addresses U1:** **partly, and differently.** It gives people a reason to eat more in plenty, and so to gather more,
  but the surplus goes into bodies, not stores. It could soften winter without anyone learning anything, and relieve the
  pressure that makes storage worth inventing.
- **Evidence:** strong.

### C8 — A longer mind

- **Code:** small in lines (the habit learner's horizon), but:
- **Reach:** **every habit of every action**, all at once.
- **New numbers:** one or two (the new horizon; perhaps how a delayed result is credited back).
- **Who:** nobody until they live through a long cause and effect: leak-free in principle, but it re-weights every
  existing habit, so earlier worlds would not reproduce.
- **Zero check:** only at the old horizon.
- **Addresses U1:** **indirectly.** U1's stop is in the *instinct* part of a choice (the forage pull's floor), while C8
  changes the *habit* part, which counts at 0.6 against instinct. Whether a longer horizon could outweigh the floor is
  unknown.
- **Evidence:** strong for the capacity, weak for its use (`evidence.md`).

## Summary

| | code | choices reached | new numbers | who | zero check | addresses U1 | evidence |
|---|---|---|---|---|---|---|---|
| **C3 (scoped)** | **one expression** | **3** | **1** | everyone, food pull only | yes | **directly** | moderate, general |
| C4 | small | 3 | 2 | **never-short: none** | yes | partly (rare, self-erasing) | moderate, mixed |
| C11 | large | many | several | everyone | only by switching off | partly, into bodies | **strong** |
| C8 | small in lines | **all habits** | 1–2 | in principle none | only at old horizon | indirectly | strong capacity, weak use |

## Answer

**C3, scoped to `food_hunger`, changes the least while addressing U1 directly.** It touches one expression and three
uses, adds one number, keeps a zero check, and leaves every social choice as it is. It matches the creator's
expectation that C3 is the safest.

**C4 is second:** nearly as small, the only one with no leak, but likely to address U1 only for a few.

**C11 and C8 change much more.** C11 is the most realistic but the largest change and may relieve the very pressure
being studied. C8 is the most interesting but reaches every habit and acts on the wrong part of the choice.

## Two cautions before any choice

1. **C0 is still on the table.** The evidence (`evidence.md`) shows that whole human societies with full human foresight
   and appetite store little, because they live by sharing (Woodburn's immediate-return societies). ACL's people look
   much like them. The missing piece may be culture, not nature. Changing nature to make storage appear risks answering
   the wrong question.
2. **C3's one number is the danger.** "Least change" is not "no risk". How slowly the pull fades past two weeks decides
   how much people gather; if it is tuned until storage appears, it is the answer written in through a number. It would
   have to be fixed from an argument, frozen before any run, and tested at more than one value, as E9 tested two
   strengths.
