# BD3 — what in a body keeps more people alive: results

Frozen as `BD3-frozen`. run_bd3.py, analyse_bd3.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present: **yes**
- One fingerprint (`code_bd3`): **yes**

Manipulation check (events of the part / opportunities for it, summed over seeds):

| arm | eat | carried | foul | seen | tools | passes |
|---|---|---|---|---|---|---|
| f | 4,883 / 93,372 | 37,467 / 47,519 | 2,136,437 / 0 | 269,835 / 0 | 11,852 / 32,404 | yes |
| f_eat | 0 / 94,657 | 37,249 / 47,405 | 2,413,231 / 0 | 282,927 / 0 | 12,025 / 32,593 | yes |
| f_carried | 4,888 / 93,665 | 0 / 47,000 | 1,938,064 / 0 | 267,599 / 0 | 11,489 / 32,013 | yes |
| f_foul | 4,716 / 91,914 | 35,990 / 45,734 | 0 / 2,027,234 | 259,242 / 0 | 11,429 / 31,726 | yes |
| f_seen | 4,908 / 93,835 | 36,745 / 46,640 | 2,065,875 / 0 | 0 / 271,959 | 11,692 / 32,432 | yes |
| f_tools | 5,037 / 94,359 | 37,393 / 47,296 | 2,181,390 / 0 | 276,859 / 0 | 0 / 30,492 | yes |
| f_eat_carried | 0 / 95,145 | 0 / 47,704 | 2,196,995 / 0 | 282,394 / 0 | 11,825 / 32,711 | yes |
| f_all | 0 / 94,180 | 0 / 47,071 | 0 / 2,080,056 | 0 / 280,557 | 0 / 30,024 | yes |

- Manipulation check: **passes**

**Valid.**

## Primary: time-averaged population

Means: f **26.14**, n **26.10**, f_eat **26.27**, f_carried **25.99**, f_foul **25.37**, f_seen **26.15**, f_tools **26.38**, f_eat_carried **26.50**, f_all **26.16**.

**(1) Gate, the gain on fresh seeds:** F / N - 1 = +0.002 [-0.034, +0.038]: **NOT replicated: everything below is described only**

**(2) Each part (F / (F-x) - 1, Holm-adjusted intervals):**

| part | F / (F-x) - 1 | interval | level | bootstrap p | reading |
|---|---|---|---|---|---|
| foul | +0.031 | [-0.010, +0.070] | 0.990 | 0.0416 | **described only (gate not passed)** |
| tools | -0.009 | [-0.039, +0.022] | 0.990 | 0.4460 | **described only (gate not passed)** |
| eat | -0.005 | [-0.041, +0.032] | 0.990 | 0.7058 | **described only (gate not passed)** |
| carried | +0.006 | [-0.032, +0.046] | 0.990 | 0.7178 | **described only (gate not passed)** |
| seen | -0.000 | [-0.045, +0.045] | 0.990 | 0.9816 | **described only (gate not passed)** |

**(3) Described:**

| quantity | estimate | 95% interval |
|---|---|---|
| share of the gain: eat | -3.14 | [-8.67, +1.81] |
| share of the gain: carried | +3.69 | [-8.99, +1.49] |
| share of the gain: foul | +18.61 | [-8.32, +17.16] |
| share of the gain: seen | -0.25 | [-3.05, +6.48] |
| share of the gain: tools | -5.67 | [-8.45, +1.66] |
| eat x carried interaction, as a share of F | +0.014 | [-0.021, +0.048] |
| F-all against N (what remains) | +0.002 | [-0.019, +0.023] |

## Survival (secondary)

