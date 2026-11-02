# Debate round 45 (2 November 2026, the creator present): BN1, born without learned content (opinions, not sign-off)

**The same text to GPT (fresh chat `6ae81c51`) and Gemini (fresh chat `f6743d0727850cae`); Claude as council.** Two
steps.
- **The origin:** IQ1's H1 (`docs/research/iq1_islamic_sources_report_2026-11-01.md`). It is inspired by Q 16:78
  ("brought you out of your mothers' wombs knowing nothing, and gave you hearing, sight and minds"), together with
  developmental science, Deutsch's rejection of Lamarckism, and biology. That is inspiration, not proof.
- **The law in v11:** a newborn's habit values start at half the parents' mean learned values.

## Step 1
- **Proposed:**
  - **Arms:** v11; z (newborn values 0); x (inherited values scrambled); s (pure sham).
  - **Primary candidates:** calibration, learning speed, recipes per adult.
- **GPT: learning speed, 78%.**
  - The primary should be the area under the |q − G| curve over each child's first 52 weeks of habit learning.
    "Whole-life calibration (a) dilutes newborn effects; cumulative recipes (c) is too indirect."
  - Scramble **within each situation**.
  - **Main confound:** "The 8% weekly caregiver pull is enormous. After 52 weeks, approximately 1.3% of the initial
    inherited difference remains."
- **Gemini: recipes per adult, with a paired t-test, 88%.**
  - The scrambled arm is right.
  - **Confounds:** the carer pull overwrites the start; a zero start may change early exploration.

## The council's correction of its own facts (between steps)
**Two facts given to both models were wrong.** They were the assistant's errors, found in the code while checking
GPT's confound:
1. **The carer pull runs every 4 weeks, not every week** (`_upbringing` when `tick % 4 == 0`).
   - About a third (0.92^13 ≈ 0.34) of a newborn's starting difference remains at age one, when habit learning
     begins.
   - GPT's 1.3% came from the wrong figure.
2. **Learned values also pass in talk.**
   - `_imitate`: the listener moves toward the speaker's whole habit table, at 0.05 × (0.5 + curiosity) × (0.5 +
     respect), if they respect the speaker or the speaker seems happier.
   - So oblique and horizontal value transmission already exist.

The same wrong figure had gone into rounds 41 and 42 and into records. Corrections are appended in each
(`WORKLOG.md`, 2 November 2026, about 00:15).

## Step 2: the revised design
- **Arms:** v11; z; x (scrambled within each situation); s.
- **Primary:** early-life calibration. Mean |q − G| over each child's first 52 weeks of habit learning (age 1 to 2),
  standardized over situation × action cells.
- **The frozen reading is about realism, not performance.** The reason for z is that learned content is not
  inherited. With a margin of 0.02:
  - "z better" if the interval lies wholly below −0.02;
  - "z not worse" if its upper bound is below +0.02;
  - "z worse" if its lower bound is above +0.02;
  - otherwise inconclusive.
  - The sham must lie within ±0.01, and the guards must pass.

**GPT: accept with one change, 91%. Adopted.**
- "Freeze the standardization and common-support rule": fixed cell weights from an independent reference run.
- Pool across children within each world and cell.
- Preregister minimum coverage; too little means "inconclusive, not selective reweighting".
- **Its caution:** "The primary measures early-life calibration, not pure learning speed."
- "It is a legitimate nature-change experiment, not a theological proof."

**Gemini: accept, 95%.**
- **Council:** its "cleanly isolates" overstates. GPT's caution stands.
- Gemini was also told that ACL uses a paired world bootstrap, not t-tests. Its earlier choice of recipes per adult
  was set aside as too indirect for a change made at birth.

## What survived checking
**BN1, a test in a copy** (`code_bn1`):
- **Arms:** v11, z, x, s on 32 paired seeds.
- **Reference worlds:** 8 separate v11 worlds fix the cell weights.
- **Primary:** early-life calibration, with the non-inferiority reading above.
- **Guards:** child deaths, population, extinctions.
- **Secondary:** content (x − v11) and level (x − z); adult calibration; recipes per adult; making.
- **Adoption** would need the creator's explicit approval (IQ1's rule).
- **Estimates:** GPT 91%, Gemini 95%, **the assistant 75%**. The risks are thin early-life coverage, guarded by the
  coverage rule, and the new code copy, guarded by the zero checks.
