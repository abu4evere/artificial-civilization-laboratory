# PB2: the episodic brain helps choose, in a copy of nature (results)

Frozen as `PB2-frozen`. run_pb2.py, analyse_pb2.py (written before data). Adults 16–49, years 130–170.

## Validity

- Zero checks (All: PASS, same `code_pb2` fingerprint): **yes**
- All worlds present (160 of 160): **yes**
- One fingerprint, `code_pb2`'s: **yes**

**Valid.**

## Guards (each brain arm against v13)

- P (steering): living-weeks ratio 1.283 [1.236, 1.335]; extinct worlds beyond v13's +0 — no guard raised
- G (LP goal): living-weeks ratio 1.263 [1.211, 1.320]; extinct worlds beyond v13's +0 — no guard raised
- G0 (random goal): living-weeks ratio 1.295 [1.246, 1.350]; extinct worlds beyond v13's +0 — no guard raised
- sham: living-weeks ratio 0.957 [0.848, 1.081]; extinct worlds beyond v13's +0 — no guard raised

Rule: a guard is raised if the living-weeks ratio is below 0.90 with its upper bound below 1, or 3+ extra extinct worlds. An arm with a guard raised is not read as a success.

## The validity check (arm c: a read-only memory scores r-hat against the habit's q as predictors of r)

- Weeks scored (own r-hat available): 12,451,910
- Mean squared error: r-hat 0.0027, q 0.8021; q − r-hat: +0.7995 [+0.7759, +0.8215]
- Described: correlation with r: r-hat 0.9019, q 0.5877; difference +0.3141 [+0.3052, +0.3241]

**r-hat predicts r better than q: yes.**

## Primary: M3, ends-directed chains

P(made a recipe using m within 8 weeks | gathered m, a needed input of a valued recipe, holding < 1) − P(made | an opportunity-matched week).

| arm | M3 | gather chains | matched chains |
|---|---|---|---|
| v13 (shadow) | 0.0034 | 299,407 | 2,781,678 |
| P (steering) | 0.0210 | 270,255 | 3,842,688 |
| G (LP goal) | 0.0203 | 254,578 | 3,779,164 |
| G0 (random goal) | 0.0200 | 273,938 | 3,921,003 |
| sham | 0.0035 | 275,192 | 2,671,689 |

| contrast | difference [95%] |
|---|---|
| G (LP goal) − P (steering) (primary) | -0.0007 [-0.0020, +0.0005] |
| G (LP goal) − G0 (random goal) (primary) | +0.0002 [-0.0009, +0.0013] |
| P (steering) − v13 (shadow) (the steering effect) | +0.0176 [+0.0157, +0.0194] |
| G (LP goal) − v13 (shadow) | +0.0169 [+0.0151, +0.0185] |
| G0 (random goal) − v13 (shadow) | +0.0166 [+0.0146, +0.0187] |
| sham − v13 (shadow) | +0.0000 [-0.0004, +0.0005] |

Rule: "a self-chosen goal helps people finish what they start" if both G − P and G − G0 lie wholly above 0 (guards first; the validity check must pass). P − c is the steering effect (it mixes a better predictor with no look-ahead; questions.md, the known limit).

**M3 reading: not shown: G − P and G − G0 do not both lie wholly above 0.**

## Co-primary: R, lineage remaking

The share of world-new kinds first made in years 130–165 whose own recipe is made again (a `make` action) within 5 years.

| arm | R | kinds | remade | remade by the inventor |
|---|---|---|---|---|
| v13 (shadow) | 0.0000 | 1,192 | 0 | 0 |
| P (steering) | 0.0023 | 2,214 | 5 | 5 |
| G (LP goal) | 0.0005 | 2,161 | 1 | 1 |
| G0 (random goal) | 0.0009 | 2,299 | 2 | 2 |
| sham | 0.0015 | 1,294 | 2 | 2 |

| contrast | difference [95%] |
|---|---|
| G (LP goal) − P (steering) | -0.0018 [-0.0035, -0.0004] |
| G (LP goal) − G0 (random goal) | -0.0004 [-0.0021, +0.0010] |
| P (steering) − v13 (shadow) | +0.0023 [+0.0005, +0.0041] |
| G (LP goal) − v13 (shadow) | +0.0005 [+0.0000, +0.0015] |
| G0 (random goal) − v13 (shadow) | +0.0009 [+0.0000, +0.0023] |
| sham − v13 (shadow) | +0.0015 [+0.0000, +0.0038] |

**Intent test 1 (above chance):** remakes per adult week holding the kind's inputs, the inventor against non-inventors who held them (all; and those who also knew the recipe, described).

| arm | inventor | others | inventor − others [95%] | others who knew it | inventor − those [95%] |
|---|---|---|---|---|---|
| v13 (shadow) | 0.00000 | 0.00000 | +0.0000 [+0.0000, +0.0000] | nan | +nan [+nan, +nan] |
| P (steering) | 0.00802 | 0.00000 | +0.0080 [+0.0024, +0.0181] | nan | +nan [+nan, +nan] |
| G (LP goal) | 0.00474 | 0.00000 | +0.0047 [+0.0000, +0.0121] | nan | +nan [+nan, +nan] |
| G0 (random goal) | 0.00238 | 0.00000 | +0.0024 [+0.0000, +0.0101] | nan | +nan [+nan, +nan] |
| sham | 0.05263 | 0.00000 | +0.0526 [+0.0351, +0.0877] | nan | +nan [+nan, +nan] |

