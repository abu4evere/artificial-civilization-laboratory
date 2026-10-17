# HS1 — Why are everyone's habits alike? Same world, or same nature? Results

Frozen as `HS1-frozen`. `code_tc1`, control world; arms N (no copying, primary) and W (today); seeds 501–616 (32); 80 years.

## Validity

- Zero check (observer leaves the world unchanged, both arms): **yes**
- All 64 replays present: **yes**
- Worlds with children reaching 20 and an other-world stranger: W 32, N 32 (need 16 each)

**Valid.**

## Population first (rule 18)

| arm | children reaching 20 (all worlds) | per world, median | worlds alive at the end |
|---|---|---|---|
| N | 1182 | 31 | 25 of 32 |
| W | 1197 | 38 | 26 of 32 |

## Sameness: a child at 20 against parents, a stranger of the same world, and a stranger of another world

| arm | r with parents | r with same-world stranger | r with other-world stranger | nature share (r_other ÷ r_same) | world share | Wilcoxon r_same vs r_other |
|---|---|---|---|---|---|---|
| N | 0.923 [0.903, 0.929] | 0.839 [0.797, 0.869] | 0.838 [0.820, 0.861] | 0.998 [0.982, 1.016] | 0.002 [-0.016, 0.018] | 0.747 |
| W | 0.938 [0.925, 0.948] | 0.872 [0.850, 0.884] | 0.880 [0.850, 0.888] | 1.005 [0.988, 1.026] | -0.005 [-0.026, 0.012] | 0.443 |

**Frozen reading (N, no copying): Mostly nature: a stranger from another world is nearly as like a child as a stranger from their own.**

Medians over worlds of per-world means, with 95% bootstrap intervals (10,000 resamples, `random.Random(2026)`). W is described beside N; no reading is made for W.
