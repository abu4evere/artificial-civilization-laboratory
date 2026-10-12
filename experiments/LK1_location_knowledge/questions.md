# LK1 — Does knowing where absent loved ones are keep ACL's worlds alive? (DRAFT for sign-off; not frozen; nothing run)

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
