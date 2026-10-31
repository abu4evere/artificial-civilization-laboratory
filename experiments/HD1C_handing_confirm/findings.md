# HD1-C — The handing law, confirmatory run on new seeds. Findings (not final until GPT and Gemini recompute)

**The safe path's confirmatory step** for HD1 (`CLAUDE.md`). HD1's code (`code_hd1`, fingerprint 8217eac3…), arms,
runner and analysis, unchanged, on 32 new paired seeds (21301–21332). Frozen as `HD1C-frozen`. Run on GitHub Actions
(run 41241346782, `skip_zero=local`). 96 worlds; LP (80 founders, 80 × 80); 200 years.

`results.md` carries HD1's title because HD1's analysis is reused unchanged (`analyse_hd1c.py` only points it at these
seeds).

**Validity:**
- zero checks pass;
- all 96 worlds are present under one fingerprint;
- every forage replay is exact, and every handing conserves the item (mismatches 0).

**Population beside it:** no world died out in any arm. Mean living population, h ÷ v10, was 0.965 [0.860, 1.085]; the
sham's was 0.948.

## The answer

**Confirmed.** The handing law again raises what tools add to food, above the sham, with no harm flag.

| arm | R (share of adults' foraged food added by tools, years 100–200) |
|---|---|
| v10 | 1.03% |
| h (handing) | 1.28% |
| sham | 1.05% |

- **h − v10: +0.25 points** [+0.18, +0.34]. The sham's own difference is +0.02 [−0.06, +0.09].
- **By HD1's frozen rule: confirmed** (SUPPORTED).
- **Smaller than HD1's** +0.36 [+0.28, +0.45]. The two intervals overlap.

### Mechanism (described)
- **Handings:** 0.18 per adult-year (57,172 in years 100–200). **Reversals:** 0.01%.
- **Adult forage weeks with a tool in hand:** 10.4% → **13.7%**.
- **Recipients forage with a tool in 49.9% of their forage weeks** in the year after receiving one.
- **Food gifts per adult-year:** 5.56 → 5.41; the sham's is 5.30.

### No-harm flags (all not raised)
- **Population:** 0.965 [0.860, 1.085].
- **Food per adult:** 1.000.
- **Recipes per adult:** 0.995.
- **Food gifts:** 0.973 [0.913, 1.034].
- **Child deaths:** −0.00 per 1,000 child-years [−1.31, +1.32].
- **Extinctions:** +0.
- **Ping-pong:** 0.01%.

## What it means
- **Across both runs** (64 paired worlds), handing raises tools' share of food by about a third (+0.25 to +0.36
  points) and puts a tool in more hands, with no harm. **The effect is real and small.** Most of TR1's 20% headroom
  stays unused, because the choice to make (and to hand) is rare.
- **What follows, by the safe path in `CLAUDE.md`:**
  1. this run's blind recompute by GPT and Gemini;
  2. both models consulted on adopting the law as **nature v11**, with the assistant's estimate ≥ 40%;
  3. `code_v11` = `code_v10` with `hand_items` default 1, zero checks, hashes and tests, a tag and a Telegram
     message.
  The creator, on Telegram (31 October): "I think that law is fine."

## Independent recompute
Pending: GPT and Gemini, each in a fresh chat, from `recompute/hd1c_one_file.csv`. Recorded only from their actual
replies.
