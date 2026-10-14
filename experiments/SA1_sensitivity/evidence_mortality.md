# SA1 follow-up: is ACL's ageing anchored? Evidence note (14 October 2026; read-only; for the creator)

SA1 found `mortality_base` sensitive (× 2: 34 of 64 worlds died out against 22). Of the three sensitive settings it is
the one with a direct evidence anchor, so it was checked first (rule 17). **Nothing in nature is changed by this note.**

## Source (read in full text)

Gurven, M. & Kaplan, H. (2007). Longevity among hunter-gatherers: a cross-cultural examination. *Population and
Development Review* 33(2): 321–365. PDF from the first author's page; Table 2 (Siler model fits, per year of age).

The Siler hazard is h(x) = a1·exp(−b1·x) + a2 + a3·exp(b3·x): juvenile, age-independent, and senescent (Gompertz)
parts. The paper's summary: "The adult mortality rate doubles every 7–10 years"; hazard "doubled to about 0.02 by age
40, doubled yet again before age 60, and again by age 70."

## ACL against it

ACL's only age-dependent death is "illness" / "old age": weekly risk = `mortality_base` × exp(`mortality_rate` × age),
with 1.5 × 10⁻⁵ and 0.0866, so about **7.8 × 10⁻⁴ per year** at age 0. Other deaths (starvation, thirst, cold,
animals, violence, drowning) arise from the world and play the part of the age-independent term a2.

| | a3 (per year) | b3 | doubling time |
|---|---|---|---|
| Average hunter-gatherer (Hadza, Ache, Hiwi, !Kung, Agta) | 1.47 × 10⁻⁴ | 0.086 | 8.1 years |
| **ACL** | **7.8 × 10⁻⁴** | **0.0866** | **8.0 years** |

Senescent hazard per year (computed from Table 2; `python` one-liner, reproduced in the commit message):

| age | Hadza | Ache | !Kung | average HG | **ACL** | ACL ÷ average |
|---|---|---|---|---|---|---|
| 20 | 0.0001 | 0.0004 | 0.0015 | 0.0008 | **0.0044** | 5.4 |
| 40 | 0.0010 | 0.0030 | 0.0072 | 0.0046 | **0.0249** | 5.4 |
| 60 | 0.0121 | 0.0232 | 0.0336 | 0.0256 | **0.1408** | 5.5 |
| 70 | 0.0423 | 0.0649 | 0.0726 | 0.0605 | **0.3348** | 5.5 |

Foragers' **total** adult hazard (a2 + senescent) on average: 0.018 at 40, 0.039 at 60.

## Reading

1. **The rate is anchored; the scale is not.** ACL's doubling time (8.0 years) equals the forager average (8.1). Its
   scale is **5.4 times** the average, the same as making every ACL person **about 19 years older** than a forager of the
   same age.
2. **ACL's illness alone exceeds foragers' total adult mortality.** At 40, ACL's illness risk (0.025 a year) is above
   foragers' risk from all causes together (0.018); at 60, 3.6 times it (0.14 against 0.039). Only the Agta (data the
   authors call questionable) come near. And every other cause of death in ACL comes on top.
3. **This bears on survival directly.** SA1's × 2 arm (about 8 years older) raised extinction strongly. Today's value
   already sits about 19 years "older" than the forager anchor, so part of ACL's extinction may be people dying of age
   too young: fewer reproductive years per woman, more orphans.

**Caveats.** a3 and b3 trade off in fitting, so a3 alone is not compared; the hazards at each age above are the fair
comparison. ACL's age-independent deaths have not yet been measured against a2 (about 0.013 a year on average): a
read-only count from saved worlds can do it, and should come before any change, because the total is what matters.

## What it would lead to (the creator decides; nothing started)

- **Measure first (read-only):** ACL's adult deaths by cause and age per person-year, against the Siler total.
- **Then, if the total is also too high:** anchor `mortality_base` to the forager average (weekly 1.47 × 10⁻⁴ ÷ 52 ≈
  2.8 × 10⁻⁶), a change to nature, so a candidate for nature v2 beside last-seen memory and A1, with zero checks and a
  comparison on fresh seeds. Every past result stays on `nature-v1`.
