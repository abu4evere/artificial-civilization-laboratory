# MK1 — Why is making not chosen? Results

Frozen as `MK1-frozen` (with draft revision 1; operational note 1). run_mk1.py, analyse_mk1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (32 of 32): **yes**
- One fingerprint (`code_v7`): **yes**
- The replay matches the decision in every world (offer and worth term mismatches 0): **yes**

**Valid.**

## Survivorship and population (worlds alive at each bin's start)

| bin (years) | worlds alive | mean population | mean adults |
|---|---|---|---|
| 0-5 | 32 of 32 | 95.1 | 73.3 |
| 5-10 | 32 of 32 | 107.5 | 57.2 |
| 10-20 | 32 of 32 | 111.7 | 45.3 |
| 20-50 | 32 of 32 | 117.0 | 66.5 |
| 50-100 | 32 of 32 | 136.8 | 83.9 |
| 100-200 | 32 of 32 | 132.5 | 86.2 |

Worlds that ended before year 200 (year): [].

## The offer gate and Q1, the score gap (adults; by bin; worlds alive at each bin's start)

Feasible per person-week; offered given feasible; why feasible but not offered (worth at most 0.05 / only things already held / both / too tired); chosen given offered; the softmax's own probability; and the mean parts of making's score when offered (worth term, habit, thought) against the others' soft maximum U_other.

| bin | worlds | feasible | offered / feasible | not offered: low / held / both / tired | chosen / offered | softmax P | make scored highest | worth term | habit | thought | U_other | mean log-odds |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0-5 | 32 | 0.235 | 0.496 | 0.67 / 0.23 / 0.10 / 0.00 | 0.0263 | 0.0263 | 0.0158 | 0.184 | 0.0004 | 0.037 | 1.252 | -5.15 |
| 5-10 | 32 | 0.574 | 0.627 | 0.70 / 0.16 / 0.14 / 0.00 | 0.0219 | 0.0222 | 0.0122 | 0.191 | 0.0015 | 0.030 | 1.314 | -5.46 |
| 10-20 | 32 | 0.734 | 0.725 | 0.70 / 0.14 / 0.16 / 0.00 | 0.0194 | 0.0194 | 0.0109 | 0.203 | 0.0049 | 0.031 | 1.349 | -5.55 |
| 20-50 | 32 | 0.785 | 0.808 | 0.74 / 0.13 / 0.12 / 0.01 | 0.0082 | 0.0082 | 0.0031 | 0.202 | 0.0116 | 0.023 | 1.559 | -6.61 |
| 50-100 | 32 | 0.812 | 0.829 | 0.87 / 0.06 / 0.06 / 0.01 | 0.0026 | 0.0026 | 0.0005 | 0.196 | 0.0203 | 0.021 | 1.786 | -7.75 |
| 100-200 | 32 | 0.818 | 0.818 | 0.93 / 0.03 / 0.03 / 0.00 | 0.0012 | 0.0012 | 0.0001 | 0.190 | 0.0280 | 0.020 | 1.960 | -8.61 |

When making was offered and not chosen, what won (share):

- 0-5: forage 0.48, join 0.13, talk 0.12, give 0.07, rest 0.04, gather 0.03
- 5-10: forage 0.50, talk 0.12, join 0.12, give 0.08, rest 0.04, gather 0.04
- 10-20: forage 0.43, talk 0.16, join 0.14, give 0.10, gather 0.05, put 0.04
- 20-50: forage 0.42, talk 0.15, join 0.12, give 0.11, gather 0.09, put 0.07
- 50-100: forage 0.41, talk 0.15, gather 0.13, give 0.12, join 0.09, put 0.08
- 100-200: forage 0.40, gather 0.15, talk 0.15, give 0.11, put 0.09, join 0.08

## Q2 — Skill and worth (described; skill and worth cause each other, so no cause is named)

Adults, offered weeks, all bins. Standardised to all adults' offered weeks over bin × hunger × tool × food (direct standardisation over the states each skill band has; the share of the reference it covers is shown).

