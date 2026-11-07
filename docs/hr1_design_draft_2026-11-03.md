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
