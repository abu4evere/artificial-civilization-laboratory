# VW1: what a valued whole needs is wanted (results)

Frozen as `VW1-frozen`. run_vw1.py, analyse_vw1.py (written before data).

## Validity

- Zero checks (All: PASS, `code_vw1` fingerprint): **yes**
- All worlds present (96): **yes**
- One fingerprint, `code_vw1`'s: **yes**
- Part-tracking checks in every world (1,185 tracked parts): failures 0: **yes**

**Valid.**

## Reading (frozen)

- **VW: no harm, no effect.** Guards raised: none.
- Co-primary 1, any made part held (MP1 stage B or beyond): VW 0.1095 against v16 0.1011: +0.0084 [-0.0046, +0.0210].
- Co-primary 2, all made parts held at once (MP1 stage C or beyond): VW 0.0494 against v16 0.0431: +0.0063 [-0.0049, +0.0171].
- Sham: co-primary 1 0.1001 against v16 0.1011: -0.0010 [-0.0191, +0.0176]; co-primary 2 0.0367 against v16 0.0431: -0.0064 [-0.0166, +0.0035]; guards raised: none.

Rule: 'supported' if no guard is raised and both co-primaries' lower bounds are above 0 (then a confirmatory run on new seeds); 'partly supported' if only co-primary 1's is; 'harm' if any guard is raised; 'no harm, no effect' otherwise.

## Guards (VW against v16; the sham against v16 beside it)

| guard | VW | v16 | VW vs v16 [95%] | sham vs v16 [95%] |
|---|---|---|---|---|
| starvation deaths per 1,000 living-years (ratio) | 3.7476 | 4.2906 | 0.8734 [0.7716, 0.9791] | 0.9194 [0.8252, 1.0236] |
| killing deaths per 1,000 living-years (difference) | 0.0022 | 0.0047 | -0.0025 [-0.0103, +0.0050] | -0.0001 [-0.0093, +0.0088] |
| adult health, mean (difference) | 94.1356 | 93.4331 | +0.7025 [+0.1391, +1.3057] | +0.5933 [-0.0051, +1.2036] |
| living-weeks (ratio) | 23,546,830.0000 | 21,960,395.0000 | 1.0722 [0.9577, 1.2166] | 1.0258 [0.9194, 1.1504] |
| extinct worlds (extra) | 2.0000 | 3.0000 | -1.0000 [+nan, +nan] | -1.0000 [+nan, +nan] |
| child deaths per 1,000 child-years (ratio) | 7.9223 | 8.4709 | 0.9352 [0.8145, 1.0850] | 0.9467 [0.8082, 1.0905] |
| child starvation deaths per 1,000 child-years (ratio) | 4.2320 | 4.9303 | 0.8584 [0.7191, 1.0208] | 0.8637 [0.6907, 1.0640] |
| food gifts to kin's children per 1,000 adult-weeks (ratio) | 5.1096 | 4.7410 | 1.0778 [0.9595, 1.2099] | 1.0890 [0.9806, 1.2035] |

## The stage funnel per arm (MP1's stages; new kinds needing a made part)

| arm | kinds | A | B | C | D | E | made by a non-inventor |
|---|---|---|---|---|---|---|---|
| v16 | 3,224 | 0.8989 | 0.0580 | 0.0118 | 0.0155 | 0.0158 | 24 |
| VW (the law) | 3,480 | 0.8905 | 0.0601 | 0.0129 | 0.0201 | 0.0164 | 31 |
| sham | 3,676 | 0.8999 | 0.0634 | 0.0068 | 0.0150 | 0.0150 | 35 |

- Made again (stage E), VW − v16: +0.0006 [-0.0052, +0.0064].
- Made by a non-inventor, VW − v16: +0.0015 [-0.0025, +0.0053].

## By depth: co-primaries per arm

| depth | arm | kinds | any part held | all parts held |
|---|---|---|---|---|
| 1 | v16 | 387 | 0.3721 | 0.1550 |
| 1 | VW (the law) | 403 | 0.3474 | 0.1514 |
| 2 | v16 | 1,231 | 0.1048 | 0.0487 |
| 2 | VW (the law) | 1,327 | 0.1304 | 0.0625 |
| 3+ | v16 | 1,606 | 0.0330 | 0.0118 |
| 3+ | VW (the law) | 1,750 | 0.0389 | 0.0160 |

## Food-production displacement: the grown's weeks by action

| arm | forage | gather | make | rest | talk |
|---|---|---|---|---|---|
| v16 | 0.3966 | 0.2384 | 0.0014 | 0.0083 | 0.0983 |
| VW (the law) | 0.3941 | 0.2419 | 0.0014 | 0.0078 | 0.0944 |
| sham | 0.3940 | 0.2372 | 0.0016 | 0.0081 | 0.0972 |

## Make options offered: a part of a valued whole (one level) or only deeper

| arm | make options | a part one level down | only deeper |
|---|---|---|---|
| v16 | 12,385,106 | 0.2639 | 0.0017 |
| VW (the law) | 13,315,149 | 0.2910 | 0.0041 |
| sham | 12,845,814 | 0.2777 | 0.0015 |

