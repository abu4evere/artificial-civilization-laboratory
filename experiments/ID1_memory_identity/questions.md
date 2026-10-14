# ID1 — What makes an ACL person who they are? (SIGNED OFF and frozen as `ID1-frozen`)

**Signed off by the creator (October 2026):** window 26 weeks; restore after 26 weeks; 128 focal people in F1's 64 control
worlds (two each); run after WS1 finishes. Nothing has been run.

**Asked by the creator (October 2026),** from the idea "is memory the foundation of identity?". In ACL a person is made of
separate parts, each a different kind of state in the code. ID1 asks which parts make a person behave as **that** person.
It changes no rule of nature: it works on **copies** of worlds, never on ACL's own worlds, and the copies are discarded.

## What an ACL person is made of (from `acl/person.py`)

| part | in the code | what it is |
|---|---|---|
| **Temperament** | `genes` | eight inborn traits (curiosity, kindness, temper, …), fixed for life |
| **Habits** | `q` | the 32 × 19 table of learned habits (the brain scan's 608 connections) |
| **Memories** | `memories` | remembered events: births, deaths, gifts, attacks, pairings |
| **Relationships** | `rel` | affection, trust, familiarity, grudges toward each other person |
| **Know-how** | `recipes`, `itemval`, `skills` | what they can make, how much they value it, how skilled they are |
| **Beliefs** | `beliefs`, `expect`, `heard`, `records` | what they believe about practices and seasons, what they were told, whom they trust as a source |
| **Places** | `places`, `springs`, `sightings`, `shores` | where life has been good, water, animals, land across the sea |

The body (age, health, food, position) and family ties (partner, children) stay the focal person's own throughout.

## The method

Worlds are fully deterministic: a snapshot holds every number, including the random-number generator's state. So a
world can be copied and run forward twice from the identical moment. In one copy nothing is touched (the **original**);
in the other, one part of one person is replaced (the **swap**).

- **Focal person and donor:** in a control world at a fixed year, pick a grown person (focal) and another grown person of
  the same sex and similar age (donor). The focal person receives the donor's part.
- **Arms per focal person:** swap one part at a time (seven arms), swap everything except temperament (one arm), and a
  **sham**: the world perturbed by one random draw with the person untouched. The sham measures how much a person's
  behaviour changes just because the world's future has changed. Any change to any person makes everyone's futures
  diverge, so the sham is the yardstick.
- **Restore:** after the swap has run for a while, put the focal person's own parts back. Does their behaviour return?

## Questions

1. **Which parts move a person's behaviour away from who they were?** For each part: how far the focal person's actions
   drift from the original copy, compared with the sham.
2. **Which parts make them behave like the donor?** Do they become more like the donor than like themselves?
3. **Is temperament enough?** With everything swapped except temperament: do they become the donor, or stay themselves?
4. **Does restoring bring them back?** After restoring, does the behaviour return to the original, or have the weeks
   lived in between already changed them?

## Measures (definitions for the creator to approve)

- **Behaviour:** how often the person chooses each of the 19 actions over a window of weeks.
- **Drift:** difference between two people's action mixes (Jensen–Shannon divergence, 0 = identical, 1 = completely
  different), focal-swapped vs focal-original, against the same measure in the sham.
- **Pull toward the donor:** whether the focal-swapped person's action mix is closer to the donor's original mix than to
  their own original mix.
- Beside each: the world's population and the focal person's age, partner and survival through the window.

## Decisions (taken by the creator at sign-off: 26-week window; restore at 26 weeks; 128 people in 64 worlds; after WS1)

1. **Window:** behaviour over (a) 13 weeks, (b) 26 weeks, or (c) 52 weeks after the swap. Longer shows lasting effects but
   lets the world's chaos grow.
2. **Restore after:** (a) 26 weeks, or (b) 52 weeks.
3. **Sample:** focal persons in (a) 64 control worlds, 2 each (128), or (b) 32 worlds, 2 each (64). Runs are short (weeks,
   not 120 years), so either is cheap.
4. **Discovery and holdout (rule 15):** half of the worlds first, the reading written down, then the other half.
5. **When:** while WS1 is running (it would slow WS1 a little), or after WS1 finishes.

## What it cannot show

How human identity works. ACL's "memory" and "habits" are far simpler than a human mind. ID1 shows which parts of an
**ACL** mind drive behaviour, and whether swapping them changes who a person behaves as.

