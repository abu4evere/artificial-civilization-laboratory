# WS1 — World size: findings (12 October 2026)

Frozen as `S1-frozen` (alias `WS1-frozen`). 256 new seeds (3001–3256), 120 years, five arms, settings only in `code_p2` with
every setting off. The numbers come from `analyse_s1.py` (frozen, unchanged) → `results.md`. The trajectories come from
`trajectories.py` (descriptive, **not pre-registered**). Raw outputs: `output/` (1,280 worlds, all read back intact).

The run was stopped twice (the PC shut down on 11 October, and slept on 12 October). Each time the runner resumed by
skipping saved worlds; no output was broken (each file re-read as JSON before resuming). The folder was renamed from
`S1_world_size` to `WS1_world_size` after the run ended, as the pre-registration's note said it would be.

## Validity

- **Zero checks** (`code_p2` with settings off equals the control code at 40 × 40 and 80 × 80): **passed.**
- **Code fingerprint unchanged in every run:** yes.
- **Sham against C:** died out 95 vs 107; 46 saved, 34 lost; p = 0.219. Below the alarm line, so no caveat applies.

**Valid.**

## Baseline (rule 14)

**C (today's world: 40 × 40, 20 founders) died out in 107 of 256 worlds (41.8%).**

## Manipulation checks: the arms differed as intended

| | C 40×40, 20 | L 80×80, 20 | LP 80×80, 80 | P 40×40, 80 | S |
|---|---|---|---|---|---|
| land tiles per founder (week one) | 32 | 128 | 32 | 8 | 32 |
| distance between founding bands | 15.3 | 29.6 | 29.3 | 15.5 | 15.3 |
| possible partners in sight per founder | 2.2 | 2.2 | 9.7 | 9.7 | 2.2 |
| seeker-weeks with an eligible single in sight (whole run) | 0.32 | 0.34 | 0.62 | 0.47 | 0.33 |

## The frozen outcomes (population beside every measure, rule 18)

| | C | L | LP | P | S |
|---|---|---|---|---|---|
| **worlds died out (of 256)** | **107** | **108** | **2** | **23** | 95 |
| growth multiple (population at 119 ÷ founders), median [IQR] | 0.65 [0, 1.95] | 1.17 [0, 3.35] | 1.77 [1.21, 2.30] | 0.56 [0.38, 0.76] | 1.02 [0, 2.04] |
| median population, year 119 | 13 | 24 | 142 | 45 | 20 |
| births per woman-year | 0.129 | 0.127 | 0.137 | 0.152 | 0.132 |
| child deaths per birth | 0.202 | 0.150 | 0.174 | 0.282 | 0.203 |
| starving share | 0.036 | 0.027 | 0.034 | 0.046 | 0.036 |
| decisions blocked for want of a partner | 0.56 | 0.57 | 0.48 | 0.46 | 0.55 |

### Q1. Does a larger world change survival? L against C

Died out 108 vs 107; 63 worlds saved and 64 lost; sign test **p = 1.000** (Holm 1.000). Effect −0.004, 95% interval
[−0.090, +0.082]. Half of F2's effect is 0.142, and the interval excludes it.

**Frozen reading: no meaningful effect.** Four times the land, for the same 20 people, does not change whether a world
survives. Its survivors grow larger (growth multiple 1.17 vs 0.65; Wilcoxon p = 8.4 × 10⁻⁵).

### Q2. Do more founders change survival, given the larger world? LP against L

Died out 2 vs 108; 106 saved and 0 lost; sign test **p < 0.001** (Holm < 0.001). Effect **+0.414**, 95% interval
[+0.355, +0.473].

**Frozen reading: the change improves survival.** The effect is about three times half of F2's effect.

### Q3. Do more founders change survival without more land? P against C

Died out 23 vs 107; 88 saved and 4 lost; sign test **p < 0.001** (Holm < 0.001). Effect **+0.328**, 95% interval
[+0.266, +0.391].

**Frozen reading: the change improves survival.**

**Descriptive only** (as frozen):
- LP against C: 2 vs 107 died out.
- LP against P: 2 vs 23. More land helps when there are 80 people, unlike with 20.

## Population over time (descriptive; NOT pre-registered; `trajectories.py`)

The worry this answers: a world that **starts** with 80 people might survive to year 120 just because it takes longer to
die out, not because it is viable. Median population at each decade mark (years 9, 19, …, 119), surviving worlds:

| arm | year 9 | 29 | 59 | 89 | 119 | survivors smaller at 119 than at 89 |
|---|---|---|---|---|---|---|
| C | 26 | 28 | 33 | 37 | 36 | 50% |
| L | 29 | 32 | 38 | 46 | 59 | 25% |
| LP | 104 | 105 | 132 | 142 | 143 | 54% |
| P | 63 | 50 | 50 | 50 | 48 | 53% |
| S | 26 | 29 | 34 | 37 | 37 | 53% |

- **P is not a slow decline.** It falls from 80 to about 50 within 30 years (crowding: 8 land tiles per founder), then
  holds there for 90 years, as C's survivors hold at about 36.
- **LP grows** to about 140 and levels off.
- **L's survivors are still growing at year 120.** More land raises how large survivors become, not whether they
  survive.

## What the result says (interpretation)

1. **People, not land, is what keeps ACL's worlds alive.** Adding land alone changed nothing. Adding founders cut
   extinction from 42% to 9% on the same land, and to under 1% with four times the land.
2. **This supports the explanation F1, P2 and GF1 point to,** without proving it: worlds die from failing to find
   partners. With 80 founders, an eligible single was in sight in 62% of seeker-weeks (LP), against 32% today (C). The
   share of decisions blocked for want of a partner fell (0.48 vs 0.56) but stayed high.
3. **It matches the evidence review (N10)** in direction only. Twenty founders hold one aggregated band of 20–40, below
   the 75–150 put forward as a minimum viable size (White 2017). The 80-founder worlds settle at about 50 (P) and 140
   (LP). The anchors describe real populations, not ACL's tiles, and do not set ACL's numbers.

## What it cannot show

- **More founders came in larger founding bands** (4 bands of 20, not 4 of 5), because the code caps bands at 4. Q2 and
  Q3 test "more founders, in larger bands"; they cannot say which matters. **MB1a** (frozen, next after AA1) measures
  whether bands ever meet, in these very worlds (seeds 3001–3064). **MB1 Stage B** (draft) is the design that separates
  the two.
- **P ran at four times today's crowding.** Its survival came with more child deaths (0.28 per birth vs 0.20) and more
  hunger (0.046 vs 0.036).
- **One stretch of land per seed.** C and L cannot share land, so Q1's pairing is by seed only.
- **AA1's shortcuts** (A1 corner crossing, A5 knowing where absent loved ones are) are present in every arm. Their size
  is measured next.

## Priors (written before the run) against the result

- **Assistant: "L worse than C."** Wrong: no meaningful effect either way.
- **Assistant: "LP better than L."** Right, and by far more than expected (2 vs 108 worlds lost).

## What it changes

- The next phase should treat population structure as the main lever: how many people, in how many bands, and whether
  they meet. Land size is not the lever for survival.
- A world with **80 founders is a candidate new baseline** for studies of culture, because only 0.8–9% of its worlds die
  out, so outcomes aren't swamped by extinction. That is a decision for the creator. It would be a new baseline, kept
  apart from the 20-founder record, never replacing it.
