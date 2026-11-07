# FP1: food production by age in nature v15, against forager evidence (frozen plan)

**A read-only study,** HR1's step 0. Council round 72 was unanimous (`docs/debate_round72_fp1_design_2026-11-06.md`).
Evidence: `docs/research/forager_production_2026-11-06.md` (Kaplan et al. 2000, read in full; Koster et al. 2020).
Nothing in nature changes. **FP1 decides no law.** Its output is a table beside the evidence. From it the council picks
HR1's target: foraging too generous, hunting the gap, or the action budget. No pass/fail band is frozen (round 72,
GPT).

## Design
- **Code:** `code_v15` (fingerprint 3d46cd2c…), unchanged. One arm, no sham. LP (80 founders, 80 × 80).
- **Seeds 24301–24332** (32 new seeds, used by no study). 200 years; years 100–200 counted.

## The observer (read-only)
Every person-week, kept by age band (0–2, 3–7, 8–11, 12–15, 16–29, 30–39, 40–49, 50+) and sex. Food is held
food + seeds, in ACL's one food unit, where 1 = an adult-day's need.

**Production (new food):**
- **forage:** the `forage` event's `got`;
- **hunt:** the food each hunter actually received, read as the change in their food across `resolve_hunts`. This is
  meat received after the carry limit; the meat allocated, meat ÷ party, is kept beside it.

**Transfers in:**
- taken from one's own stash, and from another's (`take`);
- stolen from a person, and from a stash (`steal`);
- a gift received (`give`, receiver `b`);
- inherited (`inherit`);
- fed by a parent (read in `body_phase`).

**Losses and use:**
- **spoiled:** `body_phase`'s rot step, recomputed from the person's food, kept food, seeds and fire at that moment, by
  the code's own formula;
- **eaten:** the change in held food across the eating step;
- **fed to dependents:** the HF4 ledger's `fed_out`;
- **set down in a stash:** `_put`;
- **given:** a gift given;
- **stolen from them.**

**Also recorded:**
- **need:** `Person.need`, with unmet need (the deficit);
- **the week's action** (`p.doing`);
- **hunts by party size:** tried and successful;
- **forage and hunt options offered and chosen**, counted where the decision log allows (`decide` options).

## Zero checks (hard stops)
1. **Read-only:** world and random-stream hashes with and without the observer (20 and 60 years).
2. **Conservation (DeepSeek):** for every person-week in a 30-year world,
   held food at the week's end − at its start = production + transfers in − (spoiled + eaten + fed out + set down +
   given + stolen), within 1e-6. Any breach stops the study.
3. **Event check:** forage and hunt production summed by the observer equal an independent count from the events.
4. **Reload is exact.**
5. **All 32 worlds** are present under one fingerprint.

## Measures (all with population: person-weeks and people)
1. **Net production by age band and sex:** (forage + hunt) ÷ need per person-week, and (forage + hunt) − need. This is
   Kaplan's curve. The crossover age, where production first meets need, is read from it.
2. **Prime adults** (30–39 and 40–49) by sex: production ÷ need, **over all weeks** and **per active week** (forage
   or hunt).
3. **The hunted share** of production, and of all food acquired.
4. **The action budget** of the grown (16+): the share of weeks per action; forage and hunt offered, chosen and
   successful.
5. **Losses:** spoiled ÷ produced; unmet need by age band.
6. **Transfers:** each source's share of what children (under 16) receive.

## Evidence beside the table (Kaplan et al. 2000, read in full; shape, not level)
- Children produce less than they consume **until the mid-to-late teens**.
- Grown men produce well above their own intake: production ÷ per-capita intake 1.37–3.22 over eight societies.
  Women produce 0.39–1.64.
- The **hunted share of the diet is 26–78%** (median 68.7%).
- Hunting skill peaks about 33 (Koster et al. 2020).
- **Caveats:** ACL's need is a fixed requirement (adult 7, child 4, teen 6, elder 6 per week), not measured intake.
  Per-capita intake in Kaplan counts children as full consumers. So the comparison is of shape and direction, not of
  level.

## A blind recompute
GPT, Gemini and DeepSeek, from a per-world count file built by a script written before data. They recompute the
production ÷ need by age band and sex, the hunted share and the action budget.

## Prior (the assistant)
- **Prime adults' production ÷ need over all weeks** is about 1–2 for both sexes, with no sex difference: ACL has no
  division of labour by sex.
- **Per active forage-week it is about 3.**
- **Children (3–11)** produce little.
- **The hunted share is under 1%.**
- **Reading most likely:** "hunting the gap", about 70%.

## Sign-off (6 November 2026)
The assistant, under the creator's 2 November permission and their messages this evening: "keep working bro", and, in this
session, "yes download it, keep working bro", the OK to download Kaplan et al. 2000. Council round 72: GPT 97%, Gemini
95%, DeepSeek about 87%; the assistant 90%. Frozen as `FP1-frozen` before any code or data.
