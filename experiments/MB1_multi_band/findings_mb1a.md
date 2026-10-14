# MB1a — do ACL's bands meet? Findings

Frozen as `MB1a-frozen` (Stage A; correction of 12 October and operational notes of 14 October appended). Discovery
reading written and committed before the holdout ran (`findings_mb1a_discovery.md`). Tables: `results_mb1a_discovery.md`
and `results_mb1a_holdout.md`, from `analyse_mb1a.py`.

## Validity

Zero check PASS (control code and WS1's copy). All 192 replays reproduce their saved worlds: decade populations (the
frozen check) and the final state hash, 192 of 192. One fingerprint per code copy; no person of unknown lineage.
**Valid.** (The holdout lost about two hours while the PC slept; the runner resumed by itself.)

## The frozen reading (median between-lineage meeting rate per adult pair-year; stands only where both sets agree)

| arm | discovery | holdout | reading |
|---|---|---|---|
| C, today's world (20 founders, 40 × 40) | 0.0504 | 0.0487 | **no reading: at the line** (0.05). Written before the holdout: "a flip across the line is read as at the line" |
| P (80 founders, 40 × 40) | 0.0469 | 0.0446 | **bands meet rarely** (stands) |
| LP (80 founders, 80 × 80) | 0.0008 | 0.0006 | **bands are effectively closed** (stands) |

## Beside it (both sets; described)

| | C | P | LP |
|---|---|---|---|
| survived 120 years (of 64) | 42 | 57 | 64 |
| median population, year 120 (discovery / holdout) | 31 / 18 | 39 / 48 | 130 / 157 |
| median lineages alive at year 120 | 1 / 1 | 2 / 2 | 2 / 3 |
| interacting (chose to talk, give or court), per pair-year | 0.013 / 0.009 | 0.008 / 0.009 | 0.0001 / 0.0002 |
| couples across lineages, share of all couples | 10.8% / 12.9% | 5.0% / 5.5% | 4.3% / 1.5% |
| worlds with at least one such couple | 16 / 22 of 32 | 25 / 27 of 32 | 12 / 17 of 32 |
| recipes learned from another lineage, share | 6.9% / 5.1% | 3.8% / 4.9% | 3.7% / 0.6% |
| meeting in years 0–29 → 90–119 | 0.057 → 0.088 / 0.059 → 0.004 | 0.046 → 0.017 / 0.045 → 0.005 | 0.0013 → 0.0000 / 0.0019 → 0.0000 |

## What it shows

1. **In today's world, descent lines come within sight of each other at about the frozen line**, a twentieth of
   cross-line adult pairs a year, and about one couple in eight crosses them. Most of that contact happens early, while
   founders' bands still live; by year 120 a typical world has **one** lineage left, so there is nobody "between" to meet.
2. **Eighty founders on the same land (P): bands meet rarely**, and less as time goes on.
3. **Eighty founders on four times the land (LP): the bands are effectively closed**, about a seventieth of the rate in
   the other two, and fall to zero after year 60. Two or three lineages live on side by side for 120 years and almost
   never see each other. **Yet LP is the arm that survives best** (64 of 64 here; 2 of 256 died out in WS1). Its survival
   does not come from bands meeting: each band is large enough (20 founders) to carry itself.
4. **Interaction is a fraction of meeting** everywhere (a quarter or less): even when lines meet, they seldom talk,
   give or court across them.

## Caveats (written before the holdout; unchanged)

- Lineage is by the mother (frozen), so a child of a cross-lineage couple living among the father's kin counts as
  "between-lineage" contact inside one group. This inflates C and P, where such couples are commoner.
- "Within sight" is an upper bound on contact (correction of 12 October); interaction is the closer comparison with
  Hill et al., and it is lower.

## The assistant's prior, against the result

| prior | result |
|---|---|
| 20-founder worlds effectively closed (< 0.005) | **wrong**: at the line (≈ 0.05), ten times higher |
| 80-founder worlds meet only "rarely" | **right for P; wrong for LP** (effectively closed) |
| cross-lineage couples rare | **partly**: 1.5–13% of couples; in 12–27 of 32 worlds at least one |

## What it decides (frozen dependencies; the creator decides)

- **MB1b (Stage B)** was to run "only if Stage A shows bands meet at least rarely", at fixed land and people **in LP**
  (80 × 80, 80 founders). In LP the bands are effectively closed. As drafted, MB1b would compare divisions of a people
  whose bands never meet: the question it asks (does dividing the same people differently change survival and
  culture through contact?) has no contact to work through in that world. Options for the creator: run it anyway (the
  division may still change survival through band size alone), move it to P's density, or set it aside.
- **The new baseline** (decision listed after MB1a): LP survives best but its bands are closed; P meets rarely but is
  four times as crowded. MB1a adds this to the choice; it does not make it.
- Nothing in nature changes.
