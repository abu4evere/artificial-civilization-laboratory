# MO1 — The memory order: should a learned recipe enter memory with its value? (frozen plan)

**A nature-change study: one law, frozen, with a matched control and a sham.** Chosen in sleep mode
(`docs/autonomous_decisions.md`, 27 October 2026). Both GPT (90%) and Gemini (95%) chose it first after PT1 (debate
round 10, `docs/debate_after_pt1_2026-10-27.md`).

**Adoption is not decided here.** GPT advised "do not adopt v8 without the creator's explicit decision", so whether to
make it live is left to the creator, even though sleep mode would allow it.

## The defect (PT1, final)

When someone takes a recipe from another person, the code does two things in this order:
- `knowhow.remember_recipe` adds the recipe with value 0 and, if memory holds more than 12, deletes the lowest-valued
  recipe;
- only **then** does the caller give the recipe the value that learning carries:
  - a lesson (`information.hear_how`): max(own, 0.5 × claim × credence);
  - watching (`knowhow.watch`): max(own, 0.3 × outcome).

PT1 found that in 71.4% of lesson-caused overflows the deleted recipe is the new lesson itself. In a one-event replay
with the value set first, 95.7% would survive, and what would go instead is worth about 0.01.

## The law tested (`code_mo1` = `code_v7` + one setting, `lesson_value_first`, default 0 = v7 exactly)

**`lesson_value_first = 1`:** a recipe learned from someone (taught, or copied by watching) is given the value that
learning carries **before** the memory decides what to keep. The value and the rule for deleting are the same numbers as
v7; only the order changes.

Learning by making, heating or reading marks is unchanged: those paths set no value in the same event. The principle
(GPT's wording) is "complete the learning event before evaluating what memory to retain", not "protect new knowledge".

## Arms (32 paired seeds, 18901–18932; LP: 80 founders, 80×80; 200 years; run on GitHub)

| arm | setting |
|---|---|
| **c** | v7 (`lesson_value_first` 0) |
| **o** | `lesson_value_first` 1 |
| **s** | sham: v7 with `sham_draw` 1, one extra draw from the world's random stream in week one. It measures how far a world drifts from any small change, as the yardstick for the descriptive outcomes |

## Logged (read-only observer: a wrapper on `knowhow.remember_recipe`, weekly events, a yearly census)

**For every recipe learned from someone (taught or copied):**
- the time, the kind, how it was learned, and whether it overflowed memory;
- **at an overflow:**
  - whether the new recipe survived;
  - the deleted recipe's value;
  - whether it was a useful kind (LS1's definition);
  - whether its holder had made it in the previous 52 weeks.
- **52 weeks later** (censored if the learner died):
  - whether it is still held;
  - whether it was found bad (value below −0.1);
  - whether the learner made it.

**The yearly census:**
- the living population and adults;
- recipes held per adult, and **useful recipes held per adult**;
- making events per adult-year;
- the distinct world-born kinds held by anyone alive.

## Questions and the frozen decision rule

- **M (manipulation check).** The share of learning-caused overflows in which the new recipe survives. **Passes** if
  arm o ≥ 0.90 and arm c ≤ 0.40.
- **P1 (primary: retention).** Of recipes taken by a lesson or by watching, the share still held 52 weeks later
  (learners alive then), o against c. Paired by seed; world bootstrap, 10,000 replicates. **Supports** if the 95%
  interval of o − c is above 0.
- **P2 (no harm: knowledge kept).** Useful recipes held per adult (yearly census, years 50–200), o against c. **No harm**
  if the lower 95% bound of (o − c) is above −5% of c's mean.
- **P3 (no harm: reliability).** Of recipes taken, the share found bad within 52 weeks, o against c. **No harm** if the
  upper 95% bound of (o − c) is below +0.02.
- **D (described, not decision criteria).** Each against c, with the sham's difference from c beside it as the yardstick:
  - what is deleted instead: its value, and how often it is a useful kind or one made in the past year;
  - relearning;
  - making per adult-year;
  - world-born kinds alive at 200 years;
  - population;
  - extinction.

**The change is supported** if M passes, P1 supports, and P2 and P3 show no harm. Then GPT and Gemini recompute
blind and are consulted on adoption. **Adoption as nature v8 is left to the creator**, as above. Making, population and
cumulative culture are **not** adoption criteria, so as not to tune towards an outcome.

## What would follow (stated now)
- **Supported:** a candidate v8 with one corrected order, for the creator's decision. It does not address making's
  collapse at the choice (PT1: 12 of 19,472 chains).
- **M passes but P1 does not:** new recipes survive the overflow but are lost later anyway. Memory turnover, not order,
  limits retention. Described.
- **Harm on P2 or P3:** the order protects new lessons at the cost of established or reliable knowledge. Not
  supported.

## The assistant's prior
1. M passes: o about 0.95, c about 0.29.
2. P1 supports: retention at 52 weeks rises by at least 0.15.
3. P2: useful recipes held per adult change by less than 5% (no harm).
4. P3: no harm.
5. Making per adult-year changes little (within the sham band).

## Validity (hard stops)
- **Zero checks:**
  - `code_mo1` with `lesson_value_first` 0 equals `code_v7` (state and random numbers, 20 and 60 years);
  - the observer is read-only in arm o;
  - the setting acts (o differs from c);
  - the sham acts;
  - reload is exact in arm o.
- **The observer's predicted deletion matches the code's actual deletion** in every overflow, in every arm (a mismatch
  counter that must be 0).
- All 96 worlds are present; each arm has one code fingerprint.
- An independent recompute by GPT and Gemini (fresh chats, raw files, no analysis script) of M, P1, P2 and P3 before
  the findings are final. A recompute is recorded only from numbers read from the reply.

## Sign-off (27 October 2026)
The assistant, under the creator's sleep-mode autonomy (CLAUDE.md, Sleep mode). Both models chose this study (GPT 90%,
Gemini 95%); the assistant's estimate is 80%, above the 40% threshold. Logged in `docs/autonomous_decisions.md`. Frozen
as `MO1-frozen` before any code or data. How the code reads choices the text leaves open goes in operational notes,
appended before any data.
