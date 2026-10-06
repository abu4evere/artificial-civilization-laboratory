# C1 — Why do couples drift apart? (read-only; questions frozen before any data)

**Chosen by the creator (October 2026), after F2.** No fixes, no tuning, no code changes. Rules 12, 14, 15, 16, 18.

## Why

F2: with partners found perfectly, women 16–45 spent **46%** of their weeks with their partner out of reach (beyond the
code's `camp_radius` of 2 tiles, where conception is impossible); in the control worlds (F1) **20%**. Real forager
couples live together (Hill et al. 2011: co-residence of spouses is the norm). Before asking what to change, map why
ACL's couples are apart.

## The code, read before any data (what moves people; what holds partners together)

- **Foraging:** each person scores their own tile, their home, and six random tiles within `reach` (3), and goes to the
  best. Partners choose separately (`mind.py`, Forage).
- **The only pull toward a partner:** a "join" option toward loved ones **beyond reach (more than 3 tiles)**, scored
  (0.2 + 0.6 × loneliness × sociability + 0.5 × kinship + 0.6 for a partner) × max(affection, 0.2) × (1 − 0.5 × hunger)
  (`mind.py`, `_far_people`). Partners within 3 tiles feel no pull.
- **A gap between the two thresholds:** conception needs partners within 2 tiles; the pull back starts beyond 3. At a
  distance of exactly 3, a couple can neither conceive nor is drawn together.
- **Competing pulls:** home (the best-remembered place), water, kin, fire, animals heard of, exploration.
- Courting a partner (which raises affection) is possible only when they are within perception (4).

## Questions

1. **How far apart are couples when they are apart?** Distribution of distance in apart couple-weeks: exactly 3 (the
   gap), 4–6, more than 6; how long apart spells last.
2. **Who moves away, and doing what?** For each week a couple goes from together (≤ 2) to apart: which partner's move
   made the distance, and the action that partner chose (forage, join, explore, gather, hunt, other).
3. **When apart beyond reach, is the pull there, and what beats it?** In couple-weeks with distance > 3: share of
   partner-weeks in which any "join" option was among the four top-scored options; the action chosen instead; the
   partners' affection for each other and hunger.
4. **How do couples come back together?** For apart → together weeks: the action of the partner who closed the gap.
5. **Who is apart more?** By the woman's dependants (small children or none), season, couple's years together, and
   affection.

## Worlds

Control code (`E13R_replication/code_e13r`, A2-full, defaults), the setting F1 found 20% apart in. **Discovery:** seeds
501–516, first 40 years. **Holdout:** seeds 1101–1116, first 40 years, run only after the discovery write-up is
committed. Couple-weeks counted: a woman 16–45 with a living partner. Population reported beside every measure.

## Hard stops

- The observer must be shown read-only (state hash with and without it, two seeds, 20 years).
- Replays must reproduce the saved populations of F1 for the decades run (years 10–40).
- Code fingerprint unchanged.

## What would count as an answer

A share of apart couple-weeks attributable to each named cause (the 3-tile gap; foraging choices; other pulls; weak
pull beyond reach), stated only as far as the data allow, and repeated on the holdout before being called a finding.
No change is proposed by C1; anything proposed afterwards follows rules 12 and 17 and the creator's sign-off.
