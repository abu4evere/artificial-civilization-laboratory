# DF1: who feeds the children, and what does it cost them? (frozen plan)

**A read-only audit of nature v16.** Council round 77 chose it unanimously as a separate study alongside PM1
(`docs/debate_round77_after_ff4_mp1_2026-11-07.md`). **Nothing in nature changes, and DF1 decides no law.**

## Why
- **EG1 and FF4:** women aged 30–49 are blocked from food by energy alone in 0.119 of their starving weeks, men in
  0.044–0.055. FF4's fix helped men (ratio 0.80) but not women (1.02).
- **The code:** ACL has no time or energy cost of nursing or carrying infants (`docs/research/mothers_energy_2026-11-07.md`).
- **The feeding rule** (`biology.body_phase`):
  - a child's **caregiver** feeds them first each week, as far as the caregiver's care trait takes them;
  - at birth the caregiver is **the mother** (`biology.py`: `child.caregiver = mother.id`);
  - the caregiver role passes to someone else only when the caregiver dies (`assign_caregiver`);
  - children stop being dependents at 12.

  A father feeds his children only by choosing to give.
- **A short week halves energy recovery**, and a forage week costs 25 or more.

## Design
- **Code:** `code_v16`, unchanged. One arm. LP. **Seeds 25101–25132** (32 new seeds). 200 years; years 100–200 counted.
- **The observer:**
  - reads the body phase's own ledger (`world.ledger`: need, food held before, deficit, food fed out);
  - reads `world.dependents` at the start of each body phase;
  - reads the give events (who gave food to whom).

## Measures (per person-week of the grown, 16+; by sex and age band 16–29, 30–49, 50+)
- **Caregiving:** the share of person-weeks with dependents; the number of dependents.
- **Feeding:** the food fed out to dependents.
  - **Primary: a short week caused by feeding.** The person held at least their own need before feeding, yet ended
    the week short (deficit > 0.05) after it. It is counted per 1,000 person-weeks of the grown, by sex. The contrast
    is **women − men** (a world bootstrap, 10,000 draws, NumPy seed 20261128).
- **Gifts:** food given to one's own children (under 12) by gift, by sex.
- **Caregivers by kind:** the mother, the father, or someone else (after a death).
- **The energy link:** the share of a person's next-week decisions where food was blocked by energy alone (EG1's rule,
  read with code_v16's own costs), after a feeding-caused short week against after other weeks.

## Reading (frozen)
- **"Feeding drives the gap":** women's feeding-caused short weeks per 1,000 exceed men's, and the difference's lower
  bound is above 0. In addition, women's share of those weeks is at least 0.75.
- **"Feeding does not explain it":** the difference's interval includes 0, or men's rate is higher.

## Zero checks (hard stops)
1. **Read-only:** world and random-stream hashes with and without the observer (20 and 60 years).
2. **Ledger check:** in a 30-year world, food fed out by the ledger equals the change in the dependents' held food from
   feeding, within 1e-6 per person-week.
3. **Reload is exact.**
4. **All 32 worlds** are present under one fingerprint.

## A blind recompute
GPT, Gemini and DeepSeek recompute the primary, the women − men difference and the reading, from per-world counts.

## Prior (the assistant)
"Feeding drives the gap," about 85%. The mother is the sole caregiver by rule, so nearly all feeding-caused short weeks
are women's.

## Sign-off (7 November 2026)
The assistant, under the creator's standing permissions. Council round 77 (all three: yes, alongside PM1); the
assistant 85%. Frozen as `DF1-frozen` before any code or data.
