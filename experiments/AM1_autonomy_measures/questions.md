# AM1: Measuring autonomy, with measures checked against constrained controls (frozen plan)

**A read-only study on live nature v11.** The arms change only settings that already exist, and nothing in nature
changes.
- **Why:**
  - DeepSeek's first reply: the action architecture is the real barrier to Bob's autonomy, so measures for it must
    exist before any redesign;
  - council rounds 51 and 52 (`docs/debate_round52_autonomy_measures_2026-11-02.md`): GPT 94%, Gemini 97%, DeepSeek
    about 92%;
  - the draft: `docs/autonomy_measures_draft_2026-11-02.md`.
- **What it is for:**
  - to find which measures of autonomy are **valid**, meaning they fall in worlds made less autonomous by construction;
  - to record v11's values.
- **The same frozen battery** is to be run unchanged on v12 (if FX1 is adopted) as the baseline for any redesign. A
  difference between v11 and v12 never redefines success.

## Arms (32 paired seeds 22501–22532; LP: 80 founders, 80 × 80; 200 years; years 100–200 counted)
| arm | setting | role |
|---|---|---|
| **v11** (c) | as live | the world measured |
| **no habits** (h) | `learned_weight` 0: habits are still learned but do not steer choices | a less autonomous control: no learned personal direction |
| **fewer acts** (a) | `stage` "E0-C": no make, play, heat or fill | a sanity check only: chain measures must be 0 there |
| **more chance** (t) | `choice_temperature` 0.6 instead of 0.2 | a stochasticity control: less coherent choice |
| **sham** (x) | v11 with `sham_draw` 1 | the noise of history alone |

## The measures (adults aged 16–49, years 100–200; population beside every measure)
- **M1, self-prediction gain (level A)** is SC1's C12, unchanged.
  - **Pairs:** adults alive in year t and t + 5, t = 100, 105, …, 190.
  - **The models** (ridge, λ = 1, predicting year t+5 action shares):
    - **Model A:** temperament, age, sex, year t+5 situation shares, and the year-t habit summary;
    - **Model B:** Model A plus the year-t action shares.
  - **Cross-validation:** four folds of eight worlds, within each arm.
  - **The value:** the relative cut in held-out squared error, (SSE_A − SSE_B) ÷ SSE_A.
- **M2, sequence structure** (descriptive).
  - **For each adult-year with at least 40 decisions:** the mutual information, in bits, between consecutive actions.
  - **Minus:** the same for that year's actions shuffled in time. The shuffle uses the observer's own random stream,
    seeded by the world seed, never the world's.
  - **The value:** the mean over adult-years.
- **M3, ends-directed chains (level B).**
  - **A gather chain:** an adult gathers material m, where m is an input of a recipe they know and value (item value
    > 0.05) and they hold less than 1 of m.
  - **A matched chain** (opportunity-matched, GPT): an adult-week in which the same holds for some such m, m lies (≥ 1)
    on the person's own tile, and the person does not gather. At most one per person-week: the first such m in the
    fixed material order.
  - **The outcome:** the person makes one of the recipes using m within 8 weeks.
  - **M3 =** P(made | gather chain) − P(made | matched chain), from sums pooled per world.
- **M5, resuming after a need (level B).** M3 restricted to chains whose next decision by the person is a food action
  (forage, hunt or take).
- **M4, new targets** (descriptive). The share of adult decisions whose target is new to the person:
  - a tile they have never stood on, for forage, hunt, gather, explore, flee and join;
  - a person they have never acted on, for give, care, talk, court, steal and attack;
  - a recipe they have never made, for make.

  New *kinds* of act are 0 by construction in v11.
- **M6a, new in steps or in arrangement** (descriptive). Among a person's first makes of a recipe (by make or play):
  the share that use an input (a material or a made part) **the person had never used in any make or gathered
  before**. The rest are new only in arrangement.
- **M6b, transfer** (descriptive).
  - **An established chain:** a pair (m, recipe) that the person has completed (gathered m, then made the recipe within
    8 weeks) at least twice.
  - **Its cue:** season × food band (the situation index ÷ 8).
  - **M6b =** the share of later completions of established chains that happen under a cue not seen in that person's
    earlier completions of the same pair.

## Validation rule (frozen; directional, per measure)
- **Intervals:** a paired world bootstrap, 10,000 replicates, NumPy seed 20261108. The same drawn seeds are used for
  every arm.
- **M1, M3 and M5** are each predicted to be lower in h than in c, and lower in t than in c.
  - A measure is **validated** if both c − h and c − t have 95% intervals wholly above 0.
  - It is **partly validated** if only one does. Which one is named.
  - Otherwise it is **not validated**. It is then reported, not dropped, and it is not used to judge any redesign
    until it passes in a later study.
- **The sham:** if a sham − c interval for M1, M3 or M5 lies wholly outside ±(half the c − h point difference), that
  measure is marked **"unstable"**.
- **The sanity check (arm a):** the number of M3 chains completed by a make is 0. If not, the observer is wrong and
  **AM1 is not valid**.
- **M2, M4, M6a and M6b are described only.**
  - They have no frozen prediction: chance may raise variety and new targets (DeepSeek, GPT).
  - They are reported per arm with c − control intervals.

## Validity (hard stops)
- **Zero checks:**
  - the observer is read-only (the same state with and without it, in c, h, a and t, 20 and 60 years);
  - c = `code_v11` with v11's settings;
  - h, a, t and the sham each act;
  - reload is exact (arm c, saved at year 10, continues exactly to year 15).
- **All 5 × 32 worlds** are present under the `code_v11` fingerprint.
- **A blind recompute** by GPT, Gemini and DeepSeek, from per-world sums, of:
  - M3 and M5 per arm, with the c − h and c − t intervals;
  - the readings;
  - the sanity count.

  M1 is recomputed from the per-world held-out error sums (as in SC1).

## The assistant's prior
1. **M1:** validated by t, but **not** by h. v11's choices carry personal persistence through resources, place and
   temperament even without habits (GPT's confound).
2. **M3:** partly validated, by t only. The want to gather and the pull to make are written pulls that work without
   learned habits (SC1, C5).
3. **M5:** not validated (too few interrupted chains to separate).
4. **The sanity check passes;** the sham is stable.

## Sign-off (2 November 2026)
The assistant, under the creator's sleep-mode autonomy and the permission of 2 November. It is read-only. Council
rounds 51 and 52: GPT 94%, Gemini 97%, DeepSeek about 92%, the assistant 70%. Frozen as `AM1-frozen` before any code or
data.
