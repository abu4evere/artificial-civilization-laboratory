# FX3 — food that must be opened, at gentler settings: findings

Frozen as `FX3-frozen` (Revision 2, after two GPT reviews). Tables: `results.md`, from `analyse_fx3.py`. Code
`code_fx2` unchanged. 1,280 worlds (256 seeds 7301–7556 × C, S25, S25-0, B50, B50-0), 20 founders, 40 × 40, 120 years.
**Run on GitHub's machines** (`cloud-run`, run 39638612975); zero checks passed there and here. Settings are
operational: S25 = a quarter of plant food embedded, bare hands get a fifth of it; B50 = half embedded, bare hands get
half; "-0" = the same without the tool route.

## Validity

Zero checks PASS (share 0 = `code_v2`; every arm acts; the tool route acts; read-only; reload exact); all 1,280 worlds
present; one fingerprint. **Valid.**

## The frozen readings

Baseline: **C died out in 80 of 256 (31.2%).**

**Primary 1, survival (always read):**

| comparison | tool arm died out | tool-free died out | saved / lost | Holm p | effect (tool-free − tool) | 95% interval | reading |
|---|---|---|---|---|---|---|---|
| S25 against S25-0 | 176 | 184 | 47 / 39 | 0.90 | +0.031 | [−0.039, +0.102] | **no meaningful effect** |
| B50 against B50-0 | 137 | 145 | 49 / 41 | 0.90 | +0.031 | [−0.039, +0.102] | **no meaningful effect** |

**Primary 2, tool use (carrying a hard thing, hardness ≥ 40, in adult forage-weeks):**

| comparison | seeds | median, tool / tool-free | mean difference | 95% interval | Holm p | reading |
|---|---|---|---|---|---|---|
| S25 against S25-0 | 256 | 0.404 / 0.300 | +0.093 | [+0.075, +0.110] | 7.5e-19 | **the tool route changes tool use** |
| B50 against B50-0 | 256 | 0.280 / 0.270 | +0.022 | [+0.005, +0.040] | 0.022 | **the tool route changes tool use** |

## Beside it (described)

| arm | died out (of 256) | against C (effect, C − arm) | median population, year 60 | embedded share of adults' food | embedded food opened with a hard thing | forage-weeks a hard thing was used on it |
|---|---|---|---|---|---|---|
| C | 80 | – | 26 | 0% | – | 0% |
| S25 | 176 | −0.375 | 7 | 13.4% | 57.3% | 24.3% |
| S25-0 | 184 | −0.406 | 7 | 10.9% | 0% | 0% |
| B50 | 137 | −0.223 | 12 | 38.1% | 34.9% | 23.5% |
| B50-0 | 145 | −0.254 | 10 | 37.1% | 0% | 0% |

## What it shows

1. **There was room this time.** Unlike FX2, many worlds survived at both levels (S25: about 3 in 10; B50: nearly half), so the tool question could be asked.
2. **Tools came into use, but did not save worlds.** In both levels people carried hard things more often when hard
   things helped, and used them on embedded food in about a quarter of forage-weeks; about half of the embedded food
   eaten in S25, and a third in B50, was opened with a tool. Yet survival with the tool route was within chance of
   survival without it (8 more worlds lived in each pair, inside the ±0.117 yardstick).
3. **Tools mattered more where bare hands were weaker.** Tool use rose about four times as much in S25 (bare hands a
   fifth) as in B50 (bare hands a half), as the prior said.
4. **Embedded food itself is what kills.** Every embedded arm died out far more than C, by 22 to 41 points, with or
   without tools. Survival was set by how hard the food was to reach, not by whether a tool could help reach it.
5. Described, not explained: S25 died out more than B50 although less of its food was embedded; with bare hands at a
   fifth, a quarter of the food is nearly out of reach, while in B50 half the food is still half-reachable by hand.

## Against the prior (frozen; kept as written)

- "S25 against S25-0: no meaningful effect": **right**.
- "B50 against B50-0: the tool route changes survival": **wrong** (no meaningful effect).
- "Tool use rises in both tool arms, more in S25": **right**.
- "Each tool-free arm dies out more than C": **right**.

## What it cannot show

Why tool use did not translate into survival: whether too few people used tools, whether the gain per use was too
small, or whether tool knowledge failed to spread (FX3 measured carrying and using, not how tool use was learned).
These settings are operational, not measured from real land. Adopting embedded food into nature would be a separate
Law 126 decision; FX2 and FX3 together show that, as built, it mostly makes worlds harder to survive.
