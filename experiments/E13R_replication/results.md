# E13R — Replicating E13 with a safeguard that can be measured · Results

Base world A2-full (E9 code, anticipation 1.0). Arms: A control; B any better-fed model (E13's B2); S sham; N models holding under 80; P models holding 80+. Seeds 501–516, 120 years. Frozen as `E13R-frozen` before any code.

## Validity and route (hard stop)

- V1 probe read-only (both codes): **yes**
- L2 instrumented check: only the observer's forage habit changes: **yes**
- L1 sham = control, V2 zero = control, V3 code unchanged (all seeds): **yes**
- All outcome runs finished: **yes**
- Code unchanged during outcome runs: **yes**

```
V1 a seed 501, 20 years: READ-ONLY
V1 b seed 501, 20 years: READ-ONLY
L2 arm b seed 501, 20 years: 15172 copying steps, 6894 habit updates (minimum 1000), 0 with any other change: PASS
seed 501: L1 sham = control yes; V2 zero = control yes; V3 code unchanged yes
seed 502: L1 sham = control yes; V2 zero = control yes; V3 code unchanged yes
seed 503: L1 sham = control yes; V2 zero = control yes; V3 code unchanged yes
seed 504: L1 sham = control yes; V2 zero = control yes; V3 code unchanged yes
seed 505: L1 sham = control yes; V2 zero = control yes; V3 code unchanged yes
seed 506: L1 sham = control yes; V2 zero = control yes; V3 code unchanged yes
seed 507: L1 sham = control yes; V2 zero = control yes; V3 code unchanged yes
seed 508: L1 sham = control yes; V2 zero = control yes; V3 code unchanged yes
seed 509: L1 sham = control yes; V2 zero = control yes; V3 code unchanged yes
seed 510: L1 sham = control yes; V2 zero = control yes; V3 code unchanged yes
seed 511: L1 sham = control yes; V2 zero = control yes; V3 code unchanged yes
seed 512: L1 sham = control yes; V2 zero = control yes; V3 code unchanged yes
seed 513: L1 sham = control yes; V2 zero = control yes; V3 code unchanged yes
seed 514: L1 sham = control yes; V2 zero = control yes; V3 code unchanged yes
seed 515: L1 sham = control yes; V2 zero = control yes; V3 code unchanged yes
seed 516: L1 sham = control yes; V2 zero = control yes; V3 code unchanged yes
L1/V2/V3: PASS
```

## Headline: does preparation survive success? (R1)

| arm | planner-autumns | followed by planning the next autumn | share |
|---|---|---|---|
| A | 257 of 33440 | 11 | 4.3% |
| B | 745 of 33263 | 42 | 5.6% |
| N | 756 of 34990 | 28 | 3.7% |
| P | 235 of 31776 | 7 | 3.0% |

**R1 wrong:** B 5.6% against A 4.3% (needs at least 3% and at least 3× A, with 20+ planner-autumns).

## Source: planners, or anyone better fed?

| measure | A | B | N | P | share kept by N | share kept by P |
|---|---|---|---|---|---|---|
| planner-autumns | 257 | 745 | 756 | 235 | 1.02 | -0.05 |
| habit value | 0.134 | 0.229 | 0.232 | 0.135 | 1.04 | 0.01 |

**Both measures agree: N. Reading: a general "forage while things are good" habit, learned from anyone better fed, carries the effect.**

Copying updates per arm (the dose caution): B 1,102,676, N 1,154,012, P 8,108. Extra planner-autumns over A per 1,000 updates: B 0.44, N 0.43, P -2.71.

Priors: creator N 65%, both 20%, P 15%; assistant N 60%, both 25%, P 15%.

## The rest of the chain

| measure | A | B | N | P |
|---|---|---|---|---|
| habit value, seeds where higher than A | – | 14 of 16 | 14 of 16 | 12 of 16 |
| habit value, mean over seeds | 0.134 | 0.229 | 0.232 | 0.135 |
| planners' neighbours, autumn foraging the next year | 0.461 (n=4349) | 0.480 (n=11706) | 0.472 (n=12227) | 0.451 (n=4198) |
| child-winters whose carer holds 20+ | 38.0% | 46.3% | 46.4% | 37.0% |
| children's winter starvation per child-winter | 0.61% | 0.85% | 0.85% | 0.65% |
| worlds that died out | 2 | 3 | 4 | 3 |

## Frozen predictions (Arm B against Arm A), scored

1. **wrong** — headline: repeat planning 5.6% against 4.3%.
2. **confirmed** — manipulation check: habit value higher than A in 14 of 16 seeds (needs 12).
3. **confirmed** — planner-autumns B ÷ A: 2.90 (needs 2).
4. **confirmed** — carers with 20+: 8.3 points (needs +5).
5. **wrong** — planners' neighbours' foraging B ÷ A: 1.04 (needs 1.1).
6. **wrong** — children's winter starvation B ÷ A: 1.39.

## Descriptive (reported, not scored)

Arm B copying updates by the model's food level (0 = under half a week … 3 = 6+ weeks): 0: 11%, 1: 45%, 2: 41%, 3: 4%; by season (spring, summer, autumn, winter): 27%, 26%, 25%, 22%; from models holding 80+: 1.9%.

Dose-response in B (adult samples every 10 years): 0–0 updates: habit 0.111 (n=6); 1–9 updates: habit 0.238 (n=28); 10–49 updates: habit 0.251 (n=163); 50–199 updates: habit 0.257 (n=586); 200–… updates: habit 0.279 (n=2556).

- B planner-autumns whose planner learned from a model holding 80+ that autumn: 520, followed by planning: 27 (5.2%)
- B planner-autumns whose planner did not: 225, followed by planning: 15 (6.7%)

## Reading

**Valid, and the route is verified.** Every safeguard passed: 6,894 copying updates changed nothing but the watcher's own
forage habit (L2), and the sham worlds equalled the control in all 16 seeds (L1). E13's open question is answered: the
copying acts only through the watcher's own habit.

**The headline failed.** Repeat planning was 5.6% in B against 4.3% in A (1.3×; needed 3× and 3%). On these sixteen new
worlds the control repeated far more often than on E13's four (4.3% against 0.9%), so much of E13's sevenfold contrast
came from a low control.

**The transmission links replicated:** habits higher in 14 of 16 seeds, planner-autumns 2.9×, carers holding 20+ up 8.3
points. **Neighbours of planners did not change** (1.04×, needed 1.1; E13 1.07). **Children were not saved:** winter
starvation was 1.39× the control, pooled (162 of 19,028 child-winters against 110 of 17,932). An exploratory per-seed
look, not part of the frozen analysis, found B worse in 9 worlds and better in 7, the pooled difference driven by a few
large worlds: copying did not protect children; whether it harmed them is unclear.

**Source: anyone better fed, not planners.** Arm N, which never copies anyone holding 80+, kept all of B's effect
(1.02 of planner-autumns, 1.04 of habit value); Arm P kept none. In B, 98% of copying came from models holding under 80.
Arm P made only 8,108 copying updates against B's 1.1 million, so E13R cannot say planners teach less; it shows that the
effect does not need planners. Both priors favoured N (creator 65%, assistant 60%).

**What it means.** Copying the visibly better-fed reliably spreads a general habit between adults, foraging while
moderately stocked, and that habit leaves more people well stocked at the end of autumn. It does not spread winter
preparation: repeat planning barely rose above the control, planners' neighbours did not change, and children were not
saved. By the frozen criteria E13R is not a success. Transmission between adults happens; what passes is a foraging
habit, not a plan.

**Roadmap branch (fixed before the result):** B replicates, N carries it → stage 4, testing the general habit. The
assistant recommends a read-only autopsy first: why better-stocked carers did not protect their children, and whether
the spread habit is linked to preparation at all. The creator decides.
