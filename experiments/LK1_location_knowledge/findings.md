# LK1 — Does knowing where absent loved ones are keep ACL's worlds alive? Findings

Frozen as `LK1-frozen`, amended once before any main-run data (`LK1-amend1`). `code_lk1` (fingerprint `765312576e42…`,
commit `a725702`); 256 new seeds (4001–4256), 20 founders, 40 × 40, 120 years; arms C (current location, today's world),
M (last-seen memory), S (sham). Tables: `results.md`, from `analyse_lk1.py`, unchanged since freezing. (It was run as
`PYTHONIOENCODING=utf-8 python analyse_lk1.py`: the first attempt wrote `results.md` and then stopped while printing
the same text to a console that could not show "×". The re-run wrote the same file; nothing in the script changed.)

## Validity

- Zero checks: PASS (`output/zero.txt`).
- One code fingerprint in every world: PASS.
- **The manipulation, in the main run itself:** in M, **0** go-to moves toward an out-of-sight loved one's current tile
  (required 0), and **451,834** toward remembered tiles (required above 0). In C, A5's share was **29.3%**, as AA1
  measured (~30%).

**Valid.** No error log; all 768 worlds saved.

## Baseline (rule 14)

C died out in **90 of 256** worlds (35.2%); MC1-L's control, on other seeds, 87 of 256 (34.0%).

## The frozen reading

| | C (current) | M (last seen) | S (sham) |
|---|---|---|---|
| worlds died out (of 256) | 90 | **87** | 95 |
| paired against C: saved / lost | – | 41 / 38 | 37 / 42 |
| exact two-sided sign test | – | **p = 0.822** | p = 0.653 |
| median population, year 119 | 20 | 24 | 21 |

**Effect** (C − M extinction share): **+0.012, 95% interval [−0.059, +0.082]**. Half of F2's effect: 0.120. The
interval excludes it.

**Frozen rule: no meaningful effect on survival.** Taking away knowledge of where absent loved ones are, and leaving
only where each was last seen, does not change how many worlds die out by as much as half of what perfect partner
finding did. The sham was quiet.

## Secondary measures (M against C; described, not thresholded)

Per-world medians, paired Wilcoxon (`results.md`); population beside each in the main table above.

| | C | M | p |
|---|---|---|---|
| pairings per eligible single-year | 0.027 | 0.028 | 0.97 |
| median weeks from eligible single to pairing | 142 | 150 | 0.90 |
| share of partner-weeks beyond sight | 0.213 | **0.277** | 2 × 10⁻²⁵ |
| share of mother–child-weeks beyond sight (child under 16) | 0.030 | **0.037** | 9 × 10⁻¹⁷ |
| median spell apart, partners (weeks) | 1 | **2** | 1 × 10⁻¹⁷ |
| median spell apart, mother and child (weeks) | 1 | **2** | 2 × 10⁻¹² |
| births per woman-year | 0.128 | 0.126 | 0.27 |
| A6c: partner-search moves aimed beyond sight | 0.629 | 0.637 | 0.93 |

Families drift apart more without the shortcut: partners spend about three tenths more of their weeks out of sight,
and spells apart are longer. Nothing else moved: not partner finding, not births, not the other shortcut (A6c).

## Predictions (frozen, the assistant's), against the result

| prediction | result |
|---|---|
| separation time rises in M | **right** (clearly, on every separation measure) |
| partner-finding success falls slightly | **wrong**: unchanged (0.027 vs 0.028) |
| births fall a little | **not shown**: 0.128 vs 0.126, p = 0.27 |
| A6c's share rises | **not shown**: 0.629 vs 0.637, p = 0.93 |
| extinction rises, by less than half of F2's effect | **reading right, direction wrong**: no meaningful effect; the point estimate leans toward fewer extinctions in M (87 vs 90), not significant |

## Reading (caps)

- **What is shown:** on 256 new 20-founder worlds, A5, the shortcut by which people walk toward where an absent loved
  one is *now*, does not hold worlds together. Replacing it with walking to where they were last seen keeps families
  together less, and changes nothing measurable in survival, partner finding or births.
- **Why, most likely (not tested):** A5 acts on ties that already exist. Worlds die because new partners are not
  found (F2), and A5 never helped with that: partner finding was the same in both arms.
- **What is not shown:** that A5 has no effect at all (an effect on extinction from −0.06 to +0.08 is not excluded);
  anything about 80-founder worlds; whether real people track where others are (evidence, not simulation; N8: not
  shown).
- **For Law 126:** A5 is a known compromise, measured (AA1) and now tested against a replacement that passes T1–T4. The
  replacement costs nothing measurable in survival. **Whether to adopt it into a new version of nature (v2, with the
  A1 fix) is the creator's decision**, listed in `docs/OPEN_DECISIONS.md`. Every past result stays on `nature-v1`.
- **For the thread:** partner finding remains the lever. It is not propped up by this shortcut, so the next question
  is the one already queued: do separate bands ever meet (MB1a)?

**Next:** SA1 (sensitivity audit; starts by itself after LK1), then MB1a, ID1, BL0.

## The creator's decision (13 October 2026, appended)

"**Approve last-seen + A1 for nature v2, after BL0.**" Last-seen memory replaces A5, and the A1 fix (branch
`nature-v2-a1`) goes in with it, as one change and one record. It is built only after BL0, with zero checks, new
reference fingerprints and a comparison of the combined version against `nature-v1` on fresh seeds: LK1 tested
last-seen memory alone, never the two together. `nature-v1` is kept, and every past result stays on it. Nothing in
the world changes while SA1, MB1a, ID1 and BL0 run.
