# NB3: feelings. Can a neural people live in the open world if it is born with human feelings? (results)

Frozen as `NB3-frozen`. run_nb3.py, analyse_nb3.py (written before data).

## Validity

- Zero checks (All: PASS, `code_nb3` fingerprint): **yes**
- All phase-1 worlds present (112): **yes**
- One fingerprint, `code_nb3`'s: **yes**

**Valid.**

## Reading (frozen)

- **f not viable.**
- Viability: extinct worlds c 4, n2 12, f0 11, fH 7, f 5, fmE 10, fmH 12; population (living-weeks, years 100-600) against c, point [2.5%, 97.5%]: n2 0.1654 [0.0615, 0.3048], f0 0.2209 [0.1047, 0.3659], fH 0.4658 [0.3042, 0.6724], f 0.4893 [0.3251, 0.6705], fmE 0.3896 [0.2373, 0.5400], fmH 0.1693 [0.0751, 0.2747].
- **Primary: f viable against c: no.** (By the same rule: n2 no, f0 no, fH no, f no, fmE no, fmH no)
- Survival to 16 per birth, f - n2: -0.0310 [-0.0601, -0.0043].
- Garden (if present; g = 0, learning off, feeling genes as inherited): founders alive after one year, generation 1 +0.0000 [+0.0000, +0.0000] (16 source worlds), generation 18 +0.0000 [+0.0000, +0.0000] (12 source worlds); survival to 16, generation 18 - 1: phase 2 not present.

Rule (frozen): 'f viable' if f's extinct worlds are at most c's + 3 and the upper bound of f/c's population ratio is at least 0.80. Council 84 asked that the point and the lower bound be read too.

## Survival to 16 per birth, by arm (born years 100-600)

| arm | survival | births with known outcome |
|---|---|---|
| v17 (old minds) | 0.8749 | 12,913 |
| NB2's full brain | 0.8123 | 2,616 |
| f0: no joy in attacking | 0.8216 | 3,358 |
| fH: + inborn reluctance | 0.8144 | 7,431 |
| f: all feelings | 0.7813 | 8,280 |
| f without empathy | 0.7816 | 6,356 |
| f without the inborn reluctance | 0.7956 | 2,833 |

## What each fix adds (paired differences in survival to 16)

- no joy in attacking (f0 - n2): +0.0093 [-0.0347, +0.0433]
- the inborn reluctance (fH - f0): -0.0072 [-0.0372, +0.0321]
- the other feelings (f - fH): -0.0331 [-0.0625, -0.0013]
- empathy (f - f without E): -0.0003 [-0.0438, +0.0427]
- the reluctance among all feelings (f - f without H): -0.0143 [-0.0629, +0.0394]
- f against the old minds: -0.0936 [-0.1173, -0.0671]

## g, the weight on the instincts (mean over worlds; worlds counted in brackets)

| arm | 1 | 50 | 100 | 200 | 300 | 400 | 500 | 600 |
|---|---|---|---|---|---|---|---|---|
| n2 | 1.000 (16) | 1.007 (16) | 1.029 (16) | 1.051 (9) | 1.135 (5) | 1.209 (5) | 1.268 (4) | 1.363 (4) |
| f0 | 1.000 (16) | 1.016 (16) | 1.028 (16) | 1.070 (10) | 1.145 (8) | 1.085 (6) | 1.106 (6) | 1.160 (5) |
| fH | 1.000 (16) | 1.003 (16) | 1.008 (16) | 1.021 (15) | 1.048 (14) | 1.121 (9) | 1.132 (9) | 1.193 (9) |
| f | 1.000 (16) | 1.005 (16) | 1.007 (16) | 1.024 (14) | 1.024 (14) | 1.047 (12) | 1.085 (12) | 1.077 (11) |
| fmE | 1.001 (16) | 1.004 (16) | 1.022 (16) | 1.017 (13) | 1.073 (10) | 1.103 (9) | 1.087 (8) | 1.103 (6) |
| fmH | 1.000 (16) | 1.016 (16) | 1.052 (15) | 1.034 (11) | 1.142 (8) | 1.153 (6) | 1.195 (4) | 1.280 (4) |

## The feeling genes in f (mean over worlds; start values E 0.5, G 0.5, L 1.0, A 0.5, C 0.5, H 1.0)

| gene | 1 | 50 | 100 | 200 | 300 | 400 | 500 | 600 |
|---|---|---|---|---|---|---|---|---|
| E | 0.500 (16) | 0.497 (16) | 0.501 (16) | 0.512 (14) | 0.475 (14) | 0.479 (12) | 0.454 (12) | 0.523 (11) |
| G | 0.501 (16) | 0.496 (16) | 0.497 (16) | 0.532 (14) | 0.530 (14) | 0.536 (12) | 0.540 (12) | 0.542 (11) |
| L | 1.000 (16) | 0.994 (16) | 0.998 (16) | 0.974 (14) | 0.993 (14) | 0.978 (12) | 0.972 (12) | 0.973 (11) |
| A | 0.499 (16) | 0.505 (16) | 0.505 (16) | 0.489 (14) | 0.477 (14) | 0.441 (12) | 0.405 (12) | 0.476 (11) |
| C | 0.500 (16) | 0.499 (16) | 0.504 (16) | 0.488 (14) | 0.482 (14) | 0.492 (12) | 0.496 (12) | 0.503 (11) |
| H | 1.000 (16) | 1.004 (16) | 1.000 (16) | 0.976 (14) | 1.004 (14) | 0.977 (12) | 0.962 (12) | 0.955 (11) |

