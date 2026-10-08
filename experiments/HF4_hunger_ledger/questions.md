# HF4 — The hunger ledger: did small shifts push adults over the starvation line? (read-only; SIGNED OFF, questions frozen as `HF4-questions` before any data)

**Signed off by the creator (October 2026):** the decision rule as drafted (r ≥ 0.9; shifted prediction within ±25%; the tail alternative), holdout on new seeds 1601–1616, first 40 years, and **after HF4, whatever it finds, the HB1 question is closed** and the project returns to keeping couples together with a different design. Nothing has been run.

**Asked by the creator (October 2026), after HF3.** No fixes, no tuning, no change to how the world works. Nothing has
been run.

## Why

HB1 (a shared home base) raised adult starvation about 1.6–1.8× on every set of worlds measured. Three read-only checks,
each with a frozen rule and a holdout on new seeds, found no single cause: not food on the land (HF1), not children or
meat (HF2), not lost gifts (HF3). What they agree on is a set of small shifts: food in per adult about 4% lower, adults
holding a surplus about 18% fewer, gifts about 40% fewer, foraging near home about 8% poorer. In ACL an adult's week counts
as starving when they fall more than 5% short of need. **Hypothesis (HF3, not a finding):** many adults sit near that
line, and small shifts together tipped many over it. HF4 tests it.

## The measurement problem, and its solution (precedent: W1, S1, D2)

The moment that matters is **eating**, inside the week's body phase (`biology.body_phase`): carers first feed their
dependants, then each person eats from what they hold; a shortfall above 5% of need is a starving week. A weekly observer
sees only the world after this. HF4 therefore uses an **instrumented logging copy** of HB1's code (`code_hb1`) that, at
the moment of eating, writes to a log outside the world's state, for each person: their need (after any fire saving),
the food they held just before eating, their shortfall, and, for carers, what they gave their dependants just before.
The copy changes nothing else. **Hard stop:** with the log on, the world's state hash after 20 years must equal the
uninstrumented copy's, in both arms, on two seeds; otherwise HF4 stops.

## Questions

First 40 years, arms H (HB1, `home_base = 1`) and C (the same code, settings off), adult-weeks (16+), measured at the
moment of eating.

1. **Coverage:** food held just before eating ÷ need. Distribution in bands (< 0.5, 0.5–0.95, 0.95–1.05, 1.05–1.5,
   1.5–3, ≥ 3) and median, H against C. A starving week is coverage below 0.95.
2. **How many sit near the line:** share of adult-weeks with coverage in 0.95–1.5 in C (the adults a small shift could
   tip over).
3. **Where H's extra starving weeks are:** of H's starving adult-weeks, the share that are deep (coverage < 0.5) and
   shallow (0.5–0.95), against C's.
4. **What moved coverage (descriptive):** for carers, food given to dependants just before eating, as a share of what
   they held; for all adults, food held at the start of the body phase.

## Decision rule (frozen; read on discovery and holdout separately)

Let **r** be H's median coverage ÷ C's, and let the **shifted prediction** be the starving share C would have if every C
adult-week's coverage were multiplied by r.

| | supported if, in **both** sets |
|---|---|
| **Small shifts explain the hunger** | r ≥ 0.9 (the shift is small) **and** the shifted prediction is within ±25% of H's actual starving share |
| **A tail, not a shift** | the shifted prediction falls short of H's actual starving share by more than 25%, **and** H's extra starving weeks are mostly deep (H's share of starving weeks with coverage < 0.5 exceeds C's) |
| **Otherwise** | **mixed**; reported as such, the creator decides |

## Worlds

| set | seeds | runs |
|---|---|---|
| **Discovery** | 501–516 | H and C, 40 years |
| **Holdout** | **1601–1616, new** (HF1–HF3 used 1301–1316, 1401–1416 and 1501–1516; the hypothesis came from all of them) | H and C, 40 years |

## Hard stops

- **The log changes nothing:** state hash equal with and without the instrumentation (both arms, two seeds, 20 years).
- **Replays reproduce:** on discovery, H matches HB1's saved populations and C matches F1's (years 10–40).
- **Code unchanged** during runs (fingerprint of the instrumented copy).

## Priors (written before any run; not predictions to test)

- **Assistant:** small shifts supported. Held very loosely: the last three priors were wrong (HF1, HF2, HF3).

## Decisions (taken by the creator at sign-off)

1. **The decision rule:** r ≥ 0.9; shifted prediction within ±25%; the "tail" alternative.
2. **Holdout on new seeds 1601–1616.**
3. **First 40 years** (as HF1–HF3).
4. **After HF4, whatever it finds:** close the HB1 question (proposed), recording what HF1–HF4 established, and return to
   keeping couples together with a different design.
