# MB1 — Many bands, one people: do ACL's bands meet, and does how a people is divided matter? (Stage A SIGNED OFF and frozen as `MB1a-frozen`; Stage B remains a draft)

**Signed off by the creator (October 2026):** Stage A first, read-only; after AA1; including WS1's 80-founder worlds; reading
thresholds as drafted (0.05 and 0.005 per adult pair-year). Stage B is not designed or frozen; it is decided only after
Stage A is reported. Nothing has been run.

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

## Decisions (taken by the creator at sign-off: Stage A first; after AA1; include WS1's worlds; thresholds as drafted)

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

## Stage A operational details (fixed at freezing, before any run)

- **Worlds.** Control: F1's 64 seeds, control code, 120 years; discovery 501–516 and 601–616, holdout 811–818 and
  1101–1124. WS1's 80-founder arms, replayed with WS1's code copy and settings (`code_p2`, every setting off; P = 40 × 40,
  LP = 80 × 80): discovery seeds 3001–3032, holdout 3033–3064 (a subset of WS1's 256, because an 80-founder world takes
  10–20 minutes; the subset is fixed now). Every replay must reproduce its saved WS1 or F1 populations exactly; one that
  does not is a hard stop.
- **Lineage.** Each founder's founding band is read at week one (the founders who start with ties to each other, as in
  WS1's manipulation check). Everyone born later takes their mother's lineage.
- **Meeting.** Each week, for every pair of living adults (16+) of different lineages, whether they are within
  `perception` (4 tiles) of each other. Per pair-year: the probability that a pair meets at least once in a year,
  averaged over all such pairs and years in a world. **Interacting:** the same, counting weeks in which one chose to
  talk to, give to or court the other (from the world's events).
- **Pairing.** Couples formed during the run whose partners are of different lineages, as a share of all couples formed.
- **Learning.** Recipes learned (taught, or learned by watching) from someone of another lineage, as a share of all
  recipes learned from others (from the world's teaching and learning events; if the events do not name the source,
  this measure is reported as not measurable, not estimated).
- **Reading (frozen):** per arm, the median across worlds of the between-lineage meeting rate per adult pair-year:
  ≥ 0.05 = "bands meet like forager bands"; < 0.005 = "bands are effectively closed"; otherwise "rarely". A reading
  stands only if discovery and holdout agree. Worlds in which only one lineage is left are reported separately (no
  between-lineage pairs exist there).
- **Observer:** read-only, verified by state hash (with and without it) on two seeds per code copy before any run.
- **Order of work:** WS1 (running) → AA1 → MB1a → ID1.

## Correction: what the Hill et al. (2014) benchmark measures (appended 12 October 2026, before any MB1 run; rule 19)

Re-read in full text (PLoS ONE 9(7): e102806; PMC4105570). The benchmark is narrower and less comparable than the text
above says:

- **Who:** random **same-sex** adult pairs drawn from the **whole population** (Ache: adults alive 1965–1970, 351
  interviews, 32 subjects, 88 targets; Hadza: 850 interviews in 22 bands). The pairs are not restricted to people of
  different bands, so "between-band contact among random Ache adult pairs" above is inexact: it is contact among random
  adult pairs, most of whom lived in different bands.
- **What:** yes/no recall ("did target ever ...") over the years both were adults, turned into a yearly probability by a
  model in which elapsed time is the main predictor. "About 0.20 to 0.30 per year" is the Ache range for **conversing,
  sleeping in the same camp, sharing food, and watching tool manufacture**; the Hadza were generally 2–5 times lower;
  rarer activities ran 0.02–0.08.
- **Not comparable with ACL's "within sight":** being within 4 tiles is neither conversation nor camping together. As
  the text above already says, it is an upper bound on contact, so a high ACL rate would not show forager-like mixing,
  but a low one does show its absence.

**What this changes:** nothing in the frozen reading. The thresholds (0.05 and 0.005 per adult pair-year) stay as
registered, labelled as operational cut-offs informed by this range, not as validated biological boundaries. Stage A
will also report the rate restricted to same-sex adult pairs, the subset Hill et al. sampled, as a description beside the
frozen measure, not in place of it.

## Scripts and operational notes (appended 14 October 2026, before any MB1a data; rule 19)

`run_mb1a.py` and `analyse_mb1a.py` written and smoke-tested on a throwaway seed (9301, 5 years; output kept in
`output_mb1a_smoke/`, not data). Nothing in the frozen design changes. Where the frozen text left a detail open, the
most literal reading was taken, written in the runner's header before any data:

- **Lineage** is read from the world as built, before its first week: founders joined by the ties the world gives each
  founding band form one lineage (smoke test: 4 bands of 5, 150 between-lineage adult pairs at the start, as expected).
- **Interacting** ("chose to talk to, give to or court") is read from the world's own read-only record of decisions
  (`week_decisions`), not from events alone, because a courtship that fails leaves no event. Talks and gifts that
  actually happened (events) are reported beside it as a description.
- **Learning** counts `learn` events of kind "taught" and "copied" (watching), which name their source; learning from
  marks ("read") is not learning from a person and is left out. So the measure is measurable, not estimated.
- **Replay check:** decade populations must equal the saved world's (the frozen check, a hard stop); the final week and
  state hash are also compared and reported.
- **Order of running:** after SA1 (the processors are busy until then). First `zero`, then `discovery`; the holdout
  only after the discovery reading is written (`findings_mb1a_discovery.md`).
