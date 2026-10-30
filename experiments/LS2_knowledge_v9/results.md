# LS2 — where does knowledge go? Results

Frozen as `LS2-frozen`. run_ls2.py (LS1's observer), analyse_ls2.py (LS1's analysis; written before data).

## Validity

- Zero checks: **yes**
- All worlds present (40): **yes**
- One fingerprint (`code_v9`): **yes**
- Ledger balances, kind counts and holdings match in every world: **yes**

**Valid.**

# LP (primary): 40 worlds

## Check against M1 (M1's rules, worlds alive at year 1,000)

- A4 food owed to tools per adult forage act: early 1.516, late 0.1229, late / early 0.081 [0.0607, 0.102] (26 worlds). M1 (v6): A4 0.054 [0.046, 0.063]; B-retained late 0.
- B-retained: early 0.2259, late 0.01376, late / early 0.061 [0, 0.151] (15 worlds). M1 (v6): A4 0.054 [0.046, 0.063]; B-retained late 0.

## Survivorship and population (worlds alive at each bin's start)

| bin (years) | worlds alive | mean population | mean adults | people per 100 land tiles |
|---|---|---|---|---|
| 0-5 | 40 of 40 | 101.0 | 46.6 | 3.95 |
| 5-10 | 40 of 40 | 101.0 | 46.6 | 3.95 |
| 10-20 | 40 of 40 | 101.9 | 49.6 | 3.98 |
| 20-50 | 40 of 40 | 104.0 | 58.6 | 4.06 |
| 50-100 | 40 of 40 | 117.4 | 71.2 | 4.59 |
| 100-200 | 40 of 40 | 123.3 | 77.7 | 4.82 |
| 200-300 | 38 of 40 | 112.4 | 72.5 | 4.39 |
| 300-400 | 35 of 40 | 102.5 | 65.6 | 4.01 |
| 400-500 | 34 of 40 | 96.4 | 61.2 | 3.77 |
| 500-600 | 34 of 40 | 96.5 | 60.7 | 3.77 |
| 600-700 | 34 of 40 | 104.3 | 65.5 | 4.08 |
| 700-800 | 32 of 40 | 117.9 | 73.3 | 4.61 |
| 800-900 | 30 of 40 | 127.7 | 79.3 | 4.99 |
| 900-1000 | 28 of 40 | 146.3 | 90.4 | 5.72 |

Worlds that ended before year 1,000 (year): [117, 153, 237, 271, 286, 370, 635, 671, 731, 733, 830, 850, 908, 931].

## Q1 — The ledger: copy loss and kind extinction

