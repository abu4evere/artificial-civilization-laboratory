# N3 — A harder lean season: candidates (design document, not frozen)

**Written:** October 2026, after D1, at the creator's request. **No code, no experiment, no choice.**

## Why

D1 found that ACL's world favours immediate-return living: food is predictable and keeps as seed, but it is spread thin
and **winter is barely lean**. Mid-winter land holds 504 food per person against 582 in mid-autumn (13% less), and a
week of foraging yields 17.5 in winter against 19.8 in autumn (U1). In the human literature, it is a real lean season
(with dense, predictable resources, settled life and property) that makes storing worth the trouble. The question here
is what a harder lean season would be, and whether it would still be ACL's world.

## Why winter is mild now (read from the code before writing)

- Plants regrow every week at `14 × fertility × season factor × year's weather`, with season factors spring 1.3, summer
  1.0, autumn 0.5, **winter 0.15**.
- In winter, `3% × (1 + 2 × hard)` of wild plant food dies back each week, where `hard` is drawn each year between −0.1
  and 0.15 (so 2.4% to 3.9% a week).
- On a well-stocked tile, winter regrowth (about 2 a week at fertility 1) **roughly cancels** dieback (about 2 a week
  on a full tile of 64). The land stays nearly full through winter.
- A week of foraging gathers `min(forage rate, food on the tile)`, and an adult's forage rate is 12 to 26 (about 20
  typically). **A winter only bites in practice if tiles fall below about 20.** Food on the land is not the same as food
  in reach of a forager's week.
- Cold already hurts (`cold_damage` 1.2 in a fully exposed hard-winter week); fire, covered heaps and worn things keep
  it off.
- Each year's growing weather is drawn between 0.65 and 1.25; a year's wetness and winter hardness are drawn too.

## How each candidate is judged

A change to the world is **nature** in ACL's terms (physics and ecology), so the founding rule's question is different
from N1's. The danger is not scripting a behaviour into people; it is **tuning the world until storage pays**, because
the experimenter already knows storage is the answer.

- **Realism:** does it describe real seasonal environments? (General knowledge here; to be checked against sources
  before any design is frozen.)
- **Tuning risk:** how many new numbers, and can each be fixed by a principle rather than chosen?
- **Targeting:** does it reward the behaviour being studied (storing, sowing) specifically, or make winter harder in
  general?
