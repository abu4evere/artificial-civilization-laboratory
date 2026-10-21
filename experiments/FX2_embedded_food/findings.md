# FX2 — food that must be opened: findings

Frozen as `FX2-frozen` (with the creator's notes on reading tool use). Tables: `results.md`, from `analyse_fx2.py`. 768
worlds (256 seeds 6001–6256 × C, E, E0), 40 × 40, 20 founders, 120 years, nature v2. Settings in E: half of wild plant
food is embedded (`embedded_share` 0.5), only 20% of it can be had bare-handed (`embedded_bare` 0.2), and a hard thing
in hand opens the rest (`embedded_tool` 1); E0 is the same world with no tool benefit. **These numbers are operational
assumptions, not measured from real land.** The run paused twice (computer sleep, session restart) and resumed without
loss.

## Validity

Zero checks PASS; all worlds present; one fingerprint; manipulation checks PASS (embedded food is 35.1% of adults'
foraged food in E and 30.0% in E0; needed at least 25%). **Valid.**

## The frozen readings

| question | comparison | result | reading |
|---|---|---|---|
| (1) Does making hard things useful change tool use? | E against E0 | share of adult forage-weeks with a hard thing (hardness ≥ 40) in hand: median 0.396 against 0.244; +0.124 [+0.106, +0.142], Holm p 2.8e-25 | **changes tool use** |
| (2) Survival when food is harder to reach but tools help | E against C | died out **256 of 256** against 96 of 256 | **changes survival** (E far worse) |
| (3) Does the tool benefit change survival? | E against E0 | 256 against 256 | **no meaningful effect** (both all die) |

## Beside it (described; population first)

| arm | median end of the world (year) | births per woman-year | blocked for want of a partner | embedded share of adults' food | opened with a hard thing | forage-weeks a hard thing was used on embedded food |
|---|---|---|---|---|---|---|
| C | 120 (most live) | 0.128 | 0.550 | 0% | – | 0% |
| E | 39.6 (range 10–118) | 0.110 | 0.617 | 35.1% | 68.8% | 38.6% |
| E0 | 34.0 (range 7–55) | 0.131 | 0.541 | 30.0% | 0% | 0% |

## What it shows

1. **People did take up tools when tools paid.** With embedded food that a hard thing opens, adults carried a hard
   thing in 40% of forage-weeks against 24% without the benefit, and actually used one on embedded food in 39% of
   forage-weeks; two thirds of the embedded food they ate was opened with a tool. This is the clearest case so far in
   ACL of a tool coming into use because it helps: the creator's FX2 note asked for exactly this distinction
   (carried versus actually used), and both rose.
2. **But the world as set was too hard to live in.** Every E and E0 world died out, most within 30–40 years; the
   median E world ended in year 40. Tools let E worlds last somewhat longer than E0 (median 40 against 34 years, the
   longest 118 against 55), but not to survive.
3. So the study answers question (1) and cannot answer (3): with survival at zero in both arms there is no room for the
   tool benefit to show. The operational numbers (half of all plant food embedded, 20% reachable bare-handed) made the
   land far poorer than intended.

## Against the prior (frozen; kept as written)

- "E against E0: more tool use, but small": **more tool use, right; small, wrong** (+12 points, clearly beyond chance).
- "E against C: more extinction": **right**, far beyond expectation (every world).
- "E against E0: less extinction, only if tool use spreads": **not shown**; both arms die out entirely.

## What it cannot show

Whether embedded food and tools help survival at a gentler setting (for example a smaller embedded share or more of it
reachable bare-handed): the plan named one level and labelled it operational. Whether the tool use spread by teaching
or was found again by each person was not measured here. Whether the higher partner blocking in E is a cause or a
consequence of the worlds shrinking is not shown. A follow-up at gentler settings would be a new study, needing the
creator's decision, with the numbers anchored to evidence where possible.
