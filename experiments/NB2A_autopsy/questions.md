# NB2-A: why did NB2's people die out? A read-only autopsy (frozen plan)

**Frozen** as git tag `NB2A-frozen`, before any code or data.
**Sign-off:** the creator, 10 November 2026: "go ahead check the data first then add them" (the feelings).

**Why:** NB2 (frozen reading: not viable) lost most of its worlds:
- extinct out of 16: c 4, s 9, o 15, l 11, n 13;
- killing deaths 910× and starvation deaths 2.5× v17's (n, years 100–600).

Before adding feelings (empathy, guilt, love of one's child, shame, curiosity, an inborn reluctance to harm), find out
what killed people. Already seen in NB2's own records:
- grown people attack in 0.4% of weeks in the first century (v17: 0.0%), and steal in 0.3% (v17 0.0%);
- gathering falls from 16% to 6%;
- in the code, every attack gives the attacker a feeling of +0.1, and a kill gives +0.3 × temper − 0.2 × kindness.

## Method: an exact replay with read-only recorders
- **What runs:** NB2's own code (`code_nb2`, unchanged), arms c, s and n, seeds 25601–25616, each world to its end
  (extinction or year 600). Recorders only read.
- **Validity:** every replayed world must end with the same world fingerprint as NB2's phase-1 result. If any differs,
  the recorders are not read-only and nothing is concluded.
- **Recorded:**
  1. **By decade:** population, births, and deaths by cause and age group (under 12, 12–15, 16 and over).
  2. **Every attack and kill:**
     - the attacker's age group and kinship to the target;
     - the attacker's grudge toward the target just before;
     - whether v17's old brain would have offered that attack at all (grudge > 0.15);
     - the attacker's hunger, anger and temper;
     - whether it ended in a kill, and of whom (the target or the attacker).
  3. **Every death by starvation:**
     - age group;
     - food held;
     - whether kin within reach held more than twice their own need;
     - the share of the last 8 weeks spent foraging.
  4. **The action mix of children aged 3–11 and teens 12–15,** by decade (NB2 recorded only the grown's).

## Readings (descriptive; this is an autopsy, not a test)
- **The share of deaths by cause** in s and n against c, over each world's whole life.
- **"Violence drives the collapse"** is read if killings are at least a quarter of all deaths of people 12 and over in
  n, and more than 5 times c's share.
- **"Starvation drives it"** is read on the same terms for starvation.
- **How many attacks the old brain would never have offered** (grudge ≤ 0.15): the share in s and n.
- Everything is reported with the number of worlds and events beside it.

## The assistant's prior
- Violence drives the collapse: about 60%.
- Most attacks would never have been offered by the old brain: about 85%.
- Starvation drives it: about 35% (both can hold).

## Correction 1 (appended 11 November 2026, after the data; the frozen text above is unchanged)
- **What happened:** the frozen validity check failed. 2 of the 48 replays (n:25606 and n:25611) end in the same
  week, with the same extinction, but with a different world fingerprint from NB2's phase-1 result.
- **Diagnosis:**
  - n:25611 was replayed on the creator's PC with **NB2's own runner and no recorders at all**. Its fingerprint also
    differs from the cloud original (local 5d56cbd0…, cloud 368a0207…).
  - So the world itself does not reproduce bit for bit across machines. This is most likely floating-point
    differences in the numpy arithmetic of the neural arms on different cloud CPUs.
  - The recorders are therefore not the cause. The 46 replays made with recorders on other cloud machines match NB2
    exactly; if the recorders changed anything, nearly every world with an attack would differ.
- **What is done** (not the frozen rule, stated as a deviation):
  - the results are read on the **46 exact replays** (`results.md`, `--exact-only`);
  - **all 48** are reported beside them (`results_all48.md`, `--all`);
  - any reading that differs between the two is reported as such.
- **For later studies:** a replay is checked against a replay made on the same machine, not across machines. Arms with
  neural brains are not assumed to replay exactly across cloud machines.
