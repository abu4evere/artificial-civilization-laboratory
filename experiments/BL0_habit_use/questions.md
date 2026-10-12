# BL0 — Do learned habits actually steer ACL's people? (DRAFT for sign-off; not frozen; nothing run)

**Why this comes first.** The fly-brain review (`reports/ACL audit and next phase October 2026.md`, Part 7) suggests three
learning mechanisms ACL lacks: forgetting of unused habits, need-gated use of habits, and generalisation between similar
situations. Each is a change to nature, and each only matters if learned habits already change what people do. If the
learned term almost never changes a choice, refining how it is learned cannot matter, and the next step would be
different (for example: why learning is so weak). That is unknown: no study so far has measured it (experiments/INDEX.md).

**What ACL does today (read from the code, 12 October 2026).** Each week every person at least 1 year old (`INFANT_END`)
scores each available option as *instinct* (hand-written formulas of needs, feelings and temperament, in `mind.decide`)
plus `learned_weight` (0.6) × the habit value for (situation, action). The situation is one of 32 (food held in 4 bands ×
anyone within reach × 4 seasons); the actions are 17, so each person has 544 habit values, clipped to ±1.5. Only the
habit for last week's situation and chosen action is updated (temporal-difference rule: learning rate 0.05, discount 0.8;
reward = the week's reward plus twice the change in mood); a repaid gift also nudges the giver's give-habit. Habits are
also passed on: at birth a child's habits are a quarter of the sum of the parents' (`biology.py`, birth), and until 12
a child's habits move 8% a week toward the carer's whenever they are together (`_upbringing`). Beyond that, unused
habits never change or fade. A thought on the person's mind adds a bonus (`thought.steer`). The choice is a softmax at
temperature 0.2 over the scores.

## Questions (descriptive; read-only)

1. **Reach:** per person, how many of the 544 habit values are ever updated by their own experience (as opposed to
   inherited or absorbed from a carer), by age; and how far adults' habits are from what they inherited.
2. **Influence:** in what share of decisions would the chosen action's rank-1 option differ if the learned term were
   removed? (The instinct-only top option versus the full-score top option, from the same options, same week.)
3. **Weight:** the learned term's share of the gap between the top two options, by action and situation.
4. **Staleness:** when a habit value is used, how many weeks since it was last updated.
5. **Population, survival** beside each (rules 14, 18).

## How (read-only, as AA1)

A logging copy of the control code (`code_e13r` → `code_bl0`), adding one hook at the end of `mind.decide` that records,
for each option, the instinct part and the learned part to a list held **outside** the world state (as `code_aa1` does).
No random draw added, moved or removed. Zero check before any run: state hashes of two seeds with and without the hook
identical, and identical to the control code. Worlds: F1's discovery seeds (501–516, 601–616) for discovery, holdout
811–818 and 1101–1124; 120 years, as F1. Reported per world, then median and bootstrap interval across worlds.

## Reading (draft thresholds, operational, for sign-off)

- **Habits steer:** learned term changes the top option in ≥ 10% of adult decisions (discovery and holdout).
- **Habits barely steer:** < 2%.
- Otherwise **"habits steer a little."**

## What it would decide

- If habits steer: a controlled test of one mechanism (proposals M1–M3 in the report), designed and frozen separately.
- If they barely steer: no learning mechanism is tested next; the question becomes why (weight 0.6 against instinct
  scores of what size; how often each situation recurs), read-only again.

## Cost and timing

Replays only, about F1's cost (64 worlds × 120 years). Runs after WS1, AA1 and MB1a, in the agreed order, unless the
creator decides otherwise; it does not compete with them for the computer.

## What it cannot show

Whether ACL's learning resembles a fly's or a person's. It measures only whether learned values change behaviour in ACL.
