# LH1: a fairer look-ahead (results)

Frozen as `LH1-frozen`. run_lh1.py, analyse_lh1.py (written before data). Years 100–200.

## Validity

- Zero checks (All: PASS, same `code_lh1` fingerprint): **yes**
- All worlds present (128 of 128): **yes**
- One fingerprint, `code_lh1`'s: **yes**

**Valid.**

## Primary: harm guards (each rule against v13)

Rule: population ratio < 0.90 with upper bound < 1; 3+ extra extinct worlds; hunger ratio > 1.25 with lower bound > 1; killing rate higher by > 0.05 per 1,000 living-years with lower bound > 0; health lower by > 5 with upper bound < 0.

### e (the real next choice)

- Population: living-weeks ratio 1.290 [1.138, 1.465]
- Extinction: v13 0, this rule 0 (extra +0)
- Hunger: starvation deaths per 1,000 living-years v13 4.517, this rule 6.221; ratio 1.377 [1.267, 1.496]
- Killing: deaths by killing per 1,000 living-years v13 0.0045, this rule 0.0397; difference +0.0352 [+0.0070, +0.0750]
- Health: adults' mean v13 93.09, this rule 91.73; difference -1.36 [-1.91, -0.79]
- **Harm: GUARD RAISED: hunger.**
- Making: M3 v13 0.0034, this rule 0.0116; difference +0.0082 [+0.0075, +0.0089]; makes per adult-year 0.0581 → 0.1884, ratio 3.245 [3.022, 3.465]; **making released**
- **Reading: not supported.**

### m (the experienced situation value)

- Population: living-weeks ratio 1.316 [1.169, 1.494]
- Extinction: v13 0, this rule 0 (extra +0)
- Hunger: starvation deaths per 1,000 living-years v13 4.517, this rule 7.905; ratio 1.750 [1.562, 1.939]
- Killing: deaths by killing per 1,000 living-years v13 0.0045, this rule 0.1963; difference +0.1918 [+0.1006, +0.3113]
- Health: adults' mean v13 93.09, this rule 91.17; difference -1.92 [-2.70, -1.18]
- **Harm: GUARD RAISED: hunger, killing.**
- Making: M3 v13 0.0034, this rule 0.0219; difference +0.0184 [+0.0169, +0.0199]; makes per adult-year 0.0581 → 0.3332, ratio 5.739 [5.282, 6.167]; **making released**
- **Reading: not supported.**

**Neither rule is supported.**

## Described (no frozen prediction)

- Living-weeks e (the real next choice) ÷ sham: 1.209 [1.069, 1.368]
- Living-weeks m (the experienced situation value) ÷ sham: 1.234 [1.102, 1.386]
- Living-weeks sham ÷ v13: 1.067 [0.938, 1.216]
- v13: acts aimed at a person 0.1814; steal 0.144‰; attack 0.001‰; world-new kinds 3,458, remade 0; edible food per adult 8.471
- e (the real next choice): acts aimed at a person 0.1670; steal 0.544‰; attack 0.016‰; world-new kinds 16,089, remade 2; edible food per adult 7.812
- m (the experienced situation value): acts aimed at a person 0.1583; steal 1.059‰; attack 0.074‰; world-new kinds 25,279, remade 2; edible food per adult 8.016
- sham: acts aimed at a person 0.1859; steal 0.156‰; attack 0.001‰; world-new kinds 3,512, remade 1; edible food per adult 8.334

**Deaths by cause (years 100–200; all ages).**

| cause | v13 | e (the real next choice) | m (the experienced situation value) | sham |
|---|---|---|---|---|
| childbirth | 85 | 134 | 136 | 100 |
| cold | 1 | 0 | 0 | 0 |
| hunting | 0 | 1 | 0 | 1 |
| illness | 1,931 | 2,426 | 2,484 | 2,119 |
| killed | 2 | 23 | 116 | 5 |
| neglect | 43 | 67 | 73 | 51 |
| old age | 4,315 | 4,581 | 4,220 | 4,516 |
| starvation | 2,029 | 3,604 | 4,672 | 2,374 |
| thirst | 1,076 | 1,449 | 1,567 | 1,144 |

## Population (beside every measure)

| arm | living-weeks | adult-weeks (16–49) | extinct worlds |
|---|---|---|---|
| v13 | 23,357,205 | 12,256,857 | 0 |
| e (the real next choice) | 30,127,177 | 15,660,401 | 0 |
| m (the experienced situation value) | 30,734,337 | 15,751,240 | 0 |
| sham | 24,913,697 | 13,157,091 | 1 |

