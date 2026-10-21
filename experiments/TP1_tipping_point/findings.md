# TP1 — is there a tipping point in fertile women? Findings

Frozen as `TP1-frozen` before any analysis. Read-only: only saved control worlds were read, and no new runs were made.
Tables: `results_discovery.md` (committed before the holdout was read) and `results_holdout.md`, from `analyse_tp1.py`.
Extinction uses the rule every study uses (`analyse_nv2.died`).

## Validity

All worlds were present: 512 of 512 in discovery and 256 of 256 in the holdout. **Valid.**

## The frozen reading

| set | worlds | died out | W ≤ W* died out | W ≥ W*+3 died out | reading |
|---|---|---|---|---|---|
| Discovery (RT1b C + FX2 C) | 512 | 187 | 96% of 96 world-years (W = 0) | 24% of 2,034 | **W\* = 0** |
| Holdout (FX3 C) | 256 | 80 | 95% of 43 | 20% of 1,051 | **stands** |

**The frozen rule's tipping point is W\* = 0.** A world with no woman aged 16–45 at a check year almost always dies
out. The rule takes the smallest W that qualifies; W = 1 also meets both conditions in discovery (described, not
the reading).

**The prior (W\* = 3) was wrong** and is kept as written. At W = 3, about half of the world-years went on to die out
(55% in discovery, 48% in the holdout). That is far from "almost never recovers".

## Described

- **Above zero the curve is a slope, not a cliff.** In discovery, extinction falls from 90% (W = 1) to 74% (2), 55%
  (3), 42% (4), 31% (5), 22% (6), 15% (7), 12% (8) and under 10% from W = 9. That is roughly 10–20 points per
  extra woman. The holdout follows the same shape. Each extra fertile woman helps; there is no single number below
  which hope ends, except none.
- **Recovery at W = 0 is rare but real.** 4 of 96 world-years in discovery and 2 of 43 in the holdout came back.
  Girls grew into the age band.
- **Total population tells a similar story.** Worlds of under 10 people at a check year died out in 96–100% of
  cases. Worlds of 15–19 died out in about half (45% discovery, 51% holdout). Worlds of 35 or more almost never did.
- **Single fertile women with no eligible man alive** separate the worlds less than W does. In discovery, 31% of
  world-years with none died out, against 42–49% with 1–4. In the holdout it was 26% against 36–46%. These counts
  overlap with W, so neither is a cause shown here.
- This describes ACL's worlds under today's nature (v2). It does not show a threshold in real foragers.

## What it means for ACL

F1's warning sign ("at most three fertile women at year 30") marks a world at **high risk**: about half die. It
is not a world past saving. There is no sharp tipping point to aim at. Any help for small worlds would work along
the whole slope, and the partner pipeline (PF1, PF2) stays the place to look. TP1 proposes no change.

## Correction after GPT's review (21 October 2026; appended, the text above is kept)

GPT (`gpt_review_tp1.md`) called the reading "mostly fair" but raised three points: (1) W* = 0 is what the frozen
rule selects, not a shown biological threshold; (2) world-years are not independent (a world counts up to five
times, and later check years hold only survivors); (3) W is tangled with total population, so the slope is an
association, not the effect of adding a woman. A described audit followed (`results_audit.md`, `analyse_tp1.py
audit`; added after the frozen reading and holdout were committed; not part of the reading):

- **One row per world, each check year separately:** the same shape holds at every check year in both sets (for
  example, year 30 in discovery: W 0–1 died out 41 of 43, W 2–3 62 of 101, W 4–6 66 of 193, W 7+ 16 of 173).
- **Within bands of total population, W adds little.** Under 10 people, 96–100% died out whatever W was. At
  20–34 people, 9–19% died out, roughly flat across W. Only at 10–19 people is there a modest fall in discovery
  (87% at W 0 to 52% at W 7+). In the holdout that band is nearly flat (57–75%).

**So the sentence above "each extra fertile woman helps" is corrected:** the slope in W mostly tracks how many people
are left. Among worlds of the same size, the number of fertile women says little more. What carries the risk in
these worlds is small total size. TP1 shows an association in ACL's worlds, not a cause, and not a minimum viable
population for real people.
