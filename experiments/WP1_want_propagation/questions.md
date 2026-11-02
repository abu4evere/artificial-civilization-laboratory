# WP1 — Want propagation: can new inventions be made again? (frozen plan)

**A nature-change test in a copy (`code_wp1` = `code_v11` + `want_propagation`; 0 = v11 exactly), not an adoption.**
Live nature stays v11.
- **Adoption:** only by the full safe path in `CLAUDE.md`, and **the creator is asked first**, because the change
  alters how people come to want things.
- **Its origin:** UP1 found that new inventions are never remade, mainly because their made parts are not in hand. An
  exploratory check found that the missing part usually cannot be made either; its own inputs are missing.
- **Debate round 49** (`docs/debate_round49_want_propagation_2026-11-02.md`): GPT 95%, Gemini 94%.

## The law (one setting, `want_propagation`)
In v11, a valued thing gives each **missing made part** 0.8 of its value as a reason to **make** that part, one level
deep (`mind._wanted_parts`). The pull to **gather** a material counts only recipes valued by their own use
(`mind._material_wants`).

| setting | name | what changes |
|---|---|---|
| 0 | v11 | nothing |
| 1 | **A1**, the smallest repair | The gather pull counts a recipe's value as the larger of its own value and its one-level wanted-part value (the same value the make choice already uses). Making is unchanged. |
| 2 | **A2**, one general rule | **A valued thing's value flows to its inputs at 0.8 per step, through the whole chain.** |

**A2 in detail:**
- A made part not in hand gets the **maximum** over all things it goes into of 0.8 × that thing's value, own or
  propagated.
- That reaches parts of parts, step by step, until nothing changes. Values are never summed.
- The 0.8 per step means a loop can never amplify a value.
- Both making and gathering use the propagated value.

**Nothing else changes.** No invention is named, no outcome is rewarded, and no state is stored between weeks.

## Arms (32 paired seeds 22201–22232; LP: 80 founders, 80 × 80; 200 years; years 100–200 counted)
| arm | setting |
|---|---|
| **v11** | `want_propagation` 0 (= `code_v11`, shown by the zero checks) |
| **A1** | `want_propagation` 1 |
| **A2** | `want_propagation` 2 |
| **sham** | v11 with `sham_draw` 1 |

## Primary (frozen)
- **R:** the share of world-new kinds first made in play in years 100–195 that are **made again** (a `make` of that kind,
  by anyone) within 260 weeks. Each world's counts are pooled first.
- **Intervals:** a paired world bootstrap, 10,000 replicates, NumPy seed 20261105. The same drawn seeds are used for
  every arm.
- **The contrasts:** A1 − v11, A2 − v11, A2 − A1, sham − v11, A1 − sham, A2 − sham.

## Frozen reading rule (GPT's, round 49)
1. **Inconclusive (sham):** if the sham − v11 interval lies wholly outside ±0.01.
2. **Otherwise, for each of A1 and A2:** **"positive"** only if both hold:
   - arm − v11 and arm − sham **both** have intervals above 0;
   - **both** point differences are at least 0.01 (1 percentage point).

   Otherwise **"inconclusive"**, which is not evidence that propagation is useless.
3. **A2 − A1** reads "A2 adds" by the same two conditions, against A1.
4. **Guards** (each arm against v11; any raised guard is stated with the reading):
   - **population:** arm ÷ v11 below 0.90, with the upper bound below 1;
   - **extinctions:** 3 or more beyond v11's.

## Secondary (described, not decisive)
- **The chain:** gathers, makes and makes of nested kinds per adult-year.
- **Who remakes:** by the inventor or by someone else.
- **Invention:** world-new kinds per 100 adult-years; recipes per adult; nesting depth.
- **Timing:** the weeks to the first remake.

## Validity (hard stops)
- **Zero checks:**
  - `code_wp1` with 0 = `code_v11` (state and random numbers, 20 and 60 years);
  - A1, A2 and the sham each act;
  - the observer is read-only;
  - reload is exact (arm A2 saved at year 10 continues exactly to year 15).
- **All 4 × 32 worlds** are present under one `code_wp1` fingerprint.
- **A blind recompute by GPT and Gemini** of R per arm, the six contrasts with intervals, and the readings, from
  per-world sums.

## The assistant's prior
1. **A1 inconclusive:** inputs often sit two or more steps down the chain.
2. **A2 positive.**
3. **No guard raised.**

## Sign-off (2 November 2026)
The assistant, under the creator's sleep-mode autonomy (the creator last wrote at about 03:53). It is a nature-change
test in a copy, allowed with care under the 40% rule: GPT 95%, Gemini 94%, the assistant 60%. Frozen as `WP1-frozen`
before any code or data.
