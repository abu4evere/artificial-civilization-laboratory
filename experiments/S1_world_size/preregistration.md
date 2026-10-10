# S1 — World size: more land, and more people (pre-registration, SIGNED OFF and frozen as `S1-frozen`)

**Signed off by the creator (October 2026):** 256 new seeds (3001–3256); a run-time limit of 2 days; a fourth arm **P** (40 × 40, 80 founders) added, making a 2 × 2 design; thresholds as drafted. Nothing has been run beyond the feasibility check.

## Why

- **N10:** ACL founds 20 people and holds 20–40, the size of one aggregated forager band; real forager populations
  are far larger (Hamilton et al. 2007) and a minimum viable population is put at ~75–150 (White 2017). These describe
  different things and **neither sets ACL's founder count or map size**; the values below are operational choices that
  keep ACL's own crowding.
- **F1, P2, G1:** worlds die from failing to meet partners; singles rarely search; groups hardly mix.
- The creator chose (b): test **more land alone** and **land and people together**, to challenge the current
  explanation rather than build a bigger world and hope.

## Two questions, kept apart

1. **Does a larger world change survival?** L (80 × 80, 20 founders) against C (40 × 40, 20 founders).
2. **Does adding founders change survival, given the larger world?** LP (80 × 80, 80 founders) against L.

3. **Does adding founders change survival without more land?** P (40 × 40, 80 founders) against C. (Added at sign-off.)

LP against C, and LP against P, are reported **descriptively only** (the 2 × 2 interaction is described, not tested).
**Multiplicity:** three primary comparisons, each read at p < 0.05 as before; Holm-adjusted p-values are reported
beside them, and any reading that does not survive the adjustment is marked as such.

**Known confound (the code's own rule, not altered):** founders form `min(4, founders / 4)` bands, so LP's 80 founders
start as **4 bands of 20** (C and L: 4 bands of 5), and so do P's. Questions 2 and 3 therefore test "more founders,
in larger founding bands"; they cannot separate the two. P also has four times today's crowding (8 land tiles per
founder).

## Arms (all in `code_p2` with every P2/MC1 setting off, which reproduces the control world; settings only)

| arm | width × height | founders | other |
|---|---|---|---|
| **C** | 40 × 40 | 20 | — |
| **L** | 80 × 80 | 20 | — |
| **LP** | 80 × 80 | 80 | — |
| **P** | 40 × 40 | 80 | — (added at sign-off) |
| **S** sham | 40 × 40 | 20 | `sham_draw = 1` (as before) |

L and LP with the same seed share the same land (the land is made before the founders); C and L cannot share land.

## Feasibility (done; `feasibility_results.md`)

All arms ran 10 years without error on four throwaway seeds; land share 40% in all; fertility and wildlife per land tile
comparable (0.37–0.39; 4.1–4.4 groups per 100 land tiles); manipulation as intended: land per founder 32 / 128 / 32,
distance between founding bands 15 / 30 / 31, possible partners in sight per founder 2.0 / 2.0 / 9.8. Runtime in the
first years: 1.0 / 1.5 / 5.6 seconds per world-year.

## Measures (population beside every measure; defined before any main run)

- **Rule 14 first:** C's extinction share.
- **Extinction** (as in every study so far): a world is extinct if it does not reach year 120 with someone alive
  (`pops` has 12 decade marks and the last is above 0). **Survival** = not extinct.
- **Population outcome:** population at year 119 **divided by the founders** (growth multiple), median and quartiles;
  0 for extinct worlds. Absolute population is reported beside it.
- **Manipulation checks, at week one** (deterministic, as in feasibility): land per founder; distance between founding
  bands; possible partners in sight per founder. **During the run:** P2's encounter measure (share of seeker-weeks with
  an eligible single in sight), from the same read-only observer.
- Births per woman-year; child deaths per birth; starving share (hunger ledger); groups; G1's co-residence persistence
  is not re-measured here.

## Outcome rule (frozen at sign-off)

For each question separately (L vs C; LP vs L; P vs C), paired by seed, exact two-sided sign test on worlds that differ, and the
paired difference in extinction share with a 95% bootstrap interval (10,000 resamples, fixed generator seed):

| | reading |
|---|---|
| fewer extinctions, p < 0.05 | **the change improves survival**; its size is the effect estimate |
| more extinctions, p < 0.05 | **the change harms survival** (examined read-only) |
| p ≥ 0.05, and the interval excludes a change as large as half of F2's effect (0.34 × the reference arm's extinction share) | **no meaningful effect** |
| p ≥ 0.05 otherwise | **unresolved** at this sample |

The growth multiple is reported beside each, with a paired Wilcoxon test, as a secondary outcome. S against C should not
reach p < 0.05; if it does, every reading carries that caveat.

## Pilot before the main run (rule 12; runtime only)

One LP world and one P world, 120 years each, on throwaway seeds (9101, 9102): **only their run times are recorded**,
because populations can grow and make later years slower than the feasibility estimate. The main run's projected time
is 256 × (C + L + LP + P + S per-world times) ÷ 4 workers. **Pre-registered contingency:** if it exceeds 48 hours, the
main run uses the first 128 seeds (3001–3128) instead; this is decided from the pilot's run time alone, before any
main-run data.

## Hard stops

- Zero check: `code_p2` with settings off equals the control code (`code_e13r`) at **both** 40 × 40 and 80 × 80 (state
  hash, two seeds, 20 years).
- Code fingerprint unchanged in every run.

## Priors (written before any main run; not predictions to test)

- **Assistant:** L **worse** than C (the same 20 people spread thinner, bands twice as far apart); LP **better** than L
  (four times the partners in sight at the start). Held loosely.

## Decisions (taken by the creator at sign-off)

1. **Seeds:** (a) 256 new seeds (power as in MC1-L), or (b) 128 (half the time; detects only large effects).
2. **Runtime limit:** the feasibility estimate is ~19 hours for 256 seeds, but LP may slow as it grows; the pilot will
   measure it. What is the most you want to run?
3. **A fourth arm P (40 × 40, 80 founders)?** It would complete a 2 × 2 design and show whether people help without more
   land (at four times today's crowding). Not proposed by default; it adds cost and changes crowding.
4. **Thresholds** as above (as MC1-L).
