# LS1 — where does knowledge go? Results

Frozen as `LS1-frozen`. run_ls1.py, analyse_ls1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (96): **yes**
- One fingerprint (`code_v7`): **yes**
- Ledger balances, kind counts and holdings match in every world: **yes**

**Valid.**

# LP (primary): 64 worlds

## Check against M1 (M1's rules, worlds alive at year 1,000)

- A4 food owed to tools per adult forage act: early 0.9047, late 0.05497, late / early 0.061 [0.0503, 0.0721] (51 worlds). M1 (v6): A4 0.054 [0.046, 0.063]; B-retained late 0.
- B-retained: early 0.2349, late 0, late / early 0.000 [0, 0] (21 worlds). M1 (v6): A4 0.054 [0.046, 0.063]; B-retained late 0.

## Survivorship and population (worlds alive at each bin's start)

| bin (years) | worlds alive | mean population | mean adults | people per 100 land tiles |
|---|---|---|---|---|
| 0-5 | 64 of 64 | 104.3 | 48.5 | 4.08 |
| 5-10 | 64 of 64 | 104.3 | 48.5 | 4.08 |
| 10-20 | 64 of 64 | 107.2 | 52.9 | 4.19 |
| 20-50 | 64 of 64 | 113.5 | 64.5 | 4.44 |
| 50-100 | 64 of 64 | 129.1 | 79.8 | 5.05 |
| 100-200 | 64 of 64 | 117.8 | 76.5 | 4.61 |
| 200-300 | 63 of 64 | 91.5 | 59.7 | 3.58 |
| 300-400 | 61 of 64 | 77.5 | 50.3 | 3.03 |
| 400-500 | 59 of 64 | 76.8 | 49.1 | 3.00 |
| 500-600 | 55 of 64 | 80.6 | 51.2 | 3.15 |
| 600-700 | 54 of 64 | 83.3 | 52.6 | 3.25 |
| 700-800 | 52 of 64 | 87.9 | 55.1 | 3.44 |
| 800-900 | 52 of 64 | 95.1 | 59.3 | 3.72 |
| 900-1000 | 51 of 64 | 102.1 | 63.4 | 3.99 |

Worlds that ended before year 1,000 (year): [156, 267, 287, 361, 375, 409, 418, 454, 459, 504, 628, 669, 872].

## Q1 — The ledger: copy loss and kind extinction

