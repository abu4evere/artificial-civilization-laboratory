# FF2 — Fixing three more faults, in nature v12: findings (pending the blind recompute)

Frozen as `FF2-frozen`. A fault-fix check in a copy: `code_ff2` = `code_v12` + `fix_hunt_expect` (F8), `fix_mat_limit`
(F4) and `fix_water_holder` (F5).
- **The run:** GitHub Actions run 41680655094, with the zero checks on the cloud (`zero_cloud.log`: All: PASS;
  `code_ff2` fingerprint `1bc337e7…`). The F8, F4 and F5 unit checks pass there as they did locally.
- **The worlds:** 32 paired seeds 22701–22732, 6 arms, LP, 200 years, with years 100–200 counted.
- **Every number** comes from `analyse_ff2.py`, written before data. Full tables are in `results.md`.

**Validity:** zero checks pass; all 192 worlds are present under one fingerprint.

## The decision (frozen): no harm
| contrast | living-weeks ratio [95%] | extinct (arm, v12) |
|---|---|---|
| **f / v12** | **1.0008 [0.8893, 1.1203]** | 0, 0 |
| f8 / v12 | 1.0284 [0.9359, 1.1345] | 0, 0 |
| f4 / v12 | 0.9425 [0.8362, 1.0492] | 0, 0 |
| f5 / v12 | 0.9293 [0.7924, 1.0747] | 1, 0 |
| sham / v12 | 0.9524 [0.8689, 1.0475] | 0, 0 |

**No guard is raised.** Population is unchanged and there are no extinctions. The single-fix arms and the sham all lie
within the same spread.

## The one flag, explained (read-only, from the frozen tables)
**Adult hunter-weeks per adult-week:** f / v12 = **0.789 [0.713, 0.884]** (frozen rule: outside [0.8, 1.25], with the
interval wholly below 1).
- **The cause is F8 itself, as designed.**
  - On the same hunt options, the decision's expected food per success was **35.4 under v12's rule** and **8.67 under
    the fixed rule** (arm f; v12: 35.60 against 8.45). The fixed figure matches HN1's realised 8.79 per success.
  - With the honest expectation, the hunt option weighs about a quarter as much, so fewer people choose it.
- **F8 alone gives the drop:** arm f8 has 0.1039 adult hunter-weeks per 1,000 adult-weeks, against v12's 0.1375 (−24%).
  Arms f4 (0.1438) and f5 (0.1436) are at v12's level.
- **It is not harm:**
  - population and adult-weeks are unchanged (1.0050 [0.893, 1.124]);
  - the success share is unchanged (0.0506 against 0.0532);
  - meat from hunts was already negligible (0.0038 food per adult-year on v12).
- **People now hunt as often as an honest expectation warrants.** Calibrating whether hunting **should** pay more is
  HR1's job (F7: per-species success, and meat per kill), not FF2's.
- **A side observation:** hunt options are offered a little more often under f (1.134 [1.018, 1.275]). That is
  consistent with fewer kills leaving more prey standing. It is within the [0.8, 1.25] band and not flagged.
- **Adoption is not blocked:** the explanation finds no harm.

## The three fixes at work (described)
- **F8:** hunt options are now weighed by the meat of the prey present: about 8.6 food per success instead of 35.5.
- **F4:**
  - in v12, about **4,400 material units** a century (all 32 worlds together) went past the 20-unit limit **at
    inheritance**;
  - **none came from hunting spoils** (0 in every arm; hunts with spoils are very rare);
  - under the fix these units go to the tile's pile; nothing is lost (the unit check shows conservation).
- **F5:** about **9% of adults' water-walk weeks** (41,209 of 447,970 on v12) were by someone whose best carry thing
  cannot hold water. Under the fix such a thing no longer shortens the walk.
- **Making:** makes per adult-year 0.0672 against 0.0727 (0.924 [0.836, 1.018]); made things held per adult 0.893
  against 0.953. Neither is flagged.

## Against the assistant's frozen prior
1. "No guard raised": **right.**
2. "F8: the expected food falls from about 37 to about 10; hunting becomes rarer; the ratio is flagged and explained":
   **right.** The figures were 35.5 → 8.6, and hunting fell by 21%.
3. "F4 triggers rarely (tens of units per world), mostly at inheritance": **right in kind, low in size.** It is about
   140 units per world over the century (4,418 ÷ 32), all at inheritance.
4. "F5 triggers rarely": **partly wrong.** About 9% of water-walk weeks involve a leaky carry thing.

## Next (the frozen plan's adoption path)
1. A blind recompute by GPT, Gemini and DeepSeek from `recompute/ff2_counts.csv` (`recompute/prompt.txt`).
2. If it matches: `code_v13` = `code_v12` with the three fixes on by default; zero checks (v13 with the fixes off =
   v12; v13 = FF2's arm f); reference hashes; tests; tag `nature-v13`; a Telegram message. No confirmatory run (a
   fault fix, as FF1).
