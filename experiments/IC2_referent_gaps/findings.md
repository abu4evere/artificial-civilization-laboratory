# IC2 — Where is there a real information gap: water, game or danger? Findings (final: recomputed blind by GPT and Gemini; see the end)

Frozen as `IC2-frozen` (operational note 1; **operational amendment 1**: the first run, 40653330784, failed a hard stop
because the observer missed the surprised-bear route to a mauling; fixed before any outcome was read). Decided and
signed off in sleep mode (`docs/autonomous_decisions.md`). Read-only on nature v8 (`code_v8`). Run on GitHub Actions
(run 40664447201, `skip_zero=local`). 32 worlds (seeds 19801–19832; LP, 80 founders, 80×80), 200 years. Every number
comes from `analyse_ic2.py`, written before data; full tables are in `results.md`.

**Validity:** zero checks pass; all 32 worlds are present under one fingerprint (`code_v8`); the wrappers' counts match
the law's own events (talks, accepted game places, maulings; mismatches 0).

**Population beside it:** 1 of 32 worlds died out; mean living population 122.4; 771,678 person-years (474,848
adult-years).

## The answer

**None of the three referents is workable.** In ACL today there is no referent where a learned signal could both be
grounded (people attend to it together) and be useful (one person lacks it and today's mind would act on it).

| referent | shared moments per adult-year | in pairs with ≥ 5 | gaps per adult-year | **decision-relevant gaps per adult-year** |
|---|---|---|---|---|
| water | 4.05 [3.73, 4.36] | 0.870 | 0.05 | **0.000** (0 of 25,400 gaps) |
| game | 2.00 [1.76, 2.24] | 0.807 | 2.23 [1.87, 2.60] | **0.404 [0.340, 0.468]** (191,671 of 1,059,722) |
| danger | 0.02 [0.01, 0.02] | 0.332 | 0.00 | **0.000** (no gaps at all) |

The frozen screen needs at least 1 shared moment and at least 1 decision-relevant gap per adult-year, with 25% of
moments in repeated pairs:
- **Water** is grounded but never needed: every water gap was for a listener who already had a spring of their own.
- **Game** is grounded (2.00 per adult-year, 0.807 in repeated pairs) and has real gaps, but only 0.18 of them are
  decision-relevant (a hungry listener within 3 reaches). That makes 0.40 per adult-year, under the screen's 1.
  Gaps are mostly fresh: 0.55 come from sightings 0–4 weeks old.
- **Danger** is almost never seen together (0.02 per adult-year) and never seen by one and not the other. Talk happens
  between people within 1 tile, so they see almost the same square.

### Q4 — Today's game channel (described)
- **It does some real work.** 1,173,327 game places accepted (1,520 per 1,000 person-years). 0.071 [0.068, 0.075] of
  listener-places later become that listener's destination; 0.089 for spots out of sight at the telling.
- In all choices it is small: 0.0014 of chosen options go to a told game place (an upper bound). When they do, people
  reach the tile (0.988) and then see game (0.889).
- What is told is fresh: 0.911 of accepted game places come from the speaker's own sighting 0–4 weeks old; 0.085 are
  relayed.

### Q5 — Danger (described)
- 88 maulings in 32 worlds (0.11 per 1,000 person-years). **None** followed a danger gap about the same group. With no
  decision-relevant danger gaps, near misses cannot be measured.

## Against the prior (the assistant's, frozen)
1. "Game is workable and proposed": **wrong.** Game has the most decision-relevant gaps but falls short of the screen
   (0.40 against 1 per adult-year).
2. "Water's decision-relevant gaps near 0": **right** (0).
3. "Danger gaps rare and almost never followed by a mauling": **right** (none at all).
4. "More than 5% of accepted game places later become a destination": **right** (0.071).

## What follows (from the frozen branches)
- **"If none is workable: ACL today has no referent where a learned signal could both be grounded and be useful; the
  next question is the creator's (which law change would create a real need, judged against human evidence, not
  tuned)."** This branch holds.
- **Described, not a frozen reading:** the reason looks structural. People talk only when within 1 tile, so they see
  almost the same things; water is almost always in view; game is usually in view too (about 7 groups both see); and
  wolves and bears are rare. Information is abundant where people meet. The one real gap is game seen by someone who
  was away. It is the channel that already works, and it rarely meets a hungry listener close enough to act.
- **A game-signal study is still possible,** but by the frozen screen it would have little to carry. Whether to
  change a law so that information matters more (for example, calling across a distance, or what a person saw while
  away), judged against human evidence, is **the creator's decision**. Both models are to be asked first.

## Independent recompute
Pending: GPT and Gemini, fresh chats, raw per-world counts, the Q1 and Q3 numbers. Recorded only from their actual
replies.

## Independent recompute (28 October 2026)
GPT and Gemini, each in a fresh chat, worked from raw per-world counts only, without the analysis script
(`recompute_ic2.md`). **All three agree on every key number:** game 0.4036 decision-relevant gaps per adult-year
(shared 1.9962; repeated pairs 0.8071); water and danger 0; no referent workable.

**Final.**
