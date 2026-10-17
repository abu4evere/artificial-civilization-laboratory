# Council, 16 October 2026: the whole project so far — sorted by Claude

Question: `drafts/council_q_2026-10-16_whole_project.md` (words only, no code or data). Answers:
`2026-10-16_1722_…` (Gemma 4 31B) and `2026-10-16_1723_…` (NVIDIA Nemotron 3 Super 120B; OpenAI gpt-oss-20b).
Kimi K3 is retired on NVIDIA (HTTP 410); Kimi K2.6 and Nemotron 3 Ultra are listed but answer 404
(`tools/council_models.json` updated). Ideas only: nothing here is a decision; Law 126 applies to anything touching nature.

## Where all three agree: how often people move (question C)

All three say a weekly relocation, where real foragers move camp about monthly, probably distorts partner finding and
meetings between bands, and all three propose the same test: **people move only every few weeks, with the same distance
per month**, and compare extinction, between-band meeting and age at first birth (Gemma: keep the monthly distance equal;
Nemotron: every 2 and 4 weeks).

**Sorted.** The most useful idea of the session, and it meets today's evidence: Binford's 175 mobile societies move camp
every 4.3 weeks (median; `experiments/SA1_sensitivity/evidence_ratios.py`). **But it is not yet known how often ACL's
people actually move**: "may move every week" is the rule, not the behaviour. **Measured since** (`acl_ratios.py`, read-only, 16 October): they change place in **59% of weeks**, about 2.5 times as
often as forager camps, so the idea stands as a candidate study. Also: "stay put for n weeks" would be a rule about nature and needs Law 126 (evidence:
Binford's data, now in hand), and it must not be tuned toward survival.

## Worth keeping

- **Gemma, B: a food that only opens with force.** A high-value food whose hard shell yields only to a hard, heavy strike,
  stated as a property of the food and of materials, never naming a tool. It goes at the "tools add a few percent" trap
  (E8.2) with a condition, not an outcome. Needs an evidence review (processing-dependent foods among foragers, e.g.
  nut-cracking, baobab) before it could enter nature. A candidate, not a plan.
- **Gemma, A: is the sameness of habits the environment?** TC1 left this unresolved. A cheap read-only check: do people
  living in different parts of the same world (different food, water, cold) have less alike habits than neighbours? It
  needs no change to nature.
- **Gemma, D: no more swap studies** on identity. Agreed in effect: ID1 is done and nothing further is planned.
- **gpt-oss, C: separate time step from sight.** Its "double sight" arm is already SA1 (× 2 sight: 8 of 64 died, against
  22); combined with the movement test it would separate the two.

## Declined, and why

- **Scripted outcomes** (rule: conditions, not outcomes): gpt-oss's "social value bonus for copying a tool in use", a
  "fire-proof tool", "a stone axe that makes planks for a shelter"; Nemotron's shared "storage pit" open to everyone
  (a special invented place).
- **Wrong about ACL** (each checked in the code today):
  - "no seasons or shocks" (Nemotron A): ACL has four seasons, winter scarcity and die-back, weather;
  - "no regression tests" (Nemotron D): ACL has 57 tests, property tests and exact reference replays in CI;
  - "tools disappear immediately / no durability" (gpt-oss): items have a number of uses and wear out;
  - "gossip is the only social learning" (gpt-oss): watching exists (E7: 7 copies in 1,770 observations);
  - "40 founders would be double the maximum" (gpt-oss): WS1 ran 80.
- **Calibrate a tile to 1 km and a step to a day** (gpt-oss): a chosen number, not an anchor (N10); a daily step would
  be a new world, not a test.

## What it suggests doing (for the creator to decide; nothing started)

1. When `acl_ratios.py` finishes: if ACL's people move most weeks, draft a frozen **residence-time study** (move only every
   n weeks, monthly distance held equal; extinction, meeting, first births; 256 new seeds), with its Law 126 evidence
   from Binford.
2. A read-only **habit-sameness-by-place** check from existing saved worlds, if the data allows.
3. An evidence review for a **force-to-open food**, before any design.
