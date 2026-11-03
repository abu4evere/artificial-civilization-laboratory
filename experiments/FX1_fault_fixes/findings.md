# FF1: Fixing three faults in nature v11 — findings

**The name:** the study was frozen as "FX1" in the folder `FX1_fault_fixes`. It is FF1 because the ID FX1 was already
used (amendment 2).

**A fault-fix check in a copy** (`code_fx1` = `code_v11` + `fix_make_choice` + `fix_overflow`).
- Frozen as `FX1-frozen`.
- Signed off under the creator's permission to edit world rules (2 November).
- Council round 51: GPT 97%, Gemini 99%, DeepSeek about 95%, the assistant 85%.

**The run:**
- GitHub Actions run 41571953456. The zero checks ran on the cloud (`zero_cloud.log`, saved from the job log). They
  show:
  - `code_fx1` at 0 = v11;
  - the observer and log are read-only;
  - reload is exact;
  - **F1 unit check:** the offered recipe equals an independent argmax at all 111,209 teen and adult decisions of a
    30-year world (46,074 with a make option);
  - **F2/F3 unit check:** no made thing vanished at deaths or from bodies in arm f, against 5 in v11. The fault is
    shown.
- 160 worlds: five arms × 32 paired seeds (22401–22432). LP, 200 years; years 100–200 counted.
- Every number comes from `analyse_fx1.py`, written before data, with amendment 1 (both rules' newest offer logged)
  made before data. Full tables are in `results.md`.

**Validity:** zero checks pass; all 160 worlds are present under one `code_fx1` fingerprint.

## The answer
**No harm. No guard was raised and nothing was flagged.** Under the frozen plan, f is to become **nature v12**.

| contrast | living-weeks ratio [95%] | extinct worlds (arm, v11) |
|---|---|---|
| f / v11 | **1.0003 [0.8926, 1.1301]** | 1, 1 |
| f1 / v11 | 1.1040 [0.9840, 1.2631] | 0, 1 |
| f23 / v11 | 1.0737 [0.9843, 1.1855] | 0, 1 |
| sham / v11 | 1.0307 [0.9155, 1.1636] | 1, 1 |

**Flags:** none. Every described ratio for f against v11 lies inside [0.8, 1.25] or has an interval that includes 1:
- makes per adult-year 1.055;
- kinds per adult-year 1.007;
- made things held 1.068;
- things on the ground at year 200 1.113;
- adult-weeks 1.008.

## The fixes at work (described)
- **F1, the make choice.**
  - **How often it bites:** in v11's own worlds, the old and the fixed rule offer different recipes in **8.6%** of adult
    decisions with a make option. That is about twice UP1's estimate of the skip alone, which counted old kinds only.
  - **On the same decisions,** the fixed rule offers the person's newest recipe more often: **0.106 against 0.090**.
    The fault held new recipes back, as the review said.
- **F2, an heir's things.** Over years 100–200 of the 32 v11 worlds, **63** things were deleted at inheritances. Under
  f none were deleted, and **73** were left on the ground.
- **F3, things from a body.** In both arms they go to the ground: 531 in v11 and 648 in f. Under f, it is the least
  valued that go.
- **Remaking** is unchanged: late kinds remade 1 of 3,378 in v11 and 1 of 3,429 in f. The fixes correct the rules; they
  do not unlock remaking (AF1's finding stands).

**The assistant's prior:**
1. No guard: **right**.
2. The offers differ in 1–5% of decisions, and f's newest share is higher: **partly right**. They differ in 8.6%, more
   than expected; the newest share is higher, as expected.
3. R near 0: **right**.
4. Some tens of deletions per world: **wrong**. There were 63 across all 32 worlds, about 2 per world.

## Blind recompute (`recompute_ff1.md`)
- **GPT** (chat `6ae98bab`), **Gemini 3.1 Pro** (chat `c26932d23dea0964`) and **DeepSeek** (chat `22ef6243`, by hand)
  recomputed blind, from the per-world counts, with the prompt written before data.
- **All three match every point value, the extinct counts and the reading** (no harm). Interval ends differ by at
  most 0.005 for GPT and Gemini; DeepSeek's are hand approximations.
- **FF1 is final.**

## Next (by the frozen plan)
If the recomputes match: build `code_v12` = v11 with both fixes on by default; zero checks (v12 at 0 = v11, v12 =
arm f); regenerate the reference hashes and run the tests; tag `nature-v12`; add a line to
`docs/autonomous_decisions.md`; and send a Telegram. As frozen (round 51), a fault fix needs no confirmatory run.
