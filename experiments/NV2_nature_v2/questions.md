# NV2 — Nature version 2: what goes in, and how it is checked (SIGNED OFF and frozen as `NV2-frozen`; nothing built or run)

**The creator's decisions so far:**
- 13 October: "approve last-seen + A1 for nature v2, after BL0" (one change, one record).
- 14 October: include the raft fix and the knowledge-record quirk "only after reviewing their evidence"; keep mortality
  paused until adult deaths are measured. Rule: "keep every change traceable, and don't treat a plausible explanation as a
  proven cause."

**What nature v2 is.** A new, numbered version of ACL's rules. `nature-v1` stays exactly as it is (tagged; code copies kept);
**every result so far stays on v1**, and is never re-run or re-read under v2. v2 is the version future studies start
from, once it is built, checked and signed off.

## The candidates and their evidence

| # | change | status | evidence (what was measured; nothing assumed) |
|---|---|---|---|
| 1 | **Last-seen memory replaces A5** (walk to where an absent loved one was last seen, not to where they are now) | **approved** | AA1 measured A5 (~30% of go-to moves, a channel nobody wrote); LK1 tested the replacement on 256 worlds: no meaningful effect on survival, partner finding or births; families apart more. Passes T1–T4 (LK1's freeze). |
| 2 | **A1 fix** (water touching only at a corner blocks a diagonal step) | **approved**; built on branch `nature-v2-a1` (commit `5c612d1`, with a test) | AA1: corner crossings were 83% / 30% of water crossings, concentrated in one world in three (a hidden land bridge nobody intended). |
| 3 | **ST1 fix** (a float that breaks at sea puts its owner ashore half-drowned, as the code already does when a float is missing) | **for review** | ST1 (`experiments/ST1_stranded_at_sea/finding.md`): found by the property tests; a raft that breaks after the walk strands its owner on water against Rule 3: **22 person-weeks in 1,291,054** (13 of 40 worlds; never more than one week). Same in every arm of every study. A breach of a written rule, small. |
| 4 | **Knowledge-record quirk** (record a first-baked thing's properties as a copy, not the item itself) | **for review** | ID1's trace (`experiments/ID1_memory_identity/questions.md`, 14 October): the record follows one item's wetness and contents; checked week by week on one world: **no person's behaviour differs**; only the record, and so a saved-and-loaded world is not bit-exact. A bookkeeping flaw, not behaviour. |
| — | Mortality scale | **paused** (creator) | SA1's evidence note: ACL's illness risk is 5.4 × the forager average at every age (Gurven & Kaplan 2007). Waits for a measurement of ACL's total adult mortality. |

**Recommendation on 3 and 4** (the evidence above is what exists; nothing more can be measured about them without
fixing them):
- **ST1: include.** It breaks a written rule (Rule 3). It is rare, so its effect on outcomes is expected to be nil, and v2's
  comparison will show that rather than assume it.
- **Knowledge record: include.** It changes no behaviour (measured), and fixing it makes saved worlds exact, which every
  copy-based study (ID1) relies on. Of the four, it is the only one that should leave every world bit-identical in
  behaviour: the v2 comparison can check exactly that.

## How v2 is built and checked (each step traceable)

1. **One branch, one commit per change**, each with its own test (A1's exists). The approved order: 1, 2, then 3 and 4 if
   approved.
2. **Zero checks per change:** with each change switched off by a setting, the code equals `nature-v1` exactly (state
   hash, two seeds, 20 years). With 4 on and the others off: people's choices and events identical to v1 over 120 years
   on two seeds (only the knowledge record may differ).
3. **New reference hashes** for v2 (`tests/reference_hashes.json`), CI green on windows-2022.
4. **A frozen comparison, v1 against v2**, before v2 is used: 256 new seeds, 20 founders, 120 years, arms v1, v2 and a
   sham; extinction (paired sign test, bootstrap interval, as every study) and BL0/LK1/MB1a's main measures described.
   Its purpose is to **measure** what v2 changes, not to make v2 "better": any result is reported, and v2 is not tuned.
   (A separate questions file, frozen before it runs.)
5. **The creator signs off v2** after reading that comparison. Only then do studies move to it.

## Decisions for the creator

1. Include **ST1** (recommended) and the **knowledge-record fix** (recommended)?
2. The comparison as described (256 new seeds; v1, v2, sham), or smaller?
3. Order: build v2 now, while TC1 is decided (TC1 runs on v1 and does not depend on v2), or after TC1.

## Sign-off (14 October 2026)

The creator: "**Nature v2 — include both fixes: the raft fix and the knowledge-record fix. Keep mortality paused. Make
each change in a separate commit. Run zero checks and verify the new reference fingerprints. Compare v1 and v2 on 256
new seeds before moving any study to v2. Keep all historical results tied to v1.**" Order: after TC1 ("Nature v2
validation second"). And: "don't start a run until its configuration and success criteria are saved; if results
contradict expectations, report them rather than changing thresholds afterward."

## Operational details (fixed at freezing, before any code)

**What "v1" is, precisely.** Every result so far ran on the **control code** (`code_e13r`, `anticipation_weight = 1.0`)
and code copies proven equal to it. The live package `acl/` (tag `nature-v1`) has its own reference fingerprints, which
differ from the control code's (`tests/reference_hashes.json`: "acl" against "control"). So v2 is built **from the
control code**, the version every finding stands on.

**Code `code_v2`:** a copy of `code_p2`'s acl package with every P2/MC1/HB1 setting off (it equals the control code
then, as P2's, WS1's and SA1's zero checks showed, and it already holds `sham_draw`). Four new settings, **one commit
each**, each defaulting to v1's behaviour, so that all four off is exactly v1:

| setting | v1 (default) | v2 | the change |
|---|---|---|---|
| `loved_location` | `"current"` | `"last_seen"` | LK1's code, copied unchanged (without AA1's logging) |
| `corner_block` | `0` | `1` | the A1 fix, the same lines as branch `nature-v2-a1` (`5c612d1`) |
| `ashore_if_float_breaks` | `0` | `1` | ST1: at the end of a person's action, if they stand on water with nothing that floats, they struggle ashore half-drowned, exactly as `_over_water` already does when a float is missing |
| `knowledge_copy` | `0` | `1` | the record of a first-baked thing gets a deep copy of the item at that moment, not the item itself |

**Zero checks (hard stops), before any comparison run:**
1. All four off: state hash equals the control code (seeds 501 and 601, 20 years).
2. Each change alone on: the world differs from v1 (it acts), except `knowledge_copy`, which must leave every person and
   event identical to v1 over 20 years (only the knowledge record may differ), checked week by week on the same seeds.
3. **New reference fingerprints** for v2 (all four on) on seeds 11 and 501 (5 years, as the existing references), added to
   `tests/reference_hashes.json` as "v2" beside "acl" and "control", with a test; CI green on windows-2022.

**The comparison (v1 against v2):**
- **256 new seeds, 4601–4856**, 20 founders, 40 × 40, 120 years. Arms: **v1** (all off), **v2** (all on), **sham** (v1 with
  `sham_draw = 1`). 768 worlds, about 10 hours.
- **Observer:** F1's probe (populations, births, deaths, decisions blocked for want of a partner), read-only (zero check
  with and without it).
- **Primary: extinction**, v2 against v1, paired by seed (exact sign test; effect with a 95% bootstrap interval, 10,000
  resamples, `random.Random(2026)`), half of F2's effect (0.117) as the yardstick, as LK1 and WS1:
  - p < 0.05: "**v2 changes survival**" (its direction and size reported).
  - p ≥ 0.05 and the interval excludes ±0.117: "**no meaningful effect on survival**".
  - otherwise: "**unresolved at this sample**".
- **Described:** median population at years 60 and 119; births per woman-year; decisions blocked; the sham against v1 (must
  be quiet; if not, every reading carries the caveat).
- **What it decides:** nothing automatically. The creator reads it and signs off v2 (or not) before any study moves to it.
  The live package is updated to v2 only after that sign-off.

**The assistant's prior (frozen; held loosely):** no meaningful effect on survival (LK1 found none for last-seen; A1 acts
in one world in three; ST1 is 2 in 100,000 person-weeks; the knowledge fix changes no behaviour). Births a little lower
(families apart more, LK1).

## Build record (appended 14 October 2026, before any comparison data; rule 19)

- `code_v2` built from `code_p2` in five commits: the base copy, then one per change (last-seen `d47598c`, A1 `634f101`,
  ST1 `9e73671`, knowledge copy `4bcd3e0`). Last-seen is LK1's code without its logging (diffed line by line); A1 is the
  lines of `nature-v2-a1`.
- Reference fingerprints for v2 (all four on, seeds 11 and 501, 5 years) added to `tests/reference_hashes.json` with
  `test_nature_v2_replays`; all three reference tests pass locally.
- `run_nv2.py` and `analyse_nv2.py` written and smoke-tested on a throwaway seed (9701, 10 years; `output_smoke/`, not
  data). The analysis reports births and blocked decisions with F1's own pooled-rate function, as SA1 does, and shows
  no outcome if the run is not valid.
- The comparison run waits for the zero checks and for TC1 to finish (the creator's order).
