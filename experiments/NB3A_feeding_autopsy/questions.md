# NB3-A: why do the feeling people starve? A read-only autopsy (frozen plan)

**Frozen** as git tag `NB3A-frozen`, before any code or data.
**Sign-off:** the creator's standing go-ahead ("do not ask me go ahead bro"; "keep working on project", 11 November
2026).
**Council:** round 85 (`docs/debate_round85_after_2026-11-11.md`), GPT. Its six changes are all taken. GPT's "has food
but does not eat" and "child not fed" were reworked to the world's real mechanics (below).

**Why:** NB3 (frozen reading: f not viable) ended the killing with an inborn reluctance (H). But with all feelings
(arm f, years 100–600):
- starvation is 44% of all deaths (v17 19%);
- starvation deaths per 1,000 living-years are 2.73× v17's [2.39, 3.13];
- child starvation is 2.28× [1.86, 2.80];
- survival to 16 per birth is 0.781 (v17 0.875);
- gifts to kin's children are at v17's level (×0.98);
- the population is 0.49 of v17's, the main reason f fails the viability rule.

NB2-A already saw starvation beside kin with plenty. Before building the next brain part, find out **how** these
people starve.

## Method: an exact replay with read-only recorders (as NB2-A)
- **What runs:** NB3's own code (`code_nb3`, unchanged), arms **c** (the primary comparison), **fH** (the mechanistic
  comparison) and **f**, seeds 25801–25816. Each world runs to its end. Recorders only read.
- **Validity:** each replayed world must end with NB3's phase-1 world fingerprint.
  - NB2-A found that 2 of 48 worlds drift across cloud machines. So the rule is fixed now:
    - worlds that match are read;
    - worlds that differ are reported beside them, not read;
    - if more than 4 of 48 differ, nothing is concluded.
  - The number of worlds read per arm is reported.

### Recorded
1. **By decade, per arm:**
   - population, births, and deaths by cause and age group;
   - **the food economy:** food gained per adult-week by foraging, gathering, hunting and taking from stashes; food
     eaten; food given (to own children, other kin, others); food stored; food lost to spoiling.
2. **Food received by each child under 12, per week:** from whom (a parent, other kin, others) and how much.
   Reported as the share of children who received nothing in 8 weeks, by arm.
3. **Every starvation death, over its last 24 weeks** (the frozen readings use 8):
   - each week: age group, health, food held, need, food eaten;
   - the week's act;
   - whether a food act (forage, gather, hunt, take) was offered, and whether it was chosen;
   - food gained;
   - stashes owned, and food in them;
   - whether kin within reach held more than twice their own need;
   - the season, and the year's hardness: the world's own `drought` (wetness < 0.65) and `hard_winter` (hardness >
     0.1) events, and the growing conditions (`world.weather`, 0.65–1.25);
   - whether the network changed the top choice.
4. **Every child death by starvation:** the caregiver each week (alive or not, on the same tile or not, food held,
   the food fed to dependents in the body phase, from the world's own read-only ledger, `world.ledger`) and the
   caregiver's own act.
5. **Matched survivors:** for each starvation death, one living person of the same world and age group, alive that
   week and for 8 more weeks, drawn by a recorder-only generator (`numpy.random.default_rng([seed, 85])`, never the
   world's), with the same records over the same 24 weeks.

## Readings (descriptive; an autopsy, not a test)
**What the world already does** (read in `code_nb3/acl/biology.py`, before freezing):
- eating is automatic: each week everyone eats what they hold, up to their need;
- each caregiver first feeds their dependents (children and wards in their care, wherever they are), in full if they
  can. If not, they share by their "care" gene.

So "has food but does not eat" cannot happen by construction; it is kept as a **code check** (expected 0). And a child
in care starves only if its caregiver is short or gone. The patterns follow from this.

**The six patterns.** Weeks 8 to 3 before death are "early"; the last 2 weeks are left out where marked, since weakness
may then be the cause.
- **"cannot find":** in the early weeks, food acts were chosen but brought food in fewer than half of them;
- **"does not try":** in the early weeks, a food act was offered in most weeks, health was 30 or more, and a food act
  was chosen in fewer than a quarter of them;
- **"not shared":** in at least 2 of the last 8 weeks, kin within reach held more than twice their own need;
- **"caregiver short":** a child in care whose caregiver, in at least 2 of the last 8 weeks, held less than their own
  need plus this child's want;
- **"no caregiver":** a child under 12 who, in at least 2 of the last 8 weeks, had no living caregiver;
- **"hard times":** died in a year the world marked `drought` or `hard_winter`, or with growing conditions below 0.80
  (the lowest quarter of their range).

**A pattern "leads"** if, among f's starvation deaths, its share is:
- at least 25%;
- at least 1.5 times its share among c's starvation deaths;
- **and** at least 1.5 times its share among f's matched survivors (judged on the same weeks).

**Also reported:**
- each pattern as deaths per 1,000 living-years, f against c and fH (world bootstrap, 10,000 draws, NumPy seed
  20261114);
- the overlaps between patterns;
- the 24-week versions;
- the food economy per adult-week, with intervals.

## The assistant's prior
- "Caregiver short" leads: about 45%.
- "No caregiver" leads: about 25%.
- "Not shared" leads: about 45%.
- "Does not try" leads: about 35%.
- "Cannot find": about 20%.
- "Hard times" leads: about 15%.
- Food gained per adult-week in f below c's: about 60%.
- GPT: child not fed 60%, not shared 55%, does not try 45%, cannot find 25%, hard times 15%.

## Correction 1 (appended 12 November 2026, after the data; the frozen text above is unchanged)
- **The frozen validity rule failed.** 10 of 48 replays ended with a world fingerprint different from NB3's (more than
  4), so by the rule nothing is concluded. That result is kept: `results_frozen_rule.md`.
- **The diagnosis** (`replay_plain.py`; long-run 43164318860):
  - the 10 worlds were replayed with NB3's own runner, unchanged and with no recorders. 7 of the 10 also ended with a
    different fingerprint from NB3's originals. Long neural worlds do not replay bit-exactly on the cloud, recorders
    or not (NB2-A's correction 1 saw the same in 2 of 48);
  - **all 48 autopsy replays reproduce NB3's history exactly:** the same living-weeks and the same count of every
    cause of death over years 100–600, and the same final week. The 10 plain replays do too. The drift is in the
    last bits of the final state, not in what happened.
- **Correction 1 reading:** a replay is read if its history matches NB3's exactly (living-weeks, deaths by cause,
  final week). The fingerprint test was meant to show that the recorders do not change the world, and this shows it
  directly. All 48 are read. The results are labelled "Correction 1" (`results.md`), beside the frozen-rule result.
