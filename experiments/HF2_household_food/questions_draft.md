# HF2 — Where does HB1's hunger come from? The household food balance (read-only; DRAFT for the creator's sign-off)

**Asked by the creator (October 2026), after HF1.** No fixes, no tuning, no code changes. Nothing has been run.

## Why

HB1 (a shared home base) kept couples together and raised extinction (33 of 64 against 22; p = 0.043), with more adult
starvation (714 against 412 adult starvation deaths in years 0–39). HF1 (read-only, holdout on new seeds) **did not
confirm** local depletion: the land near HB1's homes was only about 3% less full (0.970 / 0.976). The hunger is real and
repeats (179 / 191 against 100 / 109 adult starvation deaths in HF1's two sets), but its cause is open. HF1 left two
leads, neither yet a finding:

- **Meat:** hunting fell under HB1 in both of HF1's sets (hunts per person-year −40% and −22%).
- **Mouths to feed:** HB1's couples had more children (HB1 `explore.md`: births per partnered woman-year about 0.38
  against 0.28–0.34), and in ACL carers feed their dependants before themselves.

HB2 is not designed until the cause is found (HF1's frozen rule).

## The code, read before any data (`code_hb1`, the same in both arms)

Each week, in order:
1. **Food in** during actions: foraging (`forage` event, `got`); hunting (meat split equally among the party, each
   capped by what they can carry; `hunt` event: party, success, meat); taking from a store or stash (`take`); gifts
   received (`give`, amount); theft (`steal`, amount).
2. **Food out:** gifts given, theft suffered; loose food spoils 4% a week.
3. **Carers feed dependants first** (`biology.body_phase`): a dependant is a living child whose caregiver is that adult
   (under 12). If the carer cannot cover their own need and all their dependants' shortfall, they keep a share for
   themselves set by their **care** trait: the more caring, the more goes to the children.
4. **Everyone eats** what they have left; a shortfall of more than 5% of need counts as a starving week.

## Questions

All in the first 40 years, arms H (HB1, `home_base = 1`) and C (the same code, settings off), per adult-week (age 16+)
unless stated.

1. **Food in, by source:** food gained per adult-week from foraging, hunting, stores, gifts received and theft; total.
   The share from meat.
2. **Mouths:** dependants per carer-week; dependants' need as a share of the carer's food in hand before feeding
   (approximated from the week's food in and the carer's stock); the share of carers who could not cover both.
3. **Who starves:** starving share of adult-weeks for **carers** (one or more dependants), **partnered adults without
   dependants**, and **unpartnered adults**; adult starvation deaths in each group.
4. **Food out:** food given away per adult-week, and to whom (own dependants are fed in step 3, not by gifts; gifts to
   partner, other kin, others); theft suffered.
5. **Hunting:** hunts per person-year; share of adult-weeks on a hunt; meat per hunter per hunt; distance from the
   couple's home to the hunt.

## Decision rule (proposed; read on discovery and holdout separately)

Let **excess** be H's starving adult-weeks per 1,000 adult-weeks minus C's.

| | supported if, in **both** sets |
|---|---|
| **Mouths** | dependants per carer-week in H ≥ 1.2 × C's, **and** at least two thirds of H's excess starving adult-weeks fall on carers |
| **Meat** | food from hunting per adult-week in H ≤ 0.8 × C's, **and** total food in per adult-week lower in H than in C |
| **Both** | both rows hold |
| **Neither** | neither holds in both sets: the hunger has yet another cause; reported as such, the creator decides |

(How the excess is split by group: each group's starving adult-weeks per 1,000 adult-weeks in H minus in C, weighted by
H's adult-weeks in that group; the share falling on carers is that group's part of the total.)

## Worlds

| set | seeds | runs |
|---|---|---|
| **Discovery** | 501–516 (HB1's, F1's and HF1's first 16) | H and C, 40 years |
| **Holdout** | **1401–1416, new**: the leads came from HB1's 64 seeds and HF1's holdout (1301–1316), so neither may serve as the holdout here (rule 15) | H and C, 40 years |

## Hard stops

- Observer read-only: state hash with and without it after 20 years, both arms, two seeds.
- Replays reproduce: on discovery, H matches HB1's saved populations and C matches F1's (years 10–40).
- Code fingerprint unchanged.

## Priors (written before any run; not predictions to test)

- **Assistant:** **mouths** supported, meat not. HB1's couples had more children and carers feed them first; hunting fell,
  but meat may be a small share of ACL's food (E8.2 found tools add little; hunting's share of food is to be measured
  here, not assumed). HF1's prior was wrong, so this one is held loosely.

## Decisions for the creator

1. **The decision rule** and its thresholds (1.2 × dependants; two thirds of the excess on carers; hunting ≤ 0.8 ×).
2. **Holdout on new seeds 1401–1416.**
3. **First 40 years** (as HF1).
