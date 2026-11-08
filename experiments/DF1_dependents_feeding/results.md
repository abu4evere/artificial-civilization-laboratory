# DF1: who feeds the children, and what does it cost them? (results)

Frozen as `DF1-frozen`. run_df1.py, analyse_df1.py (written before data).

## Validity

- Zero checks (All: PASS, `code_v16` fingerprint): **yes**
- All worlds present (32): **yes**
- One fingerprint, `code_v16`'s: **yes**

**Valid.**

## Primary: feeding-caused short weeks per 1,000 grown person-weeks

A feeding-caused short week: the person held at least their own need before feeding dependents, and ended the week short (deficit > 0.05).

- Women: **7.384** [6.740, 8.025] (54,928 of 7,438,652 person-weeks)
- Men: **0.735** [0.650, 0.823] (6,918 of 9,411,660)
- Women − men: **+6.649** [+6.067, +7.227]
- Women's share of all feeding-caused short weeks: **0.8881** [0.8790, 0.8969]

**Reading (frozen): feeding drives the gap.**

Rule: 'feeding drives the gap' if women − men is above 0 with its lower bound above 0 and women's share is at least 0.75; 'feeding does not explain it' if the interval includes 0 or men's rate is higher.

## By age band

| band | sex | person-weeks | with dependents | dependents per week | fed out per week | short weeks per 1,000 | feeding-caused per 1,000 |
|---|---|---|---|---|---|---|---|
| 16-29 | women | 2,782,032 | 0.225 | 0.319 | 0.744 | 36.37 | 6.68 |
| 16-29 | men | 3,007,938 | 0.028 | 0.044 | 0.062 | 31.61 | 0.57 |
| 30-49 | women | 2,916,476 | 0.583 | 1.067 | 1.661 | 36.56 | 12.25 |
| 30-49 | men | 3,789,855 | 0.103 | 0.157 | 0.143 | 30.14 | 1.14 |
| 50+ | women | 1,740,144 | 0.150 | 0.183 | 0.035 | 27.29 | 0.35 |
| 50+ | men | 2,613,867 | 0.048 | 0.068 | 0.038 | 28.90 | 0.34 |

## Who feeds

- Dependent-weeks by caregiver (counted body phases): mother 4,253,879 (0.815), father 817,672 (0.157), other 150,492 (0.029)
- Food gifts to one's own children under 12: fathers 53,994 gifts (391,134.8 food); mothers 0 gifts (0.0 food).

## The energy link (the next decision with energy below 25: in v16 forage is then offered nowhere)

| sex | after a feeding-caused short week | after another short week | after a week not short |
|---|---|---|---|
| women | 0.0953 (54,810) | 0.0828 (199,313) | 0.0001 (7,180,530) |
| men | 0.1014 (6,895) | 0.0407 (277,156) | 0.0000 (9,123,390) |

