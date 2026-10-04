# E6.6: The reward horizon · how far back can people learn?

## Answers

**1. How many delayed-benefit behaviours already exist?** There are three channels that can link an act to a
later outcome, and they carry these behaviours:

| Channel | Behaviours it carries | How the delayed outcome finds the act |
|---|---|---|
| **By place**: beliefs about leaving things somewhere | sowing seed; stashing food; heaping materials (shelter from the cold); striking stone at home | the outcome happens **at the same spot**, within a year |
| **By thing**: the worth of a made thing | making any tool, wrap, carrier or raft; gathering materials for it (they are wanted for what they make) | the thing is **still in hand** when it pays off |
| **By word**: checking what was told | acting on a reported place, animal or practice | the claim is checked whenever the person gets there |
| (E6 only, never reached) | holding food in a fire; filling a vessel | when the food is eaten, or the water drunk |

In 4 worlds × 150 years there were about 34,000 acts of leaving things somewhere, about 6,000 makings, and
164,000 times a later outcome moved a belief about something left somewhere.

**2. What is the longest delay people learn from?**
- **By place: up to a year, the whole length of their memory for what they left where.** Beliefs moved by outcomes
  27–52 weeks later changed behaviour as much as those moved 5–12 weeks later. After a credit up they did the same
  act again within a year 16 points more often than after a credit down, the same gap at every delay beyond a month.
- **By thing: no limit while the thing is held.** Things first used more than a year after they were made were made
  again more often (47%) than things used at once (16%). That is mostly because things kept that long are the
  durable, valued ones, but it shows a long-delayed use still counts. Things never used were made again least (9%).
- **Habits: about 1–5 weeks.** Next week counts 0.8, so a reward 5 weeks later counts 0.33 and one 20 weeks later
  0.01. Against ordinary weekly ups and downs (standard deviation 0.11), even a large reward is lost after about 9
  weeks, and an ordinary one after about 4. Habits are kept per situation, not per act.

**3. Do they learn from outcomes 1, 5 and 20 weeks later?** Yes, yes and yes, but only by place or by thing. They
learn nothing about acts whose outcome comes back neither to the spot where something was left nor through
something they still hold.

## What this means for E6

**The reward horizon is not the bottleneck.** The water vessel's payoff, water drunk weeks later and far away,
would have reached its maker by the thing channel: drinking from it raises both its worth and their expectation of
filling it (`fill:water`). That loop exists and would have worked. **It never started, because the vessel was never
filled once.** E6.5 found the same: the broken link is the first try. People learn delayed consequences well; they
almost never take a first step that pays nothing now.

This favours the world-side mend from E6.5. If the world fills an open, tight vessel with rain, the person holds
water without having chosen to. The next time they are thirsty far from a spring, they drink it (that already
happens on its own), and the existing thing channel does the learning. Nothing about the agents changes.

## Caveats

- "Credit up, then repeated" is not a clean causal test. Credits and repeats both happen most at home. The
  comparison is between credits up and credits down in the same channel, which removes much of that, but not all.
- The by-place channel credits **everything** left at a spot in the past year, whether or not it caused the outcome.
  It learns long delays, but indiscriminately: superstition by design (Law 71). Whether long-delay beliefs are
  *correct* is not measured here.
- Made-again rates by delay are confounded by what kind of thing it is (durable things are held longer).

Watch-only replays of today's code (the live world's code), seeds 301, 302, 303, 304, 150 years each. Replays matched the saved worlds at year 100: True, True, True, True.

## 1. Habits (what kind of action goes well in a situation)

Each week's habit update counts next week's prospects at 0.8, so a reward k weeks after an act counts 0.8^k. The act's own reward is mixed with every week in between, whose rewards vary with a standard deviation of **0.11** (measured).

| delay | weight of the reward | a reward of 1.0 stands out from one ordinary week's noise? |
|---|---|---|
| 1 week | 0.800 | yes |
| 2 weeks | 0.640 | yes |
| 5 weeks | 0.328 | yes |
| 10 weeks | 0.107 | no |
| 20 weeks | 0.012 | no |
| 52 weeks | 0.000 | no |

And habits are kept per situation (32 of them: food in hand, company, season), not per act. What they carry is how good a situation tends to be, not which earlier act made it so.

## 2. Leaving things in places (sowing, stashing, heaping): credit by delay

164059 times an outcome moved a belief about something left somewhere. The delay is the weeks since that thing was last left at that spot.

| delay | credits up | credits down |
|---|---|---|
| 0–1 weeks | 28490 | 13550 |
| 2–4 weeks | 12088 | 7560 |
| 5–12 weeks | 19661 | 8562 |
| 13–26 weeks | 22439 | 9544 |
| 27–52 weeks | 25325 | 11931 |

Which experience gave the credit:

| experience | 0–1 weeks | 2–4 weeks | 5–12 weeks | 13–26 weeks | 27–52 weeks |
|---|---|---|---|---|---|
| food left there (kept or gone) | 3 | 8 | 19 | 32 | 36 |
| returned to the spot | 1492 | 7443 | 15038 | 18374 | 24365 |
| warm or cold there | 40545 | 12197 | 13166 | 13577 | 12855 |

**Did they do it again within a year?** Learning means a credit up is followed by the act more often than a credit down.

| delay | after a credit up | after a credit down | difference |
|---|---|---|---|
| 0–1 weeks | 79% of 28490 | 69% of 13550 | +9 points |
| 2–4 weeks | 74% of 12088 | 60% of 7560 | +14 points |
| 5–12 weeks | 69% of 19661 | 52% of 8562 | +17 points |
| 13–26 weeks | 67% of 22439 | 51% of 9544 | +16 points |
| 27–52 weeks | 68% of 25325 | 51% of 11931 | +16 points |

## 3. Made things: from making to first use

| first use after making | things | made again later |
|---|---|---|
| 0–1 weeks | 2430 | 16% |
| 2–4 weeks | 702 | 20% |
| 5–12 weeks | 581 | 24% |
| 13–26 weeks | 384 | 29% |
| 27–52 weeks | 261 | 21% |
| over 52 weeks | 462 | 47% |
| never used | 1154 | 9% |

A made thing's worth attaches to the thing, and grows each time it is used, for as long as it is held. So making is the one act whose payoff can come any time later and still count, as long as the thing is in hand.
