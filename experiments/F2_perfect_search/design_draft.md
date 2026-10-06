# F2 — Perfect partner finding: is it search, or size? (DRAFT for the creator's sign-off; nothing frozen, nothing run)

## Why

F1 (confirmed on a holdout): a third of control worlds die out because, after the founders, people rarely pair; births
stop and the people age out. N5: real foragers find spouses in networks of hundreds, and even with perfect search a
viable people needs some 75–150 members (White 2017), while ACL's whole world starts with 20. F1 cannot tell two stories
apart:

- **Story A, search:** partners exist but are not found. Perfect finding should save the worlds.
- **Story B, size:** twenty founders are too few. Even perfect finding cannot save them.

Rule 12: before any change to how people search, check whether search is the bottleneck at all.

## What F2 is, and is not

- **A diagnostic counterfactual, not a world change and not read-only.** A copy of the control code with one switch.
  The control code is untouched. The copy is never used as ACL's nature, and nothing in it is offered as realistic.
- **M2 stays a diagnostic of search limits, not a realistic human solution** (the creator). If perfect finding saves
  ACL, that does not mean real people have a magical search radius; real foragers widen their mating networks through
  culture (marriage between bands, kin arrangement, gatherings, exchange: Walker et al. 2011; Pearce 2014). It would
  mean ACL lacks *some* mechanism that creates a larger mating network.
- **Rule 7:** with the switch off, the copy must reproduce the control world exactly (zero check).

## The switch ("oracle pairing")

Once a week, after the people have acted and before births:

1. Every unpartnered woman who is an adult by ACL's own stage (16–49) is considered in a fixed order (by id).
2. Her candidates are every man the code already allows her to court, **anywhere in the world**: adult, unpartnered,
   not kin by `world.kinship`, born within 15 years of her, not her ward or guardian. (The code's own eligibility rule,
   with the distance limit removed.)
3. If there is one, she is paired at once with one of them, chosen by the copy's **own** random stream (seeded from the
   world seed, so the world's random stream is not consumed); the pairing is recorded as an ordinary `pair` event.
4. **He moves to her tile** (both perfectly informed and able to travel), so the code's "apart" condition for conception
   does not immediately block them. After that, the ordinary code runs: they may drift apart, be widowed, re-pair.

Attraction, courtship and the code's chance of accepting are **bypassed**: this is the upper bound for search, not a
model of choice. Everything else (food, illness, conception, birth, death, children, culture) is unchanged.

## Worlds

The same **64 seeds** as F1 (501–516, 601–616, 811–818; 1101–1124), 120 years, A2-full people, every other setting at
its default. F1's replays are the paired controls (already run, all reproduced).

## Measures (population beside every measure, rule 18)

- Worlds died out (of 64), against F1's 22 on the same seeds; paired: worlds saved, worlds lost.
- For worlds that still die: births stopping before the end (as F1), share of women's weeks with no partner, deaths by
  cause and stage, population and women of childbearing age at years 20, 30, 40.
- Manipulation check: share of woman-weeks (16–45) with no partner must fall far below F1's (55–71%). If it does not,
  the switch did not deliver perfect finding and nothing is read.

## Outcomes (thresholds proposed; the creator decides)

| perfect-search extinctions (of 64) | reading |
|---|---|
| **≤ 5** (a quarter or less of F1's 22) | **Search is the bottleneck** (Story A). Design M2/M3 properly next, anchored (rule 17). |
| **≥ 17** (three quarters or more of F1's 22) | **Size is the bottleneck** (Story B). Search is ruled out as the main cause; investigate M1 (size) and M4 (density). |
| 6–16 | **Both.** Search matters, and twenty is still too few for some worlds; F2's surviving and dying worlds are compared (read-only) before any design. |

Paired check beside it: if any world that survived in F1 dies under perfect search, it is reported and examined
(perfect pairing could crowd people together or concentrate births).

## Assistant's prior (written before any run, not a prediction to test against)

White's model (non-spatial, monogamy and a kin rule) puts the viable size well above 40. ACL's 20 founders sit below
that, so the assistant expects extinctions to fall but not vanish: likely the middle row. Written down so it cannot
drift after the data.

## Order after sign-off

1. Freeze this design (`F2-frozen`).
2. Write the copy; zero check (switch off reproduces the control world on two seeds, by state hash); a smoke test on a
   throwaway seed.
3. Run the 64 worlds; report in the frozen order; index, roadmap, picture, book.

## Decisions for the creator

1. The switch as above (pair with any eligible partner anywhere, chosen at random, and bring them together), or a
   weaker version (perfect *knowledge* only: they know where every eligible partner is, but must still walk and court)?
2. The outcome thresholds (≤ 5 / ≥ 17 of 64).
3. The same 64 seeds (paired with F1), or new seeds?
