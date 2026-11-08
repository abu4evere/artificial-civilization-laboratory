# OD1: open the world's closed doors, once (results)

Frozen as `OD1-frozen`. run_od1.py, analyse_od1.py (written before data).

## Validity

- Zero checks (All: PASS, `code_od1` fingerprint): **yes**
- All worlds present (128): **yes**
- One fingerprint, `code_od1`'s: **yes**
- MP1's part-tracking checks in every world: failures 0: **yes**

**Valid.**

## Manipulation counts (reported first)

| door | v16 | doors (D1-D5) | doors without D1 | sham |
|---|---|---|---|---|
| D1 makes with a stand-in input (per 1,000 makes) | 0.000 (0) | 99.736 (4,983) | 0.000 (0) | 0.000 (0) |
| D2 weeks above the old made-thing limit (per 1,000 grown weeks) | 0.000 (0) | 6.005 (99,329) | 5.935 (101,627) | 0.000 (0) |
| D2 weeks above the old material limit (per 1,000 grown weeks) | 0.000 (0) | 68.026 (1,125,147) | 64.352 (1,101,878) | 0.000 (0) |
| D3 made binders used (per 1,000 grown weeks) | 0.000 (0) | 0.349 (5,765) | 0.335 (5,729) | 0.000 (0) |
| D4 made hammers used (per 1,000 grown weeks) | 0.000 (0) | 1.243 (20,561) | 1.169 (20,022) | 0.000 (0) |
| D5 weeks a second thing adds warmth (per 1,000 grown weeks) | 0.000 (0) | 3.596 (59,473) | 3.276 (56,095) | 0.000 (0) |
| D5 weeks a second thing adds carrying (per 1,000 grown weeks) | 0.000 (0) | 3.624 (59,938) | 3.313 (56,722) | 0.000 (0) |

## Reading (frozen)

- **What goes live: doors (D1-D5)** (the full package (D1-D5) raises no guard).
- **Reading: no harm detected under the tested conditions.**
- Guards raised: doors none; doors without D1 none; sham none (validity check).

Rule (the creator's bar): the doors go live if they raise no guard; if they do and the doors without D1 do not, those go live and D1 stays closed; if both do, nothing goes live. A door used fewer than 32 times in all worlds is reported as barely exercised; the doors still go live, labelled so. A pass means no detected harm under the tested conditions, not that the doors are harmless.

## Guards: doors (D1-D5) against v16

| guard | doors (D1-D5) | v16 | vs v16 [95%] |
|---|---|---|---|
| starvation deaths per 1,000 living-years (ratio) | 4.8229 | 4.2050 | 1.1469 [0.9946, 1.3428] |
| killing deaths per 1,000 living-years (difference) | 0.0111 | 0.0022 | +0.0088 [-0.0023, +0.0236] |
| adult health, mean (difference) | 93.3238 | 93.6620 | -0.3382 [-0.9036, +0.2044] |
| living-weeks (ratio) | 23,483,122.0000 | 23,260,610.0000 | 1.0096 [0.9090, 1.1195] |
| extinct worlds (extra) | 0.0000 | 1.0000 | -1.0000 [+nan, +nan] |
| child deaths per 1,000 child-years (ratio) | 9.4355 | 8.0453 | 1.1728 [0.9664, 1.4351] |
| child starvation deaths per 1,000 child-years (ratio) | 5.5579 | 4.6845 | 1.1864 [0.9278, 1.5337] |
| food gifts to kin's children per 1,000 adult-weeks (ratio) | 5.2059 | 5.1429 | 1.0123 [0.9206, 1.1018] |

## Guards: doors without D1 against v16

| guard | doors without D1 | v16 | vs v16 [95%] |
|---|---|---|---|
| starvation deaths per 1,000 living-years (ratio) | 4.5090 | 4.2050 | 1.0723 [0.9579, 1.2051] |
| killing deaths per 1,000 living-years (difference) | 0.0043 | 0.0022 | +0.0021 [-0.0048, +0.0093] |
| adult health, mean (difference) | 93.4644 | 93.6620 | -0.1976 [-0.7516, +0.4063] |
| living-weeks (ratio) | 24,114,599.0000 | 23,260,610.0000 | 1.0367 [0.9402, 1.1478] |
| extinct worlds (extra) | 0.0000 | 1.0000 | -1.0000 [+nan, +nan] |
| child deaths per 1,000 child-years (ratio) | 9.0261 | 8.0453 | 1.1219 [0.9563, 1.3247] |
| child starvation deaths per 1,000 child-years (ratio) | 5.3939 | 4.6845 | 1.1514 [0.9237, 1.4532] |
| food gifts to kin's children per 1,000 adult-weeks (ratio) | 4.9621 | 5.1429 | 0.9648 [0.8863, 1.0523] |

## Guards: sham against v16

| guard | sham | v16 | vs v16 [95%] |
|---|---|---|---|
| starvation deaths per 1,000 living-years (ratio) | 4.6064 | 4.2050 | 1.0955 [0.9536, 1.2453] |
| killing deaths per 1,000 living-years (difference) | 0.0045 | 0.0022 | +0.0023 [-0.0047, +0.0103] |
| adult health, mean (difference) | 93.3944 | 93.6620 | -0.2677 [-0.7698, +0.2409] |
| living-weeks (ratio) | 23,152,760.0000 | 23,260,610.0000 | 0.9954 [0.9054, 1.0959] |
| extinct worlds (extra) | 1.0000 | 1.0000 | +0.0000 [+nan, +nan] |
| child deaths per 1,000 child-years (ratio) | 8.5436 | 8.0453 | 1.0619 [0.9249, 1.2405] |
| child starvation deaths per 1,000 child-years (ratio) | 4.7734 | 4.6845 | 1.0190 [0.8314, 1.2641] |
| food gifts to kin's children per 1,000 adult-weeks (ratio) | 5.2574 | 5.1429 | 1.0223 [0.9288, 1.1183] |

## Descriptives (not gates)

| arm | attacks | by a holder of a hard made thing | killings | by such a holder | made things carried, mean (sd) | max | materials carried, mean | makes per grown year |
|---|---|---|---|---|---|---|---|---|
| v16 | 199 | 164 | 1 | 1 | 1.336 (0.882) | 3 | 14.338 | 0.1536 |
| doors (D1-D5) | 228 | 186 | 5 | 4 | 1.295 (0.872) | 6 | 15.116 | 0.1571 |
| doors without D1 | 218 | 184 | 1 | 1 | 1.327 (0.901) | 6 | 15.160 | 0.1474 |
| sham | 183 | 136 | 2 | 1 | 1.144 (0.808) | 3 | 14.251 | 0.1455 |

| arm | things made with a stand-in: mean best tool factor | from the remembered inputs |
|---|---|---|
| v16 | nan (0) | 1.5554 (48,945) |
| doors (D1-D5) | 1.4683 (4,983) | 1.5693 (44,979) |
| doors without D1 | nan (0) | 1.5636 (48,549) |
| sham | nan (0) | 1.5630 (45,708) |

| arm | new kinds needing a made part | any made part held (B+) | all held (C+) | made again (E) |
|---|---|---|---|---|
| v16 | 3,741 | 0.1096 | 0.0438 | 0.0150 |
| doors (D1-D5) | 5,369 | 0.1185 | 0.0665 | 0.0127 |
| doors without D1 | 5,215 | 0.1221 | 0.0694 | 0.0140 |
| sham | 3,633 | 0.0988 | 0.0413 | 0.0168 |