- **Effect, from the rules:** would it make a winter week of foraging leaner, by the arithmetic above?
- **Viability:** could it simply kill the worlds? (E6's harsher worlds: four of eight died out.)
- **Continuity:** what it costs to compare with every experiment so far, all run in the current world.

---

## L0 — Keep the world as it is

- **Realism:** a winter that leaves the land seven-eighths full is mild by temperate standards; it resembles a short,
  gentle cool season.
- **Tuning risk:** none. **Targeting:** none. **Viability:** proven. **Continuity:** total.
- **Note:** keeping it is a legitimate choice. D1 then reads as: ACL's people live the life their world rewards.

## L1 — No growth in winter

The winter season factor goes from 0.15 to **0**: nothing grows in winter.

- **Realism:** strong in temperate and colder climates, where plant growth stops in winter.
- **Tuning risk:** **none in the number.** Zero is a principle, not a dial.
- **Targeting:** none; it is about plants.
- **Effect, from the rules:** dieback alone then removes 2.4% to 3.9% a week, so a tile ends winter with about 60% to 73%
  of what it held at its start. A tile of fertility 0.6 starting near 38 would end near 26: **still above a forager's
  week of about 20.** By arithmetic alone, **L1 may change little** in what a winter week of foraging yields; whether
  depletion by people closes the gap is untested.
- **Viability:** low risk. **Continuity:** a one-number change; all other rules kept.

## L2 — Wild plant food largely gone in winter

A stronger winter dieback, so that most above-ground plant food is gone by late winter (with L1, or alone).

- **Realism:** plausible for leafy and fruiting plant food in cold climates; less so for roots and stored parts of
  plants, which persist.
- **Tuning risk:** **high.** The dieback rate is a dial; where to set it decides how lean winter is. It would need to be
  fixed from a principle (for example, a stated share of plant food lost by the end of winter in a named kind of
  climate) and tested at more than one value.
- **Targeting:** none in kind.
- **Effect, from the rules:** at 10% a week, a tile starting near 38 ends near 10, **below a forager's week**: winter
  would bite.
- **Viability:** **real risk**; needs a pilot of survival before anything else.
- **Continuity:** one or two numbers.

## L3 — Food still there, but hard to reach (snow)

Winter leaves plant food in place but makes it slower to gather: a week of foraging in winter yields a fraction of what
it would otherwise, and the food is there again in spring.

- **Realism:** plausible for snowy climates: food under snow is not gone, only hard to get.
- **Tuning risk:** **high** (the winter yield fraction is a dial).
- **Targeting:** none in kind; it is about access.
- **Effect:** direct, on exactly the quantity U1 measured (yield per forage week).
- **Viability:** real risk; pilot first.
- **Continuity:** the forage rule gains a season factor; the land itself is unchanged.
- **Note:** separates two different meanings of "lean": less food (L1, L2) or food out of reach (L3).

## L4 — An autumn pulse

Much more of the year's storable food ripens in a short autumn window (as seed), with less in the other seasons.

- **Realism:** plausible for seed and nut harvests, which are seasonal pulses.
- **Tuning risk:** high (the size and timing of the pulse).
- **Targeting:** **medium to high.** It makes autumn seed, the very thing that stores, abundant: close to building the
  answer into the world.
- **Continuity:** reshapes every season's growth; large change.

## L5 — More variable years

Wider swings between good and bad years, or rare severe winters.

- **Realism:** strong in principle; real climates vary from year to year.
- **Tuning risk:** high (how wide, how rare).
- **Targeting:** none in kind.
- **Effect:** ambiguous. D1 found the world highly predictable; making it less predictable could favour storing as
  insurance, or favour sharing and moving instead. The human literature (to be checked) is not one-sided.
- **Continuity:** changes the weather draws only.

## L6 — Harsher winters where it is colder

Make winter growth and dieback depend on each tile's temperature (tiles already have one, and cold already uses it), so
that colder parts of a world have a real lean season and warmer parts keep a mild one.

- **Realism:** strong; lean seasons vary with climate.
- **Tuning risk:** medium (how temperature maps onto growth and dieback), but anchored to a quantity the world already
  has.
- **Targeting:** none.
- **Effect:** creates **within one world** both a place where storing pays and a place where it does not, so the same
  people could be compared, and could move.
- **Viability:** low to medium (warm refuges remain).
- **Continuity:** larger code change; the old world is the warm end of the new one.

## L7 — People need more food in the cold

Raise people's food need in cold weeks.

- **Realism:** plausible (keeping warm costs energy; to be checked).
- **Kind:** **this changes people's bodies, not the world**, so it belongs with N1's candidates (beside the body as a
  store, C11) rather than here.
- **Listed** so it is not mistaken for a change to the world.

## L8 — Make sown crop the food that survives winter

Wild food dies back in winter but sown crop does not (or rots less).

- **Targeting:** **high.** It rewards exactly the behaviour being studied (sowing).
- **Verdict:** **rejected.** It writes the answer into the world.

---

## Summary

| | candidate | realism | tuning risk | targeting | makes a winter week leaner? | viability risk | continuity |
|---|---|---|---|---|---|---|---|
| L0 | keep as is | mild winter | none | none | no | none | total |
| L1 | no growth in winter | strong | **none (zero)** | none | **probably little**, by arithmetic | low | one number |
| L2 | strong dieback | plausible | **high** | none | yes, at high enough rates | **real** | one or two numbers |
| L3 | snow: food out of reach | plausible | high | none | **yes, directly** | real | forage rule |
| L4 | autumn pulse | plausible | high | **medium–high** | indirectly | low | large |
| L5 | more variable years | strong | high | none | in bad years | medium | weather only |
| L6 | colder places, leaner winters | **strong** | medium, anchored | none | yes, where cold | low–medium | larger |
| L7 | more need in the cold | plausible | — | — | — | — | **people, not world** |
| L8 | crop survives winter | — | — | **high** | — | — | **rejected** |

## Assistant's view (the creator decides)

- **L1 is the cleanest change** (one number, set by principle at zero, realistic), **but the arithmetic says it may not
  be enough**: tiles would end winter still above a week's foraging. It may be worth running for exactly that reason:
  if L1 changes nothing, a lean season in ACL needs food to be truly scarce, not just not growing.
- **L6 is the most realistic and the most informative**, because one world would hold both kinds of place, but it is the
  largest change.
- **L2 and L3** make winter bite, but each turns on a dial whose setting decides the result; each would need its value
  fixed from a stated principle and tested at two values.
- **L4 and L8 lean toward building the answer into the world;** L8 is rejected.
- **L7 is about people, not the world,** and belongs with N1.

## Rules for any next step

1. Every number fixed from a principle written before any result, never tuned until storage appears; any dial tested at
   two values, as E9 tested two strengths.
2. A **survival pilot** before any experiment: a harder world that simply dies out teaches nothing (E6).
3. The current world kept as the control. All earlier findings (E8 to D1) describe the current world; a new world needs
   its own baseline.
4. Any conclusion capped: "in a world with a real lean season, delayed return does (or does not) emerge from the
   capacities ACL's people already have", not that humans needed a lean season.
5. The realism claims above checked against sources before anything is frozen.
