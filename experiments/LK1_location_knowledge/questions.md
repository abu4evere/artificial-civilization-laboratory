# LK1 — Does knowing where absent loved ones are keep ACL's worlds alive? (SIGNED OFF and frozen as `LK1-frozen`; nothing run)

**Asked by the creator (12 October 2026), after AA1:**
- Test A5 separately, as a controlled experiment, keeping the current version as the control.
- Compare current location knowledge with last-seen memory.
- Freeze predictions before running.
- Measure partner-finding success, separation time, births and extinction, and track A6c.
- "Identify the shortcut, measure its consequences, and only then change the world."

**Why it matters.** AA1 found that about 30% of all "go to" moves aim at a loved one the person cannot see, toward where
that person is *now* (`mind._far_people` reads `q.loc` with no limit of sight or memory). No rule says people may know
this. N8 found evidence that real people remember others, but none that they track where they are. Partner finding is the
mechanism behind extinction in every study since F1, so this shortcut could be holding worlds together, or not.

## What the code does today (read from the control copy, `code_e13r`)

For each of up to three loved ones (partner, mother, father, children, best friend) who are alive and beyond `reach` (3
tiles), a person may choose "join" toward **that loved one's current tile**, with a pull that grows with loneliness,
sociability, kinship and affection (`mind.decide`, "Go back to family and friends when they are out of reach").

## Arms (one new world setting in a code copy; default = today's world exactly)

| arm | what a person walks toward, for an absent loved one | |
|---|---|---|
| **C** control | the loved one's **current** tile (today; `nature-v1`) | — |
| **M** last-seen memory | the tile where the person **last had that loved one in sight** (within `perception`, 4 tiles) | the new setting |
| **S** sham | as C, plus one extra random draw | as in every study |

**M, operationally (draft):**
- Each week, every person records, for each of their loved ones in sight, that loved one's tile and the week. This record
  is held only when the setting is on, so the default world is unchanged.
- An absent loved one pulls toward the **remembered** tile, with the same pull as today.
- On reaching that tile without seeing them, the memory is spent: it no longer pulls until they are seen again.
- No memory, no pull: a loved one never seen since birth (or since the setting began) does not pull.
- Nothing else changes. A6c (partner search sees `perception + 2`), A6a and A6d stay as in C. Hearsay about where people
  are is not added. Whether stories should carry locations is a separate question.

**Both arms run on `nature-v1`** (the preserved version; A1 not fixed in either), as the creator ordered: "run the A5
experiment against the preserved version".

## Measures (population beside every measure, rule 18)

