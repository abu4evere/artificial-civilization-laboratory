# FS1 — Is the erosion the founders' head start wearing off? Findings (NOT FINAL: blind recompute pending)

Frozen as `FS1-frozen` (operational note 1); **signed off by the creator** ("yessir", 28 October 2026). An
initial-condition study: `code_fs1` = `code_v8` + one setting, `founder_skill` (`v8_to_fs1.diff`). Run on GitHub
Actions (run 40731330406, `skip_zero=local`). 128 worlds: t (today's founders), z (founders' skills all 0), c
(founders' crafting 0), x (sham), on the same 32 paired seeds (19901–19932). LP (80 founders, 80×80), 500 years.
Every number comes from `analyse_fs1.py`, written before data; full tables are in `results.md`.

**Validity:** zero checks pass (including: with today's founders the code equals v8; at week 0 only the founders'
skills differ between arms); all 128 worlds present under one fingerprint (`code_fs1`).

**Population beside it:** mean living in years 300–500: t 79.7, z 85.2, c 87.6, sham 82.5. Died out by year 500: t 5,
z 6, c 7, sham 6 (of 32). By year 100: z 1, the others 0. **Collapse flag: not raised.**

## The answer

**No. The founders' head start does not explain the erosion.** Founders who start with no skill at all lead to the
same late world as today's founders. And the decline happens without any head start: world-born people reach high
crafting skill early and then lose it, century by century, in every arm alike.

### Primary — world-born adults' (20–40) crafting skill, years 300–500
| arm | mean skill | worlds / adult-years | − today [95%] | reading |
|---|---|---|---|---|
| t (today) | 0.0946 | 31 / 192,395 | | |
| z (zero start) | 0.0959 | 30 / 205,474 | **+0.0013 [−0.0082, +0.0116]** | **converges** |
| c (no crafting start) | 0.0998 | 30 / 213,265 | +0.0052 [−0.0025, +0.0131] | not shown |
| x (sham, yardstick) | 0.0992 | 29 / 199,607 | +0.0046 [−0.0026, +0.0128] | |

- The frozen margin is ±0.012 (one making act's skill gain from zero). z's whole interval lies inside it.
- c's point difference (+0.005) is like the sham's (+0.005), but its interval reaches +0.0131, just past the margin:
  **not shown** by the frozen rule. Read beside the sham, it looks like ordinary world-to-world drift.
- Survivor-weighted: these are living adults in the worlds still alive (29–31 of 32 per arm).

### The decline happens in every arm, from the same high early level
World-born adults' crafting skill / mean living, by century:

| years | t | z | c | sham |
|---|---|---|---|---|
| 0–100 | 0.436 / 124 | 0.430 / 128 | 0.423 / 129 | 0.435 / 128 |
| 100–200 | 0.227 / 129 | 0.222 / 138 | 0.224 / 143 | 0.227 / 136 |
| 200–300 | 0.148 / 97 | 0.141 / 110 | 0.148 / 114 | 0.147 / 104 |
| 300–400 | 0.106 / 82 | 0.106 / 89 | 0.111 / 91 | 0.111 / 86 |
| 400–500 | 0.082 / 78 | 0.085 / 82 | 0.088 / 85 | 0.087 / 79 |

- **The first world-born generations become more skilled than the founders ever were** (0.43, against founders'
  0.2–0.4), **even when the founders start at 0.** Early on, people make things often (0.21 making acts per adult-year
  in every arm) and so practise.
- **Then each century's adults are less skilled than the last**, because making falls about tenfold (0.21 → 0.02 per
  adult-year by years 300–500) and crafting skill grows only by making or play.

### Secondaries (years 300–500, per adult-year)
- **Making events:** t 0.0208; z −0.0004 [−0.0030, +0.0023]; c +0.0016 [−0.0007, +0.0041]; sham +0.0016. No arm
  differs beyond the sham.
- **Made things held:** t 0.447; z +0.015 [−0.104, +0.150]; c +0.063 [−0.010, +0.145]; sham +0.092. The same.
- **Skill by age** (world-born, years 300–500): about 0.07 at 10, 0.09 at 20, 0.10 at 30, 0.11 at 40 in every arm.
  People do learn over their lives, but from a low base.

## Against the prior (the assistant's, frozen)
1. "z and c converge with t": **z right; c not shown** (interval just past the margin; its point as the sham's).
2. "No collapse": **right** (1 early extinction in z, 0 in t).
3. "The secondaries converge": **right** in the sense that no arm differs beyond the sham.

## What follows (from the frozen readings)
- **z: "converges."** The frozen text reads: "the late state does not depend on the founders' head start ... that level is
  the target for later studies." That part holds.
- **But the head-start explanation itself is wrong, as GPT warned** ("convergence would not prove erosion is only a
  starting-condition effect"): the decline is the same with no head start at all. **The erosion is made by the world's
  own dynamics, not by its starting point.** Something during the first centuries turns people away from making:
  making acts per adult-year fall about tenfold while the conditions to make stay (LS1: feasible and weighed rise,
  chosen falls).
- **This points back to the known causes** (CO1, HL1, VC1, CL1): habits copied whole in talk make common actions look
  better than they are, and making looks worse than it is through too little practice. FS1 removes the last simple
  alternative (an artificial start), so a learning-rule study is the natural next step. That is a nature-change study:
  GPT and Gemini first; the creator decides.
- **For later studies:** today's founders can stay as they are. The start does not shape the late world.

## Independent recompute
Pending: GPT and Gemini, fresh chats, raw per-world numbers (the primary's sums per arm and seed; extinctions by year
100). Recorded only from their actual replies.
