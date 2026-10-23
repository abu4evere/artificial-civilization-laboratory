# GR1 (frozen as G1) — a first season of grace: findings

Frozen as `G1-frozen` before any data, after GPT's review (`gpt_review_g1.md`). A Law 126 study. Tables:
`results.md`, from `analyse_g1.py` (written and committed before data). Code: `code_g1` = `code_v3` +
`first_season_grace` (`v3_to_g1.diff`). 512 worlds: 256 new seeds 9501–9756 × C (v3) and G (a recipe first held
less than 13 weeks ago is not the one dropped), 20 founders, 120 years. **Run on GitHub's machines** (`cloud-run`,
run 39886787053). Zero checks passed there and on this PC.

## Validity

- Zero checks passed. All 512 worlds are present, with one fingerprint.
- **Manipulation check passes:** useful inventions still held by their inventor 13 weeks later, median C 0.539,
  G 1.000 (p = 9.6e-44).

**Valid.**

## The frozen reading

**Primary, transmission** (share of useful inventions ever learned by someone else): medians C 0.110, G 0.113.

| G − C, mean | 95% interval | Wilcoxon p | reading |
|---|---|---|---|
| +0.0043 | [−0.0000, +0.0085] | 0.037 | **changes transmission (G higher)** |

**Survival check:** C died out in 99 of 256, G in 98 (35 saved / 34 lost; p = 1.0; C − G +0.004 [−0.059, +0.070]):
**no meaningful effect.**

**The adoption rule, fixed before data:** the manipulation check passes, transmission reads "changes transmission"
with G higher, and survival is not worse. So **G may be proposed for adoption into nature (v4)**, if the creator
accepts the evidence.

**The prior was partly wrong.** The direction was right, but the size was smaller than expected: +0.4 points, not
+1 to +2. More teachable recipes were dropped than expected (below).

## Beside it (described; population first)

| arm | median population, year 60 / 119 | died out | recipes held per person | weeks a useful invention stays with its inventor | built on by a learner | longest chain | children's useful inventions passed on |
|---|---|---|---|---|---|---|---|
| C | 22 / 18 | 99 | 8.78 | 660 | 2,941 | 13 | 4,086 of 62,776 |
| G | 20 / 16 | 98 | 8.80 | 817 | 4,559 | 15 | 4,394 of 64,970 |

**GPT's diagnostics (described):**
- **The cost:** in G, 162,538 drops were displacements (an older recipe went instead of a new one); 6,160 of them
  (0.9 per 100 person-years) removed a recipe its holder valued above 0.15, so one they could have taught. The
  fallback (all 12 new) never happened.
- **The pathway** (useful inventions; steps counted separately): held at 13 weeks 53.7% → 99.5%; made again by the
  inventor 5.3% → 5.9%; valued above 0.15 by the inventor 19.0% → 43.8%; offered in a lesson 19.9% → 32.2%;
  learned by someone else 11.4% → 11.7%.

## What it means (the assistant's reading; not a frozen test)

- **G passes its frozen rule, but narrowly and with a small effect.** The interval touches zero; +0.4 points is
  about a 4% relative rise. It is the smallest effect that has met an adoption rule in ACL.
- **The pathway shows where the gain is lost.** Grace works at the memory stage (99.5% kept) and the valuing stage
  (more than twice as many valued enough to teach) and the offering stage (32% offered, up from 20%). Yet learning
  barely moves (11.4% → 11.7%). **The bottleneck has moved from memory to the lesson itself:** offered inventions
  are mostly not taken up.
- **Population ran lower in G** (median 16 against 18 at year 119), though survival did not differ. An exploratory
  check, not planned, labelled as such: G's population at year 119 was lower in 107 seeds and higher in 80 (sign
  test p = 0.057; mean −2.5 people). Not shown, but worth checking before adoption: the displaced recipes might
  have been ones that mattered for living (for example carriers or tools in daily use).

## Next (for the creator)

The rule allows proposing G for nature v4. Given the small effect, the interval touching zero and the lower
population, **the assistant recommends a confirmation before adoption** (as LX1 confirmed LM1): G against C on new
seeds, with population as a frozen check alongside survival. The alternative is to adopt now by the rule as
written. The creator decides.

## Note on the name (appended 22 October 2026)

This study was planned, frozen and run as **G1**, but that ID already belonged to an earlier study
(`experiments/G1_who_receives`, and its tags `G1-questions` and `G1-done`). It is renamed **GR1** in the index,
roadmap, decisions and book. Nothing else changes. Its folder, code and runner keep the name `G1` (the cloud run
used those paths). Tag `G1-frozen` and the new `GR1-frozen` both mark this study's frozen plan (232f0ed);
`GR1-done` marks these findings. The old `G1-done` still belongs to the earlier study.
