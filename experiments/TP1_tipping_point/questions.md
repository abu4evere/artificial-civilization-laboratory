# TP1 — Is there a tipping point below which a small world cannot recover? (DRAFT, 21 October 2026; for the creator's sign-off)

**Why.** Complex-systems science (Santa Fe Institute; `../../docs/SFI_notes.md`) stresses thresholds: small changes
near a tipping point have large effects. F1 (`../F1_baseline_fragility/findings.md`) found that worlds that die can be
told apart decades ahead (population at year 20; "population below 20 and at most three fertile women at year 30"
recurring). TP1 asks whether there is a **sharp threshold** in the number of women of childbearing age, below which a
world almost never recovers. The creator approved checking (21 October 2026). **Read-only: no new runs; only saved
worlds are read.** The relationship between fertile women and extinction in these worlds has not been looked at before
this plan.

## Worlds (Decision 1)

Today's nature (v2) control worlds already saved, each with a yearly snapshot from F1's probe (`women` = women aged
16–45 alive at the snapshot):
- **Discovery:** RT1b's C (seeds 5701–5956) and FX2's C (6001–6256): 512 worlds.
- **Holdout:** FX3's C (7301–7556): 256 worlds, read only after the discovery reading is written and committed.

All three are code copies whose zero checks showed them identical to `code_v2` with their settings off.

## Measures (fixed now)

- **Unit:** a world alive at a check year t ∈ {20, 30, 40, 50, 60}; its **W** = fertile women at year t's snapshot.
- **Outcome:** the world dies out before year 120.
- **Curve:** for each W (0, 1, 2, … pooled over check years), the share of world-years that go on to die out, with
  the number of world-years beside it (rule 18).

## The frozen reading (proposed)

- **Tipping point (discovery):** the smallest W* such that worlds with W ≤ W* die out in **at least 90%** of cases and
  worlds with W ≥ W* + 3 die out in **at most 50%** (a drop of at least 40 points within three women). If no W meets
  both, the reading is **"no sharp threshold"** (a gradual slope).
- **Holdout:** W* **stands** if, in the holdout, worlds with W ≤ W* die out in at least 80% and worlds with W ≥ W* + 3 in
  at most 50%. Otherwise **"not confirmed"**.
- **Described:** the same curve for all adults (`n` of age 16+ is not in the snapshot, so total population `n`) and for
  single fertile women with no eligible man (`women_single_no_mate`); how often a world at or below W* recovers.
- It describes ACL's worlds under today's nature; it does not show a threshold in real foragers.

## The assistant's prior (to be frozen at sign-off; held loosely)

A sharp threshold exists at **W* = 3** (F1's recurring "at most three fertile women"), and it stands on the holdout.

## Decisions for the creator

1. Worlds: **RT1b C + FX2 C (discovery), FX3 C (holdout)** (recommended).
2. The reading and its thresholds (90% / 50%, three women), fixed as written.
3. The prior, frozen as written.
