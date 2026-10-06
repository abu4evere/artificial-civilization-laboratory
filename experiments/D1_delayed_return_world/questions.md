# D1 — Is delayed return adaptive in ACL's world? Questions (written before any data)

**Read-only. No new mechanic, no new psychology.** The creator, after N2: "Before discussing satiety changes, I want to
know whether delayed-return behaviour is even adaptive in ACL's world." Two questions, in the creator's order:

- **Part A:** Are ACL's food resources dense, predictable and storable enough to support delayed-return strategies?
- **Part B:** Does sowing, which already exists, function as a delayed-return behaviour that people can discover?

"If either answer is no, then changing agent psychology may be premature, because the environment itself may favour
immediate-return living." (The creator.)

**Worlds:** E13R's control (Arm A), seeds 501–516, 120 years, replayed with a read-only probe (state hash, 20 years;
every replay equal to the saved E13R run).

## The world's rules, read from the code before any data

- **Wild plant food:** each land tile holds at most 64 × its fertility and regrows 14 × fertility a week, times the
  season (spring 1.3, summer 1.0, autumn 0.5, winter 0.15) and the year's weather; in winter 3% a week dies back (more
  in hard winters).
- **Keeping:** loose food rots 4% a week (a quarter as fast near smoke or once fired); seed rots 0.5% a week. Of a plant
  harvest, the share that is seed is 0% in spring, 12% in summer, 35% in autumn, 5% in winter.
- **Sowing:** seed put in the ground sprouts 8% a week in spring and summer, each sprouted unit growing up to 5 units of
  food (× 0.4 + 0.6 × fertility); outside the growing seasons, 3% a week of it is eaten by animals. Standing crop rots
  5% a week in winter. Anyone may forage a sown tile.
- **Learning from sowing:** returning to a spot where one sowed (or saw turned earth) four or more weeks later, a person
  compares how much the spot stands out now with how it did then, and moves their belief about sowing in that season.
  Remembered placements last about a year.

## Part A — the world

1. **Density.** How concentrated is plant food on land? The share of all plant food held by the richest 10% of land
   tiles, by season.
2. **Predictability.** Does a tile that is rich this autumn tend to be rich next autumn? Year-to-year correlation of
   each land tile's plant food at mid-autumn. And how much the world's total food varies from year to year.
3. **How lean is winter?** Plant food on land per person, mid-autumn against mid-winter; and how much a week of
   foraging yields in each season (from U1).
4. **Storability.** Of the food people hold at the start of winter, how much is seed (from W1); and how long each form
   of food keeps under the rules above.

## Part B — sowing

5. **How much is sown, when, by how many?** Seed put in the ground, by season; number of distinct sowers.
6. **What does it yield, and when?** Crop that grows on sown tiles in the following year, against the seed sown (the
   return), and the weeks until it appears.
7. **Who eats it?** Crop harvested from tiles by the sower, by others, and how much rots.
8. **Do sowers learn it paid?** For each sowing: whether the sower came back to the spot four to fifty-two weeks later;
   how their belief about sowing in that season changed over the year; and whether they sowed again the next year.

## Reading rule

Descriptive; nothing scored. D1 changes nothing in any world.