Inflow by route and outflow by channel, per 1,000 person-years (worlds alive at each bin's start).

| bin | in: invented | in: rediscovered | in: taught | in: copied | in: read | in: other | out: pushout | out: useless | out: death | net | losses per held recipe-year |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0-5 | 138.5 | 321.8 | 71.4 | 1.1 | 2.4 | 0.0 | 1.7 | 0.0 | 28.9 | +504.5 | 0.032 |
| 5-10 | 269.0 | 733.7 | 167.0 | 0.6 | 52.9 | 0.0 | 165.6 | 0.0 | 171.7 | +886.0 | 0.071 |
| 10-20 | 88.6 | 424.4 | 152.0 | 0.2 | 47.0 | 0.0 | 180.8 | 0.0 | 204.1 | +327.3 | 0.045 |
| 20-50 | 46.6 | 268.6 | 69.9 | 0.0 | 24.1 | 0.0 | 88.3 | 0.0 | 281.3 | +39.6 | 0.037 |
| 50-100 | 25.1 | 192.8 | 66.1 | 0.0 | 20.3 | 0.0 | 43.1 | 0.0 | 258.6 | +2.7 | 0.032 |
| 100-200 | 10.0 | 127.6 | 71.5 | 0.0 | 12.2 | 0.0 | 13.9 | 0.0 | 249.1 | -41.7 | 0.033 |
| 200-300 | 3.8 | 90.0 | 69.7 | 0.0 | 5.9 | 0.0 | 3.4 | 0.0 | 196.3 | -30.2 | 0.034 |
| 300-400 | 1.9 | 70.7 | 68.6 | 0.0 | 3.0 | 0.0 | 1.3 | 0.0 | 159.7 | -16.7 | 0.034 |
| 400-500 | 0.8 | 57.0 | 62.7 | 0.0 | 2.1 | 0.0 | 0.5 | 0.0 | 131.8 | -9.7 | 0.034 |
| 500-600 | 0.5 | 50.2 | 52.8 | 0.0 | 1.6 | 0.0 | 0.2 | 0.0 | 110.7 | -5.7 | 0.035 |
| 600-700 | 0.4 | 45.6 | 50.0 | 0.0 | 1.2 | 0.0 | 0.1 | 0.0 | 97.8 | -0.8 | 0.034 |
| 700-800 | 0.3 | 41.8 | 46.7 | 0.0 | 1.1 | 0.0 | 0.1 | 0.0 | 90.8 | -1.0 | 0.035 |
| 800-900 | 0.2 | 38.1 | 43.2 | 0.0 | 0.9 | 0.0 | 0.1 | 0.0 | 83.8 | -1.4 | 0.036 |
| 900-1000 | 0.1 | 36.3 | 38.8 | 0.0 | 0.8 | 0.0 | 0.1 | 0.0 | 75.9 | +0.0 | 0.036 |

- **Net flow first turns negative and stays negative:** never.
- **The dominant copy-loss channel after year 100:** **death** (pushout 0.021 [0.0189, 0.0223]; useless 0.000 [0, 0]; death 0.979 [0.978, 0.981]; 661439 events in 64 worlds).
- **The dominant kind-extinction channel after year 100:** **death** (pushout 0.021 [0.0192, 0.0229]; useless 0.000 [0, 0]; death 0.979 [0.977, 0.981]; 71152 events in 64 worlds).

## Q2 — Origin, transmission, persistence (useful kinds: a factor > 1)

| origin | era first made | useful kinds | ever held by 2+ people | still held 25 years after the maker's death (eligible) | held 2+ generations after the maker |
|---|---|---|---|---|---|
| founder | years 0-100 | 5616 | 0.734 | 0.548 (of 5616) | 0.693 |
| founder | years 100-1,000 | 0 | - | - | - |
| world-born | years 0-100 | 37337 | 0.298 | 0.136 (of 37334) | 0.245 |
| world-born | years 100-1,000 | 13203 | 0.121 | 0.031 (of 13143) | 0.081 |

- Founder share of useful know-how held in years 0-100 (person-recipe-weeks): 0.727 [0.719, 0.735] (descriptive).

## Q3 — The making funnel

Adults (16+). Feasible per adult person-week; weighed given feasible; chosen given weighed; chosen per adult person-week. Teens (12-15) after the bar.

| bin | worlds | feasible | weighed / feasible | chosen / weighed | chosen per person-week | teens: chosen per person-week |
|---|---|---|---|---|---|---|
| 0-5 | 64 | 0.229 | 0.486 | 0.0268 | 0.00298 | 0.00000 |
| 5-10 | 64 | 0.553 | 0.630 | 0.0229 | 0.00796 | 0.00000 |
| 10-20 | 64 | 0.720 | 0.711 | 0.0195 | 0.00999 | 0.01285 |
| 20-50 | 64 | 0.784 | 0.796 | 0.0082 | 0.00515 | 0.00628 |
| 50-100 | 64 | 0.792 | 0.812 | 0.0026 | 0.00170 | 0.00195 |
| 100-200 | 64 | 0.802 | 0.808 | 0.0012 | 0.00075 | 0.00082 |
| 200-300 | 63 | 0.762 | 0.798 | 0.0008 | 0.00050 | 0.00048 |
| 300-400 | 61 | 0.733 | 0.796 | 0.0007 | 0.00038 | 0.00041 |
| 400-500 | 59 | 0.716 | 0.779 | 0.0006 | 0.00034 | 0.00034 |
| 500-600 | 55 | 0.692 | 0.767 | 0.0006 | 0.00029 | 0.00029 |
| 600-700 | 54 | 0.675 | 0.771 | 0.0005 | 0.00027 | 0.00028 |
| 700-800 | 52 | 0.658 | 0.759 | 0.0005 | 0.00024 | 0.00024 |
| 800-900 | 52 | 0.638 | 0.751 | 0.0005 | 0.00022 | 0.00021 |
| 900-1000 | 51 | 0.624 | 0.734 | 0.0005 | 0.00021 | 0.00019 |

**The decline decomposition (frozen): years 0-10 to years 100-200,** Δ ln(chosen per person-week) = Δ ln(feasible) + Δ ln(weighed | feasible) + Δ ln(chosen | weighed), pooled counts.

- feasible: Δ ln +0.773 [0.752, 0.794]; share of the decline -0.40 [-0.422, -0.381]
- weighed given feasible: Δ ln +0.333 [0.311, 0.354]; share of the decline -0.17 [-0.187, -0.158]
- chosen given weighed: Δ ln -3.034 [-3.1, -2.97]; share of the decline 1.57 [1.54, 1.61]
- Total Δ ln(chosen per person-week): -1.928. **The gate carrying the largest share: chosen given weighed.**
- When making was weighed and not chosen (after year 100), what won: forage 0.68, gather 0.09, put 0.07, rest 0.06, join 0.05, talk 0.03.

## Q4 — The fall in A4, exactly (A4 = s × g × k)

Worlds alive at year 1,000: 51. Decades 2-4: s 0.318, g 21.20, k 0.132; decades 95-99: s 0.021, g 21.07, k 0.123.

- s, the share of forage acts with a tool: Δ ln -2.712 [-2.92, -2.51]; share of the fall 0.97
- g, food per tool act: Δ ln -0.006 [-0.0199, 0.00887]; share of the fall 0.00
- k, the tool's share of that food: Δ ln -0.067 [-0.0968, -0.0366]; share of the fall 0.02
- Total Δ ln A4: -2.786.
- Tools used in decades 2-4: made by the holder 0.981, made by someone else 0.013, unknown 0.006; made in the first 20 years 0.046.

| bin | forage tool lost: replaced within a year | not replaced |
|---|---|---|
| 0-5 | 0.593 | 1184 of 2909 |
| 5-10 | 0.489 | 2165 of 4234 |
| 10-20 | 0.523 | 5230 of 10966 |
| 20-50 | 0.374 | 23537 of 37603 |
| 50-100 | 0.221 | 38785 of 49784 |
| 100-200 | 0.135 | 49636 of 57359 |
| 200-300 | 0.104 | 29861 of 33312 |
| 300-400 | 0.088 | 21654 of 23740 |
| 400-500 | 0.076 | 18117 of 19605 |
| 500-600 | 0.073 | 17303 of 18670 |
| 600-700 | 0.073 | 16732 of 18051 |
| 700-800 | 0.066 | 16614 of 17783 |
| 800-900 | 0.068 | 16843 of 18070 |
| 900-1000 | 0.067 | 17356 of 18603 |

## Q5 — Does each generation replace what it inherits?

World-born people, by birth cohort (50-year bands). Inheritance: of the useful recipes their carers held while they were 0-16, the share they ever acquired by 30.

| born (years) | people | inheritance rate [95%] | inherited by: taught / own making / other | useful acquired by 30 (mean) | acquired by 16: taught / copied / own (mean) | used: acquired from others and later made | onward: passed to someone younger | survival: outlived them by 25 years |
|---|---|---|---|---|---|---|---|---|
| 0-50 | 10385 | 0.410 [0.405, 0.415] | 0.24 / 0.65 / 0.11 | 14.50 | 2.00 / 0.00 / 11.71 | 0.103 | 0.036 | 0.829 |
| 50-100 | 9373 | 0.315 [0.309, 0.322] | 0.27 / 0.62 / 0.11 | 11.06 | 1.89 / 0.00 / 8.19 | 0.030 | 0.036 | 0.852 |
| 100-150 | 8416 | 0.290 [0.281, 0.299] | 0.32 / 0.61 / 0.08 | 8.77 | 1.87 / 0.00 / 6.11 | 0.021 | 0.038 | 0.867 |
| 150-200 | 7136 | 0.281 [0.272, 0.29] | 0.37 / 0.58 / 0.06 | 7.33 | 1.80 / 0.00 / 4.86 | 0.020 | 0.043 | 0.871 |
| 200-250 | 6180 | 0.272 [0.261, 0.283] | 0.39 / 0.57 / 0.03 | 6.16 | 1.64 / 0.00 / 4.01 | 0.021 | 0.046 | 0.877 |
| 250-300 | 5614 | 0.266 [0.254, 0.277] | 0.41 / 0.57 / 0.02 | 5.29 | 1.48 / 0.00 / 3.35 | 0.021 | 0.050 | 0.880 |
| 300-350 | 4968 | 0.275 [0.264, 0.286] | 0.46 / 0.53 / 0.01 | 4.87 | 1.53 / 0.00 / 2.96 | 0.022 | 0.054 | 0.882 |
| 350-400 | 4796 | 0.275 [0.263, 0.287] | 0.48 / 0.51 / 0.01 | 4.37 | 1.50 / 0.00 / 2.50 | 0.023 | 0.060 | 0.889 |
| 400-450 | 4675 | 0.274 [0.259, 0.288] | 0.50 / 0.49 / 0.01 | 3.91 | 1.40 / 0.00 / 2.15 | 0.028 | 0.058 | 0.897 |
| 450-500 | 4594 | 0.280 [0.264, 0.295] | 0.51 / 0.49 / 0.01 | 3.58 | 1.27 / 0.00 / 1.99 | 0.026 | 0.061 | 0.899 |
| 500-550 | 4705 | 0.269 [0.255, 0.283] | 0.51 / 0.48 / 0.01 | 3.29 | 1.15 / 0.00 / 1.85 | 0.030 | 0.060 | 0.896 |
| 550-600 | 4812 | 0.273 [0.257, 0.288] | 0.51 / 0.49 / 0.01 | 2.99 | 1.03 / 0.00 / 1.67 | 0.031 | 0.063 | 0.902 |
| 600-650 | 4768 | 0.278 [0.263, 0.293] | 0.52 / 0.47 / 0.01 | 2.92 | 1.02 / 0.00 / 1.62 | 0.032 | 0.064 | 0.907 |
| 650-700 | 4924 | 0.278 [0.264, 0.29] | 0.53 / 0.47 / 0.01 | 2.81 | 1.02 / 0.00 / 1.50 | 0.032 | 0.062 | 0.907 |
| 700-750 | 4983 | 0.276 [0.258, 0.294] | 0.52 / 0.47 / 0.01 | 2.62 | 0.94 / 0.00 / 1.41 | 0.027 | 0.064 | 0.908 |
| 750-800 | 5185 | 0.286 [0.27, 0.303] | 0.56 / 0.44 / 0.01 | 2.59 | 0.98 / 0.00 / 1.34 | 0.030 | 0.065 | 0.909 |
| 800-850 | 5430 | 0.275 [0.259, 0.291] | 0.56 / 0.43 / 0.01 | 2.42 | 0.91 / 0.00 / 1.25 | 0.027 | 0.063 | 0.918 |
| 850-900 | 5570 | 0.271 [0.257, 0.284] | 0.54 / 0.45 / 0.01 | 2.31 | 0.85 / 0.00 / 1.22 | 0.030 | 0.066 | 0.920 |
| 900-950 | 5792 | 0.273 [0.257, 0.288] | 0.55 / 0.44 / 0.00 | 2.23 | 0.79 / 0.00 / 1.17 | 0.034 | 0.063 | 0.925 |
| 950-1000 | 4076 | 0.264 [0.25, 0.278] | 0.54 / 0.46 / 0.00 | 2.09 | 0.77 / 0.00 / 1.14 | 0.029 | 0.058 | 0.909 |

- New knowledge: useful kinds invented by world-born people: 45610; held by someone of a later generation: 8816 (0.193).

## Described: teaching, skill and habits

| bin | lessons offered per person-year | taken | taken from parents / carers / kin / others | taken lessons later made | later passed on |
|---|---|---|---|---|---|
| 0-5 | 0.56 | 0.130 | 13 / 0 / 79 / 2092 | 0.344 | 0.186 |
| 5-10 | 2.36 | 0.077 | 1618 / 16 / 1580 / 2826 | 0.250 | 0.088 |
| 10-20 | 3.95 | 0.043 | 3476 / 77 / 4380 / 3596 | 0.187 | 0.077 |
| 20-50 | 2.51 | 0.031 | 5138 / 190 / 7089 / 4267 | 0.132 | 0.073 |
| 50-100 | 2.02 | 0.036 | 7875 / 297 / 11819 / 10292 | 0.067 | 0.057 |
| 100-200 | 1.52 | 0.052 | 12359 / 562 / 19968 / 26816 | 0.040 | 0.052 |
| 200-300 | 1.15 | 0.066 | 8141 / 351 / 14251 / 21336 | 0.032 | 0.052 |
| 300-400 | 0.97 | 0.077 | 6526 / 282 / 11265 / 16969 | 0.033 | 0.062 |
| 400-500 | 0.84 | 0.080 | 5231 / 268 / 9114 / 14353 | 0.039 | 0.065 |
| 500-600 | 0.68 | 0.083 | 4464 / 194 / 7422 / 12271 | 0.041 | 0.068 |
| 600-700 | 0.65 | 0.080 | 4174 / 135 / 6792 / 12038 | 0.042 | 0.076 |
| 700-800 | 0.58 | 0.085 | 4067 / 195 / 6618 / 11432 | 0.042 | 0.071 |
| 800-900 | 0.53 | 0.085 | 4056 / 175 / 6239 / 11664 | 0.040 | 0.069 |
| 900-1000 | 0.46 | 0.088 | 3745 / 151 / 5869 / 11163 | 0.036 | 0.060 |

| born (years) | crafting skill at 16 | at 30 | practice weeks per person | making habit at 16 | carer's | talk partners' |
|---|---|---|---|---|---|---|
| 0-50 | 0.452 | 0.488 | 39.1 | 0.0054 | 0.0052 | 0.0053 |
| 50-100 | 0.276 | 0.299 | 19.3 | 0.0107 | 0.0107 | 0.0107 |
| 100-200 | 0.183 | 0.199 | 12.1 | 0.0145 | 0.0145 | 0.0145 |
| 200-400 | 0.108 | 0.120 | 7.1 | 0.0191 | 0.0191 | 0.0191 |
| 400-600 | 0.064 | 0.074 | 4.3 | 0.0236 | 0.0236 | 0.0236 |
| 600-800 | 0.048 | 0.057 | 3.4 | 0.0268 | 0.0268 | 0.0267 |
| 800-900 | 0.041 | 0.049 | 2.9 | 0.0290 | 0.0290 | 0.0290 |
| 900-1000 | 0.038 | 0.047 | 2.5 | 0.0299 | 0.0299 | 0.0299 |

# D80 (secondary, described): 32 worlds

## Survivorship and population (worlds alive at each bin's start)

| bin (years) | worlds alive | mean population | mean adults | people per 100 land tiles |
|---|---|---|---|---|
| 0-5 | 32 of 32 | 63.2 | 31.7 | 9.88 |
| 5-10 | 32 of 32 | 63.2 | 31.7 | 9.88 |
| 10-20 | 32 of 32 | 53.8 | 28.4 | 8.40 |
| 20-50 | 32 of 32 | 45.1 | 26.6 | 7.05 |
| 50-100 | 32 of 32 | 45.5 | 28.8 | 7.11 |
| 100-200 | 30 of 32 | 43.8 | 28.6 | 6.84 |
| 200-300 | 26 of 32 | 32.2 | 21.8 | 5.02 |
| 300-400 | 24 of 32 | 28.0 | 18.4 | 4.37 |
| 400-500 | 16 of 32 | 31.9 | 21.1 | 4.98 |
| 500-600 | 12 of 32 | 33.3 | 21.3 | 5.20 |
| 600-700 | 10 of 32 | 37.5 | 23.9 | 5.86 |
| 700-800 | 9 of 32 (thin) | 38.4 | 24.6 | 6.00 |
| 800-900 | 9 of 32 (thin) | 40.9 | 26.2 | 6.39 |
| 900-1000 | 7 of 32 (thin) | 46.0 | 28.6 | 7.19 |

Worlds that ended before year 1,000 (year): [85, 100, 130, 133, 154, 170, 205, 238, 305, 323, 324, 338, 339, 343, 354, 385, 404, 405, 417, 487, 518, 563, 677, 841, 898].

## Q1 — The ledger: copy loss and kind extinction

Inflow by route and outflow by channel, per 1,000 person-years (worlds alive at each bin's start).

| bin | in: invented | in: rediscovered | in: taught | in: copied | in: read | in: other | out: pushout | out: useless | out: death | net | losses per held recipe-year |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0-5 | 108.4 | 222.4 | 56.0 | 5.2 | 2.5 | 0.0 | 0.4 | 0.0 | 52.2 | +341.7 | 0.075 |
| 5-10 | 270.6 | 642.6 | 149.9 | 2.4 | 75.1 | 0.0 | 122.7 | 0.0 | 222.8 | +795.0 | 0.082 |
| 10-20 | 94.7 | 381.3 | 94.3 | 1.1 | 76.8 | 0.0 | 144.7 | 0.0 | 300.4 | +203.0 | 0.054 |
| 20-50 | 51.1 | 245.1 | 40.8 | 0.2 | 28.8 | 0.0 | 70.7 | 0.0 | 343.5 | -48.2 | 0.043 |
| 50-100 | 26.4 | 176.3 | 44.8 | 0.0 | 24.8 | 0.0 | 28.9 | 0.0 | 283.3 | -39.9 | 0.034 |
| 100-200 | 10.2 | 117.7 | 43.7 | 0.0 | 17.1 | 0.0 | 8.0 | 0.0 | 224.4 | -43.6 | 0.032 |
| 200-300 | 3.4 | 78.0 | 37.8 | 0.0 | 7.4 | 0.0 | 0.8 | 0.0 | 170.6 | -44.8 | 0.035 |
| 300-400 | 2.0 | 57.5 | 35.6 | 0.0 | 3.7 | 0.0 | 0.4 | 0.0 | 118.5 | -20.2 | 0.034 |
| 400-500 | 0.7 | 43.1 | 27.2 | 0.0 | 1.8 | 0.0 | 0.1 | 0.0 | 88.3 | -15.6 | 0.034 |
| 500-600 | 0.3 | 36.8 | 22.1 | 0.0 | 0.8 | 0.0 | 0.1 | 0.0 | 67.4 | -7.5 | 0.033 |
| 600-700 | 0.2 | 32.9 | 19.8 | 0.0 | 0.8 | 0.0 | 0.0 | 0.0 | 54.7 | -1.0 | 0.031 |
| 700-800 | (fewer than 10 worlds: no reading) | | | | | | | | | | |
| 800-900 | (fewer than 10 worlds: no reading) | | | | | | | | | | |
| 900-1000 | (fewer than 10 worlds: no reading) | | | | | | | | | | |

- **Net flow first turns negative and stays negative:** 20-50.
- **The dominant copy-loss channel after year 100:** **death** (pushout 0.017 [0.0134, 0.0228]; useless 0.000 [0, 0]; death 0.983 [0.977, 0.987]; 61556 events in 30 worlds).
- **The dominant kind-extinction channel after year 100:** **death** (pushout 0.017 [0.0134, 0.0214]; useless 0.000 [0, 0]; death 0.983 [0.979, 0.987]; 11048 events in 30 worlds).

## Q2 — Origin, transmission, persistence (useful kinds: a factor > 1)

| origin | era first made | useful kinds | ever held by 2+ people | still held 25 years after the maker's death (eligible) | held 2+ generations after the maker |
|---|---|---|---|---|---|
| founder | years 0-100 | 1787 | 0.718 | 0.528 (of 1787) | 0.649 |
| founder | years 100-1,000 | 0 | - | - | - |
| world-born | years 0-100 | 9253 | 0.284 | 0.122 (of 9205) | 0.214 |
| world-born | years 100-1,000 | 1906 | 0.111 | 0.033 (of 1841) | 0.072 |

- Founder share of useful know-how held in years 0-100 (person-recipe-weeks): 0.670 [0.65, 0.689] (descriptive).

## Q3 — The making funnel

Adults (16+). Feasible per adult person-week; weighed given feasible; chosen given weighed; chosen per adult person-week. Teens (12-15) after the bar.

| bin | worlds | feasible | weighed / feasible | chosen / weighed | chosen per person-week | teens: chosen per person-week |
|---|---|---|---|---|---|---|
| 0-5 | 32 | 0.176 | 0.473 | 0.0218 | 0.00181 | 0.00000 |
| 5-10 | 32 | 0.509 | 0.606 | 0.0200 | 0.00615 | 0.00000 |
| 10-20 | 32 | 0.682 | 0.654 | 0.0184 | 0.00824 | 0.01277 |
| 20-50 | 32 | 0.740 | 0.785 | 0.0084 | 0.00489 | 0.00592 |
| 50-100 | 32 | 0.768 | 0.816 | 0.0024 | 0.00148 | 0.00169 |
| 100-200 | 30 | 0.775 | 0.771 | 0.0008 | 0.00049 | 0.00063 |
| 200-300 | 26 | 0.737 | 0.754 | 0.0005 | 0.00027 | 0.00025 |
| 300-400 | 24 | 0.666 | 0.744 | 0.0006 | 0.00031 | 0.00020 |
| 400-500 | 16 | 0.600 | 0.692 | 0.0004 | 0.00015 | 0.00008 |
| 500-600 | 12 | 0.554 | 0.710 | 0.0003 | 0.00010 | 0.00008 |
| 600-700 | 10 | 0.527 | 0.673 | 0.0003 | 0.00010 | 0.00009 |

**The decline decomposition (frozen): years 0-10 to years 100-200,** Δ ln(chosen per person-week) = Δ ln(feasible) + Δ ln(weighed | feasible) + Δ ln(chosen | weighed), pooled counts.

- feasible: Δ ln +0.936 [0.894, 0.981]; share of the decline -0.48 [-0.532, -0.437]
- weighed given feasible: Δ ln +0.327 [0.288, 0.365]; share of the decline -0.17 [-0.198, -0.141]
- chosen given weighed: Δ ln -3.206 [-3.32, -3.09]; share of the decline 1.65 [1.58, 1.73]
- Total Δ ln(chosen per person-week): -1.943. **The gate carrying the largest share: chosen given weighed.**
- When making was weighed and not chosen (after year 100), what won: forage 0.69, put 0.09, gather 0.09, rest 0.06, join 0.03, talk 0.02.

## Q4 — The fall in A4, exactly (A4 = s × g × k)

Worlds alive at year 1,000: 7. Decades 2-4: s 0.250, g 20.65, k 0.122; decades 95-99: s 0.007, g 21.62, k 0.110.

- s, the share of forage acts with a tool: Δ ln -3.590 [-4.11, -3.08]; share of the fall 0.98
- g, food per tool act: Δ ln +0.046 [0.00329, 0.0768]; share of the fall -0.01
- k, the tool's share of that food: Δ ln -0.106 [-0.221, 0.0155]; share of the fall 0.03
- Total Δ ln A4: -3.650.
- Tools used in decades 2-4: made by the holder 0.971, made by someone else 0.021, unknown 0.008; made in the first 20 years 0.060.

| bin | forage tool lost: replaced within a year | not replaced |
|---|---|---|
| 0-5 | 0.551 | 509 of 1134 |
| 5-10 | 0.473 | 824 of 1565 |
| 10-20 | 0.533 | 1588 of 3401 |
| 20-50 | 0.383 | 5094 of 8250 |
| 50-100 | 0.231 | 6845 of 8899 |
| 100-200 | 0.150 | 7058 of 8308 |
| 200-300 | 0.111 | 3520 of 3958 |
| 300-400 | 0.105 | 1958 of 2187 |
| 400-500 | 0.074 | 1242 of 1341 |
| 500-600 | 0.081 | 914 of 995 |
| 600-700 | 0.059 | 901 of 958 |

## Q5 — Does each generation replace what it inherits?

World-born people, by birth cohort (50-year bands). Inheritance: of the useful recipes their carers held while they were 0-16, the share they ever acquired by 30.

| born (years) | people | inheritance rate [95%] | inherited by: taught / own making / other | useful acquired by 30 (mean) | acquired by 16: taught / copied / own (mean) | used: acquired from others and later made | onward: passed to someone younger | survival: outlived them by 25 years |
|---|---|---|---|---|---|---|---|---|
| 0-50 | 2242 | 0.403 [0.395, 0.41] | 0.15 / 0.68 / 0.17 | 14.03 | 1.23 / 0.00 / 11.82 | 0.096 | 0.022 | 0.767 |
| 50-100 | 1538 | 0.298 [0.287, 0.308] | 0.18 / 0.66 / 0.17 | 10.38 | 1.19 / 0.00 / 8.06 | 0.016 | 0.022 | 0.798 |
| 100-150 | 1361 | 0.275 [0.263, 0.285] | 0.22 / 0.64 / 0.14 | 7.83 | 1.12 / 0.00 / 5.80 | 0.011 | 0.022 | 0.813 |
| 150-200 | 1152 | 0.251 [0.236, 0.265] | 0.24 / 0.66 / 0.10 | 5.94 | 0.83 / 0.00 / 4.46 | 0.015 | 0.025 | 0.808 |
| 200-250 | 826 | 0.252 [0.235, 0.268] | 0.29 / 0.65 / 0.06 | 5.10 | 0.85 / 0.00 / 3.75 | 0.018 | 0.025 | 0.795 |
| 250-300 | 657 | 0.245 [0.231, 0.262] | 0.32 / 0.64 / 0.04 | 4.33 | 0.79 / 0.00 / 3.12 | 0.022 | 0.031 | 0.781 |
| 300-350 | 552 | 0.243 [0.223, 0.264] | 0.38 / 0.60 / 0.02 | 3.62 | 0.84 / 0.00 / 2.51 | 0.022 | 0.040 | 0.805 |
| 350-400 | 520 | 0.233 [0.205, 0.263] | 0.36 / 0.60 / 0.04 | 3.07 | 0.63 / 0.00 / 2.15 | 0.013 | 0.030 | 0.792 |
| 400-450 | 424 | 0.239 [0.211, 0.288] | 0.36 / 0.63 / 0.01 | 2.64 | 0.51 / 0.00 / 1.90 | 0.021 | 0.035 | 0.824 |
| 450-500 | 397 | 0.232 [0.195, 0.272] | 0.39 / 0.60 / 0.01 | 2.31 | 0.49 / 0.00 / 1.68 | 0.012 | 0.035 | 0.800 |
| 500-550 | 375 | 0.217 [0.175, 0.251] | 0.40 / 0.59 / 0.01 | 2.12 | 0.39 / 0.00 / 1.51 | 0.008 | 0.037 | 0.809 |
| 550-600 | 372 | 0.253 [0.197, 0.289] | 0.39 / 0.61 / 0.00 | 1.99 | 0.43 / 0.00 / 1.41 | 0.008 | 0.053 | 0.839 |
| 600-650 | 393 | 0.200 [0.168, 0.236] | 0.37 / 0.62 / 0.02 | 1.84 | 0.33 / 0.00 / 1.37 | 0.010 | 0.022 | 0.799 |
| 650-700 | 390 | 0.217 [0.196, 0.235] | 0.40 / 0.59 / 0.01 | 1.69 | 0.34 / 0.00 / 1.12 | 0.017 | 0.041 | 0.849 |
| 700-750 | 362 | 0.231 [0.188, 0.261] | 0.41 / 0.59 / 0.00 | 1.87 | 0.41 / 0.00 / 1.27 | 0.012 | 0.038 | 0.846 |
| 750-800 | 403 | 0.228 [0.202, 0.255] | 0.47 / 0.53 / 0.00 | 1.77 | 0.38 / 0.00 / 1.16 | 0.012 | 0.033 | 0.849 |
| 800-850 | 368 | 0.201 [0.181, 0.24] | 0.36 / 0.63 / 0.01 | 1.57 | 0.27 / 0.00 / 1.12 | 0.006 | 0.036 | 0.834 |
| 850-900 | 340 | 0.199 [0.156, 0.235] | 0.43 / 0.55 / 0.02 | 1.56 | 0.30 / 0.00 / 1.05 | 0.011 | 0.035 | 0.868 |
| 900-950 | 351 | 0.188 [0.135, 0.234] | 0.39 / 0.60 / 0.01 | 1.55 | 0.30 / 0.00 / 1.09 | 0.011 | 0.030 | 0.856 |
| 950-1000 | 255 | 0.202 [0.144, 0.269] | 0.43 / 0.56 / 0.01 | 1.45 | 0.29 / 0.00 / 0.99 | 0.000 | 0.041 | nan |

- New knowledge: useful kinds invented by world-born people: 10193; held by someone of a later generation: 2008 (0.197).

## Described: teaching, skill and habits

| bin | lessons offered per person-year | taken | taken from parents / carers / kin / others | taken lessons later made | later passed on |
|---|---|---|---|---|---|
| 0-5 | 0.44 | 0.132 | 0 / 0 / 18 / 696 | 0.262 | 0.113 |
| 5-10 | 2.02 | 0.080 | 298 / 10 / 407 / 1015 | 0.171 | 0.036 |
| 10-20 | 2.51 | 0.042 | 443 / 20 / 652 / 863 | 0.150 | 0.041 |
| 20-50 | 1.36 | 0.033 | 401 / 38 / 1002 / 562 | 0.133 | 0.051 |
| 50-100 | 1.20 | 0.041 | 568 / 34 / 2007 / 1013 | 0.047 | 0.034 |
| 100-200 | 0.75 | 0.063 | 650 / 39 / 2917 / 2149 | 0.027 | 0.032 |
| 200-300 | 0.48 | 0.083 | 305 / 21 / 1643 / 1265 | 0.027 | 0.034 |
| 300-400 | 0.44 | 0.085 | 228 / 6 / 1092 / 650 | 0.033 | 0.056 |
| 400-500 | 0.35 | 0.081 | 116 / 8 / 565 / 471 | 0.026 | 0.054 |
| 500-600 | 0.25 | 0.093 | 73 / 6 / 423 / 304 | 0.021 | 0.035 |
| 600-700 | 0.22 | 0.095 | 67 / 8 / 407 / 263 | 0.021 | 0.028 |

| born (years) | crafting skill at 16 | at 30 | practice weeks per person | making habit at 16 | carer's | talk partners' |
|---|---|---|---|---|---|---|
| 0-50 | 0.460 | 0.487 | 38.5 | 0.0041 | 0.0039 | 0.0040 |
| 50-100 | 0.264 | 0.283 | 17.5 | 0.0081 | 0.0080 | 0.0080 |
| 100-200 | 0.164 | 0.175 | 9.9 | 0.0106 | 0.0105 | 0.0106 |
| 200-400 | 0.094 | 0.101 | 5.7 | 0.0129 | 0.0129 | 0.0129 |
| 400-600 | 0.052 | 0.056 | 3.1 | 0.0148 | 0.0148 | 0.0148 |
| 600-800 | 0.038 | 0.041 | 2.2 | 0.0160 | 0.0159 | 0.0160 |
| 800-900 | 0.035 | 0.039 | 2.1 | 0.0161 | 0.0160 | 0.0161 |
| 900-1000 | 0.032 | 0.037 | 1.8 | 0.0165 | 0.0164 | 0.0165 |

