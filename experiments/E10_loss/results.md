# E10 — The lesson of a lost child (O2) and of a death witnessed (O3) · Results

Arm 0 = E7 code; O2, O2+O3-low (witness 0.25), O2+O3-high (witness 0.50) = E10 code at weight 1.0. Seeds 301–304, 120 years. Frozen as `E10-frozen` before any code. Order: validity, leak test, causal links, deaths.

## 1. Validity

- Probe read-only (both codes): **yes**
- All runs finished: **yes**
- Zero-weight E10 code reproduces Arm 0 (seed 304): **yes**
- Arm 0 reproduces the saved E7 runs: **yes**
- Code unchanged during runs: **yes**
- **Valid.**

## 2. Leak test (hard fail)

Autumn foraging share of adults with no lesson: never bereaved (O2), and also never a witness (O2+O3 arms); compared with the same group in Arm 0.

- o2: 0.431 (n=10974) vs Arm 0 0.428 (n=11116) → ratio 1.007
- o3low: 0.428 (n=5534) vs Arm 0 0.428 (n=5796) → ratio 1.000
- o3high: 0.439 (n=5401) vs Arm 0 0.428 (n=5796) → ratio 1.027

**Leak test passed.**

## 3. Causal links

| arm | bereaved, first autumn after (forage share, n) | witnesses with children, first autumn after | median winter entry | child-winters with carer ≥ 20 food | adult-autumns reaching 80 | carriers made |
|---|---|---|---|---|---|---|
| arm0 | 0.491 (n=53) | 0.527 (n=314) | 11.8 | 37.7% | 0 of 11832 | 2038 |
| o2 | 0.590 (n=37) | 0.522 (n=228) | 11.4 | 37.3% | 6 of 11416 | 2038 |
| o3low | 0.590 (n=45) | 0.549 (n=216) | 11.8 | 37.7% | 7 of 10341 | 1907 |
| o3high | 0.577 (n=62) | 0.556 (n=214) | 11.8 | 39.0% | 14 of 10789 | 1794 |

## 4. Deaths (looked at last)

| arm | children's winter starvation per child-winter | child-winters | child starvation deaths, all seasons | all starvation deaths | population at 120 (seeds) |
|---|---|---|---|---|---|
| arm0 | 0.72% | 6909 | 81 | 195 | 40, 96, 50, 39 |
| o2 | 0.51% | 6530 | 50 | 164 | 44, 89, 55, 31 |
| o3low | 0.59% | 5775 | 65 | 157 | 85, 45, 3, 32 |
| o3high | 0.87% | 5892 | 81 | 162 | 64, 80, 1, 35 |

## 5. Frozen predictions, scored

1. **wrong** — bereaved carers' autumn foraging, O2 ÷ Arm 0: 1.20 (needs ≥ 1.3).
2. **wrong** — witnesses with children, O2+O3-high ÷ Arm 0: 1.06 (needs ≥ 1.2).
3. **confirmed** — dose response: witness ratio low 1.04 vs high 1.06; carers ≥ 20 low 37.7% vs high 39.0%.
4. **wrong** — carers with ≥ 20 food: O2+O3-high 39.0% vs Arm 0 37.7% (+1.3 points; needs ≥ +5).
5. **wrong** — children's winter starvation, O2+O3-high ÷ Arm 0: 1.20 (needs ≤ 0.80).
6. **wrong** — O2 alone, children's winter starvation ÷ Arm 0: 0.70 (predicted within 0.8–1.2).
7. **confirmed** — leak test (section 2).

## 6. Reading, per the binding order and the frozen decision table

- **The causal links barely moved.** Bereaved carers foraged more in the next autumn (1.20×, below the frozen 1.3);
  witnesses hardly at all (1.04–1.06). Food entering winter stayed about 12 in every arm, and carers holding 20+ food
  rose by at most 1.3 points.
- **So the differences in deaths cannot be credited to the mechanism.** Children's winter starvation was 0.51% (O2),
  0.59% (O2+O3-low) and 0.87% (O2+O3-high) against 0.72% in Arm 0: no consistent direction, and nothing upstream
  changed to explain it. Each code change gives each world a different history from the first week, and seed 303 nearly
  died out in both O3 arms. These are the ordinary differences between four diverging worlds. This is what the creator's
  analysis order was for: read first, O2's 30% fewer child deaths would have looked like a breakthrough.
- **Decision table, first row:** prediction 1 failed. Even losing a child, felt a season early at full strength, moves
  the bereaved only modestly and does not change how anyone enters winter. With E9, this closes the anticipation route
  in the forms tried: a lesson from one's own hunger (E9), from losing a child (O2) and from witnessing a death (O3) all
  leave the world's preparation for winter unchanged.
