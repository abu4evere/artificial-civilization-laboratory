# E9 — Candidate anticipation mechanisms (design document, not yet frozen)

**Written:** 2026-10-05, after E8.4. No E9 code exists. This document is for choosing; the chosen mechanism and
its predictions will be frozen in a separate pre-registration before any code is written.

## Why

E8.3 and E8.4 found ACL's largest killer and its cause. 88% of starvation deaths come in winter or early spring.
Autumn offers a median surplus of 163 beyond its own needs, more than the 150 a winter takes, and the median adult
walks into winter holding 13. The world allows preparation. Nobody prepares.

The reason is in how hunger works today (`mind.hunger_of`): hunger is how many weeks of food a person has in hand
or stored nearby, against their need, and it falls to zero at two weeks. A person with two weeks of food feels no
pull to forage at all. Nothing in them reaches beyond that.

## What the mind already does (precedent)

- **Thirst is anticipated from experience.** `p.expect["dry"]` follows how thirsty a person has actually been
  (biology.py). It raises the cost of going to dry places and the pull to fill a vessel (mind.py). No fact about
  drought is involved; only "I have been thirsty".
- **People already think in seasons, about materials.** Beliefs about leaving materials somewhere carry a season
  (`fiber@3`). When choosing what to gather, the mind already looks at the current season *and the next one*
  (mind.py, `season + 1`).
- **Learned expectations are a standard tool.** `knowhow.expectation` moves an expectation a fixed step toward each
  new experience.

So none of the candidates below gives people anything new in kind. Each extends to hunger what thirst and
materials already have.

## The rule every candidate must keep

No candidate may contain: a store or put instruction; any mention of carriers, containers or heaps; a rule that
fires because it is autumn; a fact about winter that the person has not lived; or any change to how things are
valued. The only thing a candidate may change is **how strongly hunger pulls**, and only from **hunger the person
has experienced** (or, in A3/A4, witnessed or been told of). Whether anyone then forages more, stores, carries or
makes anything is left entirely to the people.

## The candidates

### A1 — Remembered hunger (not seasonal)
- **Change:** a new expectation `expect["hungry"]`, learned from experienced hunger like `dry`. The pull of hunger
  becomes the larger of today's hunger and a fraction of the expected hunger.
- **What it does not change:** anything about seasons.
- **Expected behaviour:** people who have been hungry forage more all year round. Storage, if it happens, is a
  side effect of carrying more food in every season.
- **Risk:** a weak test of anticipation, because it is not tied to *when* hunger comes. It may simply make everyone
  forage more, depleting plants in the growing seasons.

### A2 — Seasonal hunger expectation (recommended)
- **Change:** an expectation per season, `expect["hunger@s"]`, learned only from the hunger a person actually felt
  in season s. In season s, hunger's pull also feels a fraction of `expect["hunger@(s+1)"]`: the same one-season
  look-ahead the mind already uses for materials.
- **What it does not change:** no fact that winter comes, no storing rule. Someone who has never been hungry in a
  winter has nothing to anticipate. Children start at zero; it is not inherited and dies with the person.
- **Expected behaviour:** in the autumns after a hungry winter, those who lived through it forage beyond today's
  need. Whether the extra is eaten, given away, carried, put in heaps or lost to rot is up to the world.
- **Risk:** most of the dead are children and infants (E8.3); survivors who carry the lesson are the adults who were
  hungry but lived. If too few survive hungry winters, the expectation may not form often enough to matter.

### A3 — Witnessed hunger (A2 plus learning from others)
- **Change:** A2, plus a weaker update to `expect["hunger@s"]` when a person sees someone near them starve, or die
  of hunger, in season s.
- **What it does not change:** the same limits as A2. Nothing is told; only seen.
- **Expected behaviour:** anticipation spreads to people who were not themselves the hungriest, including the
  young, through what they witness.
- **Risk:** two changes at once if run without A2 alone; it should be an arm beside A2, not instead of it.

### A4 — Told hunger (A2 plus stories)
- **Change:** A2, plus a weak update when a person is told a remembered story of someone starving in season s,
  through the story channel that already carries killings and thefts across generations.
- **What it does not change:** nobody is told to store anything; they only hear that hunger happened, as stories
  already carry other events.
- **Expected behaviour:** the expectation can outlive the people who felt it, carried by culture. This is the most
  civilisation-like route, and the hardest to interpret.
- **Risk:** the most moving parts; best tested only after A2 shows whether the basic capacity matters at all.

### A5 — General seasonal anticipation (every need)
- **Change:** A2's mechanism for every need that varies by season: hunger, cold and thirst.
- **What it does not change:** as A2.
- **Expected behaviour:** people prepare for cold as well as hunger, which could also raise the worth of wraps and
  shelter.
- **Risk:** many changes at once; a success could not be traced to one need.

## What should count as success (not "more foraging")

More anticipation must mean more autumn foraging, so that is only a **manipulation check**, like making in E8 Arm
1. Success is judged on what follows, mechanism arm against control:

1. **Manipulation check:** autumn foraging rises among adults who have lived through a hungry winter.
2. **Preparation:** food in hand, seeds and stores at the first week of winter.
3. **Survival:** winter starvation deaths, infant deaths, and population over the run.
4. **The chain the project has been looking for:** whether the carrying limit ever binds; whether carriers gain worth
   and are made more often; whether skill outlives the founders; recipes held; and, in a 300-year follow-up only,
   whether lasting novelty appears after year 100.
5. **The cost:** plants depleted in autumn; any rise in starvation in other seasons.
6. **A leak test:** storing or extra autumn foraging by people who have never been hungry in a winter (and, for A2,
   never seen or heard of it) would mean the mechanism is scripting rather than anticipating.

## Recommendation

**A2 alone first.** It is the smallest change that tests the hypothesis exactly: a person who has lived through a
hungry season feels that season's hunger a season early. It reuses two things the mind already does (learned
expectations, as for thirst; one-season look-ahead, as for materials). A3 and A4 become later arms only if A2 shows
the capacity matters. A1 is the fallback if A2's expectation forms too rarely.

The fraction of expected hunger that is felt, and how fast the expectation is learned, must be fixed before coding,
with a short read-only pilot of the control worlds to see how hungry people actually get in each season.
