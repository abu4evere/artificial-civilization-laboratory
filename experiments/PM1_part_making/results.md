# PM1: why are the parts of new kinds never made again? (results)

Frozen as `PM1-frozen`. run_pm1.py, analyse_pm1.py (written before data).

## Validity

- Zero checks (All: PASS, `code_v16` fingerprint): **yes**
- All worlds present (32): **yes**
- One fingerprint, `code_v16`'s: **yes**
- In every world: decisions looked at 45,071,900; make option predicted wrongly 0; event checks failed 0: **yes**

**Valid.**

## Primary: the furthest part-making stage (3,929 new kinds with made parts)

| stage | | kinds | share [95%] |
|---|---|---|---|
| P0a | the part's recipe known by no one living | 398 | 0.1013 [0.0850, 0.1180] |
| P0b | the part's recipe unknown to the knower (others know it) | 102 | 0.0260 [0.0203, 0.0323] |
| P1 | known, never the inputs in hand | 2,788 | 0.7096 [0.6879, 0.7289] |
| P2 | inputs in hand, never valued enough | 184 | 0.0468 [0.0408, 0.0531] |
| P3 | eligible, never the make option offered | 38 | 0.0097 [0.0071, 0.0122] |
| P4 | offered, never chosen | 199 | 0.0506 [0.0438, 0.0579] |
| P5 | chosen, never made | 0 | 0.0000 [0.0000, 0.0000] |
| P6 | made, never all parts held at once | 103 | 0.0262 [0.0216, 0.0309] |
| P7 | all parts held at once | 117 | 0.0298 [0.0221, 0.0385] |

**Reading (frozen): most kinds stop at P1 (known, never the inputs in hand), clear** (P1 0.7096 [0.6879, 0.7289] against the next, P0a, 0.1013 [0.0850, 0.1180]).

Rule: the largest share among P0-P6 (P0a and P0b counted apart); 'clear' if its lower bound is above the next largest's upper bound.

## By depth

| depth | kinds | P0a | P0b | P1 | P2 | P3 | P4 | P5 | P6 | P7 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 447 | 0.107 | 0.056 | 0.318 | 0.221 | 0.027 | 0.094 | 0.000 | 0.089 | 0.087 |
| 2 | 1,450 | 0.105 | 0.029 | 0.650 | 0.051 | 0.016 | 0.085 | 0.000 | 0.027 | 0.037 |
| 3+ | 2,032 | 0.097 | 0.017 | 0.838 | 0.005 | 0.001 | 0.017 | 0.000 | 0.012 | 0.012 |

## The whole's value (was the kind itself ever valued by its inventor in the 5 years?)

- Valued: 3,359; never valued: 570 (share never valued 0.1451).

| | P0a | P0b | P1 | P2 | P3 | P4 | P5 | P6 | P7 |
|---|---|---|---|---|---|---|---|---|---|
| valued (3,359) | 0.008 | 0.030 | 0.783 | 0.049 | 0.011 | 0.058 | 0.000 | 0.030 | 0.032 |
| never valued (570) | 0.653 | 0.004 | 0.275 | 0.037 | 0.000 | 0.009 | 0.000 | 0.005 | 0.018 |

## Within P3: why making the part was not the option offered (looks, in P3 kinds)

- other_won 1,905 (0.974), floor 51 (0.026)

## When another recipe won the make slot, it was (looks, all kinds)

- an old recipe 9,658 (0.908), another part of the kind 951 (0.089), another new kind 28 (0.003)

## When making the part was offered but not chosen, the choice was (looks)

- forage 11,013 (0.498), talk 5,052 (0.229), give 2,881 (0.130), gather 1,236 (0.056), rest 826 (0.037), put 463 (0.021), play 359 (0.016), join 235 (0.011), explore 22 (0.001), care 5 (0.000), court 3 (0.000), take 1 (0.000)

