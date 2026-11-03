# AF1 — Open what made things can do: can inventions be made again? (frozen plan)

**A nature-change test in a copy (`code_af1` = `code_v11` + `similar_parts` + `containers_carry`; both 0 = v11
exactly), not an adoption.** Live nature stays v11.
- **Adoption:** only by the full safe path in `CLAUDE.md`, and the creator is asked first.
- **Its origin:**
  - the creator (2 November 2026): "we should not script that but we should create the best possibilities to be
    created", and "check all other inventions if its restricted in some way of usage";
  - the audits `docs/affordance_audit_2026-11-02.md` and `docs/action_audit_2026-11-02.md`;
  - the creator's "go ahead" for step 1.
- **The evidence before it:** SC1 (late inventions never remade), UP1 (blocked at "cannot make"), WP1 (wanting the parts
  does not help).
- **Debate round 50** (`docs/debate_round50_af1_2026-11-02.md`): GPT 93%, Gemini 95%.

## The two rules (each a general law; neither names an invention)
- **S, "make by what it does"** (`similar_parts` 1).
  - **The rule:** when a person makes a thing they know, any input of the recipe may be replaced by something they hold
    whose 10 properties (edge, reach, hard, contain, warm, float, tight, plastic, fuel, flex) are each **within
    D = 10** of the original input's. The inputs are a part, a binder, a struck material, a shaped material, or a
    heated thing.
  - **Where the properties come from:** a raw material's from the material table; a made part's from the world's record
    of that kind.
  - **Which holding is used:** an exact holding first; otherwise the closest that fits, in a fixed order with no chance
    involved. The thing made follows from what was actually used, by the existing physics.
  - **The remembered recipe never changes.**
  - **A fact of the existing physics:** at D = 10 no raw material can replace another (the closest pair, stone and
    flint, differ by 15). So in practice S lets **made parts** stand in for each other.
- **K, "containers contain"** (`containers_carry` 1). The carry factor of the best thing held (1 + contain/100, the same
  factor that already multiplies the food limit) also multiplies:
  - **the made-thing limit:** 3 × factor, rounded down;
  - **the material limit:** 20 × factor.

  The container counts toward its own limit, and only the single best container counts. If a person holds more than
  their limit, for example after losing the container, the least valued extra things are set down on the ground at the
  end of the week, as OP1 already does for things pushed out.

**Nothing else changes.** Storing and building with made things (the audit's third rule) is left for a later study.

## Arms (32 paired seeds 22301–22332; LP: 80 founders, 80 × 80; 200 years; years 100–200 counted)
| arm | settings |
|---|---|
| **v11** | `similar_parts` 0, `containers_carry` 0 (= `code_v11`, shown by the zero checks) |
| **S** | 1, 0 |
| **K** | 0, 1 |
| **S+K** | 1, 1 |
| **sham** | v11 with `sham_draw` 1 |

## Primary (frozen): lineage remaking
- **R:** the share of world-new kinds first made in play in years 100–195 whose **own remembered recipe** is chosen
  again by a `make` action within 260 weeks.
  - The maker can be anyone who knows that recipe, using any inputs the arm allows. The make must succeed.
  - The recipe's identity is tracked, not the product's: in S a remake with substituted parts counts, because the same
    recipe was chosen.
  - Each world's counts are pooled first.
- **Intervals:** a paired world bootstrap, 10,000 replicates, NumPy seed 20261106. The same drawn seeds are used for
  every arm.
- **The contrasts:** each of S, K and S+K against v11 and against the sham; S+K − S; S+K − K; sham − v11.

## Frozen reading rule (GPT's, as in WP1)
1. **Inconclusive (sham):** if the sham − v11 interval lies wholly outside ±0.01.
2. **Otherwise, for each of S, K and S+K:** "positive" only if both hold:
   - arm − v11 and arm − sham both have intervals above 0;
   - both point differences are at least 0.01.

   Otherwise "inconclusive".
3. **Guards** (each arm against v11; stated with the reading):
   - **population:** arm ÷ v11 below 0.90, with the upper bound below 1;
   - **extinctions:** 3 or more beyond v11's.

## Secondary (described, not decisive)
- **Functional remaking:** a make whose product's 10 properties are each within D of a late kind's recorded properties.
  - Each make counts for at most one kind, the nearest; ties go to the earlier kind.
  - It counts only after that kind's invention.
  - Reported at D = 5, 10 and 20.
- **Recipe availability:** for each late kind, whether someone alive still knows its recipe at 1, 2 and 5 years after
  invention.
- **Use of the rules:** makes that used a substitute (S), and the mean made things and materials held by adults (K).
- **Activity:** makes per adult-year; kinds invented per 100 adult-years.

## Validity (hard stops)
- **Zero checks:**
  - `code_af1` with both settings 0 = `code_v11` (state and random numbers, 20 and 60 years);
  - S, K, S+K and the sham each act, and S, K and S+K differ from each other;
  - the observer is read-only;
  - reload is exact (arm S+K saved at year 10 continues exactly to year 15);
  - in S, **when the exact inputs are held, the recipe is made exactly as in v11** (unit checks before data).
- **All 5 × 32 worlds** are present under one `code_af1` fingerprint.
- **A blind recompute by GPT and Gemini** of R per arm, the contrasts with intervals, the readings and the guards, from
  per-world counts.

## The assistant's prior
1. **K inconclusive.** More room alone does not supply the right parts.
2. **S positive.** Made parts that are close enough often stand in.
3. **S+K positive,** and at least S's size.
4. **No guard raised.**

## Sign-off (2 November 2026)
The assistant, with **the creator's approval of step 1** ("go ahead", in this session). It is a nature-change test in a
copy under the 40% rule: GPT 93%, Gemini 95%, the assistant 55%. Frozen as `AF1-frozen` before any code or data.
