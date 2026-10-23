# G1 — a first season of grace: results

Frozen as `G1-frozen`. run_g1.py, analyse_g1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present: **yes**
- One fingerprint (`code_g1`): **yes**
- Manipulation check: useful inventions still held by the inventor 13 weeks later, C median 0.539, G median 1.000; G − C +0.464 [+0.452, +0.476], Wilcoxon p 9.64e-44, 256 seeds: **passes**

**Valid.**

## Primary: transmission (share of useful inventions ever learned by someone else, CA1's link 3)

Seeds with useful inventions in both arms: 256 of 256. Medians: C 0.110, G 0.113.

| G − C, mean | 95% interval | Wilcoxon p | reading |
|---|---|---|---|
| +0.0043 | [-0.0000, +0.0085] | 0.0366 | **changes transmission (G higher)** |

## Survival check (G against C, paired by seed)

C died out in **99 of 256**; G in **98 of 256**.

| G saved / lost (discordant pairs) | sign-test p | effect (C − G) | 95% interval | reading |
|---|---|---|---|---|
| 35 / 34 | 1 | +0.004 | [-0.059, +0.070] | **no meaningful effect** |

## The adoption rule (frozen)

**G may be proposed for adoption into nature (v4)**; the creator decides whether to accept the evidence.

## Beside it (described; population first, rule 18)

| arm | median population, year 60 / 119 | died out | recipes held per person | weeks a useful invention stays with its inventor (mean) | built on by a learner | longest part chain (median) | children's useful inventions passed on |
|---|---|---|---|---|---|---|---|
| c | 22 / 18 | 99 | 8.78 | 660.3 | 2941 | 13 | 4086 of 62776 |
| g | 20 / 16 | 98 | 8.80 | 817.1 | 4559 | 15 | 4394 of 64970 |

| arm | deaths | illness | starvation | old age | thirst | other causes |
|---|---|---|---|---|---|---|
| c | 21402 | 7633 | 6895 | 3809 | 2269 | 796 |
| g | 20865 | 7339 | 6779 | 3754 | 2189 | 804 |

### After GPT's review: the cost, the fallback, and the pathway (described)

Full-memory drops, summed over worlds (per 100 person-years in brackets). In C every drop is v3's.
In G: "displaced" = grace protected a new recipe and an older one went instead; "same" = the one v3 would drop was already older; "fallback" = every held recipe was new, so v3's rule applied.

| arm | drops | displaced | same | fallback | dropped while valued > 0.15 | displaced while valued > 0.15 | displaced that were useful kinds |
|---|---|---|---|---|---|---|---|
| c | 178,056 (25.1) | 0 (0.0) | 0 (0.0) | 0 (0.0) | 0 (0.0) | 0 (0.0) | 0 (0.0) |
| g | 194,026 (28.3) | 162,538 (23.7) | 31,488 (4.6) | 0 (0.0) | 6,195 (0.9) | 6,160 (0.9) | 156,156 (22.8) |

The pathway for useful inventions (summed over worlds; each step counted on its own, not nested):

| arm | useful inventions | held at 13 weeks | made again by the inventor | valued > 0.15 by the inventor | offered in a lesson | learned by someone else |
|---|---|---|---|---|---|---|
| c | 84,501 | 45,357 (53.7%) | 4,485 (5.3%) | 16,067 (19.0%) | 16,791 (19.9%) | 9,608 (11.4%) |
| g | 88,420 | 87,982 (99.5%) | 5,260 (5.9%) | 38,696 (43.8%) | 28,473 (32.2%) | 10,343 (11.7%) |
