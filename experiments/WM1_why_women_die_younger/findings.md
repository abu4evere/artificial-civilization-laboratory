# WM1 — Why do women die younger than men? Findings (recomputed independently; final)

Frozen as `WM1-frozen` (Revision 1, operational note 1, amendment 1); run on GitHub Actions (run 40230540160). 1,152
worlds on nature v7, 120 years: Part A read-only C20 and D80; Part B a 2 × 2 × 2 diagnostic design on C20. Seeds
17001–17128, paired. Numbers from `analyse_wm1.py` (written before data); full tables in `results.md`. Valid: zero
checks pass, all worlds present, one fingerprint per code, seeds paired.

## The answer

**1. There is a real gap.** Age-standardised death rates per 1,000 person-years, ages 16–54:

| | women | men | G (F − M) | R (F / M) | survival 16→50, women / men |
|---|---|---|---|---|---|
| C20 | 41.2 | 32.5 | **8.6** [5.9, 11.4] | **1.27** [1.18, 1.36] | 0.30 / 0.44 |
| D80 | 48.6 | 35.0 | **13.6** [11.3, 16.1] | **1.39** [1.32, 1.46] | 0.22 / 0.38 |

The gap opens from about age 20 and is widest at 25–44.

**2. It is about caring for children while short of food.**
- **In the diagnostic arms** (Q4, paired), only **K0, where the carer meets her own need first**, reduces the gap:
  main effect −6.1 [−8.2, −4.1] per 1,000 person-years, about 70% of G.
- **P0** (no extra pregnancy food) and **B0** (no childbirth deaths) are **unclear**:
  - P0: −0.6 [−2.4, 1.2];
  - B0: 0.0 [−1.1, 1.2].
  Neither reduced the gap in a way this study could see. By the frozen rule this is "unclear", not "no effect": both
  intervals reach below −1.
- No interaction is clear.

**3. With all three removed, about a quarter remains** (Q5). G = 2.1 [0.04, 4.2], 25% of the v7 gap [0%, 55%]. The
interval is just above 0, so by the frozen rule another, smaller source exists.

## Described (associations, not causes)

**Q2, by state:**

| | women | men |
|---|---|---|
| unloaded weeks, C20 | 34.5 | 31.9 |
| unloaded weeks, D80 | 33.1 | 33.6 |
| carer weeks, C20 | 49.6 | 37.6 |

- In unloaded weeks the sexes die at about the same rate, within the 10% tolerance.
- Death rates rise with the number of dependants fed, for both sexes, and steeply with recent hunger.

**Q3, by cause** (signed shares of G):

| cause | C20 | D80 |
|---|---|---|
| starvation | 68% | 64% |
| thirst | 12% | 15% |
| illness | 12% | 13% |
| childbirth | 11% | 8% |
| killed | 0% | 0% |

By state at death, the excess sits in carer weeks (129% of G in C20), offset by women's lower share of unloaded
weeks.

**Who carries the children:** women hold 76% of carer-weeks (C20). Per adult week, women give 1.23 food to dependants
and men 0.14.

**Support:**
- Pregnant women get little food from their partners: 68 thousand units in C20, against 203 thousand from kin and 153
  thousand from others.
- Women who died had a living partner 56% of the time, but he was within 2 tiles only 17% of the time.

**No men-only risks:** attacks and injuries are rare and equal for the two sexes. "Hunting weeks" logged near zero for
both; that measure may not catch hunting (not checked further, a limit).

**K0's costs:** child survival to 5 falls from 0.84 to 0.71, and births per woman reaching 45 rise from 2.98 to 3.82,
because more women live. Population and extinctions change little (time-averaged 24.8 vs 26.0; 45 vs 41 of 128 died
out).

**Founders:** G 11.4 (C20), 30.1 (D80).

## Against the prior

| prior | result |
|---|---|
| R of 1.3–1.6 in C20 | 1.27: just below |
| K0 does the most | right |
| P0 does the next most | wrong |
| B0 is under 15% of G | right: childbirth 11% of G by cause; B0 main effect about 0 |
| all three removed leaves G near 0 | partly: a quarter remains |
| most of the excess is in carer weeks | right |

## What follows (frozen)

One load reduces the gap: the rule that a mother feeds her dependants from her own food first. The frozen next step is
an evidence review of how forager women are supported while pregnant and caring: food from partners, grandmothers and
others, and what ACL lacks. Any change to nature would come after that review, frozen on its own. K0 is a measuring
tool, not a candidate (it costs children). The remaining quarter of the gap has another source, to be looked for.

## Independent recompute (25 October 2026)

GPT recomputed G, R, every arm and the main effects from the raw files without the script; every number matches (`recompute_wm1.md`).
