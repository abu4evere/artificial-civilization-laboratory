# MB1 — Many bands, one people: do ACL's bands meet, and does how a people is divided matter? (DRAFT for the creator's sign-off; nothing frozen or run)

**Asked by the creator (October 2026),** after the research report *Research to strengthen ACL* (`reports/`), whose
first conclusion was that ACL's three bottlenecks share a root: each world is one closed band of 20–40 people, while
real foragers live in bands of about 28 adults (Hill et al. 2011) nested in mixing networks of hundreds; between-band
contact among random Ache adult pairs runs at about 0.20–0.30 a year (Hill et al. 2014, full text); band composition is
stable "over months but not years"; and models and experiments find that **partly connected** groups accumulate culture
best (Derex & Boyd 2016; Derex, Perreault & Boyd 2018; Migliano et al. 2020; Cantor et al. 2021), with the caveat that
the benefit depends on how learners choose whom to copy (Leite et al. 2026, preprint; Thompson et al. 2022).

## What ACL already has (read-only reading of `world._make_founders`)

- Founders are split into `min(4, founders / 4)` bands, **each started on its own island** ("so they cannot meet until
  someone works out how to cross the water"), or far apart on the largest island if there are too few islands.
- Today: **4 bands of 5**. In WS1's 80-founder arms: **4 bands of 20** (the code caps the number of bands at 4).
- So ACL is already "multi-band" at the start. What is unknown is **whether its bands ever meet**, and the record so
  far (GF1: groups hardly mix; P2: the unpartnered rarely search; the book's "Two Peoples Who Never Met") suggests
  they mostly do not.

## Two stages (each with its own freeze and sign-off)

### Stage A — MB1a: do ACL's bands meet? (read-only; no change to ACL)

Replays of existing worlds with a read-only observer, measuring between founding-band lineages (a person's band of origin
is their mother's founding band, by descent; founders keep their own):

1. **Meeting:** per pair of adults from different lineages, the probability per year of being within sight of each
   other at least once; set beside the Ache benchmark of 0.20–0.30 per pair-year for common activities (and the
   Hadza, 2–5 times lower). Hill et al. measured interaction, not sight; ACL's "within sight" is an upper bound on it.
2. **Interacting:** the same for talking, giving food, courting.
3. **Pairing:** share of all couples whose partners come from different lineages; and how many worlds ever form one.
4. **Learning:** share of know-how (recipes) that crossed between lineages (taught to, or learned by watching, someone
   of another lineage).
5. Population beside each; how many lineages survive; how these change over the 120 years.

**Worlds:** control worlds (F1's 64 seeds; discovery 501–516 + 601–616, holdout 811–818 + 1101–1124), and, once WS1 is
reported, WS1's 80-founder worlds (P, LP) on their own seeds, so that bands of 20 can be compared with bands of 5.

**Reading rule (draft):** "bands meet like forager bands" if between-lineage meeting per adult pair-year is at least
0.05 (the low end of the Hill et al. range for any common activity) in discovery and holdout; "bands are effectively
closed" if below 0.005 (ten times lower); otherwise "rarely". The thresholds are a reading of a measured benchmark,
labelled as such.

### Stage B — MB1b: does dividing the same people into more, smaller bands change survival and culture? (only if Stage A
shows bands meet at least "rarely"; a separate design, frozen separately)

At fixed land and people (80 × 80 tiles, 80 founders: WS1's LP, already run, as the reference arm), vary only how the
founders are divided:

| arm | founding bands | band size | note |
|---|---|---|---|
| LP (WS1) | 4 | 20 | today's rule; results already exist |
| B8 | 8 | 10 | |
| B16 | 16 | 5 | today's band size, many more bands |
| sham | 4 | 20 | one extra random draw |

This needs one new **world setting**, `founding_bands` (default: today's rule, which must reproduce the control world
exactly), because the code caps bands at 4. The band sizes span the range Hamilton et al. (2007) report for dispersed
groups (geometric mean 15.6); they are operational choices, labelled as such. **Nothing about meeting, visiting or
marriage is added**: whether the bands meet, mix and learn from each other is left to the people, which is the point.
Outcomes: extinction (as in every study), between-lineage meeting, pairing and learning (Stage A's measures), and
culture measures from the research report (a technique registry counting a technique only once it has persisted and
been used; each learner's effective learning pool per skill).

## Dependencies (why MB1 waits)

1. **WS1** (running): if the 80-founder worlds already survive much better, MB1b asks *how* the division matters; if they
   do not, Stage A asks whether that is because their bands never meet.
2. **AA1** (next): two of its shortcuts act directly on between-band contact. **A1** (corner crossing) could join islands
   meant to be separate; **A5** (people know where absent loved ones are) could hold families together across distance.
   Stage A must be read knowing their size.
3. Stage A uses no new code in ACL's world; Stage B adds one setting and needs its own zero checks.

## What MB1 cannot show

What the right number or size of bands is for real people; ACL's tiles have no kilometre scale (N10). It shows whether,
in ACL, bands meet, and whether dividing the same people differently changes their fate.

## Decisions for the creator

1. Stage A first, read-only (recommended), or go straight to Stage B?
2. Stage A's reading thresholds (0.05 and 0.005 per adult pair-year, from Hill et al.'s range), or others.
3. Include WS1's 80-founder worlds in Stage A (recommended), or control worlds only.
4. Order: after AA1 (recommended, because A1 and A5 touch contact), or alongside it.

## Assistant's prior (written before any run; not a prediction to test)

Stage A: bands are effectively closed in 20-founder worlds (well under 0.005 per pair-year between lineages after the
first generation), and only "rarely" meet in 80-founder worlds; cross-lineage couples are rare. If so, the multi-band
structure ACL already has does nothing, and the open question becomes what lets real bands meet: daily forays and camp
moves (Wood et al. 2021; Lewis et al. 2014), visiting, and Lévy-like search, each needing its own evidence review.
Held loosely.
