# CO1 — What made the other options stronger? Findings

Frozen as `CO1-frozen`; run on GitHub Actions (run 40393405585, the first run with `skip_zero=local`). 32 worlds on
nature v7, LP (80 founders, 80×80), seeds 18401–18432, 200 years. Every number comes from `analyse_co1.py` (written
before data); full tables are in `results.md`.

**Validity:**
- the zero checks pass;
- all 32 worlds are present under one fingerprint (`code_v7`);
- the identity (U_other = Σ s·habit + Σ s·T·ln n + Σ s·per-entry score + spread) held in every logged week, and the
  family log-sum-exp equals the direct one (mismatches 0);
- the split of the change is exact to 2 × 10⁻¹⁶.

**Population:** people within reach of an adult when making was offered rose from 7.5 (years 0–5) to 15.3 (years
100–200). The choice to make, when offered, fell from 0.0262 to 0.0011.

## The answer

**Habits.** The other options grew stronger because people's learned habits for them grew, not because there were more
options, and only partly because their built-in pull rose.

### Q2 — The exact split of the rise in U_other (adults, matched; years 0–10 against 100–200)
U_other rose 1.302 → 1.962, **Δ +0.660 [0.647, 0.672]**:

| part | Δ | share of the rise |
|---|---|---|
| **habit** | **+0.569 [0.559, 0.577]** | **0.86** |
| per-entry score (built-in pull and the thought's) | +0.130 [0.105, 0.154] | 0.20 |
| multiplicity (more option entries) | +0.013 [0.004, 0.021] | 0.02 |
| spread (the choice divided among more families) | −0.052 | −0.08 |

**The part carrying the largest share: habit.**

By family:
- **gather:** +0.28 (habit +0.08, per-entry +0.21);
- **forage:** +0.23 (habit +0.27);
- **put:** +0.15 (per-entry +0.10);
- **talk:** +0.08;
- **give:** +0.07.

### Q3 — Counterfactual swaps (each world's own early values; diagnostic)
Making's mean log-odds fell from −5.41 to −8.62 (a fall of 3.21). In the late period:

| set back to its early value | share of the fall undone |
|---|---|
| **habits** | **0.86** |
| per-entry scores | 0.23 |
| entries (option counts) | 0.02 |
| all three | 1.16 |

Grouping every family to one entry barely changes things: −5.08 early, −8.23 late.

### Q1 — Which families
- **Gathering's share** of the competing weight rose most (0.03 → 0.18), and **putting things down** rose too (0.03 →
  0.10). Both gained built-in pull (gather 0.24 → 0.88, put 0.20 → 0.56) as well as habit.
- **Foraging** stayed the largest share (0.47 → 0.40), with its built-in pull unchanged at each hunger level, but its
  habit rose from 0.06 to 0.65.
- Social families gained entries (talk 6.9 → 9.9, give 6.4 → 9.6), but multiplicity added only 0.013.

### Q4 — Habits by bin (described)
The habit term for every common action rose steadily over 200 years:

| action | habit term, years 0–5 → 100–200 |
|---|---|
| forage | 0.04 → 0.65 |
| give | 0.03 → 0.79 |
| talk | 0.02 → 0.54 |
| join | 0.00 → 0.40 |
| gather | 0.00 → 0.35 |
| put | 0.00 → 0.26 |

**Making's own habit stayed near zero** (MK1: 0.0004 → 0.03).

## Against the prior (Claude's, frozen)
1. "Habit carries the largest share, over half, mostly in forage, gather and talk": **right** (0.86; forage the largest
   habit part).
2. "Multiplicity is measurable but under a quarter, mostly in social families": **right** (0.02, mostly talk and give).
3. "Swapping habits undoes more of the fall than swapping entries": **right** (0.86 against 0.02).
4. "Gather's share rises most": **right** (0.03 → 0.18).

**The debate's predictions:**
- GPT and Gemini: utilities carry more than multiplicity, with multiplicity contributing measurably. **Right on the
  first, and multiplicity was small.**
- Gemini first said the artefact risk was "extremely high"; it withdrew that before the data, and the data agree it was
  not.

## Reading (interpretation, not tested here)
Habit values grow for actions that are done and rewarded, and spread by copying in talk. An action that is rarely
chosen, like making, never builds a habit, so it falls further behind every year: **a rich-get-richer loop in the
learned habits.** That fits MK1 (making's worth unchanged, its habit near zero) and LS1 (making falls at the choice). It
is not shown here whether the rise comes mainly from people's own rewarded experience (TD learning) or from copying
whole habit tables in talk (C4). That is the next question.

## What follows (frozen branches)
- **Habits carry it:** next, which learning drove them, TD from rewards or copying in talk (C4), as its own read-only
  study. Fly-brain step 3 (how values are learned, on which timescale) becomes relevant.
- **Per-entry scores carry a fifth,** mostly gathering and putting things down: which inputs raised them (material wants
  and the worth of materials, warmth from piles) is a secondary question.
- **Multiplicity is not the cause** (0.02). More neighbours do not by themselves crowd out making, so the giving and
  watching candidates would not be undone by adding options.

## Independent recompute
Pending (GPT and Gemini, fresh chats). Recorded in `recompute_co1.md` before these findings are final.