(holding-weeks: inventors 1,998, others 61,600, all arms together)

**Intent test 2 (preparation):** the share of remakes preceded within 8 weeks by the maker gathering one of the recipe's materials.

| arm | prepared | remakes |
|---|---|---|
| v13 (shadow) | nan | 0 |
| P (steering) | 0.8333 | 6 |
| G (LP goal) | 1.0000 | 1 |
| G0 (random goal) | 0.0000 | 2 |
| sham | 0.6667 | 3 |

| contrast | difference [95%] |
|---|---|
| G (LP goal) − P (steering) | +0.1667 [+0.0000, +0.5000] |
| G (LP goal) − G0 (random goal) | +1.0000 [+1.0000, +1.0000] |
| P (steering) − v13 (shadow) | +nan [+nan, +nan] |
| G (LP goal) − v13 (shadow) | +nan [+nan, +nan] |
| G0 (random goal) − v13 (shadow) | +nan [+nan, +nan] |
| sham − v13 (shadow) | +nan [+nan, +nan] |

**Intent test 3 (persistence): M5**, chains whose next decision was a food action.

| arm | M5 | gather chains | matched chains |
|---|---|---|---|
| v13 (shadow) | 0.0036 | 117,233 | 1,060,867 |
| P (steering) | 0.0209 | 110,910 | 1,547,648 |
| G (LP goal) | 0.0205 | 104,662 | 1,526,065 |
| G0 (random goal) | 0.0197 | 112,002 | 1,588,375 |
| sham | 0.0036 | 108,432 | 1,021,197 |

| contrast | difference [95%] |
|---|---|
| G (LP goal) − P (steering) | -0.0005 [-0.0019, +0.0010] |
| G (LP goal) − G0 (random goal) | +0.0008 [-0.0008, +0.0022] |
| P (steering) − v13 (shadow) | +0.0174 [+0.0155, +0.0191] |
| G (LP goal) − v13 (shadow) | +0.0169 [+0.0151, +0.0185] |
| G0 (random goal) − v13 (shadow) | +0.0161 [+0.0141, +0.0181] |
| sham − v13 (shadow) | +0.0001 [-0.0007, +0.0008] |

"M3 up, R null" is a real finding, not a failure (questions.md).

## Described (no frozen prediction)

