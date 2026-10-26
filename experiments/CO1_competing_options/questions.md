# CO1 — What made the other options stronger? (frozen plan)

**Read-only on nature v7. No change to nature.** It follows MK1 (final, recomputed by GPT and Gemini). Within matched
states, the log-odds of choosing to make when offered fell 3.12 from years 0–10 to years 100–200. The other options'
soft maximum (U_other, 1.30 → 1.94) carries 1.03 of that fall, while making's own score did not change. Debate round 5
(`docs/debate_what_first_2026-10-27.md`): GPT and Gemini both chose this study first, before any nature change. Its
design is GPT's, made exact by the identity below.

## The question

Why did the other options' combined pull rise? Three kinds of explanation:
- **more options** (as more people are near, each adds give, talk, court and other entries);
- **stronger learned habits** for other actions;
- **higher built-in scores per option** (needs, ecology, the thought's pull).

Also: how evenly the choice is spread, and which kinds of action.

## The exact identity (written before data)

In a week where "make" is offered, every other option entry j has a final score U_j (after the thought's pull), and
the softmax draws with temperature T = 0.2. Group the entries by action family a (forage, gather, put, take, rest,
play, explore, hunt, give, care, talk, court, steal, attack, flee, join, heat, fill). For each family:
- **n_a** = its number of entries;
- **L_a** = T · log Σ_{j∈a} exp(U_j / T), the family's soft score;
- **h_a** = learned_weight × the habit value for that action in the week's situation, the same for every entry of the
  family;
- **M_a** = L_a − h_a − T · ln n_a, the family's **per-entry score**: built-in utility plus the thought's pull, averaged
  softly over its entries.

So L_a = h_a + T · ln n_a + M_a, exactly. With **s_a** = exp((L_a − U_other) / T), each family's share of the competing
weight:

**U_other = Σ_a s_a · h_a + Σ_a s_a · T · ln n_a + Σ_a s_a · M_a + T · H**, where H = −Σ_a s_a ln s_a (the spread).

This holds exactly in every week. Means over weeks therefore split exactly into four parts:
1. **habit;**
2. **multiplicity** (the number of entries);
3. **per-entry score;**
4. **spread.**

Each part also splits by family.

## Logged (read-only observer; the same wrapper as MK1, on `thought.steer`)

For every person-week (teen and up) in which "make" is offered, summed into MK1's matched-state cells (bin × hunger
band × holding a forage tool × food on the tile; adults and teens apart):
- offered, chosen, U_m, U_other;
- for each family: present, s_a, s_a·h_a, s_a·T·ln n_a, s_a·M_a, n_a, h_a, M_a;
- T·H.

**Within-world counterfactuals** (diagnostic calculations only; nothing in the world is changed). At the end of year
10, each world's early means of n_a, h_a and M_a, by matched state and family, are kept. For every later week in which
make is offered, the observer recomputes U_other and the probability of choosing make with one part swapped back to
that world's early value, for the families present that week. The swaps:
- **(i)** entries;
- **(ii)** habits;
- **(iii)** per-entry scores;
- **(iv)** all three together;
- **(v)** "grouped": every family counted as one entry (n_a = 1), the same week's other values kept. This is done in
  early weeks too.

## Questions (by MK1's bins up to 200 years; worlds alive at each bin's start; population beside every measure)

**Q1. Which families?** By bin: each family's mean share of the competing weight (s_a), mean entries, habit and
per-entry score. Which families gained share.

**Q2. The exact split (primary).** Early (years 0–10) against late (years 100–200), adults, matched as in MK1 (late
weighted to the early distribution of offered weeks). The change in mean U_other is split exactly into habit,
multiplicity, per-entry score and spread, each also by family. **The part carrying the largest share is named.** World
bootstrap (10,000 replicates).

**Q3. The counterfactuals.** In years 100–200, the mean log-odds of choosing make with each swap (i)–(iv). Each is
reported as the share of MK1's fall (early to late mean log-odds) it would undo. The grouped probability (v) is
reported early and late, beside the actual. The swaps interact, so their shares need not add up.

**Q4. Where it comes from (described).**
- For the families carrying the change: their habit values by bin.
- The forage family's per-entry score by hunger band.
- The number of people within reach by bin.

## What would follow (stated now; not exclusive)

- **Multiplicity carries the largest share** (or swap (i) undoes most of the fall): the decision gives more weight to
  social options as more people are near. Next: an evidence-led review of how the choice set is represented (one option
  per person against one per action) as a question about nature's design, for the creator.
- **Habits carry it:** learned values for other actions rose. Next: which learning drove them (TD from rewards, or
  copying whole habit tables in talk, C4), as its own read-only study. Fly-brain step 3 becomes relevant.
- **Per-entry scores carry it:** built-in needs or ecology changed. Next: which inputs (food, materials, warmth, thirst,
  the thought's pull), and an evidence review of whether ACL's needs are anchored.
- **Spread carries it:** the choice became more evenly divided among more kinds of actions.

## The assistant's prior (separate predictions)

1. **Habit carries the largest share** of the rise in U_other (over half), mostly in forage, gather and talk.
2. Multiplicity carries a measurable but smaller share (under a quarter), mostly in social families.
3. Swap (ii) (early habits) undoes more of the fall than swap (i) (early entries).
4. Gather's share of the competing weight rises most (MK1: gather winning 0.03 → 0.15).

**On record from the debate:** GPT and Gemini predict that rising utilities carry more than multiplicity, with
multiplicity contributing measurably. They did not split habit from built-in utility.

## Validity (hard stops)

- **Zero checks:**
  - the observer is read-only: state and random numbers identical with and without it, at 20 and 60 years;
  - reload is exact.
- **The identity holds** in every logged week, to within 10⁻⁹ (a mismatch counter that must be 0). The observer's
  U_other equals MK1's definition (the same check).
- All 32 worlds are present under one fingerprint (`code_v7`).
- **An independent recompute by GPT and Gemini** (fresh chats, raw files, no analysis script) of Q2's split and its
  largest part, and of Q3's swap (i) and (ii) shares, before the findings are final.

## Setting

Nature v7, LP (80 founders, 80×80), 32 new seeds (18401–18432), 200 years, run on GitHub.

## Sign-off (27 October 2026)

The creator: "yea draft it, approve and freeze", on this plan (debate round 5's choice, GPT's design). Frozen as
`CO1-frozen` before any code or data. How the code reads choices the text leaves open goes in operational notes,
appended before any data.
