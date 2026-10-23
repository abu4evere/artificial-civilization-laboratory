# MR1 — Remembering by use, not by slots: does it let inventions survive long enough to be taught? (SIGNED OFF 22 October 2026; frozen as `MR1-frozen` before any data)

**Why (the creator chose cumulative culture as the next bottleneck, 22 October 2026).**
- CA1: only about **10%** of useful inventions are ever learned by anyone else.
- CA3: **99%** of the inventions lost before any lesson were pushed out of a person's memory **by the 12-recipe limit,
  within a season**. A brand-new recipe starts valued at 0, so it is the first to go when a 13th arrives. 80% of the
  lost ones were made by children.
- LM1: changing *which* recipe the limit drops did nothing. Teaching a missing part helped a little (now in nature v3).

The limit itself was never tested. The evidence note (`../CA3_opportunity/evidence_memory.md`) and GPT's review agree
that **the 12-slot limit is an implementation choice, not a fact about people**. Skill memory fades **gradually with
disuse**: almost no loss soon after learning, a large loss after more than a year unused (Arthur et al. 1998,
meta-analysis of 53 studies, mostly laboratory and training). MR1 is a **Law 126 study**: one candidate change to
nature, tested like LM1 and LX1. Nothing is adopted by MR1 itself.

## The candidate (one setting, default = nature v3)

| setting | v3 | candidate | the change |
|---|---|---|---|
| `memory_by_use` (U) | 0 | **1** | Recipes are no longer pushed out by a 12-slot limit. Instead, a recipe is **forgotten when it has not been used for 2 years**: not made, taught, learned again or valued by experience. A safety cap of 60 recipes (the existing general `memory_capacity`) applies only if ever reached. The existing rule that forgets recipes found useless stays. |

**Why 2 years:** the meta-analysis shows large losses after more than a year of non-use. "2 years unused" is a simple,
deterministic stand-in (no random draws), chosen before data and never retuned. **It is exploratory, not measured** in
ACL's units.

**Not a candidate:** a bigger slot limit (24 or 48). It keeps the "slots" idea the evidence argues against. It may be
added as a described comparison arm if the creator wants a dose check (Decision 2).

## Design (the assistant's recommendation; decisions marked)

- **Code:** `code_mr1` = `code_v3` + `memory_by_use` (default 0 = v3 exactly). "Last used" is stored inside each recipe
  record, so saved worlds carry it.
- **Arms:** C (v3) and U. **Seeds: 256 new, 9201–9456**; 20 founders, 120 years; 512 worlds on GitHub.
- **Zero checks (hard stops):**
  - setting 0 equals `code_v3` (seeds 11 and 501 at 5 years, 501 and 601 at 20 years);
  - U acts;
  - observers change nothing;
  - reload is exact.
- **Manipulation check (hard stop):** in U, the share of new useful inventions still held by their inventor 13 weeks
  later rises against C (paired Wilcoxon, p < 0.05).
- **Primary (transmission):** CA1's link 3, the share of useful inventions ever learned by someone else, U against C,
  paired. Wilcoxon, mean difference with a 95% bootstrap interval. Readings as LM1: "changes transmission",
  "no meaningful effect" (interval inside ±0.02), "not shown".
- **Survival check (as LX1):** extinction, U against C, paired sign test, bootstrap, yardstick ±0.117.
- **Described:**
  - recipes held per person;
  - how long inventions stay with their inventor;
  - chains of building on others' inventions (CA1 link 5);
  - the longest chain;
  - the share of useful inventions made by children that are passed on.

## The adoption rule (fixed now, before any data)

U may be **proposed for adoption into nature (v4)** only if all of these hold:
1. The manipulation check passes.
2. Transmission reads "changes transmission" with U higher.
3. Survival is not worse ("no meaningful effect", or fewer worlds dying out).
4. The creator accepts the evidence.

Otherwise it is not adopted. As GPT advised, a gain is a consequence; the reason for adopting is that memory by use is
more like people than memory by slots.

## The assistant's prior (to be frozen at sign-off)

- The manipulation check passes easily: inventions stay with their makers much longer.
- **Transmission rises, but modestly** (by about 3–5 points on a base of about 9%). CA2 found more limits after
  memory: inventors are rarely in teaching talks with a learner, and composites need parts.
- Survival: no meaningful effect.

## Before freezing (the research rule)

GPT is asked for objections and better candidates; the answer is recorded beside this plan. The sources are checked
and labelled.

## Decisions for the creator

1. The candidate: **memory by use, 2 years unused** (recommended), as described.
2. Arms: **C and U only** (recommended), or add a described "24 slots" arm as a dose check (768 worlds).
3. Seeds: **256 new (9201–9456)** (recommended), or 512.
4. The adoption rule and the prior, as written.

## Sign-off (22 October 2026)

The creator: "yes approve all and run it on github". So:
- the candidate, memory by use with 2 years unused;
- two arms, C and U (no "24 slots" arm);
- 256 new seeds (9201–9456), 512 worlds on GitHub;
- the adoption rule and the prior, as written.

**GPT's review was not obtained before freezing.** The research rule asks for it; the browser did not respond when
the question was sent, and the creator wanted the study started before their computer went off. GPT is to be asked
after launch, and its answer recorded beside this plan as a review of a frozen plan: any point it raises can change
only what is described, through an appended note, never the frozen tests.

## Operational note (22 October 2026, while building, before any data; rule 19)

How the plan is put into code (`v3_to_mr1.diff`). Nothing else changes.
- **"Last used"** is kept per person (`recipe_used`, the week each recipe was last used), saved with the world only
  when held, so v3's worlds are unchanged. A recipe counts as used when it is made from a known recipe, made new,
  learned or re-learned (taught, copied, read, heated), taught (including a part shown by parts-first), or felt in use
  (`judge_item`).
- **Forgetting** runs with the existing seasonal check (every 13 weeks, after `forget_useless`): a recipe unused for
  104 weeks or more is forgotten. It draws no random numbers.
- **The limit** in U is the general `memory_capacity` (60) instead of 12; the drop rule at the cap is v3's.
- **Measures:** link 3 and "built on by a learner" (CA1's link 5) come from LM1's `summarise`, unchanged. "Held 13
  weeks later" counts useful inventions whose inventor was alive 13 weeks on; an inventor who died sooner is left out.
  "A child's invention" is one whose inventor was under 16 when inventing it. The longest part chain counts made
  parts below a useful kind (a kind with no made parts is 1).