| arm | died out | against F: saved / lost (discordant) | risk difference (arm - F) | McNemar p |
|---|---|---|---|---|
| f | 330 | | | |
| n | 322 | 142 / 134 | -0.008 | 0.674 |
| f_eat | 324 | 102 / 96 | -0.006 | 0.722 |
| f_carried | 317 | 119 / 106 | -0.013 | 0.424 |
| f_foul | 338 | 113 / 121 | +0.008 | 0.647 |
| f_seen | 322 | 127 / 119 | -0.008 | 0.655 |
| f_tools | 323 | 89 / 82 | -0.007 | 0.646 |
| f_eat_carried | 316 | 124 / 110 | -0.014 | 0.395 |
| f_all | 326 | 143 / 139 | -0.004 | 0.858 |

## Described (population first)

| arm | median pop. yr 60 / 120 | bodies | meat meals | carried meals | rotten meals | foul person-weeks | seen | tools to kin | kin visits | food to plants |
|---|---|---|---|---|---|---|---|---|---|---|
| f | 25 / 24 | 93,372 | 4,883 | 1,678 | 1,218 | 2,136,437 | 269,835 | 11,852 | 146,199 | 0 |
| n | 26 / 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 590,077 |
| f_eat | 25 / 26 | 94,657 | 0 | 681 | 0 | 2,413,231 | 282,927 | 12,025 | 154,946 | 0 |
| f_carried | 25 / 26 | 93,665 | 4,888 | 31 | 1,123 | 1,938,064 | 267,599 | 11,489 | 146,724 | 586,692 |
| f_foul | 25 / 24 | 91,914 | 4,716 | 1,534 | 1,221 | 0 | 259,242 | 11,429 | 144,007 | 0 |
| f_seen | 26 / 26 | 93,835 | 4,908 | 1,568 | 1,198 | 2,065,875 | 0 | 11,692 | 146,943 | 0 |
| f_tools | 26 / 26 | 94,359 | 5,037 | 1,661 | 1,254 | 2,181,390 | 276,859 | 0 | 131,759 | 0 |
| f_eat_carried | 26 / 27 | 95,145 | 0 | 23 | 0 | 2,196,995 | 282,394 | 11,825 | 155,696 | 595,430 |
| f_all | 26 / 26 | 94,180 | 0 | 23 | 0 | 0 | 0 | 0 | 133,221 | 585,191 |

**Avoidance (GPT's hypothesis): F (with the penalty) against F-foul (same moments, no penalty).**

| arm | exposures | by weeks since death 0-4 / 5-14 / 15-52 / 53-104 | back within one tile at 4 / 14 / 52 / 104 weeks (of those alive) | went there when within reach, by weeks since exposure 1-4 / 5-14 / 15-52 / 53-104 |
|---|---|---|---|---|
| f | 539,812 | 127,328 / 238,178 / 114,666 / 28,340 | 0.343 / 0.194 / 0.145 / 0.128 | 0.537 / 0.132 / 0.114 / 0.103 |
| f_foul | 520,607 | 125,887 / 232,443 / 106,548 / 25,114 | 0.343 / 0.195 / 0.146 / 0.130 | 0.537 / 0.133 / 0.114 / 0.103 |

| arm | deaths | starvation | illness | old age | thirst | killed |
|---|---|---|---|---|---|---|
| f | 93,372 | 30,418 | 33,607 | 17,015 | 8,855 | 573 |
| n | 93,848 | 31,151 | 33,351 | 16,768 | 8,985 | 655 |
| f_eat | 94,657 | 31,669 | 33,676 | 16,703 | 9,101 | 542 |
| f_carried | 93,665 | 31,091 | 33,357 | 16,895 | 8,916 | 497 |
| f_foul | 91,914 | 30,923 | 32,649 | 16,231 | 8,634 | 569 |
| f_seen | 93,835 | 31,502 | 33,221 | 16,698 | 8,906 | 556 |
| f_tools | 94,359 | 31,513 | 33,753 | 16,776 | 8,853 | 523 |
| f_eat_carried | 95,145 | 31,560 | 34,026 | 17,007 | 9,092 | 532 |
| f_all | 94,180 | 31,316 | 33,546 | 16,562 | 9,156 | 633 |
