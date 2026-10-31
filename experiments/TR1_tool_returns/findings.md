# TR1 — What do tools really add? Findings (not final until GPT and Gemini recompute)

Frozen as `TR1-frozen` (operational note 1; amendment 1). Signed off by the assistant under sleep-mode autonomy
(read-only; GPT 85%, Gemini 85%; debate round 34). 32 worlds on nature v10 (seeds 21001–21032), LP (80 founders,
80 × 80), 200 years. Every number comes from `analyse_tr1.py`, written before data; full tables are in `results.md`.

- **Run 2** (GitHub 41199047689) is the one reported.
- **Run 1** (41191446977) failed its own validity check. Three forage replays did not match because the forager died
  within the action. No outcome was read; see amendment 1 in `questions.md`. Its outputs are kept in
  `output_run1_invalid/`.

**Validity** (run 2):
- zero checks pass;
- all 32 worlds are present under one fingerprint (`code_v10`);
- every forage's replayed yield equals the food actually got (mismatches 0).

**Population beside it:** no world died out. Mean living population 138.3; 101.0 adults per world-year in years 100–200.
There were 6,608,366 adult forage weeks in years 100–200 (688,234 with a tool in hand) and 2,741 adult hunts.

## The answer

**Knowing matters, but it is unused.** Good tools exist in the world, and with them adults would forage a fifth more
food. Yet tools add 1% today, because only about one forage in ten is made with a tool in hand.

### Q1 — Food added by tools (primary)
- **Realized:** tools add **1.0%** [1.0%, 1.1%] of adults' foraged food.
- **Headroom (b):** with the best foraging tool **in anyone's hands** that week, adults would forage **20.0%** [19.5%,
  20.4%] more.
- **Headroom (a):** with the best tool of a kind **they themselves know**, they would forage **12.7%** [12.5%, 12.9%]
  more.

**The frozen reading: "knowing matters but is unused"** (headroom (b) ≥ 0.10, and the realized share is under half of
it). It is not near the line.

### Q2–Q6 (described)
- **Q2, where the help goes:** in tool-aided weeks, the tool:
  - added **nothing in 30.9%** (the carry room or the plants were already the limit);
  - was partly capped in 6.2%;
  - was fully used in 62.9%.
  Of the help the tools would give unbounded, **63.4%** reaches the food.
- **Q3, felt against real:** people feel a help of **0.144** per tool-aided week; the real gain is **0.094**. Felt help
  is half again the real gain.
- **Q4c, hunting:** tools raise the expected kills per hunt by 3.3% (0.051 → 0.053). The world's best hunting tool would
  raise them 47%. **But hunting hardly exists:** 2,741 adult hunts against 6.6 million forage weeks. Hunted meat is
  about 0.001% of adults' food.
- **Q5, by season:** the same in all four seasons (realized 1.0–1.1%; headroom (b) 18.5–21.1%).

## Against the prior (the assistant's, frozen)
1. "Barely matters: the carry room often binds, so the realized share is small": **the realized share is small**
   (1.0%), but the reason is mostly that **few people hold tools**, not the carry room. **The reading was wrong:**
   headroom is 20%.
2. "Felt help clearly exceeds the realized gain": **right** (0.144 against 0.094).
3. "Hunting tools double the kill chance, but add little food": **first part wrong** (+3%), **second right**.

## What it means
- **A world where knowing matters is already partly here,** in foraging: the best existing tools would add a fifth to
  food. The loss is that **tools do not reach hands:** about 90% of forage weeks are bare-handed.
- **Why might tools not reach hands?** From today's checks and research (not tested here):
  - **No living person can hand a tool to another.** Tools pass only by pick-up from the ground or at death
    (`docs/research/tool_passing_and_learning_2026-10-31.md`).
  - **Children under 12 cannot make known things.** Real forager children make miniature adult tools
    (`docs/research/making_time_and_child_objects_2026-10-31.md`).
  - **The choice to make loses to food** (CO2, IW1). With the help felt per use (0.14–0.16), making rarely wins.
  - **The 3-item hand limit** and wear (law 13; not measured here).
- **What follows, by the frozen branch "matters but unused":** look at access and choice. Who holds the best tools,
  and why others do not make them or get them.
  - A **read-only follow-up** can measure this.
  - A **law** letting people hand things to each other (a physical ability, with whether and when they do it left to
    culture) would be a nature-change study under the safe path, **and a question for the creator first.**
- **No change to nature** follows from this study by itself.

## Independent recompute
Pending: GPT and Gemini, each in a fresh chat, from `recompute/tr1_one_file.csv` (per-world sums from the raw output).
Recorded only from their actual replies.
