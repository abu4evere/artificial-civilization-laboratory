# NB2: connect the world to the neural brain. Can the network decide? (results)

Frozen as `NB2-frozen`. run_nb2.py, run_nb2_garden.py, analyse_nb2.py (written before data).

## Validity

- Zero checks (All: PASS, `code_nb2` fingerprint): **yes**
- All phase-1 worlds present (80): **yes**
- One fingerprint, `code_nb2`'s: **yes**

**Valid.**

## Reading (frozen)

- **not viable.**
- Viability: extinct worlds c 4, s 9, o 15, l 11, n 13; population (living-weeks, years 100-600) against c: s 0.2705 [0.1290, 0.4498], o 0.0458 [0.0002, 0.1476], l 0.2177 [0.0832, 0.3655], n 0.1769 [0.0515, 0.3406]; n viable: **no**.
- **Primary**, survival to 16 per birth (born years 100-600), n - s: -0.0184 [-0.0581, +0.0077]; above 0: **no**.
- Inherited competence (generation 18 - 1, g = 0, learning off): phase 2 not present; above 0: **no**.
- Learning's worth (generation 18, on - off): phase 2 not present.

Rule: 'not viable' if n has more than 3 extra extinct worlds than c or the population ratio's upper bound is below 0.80; 'the network decides' if n - s and the inherited garden both have lower bounds above 0; 'learning helps, but the instincts still carry it' if only n - s does; otherwise 'no improvement shown'.

## Survival to 16 per birth, by arm (born years 100-600)

| arm | survival | births with known outcome |
|---|---|---|
| v17 (old minds) | 0.8696 | 14,383 |
| sham: new options and sight, learning off | 0.8110 | 4,879 |
| o: + NB1's REINFORCE | 0.7707 | 881 |
| l: + actor-critic | 0.8148 | 3,915 |
| n: + social learning (full NB2) | 0.7926 | 3,279 |

## What each fix adds (paired differences in survival to 16)

- NB1's learning on the new options (o - s): -0.0403 [-0.0871, +0.1281]
- actor-critic instead (l - o): +0.0441 [-0.1010, +0.0626]
- social learning (n - l): -0.0222 [-0.0341, +0.0030]
- new options and sight, no learning, against the old minds (s - c): -0.0586 [-0.1165, +0.0090]
- full NB2 against the old minds (n - c): -0.0770 [-0.1174, -0.0352]

## g, the weight on the instincts (mean over worlds; worlds counted in brackets)

| arm | 1 | 50 | 100 | 200 | 300 | 400 | 500 | 600 |
|---|---|---|---|---|---|---|---|---|
| s | 1.000 (16) | 1.007 (16) | 1.013 (15) | 1.049 (10) | 1.039 (9) | 1.136 (7) | 1.134 (7) | 1.228 (7) |
| o | 1.000 (16) | 1.013 (16) | 0.976 (8) | 0.954 (2) | 1.143 (1) | 1.258 (1) | 1.329 (1) | 1.382 (1) |
| l | 0.999 (16) | 1.012 (16) | 1.028 (16) | 1.045 (10) | 1.119 (7) | 1.124 (5) | 1.223 (5) | 1.293 (5) |
| n | 1.000 (16) | 1.013 (16) | 1.025 (15) | 1.055 (12) | 1.152 (5) | 1.259 (4) | 1.394 (3) | 1.426 (3) |

## CI1's eight guards, full NB2 (n) against v17 (descriptive; 16 seeds cannot gate harm)

| measure | n | v17 | ratio [95%] |
|---|---|---|---|
| starvation deaths per 1,000 living-years | 12.3537 | 4.9015 | 2.5204 [2.0146, 3.0494] |
| killing deaths per 1,000 living-years | 2.4862 | 0.0027 | 910.2298 [361.4806, 2748.2985] |
| adult health, mean | 87.2244 | 92.7808 | 0.9401 [0.9292, 0.9607] |
| child deaths per 1,000 child-years | 15.4060 | 10.3840 | 1.4836 [1.0783, 2.0726] |
| child starvation deaths per 1,000 child-years | 10.8929 | 6.6710 | 1.6329 [1.1232, 2.3531] |
| gifts to kin's children per 1,000 adult-weeks | 4.3870 | 4.5750 | 0.9589 [0.5608, 1.4416] |

## The network's part of the decision (every 50th decision)

| arm | decisions | options per decision | network changes the top option | correlation, network and instinct | spread ratio |
|---|---|---|---|---|---|
| s | 280,249 | 26.5 | 0.2388 | -0.0397 | 0.1473 |
| o | 71,855 | 26.3 | 0.4424 | -0.3422 | 0.6079 |
| l | 240,158 | 26.5 | 0.2666 | -0.1607 | 0.1977 |
| n | 209,548 | 26.6 | 0.2354 | -0.1697 | 0.1814 |

