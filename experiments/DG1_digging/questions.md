# DG1 — Digging: what do people do when the ground can be opened? (Revision 1 after GPT's review; SIGNED OFF 23 October 2026 on the creator's instruction; frozen as `DG1-frozen` before any data)

**Why (the creator, 23 October 2026):** "make diggin possible ... make these things possible for their nature ... do
all these things i told you". Order agreed: bodies (done, now nature v4), then digging, then water. GPT's ideas
(`../BD1_bodies_stay/gpt_ideas.md`) and review of the draft (`gpt_review_dg1.md`).

A **Law 126 study** on **nature v4**: one setting, `digging`, default 0 = v4 exactly.

## The candidate (Revision 1: only hiding and keeping food, as GPT advised)

**Digging is gathering earth.** ACL's people learn a value per action; a new action would change every person's
table even with digging off. So earth is offered as one more thing to gather, only when `digging` is 1, with the same
pull as any material (curiosity, the pull of the new, and any use found). *Digging therefore shares the learned value
of gathering in general: an intended coupling, documented (GPT).*

1. **Where:** dry land that is not rock (rock below 0.6) and not frozen hard (a week colder than a hard winter's).
2. **A week of digging** deepens the pit there by 0.6 (about knee-deep by hand) times the best hard tool's factor
   (as for stone). Assumption.
3. **A pit fills back in** slowly: each week depth × 0.99 − 0.005; gone below 0.05. Assumption.
4. **Food set down in a knee-deep pit** (depth at least 0.5) by a living owner:
   - **keeps longer:** it rots at `pit_keep` = 0.5 of v4's rate (arm D), or 0.75 (arm DW, the sensitivity check
     GPT asked for). Assumption, not a measurement;
   - **is hidden:** another person sees it (and can take it, v4's rule) only if they remember a placement there, or
     the pit was dug in the last four weeks (turned earth shows), or the owner is dead.
5. **Nothing else:** no rainwater, no bodies in pits (both later), no wish to dig, no storage or burial rule.

## Design

- **Code:** `code_dg1` = `code_v4` + `digging`, `pit_keep` + read-only logging (`v4_to_dg1.diff`).
- **Arms:** C (v4), D (`pit_keep` 0.5), DW (`pit_keep` 0.75). **Seeds: 512 new, 13001–13512**; 20 founders, 120
  years; 1,536 worlds on GitHub.
- **Zero checks (hard stops):** `digging` 0 = `code_v4` (seeds 11 and 501 at 5 years, 501 and 601 at 20); D acts;
  observers and logging change nothing; reload exact (with a pit held).
- **Manipulation check (hard stop):** pits are dug in at least half of D's worlds.
- **Safety (the adoption rule), D against C:** survival (sign test, bootstrap, yardstick ±0.117); time-averaged
  population (lower bound above −5% safe). DW is reported the same way.
- **Described:** digs, diggers, digs by decade, food set down in pits (times, amount, people), pits at the end,
  starvation deaths, population.

## The adoption rule (fixed now, before any data)

Digging is **proposed for nature (v5)** if the manipulation check passes and D's survival and population are not
worse. Then the creator decides.

## The assistant's prior

- Pits are dug, mostly early, out of curiosity; digging fades once it is no longer new, because a pit gives nothing
  by itself.
- **Food is rarely or never set down in a pit**: it happens only if someone stores food where they once dug, by chance.
  So D and DW will look almost the same.
- Survival and population: no meaningful effect.

If so, DG1 says something real: **a possibility is not a use.** Storage in the ground needs a reason to dig there,
first.

## Sign-off (23 October 2026)

The creator, before going out: "do all these things i told you" (bodies, digging, water), and earlier "i like ur way".
Taken as sign-off of DG1 after GPT's review; adoption stays the creator's decision.

## Operational note (23 October 2026, while building, before any data)

- A throwaway check (seeds 9971–9973, 20–30 years, not data) first used a depth of 0.12 per dig: no pit ever reached
  knee-deep, because each filled back in before the next dig. The depth was raised to 0.6 (a week's digging by hand)
  before any data. With 0.6: 30–50 digs per world in 30 years, almost all in the first decade; no food set down in a
  pit. Nothing else was changed after it.
