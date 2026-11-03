# AM2: AM1's autonomy battery on nature v12 (results)

Frozen as `AM2-frozen`. run_am2.py, analyse_am2.py (written before data).

## Validity

- Zero checks (All: PASS, same `code_v12` fingerprint): **yes**
- All worlds present (160): **yes**
- One fingerprint, `code_v12`'s: **yes**
- Sanity (fewer acts completes no chain): **yes**

**Valid.**

## The three measures with frozen predictions (each predicted lower in no habits and in more chance)

| measure | arm | value | arm − v12 [95%] | sample |
|---|---|---|---|---|
| M1 | v12 | 0.0804 |  | person pairs 36,936 |
| M1 | no habits | 0.0875 | +0.0071 [-0.0025, +0.0174] | person pairs 27,102 |
| M1 | more chance | 0.0770 | -0.0034 [-0.0112, +0.0052] | person pairs 33,414 |
| M1 | sham | 0.0810 | +0.0007 [-0.0089, +0.0105] | person pairs 36,891 |
| M3 | v12 | 0.0036 |  | gather chains 687,828, matched 6,316,842 |
| M3 | no habits | 0.0276 | +0.0240 [+0.0224, +0.0257] | gather chains 688,959, matched 5,852,150 |
| M3 | fewer acts | nan | +nan [+nan, +nan] | gather chains 0, matched 99 |
| M3 | more chance | 0.0076 | +0.0040 [+0.0035, +0.0045] | gather chains 622,554, matched 6,528,386 |
| M3 | sham | 0.0033 | -0.0003 [-0.0006, +0.0001] | gather chains 676,610, matched 6,245,698 |
| M5 | v12 | 0.0037 |  | gather chains 272,773, matched 2,399,984 |
| M5 | no habits | 0.0305 | +0.0269 [+0.0250, +0.0287] | gather chains 237,730, matched 2,178,740 |
| M5 | fewer acts | nan | +nan [+nan, +nan] | gather chains 0, matched 37 |
| M5 | more chance | 0.0080 | +0.0043 [+0.0038, +0.0049] | gather chains 246,234, matched 2,545,728 |
| M5 | sham | 0.0034 | -0.0003 [-0.0007, +0.0002] | gather chains 269,462, matched 2,380,664 |

Rule: validated if v12 − no habits and v12 − more chance both have 95% intervals wholly above 0; partly validated if only one does; otherwise not validated (reported, not dropped). Unstable if the sham − v11 interval lies wholly outside ±(half the v12 − no habits point difference).

**M1: not validated.**
**M3: not validated.**
**M5: not validated.**

## Described (no frozen prediction)

| measure | v12 | no habits | fewer acts | more chance | sham | v12 − no habits [95%] | v12 − more chance [95%] |
|---|---|---|---|---|---|---|---|
| M2 (bits beyond shuffle, per adult-year) | 0.1619 | 0.1320 | 0.1637 | 0.1394 | 0.1625 | +0.0299 [+0.0243, +0.0353] | +0.0226 [+0.0187, +0.0269] |
| M4 new tile targets | 0.0563 | 0.0675 | 0.0532 | 0.0582 | 0.0547 | -0.0112 [-0.0160, -0.0066] | -0.0020 [-0.0051, +0.0009] |
| M4 new person targets | 0.1168 | 0.1759 | 0.1104 | 0.1128 | 0.1129 | -0.0591 [-0.0724, -0.0454] | +0.0041 [-0.0036, +0.0105] |
| M4 new recipes made | 0.0866 | 0.0319 | nan | 0.0682 | 0.0915 | +0.0547 [+0.0422, +0.0679] | +0.0184 [+0.0028, +0.0327] |
| M6a new in steps | 0.2630 | 0.4838 | nan | 0.2796 | 0.2543 | -0.2208 [-0.2396, -0.2016] | -0.0166 [-0.0345, +0.0032] |
| M6b transfer to a new cue | 0.3913 | 0.5068 | nan | 0.4823 | 0.4477 | -0.1155 [-0.1745, -0.0505] | -0.0910 [-0.1540, -0.0219] |

## v12 against v11, arm c (described only; different seeds, unpaired)

AM2's 32 worlds (seeds 22801–22832) against AM1's 32 (seeds 22501–22532). It never redefines success.

| measure | v12 | v11 | v12 − v11 [95%] |
|---|---|---|---|
| M1 | 0.0804 | 0.0821 | -0.0018 [-0.0131, +0.0092] |
| M3 | 0.0036 | 0.0036 | +0.0000 [-0.0004, +0.0004] |
| M5 | 0.0037 | 0.0038 | -0.0001 [-0.0006, +0.0004] |
| M2 (bits beyond shuffle, per adult-year) | 0.1619 | 0.1630 | -0.0011 [-0.0089, +0.0071] |
| M4 new tile targets | 0.0563 | 0.0612 | -0.0049 [-0.0133, +0.0037] |
| M4 new person targets | 0.1168 | 0.1237 | -0.0068 [-0.0210, +0.0076] |
| M4 new recipes made | 0.0866 | 0.0894 | -0.0028 [-0.0223, +0.0165] |
| M6a new in steps | 0.2630 | 0.2469 | +0.0160 [-0.0048, +0.0386] |
| M6b transfer to a new cue | 0.3913 | 0.4422 | -0.0509 [-0.1392, +0.0370] |


## Population (beside every measure)

| arm | living-weeks | adult-weeks (16–49) | extinct worlds |
|---|---|---|---|
| v12 | 23,176,597 | 12,206,512 | 0 |
| no habits | 18,243,321 | 9,262,708 | 3 |
| fewer acts | 23,282,840 | 12,265,247 | 0 |
| more chance | 21,224,492 | 11,102,499 | 2 |
| sham | 23,134,685 | 12,204,649 | 0 |

