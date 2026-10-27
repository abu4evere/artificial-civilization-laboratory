# OP1 — Objects in the world: made things drop instead of vanishing (frozen plan)

**A nature-change study: one law, frozen, with a matched control and a sham.** Chosen in sleep mode
(`docs/autonomous_decisions.md`, 27 October 2026), after HC1. Both GPT (80%) and Gemini (95%) chose it. It was also
both models' first or near-first concern in the review of all 38 laws (`docs/gpt_review_laws_v7_2026-10-27.md`).
GPT's design is adopted (debate round 14, `docs/debate_after_hc1_2026-10-27.md`). **Adoption is left to the
creator.**

## The problem (code and TF1, final)
- **A person carries at most 3 made things (`item_limit`).** When a 4th is made, the least valued is **deleted**
  (`actions._keep`). TF1: 12.4% of things made in play vanished the same week.
- When kin inherit tools from a body over the limit, the extra are deleted too (`bodies_week`, oldest first).
- **Made things can never lie in the world.** They exist only in hands or on a body.

## The law tested (`code_op1` = `code_v7` + one setting, `ground_items`, default 0 = v7 exactly)

**`ground_items = 1`:**
1. **Drop, not delete.** Whenever the carry limit removes a made thing (in `_keep`, and in inheritance from a body),
   that thing is **left on the ground** where the person stands, unchanged (its kind, properties and remaining uses).
2. **Picking up.** Each week, after bodies, a person aged 12 or older standing on a tile with things on the ground,
   **with room in their hands** (fewer than 3 made things), picks them up:
   - one at a time;
   - the one they value most first (their own learned worth of its kind; ties broken by the order the things were
     left);
   - until full.

   People are taken in id order. This draws no random numbers.
3. **Things on the ground do not rot or wear while lying there.** The same is true of tools on a body today (BD1).

**No new number is introduced.** The age (12, the end of childhood) and the room (`item_limit`) are existing settings.
Nothing in choosing changes: picking up is passive, like kin taking tools from a body.

## Arms (32 paired seeds, 19301–19332; LP: 80 founders, 80×80; 200 years; run on GitHub)

| arm | setting |
|---|---|
| **c** | v7 (`ground_items` 0) |
| **o** | `ground_items` 1 |
| **x** | sham: v7 with `sham_draw` 1 |

## Logged (read-only observer; the law emits `drop` and `pickup` events, only when on)

- every drop: who, where, when, the kind;
- every pick-up: who (the one who dropped it, or someone else), and weeks on the ground;
- things still on the ground at the end;
- the yearly census: living population and adults; made things held per adult;
- extinction.

## Questions and the frozen decision rule (GPT's, adopted)

- **M (manipulation).** Arm o has drops, and no made thing is deleted by the carry limit (counted from the events and
  the ground list). In arm c the same overflows are counted as deletions. **Passes** if arm o has at least one drop in
  every world with an overflow, and zero carry-limit deletions.
- **P (primary: the mechanism).** Of the things dropped in arm o, the share later picked up by a living person (pooled
  over worlds). **Supports** if at least 0.05, with the world-bootstrap 95% lower bound above 0.
  - GPT: "a proposed practical minimum, not a scientifically established value".
  - It is not set from a replay. Things picked up by **someone other** than the one who dropped them are reported
    beside it.
- **H (no harm; flags, not gates).** Mean population in years 100–200, o against c. Flagged if below 0.90 × c, or if
  o has 3 or more extinct worlds beyond c. A flag blocks any recommendation to adopt.
- **D (described).** For each, the sham's difference from c is shown beside it:
  - things on the ground at year 200 (accumulation);
  - weeks to pick-up;
  - made things held per adult;
  - making per adult-year.

**The change is supported** if M passes and P supports. Then GPT and Gemini recompute blind and are consulted.
**Adoption is left to the creator.** More inventions or more making are **not** criteria.

## What would follow (stated now)
- **Supported:** a candidate v8 law (things persist), for the creator's decision.
- **Things persist but almost nobody picks them up** (P fails): the world now allows it, but people's lives do not bring
  them to those tiles with room in their hands. That is a finding about the decision system (GPT: "that negative
  result tells us something important").

## The assistant's prior
1. M passes.
2. P supports: 10–40% of dropped things are picked up, mostly by the one who dropped them, after a tool wears out.
3. No harm flags.
4. Things accumulate on the ground over time (more dropped than picked up).

## Validity (hard stops)
- **Zero checks:**
  - `code_op1` with the setting 0 equals `code_v7` (state and random numbers, 20 and 60 years);
  - the observer is read-only in arm o;
  - the setting acts;
  - the sham acts;
  - reload is exact in arm o (the ground is saved and restored).
- **Conservation in arm o:** dropped = picked up + still on the ground (a mismatch counter that must be 0).
- All 96 worlds are present under one fingerprint.
- An independent recompute by GPT and Gemini (fresh chats, raw files) of M and P before the findings are final. A
  recompute is recorded only from numbers read from the reply.

## Sign-off (27 October 2026)
The assistant, under the creator's sleep-mode autonomy (CLAUDE.md, Sleep mode). Both models chose it (GPT 80%, Gemini
95%); the assistant's estimate is 75%, above the 40% threshold. Logged in `docs/autonomous_decisions.md`. Frozen as
`OP1-frozen` before any code or data.

## Operational note 1 (27 October 2026, after freezing, before any data)

How the code (`code_op1`, `run_op1.py`, `analyse_op1.py`) reads the text where it left a choice, found in 20-year
smoke worlds (seed 9937, all arms; not data):
1. **The law.**
   - `actions._keep` takes the world; with the setting on, an overflowed thing goes to `world.ground` (with where,
     when, by whom) and a `drop` event is emitted.
   - Inheritance overflow in `bodies_week` does the same.
   - `actions.ground_week` runs every week right after `bodies_week`.
   - The ground is saved in the world's state only when non-empty, so v7 worlds are unchanged.
   - Diff: `v7_to_op1.diff`.
2. **"Picked up by a living person"** counts `pickup` events. "By someone other" means the picker is not the one who
   dropped it.
3. **The manipulation** counts carry-limit overflows from making through a read-only wrapper on `actions._keep`. In
   arm o each overflow must add exactly one thing to the ground. Inheritance drops come from the events.
4. **The census** runs at year ends: living people, adults (16+), made things held by adults, and `make` events that
   year.
5. **Seeds:** 19301–19332, the same in every arm.
6. **A label slip (no effect on any check).** The zero log's wording "eviction-prediction mismatches" was carried over
   from MO1's runner. In OP1 that field counts the observer's drop and conservation mismatches (`drop_missing`,
   `conservation`), and both are 0.
