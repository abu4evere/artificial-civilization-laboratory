# H1 — How far apart are partners' homes? (read-only feasibility check, rule 12; questions frozen before any data)

**Chosen by the creator (October 2026), after N6.** No fixes, no tuning, no code changes.

## Why

N6: real forager couples share a camp each night; ACL's couples share no home. Candidates: L1 (make the two thresholds
agree), L2 (a shared home base), L3 (a pair bond at any distance). Rule 12: before any design, check what the world
already does. If partners' personal homes already lie close together, a smaller change (L1) may suffice; if not, L2.

## The code, read before any data

A person's **home** is the tile with the highest remembered wellbeing among the places they remember (`person.py`,
`home()`; `knowhow.feel_place`: each week's wellbeing updates the value of the tile where it was spent, other places fade
by 0.5% a week; at most a fixed number of places are kept). It may be none, changes when another place comes to stand
out, and is not shared with a partner. People are drawn toward their home when it is within reach and remembered as
better than where they are.

## Questions

1. **Distance between partners' homes**, in couple-weeks (woman 16–44 with a living partner, both with a home): share
   within 2 tiles (conception distance), 3, 4–6, 7 or more.
2. **Where partners are relative to their own homes:** share of partner-weeks at home (same tile), within 2, further.
3. **When couples are apart** (more than 2 tiles), how often are both partners within 2 tiles of their own homes (apart
   because their homes are apart), and how often is at least one away from home?
4. **How stable homes are:** share of person-weeks in which a person's home changed; share of couple-weeks with either
   partner homeless.

## Decision rule (frozen now; read on discovery and holdout separately)

- If partners' homes are within 2 tiles in **at least two thirds** of couple-weeks in both sets: homes are already shared
  in effect; **L1 is the plausible smaller change**.
- If within 2 tiles in **at most one third** in both sets: partners' homes are separate; **L2 (a shared home base) is
  needed** if co-residence is to be anchored.
- Otherwise: **mixed**; reported as such, and the creator decides.

## Worlds

Control code (`E13R_replication/code_e13r`, A2-full, defaults), first 40 years. Discovery seeds 501–516, holdout seeds
1101–1116 (the C1 seeds). Couple-weeks and population reported. Hard stops: observer read-only (state hash, two seeds,
20 years); replays reproduce F1's populations for years 10–40; code fingerprint unchanged.
