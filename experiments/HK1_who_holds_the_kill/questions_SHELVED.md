**SHELVED (6 November 2026, 19:20), never frozen.** Council round 70, part 2, was unanimous. Read-only counts on
v14 found 0 party kills in 105 kills, and 1 pair in 713 hunt attempts, so this law would have nothing to act on.
**Revival condition** (DeepSeek, adopted): party kills reach a countable base (at least 50 in the smoke worlds), and
the live nature then contains the law's precondition. The first check comes after HR1 (hunting calibrated to
evidence) and a law for acting together on purpose. Record: `docs/debate_round70_hk1_design_2026-11-06.md`.

# HK1: who holds the kill (plan; to be frozen as `HK1-frozen`)

**A test of one law in a copy, with a sham.** It removes a hand limit: the forced equal split of a party's meat
(`actions.resolve_hunts`, `share = meat / n`). The law-limits council chose it first
(`docs/gpt_review_law_limits_2026-11-06.md`), and round 70 set the design (`docs/debate_round70_hk1_design_2026-11-06.md`).
It adds no outcome: sharing, keeping, theft and conflict are left to the choices people already have.

## Base nature
**The nature live at the freeze** (round 70: all three).
- If CI1-C confirms and v15 is adopted first, the base is `code_v15`; otherwise `code_v14`.
- The freeze names the version and its fingerprint, and nothing changes after the freeze.
- `code_hk1` = the base + one setting, `hold_kill` (0 = the base).

## The law (HK, `hold_kill` = 1)
- **Only party successes change.** When a party of two or more hunters on one tile succeeds, all the meat goes to one
  member: the one who lands it.
- **The lander is drawn** with weights equal to that member's own (0.5 + hunting skill) × hunt-tool factor, normalised
  in the party. These are the same factors the party's chance already uses.
  - The draw comes from **a stream of its own**, seeded from the world's seed, the week and the tile, as `util.tie_pick`
    does. It never touches the world's generator.
  - A zero total weight cannot occur, because 0.5 + skill > 0 and the tool factor is ≥ 1. A check asserts it.
- **The others get no meat from the hunt step.** Everything else is as in the base:
  - hide and bones are drawn by coin from the world's generator;
  - skill gain, watching, wear, injury and the bond bump;
  - the reward formula (0.3 × min(1, got / need) on a success), so a member who gets nothing gets 0;
  - the carry rule: the holder gets min(meat, carry room), and the rest is deleted as in the base. The loss is
    measured in every arm.
- **Solo hunts are unchanged** (n = 1).
- **The hunt option's expectation is unchanged:** the even-split `expected_take / n` (round 70: GPT and DeepSeek;
  Gemini dissenting). People have not been told the new rule.

## Arms
- **live:** the base.
- **HK:** `hold_kill` = 1.
- **sham:** the standard sham (one extra draw from the world's generator in week one). It also logs who would have
  landed each party kill, from the same separate stream. Its meat is split evenly.

**Seeds 24201–24232** (32 new paired seeds, used by no study). LP; 200 years; years 100–200 counted.

## Frozen decision rule
**Manipulation check (pre-registered).** Both must hold:
1. In HK, every party success gives all its meat that reaches anyone to the drawn lander. A unit check confirms this,
   and so does the run's log.
2. HK has at least POWER party successes in years 100–200, summed over its 32 worlds. POWER is set from the
   exploration before the freeze.

**Harm guards, HK against live.** CI1's eight, exactly:
- starvation deaths per 1,000 living-years: ratio above 1.25 with the lower bound above 1;
- killings per 1,000 living-years: difference above 0.05 with the lower bound above 0;
- adult health: difference below −5 with the upper bound below 0;
- living-weeks: ratio below 0.90 with the upper bound below 1;
- extinctions: 3 or more extra worlds;
- child deaths per 1,000 child-years: ratio above 1.25, the lower bound above 1, and a rise of 3 or more;
- child starvation per 1,000 child-years: ratio above 1.25 with the lower bound above 1;
- food gifts to kin's children per 1,000 adult-weeks: ratio below 0.80 with the upper bound below 1.

**Readings:**
- **supported:** the manipulation check passes, and no guard is raised;
- **harm:** any guard other than killing is raised;
- **killing only:** the killing guard is the only one raised, and HK's killings stay within the forager range (at most
  28% of all deaths, the top of the samples read). Then the reading is "killing rise within the forager range". It is
  neither adopted nor rejected automatically: **the creator decides**. This is a question of values. GPT: removing
  the limit and failing safety are separate conclusions. The creator has said life in ACL looks "too peaceful";
- **harm, killing beyond the range:** the killing guard is raised and killings exceed 28% of all deaths;
- **not informative:** the manipulation check fails.

**If any guard is raised,** the meat deleted at the carry limit is reported beside it (DeepSeek): is the harm
mechanical, food lost to deletion, rather than social? If it is mechanical, the next study is the kill-site stash (a
separate law), not a verdict on HK.

**A supported reading goes to a confirmatory run on new seeds before any adoption** (`CLAUDE.md`'s safe path).

## Described (not decisive; population beside each)
- **Meat:**
  - meat deleted at the carry limit, total and per party success;
  - meat per hunter-week, by skill rank;
  - inequality of meat over party successes of 2 or more;
  - the share of party kills landed by each skill rank (do the weights predict the lander?);
  - the same person landing again and again.
- **After a kill:**
  - the holder's food against the other members' over the next 2 weeks;
  - food gifts by holders within 2 weeks, and to whom (kin, partner, a party member, others);
  - chains of who got meat from whom;
  - hunger and starvation of hunters against non-hunters.
- **Conflict:**
  - thefts tried, successful and noticed;
  - thefts aimed at recent holders;
  - grudges formed;
  - attacks;
  - killings, also as a share of all deaths, beside the forager range;
  - injuries and deaths among holders, failed hunters and others.
- **Hunting:**
  - hunts per adult-year;
  - party size, and the share of hunts by parties;
  - whether the less skilled stop joining;
  - the unsuccessful hunters' next action;
  - trust and respect toward those who share.
- **CI1's context measures.**

## Validity (hard stops)
- **Zero checks:**
  - `code_hk1` at 0 = the base (20 and 60 years);
  - the observer is read-only;
  - HK and the sham act;
  - reload is exact;
  - the unit check: in an HK world, every party success's meat goes only to the drawn lander, and the separate stream
    leaves the world's generator untouched.
- **All 3 × 32 worlds** are present under one fingerprint.
- **A blind recompute** by GPT, Gemini and DeepSeek.

## The assistant's prior
To be written at the freeze, after the exploration.
