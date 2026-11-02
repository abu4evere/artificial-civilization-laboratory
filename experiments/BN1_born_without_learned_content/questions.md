# BN1 — Born without learned content: a nature-change test in a copy (frozen plan)

**A test in a copy (`code_bn1` = `code_v11` + `newborn_values`; 0 = v11 exactly), not an adoption.** Live nature
stays v11. Under IQ1's rule, adoption of anything from this study needs **the creator's explicit approval** (the
creator, 1 November 2026), on top of the safe path in `CLAUDE.md`.

**IQ1-H1.** It is inspired by Q 16:78 ("brought you out of your mothers' wombs knowing nothing, and gave you hearing,
sight and minds"; Ibn Kathir: the faculties "develop gradually"), together with developmental science (innate
structure, not learned content), Deutsch's rejection of Lamarckism, and biology (learned values are not inherited
genetically). The sources are inspiration only. No result here proves or disproves them.

## Why
- **The law in v11:** a newborn's habit values start at **half the parents' mean learned values**
  (`acl/biology.py`: `child.q = [0.25 * (a + b) ...]`). That is learned content passed at birth, which Earth's biology
  does not do.
- **Two more channels pass learned values after birth** (corrected 2 November 2026):
  - the **carer pull** (8% toward the carer's values every 4 weeks, under 12);
  - **talk** (`_imitate`: toward a respected or happier speaker's whole habit table, at any age).
- **The question:** does inheriting learned content at birth matter, given those channels? Without it, is learning
  worse, the same, or better?
- **Debate round 45** (`docs/debate_round45_bn1_2026-11-02.md`): both models accepted the design below (GPT 91% with
  fixed weights and a coverage rule, adopted; Gemini 95%).

## The law (one setting, `newborn_values`; 0 = v11)
- **0:** as v11. Newborn values are 0.25 × (mother's + father's), with the father's replaced by the mother's if he is
  dead or absent.
- **1 (z):** newborn values all **0**.
- **2 (x):** the same inherited numbers as v11, but **shuffled across actions within each situation** with the
  world's random stream. Each situation keeps its mean and spread; the parents' content (which action has which
  value) is lost.

**Nothing else changes:** the carer pull, talk, learning, choice and all other laws. No action is favoured.

## Arms (32 paired seeds 21801–21832; LP: 80 founders, 80 × 80; 200 years; years 100–200 counted)
| arm | setting |
|---|---|
| **v11** | `newborn_values` 0 (= `code_v11`, shown by the zero checks) |
| **z** | `newborn_values` 1 |
| **x** | `newborn_values` 2 |
| **s** | sham: v11 with `sham_draw` 1 |

**Reference worlds:** 8 further v11 worlds (seeds 21901–21908), used **only** to fix the cell weights below.

## Measures (paired world bootstrap, 10,000 replicates; NumPy seed 20261102)
- **Early-life updates:** habit updates started when the person is between 52 and 103 weeks old, the first 52 weeks
  of habit learning, in years 100–200.
  - G is ES2's realized return (Σ_j 0.8^j r over the person's next updates, closed when the weight falls below
    0.001).
  - Updates whose G was closed by death are left out of the primary, and reported.
- **Cells:** situation × action (32 × 16).
- **Fixed weights:** each cell's share of early-life updates (not death-closed) in the 8 reference worlds, pooled.
- **Common support:** cells with at least 30 early-life updates (pooled over seeds) in **every** arm, and a reference
  weight above 0.
- **Coverage:** for each arm, the share of its early-life updates that fall in common cells.
- **PRIMARY:** E = Σ_c w_c × mean|q − G|_c over common cells, with weights renormalized, per arm.
  - The cell means pool children within each world and cell (GPT).
  - **Contrast: D_z = E_z − E_v11.**
  - In a resample, a common cell empty in any arm is left out for all arms, and the weights renormalized.

## Frozen decision rule (non-inferiority; the motive for z is realism, not performance)
1. **Inconclusive (coverage):** coverage below 0.80 in any arm.
2. **Inconclusive (sham):** the sham's point difference E_s − E_v11 lies outside ±0.01.
3. **Otherwise, on D_z's 95% interval:**
   - **"z better":** the upper bound is below −0.02;
   - **"z not worse":** the upper bound is below +0.02, and "better" does not hold;
   - **"z worse":** the lower bound is above +0.02;
   - **otherwise "inconclusive".**
4. **Guards** (z against v11; each reported, and any raised guard is stated with the reading):
   - **child deaths** per 1,000 child-years: up by more than 10% of v11's rate, with the lower bound above 0;
   - **population:** z ÷ v11 below 0.90, with the upper bound below 1;
   - **extinctions:** 3 or more beyond v11's.

**GPT's caution** goes with the reading: this measures **early-life calibration**, not pure learning speed. Initial
values, action selection and socially passed values all affect it.

## Secondary (described, not decisive)
- **Content:** E_x − E_v11. **Level:** E_x − E_z.
- **Signed early-life bias** mean(q − G) per arm.
- **Adult calibration** (ages 16+, all actions, years 100–200) per arm.
- **Recipes known per adult** (yearly census); **making per adult-year**; **population**; **child deaths**.

## Validity (hard stops)
- **Zero checks:**
  - `code_bn1` with `newborn_values` 0 = `code_v11` (state and random numbers, 20 and 60 years);
  - z, x and the sham each act;
  - the observer is read-only;
  - every habit update replays exactly (mismatch 0);
  - reload is exact (arm x saved at year 10 continues exactly to year 15);
  - **in z, every newborn's values are all 0;**
  - **in x, every newborn's values are a within-situation permutation of the inherited ones** (mismatch 0).
- **All 4 × 32 worlds and the 8 reference worlds are present** under one `code_bn1` fingerprint.
- **A blind recompute by GPT and Gemini** of E per arm, D_z with its interval, the coverage and the reading, from
  per-world cell sums.

## The assistant's prior
1. **"z not worse".** The carer pull and talk pass values soon after birth, so starting at zero costs little.
2. **Content matters a little:** E_x is slightly above E_v11.
3. **No guard is raised.**

## Sign-off (2 November 2026)
The assistant, with the creator present and asking to keep working. This is a nature-change test in a copy under the
40% rule; adoption only with the creator's explicit approval. GPT estimates 91%, Gemini 95% and the assistant 75%.
Frozen as `BN1-frozen` before any code or data.

## Correction (2 November 2026, appended; the frozen text above is unchanged)
- **"Cells: situation × action (32 × 16)" is wrong: it is 32 × 19.** v11 has 19 actions (`acl/person.py`:
  `ACTIONS`, `N_ACTIONS` = 19), so a habit table has 608 values. Found while writing the ODD description from the code.
- **The code was already right.** `code_bn1`'s shuffle (arm x) and the runner's newborn check both use `N_ACTIONS`
  from nature, and the analysis takes its cells from the data. The zero checks passed with it (`zero_cloud.log`).
  The rule, measures and arms are unchanged. The error was only in this text.
