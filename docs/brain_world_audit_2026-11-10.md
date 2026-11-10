# Where the world is built for the old brain: an audit for the neural brain (10 November 2026)

**Why:** the creator, 10 November 2026: "Check the world itself laws and nature if anything against our new neural
brain fix it. Because most rules are builded over old brain but now we got more powerful brain … we gotta stay with
this brain and connect it to world not against its laws."

**What was read:**
- `acl/mind.py` (`decide`, lines 123–598: how every week's choice is built);
- `acl/biology.py` (the body phase, `_feelings`, `_learn`, `_follow`, `_upbringing`);
- NB1's brain (`experiments/NB1_neural_brain/brain_nb.py`).

**Physics and biology are not the problem:** food, water, cold, prey, making, ageing, birth and death. The problem is
that the *deciding* in nature is still the old brain's. The neural brain was bolted on top of it.

## 1. The old brain still decides what can be chosen
`decide` builds the list of options, and the network may only rescore that list. Two kinds of old-brain judgment sit
inside the list itself.

**a. Targets are pre-chosen by hand formulas.** For each kind of action, the old brain picks one target by its own
utility (argmax), then offers only that one:
- forage: the best tile by `(0.25 + 1.6 hunger) × got`;
- hunt: the best prey tile by expected meat, boldness and dread;
- gather: the best material and tile by "worth" and curiosity;
- make: one recipe, by item value and a floor of 0.05;
- put, take, explore: one destination each.

So **the network chooses the verb, never where, what or which thing.** It cannot learn "this valley is better", or
"make the other tool".

**b. Possible actions are hidden behind the old brain's thresholds** (mind.py; these are not physics):

| action | hidden unless (old judgment) |
|---|---|
| give food | food held − 2 × own need − dependents' need > 1 |
| take another's stash | hunger > 0.4 |
| steal | hunger > 0.3 and kin < 0.5 |
| attack | grudge > 0.15 |
| care | trouble > 0.2 and (kin, partner or affection > 0.3) |
| court a non-partner | affection > −0.2 |
| make | value > 0.05 and not already held |
| explore, join, put, hunt | grown only (children never explore) |

A neural brain can only learn among the doors the old brain opens. Real limits stay, because they are the body:
energy for the action, adulthood for courting, no kin as mates, a hunter's age, things that exist.

**c. `thought.steer`** (the old mind's focus) reshapes the scores before the choice.

## 2. The network is blind to what the old brain used
- **The network sees:**
  - its body (energy, health, food held, thirst, cold, hunger, fatigue, loneliness, mood, dependents);
  - its life stage, the season and company;
  - for each option, only the action's kind, the distance, whether it is a person, and kinship and affection;
  - what others nearby did and how their mood went.
- **It does not see:**
  - how much food is on a tile;
  - prey or dread;
  - water or fire nearby;
  - its own stash;
  - another person's food, hunger, health, trust, grudge or strength;
  - whether a thing is held or valued;
  - what it remembers, or what others told it.

Every one of these is in the hand-written score instead. So the network cannot do better than the rules, and evolution
learned to trust the rules (g rose from 1.00 to 1.23).

## 3. Learning from others is wired only to the old brain
- `_upbringing`: "children absorb the ways of whoever raises them", but it copies the **habit table** `p.q`.
- `_follow` (E13, B2): watching a better forager teaches, but it also writes `p.q`.
- **NB1 does not use `p.q`, so for neural people both are dead.** A neural child learns nothing from its parents
  except one inherited genome. Culture can't pass through the brain.

## 4. The way the network learns works against needed hard work
- **REINFORCE on one week's feeling** (`r = reward + 2 × mood change`).
- **One baseline per person:** no sense of "this was a bad situation anyway".
- **No look ahead,** although the old habit table counts next week's value.
- **The gradient is multiplied by 1/temperature = 5.**

So actions taken in hard weeks (foraging while starving, caring for the sick) look bad and get pushed down. NB1 fits
this:
- the learning network's scores ran *against* the instincts (correlation −0.30);
- starvation doubled;
- learning on lowered children's survival by 0.045.

## 5. What stays (the body, which is right as it is)
- **Feelings:** wellbeing is built from being fed, health, company, the family's health and warmth, against grief, fear
  and anger. This is the body telling the brain what is good. It suits a neural brain.
- **Reflexes of the body:** eating what is held, drinking, parents feeding the young first.
- **Physics:** what an action costs, what a tile holds, what a recipe needs.

## Proposed fix: NB2, "connect the world to the neural brain"
It goes in a copy of v17, with a sham. The world's physics are unchanged.
1. **Options are what the body can do, not what the old brain likes.**
   - Several candidate targets per action, for example the k nearest reachable tiles, the people in reach and every
     makeable recipe, each described by raw facts.
   - The thresholds in 1b are removed; real limits stay.
2. **The network sees the facts** the hand-written score used (the list in 2), as raw numbers, never as utilities.
3. **Learning that looks ahead and judges the situation:**
   - an actor–critic: the brain also learns how good its situation is, and that becomes the baseline;
   - a return over several weeks (discounted);
   - the 1/temperature factor is taken out of the step.
4. **Learning from others, for the network:**
   - children nudge their network toward what their carer does in the same situation;
   - watching someone do well nudges toward their action.

   This replaces the `p.q` writes for neural people.
5. **The instincts:**
   - the hand-written score remains only as an inborn bias, weighted by the gene g that evolution can turn down;
   - the network makes the whole choice.

   Whether the instincts should fade to nothing in time is a question for the council and the creator.

**Not changed:** physics, biology, the feelings, and nature v17 for the live world, until a tested NB2 is adopted by the
safe path.

**Next:**
- the council (GPT, Gemini, DeepSeek) on this list;
- a frozen NB2 plan for the creator's sign-off;
- then build, zero checks, the run and the blind recompute.
