# Council round 72: FP1, food production by age, before the freeze (6 November 2026, 22:38)

**Opinions of GPT, Gemini and DeepSeek, not sign-off.**
- **The question:** `docs/debate_round72_question_2026-11-06.md` (the same paragraph to all three).
- **The chats:** GPT, the main chat ("Instant"); Gemini, chat 87f468c684ee5839; DeepSeek, chat 2552dbba (read from
  screenshots).
- **Recorded from the replies read in the chats.**

| | GPT | Gemini | DeepSeek |
|---|---|---|---|
| 1. FP1 before HR1? | **Yes**: calibrating hunting alone risks compensating for a wrongly scaled food economy | **Yes**: raising hunting without auditing foraging could remove scarcity | **Yes**: HR1's target is ambiguous, and calibrating before knowing which quantity is off risks tuning |
| 2. measures to add | **Keep new production apart from transfers** (stash, gifts, theft and inheritance only move food); record actual food eaten, unmet need, spoilage and stock changes; food eaten while foraging; forage and hunt options offered, chosen, successful and their returns; children's own production; meat allocated against meat received | **actual consumption and food lost to rot**, beside need; meat and plant food in one unit; failed actions in the action budget | **a conservation identity as a zero check**: food acquired by source = eaten + stored + rotted + lost + given away, per person-week. Also: is forage yield gross of food eaten that week; production ÷ need per active week and per all weeks; split 30–49 into 30–39 and 40–49 (Koster's peak at 33); children's foraging, stash and inheritance apart from production; hunts tried and successful by party size |
| 3. evidence and comparability | Koster for the hunting age profile only. **Do not freeze numerical bands from search summaries.** Production ÷ need is comparable to kcal produced ÷ consumed only if the units carry consistent energy and the accounting boundaries match. **Freeze the measurement protocol, not pass/fail bands** | Kaplan for the crossover age (net consumer to net producer) and the peak; the denominator should be actual consumption, waste included | Koster for the age profile, Kaplan for the production ÷ need shape, Hadza and Aché for hunting returns. **Comparable in shape, not level**; use bands, not point targets; report gross and net side by side |
| 4. estimate | **97%** | **95%** | **about 87%** |

## Checked (the assistant)
- **ACL has one food unit:** meat from a hunt is added to `p.food` like foraged food (`actions.resolve_hunts`), so
  meat and plant food already share a unit. Gemini's point holds by construction. The *hunted share* is a share of
  food units, not of energy (DeepSeek's caveat).
- **What FP1 must still trace in code before the freeze:**
  - how eating draws on held food each week;
  - where held and stashed food rots (`weather.py` touches stashes);
  - whether foraging eats on the spot.
  - The conservation identity (DeepSeek) depends on these.

## Merged plan (to be frozen after the code trace)
- **Read-only on v15,** one arm, 32 new seeds 24301–24332, 200 years, years 100–200.
- **Production** (forage, hunt) is kept apart from **transfers** (stash, gifts, theft, inheritance).
- **Consumption and losses** are recorded beside need: eaten, rotted, lost, unmet need, stock change.
- **Zero check, the conservation identity:** acquired = eaten + Δstock + rotted + lost + given, per person-week.
- **Production ÷ need,** per active week and per all weeks.
- **Age bands** 0–2, 3–7, 8–11, 12–15, 16–29, 30–39, 40–49, 50+, by sex.
- **The action budget,** with offered, chosen and successful forage and hunt counts, and hunts by party size.
- **The output is a table beside the evidence. No pass/fail bands are frozen** (GPT). The council reads it and picks
  HR1's target. The comparison is in shape (the crossover age and the peak), not in absolute energy.
