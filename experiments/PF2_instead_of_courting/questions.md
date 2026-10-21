# PF2 — What do people do instead of courting? (DRAFT, 21 October 2026; for the creator's sign-off)

**Why.** PF1 (`../PF1_partner_pipeline/findings.md`, `PF1-done`): in about half of the weeks a fertile woman is single, a
suitable man is within reach and neither of them courts (S5, "not tried"), in every arm and both sets. PF1 could see
that `court` was not chosen, not what was chosen instead or whether courting was even among the options. GPT's review
(`../PF1_partner_pipeline/gpt_review_pf1.md`) put this audit first. The creator approved going ahead (21 October
2026). **Read-only: nothing in ACL changes.**

## Questions

1. In S5 weeks, was courting the suitable man **offered** to her (or to him) at the moment of deciding at all?
2. If it was offered: **what won instead**, and how much chance did courting have (its share of the choice)?
3. If it was not offered: **why not**, by the code's conditions for the option?

## How a weekly choice works today (read from `code_mb1b`, 21 October 2026)

Each week a person scores every option (`mind.decide`): forage, eat, drink, rest, talk, give, care, court, explore,
join, play and others, then picks one at random with chances weighted by score (`softmax_pick`, temperature 0.2).
`court` toward someone is an option only if both are adults of opposite sex, unrelated (`kinship` 0), within 15 years in
age, neither is the other's ward, both are single, her feeling for him is above −0.2, and **he is among the nearest 12
people within reach (3 tiles) at that moment**. The world already records each decision's top four options and the one
chosen (`week_decisions`), but not the full list, so courting can be offered and still be invisible there.

## Design (the assistant's recommendation; decisions marked)

- **Instrument (Decision 1):** a logging copy of `code_mb1b` (`code_pf2`) that records, for every decision by a single
  adult, the full option list after scoring (action, aim, score) and the chosen one, into a world attribute that is not
  saved and read by nothing (as PF1 and CA2). It draws no random numbers. **Shown to change nothing** (state hash equal
  to `code_mb1b` with and without logging; seeds 501 and 601, 20 years, 20 and 80 founders, P4 and B16). PF1's weekly
  observer is reused unchanged to find the S5 weeks.
- **Unit:** an S5 woman-week as PF1 defined it, with the suitable men within reach at the end of the week.
- **Classification of each S5 week (first that applies):**
  - **O1 offered to her:** her options included `court` toward one of those men; record what she chose and courting's
    share of the choice (its softmax weight among all her options);
  - **O2 offered to him only:** not offered to her, but one of those men had `court` toward her among his options;
    record what he chose and courting's share;
  - **N not offered to either:** record the first failed condition for her and for him (not within reach at the moment
    of deciding; outside the nearest 12; feeling at or below −0.2; age or kin; a ward; no decision made that week).
- **"What won instead":** the chosen action, grouped as **subsistence** (forage, eat, drink, hunt, fish, store, sow,
  dig), **rest**, **other social** (talk, give, care, play, teach), **movement** (explore, join, flee, travel), and
  **other**.
- **Worlds (Decision 2):** MB1b's own worlds replayed exactly (final state hash equal to the saved one): **P4 and B16
  only**, **discovery seeds 5301–5316, holdout 5317–5332** (64 worlds). B8 sat between them in PF1.
- **Computer (Decision 4):** two spare workers beside FX2 and LM1 (several hours).

## The frozen reading (proposed)

- **Q1:** the share of S5 weeks that are O1, O2 and N, per arm, pooled, with population beside it.
- **Q2:** among O1 and O2 weeks, the share won by each group, and the median share of the choice courting had.
  **"What wins"** is the group with the largest share; it counts only if the same in discovery and holdout.
- **Q3:** among N weeks, the share at each first failed condition.
- Described, no test. It shows what the code chose; it does not show that changing a rule would save worlds.

## The assistant's prior (to be frozen at sign-off; held loosely)

Courting is usually **offered** (O1 or O2 in most S5 weeks), and it loses to **subsistence** (foraging and eating):
courting's score falls with hunger, and most weeks people are at least a little hungry. Courting's median share of the
choice is small (under 10%). Second guess: when not offered, it is mostly because he was not within reach at the moment
of deciding (positions at the end of the week overstate nearness).

## Decisions for the creator

1. Instrument: **a logging copy of the full option list, shown to change nothing** (recommended), or only the top four
   options the world already records (courting may then be invisible when it was offered but ranked low).
2. Worlds: **MB1b's P4 and B16, seeds 5301–5316 then 5317–5332, replayed exactly** (recommended), or add B8 (96 worlds).
3. The prior above, frozen as written.
4. When: **now, on two spare workers beside FX2 and LM1** (recommended), or after LM1.
