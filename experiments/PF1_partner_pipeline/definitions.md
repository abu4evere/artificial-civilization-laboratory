# PF1, question 3: what MB1b's described measures count

Read from the observers' code on 20 October 2026 (F1's `Probe` in `experiments/F1_baseline_fragility/run_f1.py`;
MB1a's `Lineages` in `experiments/MB1_multi_band/run_mb1a.py`; pooled in `analyse_mb1b.py`). Asked by GPT's review
(`../MB1_multi_band/gpt_review_mb1b.md`, check 2). Nothing here changes MB1b's numbers; it says what they are.

| measure in MB1b | unit | numerator | denominator | pooled how |
|---|---|---|---|---|
| **blocked for want of a partner** (≈ 0.46) | woman-week | weeks in which a woman aged 16–45 (`fertile_from`–`fertile_until`) has **no partner** at the end of the week (the first of the code's conception conditions she fails is "no partner"; a pregnant woman counts as "pregnant", not here) | all weeks lived by women aged 16–45 | summed over all worlds of the arm, years 0–119, then divided |
| **births per woman-year** | woman-year | births | weeks lived by women aged 16–45, ÷ 52 | as above |
| **between-lineage meeting per adult pair-year** | adult pair-year | pairs of adults (16 and over) of **different founding lineages** who were within `perception` (4 tiles) of each other at the end of at least one week in the year | pairs of adults of different lineages alive together in that year | counted per year in each world, summed over years and worlds, then divided |
| **couples across lineages** | couple formed | `pair` events whose two people belong to different founding lineages | all `pair` events | summed over the run (cumulative: every couple formed, not a snapshot) |
| **lineages alive at the end** | world | distinct founding lineages among the living at the last decade mark (lineage follows the mother) | — | median over worlds of the arm |

Notes. A founding lineage is a founding band and everyone descended from it through mothers. The blocked share counts
**weeks**, not women: a woman single for ten years adds 520 weeks. It is a share of time, so it can stay flat while
couples change partners, form across lineages, or form sooner and end sooner.
