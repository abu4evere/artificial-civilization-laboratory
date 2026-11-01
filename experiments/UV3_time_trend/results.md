# UV3 — Is the shrinking habit gap rising returns or climbing values? Results

Frozen as `UV3-frozen`. run_uv3.py, analyse_uv3.py (written before data).

## Validity

- Zero checks (`zero_local.log`): **yes**
- All worlds present (32 of 32): **yes**
- One fingerprint, the same as ES2's (`code_es2`): **yes**
- Every habit update replays exactly (mismatches 0): **yes**
- The replay matches ES2's r arm (world hash, pooled n and sum of abs(q - G); 32 worlds compared): **yes**
- Every counted update in the decade table once: **yes**
- The primary population's B by quarter equals UV2's to 4 decimals: **yes**

**Valid.**

## Primary (frozen): the standardized change in realized return, years 175-199 minus 100-124

Population: k >= 80, ages 16-44, G not closed by death. Cells: age bin x situation x action, common support (at least 100 updates in both quarters), fixed count weights.

| quantity | value [95%] |
|---|---|
| **Delta G** | **-0.0100 [-0.0157, -0.0039]** |
| Delta q (secondary) | +0.0651 [+0.0606, +0.0694] |
| Delta B = Delta q - Delta G (standardized) | +0.0751 |
| common-support cells | 21 of 43 |
| coverage: years 100-124 / 175-199 | 0.996 / 0.999 |

Rule: inconclusive if coverage < 0.8 in either quarter; returns rising if Delta G's interval lies wholly above +0.05; stable if inside [-0.05, +0.05]; falling if wholly below -0.05; else mixed.

**Reading: returns stable.**

## Secondary (described, not decisive)

### The primary population by quarter (not standardized)

| quarter | n | mean q | mean G | B |
|---|---|---|---|---|
| years 100-124 | 327,979 | +0.5428 | +0.6888 | -0.1460 |
| 125-149 | 344,940 | +0.5649 | +0.6835 | -0.1186 |
| 150-174 | 350,287 | +0.5847 | +0.6793 | -0.0945 |
| 175-199 | 352,802 | +0.6015 | +0.6759 | -0.0745 |

### Per decade (k >= 80, ages 16-44, not death-closed)

| decade | n | mean q | mean G | B |
|---|---|---|---|---|
| 100s | 124,769 | +0.5378 | +0.6966 | -0.1588 |
| 110s | 135,111 | +0.5436 | +0.6847 | -0.1411 |
| 120s | 136,049 | +0.5532 | +0.6837 | -0.1306 |
| 130s | 136,957 | +0.5630 | +0.6817 | -0.1187 |
| 140s | 140,033 | +0.5709 | +0.6845 | -0.1136 |
| 150s | 139,712 | +0.5804 | +0.6806 | -0.1003 |
| 160s | 138,497 | +0.5855 | +0.6783 | -0.0928 |
| 170s | 143,707 | +0.5924 | +0.6770 | -0.0846 |
| 180s | 145,800 | +0.6007 | +0.6786 | -0.0779 |
| 190s | 135,373 | +0.6067 | +0.6733 | -0.0666 |

### B by birth decade within each decade (same population; B, with n in brackets)

| decade | born 50s | born 60s | born 70s | born 80s | born 90s | born 100s | born 110s | born 120s | born 130s | born 140s | born 150s | born 160s | born 170s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100s | -0.153 (10,532) | -0.162 (69,239) | -0.157 (41,853) | -0.140 (3,145) | - | - | - | - | - | - | - | - | - |
| 110s | - | -0.149 (12,081) | -0.142 (73,318) | -0.138 (46,828) | -0.134 (2,884) | - | - | - | - | - | - | - | - |
| 120s | - | - | -0.131 (10,975) | -0.134 (79,429) | -0.125 (43,338) | -0.125 (2,307) | - | - | - | - | - | - | - |
| 130s | - | - | - | -0.114 (13,507) | -0.123 (77,197) | -0.113 (44,044) | -0.111 (2,209) | - | - | - | - | - | - |
| 140s | - | - | - | - | -0.112 (11,443) | -0.116 (83,307) | -0.111 (42,740) | -0.092 (2,543) | - | - | - | - | - |
| 150s | - | - | - | - | - | -0.103 (14,456) | -0.103 (78,916) | -0.094 (43,762) | -0.103 (2,578) | - | - | - | - |
| 160s | - | - | - | - | - | - | -0.095 (12,050) | -0.094 (82,068) | -0.091 (42,428) | -0.076 (1,951) | - | - | - |
| 170s | - | - | - | - | - | - | - | -0.088 (13,797) | -0.085 (82,922) | -0.083 (44,836) | -0.085 (2,152) | - | - |
| 180s | - | - | - | - | - | - | - | - | -0.075 (13,685) | -0.081 (84,105) | -0.075 (45,802) | -0.063 (2,208) | - |
| 190s | - | - | - | - | - | - | - | - | - | -0.071 (13,050) | -0.070 (81,044) | -0.059 (39,384) | -0.071 (1,895) |

### Newborns' mean starting habit value by birth decade (all years)

| born | births | mean starting value |
|---|---|---|
| 0s | 2,357 | +0.0015 |
| 10s | 1,214 | +0.0045 |
| 20s | 941 | +0.0074 |
| 30s | 1,108 | +0.0099 |
| 40s | 1,113 | +0.0121 |
| 50s | 1,091 | +0.0142 |
| 60s | 1,089 | +0.0163 |
| 70s | 1,153 | +0.0181 |
| 80s | 1,203 | +0.0198 |
| 90s | 1,158 | +0.0213 |
| 100s | 1,239 | +0.0228 |
| 110s | 1,214 | +0.0242 |
| 120s | 1,211 | +0.0253 |
| 130s | 1,257 | +0.0266 |
| 140s | 1,250 | +0.0276 |
| 150s | 1,280 | +0.0286 |
| 160s | 1,274 | +0.0296 |
| 170s | 1,211 | +0.0306 |
| 180s | 1,282 | +0.0315 |
| 190s | 1,234 | +0.0324 |

### Tools' share of adults' foraged food by quarter

| quarter | share |
|---|---|
| years 100-124 | 0.0368 |
| 125-149 | 0.0353 |
| 150-174 | 0.0328 |
| 175-199 | 0.0299 |

