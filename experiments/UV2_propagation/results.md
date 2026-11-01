# UV2 — Does the habit floor come from unpractised choices further ahead? Results

Frozen as `UV2-frozen`. run_uv2.py, analyse_uv2.py (written before data).

## Validity

- Zero checks (`zero_local.log`): **yes**
- All worlds present (32 of 32): **yes**
- One fingerprint, the same as ES2's (`code_es2`): **yes**
- Every habit update replays exactly, and every completed update had its U (mismatches 0): **yes**
- The replay matches ES2's r arm (world hash, pooled n and sum of abs(q - G); 32 worlds compared): **yes**
- Every counted update binned once: **yes**; Dn outside [0, 1]: **0**
- The primary pooled over all Dn equals UV1's r B_high to 4 decimals: **yes**

**Valid.**

## Primary (frozen): signed bias B = mean(q - G), k >= 80, ages 16-44, G not closed by death

| cell | B [95%] | n | worlds |
|---|---|---|---|
| **Dn < 0.1** (discounted future almost all well-practised choices) | -0.1108 [-0.1151, -0.1064] | 362,963 | 32 of 32 |
| all Dn | -0.1077 [-0.1106, -0.1047] | 1,376,008 | 32 of 32 |

Rule: propagation if the Dn < 0.1 interval lies inside [-0.05, +0.05] and abs(B) <= 0.5 x abs(B over all Dn); not propagation if its whole interval lies below -0.05; else mixed; inconclusive if the cell has under 100,000 updates or updates in under 24 worlds.

**Reading: not propagation.**

## Secondary (described, not decisive)

### Dose-response: B by Dn (k >= 80, ages 16-44, not death-closed)

| Dn | B [95%] | n | worlds |
|---|---|---|---|
| 0-0.05 | -0.0837 [-0.0887, -0.0786] | 143,427 | 32 |
| 0.05-0.1 | -0.1284 [-0.1322, -0.1247] | 219,536 | 32 |
| 0.1-0.2 | -0.1315 [-0.1346, -0.1283] | 406,699 | 32 |
| 0.2-0.4 | -0.1012 [-0.1050, -0.0975] | 466,978 | 32 |
| 0.4-1 | -0.0520 [-0.0592, -0.0449] | 139,368 | 32 |

### B by Dn within each k bin (ages 16-44, not death-closed; B, with n in brackets)

| k | 0-0.05 | 0.05-0.1 | 0.1-0.2 | 0.2-0.4 | 0.4-1 |
|---|---|---|---|---|---|
| 0-9 | -0.313 (35,966) | -0.350 (81,692) | -0.354 (243,077) | -0.318 (608,525) | -0.219 (1,184,740) |
| 10-19 | -0.145 (45,455) | -0.180 (100,600) | -0.186 (282,862) | -0.169 (648,861) | -0.111 (1,001,110) |
| 20-39 | -0.093 (212,788) | -0.136 (332,375) | -0.148 (709,467) | -0.128 (1,192,109) | -0.086 (1,035,501) |
| 40-79 | -0.075 (322,167) | -0.117 (459,170) | -0.130 (881,962) | -0.122 (1,256,892) | -0.096 (965,838) |
| 80-159 | -0.084 (143,165) | -0.128 (219,128) | -0.132 (406,184) | -0.101 (466,581) | -0.052 (139,317) |
| 160+ | -0.134 (262) | -0.100 (408) | -0.084 (515) | -0.052 (397) | -0.029 (51) |

### One-step U: B by the next decision's unpractised mass (k >= 80, ages 16-44, not death-closed)

| U | B [95%] | n |
|---|---|---|
| 0-0.1 | -0.1083 [-0.1117, -0.1048] | 685,815 |
| 0.1-0.25 | -0.1218 [-0.1249, -0.1186] | 255,613 |
| 0.25-0.5 | -0.1116 [-0.1152, -0.1079] | 172,074 |
| 0.5-1 | -0.0898 [-0.0950, -0.0847] | 262,506 |

### Year quarters (k >= 80, ages 16-44, not death-closed)

| quarter | B [95%] | n | share with Dn < 0.1 |
|---|---|---|---|
| years 100-124 | -0.1460 [-0.1490, -0.1427] | 327,979 | 0.244 |
| 125-149 | -0.1186 [-0.1222, -0.1147] | 344,940 | 0.260 |
| 150-174 | -0.0945 [-0.0981, -0.0909] | 350,287 | 0.272 |
| 175-199 | -0.0745 [-0.0779, -0.0711] | 352,802 | 0.278 |

### B by Dn for each age (all k, not death-closed; B, with n in brackets)

| age | 0-0.05 | 0.05-0.1 | 0.1-0.2 | 0.2-0.4 | 0.4-1 |
|---|---|---|---|---|---|
| 1-5 | -0.197 (60) | -0.216 (960) | -0.333 (12,514) | -0.380 (116,570) | -0.391 (2,834,772) |
| 6-11 | -0.342 (16) | -0.326 (256) | -0.361 (1,937) | -0.387 (33,448) | -0.377 (3,398,747) |
| 12-15 | - | -0.389 (24) | -0.409 (735) | -0.314 (31,541) | -0.175 (2,207,661) |
| 16-29 | -0.137 (55,600) | -0.167 (186,325) | -0.191 (762,600) | -0.176 (2,343,785) | -0.129 (3,793,576) |
| 30-44 | -0.094 (704,203) | -0.142 (1,007,048) | -0.151 (1,761,467) | -0.134 (1,829,580) | -0.134 (532,981) |
| 45-59 | -0.095 (1,222,466) | -0.150 (950,902) | -0.148 (970,577) | -0.131 (585,639) | -0.180 (155,731) |
| 60+ | -0.112 (784,940) | -0.179 (429,297) | -0.172 (324,285) | -0.165 (159,742) | -0.230 (63,204) |

