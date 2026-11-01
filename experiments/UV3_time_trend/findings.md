# UV3 — Is the shrinking habit gap rising returns or climbing values? Findings (not final until GPT and Gemini recompute)

**Read-only: no change to nature.** Frozen as `UV3-frozen`. Signed off by the assistant (GPT 95%, Gemini 97%, the
assistant 75%; debate round 42). Run on GitHub Actions (run 41357015837, `skip_zero=local`). 32 worlds: ES2's r arm
replayed on its 32 seeds (21501–21532) with a wider observer. Every number comes from `analyse_uv3.py`, written before
data and tested on a smoke world. The smoke caught one check that needed data in all quarters; it was fixed before data
(`WORKLOG.md`, 17:54). Full tables are in `results.md`.

**Validity:**
- zero checks pass;
- all 32 worlds are present under ES2's fingerprint;
- every update replays exactly;
- **every world matches ES2's r file exactly** (hash, n and Σ|q − G|);
- every update is in the decade table once;
- **the primary population's B by quarter equals UV2's to 4 decimals.**

**Population beside it:** ES2's r worlds, unchanged. Mean living population, r ÷ v11, 1.160 [1.029, 1.289] (ES2).

## The answer
**Returns stable, by the frozen rule.** Practised adult habits (k ≥ 80, ages 16–44, not death-closed) earned about the
same in years 175–199 as in years 100–124. Their **values rose**:

| quantity (standardized, years 175–199 minus 100–124) | value [95%] |
|---|---|
| **ΔG** (realized return) | **−0.010 [−0.016, −0.004]** |
| Δq (habit value) | +0.065 [+0.061, +0.069] |
| ΔB = Δq − ΔG | +0.075 |

The common support covers 21 of 43 cells, which hold 99.6% and 99.9% of the two quarters' updates.

**So the gap shrinks because the minds' values climb toward what life returns, not because the world changes.**

### Secondary (described, not decisive)
- **Per decade** (same population):
  - mean q rises steadily from +0.538 (100s) to +0.607 (190s);
  - mean G drifts slightly down, from +0.697 to +0.673;
  - B goes from −0.159 to −0.067.
- **Cohorts side by side:**
  - Within a decade, people born in different decades have similar gaps. For example, in the 140s: −0.112, −0.116,
    −0.111 and −0.092 for those born in the 90s, 100s, 110s and 120s.
  - Within each birth decade, the gap shrinks decade by decade. For those born in the 70s: −0.157, −0.142, −0.131.
  - **So the climb is shared by everyone alive at the time, not mainly carried by newer generations.** Age, period and
    cohort cannot be fully separated (GPT).
- **Newborns' starting values rise every decade:** +0.0015 (born in the 0s), +0.0228 (100s), +0.0324 (190s). This is
  the mean over all habit entries, most of which are near 0.
- **Tools' share of adults' foraged food falls:** 3.68%, 3.53%, 3.28%, 2.99% over the four quarters. H1's proposed
  mechanism (tools spreading) is absent.

## Against the prior (the assistant's, frozen)
1. "Returns stable: values climb, and G changes little": **right.**
2. "Newborns' starting values rise from decade to decade": **right.**
3. "Tools' share of food rises": **wrong.** It falls.

## What it means
- **Under the realized look-ahead, ACL's minds are still catching up, two centuries in.** The world's returns hold
  steady, but the population's values climb slowly toward them, by about 0.008 a decade (0.538 to 0.607 over nine decades).
- **The UV studies together:**
  - **UV1:** practice closes about half the gap fast.
  - **UV2:** what remains is not passed back from unpractised choices.
  - **UV3:** it shrinks over time with values rising for everyone at once.
- **The leading reading** (a hypothesis, not tested): values travel through families. Newborns start at half their
  parents' values, and children are pulled toward their carer's.
  - Each generation's start is held below the parents' level (the halving).
  - Yet it rises as the parents' values rise.
  - The whole population then converges slowly, as one coupled system.
  - GPT's caution: stable G with rising q "supports value adaptation, but does not establish inherited learning as the
    cause".
- **For Bob:** this is **cumulative inheritance of values, but slow.** Each generation starts a little higher than the
  last (newborns' starts rise every decade), so what earlier lives learned is passed on. But the passing-on halves it,
  and children take values from one carer only (`docs/research/value_transmission_2026-11-01.md`: forager children
  learn from many people after age 6). How fast a culture's sense of worth can catch up with its world may matter for
  minds that build on what others learned.
- **No change to nature** follows from this study.

## Independent recompute
Pending: GPT and Gemini, each in a fresh chat, from `recompute/uv3_cells.csv` (a CSV file). Recorded only from their
actual replies.