- **Rule 14 first:** C's extinction share.
- **Primary: extinction**, as in every study (not reaching year 120 with someone alive).
- **Secondary** (the creator's list):
  1. **Partner-finding success:** pairings per eligible single adult-year; and the median weeks from becoming an eligible
     single to pairing, among those who pair.
  2. **Separation time:** for every partner pair, and every mother–child pair under 16, the share of weeks spent out of
     each other's sight (beyond `perception`); and the median length of a separation spell.
  3. **Births** per woman-year.
  4. **A6c:** the share of partner-search moves aimed beyond sight. A6c is untouched, but people may lean on it more
     when A5 is gone.
- **Manipulation check:**
  - In M, "join" moves toward an absent loved one's current tile are **0** by construction, and moves toward a remembered
    tile are counted.
  - In C, AA1's A5 share (~30%) is reproduced.
- **Zero check:** the code copy with the setting off equals the control code (state hash, two seeds, 20 years). Hard
  stop otherwise.

## Outcome rule (as WS1 and MC1-L, for comparability)

M against C, paired by seed, exact two-sided sign test on worlds that differ; the paired difference in extinction share
with a 95% bootstrap interval (10,000 resamples, `random.Random(2026)`):

- **Fewer extinctions, p < 0.05:** "knowing where loved ones are *harms* survival". Unexpected, so it is examined
  read-only.
- **More extinctions, p < 0.05:** "current-location knowledge **holds worlds together**". Its size is the estimate of how
  much A5 props up survival.
- **p ≥ 0.05, and the interval excludes half of F2's effect:** no meaningful effect on survival.
- **p ≥ 0.05 otherwise:** unresolved at this sample.

The secondary measures are reported with paired Wilcoxon tests and intervals, described, not thresholded. S against C
should not reach p < 0.05; if it does, every reading carries that caveat.

## Worlds and cost (draft)

- **256 new seeds** (4001–4256), 20 founders, 40 × 40, 120 years, as WS1's control arm. Today's 20-founder world is the
  one every earlier result comes from, and the one in which partner-finding fails.
- Cost from WS1's C arm (~3 minutes a world): 3 arms × 256 ≈ 768 worlds ≈ **10 hours** on four workers.
- **Feasibility pilot first** (rule 12): the manipulation check on four throwaway seeds, 10 years, before the main run.
  Run times only.

## Predictions (to be frozen; the assistant's, held loosely)

- Separation time **rises** in M (people lose track of each other).
- Partner-finding success **falls slightly**: A5 mostly concerns existing ties, not new partners.
- Births **fall** a little.
- A6c's share **rises**.
- Extinction **rises**, but less than half of F2's effect (so the reading is "no meaningful effect" or "unresolved").
  Held loosely: partner finding is what kills worlds, but A5 mostly keeps existing couples and families together.

## What it cannot show

- Whether real people track loved ones. That is evidence, not simulation (N8: not shown).
- What happens in 80-founder worlds (a later question, if the creator wants it).
- Whether the other information shortcuts matter. A6a and A6d get their own read-only diagnostics.

## Decisions for the creator (before freezing)

1. **Last-seen rule** as drafted: memory spent on arrival; no hearsay; partner, parents, children, best friend.
2. **Seeds:** 256 (as WS1), or 128 (half the time; large effects only).
3. **World:** 20 founders, 40 × 40 (recommended: the world every earlier result comes from), or also 80 founders.
4. **Order:** before MB1a, or after it. MB1a is read-only and doesn't depend on A5. But A5 changes how MB1a's "meeting"
   should be read, because people walk toward absent loved ones across bands.
5. **Thresholds** as above (the same as WS1).

## Sign-off (12 October 2026)

The creator: **"adopt Law 126 as drafted, then freeze LK1."** Law 126 (World Bible v8.2) was adopted first, so LK1 is the
first test of its failed-rule path: A5 is a known compromise; it has been measured (AA1); it is now tested against
a replacement, with `nature-v1` preserved. The decisions above were not answered one by one, so **each is frozen as
recommended in this draft**:

1. Last-seen rule as drafted (operational details below).
2. **256 seeds** (4001–4256).
3. **20 founders, 40 × 40**, only.
4. **Order of running:** not part of the design; the creator sets it before the run. (Recommended: before MB1a.)
5. Thresholds as above (the same as WS1).

**Law 126's checks before freezing:**
- **The rule under test.** A5 was measured by AA1, and it breaks Law 12.
- **The replacement rule.** Walking toward where one last saw someone passes the four tests:
  - T1: it is a capacity (memory of places), not a content.
  - T2: remembering where one last saw someone is human-universal by any account; no number is set by it.
  - T3: it names no outcome.
  - T4: its only channel is the person's own sight.

## Operational details (fixed at freezing, before any code)

- **Code copy `code_lk1`.** It starts from `experiments/P2_outward_search/code_p2`, with every P2/MC1 setting off. That
  copy has `sham_draw` and was zero-checked against the control code for WS1. To it are added:
  - AA1's logging hooks, unchanged from `code_aa1`, which write to a log held outside the world's state;
  - **one new setting**, `loved_location` (`"current"`, the default, which is today's world; or `"last_seen"`).
- **Arms:**
  - **C:** `loved_location="current"`.
  - **M:** `"last_seen"`.
  - **S:** `"current"` and `sham_draw=1`.
- **Loved ones:** as `mind._far_people` defines them: partner, mother, father, children, best friend; at most three
  pulled toward, as today.
- **In M, each week, before the person decides:**
  - **Memory.** For each loved one within `perception` (4 tiles) of the person, record that loved one's tile and the
    week. The record lives in the person's state, so it is saved and restored. It is held only in M; in C and S it does
    not exist, so they equal today's world.
  - **Seen now.** A loved one **in sight** is treated exactly as today: no pull if within `reach`, otherwise a pull
    toward their current tile.
  - **Not in sight, memory unspent.** The pull is toward the **remembered tile**, with today's pull formula unchanged.
  - **Memory spent.** If the remembered tile is within the person's `perception` and the loved one is not in sight, the
    person can see the spot is empty: the memory is **spent** and pulls no more until the loved one is seen again.
  - **No memory, or a spent one:** no pull.
- **Zero checks (hard stops):**
  - `code_lk1` with `loved_location="current"` equals the control code (`code_e13r`, `anticipation_weight=1.0` as every
    control): state hash, seeds 11 and 501, 20 years.
  - Its logging leaves the hash unchanged (with and without the log).
- **Manipulation check (pilot, four throwaway seeds 9201–9204, 10 years):**
  - in M, zero "join" moves toward an out-of-sight loved one's current tile;
  - some moves toward remembered tiles;
  - in C, AA1's A5 share reproduced to within its holdout interval (27–31%).
- **Measures, operationally (read-only, from the world's events and the log):**
  - **Eligible single:** alive, 16 or older, unpartnered.
  - **Pairings:** `pair` events, per eligible single-year.
  - **Weeks to pairing:** from becoming an eligible single to the `pair` event, for those who pair.
  - **Separation:** for each living partner pair and each living mother–child pair (child under 16), the share of
    weeks the two are beyond `perception` of each other, and the median length of such spells.
  - **Births** per woman-year (women 16–45).
  - **A6c:** AA1's measure, unchanged.
  - **Population** beside every measure.
- **Analysis script** written and smoke-tested before any main-run data, as for every study.

## Pilot result and a proposed amendment (12 October 2026, before any main-run data; rule 19; APPROVED, see Amendment 1 below)

**Zero checks: PASS** (`output/zero.txt`). With `loved_location="current"`, the copy reproduces the control world, with
and without observers, on seeds 11 and 501; arms M and S differ from it.

**Pilot (`output_pilot/manipulation.txt`), first attempt: FAIL on checks 1 and 3.**

1. **Check 1** (M: zero moves toward an out-of-sight loved one's current tile) showed 276. The cause was **a labelling
   bug, not the rule**. A move toward a remembered spot was labelled "current" whenever the loved one had not moved since
   being seen, because the label compared positions instead of recording where the target came from. Fixed: each move is
   labelled by its source ("now" or "memory"). Afterwards: **0**, and 558 moves toward remembered spots
   (276 + 282: the same moves, relabelled). Zero checks re-run after the fix: PASS. The fix touches only the label,
   which is outside the world's state.
2. **Check 2** (M: some moves toward remembered spots): PASS.
3. **Check 3** (C: A5 share within AA1's holdout interval, 27.2–31.4%) gave **25.0%** (1,079 of 4,310). **The check was
   mis-specified at freezing.** It compares a 10-year pilot on four throwaway seeds with an interval measured over 120
   years on other seeds; the share in a world's first decade need not equal its 120-year share. What the check was meant
   to show, that C measures A5 exactly as AA1 did, was tested directly instead. C, run on AA1's seed 601 for 120 years,
   **reproduces AA1's counts exactly**: go-to moves 11,872; toward loved ones 4,567; beyond sight 2,989; partner search
   329 / 151; crossings 170; gifts 17,226. The test output was not kept as main-run data.

**Proposed amendment (for the creator's sign-off; the main run does not start until then):** replace check 3 with
"**C reproduces AA1's audit counts exactly on an AA1 seed (601, 120 years)**". This is already shown, and it is stricter
than the original check: equality, not an interval. Nothing else changes: not the arms, seeds, measures, outcome rule,
nor any threshold.

## Amendment 1 (approved by the creator, 12 October 2026, before any main-run data; frozen as `LK1-amend1`)

**The change.** Pilot check 3 is replaced.

- **Original check 3 (SUPERSEDED, kept in the record):** "in C, AA1's A5 share (~30%) is reproduced to within its
  holdout interval (27.2–31.4%)", on the pilot's four throwaway seeds over 10 years.
  - **Its result:** **25.0%** (1,079 of 4,310), **outside** the interval, so the pilot read **FAIL**. Recorded in
    `output_pilot/manipulation.txt`, which is kept unchanged.
- **Replacement check 3:** "**C reproduces AA1's recorded audit counts exactly on an AA1 world (seed 601, 120 years)**".
  - **Its result:** exact equality on every count compared: go-to moves 11,872; toward loved ones 4,567; beyond sight
    2,989; partner search 329 / 151; crossings 170; gifts 17,226. (The run was a check, not main-run data; its output
    was deleted after comparison.)

**Why.** The original compared **incompatible time windows**: a 10-year pilot on other worlds against an interval
measured over 120 years. A world's first decade need not share its 120-year A5 share. The replacement compares the
same world over the same 120 years.

**What the replacement shows, and what it does not.** It shows that C reproduces AA1 on that world: control-arm
fidelity. It does **not** prove identical behaviour on every seed, nor the validity of every LK1 measure. That rests on:

- the independent zero checks (seeds 11 and 501, with and without observers: PASS);
- the main-run validity checks in `analyse_lk1.py`:
  - one code fingerprint in every world;
  - **the manipulation verified in the main run itself**: M's go-to moves toward an out-of-sight loved one's current
    tile must total **0**, and moves toward remembered tiles must be **above 0**.

  If any of these fails, the run is reported **not valid** and no outcome is read.

**Also recorded.** The first pilot attempt failed check 1 (276 moves), which was traced to a labelling bug and fixed.
The file holding that first attempt was overwritten when the pilot was re-run after the fix; its numbers are kept in the
section above.

**Code revision frozen for the main run:**
- commit `a725702`;
- `code_lk1` fingerprint `765312576e42ffba6a3bee469208ced06f749b72c86db8577ad489cc23525d22`;
- runner `run_lk1.py` and analysis `analyse_lk1.py` as committed at that revision.

**No further changes to the design, code or analysis once main-run results begin.** If a validity check fails, the run is
stopped and reported, not adjusted.

