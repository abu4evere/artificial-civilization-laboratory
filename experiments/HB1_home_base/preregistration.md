# HB1 — A shared home base (candidate L2 of N6) (pre-registration, SIGNED OFF and frozen as `HB1-frozen`)

**Signed off by the creator (October 2026):** couples only; return distance `reach` (3 tiles); the outcome rule (paired exact sign test at p < 0.05, with a sham arm) and the feasibility pilot, as written. Nothing has been run.

## Why

- **C1:** couples are apart about half their weeks; foraging splits them; the pull back is outbid by food.
- **N6:** real foragers return to a central place each night (Garg et al. 2021; Kelly 2013); spouses often forage apart
  by day but share a camp (Marlowe 2007; Hill et al. 2011; Dyble et al. 2015). At ACL's weekly step a real couple would be
  together almost every week.
- **H1:** partners' personal homes coincide only half the time and change every five or six weeks.
- **T1:** adding a pull toward a partner's position did not keep couples together: food outbid it. A slight change also
  flipped the fate of 19 of 64 worlds (p = 0.36): differences of a few worlds are noise.

HB1 tests the change the evidence points to: **a couple shares a home, forages out from it, and comes back to it.**

## The change (nature, not culture)

For **partnered adults only** (the scope proposed; see decision 1):

1. **The couple's home.** Each week, a couple's shared home is the place, among those either partner remembers, with the
   **highest combined value** (the sum of the two partners' remembered values for it; zero for a place one of them does
   not remember). If neither remembers anywhere, there is no shared home that week. This is ACL's existing personal home
   (`person.home()`, the place where life has felt best) extended to the pair; **no new number is introduced**, and the
   home moves when another place comes to stand out for the two of them.
2. **Return each week (central-place foraging).** After everyone has acted, each partnered adult who is **within `reach`
   (3 tiles) of the couple's home** goes back to it. The week's action has happened where they went (they foraged,
   gathered, talked or gave there); only where they end the week changes. `reach` is the existing distance a person can
   travel and still act in a week, read here as a day's trip out and back. A partner further away than `reach` (on a
   longer trip) does not return that week.
3. Nothing else changes: how people choose actions, foraging yields, the pull toward loved ones, courtship, conception,
   children following their carer, crowding.

**Culture is not written:** nothing says who moves to whom at marriage (no matrilocal or patrilocal rule), who forages
for what (no division of labour), or that anyone shares food at home. The shared home is chosen from both partners'
memories alike.

**Anchors (rule 17):** returning to a central place each night (Garg et al. 2021; Kelly 2013); spouses co-resident
(Hill et al. 2011; Dyble et al. 2015). No value is tuned: the home is ACL's existing place memory, the return distance is
ACL's existing `reach`.

**Known consequence, reported, not tuned:** ACL raises the chance of illness by 15% for each person beyond four on one
tile. Families living together will be more crowded and may fall ill more. If that matters, it is a finding about the
model's crowding rule, to be examined separately, not adjusted here.

## Arms (the noise is measured, T1's lesson)

| arm | what it is |
|---|---|
| **C** control | F1's replays of the 64 seeds (already run, verified) |
| **H** HB1 | the change above |
| **S** sham | the control code, plus a single extra draw from the world's random generator in the first week, changing each world's history without changing any rule |

The sham shows how many worlds change fate by chance alone when a world's history is perturbed. HB1 is read against
both C and S.

## Feasibility pilot (rule 12; manipulation only, no outcomes read)

Before the main run: HB1 on four new seeds (1201–1204) for 20 years, with C1's observer. **Pass** if couples are apart in
at most half as many couple-weeks as C1 found (≤ 24%). **Fail:** stop, and the design returns to the creator. Extinction
is not looked at in the pilot.

## Main run

The 64 F1 seeds, 120 years, A2-full people, arms H and S (C already exists). Observers: F1's (whole run) and C1's (first
40 years), both read-only. Zero checks before any data: with HB1 off, the copy reproduces the control world exactly; the
sham differs from the control.

## Measures (population beside every measure)

- **Manipulation check:** couples apart per partnered, non-pregnant woman-week (`C1/reconcile.py`'s measure): must fall
  to **at most half** of the control's 57.8% (≤ 28.9%). Otherwise the outcome is not read.
- **Primary:** worlds died out (of 64): H against C, and S against C, each with the paired worlds that changed fate and an
  exact two-sided sign test.
- Births per woman-year; women without a partner; median population at years 40, 80, 119; child deaths per birth;
  starvation; illness deaths (the crowding consequence).

## Outcome rule (proposed; the creator decides)

| | reading |
|---|---|
| H fewer extinctions than C, sign test p < 0.05 | **HB1 reduces extinction** (magnitude reported: worlds saved and lost) |
| H more extinctions than C, p < 0.05 | **HB1 increases extinction** (examined read-only: crowding, food near home) |
| p ≥ 0.05 | **no detectable effect on extinction** at this sample, whatever the counts |

Beside it: S against C (the sham's own sign test should not reach p < 0.05; if it does, the noise is larger than the
test assumes and the result is reported with that caveat), and births and couples apart, which show whether HB1 worked
through the mechanism it targets.

## Priors (written before any run; not predictions to test)

- **Assistant:** the manipulation works (couples apart falls sharply, since partners within 3 tiles of home end each week
  there); births rise; extinction falls but the sign test may not reach p < 0.05 with 64 worlds, since F2, with perfect
  partner finding, saved 17 and HB1 does nothing for finding partners. Illness from crowding may offset part of the gain.

## Order after sign-off

1. Freeze (`HB1-frozen`). 2. Copy the code; add the setting and the sham; zero checks; smoke test on a throwaway seed.
3. Feasibility pilot (seeds 1201–1204). 4. If it passes, the main run. 5. Report in the frozen order; index, roadmap,
picture, book.

## Decisions for the creator

1. **Scope:** couples only (proposed; the question is pair co-residence, and singles' searching depends on wandering), or
   everyone returns to their own home each week (closer to real central-place foraging, but a larger change that may
   reduce mate finding)?
2. **The return distance:** `reach` (3 tiles), as proposed?
3. **The outcome rule:** paired sign test at p < 0.05 with a sham arm, as proposed?
4. **The feasibility pilot** as proposed (manipulation only, four new seeds)?
