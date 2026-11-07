# EG1: when someone is starving, does the energy rule stand between them and food? (frozen plan)

**A read-only audit of nature v15.** It comes from play mode (`experiments/PLAY1_inside_acl/journal.md`; not data) and
council round 75 (`docs/debate_round75_after_play_2026-11-07.md`), where all three models, after the code facts, put
this audit first. **Nothing in nature changes, and EG1 decides no law.** Its reading tells the council whether the
energy rule is worth a frozen law or calibration test, and which one.

## The rule being audited (v15, `acl/mind.py`, `acl/biology.py`, `acl/actions.py`)
- **An option is dropped when energy is below its cost.** `decide`'s `add` drops any option with energy < `COST[action]`
  + 4 × distance. Forage costs 25 and hunt 40.
- **Energy recovery.** Energy recovers 25 a week × (1 − 0.5 × deficit), up to 100. A rest week adds 40 more.
- **Forage is weighed only at its best tile.** `decide` weighs forage at the **single best tile** among those it looks
  at, chosen without regard to energy. If that tile is unaffordable, forage is not offered at all, even when a nearer
  tile with food was affordable.
- **Hunt.** Hunt (the grown only) is weighed at its best tile with prey, the same way.

## Design
- **Code:** `code_eg1` = `code_v15` plus logging lines only: `world.eg1log` is set by the runner, not saved, and read by
  nothing in nature. Zero checks 1 and 2 show it behaves exactly as v15.
- **Arms:** one arm, no sham. LP (80 founders, 80 × 80).
- **Seeds:** 24701–24732 (32 new seeds, used by no study). 200 years; years 100–200 counted.

## What is logged (every `decide` call, people aged 6 and over)
- **Before the call:**
  - age;
  - sex;
  - `p.starving` (consecutive weeks short, from the last body phase);
  - energy;
  - health.
- **Forage:**
  - the best tile's distance and expected food (`got`, by `decide`'s own formula);
  - whether it was affordable;
  - the most food expected at any tile looked at that **was** affordable;
  - the food expected on one's own tile.
- **Hunt** (the grown): whether a tile with prey was found, its distance, and whether it was affordable.
- **The options actually offered** (read at `thought.steer`) and the action chosen.
- **Deaths:** the cause and the person's age, with their last 4 weeks of log.

## Definitions
- **Starving person-week:** a `decide` call, aged 6+, with `p.starving` ≥ 1, meaning the person went short (deficit >
  0.05) last week.
- **Food feasible** (energy aside, by the existing rules):
  - forage's best tile had expected food `got` > 0; **or**
  - (for the grown) a hunt tile with prey was found.
- **Blocked by energy alone:** food was feasible, and neither forage nor hunt was offered because energy was below the
  cost.

## Primary outcome (council round 75: GPT, Gemini and DeepSeek converge)
**P = blocked-by-energy-alone starving person-weeks ÷ all starving person-weeks**, pooled over the 32 worlds. Its 95%
interval is a world bootstrap (10,000 draws of 32 seeds with replacement).

**Readings (frozen):**
- **"energy binds when starving":** P ≥ 0.20 and its lower bound ≥ 0.10;
- **"energy rarely binds":** P's upper bound < 0.05;
- **"a minor contributor":** otherwise.

## Secondaries (each with its population)
1. **The split of starving person-weeks into four parts:**
   - (a) a food option was offered and chosen;
   - (b) offered, but not chosen;
   - (c) blocked by energy alone (P);
   - (d) no food feasible.
2. **The same split by age band** (6–11, 12–15, 16–29, 30–49, 50+) and sex.
3. **Non-starving weeks:** the share of non-starving person-weeks blocked by energy alone (DeepSeek: is the gate binding
   in general?).
4. **The best-tile quirk:** of the blocked weeks in P, the share where a tile looked at had food and **was** affordable.
   Beside it, the share where even one's own tile (cost 25) was unaffordable.
5. **What was done instead** in blocked starving weeks: the chosen action's shares.
6. **How long it lasts:** runs of consecutive blocked starving weeks per person: the mean, and the share of runs of 2
   weeks or more.
7. **Deaths:** of starvation deaths at age 6+, the share with at least one blocked starving week in their last 4 weeks.
8. **Rest weeks of the grown** (16+, DeepSeek): the share where food was blocked by energy alone vs where food was offered
   and rest was chosen.
9. **Energy at decision:** the mean, in starving and in non-starving weeks.

## Zero checks (hard stops)
1. **`code_eg1` with no log = `code_v15`:** world and random-stream hashes match (seed 501 for 20 years; seed 601 for
   60 years).
2. **Read-only:** `code_eg1` with the log on = `code_v15` (the same seeds and years).
3. **Hook check:** in every logged person-week of a 30-year world (seed 701), the log's prediction (forage offered ⇔
   energy ≥ 25 + 4 × the best tile's distance; hunt offered ⇔ a prey tile was found and energy ≥ 40 + 4 × its distance)
   equals the presence of forage and hunt among the options actually offered. **Any mismatch stops the study.**
4. **Reload is exact.**
5. **All 32 worlds** are present under one fingerprint.

## A blind recompute
GPT, Gemini and DeepSeek recompute from a per-world count file built by a script written before data. The file has, per
world: starving weeks, blocked weeks, the four-part split, non-starving weeks and their blocked count, the quirk count,
starvation deaths at 6+ and those with a blocked week before them. They recompute P with its interval, secondaries 1, 3,
4 and 7, and the reading.

## Prior (the assistant)
- P is about 0.25: a starving week recovers only 12.5, so a starving forager falls below the cost within two weeks. The
  most likely reading is "energy binds when starving", about 55%.
- The quirk is a sizeable part of the blocked weeks, about 30%.
- Most runs last 1 week, because one rest week restores 52.5.

## Sign-off (7 November 2026)
The assistant, under the creator's standing permissions (2 November: edit world rules; 7 November: "you can keep going do
not rely on me"; 03:15 Telegram: "do not ask for permissions from me just go").

Council round 75 estimates:
- GPT: 96%;
- Gemini: 95%;
- DeepSeek: about 87%;
- the assistant: 90%.

Frozen as `EG1-frozen` before any code or data.
