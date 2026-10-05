# E13 — Following those who visibly do well (B2): pre-registration (FROZEN)

**Status:** signed off by the creator on 2026-10-06 and frozen as `E13-frozen` before any E13 code was written. Not to
be edited after the results.

## 1. Why

E12: the first winter planners were visible, fed more people and gained standing, and nobody around them changed,
because no adult in ACL can copy what a neighbour does. The E13 pilot: planners' habits do hold the lesson modestly
(habit value for autumn foraging while stocked 0.28 against 0.20); planners are the best-fed adult within sight 72% of
the time but the most respected only 3%, so models are chosen by visible success, not respect. The creator's question:
once a few innovators exist, can social learning amplify them?

## 2. Base world

**A2-full** (E9's code, anticipation weight 1.0), where planners exist. On the plain world there are none, and nothing
to copy. With B2 off, the E13 code reproduces E9 A2-full exactly (section 5).

## 3. The mechanism, exactly (only behaviour is copied)

Each week, in the body phase after a person's own habit update, for every adult observer p (16+):

1. **Model (deterministic):** among adults within sight (`cfg.perception`, 4 tiles), not p, the one with the most food in
   hand (`edible()`), provided it is more than p's own. Ties go to the lower id. **Arm C only:** candidates must have at
   least one child and every child they have had still alive. If no one qualifies, nothing happens.
2. **What is seen:** whether the model foraged this week (their action this week) and how much food they got (this
   week's forage event). Only foraging is copied.
3. **What is learned:** p updates their own habit for foraging in the model's situation (`m.last_ctx`: the model's food
   level, company and season), using the existing foraging reward applied to what p saw and to p's own state, at the
   existing habit learning rate and discount:

```
r      = 0.3 * min(1, got_by_model / p.need) * (0.3 + 0.7 * hunger_of(p))      # actions._forage's own reward
future = max(p.q[ctx_m * N_ACTIONS : (ctx_m + 1) * N_ACTIONS])
i      = ctx_m * N_ACTIONS + A["forage"]
p.q[i] = clamp(p.q[i] + learning_rate * (r + discount * future - p.q[i]), -1.5, 1.5)
```

Nothing else is copied: no expectation, anticipation, belief, memory or knowledge of winter. No new number is
introduced; no random draw is added.

## 4. Arms

| arm | code | B2 |
|---|---|---|
| A | A2-full (control) | off |
| B | A2-full + B2 | model: best-fed visible adult, better fed than oneself |
| C | A2-full + B2 | as B, among adults with at least one child and all their children alive |

Seeds 301–304, 120 years. No other variant will be run in E13.

## 5. Validity (kill criteria)

- Probe read-only (state hash, 20 years, both codes).
- **Zero check:** E13 code with B2 off reproduces E9 A2-full's population at every 10-year sample (seed 304).
- Arm A reproduces E9 A2-full for all seeds; code unchanged during runs; no crashes.
- **Leak test (hard fail):** adults who never once saw a better-fed adult forage (the probe applies the same rule in
  every arm) forage in autumn within ±10% of the same group in Arm A, pooled.

## 6. Order of reading (binding)

Validity and the leak test; then **repeat planning (headline)**; then the manipulation check (habit value for autumn
foraging while stocked), neighbours' foraging, planners, carers holding 20+; children's winter starvation last, read only
if the links before it hold. The strongest permitted conclusion of a success is that social learning solved the
transmission bottleneck E12 identified, not that it solved civilization.

## 7. Predictions (Arm B unless stated)

1. **Headline: preparation survives success.** At least 10% of planner-autumns are followed by planning the next
   autumn (Arm A expected about 1%), with at least 20 planner-autumns.
2. **Manipulation check.** Adults' mean habit value for foraging in autumn with 2+ weeks of food, averaged over the
   10-year samples, is higher than in Arm A in at least 3 of 4 seeds.
3. **Neighbours follow.** Planners' neighbours forage in the next autumn at least 1.1× as much as planners' neighbours in
   Arm A, pooled.
4. **More planners.** Planner-autumns at least 2× Arm A's, pooled.
5. **Better-stocked carers.** Child-winters whose carer holds 20+ food at least 5 points above Arm A, pooled.
6. **Children saved, read only if 2, 4 and 5 hold.** Children's winter starvation at least 20% below Arm A, pooled.
7. **No leak** in Arms B and C.

Arm C against Arm B: reported, with no directional prediction.
