# HA1 — Why does handing stay rare? A read-only audit on live nature v11 (frozen plan)

**Read-only: no change to nature.** Live nature v11 (`experiments/NV11_nature_v11/code_v11`, the frozen copy of `acl/`).

## Why
- **Nature v11** (31 October 2026, adopted by the safe path): people can hand a made thing to one another.
- **HD1 and HD1-C:** handing adds a third to what tools add to food, a small effect. There were only **0.20 handings
  per adult-year**.
- **Why it stays rare** was the first open question on v11 (`research/state.json`).
- **Debate round 43** (`docs/debate_round43_handing_audit_2026-11-01.md`): both models chose this audit (GPT 96%,
  Gemini 92%). Both accepted the design below (GPT 97% with a hierarchical rule, adopted; Gemini 96%).
- **GPT:** "For Bob, transmitting knowledge matters more than transmitting optimistic values."

## How handing works in v11 (from the code: `acl/mind.py`, `acl/actions.py`)
- **When:** a person holding made things (up to 3) considers each of the up to 12 nearest people within reach.
- **Room:** if that person has room (fewer than 3 things), the thing with the highest **net** use is picked: the
  receiver's gain over their own best for any use, minus the giver's loss (`hand_pick`).
- **Value:** if net > 0, the handing value is net × **social**, where social = 0.25 × kindness + 0.6 × affection +
  0.6 × kin + 0.6 if partner + a payback term.
- **Competition:**
  - It replaces the food-giving value for that person only if it is larger.
  - It then enters the choice as a `give` option, scored like every option (utility + 0.6 × habit).
  - The choice is a softmax at temperature 0.2.

## The question
**Where does the handing funnel narrow:** in opportunities (handing options rarely exist), or in the choice (they
exist but are rarely chosen)?

## Design
- **Worlds:** live v11 (`code_v11`, unchanged). **32 new seeds 21601–21632**, LP (80 founders, 80 × 80), 200 years.
  Years 100–200 are counted.
- **Eligible decisions:** decisions that reach the choice (the softmax), made by a person holding at least one made
  thing, in years 100–200. Children are included and reported apart.
- **The observer** (read-only; it reads the options after `thought.steer`, as ES2's observer did) logs, for every
  eligible decision:
  1. **room:** someone among the decision's nearest-12 within reach has room;
  2. **net:** someone has net > 0 (`hand_pick`, a pure function);
  3. **option:** at least one handing option is among the options (a `give` option whose handing intent is set);
  4. **mass:** the choice's softmax probability mass on handing options (the same scores and temperature the choice
     uses; no random draw);
  5. **by relation:** the handing options and their mass, by kin (kinship > 0), partner or other;
  6. **scores:** the best handing option's score, against the top score among all options.
- **Also recorded:**
  - **every handing** (`hand` event) in years 100–200: giver, receiver, the thing's kind, the relation, and **whether
    the receiver already knew how to make that kind** (it was in their recipes);
  - **every making** (`make` event) in years 100–200: maker and kind;
  - a **yearly count of made things held,** by holder age (under 12, 12–15, 16–59, 60+).

## Primary (frozen)
- **E = the share of eligible decisions with at least one handing option.**
- **C = the mean softmax mass on handing options, over eligible decisions that have at least one.**
- Both are pooled over the 32 worlds, with 95% world-bootstrap intervals (10,000 resamples; NumPy seed 20261101).

## Frozen decision rule (GPT: hierarchical, mutually exclusive; applied to the pooled point estimates)
1. **Opportunity-limited:** E < 0.10.
2. **Choice-limited:** E ≥ 0.10 and C < 0.05.
3. **Neither:** otherwise.

## Secondary (described, not decisive)
- **The funnel:** the shares of eligible decisions at stages 1–3, the expected handings (the summed mass) and the
  handings done.
  - The expected and the actual handings should be close (a consistency check). Handing can fail at action time if
    the thing or the room is gone.
- **By relation:** the share of handing options, and of their mass, to kin, partners and others.
- **Scores:** the gap between the top option's score and the best handing option's score.
- **By giver's age:** children (under 12), 12–15, 16+.
- **Knowledge with the object** (GPT: "an association", not proof of transmission):
  - among receivers who did not know how to make the kind they received, the share who **made** that kind within
    5 years;
  - the same among receivers who already knew;
  - only handings at least 5 years before the end are counted.
- **Who holds made things,** by age group (yearly census).

## Validity (hard stops)
- **Zero checks:**
  - the observer is read-only: the world state and random numbers are the same with and without it (20 and 60
    years);
  - the observer's handing-intent reading matches the code's: every executed handing came from a decision the observer
    saw with a handing option to that receiver (mismatch 0);
  - every observed decision is counted once.
- **All 32 worlds are present** under `code_v11`'s fingerprint.
- **A blind recompute by GPT and Gemini** of E, C, their intervals and the reading, from per-world sums.

## The assistant's prior
1. **Choice-limited.** Handing options exist often (when people sit near kin), but they score low against food and
   rest: the handing value is a small net times a social weight.
2. **Most handing options and handings are to kin and partners.**
3. **Receivers who did not know the kind rarely make it** within 5 years (under 10%).

## Sign-off (1 November 2026)
The assistant, under the creator's sleep-mode autonomy (a read-only study under the 40% rule). GPT estimates 97%,
Gemini 96% and the assistant 80%. Frozen as `HA1-frozen` before any code or data.
