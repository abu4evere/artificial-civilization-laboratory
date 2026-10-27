# MO1 — The memory order. Findings (recompute by GPT and Gemini pending; not yet final)

Frozen as `MO1-frozen` (operational note 1); decided and signed off in sleep mode (`docs/autonomous_decisions.md`). A
nature-change study: `code_mo1` = `code_v7` + one setting (`v7_to_mo1.diff`). Run on GitHub Actions (run 40480396086,
`skip_zero=local`). 96 worlds: arms c (v7), o (the setting), s (sham), on the same 32 seeds (18901–18932). LP, 200
years. Every number comes from `analyse_mo1.py`, written before data; full tables are in `results.md`.

**Validity:**
- zero checks pass (`code_mo1` with the setting off equals `code_v7` exactly; the observer is read-only; the setting and
  the sham act; reload is exact);
- all 96 worlds are present under one fingerprint;
- every predicted deletion matches the code's (mismatches 0).

## The answer

**By the frozen rule, the change is not supported, because the manipulation check fails.** Under the new order,
recipes taken from others survive a memory overflow 0.837 of the time, below the frozen threshold of 0.90 (v7: 0.296).
The other three criteria are met:
- retention at 52 weeks rises by 0.243;
- useful knowledge held changes by −2% (within the −5% allowed);
- no taken recipe was found bad in either arm.

The frozen rule needs all four, so **MO1 does not make the memory-order change a candidate for nature v8.**

| measure | c (v7) | o | s (sham) | o − c [95%] | s − c [95%] |
|---|---|---|---|---|---|
| **M:** the new recipe survives an overflow | 0.296 | **0.837** | 0.303 | +0.540 [+0.494, +0.601] | +0.007 [−0.015, +0.028] |
| **P1:** taken recipes still held at 52 weeks | 0.672 | 0.915 | 0.679 | **+0.243 [+0.220, +0.273]** | +0.007 [−0.015, +0.027] |
| **P2:** useful recipes held per adult (years 50–200) | 9.34 | 9.14 | 9.45 | −0.19 [−0.32, −0.06] (allowed: above −0.47) | +0.11 [−0.09, +0.30] |
| **P3:** taken recipes found bad within 52 weeks | 0 | 0 | 0 | 0 | 0 |

**The decision rule:** M **fails**; P1 supports; P2 no harm; P3 no harm. **Not supported.**

**Populations:**
- 43,118 overflows in arm o, against 47,196 in c;
- 81,336 taken recipes checked at 52 weeks in o, against 88,155 in c;
- almost all of them were lessons (watching: about 40 per arm over all worlds).

### Described (not decision criteria; the sham's difference from c is the yardstick)
- **What is deleted instead** when the new recipe survives:
  - its value rises from 0.005 to 0.017;
  - a useful kind 0.92, against 0.97;
  - made by its holder in the past year 0.0027, against 0.0011.

  All are small.
- **Relearning:** 0.114 per learned recipe, against 0.128.
- **Making per adult-year:** 0.130 against 0.128. The interval includes 0, inside the sham band.
- **Population (years 150–200):** 110.7 against 116.7, with the sham at 110.1. The difference is within the sham band.
- **World-born kinds alive at year 200:** 100.1 against 98.6. The interval includes 0.
- **Extinct worlds:** c 1, o 0, s 1.

## Why M fell short (reading; not tested here)
PT1's threshold came from a **one-event replay** in v7 worlds: in v7's memories, 95.7% of new lessons would have
survived. In arm o the worlds themselves change.
- **Memories fill with lesson-valued recipes** that, in v7, would have been deleted at once.
- **A new lesson then competes** with others valued about the same, and loses about one time in six.
- **The deleted recipe's mean value** at an overflow is 0.022 in o, against 0.0017 in c.

The frozen threshold did not allow for that feedback. This is recorded as a lesson about thresholds set from one-event
replays. **The rule is not re-read after the data.**

## Against the prior (the assistant's, frozen)
1. "M passes: o about 0.95, c about 0.29": **wrong for o** (0.837), right for c (0.296).
2. "P1 rises by at least 0.15": **right** (+0.243).
3. "P2 changes by less than 5%": **right** (−2.1%).
4. "P3 no harm": **right** (no bad recipes in either arm).
5. "Making changes little (within the sham band)": **right.**

## What follows (from the frozen branches)
- **Not supported.** There is no nature-v8 candidate from MO1. v7 stays live.
- **The defect is still real** (PT1, final). The new order keeps a quarter more of taught recipes for a year, at little
  measured cost. Whether to test it again, under a new frozen plan whose manipulation threshold allows for this feedback,
  is **the creator's decision**. It is not re-decided here.
- As predicted by both models and stated in the plan, **it does not touch making** (0.130 against 0.128).
