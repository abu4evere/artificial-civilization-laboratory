# AM1: Measuring autonomy against constrained controls (results)

Frozen as `AM1-frozen`. run_am1.py, analyse_am1.py (written before data).

## Validity

- Zero checks (All: PASS, same `code_v11` fingerprint): **yes**
- All worlds present (160): **yes**
- One fingerprint, `code_v11`'s: **yes**
- Sanity (fewer acts completes no chain): **yes**

**Valid.**

## The three measures with frozen predictions (each predicted lower in no habits and in more chance)

| measure | arm | value | arm − v11 [95%] | sample |
|---|---|---|---|---|
| M1 | v11 | 0.0821 |  | person pairs 35,359 |
| M1 | no habits | 0.0859 | +0.0038 [-0.0059, +0.0136] | person pairs 24,695 |
| M1 | more chance | 0.0478 | -0.0344 [-0.0812, -0.0047] | person pairs 33,233 |
| M1 | sham | 0.0826 | +0.0005 [-0.0102, +0.0108] | person pairs 35,468 |
| M3 | v11 | 0.0036 |  | gather chains 658,091, matched 6,051,007 |
| M3 | no habits | 0.0293 | +0.0257 [+0.0238, +0.0277] | gather chains 635,873, matched 5,285,248 |
| M3 | fewer acts | nan | +nan [+nan, +nan] | gather chains 0, matched 1,019 |
| M3 | more chance | 0.0077 | +0.0041 [+0.0034, +0.0047] | gather chains 605,745, matched 6,520,661 |
| M3 | sham | 0.0035 | -0.0001 [-0.0005, +0.0003] | gather chains 673,130, matched 5,996,496 |
| M5 | v11 | 0.0038 |  | gather chains 260,387, matched 2,310,587 |
| M5 | no habits | 0.0318 | +0.0280 [+0.0259, +0.0302] | gather chains 216,851, matched 1,961,079 |
| M5 | fewer acts | nan | +nan [+nan, +nan] | gather chains 0, matched 407 |
| M5 | more chance | 0.0083 | +0.0045 [+0.0037, +0.0053] | gather chains 241,415, matched 2,531,208 |
| M5 | sham | 0.0035 | -0.0002 [-0.0007, +0.0003] | gather chains 265,681, matched 2,277,508 |

Rule: validated if v11 − no habits and v11 − more chance both have 95% intervals wholly above 0; partly validated if only one does; otherwise not validated (reported, not dropped). Unstable if the sham − v11 interval lies wholly outside ±(half the v11 − no habits point difference).

**M1: partly validated (by more chance only).**
**M3: not validated.**
**M5: not validated.**

## Described (no frozen prediction)

| measure | v11 | no habits | fewer acts | more chance | sham | v11 − no habits [95%] | v11 − more chance [95%] |
|---|---|---|---|---|---|---|---|
| M2 (bits beyond shuffle, per adult-year) | 0.1630 | 0.1318 | 0.1641 | 0.1389 | 0.1639 | +0.0312 [+0.0250, +0.0368] | +0.0241 [+0.0200, +0.0281] |
| M4 new tile targets | 0.0612 | 0.0756 | 0.0607 | 0.0663 | 0.0618 | -0.0143 [-0.0190, -0.0094] | -0.0051 [-0.0087, -0.0018] |
| M4 new person targets | 0.1237 | 0.1844 | 0.1272 | 0.1291 | 0.1262 | -0.0608 [-0.0734, -0.0468] | -0.0055 [-0.0156, +0.0037] |
| M4 new recipes made | 0.0894 | 0.0311 | nan | 0.0685 | 0.0859 | +0.0582 [+0.0446, +0.0723] | +0.0209 [+0.0065, +0.0345] |
| M6a new in steps | 0.2469 | 0.4753 | nan | 0.2951 | 0.2461 | -0.2283 [-0.2510, -0.2058] | -0.0481 [-0.0685, -0.0268] |
| M6b transfer to a new cue | 0.4422 | 0.4971 | nan | 0.4660 | 0.3913 | -0.0549 [-0.1152, +0.0152] | -0.0238 [-0.0979, +0.0625] |

## Population (beside every measure)

| arm | living-weeks | adult-weeks (16–49) | extinct worlds |
|---|---|---|---|
| v11 | 22,182,887 | 11,649,823 | 1 |
| no habits | 16,576,852 | 8,415,054 | 1 |
| fewer acts | 21,807,441 | 11,481,814 | 0 |
| more chance | 21,213,665 | 11,058,721 | 0 |
| sham | 22,385,275 | 11,728,989 | 0 |