## CI1's guards, f (all feelings) against v17 (descriptive; years 100-600)

| measure | n | v17 | ratio [95%] |
|---|---|---|---|
| starvation deaths per 1,000 living-years | 11.3472 | 4.1526 | 2.7325 [2.3899, 3.1257] |
| killing deaths per 1,000 living-years | 0.0090 | 0.0059 | 1.5327 [0.0000, 7.7953] |
| adult health, mean | 89.5825 | 94.1233 | 0.9518 [0.9416, 0.9620] |
| child deaths per 1,000 child-years | 17.7552 | 9.6801 | 1.8342 [1.5197, 2.2177] |
| child starvation deaths per 1,000 child-years | 13.0356 | 5.7291 | 2.2753 [1.8567, 2.8049] |
| gifts to kin's children per 1,000 adult-weeks | 4.6351 | 4.7184 | 0.9824 [0.8087, 1.2268] |

## Causes of death, share of all deaths by arm (years 100-600)

| arm | deaths | childbirth | cold | hunting | illness | killed | neglect | old age | starvation | thirst |
|---|---|---|---|---|---|---|---|---|---|---|
| c | 14,637 | 0.009 | 0.000 | 0.000 | 0.205 | 0.000 | 0.004 | 0.482 | 0.194 | 0.106 |
| n2 | 2,964 | 0.010 | 0.000 | 0.000 | 0.209 | 0.128 | 0.001 | 0.229 | 0.356 | 0.067 |
| f0 | 3,757 | 0.011 | 0.000 | 0.000 | 0.204 | 0.116 | 0.003 | 0.271 | 0.332 | 0.062 |
| fH | 7,820 | 0.012 | 0.000 | 0.000 | 0.214 | 0.001 | 0.002 | 0.292 | 0.402 | 0.077 |
| f | 8,702 | 0.009 | 0.000 | 0.000 | 0.207 | 0.000 | 0.003 | 0.256 | 0.436 | 0.089 |
| fmE | 6,929 | 0.009 | 0.000 | 0.000 | 0.211 | 0.002 | 0.003 | 0.287 | 0.388 | 0.101 |
| fmH | 3,121 | 0.009 | 0.000 | 0.000 | 0.177 | 0.110 | 0.002 | 0.228 | 0.393 | 0.081 |

## Adults' acts, share of all adult acts by arm (centuries 1-5, years 100-600)

| arm | acts | hunt | attack | steal | give | care | take | make |
|---|---|---|---|---|---|---|---|---|
| c | 25,374,708 | 0.0001 | 0.0000 | 0.0001 | 0.0625 | 0.0022 | 0.0001 | 0.0009 |
| n2 | 3,893,171 | 0.0009 | 0.0026 | 0.0026 | 0.0400 | 0.0198 | 0.0011 | 0.0175 |
| f0 | 5,276,213 | 0.0010 | 0.0025 | 0.0029 | 0.0418 | 0.0173 | 0.0013 | 0.0209 |
| fH | 10,970,491 | 0.0009 | 0.0000 | 0.0000 | 0.0402 | 0.0179 | 0.0012 | 0.0185 |
| f | 11,365,793 | 0.0009 | 0.0000 | 0.0001 | 0.0471 | 0.0208 | 0.0014 | 0.0194 |
| fmE | 9,174,821 | 0.0008 | 0.0001 | 0.0001 | 0.0475 | 0.0193 | 0.0015 | 0.0240 |
| fmH | 3,901,723 | 0.0009 | 0.0026 | 0.0031 | 0.0479 | 0.0215 | 0.0012 | 0.0219 |

## The network's part of the decision (every 50th decision; H counted with the instincts)

| arm | decisions | options per decision | network changes the top option | correlation, network and instinct | spread ratio |
|---|---|---|---|---|---|
| n2 | 196,652 | 26.1 | 0.2586 | -0.1966 | 0.1946 |
| f0 | 241,318 | 26.3 | 0.2396 | -0.1123 | 0.1887 |
| fH | 437,602 | 26.8 | 0.2277 | -0.2150 | 0.1410 |
| f | 452,117 | 26.5 | 0.2792 | -0.2438 | 0.1645 |
| fmE | 377,951 | 26.4 | 0.2622 | -0.2099 | 0.1484 |
| fmH | 198,707 | 26.0 | 0.2673 | -0.1922 | 0.1998 |

