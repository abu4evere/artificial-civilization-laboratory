# E13R — Replicating E13 with a safeguard that can be measured: design (DRAFT, not frozen)

**Status:** reviewed by the creator; decisions recorded below. Ready to freeze as `E13R-frozen` on the creator's final
sign-off, before any code is written. No E13R code exists and nothing has run.

## 1. Why

E13 let adults learn the foraging of visibly better-fed neighbours (B2). Against the control it gave the strongest
lead ACL has produced: planner-autumns 4.1×, repeat planning 6.3% against 0.9%, carers holding 20+ up 8.1 points,
habits higher in all four worlds. It is formally failed: its leak test compared adults who never once saw a better-fed
adult forage, and over 120 years that group was empty.

Because each world is deterministic, and E13's zero check showed the new code with copying off reproduces the control
exactly, it is already established that **switching copying on caused the change**. E13 left two questions open, and
E13R asks only these:

1. **Route.** Did the effect travel only through the designed channel: an observer's own foraging habit, changed by
   watching? Or does the mechanism touch the world in some other way?
2. **Source.** Is what spreads a preparation practice learned from planners, or a general "forage while things are
   good" habit learned from anyone better fed? Planners' neighbours foraged only 1.07× as much in E13, which leaves
   the second reading open.

E13R adds no new kind of learning. Its mechanism is E13's, unchanged in strength.

## 2. What went wrong in E13's leak test, and the rule that follows

E13's test defined its group by a lifetime of exposure, and almost everyone is exposed at some point. A behavioural
group test has a second, deeper problem: people who never watched still live among people who did, and are fed,
crowded or outcompeted by them. They can legitimately change, so a difference would not prove a leak either.

**New rule for this and later experiments:** every test states its minimum sample before the run. A test below its
minimum is reported as **unscorable**, separately from passed or failed. A hard-fail test that is unscorable still
counts as failed, so the strictness stays, which is why E13R's hard tests are built so that they cannot come out empty.

## 3. Arms

