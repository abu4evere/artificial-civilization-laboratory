# AM1: Measuring autonomy against constrained controls — findings

**A read-only study on nature v11** (`code_v11`). The arms change existing settings only.
- Frozen as `AM1-frozen`, with amendment 1 made before data: "more chance" is temperature 0.25, chosen on survival
  only.
- Signed off under the creator's sleep-mode autonomy. Council round 52: GPT 94%, Gemini 97%, DeepSeek about 92%, the
  assistant 70%.

**The run:**
- GitHub Actions run 41587348657 (2 h 10 min).
- The zero checks ran locally (`zero_local.log`: All: PASS). They show:
  - the observer is read-only in all four observed arms;
  - the controls act;
  - the fewer-acts arm completes no chain;
  - reload is exact.
- 160 worlds: five arms × 32 paired seeds (22501–22532). LP, 200 years; years 100–200 counted.
- Every number comes from `analyse_am1.py`, written before data. Full tables are in `results.md`.

**Validity:**
- the zero checks pass;
- all 160 worlds are present under `code_v11`'s fingerprint;
- the sanity check passes (the fewer-acts arm completes no chain).

## The answer
**Only M1 behaves partly like a measure of autonomy. M3 and M5 run the other way: worlds made less autonomous by
construction show *more* gather-then-make chains than v11.**

| measure | v11 | no habits − v11 [95%] | more chance − v11 [95%] | reading |
|---|---|---|---|---|
| **M1**, a person's own past predicts their next choices (SC1's C12) | 0.0821 | +0.0038 [−0.0059, +0.0136] | **−0.0344 [−0.0812, −0.0047]** | **partly validated** (by more chance only) |
| **M3**, gather an input, then make with it (against opportunity-matched weeks) | 0.0036 | **+0.0257 [+0.0238, +0.0277]** | **+0.0041 [+0.0034, +0.0047]** | **not validated** (both controls *higher*) |
| **M5**, the same after a week spent on food | 0.0038 | **+0.0280 [+0.0259, +0.0302]** | **+0.0045 [+0.0037, +0.0053]** | **not validated** (both controls *higher*) |

- **The sham is stable** for all three: its intervals lie within the frozen band.
- **The sanity check passes:** the fewer-acts arm completes no chain. M3 and M5 cannot be computed there (0 ÷ 0).
- **Population, beside every measure:**

  | arm | living-weeks |
  |---|---|
  | v11 | 22.2 M |
  | no habits | 16.6 M (75%) |
  | fewer acts | 21.8 M |
  | more chance | 21.2 M |
  | sham | 22.4 M |

**The assistant's prior:**
1. M1 validated by more chance, not by no habits: **right**.
2. M3 partly validated, by more chance: **wrong**. It is not validated, and both controls run the other way.
3. M5 not validated: **right**.
4. Sanity passes and the sham is stable: **right**.

## Described (no frozen prediction)
| measure | v11 | no habits | more chance |
|---|---|---|---|
| M2, sequence structure (bits beyond a time-shuffle, per adult-year) | 0.163 | 0.132 | 0.139 |
| M4, new tiles / new persons / new recipes made | 0.061 / 0.124 / 0.089 | 0.076 / 0.184 / 0.031 | 0.066 / 0.129 / 0.069 |
| M6a, a first make that uses a never-handled input | 0.247 | 0.475 | 0.295 |
| M6b, an established chain done under a new cue | 0.442 | 0.497 | 0.466 |

**M2** falls in both controls (intervals above 0 for v11 − control). It behaves as a measure of autonomy should, but
had no frozen prediction. It is a candidate for a later frozen validation.

## What it means (the assistant's reading; for the council)
1. **In v11, learned habits suppress following through.** Without habits steering choice, a gather of a needed input
   leads to a make about eight times as often (beyond matched weeks). This is the same direction as:
   - CO2: "the decline over time is habit";
   - VC1: habits over-value common actions and under-value making.
   The habit system, TD learning with a max look-ahead, pulls people back to common actions and away from finishing
   what they started.
2. **Habits also keep people alive.** The no-habits arm has a quarter fewer living-weeks. So habits are not simply
   wrong: the same learning that helps survival crowds out ends-directed making.
3. **M1 (personal predictability) does not depend on habits.** Without them, a person's past still predicts their
   future as well: through temperament, place and resources (GPT's confound in round 52). M1 is a measure of personal
   style, not of self-direction.
4. **For Bob:** none of M1, M3 and M5 can yet judge a redesign. M2 is the best candidate. Any law aiming at goals
   across weeks (`docs/research/options_routines_2026-11-02.md`) must face this tension: what makes people survive (habit
   toward common actions) is what stops them from finishing ends.

## Blind recompute (`recompute_am1.md`)
- **GPT** (chat `6ae998a7`) and **Gemini 3.1 Pro** (chat `be3f18612734932e`) recomputed M3, M5 and their contrasts
  with code, blind, from the per-world counts, with the prompt written before data. Both **match every value,
  interval, reading and the sanity count**.
- **DeepSeek** (chat `2e5c76a3`, by hand) matches every point value and reading. Its intervals were too narrow, an
  approximation that decides nothing.
- **M1** is not in the recompute prompt, as in SC1, where it was recomputed from saved error sums. That leaves AM1's
  partial validation of M1 as the analysis's own number; it is the measure's prior use, and it matches SC1's C12.
- **AM1 is final** for M3 and M5.

## Next
- **The identical battery on v12** (round 52's plan). It now carries one more question: does FF1's make-choice fix
  change M3?
- **For the council:** the habit/ends tension above, as the main lead toward goals across weeks.
