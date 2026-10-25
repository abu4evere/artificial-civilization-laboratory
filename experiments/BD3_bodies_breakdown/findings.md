# BD3 — What in a body keeps more people alive? Findings

Frozen as `BD3-frozen` before any code or data (signed off by the creator, 24 October 2026; Revision 1 after GPT's
review; operational amendment 1 and note 2 recorded before data). Tables: `results.md`, written by `analyse_bd3.py`
(committed before data). Code: `code_bd3` = `code_v6` + five probe switches (`v6_to_bd3.diff`). **9,216 worlds**: 1,024
new seeds (15001–16024) × nine arms, 20 founders, 120 years, run on GitHub (`cloud-run`, run 40149607984). Zero checks
passed here and there.

## Validity

Zero checks passed; all 9,216 worlds present; one fingerprint; **manipulation check passes** in every arm (each part's
events are zero where it is switched off, and its opportunities are there). **Valid.**

## The frozen reading

**(1) The gate: does the bodies' gain replicate on fresh seeds? No.** Time-averaged population: F (nature v6) **26.14**,
N (v6 without bodies) **26.10**: F / N − 1 = **+0.2%**, 95% interval [−3.4%, +3.8%]. By the rule fixed before data,
everything after the gate is **described only**.

**(2) The parts (described only):** removing any one part changed population by less than the uncertainty: foul
+3.1% [−1.0%, +7.0%] (the largest, raw bootstrap p 0.04, not significant after Holm), tools −0.9%, eat −0.5%,
carried +0.6%, seen 0.0%. The eat × carried interaction: +1.4% of F [−2.1%, +4.8%]. All five off (F−all) against N:
+0.2% [−1.9%, +2.3%]. Shares of a gain that is itself about zero are meaningless and are not read.

**Survival (secondary):** died out by year 120: F 330 of 1,024, N 322; every F−x arm 316–338; no paired comparison
with F near significance (McNemar p 0.39–0.86).

**Avoidance, measured directly (GPT's hypothesis):** among people who stood by a rotten body, the share back within one
tile 4, 14, 52 and 104 weeks later was **identical** with the disgust (F: 0.343, 0.194, 0.145, 0.128) and without it
(F−foul: 0.343, 0.195, 0.146, 0.130); so was the share who went to such a place when it was within reach. **The
disgust at rot, as v6 has it, does not change where people go.**

## What it means

- **BD2's remaining gain (+7.7% against no bodies) was not replicated.** On 1,024 new seeds, worlds with realistically
  rotting bodies hold about the same population as worlds where the dead vanish. It now appears likely to have reflected
  sampling variation, above all in the no-bodies arm: BD2's R arm (26.16) matches BD3's F (26.14) almost exactly, while
  BD2's N came out lower (24.28 against BD3's 26.10). That is suggestive, not proof. BD3's interval [−3.4%, +3.8%]
  makes a gain of BD2's size unlikely; it does not prove the effect is exactly zero. A correction is appended beside BD2's findings.
- **What stays true:** BD1 and BD2 found a real gain with v4's slow rot (bodies rotting for about two years): +19–20%
  population and fewer extinctions, repeated twice. Realistic rot removed it entirely, not "most of it".
- **Bodies are in nature (v4–v6) for their truth, not their benefit**, as the adoption rules said; nothing about that
  changes. The dead now stay, rot as real bodies do, can be eaten, are seen, keep their tools for kin, and do not, in
  this world, change how many people live.
- **Foul, described only:** removing the disgust at rot lowered population by an estimated 3.1%, but its adjusted
  interval [−1.0%, +7.0%] includes zero (raw p 0.04, not significant after Holm, and the gate failed): suggestive at
  most.
- **The avoidance idea (BD1's exploratory reading, GPT's suspicion) is not supported at realistic rot:** the place
  penalty is applied about two million times, yet return rates are identical. One plausible reason (not tested): a
  rotten body is foul for only weeks, and a single −0.3 in a place's remembered value is small against food and company.
- **The assistant's prior was wrong** (it expected the gain to replicate at about +6%, carried mostly by eating).

## For the record

- 1,024 seeds per arm were enough to answer the gate clearly; they were not enough to resolve parts of 1–3% (as the
  plan warned), and since the gate failed, no part is read.
- A lesson the method already holds (rule 15): what one set of worlds shows is checked on worlds nobody has seen. BD2's
  +7.7% looked solid on 512 seeds and did not replicate on 1,024 fresh ones, as GR1 did not with GR2. GPT's lessons:
  replicate important effects on fresh seeds even when adoption rests on realism; explain an effect only once it is
  confirmed; justify the laws of the world independently of the outcome hoped for (`gpt_view_bd3.md`).
