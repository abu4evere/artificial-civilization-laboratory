# UV3 — Is the shrinking habit gap rising returns or climbing values? A read-only replay of ES2's r arm (frozen plan)

**Read-only: no change to nature.** Live nature stays v11. UV3 replays ES2's r worlds exactly (`code_es2`, unchanged,
`realized_lookahead` 1) with a wider observer.

## Why
- **UV1** (final): under the realized look-ahead, practised habits stay under-valued (a floor near −0.11).
- **UV2** (final, not propagation): the floor is not passed back from unpractised choices further ahead. It **shrinks
  over time**. For practised adult habits, B goes −0.146, −0.119, −0.095, −0.075 across years 100–124, 125–149,
  150–174 and 175–199.
- **Two readings:**
  - **(H1) returns rise** (tools spread) faster than values follow;
  - **(H2) values climb** across generations, each starting at half its parents' values.
- **Debate round 42** (`docs/debate_round42_time_trend_2026-11-01.md`): both models chose this study first (GPT 93%,
  Gemini 95%). Both accepted the design below (GPT 95% with a coverage safeguard, adopted; Gemini 97%). A new test of
  ES2's rule (ES3) is deferred until after UV3. ES2 stays recorded as failed.

## The question
B = q − G, so the change in B over time is Δq − ΔG. **Did the realized returns G of practised adult habits rise, stay
stable or fall between years 100–124 and 175–199?**
- **H1** predicts G rises.
- **H2** predicts G stays stable while q rises.
- **Falling G** (for example crowding) is a third case.

**What it can and cannot show** (GPT):
- Age, period and cohort cannot be fully separated, so UV3 compares the hypotheses' predictions instead of fitting
  them.
- Stable G with rising q "supports value adaptation, but does not establish inherited learning as the cause".
- Rising G "supports H1's return-change component, not necessarily its proposed tool mechanism".

## Design
- **Worlds:** ES2's arm r only (`realized_lookahead` 1). The same 32 seeds 21501–21532, LP (80 founders, 80 × 80),
  200 years, the same code and settings. 32 worlds.
- **The observer:** UV1's observer, unchanged (k, age, death-closed), plus the following.
  - **The primary table:** for updates with k ≥ 80 and ages 16–44, sums of n, q and G. They are kept by year quarter
    (100–124, 125–149, 150–174, 175–199) × age bin (16–29, 30–44) × situation (the 32 situations) × action ×
    death-closed.
  - **A decade table:** for all updates, sums of n, q and G by the update's decade (100–109 … 190–199) × k bin × age
    bin × the person's **birth decade** (cohort) × death-closed.
  - **Newborns' starting values:** at every birth, the mean of the child's habit values (all entries), summed by birth
    decade (all years).
  - **Tools' share of foraged food by quarter:** adults' food with and without the tool in hand (TR1's measure, as in
    ES2), summed by year quarter.
- **As in ES2 and UV1:** q is the value just before the update; G = Σ_j 0.8^j r over the person's next updates; only
  updates started in years 100–200 are counted. The quarter and decade are those of the update's start.

## Primary (frozen)
- **The population:** updates with k ≥ 80, ages 16–44, G not closed by death.
- **Cells:** c = age bin × situation × action.
- **Common support:** cells with at least 100 updates (pooled over the 32 worlds) in **both** years 100–124 (Q1) and
  years 175–199 (Q4).
- **Weights:** w_c = (n_c,Q1 + n_c,Q4) / Σ over common cells. They come from update counts only, are fixed, and are
  never recomputed from G (GPT).
- **ΔG = Σ_c w_c (Ḡ_c,Q4 − Ḡ_c,Q1),** where Ḡ is the pooled mean G in the cell.
- **Interval:** 95%, by a world bootstrap (10,000 resamples of the 32 seeds; NumPy seed 20261101). The weights stay
  fixed. In a resample, a cell with no updates in Q1 or Q4 is left out, and the remaining weights are renormalized.
- **Coverage (GPT):** the share of the population's updates in common-support cells, reported for Q1 and Q4.

## Frozen decision rule
- **Inconclusive:** coverage below 80% in Q1 or in Q4.
- **Returns rising:** ΔG's interval lies wholly above +0.05.
- **Returns stable:** ΔG's interval lies inside [−0.05, +0.05]. Then the shrinking gap is values climbing.
- **Returns falling:** ΔG's interval lies wholly below −0.05.
- **Mixed:** anything else.

## Secondary (described, not decisive)
- **Δq,** the same way. A check: Δq − ΔG equals the standardized ΔB.
- **Mean q, mean G and B per decade** (the population above).
- **B by birth decade within each decade** (cohorts side by side).
- **Newborns' mean starting value by birth decade.** H2's direct mark: do inherited starts climb?
- **Tools' share of adults' foraged food by quarter** (GPT: tool availability).

## Validity (hard stops)
- **Zero checks:**
  - the observer is read-only: the world state and random numbers are the same with and without it (20 and 60
    years);
  - every habit update replays exactly (mismatch 0);
  - every counted update lands in the decade table exactly once (its n equals the ES2 table's n);
  - newborns are recorded (at least one birth in the 60-year run).
- **All 32 worlds are present** under `code_es2`'s fingerprint (the same as ES2's).
- **The replay matches ES2:** every world's hash, and its pooled n and Σ|q − G|, equal ES2's r file for the same seed.
- **The primary population's B by quarter equals UV2's year-quarter B** to 4 decimals (the same updates).
- **A blind recompute by GPT and Gemini** of ΔG, its interval, the coverage and the reading, from per-world cell sums.
  These are too many to paste, so each model gets them as a CSV file (`recompute/uv3_cells.csv`). If a model cannot
  take the file, it recomputes ΔG and the reading from the pooled cell sums as text, and that is recorded as a
  narrower recompute.

## The assistant's prior
1. **Returns stable:** values climb, and G changes little.
2. **Newborns' starting values rise** from decade to decade.
3. **Tools' share of food rises** over the four quarters.

## Sign-off (1 November 2026)
The assistant, under the creator's sleep-mode autonomy (a read-only study under the 40% rule). GPT estimates 95%,
Gemini 97% and the assistant 75%. Frozen as `UV3-frozen` before any code or data.
