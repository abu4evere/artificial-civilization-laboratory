# LA1 — Why are lessons refused? Findings (final: recomputed blind by GPT and Gemini)

Frozen as `LA1-frozen` (operational note 1). Run on GitHub Actions (run 40461644999, `skip_zero=local`). 32 worlds on
nature v7, LP (80 founders, 80×80), seeds 18701–18732, 200 years. Every number comes from `analyse_la1.py`, written
before data. The full tables are in `results.md`.

**Validity:**
- the zero checks pass;
- all 32 worlds are present under one fingerprint (`code_v7`);
- credence replays exactly for every lesson reaching G3;
- every outcome matches its recorded gate (mismatches 0).

## The answer

**Lessons for world-born kinds are refused mainly because the learner cannot follow them.** 85–88% of offered lessons
need a part the learner cannot make, which is the "cannot follow" gate (G4). Belief and openness pass about one lesson in
five. Acceptance per lesson **does not fall** after year 50: the premise behind Q4 does not hold at the level of single
lessons.

### Q1 — The rejection funnel (world-born useful kinds; all ages)

| era | offered | G1 known | G2 tried-and-bad | G3 not taken up | G4 cannot follow | taken | cannot follow (regardless of order) |
|---|---|---|---|---|---|---|---|
| 0–50 | 172,203 | 0.041 | 0.000 | 0.741 | 0.194 | 0.0236 | 0.862 |
| 50–100 | 173,172 | 0.031 | 0.000 | 0.753 | 0.195 | 0.0212 | 0.876 |
| 100–200 | 206,088 | 0.033 | 0.000 | 0.766 | 0.177 | 0.0247 | 0.851 |

- **G3 comes before G4 in the code**, so in the order of the gates the chance draw rejects about three in four lessons.
  Most of those lessons could not have been followed anyway: 0.85–0.88 of all offered lessons need a part the learner
  lacks.
- **Of lessons taken, 0.56 (early) and 0.37 (late) are pushed out at once** by a full 12-recipe memory.
- **G2 (tried and found bad) never rejects a lesson.** G1 (known) rejects 3–4%.
- **Part lessons** (shown instead at G4, parts-first) number about 21,000 per era. They are kept out of the funnel.

### Q2 — Threshold margins (lessons reaching G3)
- **Mean p:** 0.227 → 0.223 → 0.209. It is not near zero: only 0.2–0.4% of lessons have p < 0.05.
- **Openness** is flat (0.354 → 0.354). **Credence** falls (0.632 → 0.572), through its base, goodwill weighed against
  the record (+0.551 → +0.484).
- The child bonus (+0.026), health (+0.067) and evidence (+0.019 → +0.012) hardly move.

### Q3 — Groups (world-born useful unless stated)
- **Founder kinds** are taken 0.084 of offered, against 0.023 for world-born kinds, at the same mean p (0.223 against
  0.219). The difference is not belief.
- **Teacher:**

  | teacher | taken | mean p |
  |---|---|---|
  | parent | 0.066 | 0.60 |
  | carer | 0.051 | 0.49 |
  | other kin | 0.023 | 0.24 |
  | others | 0.018 | 0.16 |

- **Learner:** children take 0.027, teens 0.024, adults 0.022.

### Q4 — The frozen decomposition (years 0–50 against 100–200)

| term | 0–50 | 100–200 | Δ ln [95%] |
|---|---|---|---|
| T1 passes G1 | 0.9587 | 0.9671 | +0.009 [0.002, 0.017] |
| T2 passes G2 | 1.0000 | 1.0000 | 0 |
| T3 mean p at G3 | 0.2272 | 0.2087 | **−0.085 [−0.114, −0.053]** |
| T4 can follow (p-weighted) | 0.1082 | 0.1231 | +0.129 [0.037, 0.228] |
| **P(taken), expected** | **0.0236** | **0.0248** | **+0.053 [−0.038, 0.155]** |

- **There is no fall to decompose.** Expected acceptance rose slightly, and its interval includes zero.
- The script's frozen rule names **T3 (mean p)**: it is the only term that fell. But the "shares of the fall" in
  `results.md` (−1.59, 2.43) are not meaningful, because the total is not a fall. They are read here as Δ ln only.
- **T3's fall** splits into:
  - credence −0.0211;
  - openness +0.0002;
  - covariance +0.0024.

  Within credence, it is the base (goodwill against the record).
- **T4 is the smallest term by far.** Only 0.11–0.12 of the p-weighted lessons reaching G3 can be followed. The level
  of T4, not its change, is what holds acceptance down.

### Q5 — Counterfactual replay (years 100–200; diagnostic, no later effects)
The actual expectation is 5,121 lessons taken. Against it, setting one thing alone:

| set back alone | × actual |
|---|---|
| (a) p to its early mean | 1.06 |
| (b) credence | 1.05 |
| (c) openness | 1.00 |
| (d) G1 removed | 1.44 |
| **(e) G4 removed** | **8.12** |

## Why NA1 saw a fall (reading; not tested here)
NA1's 0.031 → 0.004 is a different measure. It is per kind and per distinct person, and its eras are the era of the
kind's **first making**, not the lesson's time. LA1 counts every lesson by **when it was offered**.

Read together:
- a lesson offered late is as likely to be taken as an early one;
- kinds first made later are taken by fewer of the people offered them.

That is consistent with later kinds being deeper (needing more parts the learner lacks), but LA1 did not test it.

## Against the prior (the assistant's, frozen)
1. "G3 rejects over 80% of offered, G1 most of the rest": **wrong on both.** G3 rejects 0.74–0.77 in order, and G4,
   not G1, rejects most of the rest (0.18–0.20, against G1's 0.03–0.04).
2. "Mean p about 0.1 early, lower late": **wrong level** (0.227), **right direction** (0.209).
3. "The late fall is carried mainly by E[p], through credence, through the record and the child bonus": **the fall does
   not exist per lesson.** E[p] did fall slightly, through credence's base, not the child bonus.
4. "Setting p back at least triples late takes": **wrong** (×1.06).

## What follows (from the frozen branches)
- **G4 carries acceptance down.** The frozen branch: "lessons need parts the learner lacks. Parts-first teaching is the
  existing route." So the question moves to parts-first, whether part lessons are taken and lead on to the whole. Q5's
  ×8.1 shows how much is held at G4. It says nothing about whether removing the gate would help, since a learner who
  cannot make a part cannot make the whole.
- **Not a malfunction of belief.** p is about 0.21–0.23, flat in openness and slightly lower in credence. Credence falls
  through goodwill weighed against the record, which may be rational. Raising belief would add about 5% (Q5 a and b).
- **Memory pushes out half of what is taken early.** This is the 12-recipe limit, and it is a second leak after taking.
- **The chain stands:**
  - tools pay (MK1);
  - making loses at the choice to habits (CO1, HL1);
  - lessons are refused mostly because their parts are missing (LA1);
  - what is taken is often pushed out of a full memory.

## Independent recompute (27 October 2026)
GPT and Gemini, each in a fresh chat, worked from the raw cells only, without the analysis script
(`recompute_la1.md`). **All three agree on every key number:**
- the gate shares;
- T1–T4;
- P 0.0236 → 0.0248, Δ ln +0.053;
- intervals including zero ([−0.040, 0.157] and [−0.040, 0.157]).

**Final.**
