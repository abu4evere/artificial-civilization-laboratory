# NV2 — Nature v2 against v1: findings

Frozen as `NV2-frozen`, amended once before any data (`NV2-amend1`, approved 14 October 2026). Table: `results.md`, from
`analyse_nv2.py`. Run: `run_nv2.py run` (log `run_nv2.log`; the PC shut down at 745 of 768 worlds on 16 October; every
saved file was checked whole and the runner resumed the other 23, skipping finished worlds; nothing was re-run or changed).

## Validity

Zero checks PASS (all four changes off = the control code; each change acts; ST1 removes the strandings in the five
worlds where v1 strands someone; the knowledge copy changes no behaviour; the probe is read-only). All 768 worlds present;
one code fingerprint. Sham against v1: p = 0.119 (quiet). **Valid.**

## The frozen reading: no meaningful effect on survival

v1 died out in 97 of 256 worlds (37.9%; rule 14).

| arm | died out (of 256) | saved / lost against v1 | p | effect (v1 − arm) | 95% interval |
|---|---|---|---|---|---|
| v2 | 94 | 39 / 36 | 0.818 | +0.012 | [−0.055, +0.078] |
| sham | 82 | 48 / 33 | 0.119 | +0.059 | [−0.012, +0.129] |

The interval for v2 lies inside ±0.117 (half of F2's effect). **Frozen rule: "no meaningful effect on survival."**

## Described (not frozen readings; population first, rule 18)

| arm | median population, year 60 / 119 | births per woman-year | decisions blocked for want of a partner |
|---|---|---|---|
| v1 | 22 / 14 | 0.129 | 0.568 |
| v2 | 26 / 23 | 0.128 | 0.546 |
| sham | 25 / 26 | 0.133 | 0.550 |

- **Births and partner finding:** v2 equals v1 within what the sham shows chance alone does.
- **Median population at year 119** is higher under v2 (23 against 14), **but the sham is higher by as much (26)**: one
  extra roll of the dice moves this median as far as all four changes. It is not read as an effect of v2.
- **The sham is a warning about the yardstick.** It is quiet by the frozen test, but its interval reaches 0.129, beyond
  the ±0.117 yardstick: at 256 worlds, chance alone can move extinction almost as far as the line used to call an effect
  "meaningful". The reading for v2 stands (its interval is well inside), and future comparisons should keep the sham.

## The assistant's prior, against the result

| prior (frozen) | result |
|---|---|
| no meaningful effect on survival | **right** |
| births a little lower (families apart more, as in LK1) | **not seen**: 0.128 against 0.129, inside chance |

## Reading

The four changes of nature v2 (last-seen memory instead of A5, the corner-crossing fix A1, the raft-stranding fix ST1,
and the knowledge-record copy) do not change whether ACL's worlds survive, nor births or partner finding, beyond what
chance does. v2 removes three channels nobody intended (knowledge of absent loved ones' current place, a hidden land
bridge at diagonal corners, people left on open water) and one bookkeeping flaw, at no measurable cost to the world's
demography. Measuring this, not improving the world, was the purpose; v2 was not tuned.

**What it decides (the creator decides):** whether to sign off nature v2. If signed off: the live package `acl/` moves to
v2, future studies start from `code_v2` with all four on, and every past result stays on v1 (tagged `nature-v1`). Not
in v2: the mortality scale (paused), situation-specific copying (TC1; needs its evidence review).

## Sign-off (16 October 2026)

The creator, after reading this comparison: "**approve nature v2**". Nature v2 is `code_v2` with all four changes on
(`loved_location = "last_seen"`, `corner_block = 1`, `ashore_if_float_breaks = 1`, `knowledge_copy = 1`) on the control
code's settings (`anticipation_weight = 1.0`), tagged `nature-v2`. Every past result stays on v1 (`nature-v1`, the control
code). New studies start from v2. The live package `acl/` is moved to v2 next (its own commit, with tests; recorded below).

## The live package moved to v2 (16 October 2026)

`acl/` now holds `code_v2`'s rules (world bible 8.1) with nature v2 as its defaults (`anticipation_weight = 1.0` and the
four changes on); its own viewer files (`viewer.py`, `viewer.html`, `viewer_pixel.html`, `mindview.py`, with v2's two new
action names) are kept. **Check:** with no settings given, the live package reproduces v2's signed-off reference
fingerprints exactly (seeds 11 and 501), so `tests/reference_hashes.json`'s "acl" entry now equals "v2". Tests adapted
and recorded: two matter tests read v2's 0–100 property scale; the ST1 stranding test lost its `xfail` mark, as it was
written to (world 803 is no longer stranded); saves now record their laws' version, and a save from before v2 is refused
with a message (not loaded into the wrong laws, not deleted). All tests pass. Before this, the live package was the
older world bible 7.1, which no study has used since E8; it stays at the tag `nature-v1`.
