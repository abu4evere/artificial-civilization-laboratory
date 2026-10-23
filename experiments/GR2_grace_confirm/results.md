# GR2 — does first-season grace hold up, and is it safe for population? results

Frozen as `GR2-frozen`. run_gr2.py (GR1's code and runner), analyse_gr2.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present: **yes**
- One fingerprint (`code_g1`): **yes**
- Manipulation check: useful inventions still held by the inventor 13 weeks later, C median 0.551, G median 1.000; G − C +0.455 [+0.446, +0.463], Wilcoxon p 1.39e-85, 512 seeds: **passes**

**Valid.**

## Primary: transmission (share of useful inventions ever learned by someone else, CA1's link 3)

Seeds with useful inventions in both arms: 512 of 512. Medians: C 0.111, G 0.113.

| G − C, mean | 95% interval | Wilcoxon p | reading |
|---|---|---|---|
| +0.0007 | [-0.0025, +0.0040] | 0.8 | **no meaningful effect** |

## Survival check (G against C, paired by seed)

C died out in **170 of 512**; G in **179 of 512**.

| G saved / lost (discordant pairs) | sign-test p | effect (C − G) | 95% interval | reading |
|---|---|---|---|---|
| 56 / 65 | 0.467 | -0.018 | [-0.059, +0.025] | **no meaningful effect** |

## Population safety (frozen; margin −5%)

Time-averaged population, mean over seeds: C **24.61**, G **24.29**.

| relative difference (G / C − 1) | 95% interval | reading |
|---|---|---|
| -0.013 | [-0.055, +0.032] | **inconclusive** |

## The adoption rule (frozen)

**Not adopted** (transmission: no meaningful effect).

## Beside it (described; population first, rule 18)

| arm | median population, year 60 / 119 | died out | recipes held per person | weeks a useful invention stays with its inventor (mean) | built on by a learner | longest part chain (median) | children's useful inventions passed on |
|---|---|---|---|---|---|---|---|
| c | 22 / 22 | 170 | 8.78 | 662.6 | 5969 | 13 | 9146 of 129834 |
| g | 22 / 22 | 179 | 8.78 | 850.2 | 9224 | 14 | 9269 of 133775 |

| arm | deaths | illness | starvation | old age | thirst | other causes |
|---|---|---|---|---|---|---|
| c | 44917 | 15844 | 14946 | 7961 | 4477 | 1689 |
| g | 44518 | 15748 | 14622 | 7872 | 4563 | 1713 |

### After GPT's review: the cost, the fallback, and the pathway (described)

Full-memory drops, summed over worlds (per 100 person-years in brackets). In C every drop is v3's.
In G: "displaced" = grace protected a new recipe and an older one went instead; "same" = the one v3 would drop was already older; "fallback" = every held recipe was new, so v3's rule applied.

| arm | drops | displaced | same | fallback | dropped while valued > 0.15 | displaced while valued > 0.15 | displaced that were useful kinds |
|---|---|---|---|---|---|---|---|
| c | 376,009 (24.9) | 0 (0.0) | 0 (0.0) | 0 (0.0) | 0 (0.0) | 0 (0.0) | 0 (0.0) |
| g | 399,874 (26.7) | 334,289 (22.4) | 65,585 (4.4) | 0 (0.0) | 11,734 (0.8) | 11,689 (0.8) | 320,254 (21.4) |

The pathway for useful inventions (summed over worlds; each step counted on its own, not nested):

| arm | useful inventions | held at 13 weeks | made again by the inventor | valued > 0.15 by the inventor | offered in a lesson | learned by someone else |
|---|---|---|---|---|---|---|
| c | 173,699 | 94,635 (54.5%) | 8,951 (5.2%) | 33,536 (19.3%) | 35,316 (20.3%) | 20,392 (11.7%) |
| g | 180,462 | 179,612 (99.5%) | 10,382 (5.8%) | 79,064 (43.8%) | 58,826 (32.6%) | 21,053 (11.7%) |
