# P2 — Feasibility pilot: STOP

**Frozen gate (`P2-frozen`, decision 4):** stop if the outward step is taken in fewer than 5% of trigger weeks.
**Result:** taken in **865 of 22,284** trigger weeks in P (**3.9%**). **STOP:** the main run is not started; the design
returns to the creator. Extinction was not looked at. Tables: `output_pilot/pilot.md`, from `run_p2.py pilot`
(seeds 2513–2516, 20 years, arms C and P; zero checks passed beforehand, `output/zero.txt`).

## What the pilot showed (behaviour only)

| | C | P |
|---|---|---|
| seeker-weeks (4 worlds, 20 years) | 22,471 | 23,352 |
| trigger weeks (seeking, no one to court in sight, no eligible single within sight + 2) | 21,426 (95% of seeker-weeks) | 22,284 (95%) |
| of which P used the outward direction / fell back to random | – | 19,168 / 3,116 |
| an explore step to the branch's destination was taken | 1,447 (6.8%)* | 1,189 (5.3%), of which outward **865 (3.9%)** |
| seeker-weeks with an eligible single within sight | 3.4% | 2.7% |
| people newly partnered | 44 | 42 |

\* In C the branch's random destination is shared with the general explore option, so C's figure counts both; P's
counts only the branch's own step. (Written in `analyse_p2.py` before data.)

1. **The trigger holds almost always:** 95% of a seeker's weeks have no eligible partner in sight (F1: 98% for single
   women). The condition P2 targets is the normal state of a single adult in ACL.
2. **The search itself is rarely chosen.** The seeker branch's pull (0.15 + 0.25·sociability + 0.15·boldness) is outbid
   most weeks by food, water, warmth, family and home: under 7% of trigger weeks end in any explore step even in C.
   Changing only the direction, as frozen, therefore changes behaviour in about 4% of the weeks it is meant to act in.
3. The encounter and pairing figures differ little between arms over 4 worlds and 20 years; they are noise at this size
   and are not read.

## What this means

P2 as anchored (direction only, timing and pull unchanged) **barely acts**: the bottleneck is not *where* seekers search
but **how seldom searching wins** against the other needs of the week. This is T1's lesson again (the partner pull was
outbid by food), now for finding a partner rather than staying with one.

## For the creator (nothing chosen; any change needs a new sign-off, new pilot seeds, and no tuning toward the gate)

- **(a) Record P2 as not feasible in this form and stop.** The finding stands: seekers in ACL spend over 90% of their
  weeks on other things.
- **(b) Evidence first (rule 17):** how much of their time unpartnered foragers spend travelling to meet others, or
  visiting other camps, compared with food getting. Only an anchored figure could justify changing the search's pull;
  without one, raising it would be tuning.
- **(c) A direction-only variant:** a seeker with no one in sight takes *every* exploratory step outward (the general
  curiosity/hunger explore option too), still with no new number. It would act somewhat more often (C's 6.8% is the
  ceiling for explore steps in these weeks), but it also redirects searching for food, and it would be a new design,
  not a rescue of this one.
- **(d) Return to N8's other candidates** (P1 held for lack of evidence; P4 borderline; P5 size).

**Assistant's view:** (b) before anything else; the pilot says the question is now *how much* people search, not
*where*, and that is a number only evidence may set.
