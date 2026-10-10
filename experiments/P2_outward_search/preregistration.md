# P2 — Leave when there is no one: outward search by the unpartnered (candidate P2 of N8) (pre-registration, DRAFT for the creator's sign-off; nothing frozen, nothing run)

## Why

- **F1:** a third of worlds die out; single women almost never have an eligible man within sight (98%), though one
  usually exists elsewhere in the world.
- **F2:** perfect partner finding (a diagnostic, not a mechanism) cut extinction from 22 to 7 of 64: **finding partners
  is the main lever.**
- **C1 → MC1 → MC1-L:** keeping couples together raises births but not survival; at 256 worlds the moving camp is
  **genuinely weak** (effect −0.023, 95% interval [−0.086, +0.039], below half of F2's effect). Pair stability is not
  the limit; finding a partner is.
- **N8 evidence:** in small groups, when partners are scarce by chance, people go outside the group to find them
  (Kramer et al. 2017), and either sex may be the one to go (Hill et al. 2011). **Anchored in behaviour; no source gives
  how long people wait before leaving**, so only a form whose timing needs no chosen number may be designed. P1
  (walking to known people) is held: not anchored.

**What P2 tests:** whether a realistic, anchored change in *where* the unpartnered search, in the direction of
leaving rather than wandering, improves survival. **Not** whether survival can be forced: nothing in P2 is chosen to
make worlds live, and a null or a harm is a result.

## What the code does today (read-only reading of `acl/mind.py`)

A single adult who is **seeking** (adult, no partner, under 45) and has **no one to court within sight**
(`mates_in_reach == 0`) first looks a little further (sight + 2 tiles) for an eligible single and, if there is one,
walks toward them. **If there is no one, they take an exploratory step** to `dest`: a random point `reach` (3) tiles
away (`dx ∈ {−3, 0, +3}`, `dy ∈ {−3, +3}`), the same random destination used by the general curiosity/hunger explore
option. Its pull is `0.15 + 0.25·sociability + 0.15·boldness`, and it competes with every other option that week
(food, water, fire, family, home).

People keep up to 8 **remembered places** (`p.places`: "how good life has been there", updated weekly, slowly fading);
`p.home()` is the best of them.

## The change (nature, not culture): one direction, nothing else

In exactly that branch, a seeking adult with no eligible partner within sight, **the exploratory step goes outward,
away from the places they have known, instead of in a random direction.**

- **Unchanged:** when it fires (the code's own trigger), its pull (same formula), its length (`reach`, 3 tiles), and
  every other option, including the general explore option (still random), the pull back to family and partner, and
  the pull back home. Leaving therefore has to win against those pulls, as it would for a real person, and it costs
  what walking costs (food, water, safety); nothing is done to soften that.
- **Outward:** `world.step_away_land(p.loc, centre, reach, p)`, the step the code already uses for fleeing (never ends
  on water the person cannot cross), away from a centre of remembered places (decision 1).
- **Falls back to today's random step** when the person remembers no places, or stands exactly on the centre (no
  direction exists), or the branch's destination was a sea voyage (boats are left as they are).
- **No new number.** The trigger, pull, step and memory are all existing ones. Nothing says which sex leaves.
- **No new random draws:** the outward step is computed deterministically, so P differs from C only through behaviour.

**Anchors (rule 17):** dispersal outside the group when partners are locally scarce (Kramer et al. 2017); either sex may
disperse (Hill et al. 2011); random movement fails to keep contact at low density (Pearce 2014, from N5).

## Arms

| arm | what it is |
|---|---|
| **C** control | the new copy with the setting off (must reproduce the control world exactly) |
| **P** outward search | the change above |
| **S** sham | setting off, one extra random draw in week one (as HB1's, MC1's and MC1-L's sham) |

## Worlds (decision 2)

**Proposed: 256 new seeds, 2257–2512**, all three arms, 120 years (768 world-runs, about 9 hours). Sized from N8's
power table: 0.92 to detect half of F2's effect; MC1-L's sham confirmed the noise the table assumed (29% of worlds
changing fate by chance, against 28%).

## Measures (population beside every measure)

- **Rule 14, first:** C's extinction share on the new seeds.
- **Manipulation check (did the behaviour reach its target?), from a new read-only weekly observer:** among seeking
  adults (the code's own definition), the **share of seeker-weeks with an eligible single of the other sex within sight**
  (`perception`, 4 tiles; eligible as in the code: adult, unpartnered, not kin, within 15 years of age). P against C,
  per world, paired (decision 3).
- **Mechanism:** new pairings per seeker-year; women 16–45 without a partner (F1's measure); F1's yearly "single women
  with an eligible man somewhere but none in sight".
- **Primary outcome:** worlds died out (of 256), P against C, paired exact two-sided sign test; S against C likewise.
- **Effect size:** C − P extinction share with a 95% percentile bootstrap interval (10,000 resamples, fixed generator
  seed), against **half of F2's effect** on these seeds (0.34 × C's extinction share), as in MC1-L.
- **Costs (HF4's lesson: from the first week, every arm):** the hunger ledger (food held ÷ need at eating; starving
  share); deaths by cause (starvation, thirst, violence, exposure), so a cost of leaving shows if there is one.
- **Logging only (outside the world state, as HF4's ledger):** weeks the trigger held, and in how many of them an
  explore step was taken; in P, how many used the outward direction and how many fell back. This shows how often P2
  acts at all. The utility is unchanged, so the take-up should be similar in C and P.
- Births per woman-year; child deaths per birth; median population at years 40, 80, 119.

## Feasibility pilot (rule 12; behaviour only)

P and C on four further new seeds (2513–2516), 20 years, with the observer and the log. **Report** how often the trigger
holds, how often the explore step wins, and the share that went outward. **STOP** (the design returns to the creator)
if the outward step is taken in **fewer than 5% of trigger weeks**, which would mean P2 barely acts (decision 4).
Extinction is not looked at.

## Outcome rule (as MC1-L's)

| | reading |
|---|---|
| manipulation check fails | **the outcome is not read** (the change did not reach its target) |
| P fewer extinctions than C, sign test p < 0.05 | **outward search saves worlds**; its size is the effect estimate |
| P more extinctions than C, p < 0.05 | **outward search harms survival** (examined read-only, starting with the costs) |
| p ≥ 0.05 and the interval's upper bound for C − P is below half of F2's effect | **P2 is genuinely weak** |
| p ≥ 0.05 and the interval reaches half of F2's effect | **unresolved** at 256 worlds; the creator decides |

Beside it: S against C (should not reach p < 0.05; if it does, every reading carries that caveat).

**Whatever the result, P2 is not added to ACL's nature by this experiment.** That is a separate decision for the
creator, after the evidence.

## Hard stops

- Zero checks before any run: the setting off (with observer and log on) reproduces the control code's world exactly
  (state hash) on two of the new seeds; P and S differ from C.
- The copy's fingerprint is recorded and unchanged before and after every run.
- A pilot STOP stops everything.

## Audit against the rules

| rule | how P2 meets it |
|---|---|
| founding rule (nature, not culture) | a drive acting on local scarcity, attested across foragers; nothing about marriage, gatherings, or who moves |
| 11 (the creator signs off) | this is a draft; nothing is frozen or run before sign-off |
| 12 (feasibility before design) | the trigger's condition exists (F1: an eligible partner usually exists elsewhere); the pilot checks P2 acts often enough |
| 14 (baseline first) | C's extinction share reported before anything else |
| 15 (fresh seeds) | 256 seeds never run in any arm |
| 16 (traceable numbers) | every number from committed scripts (`run_p2.py`, `analyse_p2.py`) |
| 17 (anchored, not tuned) | only the direction changes; trigger, pull, step and memory are existing ones; no radius, wait or pull chosen |
| 18 (population beside measures) | median population and seeker counts beside every rate |
| 19 (corrections in the open) | appended, never edited away |
| sham and paired test; power | sham kept; paired sign test; 256 worlds from N8's power table |
| no tuning toward an answer | no number in P2 may be changed after any data; a null or harm is reported as such |

## Priors (written before any run; not predictions to test)

- **Assistant:** the trigger holds very often (most seeking weeks) but the exploratory step wins only some of them,
  against food, water and the pull home; the manipulation check probably passes but modestly, since a 3-tile step
  outward each week does not travel far before home pulls back. Extinction: no detectable benefit, likely "genuinely
  weak" or "unresolved"; a small hunger/thirst cost of leaving is possible. Held loosely (several recent priors were
  wrong).

## Order after sign-off

1. Freeze (`P2-frozen`). 2. Copy MC1's code (which carries HF4's ledger); add the setting `outward_search` (off by
default), the log and the observer; zero checks; smoke test on a throwaway seed. 3. Feasibility pilot (2513–2516).
4. If it passes, the main run (C, P, S on 2257–2512). 5. Report in the frozen order; index, roadmap, picture, book.

## Decisions for the creator

1. **"Away from the places they have known": the centre to step away from.**
   - **(a) the centre of all remembered places** (up to 8; the mean position on the wrapping map, taken per axis; no
     weights), **proposed**: closest to the evidence's "leaving the group's range", and not tied to one tile; or
   - **(b) home**, the single best remembered place (`p.home()`, existing): simplest, but the pull back home works
     directly against it, and a person standing at home has no direction (falls back to random).
2. **Worlds:**
   - **(a) 256 new seeds 2257–2512, all three arms, proposed** (about 9 hours; clean, independent of every result seen);
     or
   - **(b) reuse MC1-L's seeds 2001–2256 and its C and S runs** (verified by reproducing their saved world hashes),
     running only P (about 3 hours). The weekly encounter observer would then be missing from C, so the manipulation
     check would use F1's yearly snapshot (women only, once a year) instead.
3. **Manipulation threshold.** No source gives a size, so a fixed size would be chosen. **Proposed:** the encounter
   share is higher in P than in C, paired over worlds, sign test p < 0.05 (a direction, not a chosen size). Alternative:
   a fixed rise (e.g. +25% relative), which would be a number without an anchor.
4. **Pilot stop:** outward step in fewer than 5% of trigger weeks (proposed), or no pilot gate (report only).
