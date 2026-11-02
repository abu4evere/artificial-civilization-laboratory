# SC1 — A scorecard of the creator's twelve capacities on live v11 (frozen plan)

**Read-only: no change to nature.** Live v11 (`code_v11`).
- **Its origin:** the creator's twelve capacities that "may create Bob" (Telegram, 2 November 2026).
- **Debate round 46** chose a scorecard first (GPT 90%, Gemini 90%).
- **Debate round 47** shaped it (`docs/debate_round47_sc1_2026-11-02.md`; GPT 86%, Gemini 94%).
- **The draft** it came from: `docs/sc1_design_draft_2026-11-02.md`.

**What it is not:** a measure of Bob, an intelligence score, or a test of whether a capacity is absent. It is a
**baseline**, so that later nature changes can be judged against it.

## Common design
- **Worlds:** 32 new seeds, 22001–22032 (used by no study). LP: 80 founders, 80 × 80, 200 years; years 100–200
  counted.
- **Intervals:** a world bootstrap, 10,000 replicates, NumPy seed 20261103. Every rate is pooled within a world, and
  worlds are resampled.
- **Population:** reported beside every measure (people and adult-years in the measure's sample).
- **Labels:**
  - **Given:** written as a law; nothing emergent to score.
  - **Not measurable in v11:** no mechanism exists. **Never scored zero.**
  - **Measured:** one **primary contrast**, with its own control and its own **minimum effect δ**, fixed here.
    - The reading is **"positive contrast detected"** only if the 95% interval's **lower bound exceeds δ**.
    - Otherwise it is **"inconclusive"**. **Never "absent".**
- **No combined score.**

## The twelve
### Given (described only)
- **1. Perception.** Senses are fixed laws: reach 3, sight 4, the 12 nearest people (`mind.decide`). Described: the
  share of adult decisions with company in reach, and with fresh water in reach.
- **11. Motivation and emotion-like regulation.** Drives, the eight traits, six feelings and their decay rates are
  written (`biology._feelings`). Described: mean mood and loneliness of adults.
- **3 (the rule). Learning.** The habit rule is written. Its effect is measured below as C3, but labelled "the
  written rule works", not an emergent capacity.

### Not measurable in v11
- **2. Memory, retrieval when relevant.** Memories reach choices only by salience × strength (grief, the worst memory,
  gossip, the latest salient memory in talk). Nothing recalls a memory because it matches the present
  (`thought.py` 116–132; `information.py` 148; `mind.py` 443). Described: memories held, lived against told.
- **3 (transfer).** The habit table is one value per situation × action, so learning cannot carry over to an unseen
  situation.
- **8. Self-model and metacognition.** Nothing represents a person's own ability or uncertainty.
- **10a (social cognition).** Whom people trust is written (`information.credence`; `tested` changes trust).
  Partner choice cannot be told apart from those laws. Social **learning** is described: the share of recipe gains by
  each path (made, taught, copied, read, with or without an error).

### Measured (primary contrast, control, δ)
- **C3. The learning rule's effect** (label: "the written rule works").
  - **Sample:** adults 16–44; habit updates whose realized return G closes before death. The replay and G come from
    ES2/UV1's observer, and k is the number of earlier updates of the same habit by the same person.
  - **Primary:** mean abs(q − G) at k 0–19 minus at k 80+, standardized over situation × action cells.
    - The weights are the pooled k 0–19 counts.
    - Common cells have at least 30 updates in both bands, pooled over worlds.
  - **δ = 0.02.**
- **C4. Causal understanding (proxy): switching means after a surprise.**
  - **Sample:** own tests of a made thing's worth (`tested` events on `m:` keys). Only tests by people who know at
    least one other recipe that shares a material with the tested one (the opportunity for an alternative), and only
    those followed by a make within 13 weeks.
  - **Outcome:** that first make is an **alternative**: a different recipe sharing a material.
  - **Primary:** P(alternative | surprising test, abs(gap) ≥ 0.25) − P(alternative | confirming test, abs(gap) < 0.1).
  - **δ = 0.05.**
  - **Note:** the puzzle's steer pulls toward the **same** thing (`thought.steer`), so the law works against this
    contrast.
- **C5. Planning (label at most "organized production detected", never "planning"; the written pulls drive both
  steps).**
  - **Sample:** adults' gathers of a material by people who know a recipe that uses it.
  - **Outcome:** a make of such a recipe within 26 weeks.
  - **Primary:** P(make | the material was wanted at the decision, `mind._material_wants` > 0) − P(make | not wanted).
    Gathers are matched on season and on the person holding fewer than 1 of the material before the gather; the
    contrast is standardized over material × season.
  - **δ = 0.05.**
- **C6. Invention with selection by use.**
  - **Sample:** world-new kinds (first entry in the world register) made in play in years 100–200.
  - **Outcome:** **made again by choice** (a `make` event of that kind, by anyone) within 260 weeks.
  - **Function of a kind:** its best factor over the uses (`matter.factor`: forage, hunt, wood, stone, fiber, fight,
    carry, cold), read from the register's properties.
  - **Primary:** P(remade | functional, best factor ≥ 1.10) − P(remade | non-functional, best factor < 1.02).
  - **δ = 0.05.**
- **C7. Own goals (proxy): own puzzles against told ones, matched on size.**
  - **Sample:** `m:` puzzles opened while the person knows that recipe.
    - "Own" means it opened from the person's own surprise (`inquiry.surprised`).
    - "Told" means it opened from a lesson (`information._wonder`).
  - **Size bins:** 0.25–0.35 and 0.35–0.45, where both kinds occur.
  - **Outcome:** the person makes that kind within 26 weeks.
  - **Primary:** P(acted | own) − P(acted | told), standardized over size bins with pooled weights.
  - **δ = 0.05.**
- **C9. Communication: told places beat chance.**
  - **Sample:** told water and game places (`hear_place`) that the listener later checks (`verified` or `refuted`).
  - **Control:** for each checked place, one land tile at the same distance from where the listener was when told,
    picked with the **observer's own** random stream (never the world's). The same check is applied at the same week:
    fresh water within 1 tile, or prey within 1 tile.
  - **Primary:** P(verified) − P(control check true).
  - **δ = 0.10.**