Base world A2-full (E9's code, anticipation weight 1.0), as in E13. Models are always chosen deterministically: the
adult within sight (`perception`, 4 tiles) with the most food in hand, more than the observer's own, lower id on ties.

| arm | B2 | model pool | purpose |
|---|---|---|---|
| **A** control | off | — | baseline |
| **B** any better-fed | on | as E13 | replication |
| **S** sham | runs fully, **writes nothing** | as B | route test (L1) |
| **N** not planners | on | only adults holding **under 80** food | source test |
| **P** planners only | on | only adults holding **80 or more** food | source test |

80 is E9.3's existing planner threshold, applied to food a neighbour can see in hand at that moment. No new number is
introduced. Arm C from E13 (children-alive filter) is dropped, by the creator's decision: the filter left few models, the signal
collapsed and one of its worlds died out; the runs go to replication power instead.

**Seeds:** 8 new seeds, 501–508, 120 years, fixed now; a world that dies out counts as it falls. E13's seeds are not
reused, so this is a true replication. Cost: 40 runs at about 6 minutes each, 4 at a time, roughly an hour.
**[DECIDE: 8 seeds unless the creator asks for more]**

## 4. Validity (hard fail unless stated)

- **V1** Probe read-only: state hash with and without the probe, 20 years, both codes.
- **V2** Zero check: E13R code with B2 off reproduces Arm A's population at every 10-year sample, all seeds.
- **V3** Code unchanged during runs (fingerprints before and after); no crashes.
- **L1 Sham (route, whole world).** Arm S, where the copying step does everything except write the habit, must give a
  **state hash identical to Arm A at year 120 in all 8 seeds**. This proves that choosing models, looking and computing
  the lesson change nothing at all. Cannot be empty.
- **L2 Instrumented check (route, each update).** In Arm B, seed 501, the first 20 years: before and after every copying
  step, snapshot every person's full state and the world's random state. The only difference allowed is the one
  forage habit entry of the observer. At least 1,000 copying updates must be checked, or L2 is unscorable and so
  failed. Plus a unit test: an observer with no qualifying model foraging that week is left exactly unchanged.

Together L1 and L2 answer E13's open question directly: any difference between A and B can only have started as a
change to a watcher's own foraging habit. What follows from that through ordinary life, people eating, sharing and
competing differently, is the effect being studied, not a leak.

## 5. Order of reading (binding)

Validity and route (V1–V3, L1, L2); then **the replication headline**; then the source test; then manipulation check,
neighbours, planners, carers; children's winter starvation last, read only if the links before it hold in Arm B.

## 6. Predictions

### Replication (Arm B against Arm A, pooled over 8 seeds)

- **R1 Headline (creator's decision):** the share of planner-autumns followed by planning the next autumn is at least
  3× Arm A's and at least 3%, with at least 20 planner-autumns in B (minimum sample; below it, unscorable). E13's 10%
  is not kept: it was frozen before the size of any effect was known, and E13 reached 6.3% against 0.9%. Repeat planning
  measures whether a lesson survives its own success (E9.4); it is the headline because E13 was framed by it.
- **R2** Manipulation check: habit value for autumn foraging with 2+ weeks of food higher than A in at least 6 of 8 seeds.
- **R3** Planner-autumns at least 2× A's.
- **R4** Carers holding 20+ at least 5 points above A.
- **R5** Planners' neighbours forage in the next autumn at least 1.1× A's (missed in E13; kept to see if it was noise).
- **R6** Children's winter starvation at least 20% below A, read only if R2, R3 and R4 hold.

### Source (no winner predicted; both answers are findings)

For each of planner-autumns and habit value, the share of B's effect each arm keeps:
`share_N = (N − A) / (B − A)`, `share_P = (P − A) / (B − A)`, pooled. Read only if B's effect replicates (R2 and R3).

| result | reading |
|---|---|
| N keeps ≥ 0.5, P < 0.5 | a general "forage while things are good" habit, learned from anyone better fed, carries the effect |
| P keeps ≥ 0.5, N < 0.5 | learning from planners carries it: a preparation practice spreading |
| both ≥ 0.5 | either source is enough |
| both < 0.5 | it takes the mix; no single source |

**Dose caution, stated now:** planners are rare, so Arm P will make far fewer copying updates than B or N. Updates per
arm are reported, with effect per 1,000 updates, so that "P did less" is not mistaken for "planners teach less".

**Priors, written before the run** (the E2 custom). Creator: leans toward N, because the weak neighbour effect in E13
(1.07×) does not look planner-specific. **[DECIDE: the creator's odds as numbers, if wanted]** Assistant: 60% that N
keeps most of the effect (general habit), 25% both, 15% P alone.

Even a P result shows only that learning from very well-stocked models is enough, within this mechanism; calling
planners the founders of a practice would need lineage evidence (who learned from whom, across generations).

## 7. Descriptive measures (reported, not scored)

- Copying updates per arm, by the model's food level and season (what situations are being taught).
- Dose-response in B: adults' habit value by how many copying updates they received.
- Repeat planning by whether the planner's own model that autumn was a planner.

## 8. What E13R can and cannot conclude

- If L1 and L2 pass and R1–R4 hold: copying the visibly successful reliably moves preparation-related behaviour
  between adults, through the designed channel only. The transmission bottleneck counts as crossed only if R3 (more
  planners) holds; R1 alone would show that lessons survive success, not that they spread. It is not evidence of
  self-sustaining culture: nothing yet tests whether the practice persists if copying were later switched off, or
  across generations without it. The cap stays: this would show that social learning solved
  the transmission bottleneck E12 identified, not civilization.
- If R1–R4 do not hold on new worlds: E13's lead was specific to its four worlds.
- The source test says what is passed on, within this mechanism and this strength only.

## 9. Code changes (after freezing only)

Copy E13's code to `code_e13r`, then:
- `b2_mode` 3 (N: candidates hold under 80) and 4 (P: candidates hold 80+);
- `b2_write: bool = True`, where False (sham) runs the copying step to the point of writing and returns;
- nothing else. Update counts come from the probe, which applies the same model rule each week (as E13's probe did),
  so the world's code writes no extra records.

No new random draws. Each arm's code is checked by V2, L1 and L2.
