# PF1 — Why doesn't more contact help people find partners? (SIGNED OFF 20 October 2026; frozen as `PF1-frozen` before any code or data)

**Why.** MB1b (`../MB1_multi_band/findings_mb1b.md`, `MB1b-done`): splitting the same 80 founders into smaller bands made
lineages meet about four times as often and cross-lineage couples about eight times as common, yet the share of
fertile woman-weeks without a partner stayed at about 0.46 and births did not move. GPT's review
(`../MB1_multi_band/gpt_review_mb1b.md`) recommended a read-only audit of where partner finding fails, before any new
study. The creator approved going ahead with that audit (20 October 2026). **Read-only: nothing in ACL changes.**

## Questions

1. In the weeks a fertile woman has no partner, at which step of partner finding does it stop?
2. Does that step shift between P4 (4 bands of 20) and B16 (16 bands of 5), and does it explain why more contact left
   the blocked share unchanged?
3. (GPT's check 2) What exactly MB1b's measures count: their units and denominators, written down.

## How partner finding works today (read from `code_mb1b` = `code_v2` + one setting, 20 October 2026)

A couple forms only through `court` (`mind.py` options, `actions._court`):

| step | rule in the code |
|---|---|
| S1 **a match exists** | somewhere alive: an adult man, single, **unrelated** (`world.kinship` = 0: not parent, child, sibling, grandparent, aunt or uncle), born within 15 years of her, not her ward or guardian |
| S2 **in sight** | such a man within `perception + 2` tiles (a single adult with no one to court in reach walks toward one this close) |
| S3 **in reach** | within `reach` (3 tiles): only people this close are options at all (`people_near(p.loc, c.reach)`, the nearest 12) |
| S4 **not disliked** | her feeling for him above −0.2 (court is offered only then); likewise his for her |
| S5 **courting tried** | one of the two actually chose `court` with the other that week |
| S6 **accepted** | the one courted finds the other attractive enough (> 0.55) and a draw of 0.6 succeeds; then they pair |

## Design (the assistant's recommendation; decisions marked)

- **Unit:** a **fertile single woman-week**: a woman aged 16–45 with no partner at the end of a week, exactly the unit
  of MB1b's "blocked for want of a partner" (F1's probe: the share of woman-weeks aged 16–45 in which she has no
  partner). Each such week is assigned the **first step it fails** (S1 … S6).
- **Instrument (Decision 1):** a logging copy of `code_mb1b` (`code_pf1`) that records every `court` attempt and its
  result into a world attribute that is not saved and read by nothing (as CA2), plus a read-only weekly observer that
  checks S1–S4 from the world state at the end of the week. **Shown to change nothing**: state hash equal to
  `code_mb1b` with and without logging (seeds 501 and 601, 20 years, at 20 and 80 founders, both `founding_bands` 0 and
  16). Positions are read at the end of the week, so S2–S3 are as of then (an approximation, stated).
- **Worlds (Decision 2):** MB1b's own worlds, **replayed exactly** (each replay's final state hash must equal the saved
  one): arms **P4, B8, B16**; **discovery seeds 5301–5316, holdout 5317–5332** (96 worlds). Sham is left out (it only
  measures chance).
- **Computer:** two spare workers beside RT1b (about 7–8 hours).
- **Also written down (question 3):** the definitions and denominators of MB1b's described measures (blocked share,
  births per woman-year, between-lineage meeting, cross-lineage couples, lineages alive), from the observers' code.

## The frozen reading (proposed)

- For each arm, the **share of fertile single woman-weeks ending at each step** (S1 … S6), pooled over worlds, with
  population beside it (rule 18). **The bottleneck** is the step with the largest share; it counts only if it is the
  same step in discovery and holdout.
- **The shift (question 2):** each step's share in B16 minus P4, described (no test), in both sets.
- It locates where partner finding stops; it does not show that removing that step would save worlds.

## The assistant's prior (to be frozen at sign-off; held loosely)

The bottleneck is **S1, no match alive**: most blocked weeks have no unrelated single man of a suitable age anywhere,
because single men are few (most adult men already have partners or have died) and, in small lineages, many are kin.
Smaller bands move weeks from S2/S3 (no one in sight or reach) to S1, which is why more contact leaves the blocked share
unchanged. Second guess: S5, courting not tried, for women past their mid-thirties.

## Decisions for the creator

1. Instrument: **a logging copy shown to change nothing, plus a read-only observer** (recommended), or the observer only
   (cannot see court attempts, so S5 and S6 merge).
2. Worlds: **MB1b's P4, B8, B16, seeds 5301–5316 then 5317–5332, replayed exactly** (recommended), or all four arms
   (sham too; about 10 hours).
3. The prior above, frozen as written.
4. When: **now, on two spare workers beside RT1b** (recommended), or after FX2.

## Sign-off (20 October 2026)

The creator: "approve all recommendations, freeze it". So: (1) a logging copy shown to change nothing, plus a
read-only observer; (2) MB1b's P4, B8, B16 worlds, seeds 5301–5316 (discovery) then 5317–5332 (holdout), replayed
exactly; (3) the prior above, frozen as written; (4) now, on two spare workers beside RT1b.
