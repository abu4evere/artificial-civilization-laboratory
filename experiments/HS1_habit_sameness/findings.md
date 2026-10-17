# HS1 — Why are everyone's habits alike? Same world, or same nature? Findings

Frozen as `HS1-frozen` (16 October 2026; two operational fixes before any data, recorded in `questions.md`). Read-only
replays of TC1's worlds (code `code_tc1`, arms W and N, seeds 501–516 and 601–616, 80 years). Table: `results.md`, from
`analyse_hs1.py`. Asked by the council (Gemma 4); run at the creator's request.

## Validity

Zero check PASS (the observer leaves both arms' worlds unchanged); all 64 replays present; every world (32 of 32 in each
arm) has children reaching 20 and a stranger from another world. **Valid.**

Population first (rule 18): **1,182 children reached 20 in N** (median 31 per world) and **1,197 in W** (38); 25 and 26 of
32 worlds alive at year 80.

## The frozen reading: mostly nature

A child's habits at 20, against three others (Pearson correlation over the whole habit table; medians over worlds, 95%
bootstrap intervals):

| arm | parents | stranger, same world | stranger, **another world** | nature share (other ÷ same) |
|---|---|---|---|---|
| **N (no copying)** | 0.923 [0.903, 0.929] | 0.839 [0.797, 0.869] | **0.838** [0.820, 0.861] | **0.998** [0.982, 1.016] |
| W (today) | 0.938 [0.925, 0.948] | 0.872 [0.850, 0.884] | 0.880 [0.850, 0.888] | 1.005 [0.988, 1.026] |

**A stranger from a different world is exactly as like a child as a stranger from the child's own world** (N: Wilcoxon
p = 0.75; the nature share's whole interval lies between 0.98 and 1.02). **Frozen rule: "mostly nature".** The same holds
with today's copying (W).

## What it means

1. **Sharing this world adds nothing measurable** to how alike unrelated people's habits are. Not the map, not the
   neighbours, not the history: a person from another island chain, who never met anyone in this one, is as alike.
2. **What makes strangers alike is what every world shares**: the rules, the body, the kind of land (islands, seasons,
   the same foods) and the structure of the habit table itself (situations nobody meets stay near zero for everyone).
   HS1 cannot separate these (written in advance as its caution); together they are "nature" here.
3. **Families still matter, on top.** Parents' habits are closer than any stranger's (0.92 against 0.84 in N): what
   parents pass on at birth and in upbringing is real and specific.
4. **This sharpens TC1.** TC1 found that most of the sameness survives with no copying, and suspected "the world everyone
   shares". HS1 shows which part: not this world, but the nature all worlds share. Copying in talk (W against N) raises
   every correlation a little (0.84 → 0.87 with strangers), as TC1 found.

## Described, not explained

The stranger correlations here (W 0.87) are lower than BL0's 0.92, measured on the same code and kind of world. The
designs differ (80 against 120 years; tables read at the end of the birth week; 32 of the 64 seeds), and HS1 does not say
which difference accounts for it. Both studies agree on the order: parents above strangers, and strangers very alike.

## The assistant's prior, against the result

| prior (frozen) | result |
|---|---|
| mostly nature: other-world strangers above 0.9 of same-world strangers | **right**: 0.998 |

## What it decides

Nothing in nature changes. For the open question of talk (TC1): whatever form copying takes, it is not why everyone is
alike; the shared nature is. A world in which people's habits differed more would need differences the rules let people
live in (places that demand different lives), not less copying.
