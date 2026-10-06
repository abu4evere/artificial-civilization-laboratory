# N4 — Unpredictable winters (L5 expanded): candidates (design document, not frozen)

**Written:** October 2026, after L1, at the creator's request. **No code, no experiment, no choice.**

## Why: the hypothesis L1 created

L1 removed winter growth and found (as a post-hoc observation, not a frozen finding) that a **steady** leaner winter was
absorbed by **density**: populations settled lower, each person's winter stayed as plentiful as before, and nothing in
how people lived changed. A permanently harsher world can be answered by fewer people. That turns attention to
**uncertainty**: a family stores because *this* winter might be worse than average, not because every winter is a
little worse. The creator's hypothesis, written down before any L5 work:

> **H-L5:** Delayed-return behaviour is primarily an adaptation to **uncertainty** rather than to **average scarcity**.

**A sharpening, from ACL's own record (to be checked against the literature in the evidence review):** sharing insures
against misfortune that falls on **some** families (P1: a hungry member of a family with food is far safer); it fails
when misfortune falls on **everyone at once** (P1: people die when the whole family is near empty). Storage is the
insurance that still works when nobody has anything to share. So H-L5 predicts more specifically: **storage should
answer bad years that strike the whole world together (correlated risk), more than bad luck that strikes some places or
families (idiosyncratic risk), which sharing already covers.**

## What uncertainty ACL has now (read from the code)

- Each year the world draws, uniformly and independently of every other year: growing weather 0.65–1.25 (scales all
  plant growth that year), wetness 0.45–1.35, and winter hardness −0.1 to 0.15 (raises winter dieback to 2.4–3.9% a
  week, and cold).
- The draws are the **same for the whole world** (correlated risk), **mild** (D1: a world's autumn food varies about 7%
  from year to year), **thin-tailed** (uniform: no rare catastrophes), and **independent** from year to year (no runs of
  bad years).

## Three lessons from L1 that bind every candidate

1. **Mean-preserving.** A change that lowers the average is answered by density (L1). To test uncertainty rather than
   scarcity, a candidate must keep **average** growth as it is and change only its spread or its tail.
2. **Measure the land itself.** The manipulation check must use food **per tile** as well as per person (L1's flaw).
3. **Same-seed controls and population beside every measure,** from the start (L1's redesigned pilot and Amendment 1).

## How each candidate is judged

As in N3: realism, tuning risk, targeting, effect from the rules, viability, continuity; plus two new questions:
**Is it mean-preserving?** and **Is the risk correlated (whole world) or idiosyncratic (some places)?**

---

## U0 — Keep the weather as it is

Mild, uniform, independent, world-wide variation. The control for any other candidate. A legitimate choice: ACL then
reads as a world of predictable seasons, where density and sharing are enough.

## U1 — Wider swings, same average

Widen the yearly growing-weather range around the same mean (for example 0.65–1.25 to something wider with mean 0.95).

- **Realism:** plausible; real years vary more than 7%. **Mean-preserving:** yes, by construction.
- **Risk:** correlated (whole world).
- **Tuning risk:** **high**: the width is a dial. It would have to be anchored to a real measure of year-to-year
  variability in a named kind of climate (evidence review).
- **Effect:** bad years would be worse and good years better; whether bad years outrun density depends on how fast
  populations fall.

## U2 — Rare severe winters (a fat tail)

Most winters as now; occasionally (say one year in N) a winter far harsher than any now possible (much higher dieback,
or no growth, and more cold), with the average over the years unchanged or nearly so.

- **Realism:** plausible; rare severe winters and famine years are part of real climates.
- **Mean-preserving:** nearly, if the rare winter is balanced; strictly only by design.
- **Risk:** correlated.
- **Tuning risk:** **high** (how rare, how severe). Two dials.
- **Effect:** the case closest to H-L5's story: a winter density cannot have prepared for. **Viability risk:** real;
  a rare winter severe enough to matter could end small worlds (pilot with same-seed controls).

## U3 — Runs of bad years

Make years depend on the year before (good years tend to follow good, bad follow bad), without changing the average.

- **Realism:** plausible (droughts and cold spells last more than one year).
- **Mean-preserving:** yes, by construction.
- **Risk:** correlated, and persistent.
- **Tuning risk:** medium (one persistence number).
- **Effect:** a run of bad years outlasts any one-year store; storage of seed (which keeps) could matter more than
  loose food. Population would also have time to fall, so density may again answer it.

## U4 — Patchy bad years (idiosyncratic risk)

Make the bad year fall on **some regions** of a world and not others, with the world average unchanged.

- **Realism:** plausible (local droughts, local failures).
- **Mean-preserving:** yes, for the world.
- **Risk:** **idiosyncratic** (some places).
- **Tuning risk:** medium (how large the regions, how often).
- **Effect:** the theory sharpening above predicts this is answered by **sharing and moving**, not storage. It is the
  natural partner of U1 or U2: the same total variability, distributed differently, testing the correlated against the
  idiosyncratic prediction directly.
- **Continuity:** larger code change (weather becomes local).

## U5 — Unpredictable timing (winters that come early or last long)

Let the start and length of winter vary from year to year.

- **Realism:** strong (real winters do not start on the same day).
- **Mean-preserving:** yes, if average length is kept.
- **Tuning risk:** medium.
- **Effect:** a long winter is exactly the case where a store is needed; an early winter catches people before autumn
  gathering ends.
- **Continuity:** **large**: ACL's seasons are fixed 13-week blocks throughout the code; changing them touches much of
  it.

## U6 — Harsher on average and more variable

Combine L1 (no winter growth) with any of the above.

- **Mean-preserving:** **no.** L1 showed a lower average is answered by density.
- **Verdict:** **not a test of H-L5.** Listed so it is not mistaken for one.

---

## Summary

| | candidate | mean-preserving | risk | realism | tuning risk | continuity |
|---|---|---|---|---|---|---|
| U0 | keep as is | — | correlated, mild | — | none | total |
| U1 | wider swings | yes | correlated | plausible | high (width) | settings only |
| U2 | rare severe winters | nearly / by design | correlated | plausible | high (rarity, severity) | small code |
| U3 | runs of bad years | yes | correlated, persistent | plausible | medium | small code |
| U4 | patchy bad years | yes (world) | **idiosyncratic** | plausible | medium | larger code |
| U5 | unpredictable timing | yes (if length kept) | correlated | strong | medium | **large** |
| U6 | harsher and more variable | **no** | — | — | — | **not a test of H-L5** |

## Assistant's view (the creator decides)

- **U2 (rare severe winters)** is closest to H-L5's own story: a winter that density could not have anticipated.
- **U1 (wider swings)** is the simplest mean-preserving change, but its width is a dial.
- **U4 (patchy bad years)** is the most informative **partner**: run beside U1 or U2 with the same total variability, it
  tests the sharpened prediction (storage answers correlated risk; sharing answers idiosyncratic risk) directly.
- **U5** is the most realistic but the largest change. **U6** is not a test of H-L5.

**Before any choice:** the evidence review must check (1) whether storage in real societies answers year-to-year
variability, and specifically correlated more than idiosyncratic risk; (2) how variable real years are, so that any
width or rarity is anchored to a source, not tuned; (3) how real foragers answer rare bad years (storage, sharing,
moving, eating different foods).