- **C10b. Cumulative culture: building on others' know-how.**
  - **Sample:** world-new kinds in years 100–200 whose recipe uses a made part (a bind with a made part, or a heat of
    a made thing).
  - **Outcome:** the inventor had learned the part's recipe **from someone** (taught, copied or read, with or without
    an error).
  - **Primary:** that share, minus the share of the inventor's whole repertoire that was learned from someone at that
    moment (the opportunity).
  - **δ = 0.05.**
  - **Secondary:**
    - the new kind's best factor against its part's (improvement);
    - kinds alive whose first maker is dead;
    - the number of distinct holders per kind;
    - nesting depth in years 100–125 against 175–200.
- **C12. Stable behavioural individuality** (not identity; not chosen goals).
  - **Sample:** adults alive in year t and in year t + 5, for t = 100, 105, …, 190.
  - **Data per person and year:** shares of their 19 actions; shares of their 32 situations; temperament; age; sex;
    and the year-t **habit summary**. The summary is, per action, the mean q over the 32 situations, weighted by their
    own situation shares in year t.
  - **The two models** (ridge, λ = 1, predicting year t+5 action shares):
    - **Model A:** temperament, age, sex, year t+5 situation shares, and the year-t habit summary;
    - **Model B:** Model A plus the year-t action shares.
  - **Cross-validation:** four folds of eight worlds each; each world is scored by a model trained on the other folds.
  - **Primary:** the relative reduction in held-out mean squared error, (MSE_A − MSE_B) ÷ MSE_A, pooled per world.
  - **δ = 0.05.**
  - **Secondary:** Gemini's cross-situation test. Does a person's choice bias in situations they know well predict
    their bias in situations they have been in fewer than 5 times?

## Validity (hard stops)
- **Zero checks:**
  - the observer is read-only: the world's state and random stream are unchanged, with and without it, at 20 and 60
    years;
  - every habit update replays exactly (mismatch 0);
  - the observer's own random stream never touches the world's;
  - the `_material_wants` and recipe reads change nothing.
- **All 32 worlds** are present under `code_v11`'s fingerprint.
- **A blind recompute by GPT and Gemini** of every primary contrast and its interval, from per-world sums.

## The assistant's prior
- **Positive contrast detected:** C3, C9, C12.
- **Inconclusive:** C4, C5, C6, C7, C10b.
  - C4: the law pulls toward the same thing.
  - C5: the written pulls drive both steps.
  - C10b: nested building is rare.
- **The picture:** v11 shows individual learning, honest communication and stable individuality, but little evidence
  of goals, planning or building on others.

## Sign-off (2 November 2026)
The assistant, with the creator present and asking to keep working. A read-only study under the 40% rule: GPT 86%,
Gemini 94% (round 47), the assistant 70%. Frozen as `SC1-frozen` before any code or data.
