# LX1 — Does parts-first teaching cost survival? The check before adopting it (SIGNED OFF 21 October 2026; frozen as `LX1-frozen` before any code or data)

**Why.** LM1 (`../LM1_memory_and_parts/findings.md`, `LM1-done`): showing a missing part after a failed lesson (L1,
`parts_first`) raised the share of useful inventions passed on by 2.2 points, the first change to move CA1's
bottleneck. But extinction was described, not tested, and L lost more worlds than C (93 against 79 of 256). The
decision of 21 October 2026 (`../../docs/decision_2026-10-21_LM1_FX.md`, the creator delegating to GPT's review): adopt
L1 into nature only after a frozen check that it does not cost survival. **A Law 126 check; nothing is adopted by it.**

## Question

Does L1 change extinction against today's nature, on new worlds?

## Design (the assistant's recommendation; decisions marked)

- **Code:** `code_lm1` exactly as frozen (`LM1-frozen`); arms **C** (`parts_first` 0) and **L** (`parts_first` 1).
  No new code.
- **Seeds (Decision 1):** **512 new, 7601–8112** (used by no study), 20 founders, 40 × 40, 120 years; 1,024 worlds.
  512 rather than 256 because extinction is noisy and the question is a safety check (intervals about ±0.05 instead of
  ±0.07).
- **Where:** GitHub's machines (`cloud-run`), zero checks there first; results fetched and analysed here.
- **Primary (survival):** extinction, L against C, paired by seed: exact sign test; effect = C's extinction share − L's,
  95% bootstrap (10,000 resamples, `random.Random(2026)`); yardstick ±0.117. Readings as every study: "changes survival"
  (p < 0.05; with a size label, beyond or within the yardstick), "no meaningful effect" (p ≥ 0.05 and the interval
  inside ±0.117), otherwise "unresolved".
- **Secondary (replication of LM1):** share of useful inventions passed on (CA1's link 3), L against C, Wilcoxon,
  bootstrap interval of the mean difference.
- **Described:** median population at years 60 and 119; births; partner blocking; causes of death.

## The adoption rule (fixed now, before any data)

- **Adopt L1 into nature (v3)** if survival reads "no meaningful effect", or "changes survival" with L dying out
  **less**, **and** the replication shows L raising transmission (p < 0.05).
- **Do not adopt** if survival reads "changes survival" with L dying out **more** (whatever its size), or if the
  replication fails.
- **Unresolved survival:** do not adopt now; report, and the creator decides whether to run more seeds.

## The assistant's prior (to be frozen at sign-off; held loosely)

Survival: **no meaningful effect** (LM1's 93 against 79 was within chance for one comparison among several). The
replication holds (L raises transmission by about 2 points). So L1 would be adopted.

## Decisions for the creator

1. Seeds: **512 new, 7601–8112** (recommended), or 256 (7601–7856; less precise).
2. The adoption rule above, fixed as written.
3. The prior, frozen as written.

## Sign-off (21 October 2026)

The creator: "approve all recommendations, freeze both". All recommended options and the prior stand as written.