| crafting skill | offered weeks | chosen / offered (standardised) | softmax P (std.) | v (std.) | worth term (std.) | reference weight covered |
|---|---|---|---|---|---|---|
| <0.1 | 447641 | 0.0006 | 0.0008 | 0.120 | 0.162 | 0.84 |
| 0.1-0.2 | 2978521 | 0.0014 | 0.0013 | 0.133 | 0.177 | 0.96 |
| 0.2-0.35 | 6743486 | 0.0022 | 0.0022 | 0.141 | 0.188 | 1.00 |
| 0.35-0.5 | 4051254 | 0.0028 | 0.0028 | 0.150 | 0.200 | 1.00 |
| 0.5+ | 2828659 | 0.0050 | 0.0048 | 0.163 | 0.217 | 1.00 |

**Deliberate makings of forage tools (factor > 1), by the maker's skill at the time.** Worth: the maker's learned worth for that kind at the making, 13 and 52 weeks later (alive makers). 'Relative' = the worth minus the mean for the same kind at 52 weeks over all makers (so kinds are compared with themselves).

| crafting skill | makings | forage factor (mean) | worth at making | at 13 weeks | at 52 weeks | relative at 52 weeks |
|---|---|---|---|---|---|---|
| <0.1 | 275 | 1.172 | 0.128 | 0.149 | 0.156 | -0.002 |
| 0.1-0.2 | 2957 | 1.165 | 0.133 | 0.147 | 0.151 | -0.005 |
| 0.2-0.35 | 12125 | 1.160 | 0.136 | 0.146 | 0.149 | -0.005 |
| 0.35-0.5 | 16620 | 1.162 | 0.141 | 0.148 | 0.150 | -0.005 |
| 0.5+ | 31365 | 1.151 | 0.150 | 0.154 | 0.155 | +0.005 |

## Q3 — Early (years 0-10) against late (years 100-200), matched

Adults, offered weeks. Matched states: hunger band × forage tool held × food on the tile; late states weighted to the early distribution of offered weeks (states present in both). Exact split of the change in mean log-odds of choosing to make: Δ = (Δ worth term + Δ habit + Δ thought − Δ U_other) / T, the worth term split by Shapley into v, diligence and hunger, with the cell-level covariance left as its own term.

**worlds alive at year 100** (32 worlds, 24 matched states):

- chosen given offered: raw 0.0232 → 0.0012; matched 0.0232 → 0.0020 (late / early 0.086 [0.076, 0.0965]). Softmax P matched 0.0234 → 0.0020.
- Δ ln(chosen given offered): raw -2.974; matched -2.457. **Share of the fall that remains within matched states: 0.83.**
- mean v 0.144 → 0.144; U_other 1.296 → 1.937.

| part | Δ mean log-odds | share of the change |
|---|---|---|
| v, the learned worth | -0.001 [-0.0239, 0.0218] | 0.00 |
| diligence | -0.010 [-0.0189, -0.00146] | 0.00 |
| hunger | +0.006 [0.00534, 0.00637] | -0.00 |
| worth term: covariance | +0.002 [0.000241, 0.00351] | -0.00 |
| habit | +0.134 [0.127, 0.14] | -0.04 |
| thought's pull | -0.046 [-0.059, -0.0341] | 0.01 |
| the other options (− U_other) | -3.204 [-3.28, -3.13] | 1.03 |
| **total** | -3.120 [-3.19, -3.05] | 1.00 |

(Exactness check: total minus the parts = 2.22e-15.) Raw (unmatched) Δ mean log-odds: -3.246.

**The part carrying the largest share of the change (worlds alive at year 100): others.**

**all worlds (late from those alive)** (32 worlds, 24 matched states):

