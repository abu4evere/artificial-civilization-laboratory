# HR1 draft: calibrating hunting to forager evidence (3 November 2026; for council round 55, after FF2)

**What this is:** a draft for the council once FF2's result is known. Nothing is frozen or run. HR1 would run on v13 if
FF2 is adopted (F8 fixed: the hunt decision expects the meat of the prey it sees), otherwise on v12.
- **The sources:**
  - HN1's findings;
  - round 54 (`docs/debate_round54_after_hn1_am1_2026-11-03.md`);
  - the evidence note, `docs/research/hunting_success_hadza_2026-11-03.md` (Hawkes et al. 2014; Walker et al. 2002).

## The problem in numbers (HN1, v11)
- **A forage-week yields 20.77 food;** a hunt success yields 8.79 (mostly rabbits and fish); success is 5.4%.
- **The return ratio** (food per hunter-week ÷ food per forage-week) is 0.023. The frozen target range is 0.5–1.5
  (Aché about 1.1).
- **Even 100% success gives 0.42.** So the meat a success brings is binding, not only the chance.
- **The arithmetic** (the assistant's): R ≈ success × food per success ÷ 20.77. To reach R = 1, a week's hunt must
  bring 20.8 food on average:
  - rabbits (9 per success) cannot do it at any chance;
  - deer (22) needs about 95% success;
  - bison (55) needs about 38%.

## Two existing things to calibrate (no new law)
1. **Success per species** (F7). The species table already declares a catch rate per species (rabbit 0.40, deer 0.16,
   bison 0.10, fish 0.25). Its provenance is unknown, but its **order** matches the Aché per-encounter evidence (small
   prey are killed more often than deer, and large prey less often).
   - **The change:** the species is chosen **before** the roll (the same random choice `take_prey` makes now, moved
     earlier). The roll then uses that species' rate × the party, skill and tool terms, in place of the flat 0.10.
   - **The levels** are set by evidence, not taken from the table as they stand.
2. **Food per kill.** Each species' `meat`, and the number of small animals a success takes. These are
   **unit-bound**:
   - one ACL food unit is one adult-day's food (an adult needs 7 a week);
   - so a real carcass converts as live weight × edible share × energy density ÷ an adult-day's energy.
   - The frozen plan must name sources for the edible share and the energy density. Neither is read yet.

## The targets
- **Primary:** the return ratio R in 0.5–1.5, measured as in HN1 (pooled, with the matched version beside it).
- **Second check: success per hunter-week.**
  - Hadza large game: about 3.4% per hunter-day, about 21% per hunter-week if days are independent (the assistant's
    arithmetic).
  - Aché: kill per encounter 10–24% at the peak age.
  - The conversion from per-encounter or per-day to ACL's one hunt a week is written in the plan before data.
- **Guards first** (as AG1): population and extinctions. Hunting that pays may change who survives.
- **Described only:** the animal share of food, armed against bare-handed returns, and tool making and remaking. Never
  chosen on these.

## Open questions for the council
1. Should both things be calibrated in one study (a small grid), or meat first, since it binds?
2. **Units:** is "1 food = one adult-day's food" the right reading of `need_adult` 7? Which sources should fix edible
   share and energy per kg?
3. **Species roll order:** is choosing the species before the roll a calibration of existing parts, or a change of law
   needing a sham-controlled test of its own?
4. **Foraging is generous** (20.77 food a week, about 3 weeks of an adult's need). Should HR1 calibrate hunting only, or
   is foraging the side that is off? The older review found tools add 1% because the world is forgiving (TR1).

## Added after council round 70 (6 November 2026, 19:2x): HR1 is next on the laws road
- **Why now.** HK1 (who holds the kill) was shelved: on v14 there were 0 party kills in 105 kills, 1 pair in 713 hunt
  attempts, and 0.043-0.085 hunts per grown-year (`docs/debate_round70_hk1_design_2026-11-06.md`). Every social law
  about kills waits on hunting being real.
- **The council's conditions (unanimous after one revision):**
  - the target is an outside, pre-registered evidence quantity, never an ACL outcome;
  - **the conversion of units is frozen first**: what one ACL hunt is (one action a week at a tile with prey), and how
    per-day and per-encounter figures become per-week figures;
  - **F7's table is dropped.** Any per-species rate is derived from evidence. This settles open question 3 above:
    choosing the species before the roll is part of using evidence-derived rates, and it still needs a sham.
  - one setting per arm;
  - CI1-style harm guards;
  - participation and returns are described against the evidence, **never tuned afterwards** (GPT: the decision may
    still prefer foraging, and that is an informative null).
- **Open question 4 (is foraging too generous?) stays the first thing to settle.** If foraging is off, calibrating
  hunting alone moves the wrong side. A forage-week of 20.77 food is about 3 weeks of an adult's need.
- **Base:** the nature live when HR1 is frozen (v15 if CI1-C confirms and it is adopted).

## Added after FP1 (7 November 2026, 06:4x): the gap in ACL's own unit (a proposal for the unit conversion, not frozen)
**ACL v15, from FP1's 32 worlds** (a script on FP1's outputs):
- 2,092 hunts, 99 successful (**4.73%**);
- **9.24 food per success**;
- **0.437 food per hunt-week**;
- 17.50 food per forage-week (all ages);
- hunting ÷ foraging per week = **0.025**. HN1 measured 0.023 on v11, so nothing has moved.

**The evidence in ACL's unit** (Kaplan et al. 2000, Table 2, read in full: men's daily meat production in kcal; a
script). ACL's unit is one adult-day's need. An adult-day is taken as 2,500–3,400 kcal; that range is an
assumption, to be fixed from a source before freezing. Men's meat per man-week, in ACL food units:
- Hadza 14.9–20.3; Aché 10.2–13.9; Arnhem 9.4–12.8; Onge 8.1–11.0; Hiwi 6.6–9.0; Nukak 6.3–8.6; !Kung 4.6–6.3;
  Gwi 3.3–4.5.
- So **a forager man's meat week is worth roughly 3–20 ACL food units, against ACL's 0.44 per hunt-week: about 10–45
  times more.** It is the same order as an ACL foraging week (17.5).
- These are averages over all days, including days without hunting. So per hunting week the evidence is higher still.

**What this suggests (for the council, nothing decided):**
1. **The size of a success.** At the Hadza's about 21% large-game success per hunter-week, 10–20 food a week needs
   about 50–100 food per success. That is the order of ACL's bison (55), not its rabbits (3 each; 9.2 per success on
   average).
   - So the calibration may be the **mix and size of prey taken** as much as the success chance.
   - Which prey a success yields today follows `take_prey`: a random herd on the tile. Small game dominates.
2. **Children's foraging (FP1):** children reach their need at 8–11 against the mid-to-late teens. It is a separate
   calibration, with its own evidence (Kaplan's Figure 2 and text; Hadza children forage more than Aché children).
3. **A unit source** for "1 food = an adult-day" in kcal is needed before freezing: for example, adult energy needs in
   forager studies (Pontzer et al. 2012 on the Hadza, not yet read).