## Assistant's prior (written before any run; not a prediction to test)

Habits and temperament will matter most; memories (episodic) the least, because in the code memories mostly colour
feelings, not choices; restoring will mostly bring people back, but not completely, because the weeks lived in between
change their habits too. Held loosely.

## Operational details (fixed at freezing, before any run)

- **Worlds and moment:** F1's 64 control seeds, control code (`code_e13r`), the world as it stands at the start of
  **year 20** (most worlds are still alive then; F1's dying worlds mostly die later). A world with no eligible pair is
  skipped and reported; the sample is then smaller, never topped up from other seeds.
- **Focal people and donors:** chosen with `random.Random(seed)` among living people aged 20–45: two focal people per
  world, each with a donor of the same sex, within 10 years of age, not kin (kinship 0) and not their partner. The two
  focal people in a world are different people, and neither is the other's donor.
- **Runs per focal person (each 52 weeks from the same snapshot):** the **original** (nothing touched); the **sham**
  (one extra random draw at the moment of the swap, person untouched); **eight swap arms** (temperament, habits,
  memories, relationships, know-how, beliefs, places, and everything except temperament). In every swap arm, the swapped
  part is **restored at week 26** to the focal person's own values as they were at the moment of the swap. References
  to the focal person inside swapped relationships or memories are left as they are (the donor's view of the focal
  person becomes the focal person's view of themselves; this is recorded as a known oddity, and it applies to
  relationships only).
- **Behaviour window:** weeks 1–26 (swapped) and weeks 27–52 (restored). Action mix = share of weeks spent on each of the
  19 actions. Weeks in which the focal person is dead are excluded; a focal person alive for fewer than 13 weeks of a
  window is dropped from that window, and the count is reported.
- **Drift** = Jensen–Shannon divergence (base 2) between the arm's action mix and the original copy's, same window.
- **Q1 (which parts move a person):** for each of the eight arms, paired Wilcoxon signed-rank test of arm drift vs sham
  drift in weeks 1–26 (two-sided); Holm adjustment over the eight; **"moves the person"** if Holm-adjusted p < 0.05 and
  the median paired difference is positive.
- **Q2 (pull toward the donor):** for each arm, the focal person counts as pulled if the arm's action mix (weeks 1–26)
  is closer (JSD) to the donor's original-copy mix than to the focal person's own original-copy mix; exact sign test
  against the same count in the sham; Holm over eight.
- **Q3 (is temperament enough):** read from the "everything except temperament" arm under Q2: pulled toward the donor
  (p < 0.05) = **the person follows their parts, not their temperament**; not pulled and Q1 significant = **changed, but
  not into the donor**; neither = **temperament holds them**.
- **Q4 (does restoring bring them back):** for each arm that moved the person in Q1, weeks 27–52 drift vs sham drift
  (paired Wilcoxon, Holm): p ≥ 0.05 = **no detectable lasting change** (not proof of full return); p < 0.05 = **a
  lasting change**: the weeks lived with the other part changed them.
- **Rule 15:** discovery = the 32 worlds 501–516 and 601–616; reading written down; then holdout = 811–818 and
  1101–1124. A reading stands only if the holdout agrees in direction and significance.
- **Hard stops:** the original copy reproduces the uncopied control run exactly (state hash at week 52); the sham and
  every swap differ from it; code fingerprint unchanged.

## Correction (appended 12 October 2026, before any ID1 code or run; rule 19)

The habit table has **17 actions, not 19**: `acl/person.py` lists rest, forage, hunt, gather, put, take, make, play,
explore, give, care, talk, court, steal, attack, flee, join. So **Habits** is the 32 × 17 table of **544** values (not
608), and the behaviour measure is the share of each of the **17** actions. The figure 19 came from the brain-scan page,
whose labels were wrong in the same way (corrected on the same day). Nothing else in the frozen design changes: the
measures are defined over whatever actions the code has, and the swaps, sham, people, worlds and tests are unchanged.

## Scripts and operational notes (appended 14 October 2026, before any ID1 data; rule 19)

`run_id1.py` and `analyse_id1.py` written and smoke-tested on a throwaway seed (9401: snapshot at year 2, 8 weeks,
restore at week 4; output kept in `output_smoke/`, not data). Nothing in the frozen design changes. Details the frozen
text left open, written in the runner's header before any data:

- **The original and the sham are run once per world** and serve both focal people: neither depends on who is focal, so
  a second run would be the identical world.
- **Parts** follow the frozen table exactly; fields outside it (puzzles, marks, placements, voyage, the week's thoughts
  and feelings, body, family) stay the focal person's own.
- **Swap and restore** use deep copies; checked directly on the smoke world: after the swap the focal person holds
  independent copies of the donor's values, and after restoring, the person is identical to their own copy. If the
  focal person has died by week 26, nothing is restored.
- **Focal people** are chosen in a fixed, seeded order (the header gives it). A world with only one possible focal
  person keeps its one.
- **Behaviour** is read from the world's read-only record of decisions (the same record MB1a uses).
- **Smoke note:** over the smoke test's 4-week swap one swap (one person's temperament) left the world identical, because
  no choice in those weeks turned on it; over 26 weeks the same swap changed 13 of her 26 actions. In the main run the
  frozen hard stop stands as written: if any swap leaves the world identical after 52 weeks, the run is reported, not
  adjusted.
