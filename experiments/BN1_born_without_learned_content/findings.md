# BN1 — Born without learned content: findings (final: recomputed blind by GPT and Gemini; see the end)

**A nature-change test in a copy (`code_bn1` = `code_v11` + `newborn_values`). Live nature stays v11.** Under IQ1's
rule, adopting anything from this study needs **the creator's explicit approval** (1 November 2026). Frozen as
`BN1-frozen`; signed off by the assistant with the creator present (GPT 91%, Gemini 95%, the assistant 75%; debate
round 45).

**IQ1-H1:** inspired by Q 16:78 ("brought you out of your mothers' wombs knowing nothing"), developmental science and
biology. That is inspiration only. This study neither proves nor disproves any of those sources.

**The run:**
- GitHub Actions run 41394713611; the zero checks ran on the cloud (`zero_cloud.log`).
- 136 worlds: four arms × 32 paired seeds (21801–21832), plus 8 reference v11 worlds (21901–21908) used only for the
  cell weights. LP, 200 years; years 100–200 counted.
- Every number comes from `analyse_bn1.py`, written before data and tested on smoke worlds. Full tables are in
  `results.md`.

**Validity:**
- zero checks pass;
- all 136 worlds are present under one `code_bn1` fingerprint;
- every habit update replays exactly, and every newborn followed its arm's law (mismatches 0);
- coverage is 1.000 in every arm (28 of 41 early-life cells are common).
- **A correction appended to the plan** (before this analysis, text only): the cells are 32 × 19, not 32 × 16.

## The answer
**Inconclusive under the frozen rule. Newborns who start at zero are slightly worse calibrated in their first year of
habit learning, by about the size of the margin. No guard was raised.**

| quantity | value [95%] |
|---|---|
| E, v11 (half the parents' values) | 0.2734 |
| E, z (born at 0) | 0.2939 |
| E, x (the same numbers, shuffled within each situation) | 0.2844 |
| E, sham | 0.2733 |
| **D_z = z − v11** | **+0.0205 [+0.0157, +0.0252]** |
| sham − v11 | −0.0001 [−0.0077, +0.0072] |
| x − v11 (content) | +0.0110 [+0.0057, +0.0162] |
| x − z (level) | −0.0095 [−0.0155, −0.0037] |

**Why the rule reads "inconclusive":**
- D_z's interval lies wholly above 0, so **z is worse**: about 7.5% of v11's error.
- But the interval straddles the +0.02 margin. "Not worse" needs an upper bound below +0.02, and "worse" needs a lower
  bound above it.
- The sham passed (−0.0001), so chance alone does not move E at this size.

**Guards (z against v11): none raised.**

| guard | z | v11 | difference or ratio [95%] |
|---|---|---|---|
| child deaths per 1,000 child-years | 7.98 | 8.10 | [−1.19, +0.89] |
| population, z ÷ v11 | | | 0.957 [0.872, 1.048] |
| extinctions | 1 | 1 | (x 1, sham 1) |

### Secondary (described, not decisive)
| arm | early signed bias mean(q − G) | all-age calibration | recipes per adult | making per adult-year |
|---|---|---|---|---|
| v11 | −0.203 | 0.401 | 10.07 | 0.065 |
| z | −0.250 | 0.390 | 10.15 | 0.069 |
| x | −0.233 | 0.390 | 10.23 | 0.069 |
| sham | −0.203 | 0.401 | 10.02 | 0.064 |

- **Where z's extra error comes from:** z's young undervalue more (signed bias −0.250 against −0.203). Starting at 0
  puts them further below the realized returns, which are on average above zero. The inherited values, half the parents',
  start them closer.
- **Content matters, and so does level.**
  - Content: shuffling the same numbers across actions (x) costs +0.011 against v11.
  - Level: x is still better than z (−0.0095), so the general size of the values helps on its own.
- **Across all ages, calibration does not get worse:** z and x are both slightly lower (0.390 against 0.401). Any early
  cost does not carry into adult life. This is described only; it was not tested.
- **Know-how and making do not suffer:** recipes per adult and making per adult-year are the same or slightly higher
  in z and x.

## Against the prior (the assistant's, frozen)
1. **"z not worse": not shown.** z is worse by about the margin, and the rule cannot tell which side of it the truth
   lies.
2. **"Content matters a little": right.** x − v11 is +0.011.
3. **"No guard is raised": right.**

## What it means
- **Inheriting half the parents' learned values does help newborns a little at the start of habit learning.** The
  effect is small (2 hundredths on an error of about 0.27), and it is mostly a matter of level: starting near the
  right size.
- **The other channels make up much of the difference:** the carer pull and talk start soon after birth. Across all
  ages, people born at zero are as well calibrated as v11's.
- **Seen against the literature** (`docs/research/lamarckian_inheritance_learning_2026-11-02.md`, written before the
  data): passing on learned content tends to help early and in stable settings. BN1's small early cost with no later
  cost fits that. The analogy is partial: ACL's habit table is not a gene.
- **For the creator (no decision is needed now):**
  - BN1 gives no reason **against** removing birth inheritance on realism grounds: no guard, no later cost.
  - Nor does it show "not worse" by the frozen margin.
  - Any change to live nature is the creator's decision alone. A confirmatory run with a pre-registered margin would be
    the safe path.

## Blind recompute (`recompute_bn1.md`)
GPT (chat `6ae852b9`) and Gemini (chat `1a3a6aeafc603932`) recomputed BN1 from the per-world cell sums, with the prompt
written before the data and without the analysis script. **Both match every point value (E per arm, the four
differences, 28 common cells) and the reading, inconclusive.** Interval ends differ by at most 0.0001. Gemini's
table of per-arm totals was garbled and is not used. **BN1 is final.**
