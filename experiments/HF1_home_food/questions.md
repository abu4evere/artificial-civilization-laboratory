# HF1 — Did food run short around HB1's homes? (read-only check, rule 12; DRAFT for sign-off, questions to be frozen before any data)

**Chosen by the creator (October 2026), after HB1:** measure food around homes read-only before designing HB2. No fixes,
no tuning, no code changes.

## Why

HB1 kept couples together (apart 57.8% → 0.1%) but raised extinction (33 of 64 against 22; p = 0.043; sham p = 0.815).
The exploratory reading was that **food near fixed homes ran short**: starvation rose (adult starvation deaths 714 against
412 in years 0–39), while illness, the cost of crowding, fell as a share of deaths. But food on the land was never
measured; depletion was inferred from deaths. HB2 (a home that moves with the food) only makes sense if the inference is
right. HF1 measures it directly.

## The code, read before any data

- **Wild plant food** is `tile.plants`. Each week it regrows by `plant_regrow × fertility × growth` (season, weather,
  wetness) up to a cap of `plant_cap × fertility` (64 at fertility 1), and dies back in winter (`world._grow_land`).
- **Foraging** (`actions._forage`) takes up to the forager's rate (`forage_base + forage_skill × skill`, times stage and
  tool; capped by what they can carry) from the tile they stand on: sown crop first, then wild plants. If the tile holds
  less, they get less. Meat (hunting, fish) is a second source and is not taken from tiles.
- **The couple's home** is `world.couple_home(a, b)`: the place either partner remembers with the highest combined value.
  It draws no random numbers and exists in the code whether `home_base` is on or off, so it can be computed for control
  couples too (where nobody returns to it).

## Questions

All in the first 40 years (where HB1's starvation gap was largest), per couple-week (both partners alive and adult, a
couple home exists), arms H (HB1, `home_base = 1`) and C (the same code, settings off).

1. **Food near home.** Wild plant fullness (`plants ÷ cap`, over tiles with a cap) on tiles **within `reach` (3) of the
   couple's home**, and on the ring **4–6 tiles** from it. Reported overall and by season.
2. **Foraging returns.** Mean food gained per adult forage action (`forage` events, `got`), split by where it happened:
   within 3 tiles of the forager's couple home, or further. Plus the share of forage actions that left the tile with
   less than 1 unit of wild plants (the tile was emptied).
3. **People near home.** People per tile within 3 tiles of the couple's home (the load on that land), beside every
   measure (rule 18), with population.
4. **Before starvation deaths** (descriptive, not in the rule): for adults who died of starvation, wild plant fullness
   within 3 tiles of where they were, over their last 8 weeks, against the same measure for all adults in those weeks.

Hunting is reported beside (hunts per person-year), to see whether meat made up for, or added to, any plant shortfall.

## Decision rule (proposed; frozen at sign-off; read on discovery and holdout separately)

| | reading |
|---|---|
| In **both** sets: H's fullness within 3 tiles of home is **at most 80%** of C's, **and** H's food per forage action is lower than C's | **Depletion confirmed.** HB2's design can rest on it |
| In **both** sets: H's fullness within 3 tiles of home is **at least 95%** of C's | **Not confirmed.** The hunger has another cause; HB2 is not designed until it is found |
| Otherwise | **Mixed.** Reported as such; the creator decides |

The 4–6 ring answers a second question beside the rule: whether, in H, food stood untouched a short walk beyond the
home (a home that should have moved), or ran short everywhere (too many people for the land).

## Worlds

| set | seeds | runs |
|---|---|---|
| **Discovery** | 501–516 (HB1's and F1's first 16) | H and C, 40 years |
| **Holdout** | **1301–1316, new**, never run in any arm (rule 15: HB1's reading came from all 64 of its seeds) | H and C, 40 years |

## Hard stops

- **Observer read-only:** with the observer attached, the world's state hash after 20 years equals the hash without it
  (H and C, two seeds).
- **Replays reproduce:** on the discovery seeds, H matches HB1's saved populations and C matches F1's, for years 10–40.
- **Code unchanged:** `code_hb1`'s fingerprint before and after each run.

## Priors (written before any run; not predictions to test)

- **Assistant:** depletion confirmed: H's fullness near home clearly below C's, food per forage action lower. Less sure
  about the ring: I expect food left a few tiles out (a home that should have moved), which would support HB2 directly.

## Decisions for the creator

1. **The threshold:** confirmed at **≤ 80%** of the control's fullness near home (with lower food per forage action);
   not confirmed at **≥ 95%**?
2. **Holdout on new seeds** 1301–1316 (unseen by HB1), as proposed?
3. **First 40 years only**, as proposed?