- **Cost:** about a minute a world; each set (32 worlds) about 10 minutes on four workers. Runs after MB1a.

## Hard stop on the first discovery run, and the fix (appended 14 October 2026, before any ID1 outcome was read; rule 19)

**What happened.** The first discovery run stopped at seed 504: the original copy did not reproduce the uncopied world
at week 52 (the frozen hard stop). Seeds 501–503 had reproduced. No outcome of any seed was read. The outputs of that
attempt are kept unchanged in `output_firstattempt/`.

**Cause: a shared reference in ACL's own code, lost by the copy.** When a person first bakes a kind of clay, the world's
record of that kind of thing (`world.knowledge[sig]["props"]`) is given **the baked item itself**, not a copy of its
properties (`acl/biology.py`, `_baked`, `props=out`). So the record changes whenever that item dries or is filled. The
runner copied worlds through the world's own `to_dict` and JSON, which breaks the shared reference: in the copy the
record stops following the item. On seed 504 the two worlds differed **only in that record** (two kinds of fired clay,
"wet" 1 against 5); people, events and every other part of the world were identical in all 52 weeks (checked week by
week).

**Fix (implementation only; the design is unchanged).** Snapshots are now exact in-memory deep copies, which keep the
shared reference. On seed 504 the original copy then reproduces the uncopied world exactly; the smoke test again
passes. The whole discovery set is re-run with the fixed runner; the hard stop stays as frozen.

**The quirk itself** (not part of ID1): a record that should hold a kind of thing's properties when first made instead
follows one particular item. It changes no person's behaviour (no decision reads it; only measurements and the viewer
do), but a world saved to a file and loaded again is not bit-identical to the one that kept running. Listed for nature
v2, beside ST1, last-seen memory and A1; a fix needs the creator's sign-off and a new version.

## Proposed Amendment 1 (14 October 2026; FOR THE CREATOR'S SIGN-OFF; the holdout does not run until then)

**What stopped the run.** The re-run discovery set (deep-copy snapshots) reproduces the uncopied world in all 31 worlds
with focal people (seed 513 had none and is skipped, as frozen). But the frozen hard stop "the sham and every swap
differ from the original" fails in one place: **seed 511, focal person p00005, the beliefs and places swaps** end in a
world identical to the original.

**Why.** p00005 (aged 40.6) **died in week 3** in the original and in every swap. In the two weeks alive their choices
("care", "care") did not turn on beliefs or places, and death clears both parts (`biology.die`), so the worlds
converge exactly. The swap was applied (checked: the donor's values differ from the focal person's in all eight
fields). This is a real event, not a failed swap, which is what the hard stop was written to catch. The frozen
13-week rule already drops this person from every test (the analysis reports 1 dropped in weeks 1–26).

**Proposed change:** the hard stop "every swap differs from the original" does **not** apply to a focal person who dies
before week 13 (whom the frozen rule already drops from the tests). Every other part of the hard stop stays. Nothing
else changes: not the people, worlds, arms, measures, tests or thresholds.

**Disclosure.** The analysis script prints its tables even when the run is not valid, so the discovery outcome tables
were displayed before this proposal. The proposal does not depend on them: the person it concerns is already excluded
from every test, so **no number in any table changes** under it; only the validity label does. Recorded so the
creator can weigh it. The holdout (811–818, 1101–1124) has not been run.

**If approved:** the discovery reading is written, then the holdout runs. **If not:** ID1 is reported as stopped by
its hard stop, with this explanation.