Inflow by route and outflow by channel, per 1,000 person-years (worlds alive at each bin's start).

| bin | in: invented | in: rediscovered | in: taught | in: copied | in: read | in: other | out: pushout | out: useless | out: death | net | losses per held recipe-year |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0-5 | 153.9 | 351.5 | 65.3 | 1.4 | 4.2 | 0.0 | 2.2 | 0.0 | 38.1 | +535.8 | 0.038 |
| 5-10 | 301.8 | 749.8 | 159.6 | 0.8 | 58.7 | 0.0 | 178.0 | 0.0 | 205.8 | +886.9 | 0.077 |
| 10-20 | 97.4 | 443.9 | 139.0 | 0.4 | 54.5 | 0.0 | 195.7 | 0.0 | 241.0 | +298.6 | 0.050 |
| 20-50 | 49.4 | 288.5 | 61.2 | 0.1 | 26.2 | 0.0 | 97.2 | 0.0 | 300.3 | +27.9 | 0.040 |
| 50-100 | 25.9 | 211.4 | 57.6 | 0.0 | 22.6 | 0.0 | 47.5 | 0.0 | 265.0 | +5.0 | 0.033 |
| 100-200 | 10.6 | 147.7 | 58.3 | 0.0 | 14.2 | 0.0 | 14.9 | 0.0 | 244.9 | -29.1 | 0.033 |
| 200-300 | 4.3 | 107.6 | 48.8 | 0.0 | 8.5 | 0.0 | 3.3 | 0.0 | 192.6 | -26.6 | 0.034 |
| 300-400 | 2.2 | 89.5 | 42.7 | 0.0 | 4.9 | 0.0 | 1.0 | 0.0 | 154.3 | -16.0 | 0.034 |
| 400-500 | 1.2 | 79.1 | 41.3 | 0.0 | 3.8 | 0.0 | 0.6 | 0.0 | 131.3 | -6.5 | 0.034 |
| 500-600 | 0.7 | 70.8 | 38.6 | 0.0 | 3.3 | 0.0 | 0.5 | 0.0 | 115.8 | -3.0 | 0.034 |
| 600-700 | 0.5 | 65.3 | 34.6 | 0.0 | 2.9 | 0.0 | 0.3 | 0.0 | 104.4 | -1.4 | 0.034 |
| 700-800 | 0.5 | 63.1 | 31.9 | 0.0 | 3.1 | 0.0 | 0.3 | 0.0 | 98.6 | -0.3 | 0.035 |
| 800-900 | 0.4 | 63.3 | 29.5 | 0.0 | 2.8 | 0.0 | 0.2 | 0.0 | 95.8 | +0.1 | 0.035 |
| 900-1000 | 0.5 | 64.8 | 29.9 | 0.0 | 3.4 | 0.0 | 0.4 | 0.0 | 96.9 | +1.4 | 0.036 |

- **Net flow first turns negative and stays negative:** never.
- **The dominant copy-loss channel after year 100:** **death** (pushout 0.020 [0.0181, 0.0216]; useless 0.000 [0, 0]; death 0.980 [0.978, 0.982]; 487257 events in 40 worlds).
- **The dominant kind-extinction channel after year 100:** **death** (pushout 0.021 [0.0187, 0.0236]; useless 0.000 [0, 0]; death 0.979 [0.976, 0.981]; 50086 events in 40 worlds).

## Q2 — Origin, transmission, persistence (useful kinds: a factor > 1)

| origin | era first made | useful kinds | ever held by 2+ people | still held 25 years after the maker's death (eligible) | held 2+ generations after the maker |
|---|---|---|---|---|---|
| founder | years 0-100 | 4878 | 0.651 | 0.432 (of 4878) | 0.590 |
| founder | years 100-1,000 | 0 | - | - | - |
| world-born | years 0-100 | 22475 | 0.304 | 0.128 (of 22458) | 0.257 |
| world-born | years 100-1,000 | 10345 | 0.135 | 0.025 (of 10172) | 0.101 |

- Founder share of useful know-how held in years 0-100 (person-recipe-weeks): 0.733 [0.719, 0.746] (descriptive).

## Q3 — The making funnel

Adults (16+). Feasible per adult person-week; weighed given feasible; chosen given weighed; chosen per adult person-week. Teens (12-15) after the bar.

| bin | worlds | feasible | weighed / feasible | chosen / weighed | chosen per person-week | teens: chosen per person-week |
|---|---|---|---|---|---|---|
| 0-5 | 40 | 0.232 | 0.474 | 0.0367 | 0.00404 | 0.00000 |
| 5-10 | 40 | 0.562 | 0.600 | 0.0306 | 0.01032 | 0.00000 |
| 10-20 | 40 | 0.708 | 0.678 | 0.0256 | 0.01227 | 0.01707 |
| 20-50 | 40 | 0.750 | 0.779 | 0.0116 | 0.00679 | 0.00866 |
| 50-100 | 40 | 0.779 | 0.816 | 0.0040 | 0.00254 | 0.00295 |
| 100-200 | 40 | 0.804 | 0.818 | 0.0018 | 0.00119 | 0.00123 |
| 200-300 | 38 | 0.766 | 0.807 | 0.0012 | 0.00072 | 0.00077 |
| 300-400 | 35 | 0.728 | 0.795 | 0.0010 | 0.00060 | 0.00062 |
| 400-500 | 34 | 0.706 | 0.792 | 0.0010 | 0.00059 | 0.00059 |
| 500-600 | 34 | 0.680 | 0.774 | 0.0010 | 0.00051 | 0.00051 |
| 600-700 | 34 | 0.659 | 0.763 | 0.0010 | 0.00048 | 0.00047 |
| 700-800 | 32 | 0.646 | 0.761 | 0.0010 | 0.00050 | 0.00048 |
| 800-900 | 30 | 0.630 | 0.762 | 0.0011 | 0.00050 | 0.00050 |
| 900-1000 | 28 | 0.629 | 0.763 | 0.0011 | 0.00053 | 0.00051 |

**The decline decomposition (frozen): years 0-10 to years 100-200,** Δ ln(chosen per person-week) = Δ ln(feasible) + Δ ln(weighed | feasible) + Δ ln(chosen | weighed), pooled counts.

- feasible: Δ ln +0.765 [0.732, 0.799]; share of the decline -0.44 [-0.476, -0.41]
- weighed given feasible: Δ ln +0.387 [0.357, 0.418]; share of the decline -0.22 [-0.245, -0.203]
- chosen given weighed: Δ ln -2.887 [-2.97, -2.8]; share of the decline 1.66 [1.62, 1.72]
- Total Δ ln(chosen per person-week): -1.736. **The gate carrying the largest share: chosen given weighed.**
- When making was weighed and not chosen (after year 100), what won: forage 0.67, gather 0.10, put 0.09, rest 0.04, join 0.04, talk 0.03.

## Q4 — The fall in A4, exactly (A4 = s × g × k)

Worlds alive at year 1,000: 26. Decades 2-4: s 0.588, g 21.34, k 0.119; decades 95-99: s 0.051, g 21.47, k 0.132.

- s, the share of forage acts with a tool: Δ ln -2.449 [-2.75, -2.24]; share of the fall 1.05
- g, food per tool act: Δ ln +0.006 [-0.0132, 0.0254]; share of the fall -0.00
- k, the tool's share of that food: Δ ln +0.108 [0.0722, 0.14]; share of the fall -0.05
- Total Δ ln A4: -2.335.
- Tools used in decades 2-4: made by the holder 0.559, made by someone else 0.064, unknown 0.376; made in the first 20 years 0.064.

| bin | forage tool lost: replaced within a year | not replaced |
|---|---|---|
| 0-5 | 0.644 | 715 of 2006 |
| 5-10 | 0.738 | 615 of 2344 |
| 10-20 | 0.716 | 1331 of 4686 |
| 20-50 | 0.508 | 10924 of 22192 |
| 50-100 | 0.309 | 27099 of 39245 |
| 100-200 | 0.196 | 42870 of 53346 |
| 200-300 | 0.144 | 28970 of 33850 |
| 300-400 | 0.128 | 22535 of 25829 |
| 400-500 | 0.122 | 19779 of 22523 |
| 500-600 | 0.126 | 18185 of 20799 |
| 600-700 | 0.117 | 18564 of 21024 |
| 700-800 | 0.128 | 19571 of 22453 |
| 800-900 | 0.133 | 20100 of 23185 |
| 900-1000 | 0.144 | 21720 of 25387 |

## Q5 — Does each generation replace what it inherits?

World-born people, by birth cohort (50-year bands). Inheritance: of the useful recipes their carers held while they were 0-16, the share they ever acquired by 30.

| born (years) | people | inheritance rate [95%] | inherited by: taught / own making / other | useful acquired by 30 (mean) | acquired by 16: taught / copied / own (mean) | used: acquired from others and later made | onward: passed to someone younger | survival: outlived them by 25 years |
|---|---|---|---|---|---|---|---|---|
| 0-50 | 6057 | 0.391 [0.385, 0.398] | 0.22 / 0.66 / 0.12 | 14.85 | 1.75 / 0.00 / 12.16 | 0.151 | 0.032 | 0.823 |
| 50-100 | 5399 | 0.317 [0.307, 0.328] | 0.23 / 0.64 / 0.13 | 11.50 | 1.65 / 0.00 / 8.76 | 0.052 | 0.031 | 0.853 |
| 100-150 | 5342 | 0.293 [0.281, 0.306] | 0.27 / 0.64 / 0.09 | 9.13 | 1.56 / 0.00 / 6.62 | 0.036 | 0.033 | 0.873 |
| 150-200 | 5115 | 0.273 [0.265, 0.281] | 0.26 / 0.67 / 0.07 | 7.49 | 1.25 / 0.00 / 5.39 | 0.032 | 0.034 | 0.882 |
| 200-250 | 4526 | 0.260 [0.255, 0.266] | 0.27 / 0.67 / 0.05 | 6.30 | 1.09 / 0.00 / 4.52 | 0.031 | 0.036 | 0.884 |
| 250-300 | 4220 | 0.254 [0.247, 0.26] | 0.29 / 0.67 / 0.04 | 5.51 | 0.99 / 0.00 / 3.89 | 0.033 | 0.037 | 0.891 |
| 300-350 | 3937 | 0.251 [0.242, 0.26] | 0.30 / 0.67 / 0.03 | 4.93 | 0.88 / 0.00 / 3.44 | 0.034 | 0.036 | 0.892 |
| 350-400 | 3637 | 0.254 [0.246, 0.262] | 0.30 / 0.67 / 0.03 | 4.57 | 0.87 / 0.00 / 3.16 | 0.035 | 0.041 | 0.896 |
| 400-450 | 3618 | 0.257 [0.245, 0.268] | 0.33 / 0.64 / 0.02 | 4.27 | 0.86 / 0.00 / 2.83 | 0.041 | 0.041 | 0.900 |
| 450-500 | 3480 | 0.256 [0.246, 0.268] | 0.34 / 0.64 / 0.03 | 4.04 | 0.82 / 0.00 / 2.64 | 0.040 | 0.044 | 0.904 |
| 500-550 | 3589 | 0.250 [0.24, 0.262] | 0.35 / 0.63 / 0.02 | 3.82 | 0.81 / 0.00 / 2.44 | 0.042 | 0.042 | 0.909 |
| 550-600 | 3666 | 0.250 [0.237, 0.264] | 0.36 / 0.62 / 0.02 | 3.60 | 0.76 / 0.00 / 2.27 | 0.041 | 0.045 | 0.917 |
| 600-650 | 3786 | 0.256 [0.243, 0.269] | 0.35 / 0.63 / 0.02 | 3.43 | 0.72 / 0.00 / 2.18 | 0.040 | 0.049 | 0.919 |
| 650-700 | 3925 | 0.254 [0.242, 0.267] | 0.35 / 0.63 / 0.02 | 3.25 | 0.66 / 0.00 / 2.06 | 0.038 | 0.046 | 0.914 |
| 700-750 | 4018 | 0.251 [0.237, 0.263] | 0.35 / 0.63 / 0.02 | 3.22 | 0.66 / 0.00 / 2.02 | 0.050 | 0.044 | 0.921 |
| 750-800 | 4066 | 0.243 [0.232, 0.254] | 0.32 / 0.65 / 0.03 | 3.10 | 0.58 / 0.00 / 2.00 | 0.043 | 0.043 | 0.925 |
| 800-850 | 4094 | 0.257 [0.242, 0.269] | 0.34 / 0.64 / 0.02 | 3.13 | 0.59 / 0.00 / 2.00 | 0.054 | 0.043 | 0.933 |
| 850-900 | 4192 | 0.252 [0.237, 0.266] | 0.33 / 0.65 / 0.02 | 3.10 | 0.57 / 0.00 / 1.98 | 0.049 | 0.043 | 0.934 |
| 900-950 | 4334 | 0.261 [0.245, 0.275] | 0.33 / 0.64 / 0.03 | 3.12 | 0.58 / 0.00 / 1.97 | 0.053 | 0.044 | 0.943 |
| 950-1000 | 3006 | 0.254 [0.238, 0.268] | 0.33 / 0.64 / 0.02 | 3.08 | 0.60 / 0.00 / 2.04 | 0.044 | 0.039 | 0.919 |

- New knowledge: useful kinds invented by world-born people: 29229; held by someone of a later generation: 5607 (0.192).

## Described: teaching, skill and habits

| bin | lessons offered per person-year | taken | taken from parents / carers / kin / others | taken lessons later made | later passed on |
|---|---|---|---|---|---|
| 0-5 | 0.55 | 0.126 | 13 / 0 / 31 / 1225 | 0.414 | 0.188 |
| 5-10 | 2.38 | 0.073 | 1049 / 11 / 929 / 1500 | 0.304 | 0.091 |
| 10-20 | 3.56 | 0.044 | 2142 / 40 / 2381 / 1795 | 0.247 | 0.088 |
| 20-50 | 1.98 | 0.034 | 2493 / 97 / 3848 / 1911 | 0.201 | 0.090 |
| 50-100 | 1.64 | 0.039 | 3608 / 151 / 6412 / 4621 | 0.116 | 0.074 |
| 100-200 | 1.18 | 0.054 | 5912 / 270 / 11372 / 12942 | 0.063 | 0.052 |
| 200-300 | 0.73 | 0.073 | 3226 / 162 / 8698 / 10222 | 0.050 | 0.042 |
| 300-400 | 0.53 | 0.087 | 2348 / 110 / 6816 / 7302 | 0.055 | 0.041 |
| 400-500 | 0.49 | 0.091 | 2127 / 91 / 5940 / 6507 | 0.061 | 0.046 |
| 500-600 | 0.42 | 0.096 | 1960 / 100 / 5010 / 6364 | 0.063 | 0.046 |
| 600-700 | 0.38 | 0.096 | 1861 / 48 / 4493 / 6129 | 0.061 | 0.049 |
| 700-800 | 0.34 | 0.100 | 1766 / 89 / 4282 / 6046 | 0.067 | 0.041 |
| 800-900 | 0.31 | 0.101 | 1675 / 82 / 3813 / 5829 | 0.074 | 0.047 |
| 900-1000 | 0.31 | 0.102 | 1811 / 66 / 3869 / 6276 | 0.059 | 0.040 |

| born (years) | crafting skill at 16 | at 30 | practice weeks per person | making habit at 16 | carer's | talk partners' |
|---|---|---|---|---|---|---|
| 0-50 | 0.483 | 0.521 | 44.2 | 0.0068 | 0.0065 | 0.0066 |
| 50-100 | 0.299 | 0.331 | 22.3 | 0.0144 | 0.0144 | 0.0144 |
| 100-200 | 0.196 | 0.219 | 13.6 | 0.0204 | 0.0204 | 0.0204 |
| 200-400 | 0.123 | 0.140 | 8.4 | 0.0280 | 0.0281 | 0.0280 |
| 400-600 | 0.083 | 0.099 | 6.0 | 0.0357 | 0.0358 | 0.0357 |
| 600-800 | 0.067 | 0.082 | 5.1 | 0.0413 | 0.0412 | 0.0413 |
| 800-900 | 0.064 | 0.081 | 5.0 | 0.0460 | 0.0461 | 0.0460 |
| 900-1000 | 0.065 | 0.082 | 4.7 | 0.0482 | 0.0481 | 0.0482 |

