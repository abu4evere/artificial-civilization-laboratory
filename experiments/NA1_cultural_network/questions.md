# NA1 — Who actually gets a chance to learn? The effective cultural network audit (frozen plan)

**Read-only on nature v7. No change to nature.** From debate round 6 (`docs/debate_similar_projects_2026-10-27.md`):
GPT's first choice, which Gemini adopted. Instead of counting people, measure the **effective cultural network**: while
someone who knows a useful thing is alive, how many people who don't know it get a real chance to learn it, and how far
each gets. Also GPT's **ratchet ledger**: A invents → B learns → B improves → C learns the improvement.

## Why

- LS1: 98% of lost knowledge goes with its holder's death. Only 12% of useful kinds invented after year 100 are ever
  held by a second person.
- MK1: making loses to other options whose scores rise.
- TF1: things never pass between the living.
- The cultural-evolution literature (Henrich 2004; Derex et al. 2013; Muthukrishna et al. 2014; Derex & Boyd 2016, to
  check) says what matters is who can learn from whom, not headcount.

This study measures that network in ACL directly.

## Setting

Nature v7 (`code_v7`) unchanged, LP (80 founders, 80×80), 32 new seeds (18501–18532), 200 years (as MK1, TF1, CO1), run
on GitHub. "Useful" = a kind with a factor > 1 for any use (LS1's definition).

## Logged (read-only: weekly observer, plus wrappers that read state and call the original unchanged)

For every useful kind, from its first making, the observer follows its **knowers** (living people holding its recipe),
its **inventor** (its first maker in the world), and every living **non-knower** (aged 4+, the youngest age that can be
taught) at each stage:

| stage | a non-knower reaches it for a kind when … |
|---|---|
| **co-present** | they are within reach (the decision's `reach`) of a living knower in some week |
| **talked** | they talk with a living knower (either one starts it) |
| **offered** | a knower offers them a lesson meant for that kind (`information.hear_how`) |
| **took** | they gain that kind's recipe from such a lesson |
| **made** | having taken it, they later make or play-make that kind |
| **passed** | having taken it, they later teach it to someone who takes it |

Each stage counts **distinct people per kind**, twice:
- **with the inventor**, only while the inventor is alive;
- **with any knower**, over the kind's whole life.

**The ratchet ledger.**
1. B holds kind k by a social route (taught, copied or read), learned from A.
2. B then invents a new kind k′ (first in the world) that has k as a part (bound in, or heated), with a higher best
   factor than k.
3. Later, someone other than B (C) gains k′ by a social route.

Each completed A→B→C chain is counted, and so are incomplete ones (B improves, nobody learns it).

## Questions (by era of first making: years 0–50, 50–100, 100–200; world-born kinds primary; founders described)

**Q1. The effective network.** Per useful kind invented by a world-born person, while the inventor is alive:
- the number of distinct non-knowers co-present with the inventor, talked with, offered, took;
- the mean, median and share with zero at each stage.

The same with any knower, over the kind's life. Beside these: population, and people within reach.

**Q2. The funnel (primary).** Pooled over world-born useful kinds and their non-knowers (any knower, whole life), the
conversion at each step: co-present → talked → offered → took → made → passed. The overall rate from co-present to
passed splits exactly:

Δ ln = Σ ln(step rates).

**The step with the largest loss (the most negative ln step rate) is named.** World bootstrap (10,000 replicates).

**Q3. The ratchet ledger.** Per 1,000 useful world-born kinds: improvements by a social learner (B), and completed
chains (A→B→C), by era.

**Q4. Network against population (described).** Across worlds and eras: a kind's mean reach (non-knowers co-present
with a knower; non-knowers who took it) beside population and people within reach.

## What would follow (stated now; not exclusive)

- **The largest loss is co-present → talked:** knowers and learners meet but don't interact. Next: why talk goes
  elsewhere (CO1's social options).
- **talked → offered:** knowers talk but don't teach that kind (a teacher offers only their three most valued things,
  worth > 0.15). Next: what teaching offers, with C2 (teaching only inside talk) as a candidate.
- **offered → took:** lessons are refused (LU1: closedness). Next: the learner side, without tuning uptake.
- **took → made:** learners know it but never make it (MK1's choice). The giving and watching candidates (A1, C1) are
  relevant.
- **made → passed:** learners make it but never teach it on.
- **Co-presence itself is small** (few non-knowers ever near a knower): the network is thin, and band structure or
  movement is the question. **Population** by itself is not the answer unless reach grows with it (GPT's caution).
- **No completed ratchet chain:** ACL has no cumulative culture by the A→B→C test, whatever else holds.

## The assistant's prior (separate predictions)

1. Co-presence is wide: a world-born useful kind's knowers are within reach of dozens of non-knowers (median over 20,
   any knower).
2. **The largest loss is talked → offered.** Knowers rarely offer a given kind, because teaching offers only one of the
   teacher's three most valued things.
3. offered → took is the second loss (about 0.05–0.15).
4. Completed A→B→C improvement chains: under 1 per 1,000 world-born useful kinds.
5. A kind's reach does not rise with population across worlds (no clear association).

**On record from the debate:** GPT expects the audit to separate population from real chances to learn. Gemini
expects transmission leaks at the physical and observational stages (which are absent by construction).

## Validity (hard stops)

- **Zero checks:**
  - the observer and wrappers are read-only: state and random numbers identical with and without them, at 20 and 60
    years;
  - reload is exact.
- **Internal checks** (mismatch counters that must be 0):
  - a person counted at a stage for a kind was a non-knower of it when they first reached that stage;
  - "took" is recorded only when the learner's recipes gained that kind in that lesson;
  - every stage's set is contained in the stage before it.
- All 32 worlds are present under one fingerprint (`code_v7`).
- **An independent recompute by GPT and Gemini** (fresh chats, raw files, no analysis script) of Q2's step rates and
  largest loss, and of Q3's counts, before the findings are final.

## Sign-off (27 October 2026)

The creator: "yea draft the network audit, approve and freeze", on this plan (debate round 6: GPT's design, Gemini in
agreement). Frozen as `NA1-frozen` before any code or data. How the code reads choices the text leaves open goes in
operational notes, appended before any data.

## Operational note 1 (27 October 2026, after freezing, before any data)

How the code (`run_na1.py`) reads the text where it left a choice, found in a 20-year smoke world (seed 9953, not data):
1. **"Took" is exact.** A learner "took" a kind when that very kind (the lesson's meant kind) entered their recipes in
   the lesson. A lesson can come across wrong (`_recipe_as_shown`) and leave the learner with a different, new recipe.
   That is counted separately as **"took a variant"** and reported beside "took". LS1's "taken" counted any new
   recipe, so the two are not the same measure.
2. **A lesson implies talk and presence.** A learner offered a lesson is also counted as talked and co-present for that
   kind, since a lesson is given inside a talk within reach. The observer's weekly co-presence check reads positions at
   the week's end, after people have moved. So containment (talked ⊆ co-present, offered ⊆ talked) holds by
   construction; the check guards against coding errors.
3. **Founders' starting kinds** have no inventor. They are described, not in the primary readings. A kind becomes
   "useful" when its best factor exceeds 1.
4. **Ratchet improvement:** k is a part of k′ in k′'s recipe (bound parts, or the part heated). "Higher best factor" is
   over LS1's eight uses. "C learns k′" is any social route (taught, copied, read) by someone other than B.
