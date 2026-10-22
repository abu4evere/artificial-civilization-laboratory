# CT2 — A confirmatory test of K2 (loneliness in courting) (DRAFT for the creator; nothing built or run)

**Why.** In CT1's exploratory reading (Amendment 2), K2 was the only candidate leaning toward saving worlds: 70 against
83 of 256 died out, effect +0.051, [−0.016, +0.117], unresolved. It barely acted on courting, though: +0.003 attempts per
single adult-year, p = 0.04. CT1 was not valid as committed, so no candidate can enter nature on it. CT2 would test K2
properly, on its own, with a fresh plan.

## Design (proposed)

- **Code:** `code_ct1` unchanged, which is already built and zero-checked. Arms **C** (v3) and **K2**
  (`lonely_courting` 1) only; no K12, so there is only one manipulation check.
- **Seeds:** **512 new**, 8601–9112. 1,024 worlds on GitHub (about the same as LX1).
- **Manipulation check (hard stop, K2 only):** courting attempts per single adult-year rise against C (paired
  Wilcoxon, p < 0.05, mean > 0).
- **Primary:** extinction, K2 against C, paired: sign test, bootstrap interval, yardstick ±0.117, the usual three
  readings.
- **Harms:** as CT1 (infant deaths per birth and adult starvation are the serious ones), with absolute changes and
  intervals.
- **Adoption rule:** as CT1's. K2 may be **proposed** only if the check passes, survival is not worse, and no serious
  harm rises. The creator then judges whether the evidence is enough, which is CT1's weak point: no source shows that
  loneliness raises courting specifically.

## The assistant's prior

K2 reads "no meaningful effect". CT1's lean was chance; K2 moves courting too little to matter.

## Decisions for the creator

1. Run CT2 (512 seeds), choose CB1 first (read-only and cheaper), or neither.
2. Whether K2's evidence could ever be enough for nature, even if CT2 passes. If not, CT2 is not worth running.
