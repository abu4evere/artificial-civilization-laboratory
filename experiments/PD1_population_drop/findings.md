# PD1 — Why does population fall when made things persist? Findings (recompute by GPT and Gemini pending; not yet final)

Frozen as `PD1-frozen` (operational note 1); decided and signed off in sleep mode (`docs/autonomous_decisions.md`).
Read-only, on OP1's code (`code_op1`). Run on GitHub Actions (run 40606901380, `skip_zero=local`). 192 worlds: c (v7),
o (things drop), x (sham), on the same **64** paired seeds (19401–19464). LP, 200 years. Every number comes from
`analyse_pd1.py`, written before data; full tables are in `results.md`.

**Validity:**
- zero checks pass;
- all 192 worlds are present under one fingerprint;
- founders + births − deaths = living at the end, in every world (mismatches 0).

## The answer

**With twice as many paired worlds, the population fall does not repeat.** OP1's flag was most likely chance. No
cause of death and no birth rate differs between o and c beyond what the sham shows.

### Q1 — The exact split of the gap in final population (summed over 64 paired worlds)
- **Living at year 200:** c 7,323, o 7,101, x 6,995.
- **The gap:**
  - **o − c: −222 [−900, +485]** (−3%);
  - **the sham's own gap, x − c: −328 [−1,041, +345],** larger than o's.
- **Every component's interval includes 0** (`results.md`):

  | component | o − c |
  |---|---|
  | births | −909 [−3,244, +1,504] |
  | deaths from illness | +568 [−254, +1,386] |
  | deaths from violence | −8 [−53, +36] |

- By the frozen rule, the component with the largest share is **births** (share 4.09). But the gap is small and
  uncertain, so the shares are not meaningful. The sham shows the same pattern (births −1,998).
- **Described for comparison with OP1's flag:** mean population in years 100–200 is c 129.8, o 127.9, x 124.2. The
  ratio o ÷ c is **0.985** (OP1 had 0.845); the sham ÷ c is 0.957. Extinct: c 0, o 1, x 0.

### Q2 — Rates (per 1,000 person-years)

| rate | o − c [95%] | x − c [95%] |
|---|---|---|
| births per 1,000 woman-years | +1.58 [−1.28, +4.38] | +1.47 [−1.58, +4.53] |
| all deaths | +0.21 [−0.23, +0.65] | +0.19 [−0.23, +0.58] |

- **No cause-specific death rate differs:** hunger +0.23, illness −0.11, violence +0.01 (all intervals include 0).
- **One age band, teens, is just outside:** +0.77 [+0.05, +1.52] per 1,000 teen-years. With 14 rates tested, one
  interval excluding 0 is about what chance gives. Described, not claimed.

### Q3 — Fighting
- **People more often fight with a tool in hand:** 0.593 of attacks against 0.400 (**+0.193 [+0.147, +0.238]**; the
  sham −0.013).
- **But fights are not more frequent or deadlier:**
  - attacks per 1,000 adult-years −0.23 [−0.55, +0.12];
  - killings +0.01 [−0.02, +0.05];
  - the kill rate with a tool +8 [−8, +23] per 1,000 attacks.

## Against the prior (the assistant's, frozen)
1. "Violence carries the largest share of the gap": **wrong.** There is no violence effect (−8 deaths).
2. "More attacks with a tool in hand, with a higher kill rate": **first part right** (0.40 → 0.59), **second not
   shown.**
3. "Births change little": **right** (the rate +1.6, interval includes 0).

**Gemini's expectation** (weapon access turning disputes lethal) is **not supported.** **GPT's caution** about the sham
and baseline variation is borne out: OP1's 15% drop sat inside the range a trivial change produces.

## What follows (from the frozen branches)
- **"o's differences are inside the sham's band: the OP1 flag was chance. OP1 can be reconsidered with this evidence,
  which is the creator's decision."** This branch holds.
- **For the creator:** OP1's law (made things drop instead of vanishing, and are picked up) was supported on its
  mechanism. Its population flag does not repeat with 64 paired worlds. **Whether to adopt it as nature v8 is the
  creator's decision**, after this study's recompute. The adoption path would then be:
  1. both models consulted;
  2. `code_v8` with zero checks;
  3. the tests;
  4. a `nature-v8` tag.