**Action shares (adults, years 130–170; PB0's warning: a shift to social acts).**

| action | v13 (shadow) | P (steering) | G (LP goal) | G0 (random goal) | sham |
|---|---|---|---|---|---|
| attack | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| care | 0.0027 | 0.0161 | 0.0158 | 0.0158 | 0.0027 |
| court | 0.0013 | 0.0044 | 0.0042 | 0.0043 | 0.0013 |
| explore | 0.0013 | 0.0032 | 0.0030 | 0.0029 | 0.0014 |
| flee | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| forage | 0.3940 | 0.4098 | 0.4105 | 0.4115 | 0.3954 |
| gather | 0.2362 | 0.1889 | 0.1833 | 0.1832 | 0.2282 |
| give | 0.0808 | 0.0957 | 0.0984 | 0.0982 | 0.0857 |
| heat | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| hunt | 0.0001 | 0.0001 | 0.0001 | 0.0001 | 0.0001 |
| join | 0.0623 | 0.0590 | 0.0599 | 0.0597 | 0.0644 |
| make | 0.0012 | 0.0049 | 0.0048 | 0.0048 | 0.0013 |
| play | 0.0012 | 0.0034 | 0.0033 | 0.0033 | 0.0013 |
| put | 0.1131 | 0.0868 | 0.0841 | 0.0855 | 0.1099 |
| rest | 0.0070 | 0.0115 | 0.0110 | 0.0114 | 0.0072 |
| steal | 0.0002 | 0.0004 | 0.0004 | 0.0004 | 0.0001 |
| take | 0.0001 | 0.0001 | 0.0001 | 0.0001 | 0.0002 |
| talk | 0.0987 | 0.1155 | 0.1212 | 0.1188 | 0.1008 |

Share of acts aimed at a person (give, care, talk, court, steal, attack): v13 (shadow) 0.1836; P (steering) 0.2322; G (LP goal) 0.2399; G0 (random goal) 0.2374; sham 0.1906. P (steering) − v13 +0.0486 [+0.0434, +0.0532]; G (LP goal) − v13 +0.0563 [+0.0515, +0.0610]; G0 (random goal) − v13 +0.0538 [+0.0502, +0.0576]; sham − v13 +0.0070 [-0.0052, +0.0194].

| measure | v13 (shadow) | P (steering) | G (LP goal) | G0 (random goal) | sham | P − v13 [95%] | G − v13 [95%] |
|---|---|---|---|---|---|---|---|
| M2 (bits beyond shuffle, per adult-year) | 0.1620 | 0.1236 | 0.1261 | 0.1243 | 0.1604 | -0.0383 [-0.0436, -0.0330] | -0.0358 [-0.0409, -0.0306] |
| M3 among people born after year 100: gather chains made | 0.0035 | 0.0212 | 0.0203 | 0.0204 | 0.0036 | +0.0177 [+0.0158, +0.0195] | +0.0168 [+0.0151, +0.0183] |
|   matched chains made (born after year 100) | 0.0003 | 0.0011 | 0.0010 | 0.0010 | 0.0003 | +0.0009 [+0.0008, +0.0010] | +0.0007 [+0.0006, +0.0008] |
| makes per adult-year | 0.0611 | 0.2535 | 0.2517 | 0.2521 | 0.0664 | +0.1924 [+0.1768, +0.2080] | +0.1906 [+0.1726, +0.2070] |
| world-new kinds per world (years 130–165) | 37.2500 | 69.1875 | 67.5312 | 71.8438 | 40.4375 | +31.9375 [+23.7180, +40.3750] | +30.2812 [+22.0625, +39.1250] |
| edible food per adult (year-end census) | 8.7095 | 8.4230 | 8.3840 | 8.2668 | 8.6923 | -0.2864 [-0.6507, +0.0842] | -0.3255 [-0.6617, -0.0044] |
| goal weeks per adult week | 0.0000 | 0.0000 | 0.4747 | 0.4662 | 0.0000 | +0.0000 [+0.0000, +0.0000] | +0.4747 [+0.4739, +0.4755] |
| decisions falling back to q (share) | 0.0081 | 0.0087 | 0.0086 | 0.0086 | nan | +0.0006 [+0.0004, +0.0007] | +0.0005 [+0.0004, +0.0006] |
| adult weeks of people born after year 100 (share) | 0.8681 | 0.8971 | 0.8958 | 0.8979 | 0.8698 | +0.0290 [+0.0238, +0.0347] | +0.0277 [+0.0216, +0.0338] |

**Goals in G (LP goal):** 153,805 adoptions.

| output | direction | adoptions | mean LP at adoption | finished goals | mean weeks held |
|---|---|---|---|---|---|
| food gained | + | 5,784 | 0.1221 | 5,584 | 25.5 |
| food gained | − | 27 | 0.1091 | 26 | 26.0 |
| net food | + | 7,588 | 0.1420 | 7,371 | 25.2 |
| net food | − | 290 | 0.1433 | 283 | 25.5 |
| health | + | 44,683 | 0.3975 | 43,386 | 27.9 |
| health | − | 167 | 0.4742 | 166 | 23.8 |
| energy | + | 6,657 | 0.1926 | 6,530 | 24.8 |
| energy | − | 11,171 | 0.1994 | 10,894 | 25.4 |
| materials held | + | 22,192 | 0.1750 | 21,772 | 23.3 |
| materials held | − | 377 | 0.1726 | 375 | 20.9 |
| things held | + | 21,905 | 0.3528 | 21,315 | 25.3 |
| things held | − | 9,073 | 0.3267 | 8,851 | 25.0 |
| affection | + | 22,006 | 0.2553 | 21,389 | 26.0 |
| affection | − | 1,885 | 0.3264 | 1,838 | 25.5 |

**Goals in G0 (random goal):** 160,132 adoptions.

| output | direction | adoptions | mean LP at adoption | finished goals | mean weeks held |
|---|---|---|---|---|---|
| food gained | + | 11,426 | 0.0064 | 11,128 | 24.7 |
| food gained | − | 11,473 | 0.0059 | 11,182 | 25.2 |
| net food | + | 11,502 | 0.0084 | 11,215 | 25.5 |
| net food | − | 11,521 | 0.0082 | 11,184 | 26.3 |
| health | + | 11,372 | 0.0168 | 11,102 | 26.1 |
| health | − | 11,401 | 0.0181 | 11,105 | 25.8 |
| energy | + | 11,311 | 0.0081 | 11,059 | 24.7 |
| energy | − | 11,301 | 0.0102 | 11,023 | 25.1 |
| materials held | + | 11,453 | 0.0075 | 11,191 | 23.3 |
| materials held | − | 11,385 | 0.0064 | 11,144 | 22.5 |
| things held | + | 11,311 | 0.0134 | 11,034 | 24.3 |
| things held | − | 11,720 | 0.0124 | 11,423 | 24.1 |
| affection | + | 11,444 | 0.0095 | 11,146 | 25.5 |
| affection | − | 11,512 | 0.0079 | 11,201 | 25.1 |

## Population (beside every measure)

| arm | living-weeks | adult-weeks (16–49) | extinct worlds |
|---|---|---|---|
| v13 (shadow) | 9,925,141 | 5,252,544 | 0 |
| P (steering) | 12,733,537 | 6,456,224 | 0 |
| G (LP goal) | 12,534,861 | 6,358,068 | 0 |
| G0 (random goal) | 12,852,786 | 6,549,871 | 0 |
| sham | 9,494,526 | 5,035,780 | 0 |

