# NB1: can a neural-brained people survive and improve over generations? (results)

Frozen as `NB1-frozen` (amendments 1, 2 and 3). run_nb1.py, run_nb1_garden.py, analyse_nb1.py (written before data).

## Validity

- Zero checks (All: PASS, `code_nb1` fingerprint): **yes**
- All phase-1 worlds present (48): **yes**
- One fingerprint, `code_nb1`'s: **yes**

**Valid.**

## Reading (frozen)

- **decorative (g stays at or above 0.9).**
- Viability: extinct worlds c 1, n 3, e 3; population (living-weeks, years 100-600) n/c 1.1677 [0.8825, 1.4587], e/c 1.4489 [1.1482, 1.7251]; viable: **yes**.
- Primary 1 (n): slope per generation of survival to 16 per birth +0.00371 [+0.00190, +0.00562] (14 worlds); of adult lifespan (years) +0.17941 [+0.10077, +0.25417] (14 worlds); improves: **yes**.
- Primary 1 (e, evolution only): survival to 16 +0.01255 [+0.00305, +0.03117] (14 worlds); adult lifespan +0.05680 [-0.04427, +0.14046] (14 worlds).
- Primary 2, inherited (generation 18 - 1, learning off, children's survival to 16): +0.00537 [-0.03104, +0.04412] (13 worlds); yes: **no**.
- Lifetime learning (on - off, pooled over generations): -0.04504 [-0.06538, -0.02444] (43 worlds).
- g falls below 0.9 by year 600 (n): **no**; decorative: **yes**.

Rule: 'not viable' if n has more than 3 extra extinct worlds or the population ratio's upper bound is below 0.80; 'improves by itself' if primary 1 or primary 2 (inherited) is yes and g falls; 'decorative' if g stays at or above 0.9; otherwise 'no improvement shown'.

## The g trajectory (mean over worlds of the mean g at each year)

| year | 1 | 50 | 100 | 200 | 300 | 400 | 500 | 600 |
|---|---|---|---|---|---|---|---|---|
| neural brain, learning | 1.001 | 1.007 | 1.022 | 1.091 | 1.109 | 1.141 | 1.190 | 1.229 |
| neural brain, evolution only | 0.999 | 0.993 | 0.993 | 1.038 | 1.095 | 1.178 | 1.222 | 1.272 |

## CI1's eight guards, neural brain (n) against v17 (descriptive; 16 seeds cannot gate harm)

| measure | n | v17 | ratio [95%] |
|---|---|---|---|
| starvation deaths per 1,000 living-years | 9.7870 | 4.4156 | 2.2165 [1.9446, 2.6007] |
| killing deaths per 1,000 living-years | 0.7371 | 0.0038 | 195.5369 [106.0947, 598.6387] |
| adult health, mean | 90.4796 | 93.5475 | 0.9672 [0.9598, 0.9733] |
| child deaths per 1,000 child-years | 17.9845 | 9.3813 | 1.9171 [1.6938, 2.1933] |
| child starvation deaths per 1,000 child-years | 13.2826 | 5.3496 | 2.4829 [2.0417, 3.1440] |
| gifts to kin's children per 1,000 adult-weeks | 5.6932 | 4.5409 | 1.2537 [1.0740, 1.4752] |

## The network's part of the decision (sampled every 50th decision)

| arm | decisions | mean correlation, network and hand-written scores | spread ratio, network / hand-written |
|---|---|---|---|
| neural brain, learning | 1,087,496 | -0.3034 | 0.7912 |
| neural brain, evolution only | 1,314,549 | -0.0773 | 0.1322 |

## Action mix of the grown: entropy (bits) by century

| arm | 0-100 | 100-200 | 200-300 | 300-400 | 400-500 | 500-600 |
|---|---|---|---|---|---|---|
| v17 | 2.572 | 2.361 | 2.328 | 2.321 | 2.341 | 2.342 |
| neural brain, learning | 2.367 | 2.325 | 2.355 | 2.374 | 2.402 | 2.384 |
| neural brain, evolution only | 2.716 | 2.619 | 2.585 | 2.572 | 2.547 | 2.537 |

