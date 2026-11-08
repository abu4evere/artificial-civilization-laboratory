# DF1 findings: who feeds the children, and what does it cost them?

**Status: final.** The blind recompute (`recompute_df1.md`, 7 November 2026, 19:49) matches: GPT and Gemini agree
in every point estimate and in the reading.

Every number is from `results.md` (analyse_df1.py, frozen before data) on cloud run 42425472140:
- 32 worlds, seeds 25101–25132, on `code_v16`, read-only; years 100–200 counted;
- zero checks All: PASS (`zero_local.log`):
  - the observer is read-only;
  - the ledger's food fed out equals the dependents' gain in every feeder-week (16,630 feeder-weeks, 0 mismatches);
  - reload exact.

## The answer in one line
**The frozen reading: feeding drives the gap.**

| | short weeks caused by feeding, per 1,000 grown person-weeks |
|---|---|
| women | **7.38** [6.74, 8.03] (54,928 of 7,438,652) |
| men | **0.74** [0.65, 0.82] (6,918 of 9,411,660) |
| women − men | **+6.65 [+6.07, +7.23]** |

**Women carry 0.888 [0.879, 0.897] of all feeding-caused short weeks.**

## Why: the mother feeds, by rule
- **The caregiver rule.** A child's caregiver is set at birth to the mother (`biology.py`). It passes to another person
  only when the caregiver dies. Each body phase, the caregiver feeds her dependents first, as far as her care trait
  takes her.
- **Who feeds, by dependent-weeks:**

  | caregiver | dependent-weeks | share |
  |---|---|---|
  | mother | 4,253,879 | 0.815 |
  | father (after the mother's death) | 817,672 | 0.157 |
  | someone else | 150,492 | 0.029 |

- **Fathers feed their children only by gift:** 53,994 gifts, 391,135 food in all. Women fed out about 7.0 million food
  in the same years (from the table below). So **fathers' gifts are about one twentieth of what mothers feed by
  rule.** Mothers made no gifts to their own children; the rule feeds them already.

**By age band** (per grown person-week):

| band | sex | with dependents | fed out | short weeks per 1,000 | caused by feeding per 1,000 |
|---|---|---|---|---|---|
| 16–29 | women | 0.225 | 0.744 | 36.4 | 6.68 |
| 16–29 | men | 0.028 | 0.062 | 31.6 | 0.57 |
| **30–49** | **women** | **0.583** | **1.661** | **36.6** | **12.25** |
| 30–49 | men | 0.103 | 0.143 | 30.1 | 1.14 |
| 50+ | women | 0.150 | 0.035 | 27.3 | 0.35 |
| 50+ | men | 0.048 | 0.038 | 28.9 | 0.34 |

## The energy link
After a feeding-caused short week, the next decision starts with energy below 25 in 0.095 of cases for women and 0.101
for men. In v16, forage is then offered nowhere. After a week that was not short, the share is 0.0001 or less.

**So feeding costs a mother food, and through a short week it costs her energy.** This is the women 30–49 gap seen in
EG1 and FF4.

## What it means
- **The women 30–49 gap in ACL is a rule of nature, not a behaviour that emerged.** The mother alone carries the
  children's food by default, and the father helps only by choosing to give.
- **Real foragers differ.** Mothers' burden is shared by fathers' provisioning, kin, and children who mind the young
  (`docs/research/mothers_energy_2026-11-07.md`: Jang et al. 2022; Hurtado et al. 1992, record only).
- **For the council, a law question** (not a fault: the rule does what its comment says). Should dependents be fed
  from a household's food? Or should both parents' food count for their children? Either would be a general law, with
  no named role, tested in a copy with a sham and CI1's guards.