- chosen given offered: raw 0.0232 → 0.0012; matched 0.0232 → 0.0020 (late / early 0.086 ). Softmax P matched 0.0234 → 0.0020.
- Δ ln(chosen given offered): raw -2.974; matched -2.457. **Share of the fall that remains within matched states: 0.83.**
- mean v 0.144 → 0.144; U_other 1.296 → 1.937.

| part | Δ mean log-odds | share of the change |
|---|---|---|
| v, the learned worth | -0.001  | 0.00 |
| diligence | -0.010  | 0.00 |
| hunger | +0.006  | -0.00 |
| worth term: covariance | +0.002  | -0.00 |
| habit | +0.134  | -0.04 |
| thought's pull | -0.046  | 0.01 |
| the other options (− U_other) | -3.204  | 1.03 |
| **total** | -3.120  | 1.00 |

(Exactness check: total minus the parts = 2.22e-15.) Raw (unmatched) Δ mean log-odds: -3.246.

**The part carrying the largest share of the change (all worlds (late from those alive)): others.**

## Q4 — Does making a forage tool pay? (described; an observational benefit-cost proxy, not a causal net return)

Every forage tool (factor > 1) made deliberately, followed while its maker holds it. Benefit: the food owed to the tool (got × (1 − 1/f)) at the maker's forage acts, cumulative to each horizon; a tool that stops being followed (maker died, or no longer holds it) keeps what it had earned. Cost: one forage act's food forgone in the making week, estimated as the mean food per adult forage act in the maker's own world, bin and state (hunger × tool × food × skill).

| bin made | tools | uses (mean) | owed by 13 wk | owed by 26 wk | owed by 52 wk | owed by 104 wk | lifetime owed | followed past 52 weeks | cost (one act) | proxy at 52 weeks (owed − cost) |
|---|---|---|---|---|---|---|---|---|---|---|
| 0-5 | 1689 | 11.6 | 10.7 | 20.0 | 29.4 | 32.6 | 34.2 | 0.26 | 18.9 | +10.5 |
| 5-10 | 3226 | 11.7 | 10.7 | 20.0 | 29.7 | 34.8 | 36.8 | 0.31 | 21.2 | +8.5 |
| 10-20 | 9157 | 12.2 | 8.7 | 16.4 | 26.0 | 32.4 | 35.2 | 0.40 | 22.0 | +4.0 |
| 20-50 | 17675 | 15.7 | 10.8 | 20.8 | 33.8 | 41.1 | 43.7 | 0.45 | 21.0 | +12.8 |
| 50-100 | 13078 | 18.1 | 12.8 | 25.0 | 41.4 | 48.4 | 49.9 | 0.45 | 20.3 | +21.1 |
| 100-200 | 12091 | 18.1 | 13.4 | 26.2 | 44.4 | 50.9 | 51.7 | 0.45 | 20.3 | +24.1 |

Why tools stopped being followed: {'not held': 54801, 'died': 2033, None: 82}.

| maker's skill | tools | owed by 52 weeks | proxy at 52 weeks |
|---|---|---|---|
| <0.1 | 406 | 53.0 | +33.0 |
| 0.1-0.2 | 3320 | 47.2 | +27.0 |
| 0.2-0.35 | 12070 | 43.6 | +23.5 |
| 0.35-0.5 | 15757 | 39.0 | +18.7 |
| 0.5+ | 25363 | 29.2 | +7.8 |

## Q5 — The three hypotheses (read from the tables above; all may hold)

- **Low-skill trap:** within matched states, choosing to make rises with skill (Q2's standardised rates); the learned worth of the same kind is lower for low-skill makers (Q2's relative worth); late makers' lower worth goes with lower skill (Q3's v part, read beside Q2).
- **Opportunity cost dominates:** skilled makers also reject making (Q2's top band); the other options' soft maximum carries the fall (Q3's '− U_other' part); making pays less than one forage act within a year (Q4's proxy).
- **Delayed-benefit failure:** a tool's owed food over a year exceeds the cost (Q4's proxy > 0), while learned worth and the chance of choosing to make stay low.

