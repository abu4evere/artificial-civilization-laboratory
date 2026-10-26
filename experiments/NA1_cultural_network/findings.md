# NA1 — Who actually gets a chance to learn? Findings (recomputed independently by GPT and Gemini; final)

Frozen as `NA1-frozen` (operational note 1); run on GitHub Actions (run 40398335893, `skip_zero=local`). 32 worlds on
nature v7, LP (80 founders, 80×80), seeds 18501–18532, 200 years. Every number comes from `analyse_na1.py` (written
before data); full tables are in `results.md`.

**Validity:**
- the zero checks pass;
- all 32 worlds are present under one fingerprint (`code_v7`);
- the internal checks pass (non-knowers only; "took" only in a lesson; each stage within the one before).

**Population:** 112–130 per world; people within reach of a person aged 4+: 8.9 (years 0–50) → 13.7 (years
100–200).

## The answer

**Knowledge meets plenty of people and is offered to some. It is almost never taken, and what is taken is almost never
made.** The network is not thin. The leak is at the lesson, and then at use.

### Q1 — The effective network, per useful world-born kind (median)
- While its inventor lived, a new useful kind's inventor was within reach of **47–77 non-knowers** and talked with
  **39–63**.
- **Over half of new kinds were never offered by their inventor in years 0–50** (0.58 with no lesson offered), and 0.38
  were never offered by anyone in years 100–200.
- **Any knower over the kind's whole life:** co-present with 66–82 non-knowers (median), offered to 1–3, taken by
  0 (0.93–0.98 of kinds never taken by anyone).

### Q2 — The funnel (primary; pooled over 20,593 world-born useful kinds and their non-knowers)

| step | rate [95%] | ln |
|---|---|---|
| co-present → talked | 0.849 [0.843, 0.856] | −0.16 |
| talked → offered | 0.135 [0.123, 0.146] | −2.01 |
| **offered → took** | **0.020 [0.018, 0.023]** | **−3.91** |
| took → made | 0.033 [0.024, 0.044] | −3.40 |
| made → passed | 0.61 [0.45, 0.80] | −0.50 |

Counts: co-present 2,044,075; talked 1,736,075; offered 233,771; took 4,694; made 156; passed 95.

**The step with the largest loss: offered → took.** Took → made is close behind.

By era, offered → took fell from **0.031 (years 0–50) to 0.004 (50–100) and 0.003 (100–200)**. In the two later eras,
nobody who took a world-born kind ever made it (took → made fell to zero; 235 and 121 took). When a lesson failed, a
**different** recipe was taken about as often as the right one (took a variant: 0.27 per kind early against 0.36 took).

### Q3 — The ratchet ledger (A → B → C)
- **123 improvements** by someone who had learned the part from another person (6.0 per 1,000 world-born useful
  kinds). Mean factor gained: +0.26.
- **38 completed A→B→C chains** (1.85 per 1,000 kinds): **36 in years 0–50, 1 in 50–100, 1 in 100–200.**
- ACL does produce cumulative steps, rarely, and almost only in its first half-century.

### Q4 — Network against population (described)
- A kind's reach fell over the eras (104 → 84 → 75 non-knowers co-present per kind), while population rose and fell.
- Across world-eras, population and reach go together (rank correlation 0.59, 96 world-eras). This is confounded by
  era and was not tested further.

## Against the prior (Claude's, frozen)
1. "Co-presence is wide (median over 20)": **right** (66–82).
2. "The largest loss is talked → offered": **wrong.** It is offered → took (talked → offered is third).
3. "offered → took is the second loss, about 0.05–0.15": **wrong.** It is the largest, at 0.02.
4. "Completed A→B→C chains under 1 per 1,000 world-born kinds": **wrong** (1.85), though almost all early.
5. "Reach does not rise with population": **wrong as described** (0.59), and confounded by era.

**The debate's expectations:**
- GPT expected the audit to separate population from real chances to learn. It did: the chances are there, and they
  are refused.
- Gemini expected leaks at the physical and observational stages. Those are absent by construction, so they were not
  measured here.

## What follows (frozen branches)
- **offered → took carries the largest loss:** lessons are refused. Next: the learner side, without tuning uptake.
  LU1 found the main reason was "not open" (credence × openness). Why uptake falls tenfold after year 50 is a question
  on its own; one candidate, not tested, is that learners are near the 12-recipe limit or already hold variants.
- **took → made is close behind** (and zero after year 50): learners who take a recipe don't make it. This is MK1's
  and CO1's choice: other habits outscore making. Giving and watching (A1, C1) remain relevant to it.
- **Co-presence is not small:** the network is not thin. Population, band structure and movement are **not** the first
  levers (GPT's caution confirmed).
- **Ratchet chains exist but die out after year 50**, with the same timing as the collapse of the making choice (MK1,
  CO1).

## Independent recompute (27 October 2026)
GPT and Gemini, each in a fresh chat, from the raw rows only, without the analysis script (`recompute_na1.md`). **All
three agree:**
- the stage totals;
- the step rates (offered → took 0.020079 [0.0176, 0.0230]);
- the largest loss;
- the by-era rates (0.0311 / 0.0041 / 0.0032);
- the medians;
- the ratchet counts (123; 38).

**Final.**
