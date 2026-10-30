# Design note (draft, 30 October 2026): an apprenticeship law, and an early autonomy audit

**Status: a design note, not a frozen plan.** Nothing here is decided. The creator signs off later, and LS2's findings (the 1,000-year audit of where knowledge is lost under v9; 18 of 20 chunks at `WORKLOG.md:351-352`) will shape the details. This note does what the creator agreed (`WORKLOG.md`, 2026-10-30 01:38: "yea i agree go ahead with that order"): LS2 first, then apprenticeship, and autonomy defined and measured early.

**Sources.** The note uses only the three read-only scout reports: A (the code for apprenticeship), B (signs of autonomy) and C (past studies). Their file:line citations are kept. I re-read the following myself, and the citations matched:
- code: `acl/actions.py:85-98, 180-194, 392-417`; `acl/knowhow.py:229-244`; `acl/mind.py:273-300`; `acl/config.py:125-169`; `acl/inquiry.py:22-73`; `acl/thought.py:164-220`;
- study records: `experiments/FS1_founder_start/questions.md:30-59`; `experiments/LC1_long_curiosity/questions.md:10-29` and `findings.md:10-49`; `experiments/CU1_curiosity/questions.md:38-50` and `findings.md:38-41, 68`; `experiments/LS2_knowledge_v9/questions.md`; `docs/gpt_view_mission_focus_2026-10-30.md`;
- scout A's scratch outputs and script (`run50.json`, `obs10.json`, `raw10.json`, `smoke_makewatch.py` in the session scratchpad).

Every smoke or probe number is **scratch, not data**: one or three worlds, nothing frozen, nothing recomputed independently. Arithmetic I derived myself is labelled as mine.

---

## Part 1: Apprenticeship law (watching someone make a thing teaches technique)

### 1.1 What exists today
- **Making gives the maker one crafting-skill step and nothing else.**
  - `_make` (`actions.py:392-400`) calls `_craft`. On success it gives reward +0.1 and emits one `"make"` event.
  - `_craft` calls `_gain_skill(world, p, "crafting")` before the outcome is known (`actions.py:408`).
  - Making never touches recipes, `world.knowledge`, or any other person (scout A §1).
- **The skill step:** `skill_gain × (1 − skill)`, capped at 1.0. `skill_gain = 0.012` (`config.py:164`). It is ×1.6 while the person is "focused" (`actions.py:96-98`).
  - Skill starts at 0 at birth (`person.py:112`). Nothing ever lowers it: the only writes are `actions.py:98` and `world.py:227`.
- **Children under 12 cannot make** (`mind.py:279`). All their crafting skill comes from play (PL1: share from play 1.000 at ages 3–6 and 0.977 at 7–12, `experiments/PL1_child_play/findings.md:34-35`).
- **The existing watching law** (`knowhow.watch`, `knowhow.py:229-244`) passes a **recipe, never skill**, and is set off by **use, not making**. Two places call it:
  - after a crossing: onlookers within `perception` (4 tiles), aged 6+ (`actions.py:90-93`);
  - in a hunt: **co-hunters only**, with no sight radius and no age check (`actions.py:186-189`).

  The chance of noticing, `0.04 × (0.5 + curiosity)`, is a literal in the code, not a setting (`knowhow.py:235`).
- **Correction to the record (scout C, confirmed by me).** The council text at `docs/gpt_view_mission_focus_2026-10-30.md:29-31` says onlookers aged 6+ within sight learn from hunts. The code limits hunt-watching to co-hunters. This should be **appended** as a correction (never a rewrite) before any plan cites that text.

### 1.2 The proposed law
**In plain words:** when someone successfully makes a thing, each person nearby who notices it gets one ordinary step of crafting practice, as if they had practised themselves. Nothing else changes.

**In code terms (a sketch to discuss, not code to commit; it would live in the study's own code copy, and live `acl/` is untouched until adoption):**
- **Setting:** `make_watch: int = 0` next to `curiosity_pull` (`config.py:129-130`).
  - 0 = v9 exactly.
  - 1 = the law is on.
  - 2 = the sham (see 1.4).
  - It follows the `curiosity_pull` pattern: a setting check only (`mind.py:178`, `biology.py:397`), and the v8→v9 diff as the template (scout A §5).
- **Hook:** inside `_make`'s success branch, after `world.emit("make", ...)` (`actions.py:397-400`), under `if world.cfg.make_watch:`. With the setting off there is no `people_near` call, no random draw, no skill write and no event.
  - **Not in `_craft`.** `_craft` also runs in children's play (`actions.py:558`) and on failed attempts (`actions.py:408`). That would change what "making" means (scout A §5).
- **Who can watch** (reusing the crossing rule, `actions.py:90-93`):
  - everyone within `cfg.perception` (4 tiles; `config.py:155`) of the maker, through `world.people_near` (`world.py:397-409`, which draws nothing and changes nothing);
  - aged 6 or older, with the age check made **before** the draw, as at the crossing;
  - the maker excluded.
  - No upper age limit: the existing rules set only a lower age, and an upper limit would be a new boundary (scout A, open question).
- **Chance reused:** one draw per eligible onlooker at `0.04 × (0.5 + curiosity)` (`knowhow.py:235`).
  - If this is moved into a shared helper, its single draw must stay after `watch`'s three early returns (`knowhow.py:233-236`), so existing callers draw exactly as in v9 (scout A §5).
- **Increment reused:** on a hit, `_gain_skill(world, q, "crafting")` (`actions.py:96-98`). That is the plain step towards 1.0, including the ×1.6 focus factor, because that is what plain reuse does.
- **What does NOT change:**
  - the maker's state;
  - recipes and `world.knowledge` (written only by `remember_recipe`, `knowhow.py:83-86`);
  - item values;
  - habit values `q` and `tried` counts (`person.py:182` defines them as one's own learning);
  - the LS ledger routes;
  - saved person state (skills are already saved, so no new state is needed);
  - every random draw when the setting is off.

### 1.3 Two options, and a recommendation
**(i) Technique only (GPT's preference: one mechanism at a time).** Code size: the setting, about 2 lines in `_make`, and a new function of about 6 lines (scout A §6).

**(ii) Technique and recipe (Gemini).** Option (i) plus `knowhow.watch(world, q, p, sig, p.itemval.get(sig, 0.0))`, with these details:
- **Pass the recipe key `sig`, not the made item's name.** For heat recipes the item's name is the part plus the actual fire level (`matter.py:161`), while the recipe key uses the recipe's own level (`information.py:340`).
- **`watch` makes its own draws:** the notice (`knowhow.py:235`), the copy error (`information.py:294-318`), and 0.15 (`knowhow.py:238`). So either each watcher gets two independent rolls, or `watch` is split so that one notice serves both, keeping the existing draw order for its current callers.
- **Watched recipes meet the PT1 order problem.** The new copy is remembered before its value is set (`knowhow.py:243-244`, confirmed). PT1 found the new lesson evicted in 0.714 of overflows (`experiments/PT1_parts_teaching/findings.md:62`). MO1's fix failed its manipulation check (`experiments/MO1_memory_order/findings.md:27-47`), so v9 still has the problem.

**Recommendation: (i), technique only.** Reasons:
1. **One setting, one mechanism.** This is ACL's rule, and GPT's argument (`gpt_view_mission_focus:40-46`).
2. **Recipe-by-watching already exists, and it passes almost nothing:**
   - CA1: 6 and 4 first transmissions by watching, against 806 and 643 by teaching (`experiments/CA1_chain_audit/findings.md:38-40`);
   - E7.7: 7 copies from 1,149 times a boat was watched (`experiments/E7_7_imitation/results.md:40-47`);
   - LS1: 0.00 recipes acquired by copying by age 16, in every cohort (`LS1_where_knowledge_goes/results.md:140-159`).

   The missing capacity is technique, not one more recipe route.
3. **(ii) would mostly feed recipes into full memories, where they are evicted at once** (the order problem above).
4. **(i) leaves the LS ledger's recipe routes unchanged**, so LS1/LS2's recipe accounting stays valid as is.

**Gemini's strongest counter-argument should go to GPT.** Technique without the recipe cannot itself produce making. GPT's answer would have to be that crafting skill is one store for all recipes (`person.py:16`) and acts on:
- the quality of struck edges, including in children's play (`matter.py:83-85`);
- the gathering rate (`actions.py:240`);
- the copying error in later lessons (`information.py:288`).

So technique can matter without a recipe. But **skill does not enter the utility of making** (`mind.py:289-296`, confirmed), and MK1 found the low-skill trap weak (`experiments/MK1_why_not_make/findings.md:49-50, 69`). So neither option should be expected to raise making directly.

**Ledger and observer implications of (i):**
- **Measures that would mix watching with doing:**
  - LS1/LS2's per-person "practice" counter (weeks in which crafting skill rose);
  - skill at 16 and 30 (LS2 `questions.md:27-29`);
  - PL1's skill wrapper, which files each gain under the gainer's own action (`run_pl1.py:99-102`), so watched gains would be misfiled.
- **The fix:** keep the new code in its own named function, so a read-only observer can wrap it and tag watched gains. That is ACL's usual pattern.
- **A `"watched"` event emitted only when the setting is on** is optional. It cannot break off = v9, because no event is emitted when off; events change event ids and the event chain, which are saved state (`world.py:448-461, 534-535, 701-707`). It does add bulk. Left open.

### 1.4 Zero checks (ACL's usual pattern)
1. **Off = v9 exactly.** With `make_watch` 0, the world state and the random-number state are identical to `code_v9` at 20 and 100 years on LP (LS2's check points). The comparison leaves the settings out of the hash, because `World.state_hash` includes the settings (`world.py:697, 755-757`); this is how NV9's `run_nv9.py` `world_hash` does it.
2. **On acts.** With `make_watch` 1:
   - the world differs from off;
   - the new function fires (watched gains > 0 in a short run);
   - every watched gain goes to someone aged 6+ within 4 tiles of a successful make.
3. **The sham acts and is inert as designed.** With `make_watch` 2, the same onlookers are found and the same draws are made, but no skill is written. It differs from off (the random stream moves) and has exactly 0 watched gains.
   - Precedent: E13R's sham `b2_write = False`, which "runs the copying step to the point of writing, then returns" (`config.py:169`).
   - The alternative is the standard yardstick sham, `sham_draw` 1: one extra draw in week one (`config.py:131`).
4. **The observer is read-only.** State and random numbers are identical with and without it, at 20 and 100 years. This is the scout A smoke pattern: the hash was identical at 10 years, `8d83e5ec…` in `obs10.json` and `raw10.json`.
5. **Reload exact.** Save mid-run, reload and continue: the result equals an uninterrupted run, in each arm. Old code ignores unknown settings (`config.py:191-200`, per scout A; I did not re-read these lines).
6. **One code fingerprint for all worlds; all worlds present; the existing tests pass with the setting off.** CLAUDE.md lists 64 on v9.

### 1.5 Exposure: the main risk, with the scouts reconciled
Scouts A and C seemed to disagree about exposure by about 5×. They agree once the era is matched.

| source | era / making rate | watched steps per juvenile-year | relative to own practice |
|---|---|---|---|
| A, smoke (seed 9931, years 0–50; onlookers aged 3–15) | early; **0.437 makes per adult-year** (my arithmetic from `run50.json`: 1,679 makes ÷ 3,845 adult-years) | 0.136 | 2.95% of ages 3–15's own steps |
| A, same smoke, **ages 6–15 only** (the 6+ rule) | same | 0.142 | **6.1%** of ages 6–15's own steps (my arithmetic: 265.0 expected ÷ 4,334 own steps) |
| A, the radius-1, chance-0.5 rule instead (ages 3–15) | same | about 0.46 | about 9.9% |
| C, back-of-envelope (v7 reach × CU1's v9-arm making, 0.0758) | years 100–200 | about 0.027 | about 0.0045 skill over ages 6–20 |
| A's 0.142 scaled to CU1's v9 making, 0.0758 (`CU1 findings.md:68`) (my arithmetic; assumes onlookers per make stay constant) | years 100–200 | about 0.025 | about 0.35 steps over ages 6–20, about 0.004 skill |

Context for the table:
- Making falls over time: LC1's curiosity arm had 0.313 makes per adult-year in years 0–100, 0.034 in 400–500, and 0.028 in 900–1,000 (`LC1 findings.md:39-41`).
- Adults watch too: 7.01 adult onlookers per make, against 5.11 juveniles (scout A).

By the same scaling (my arithmetic), adult watching roughly doubles a person's watched steps by age 30. That is still about 0.5 steps, about 0.006 skill, in years 100–200, **below FS1's ±0.012 margin**, unless feedback amplifies it (better skill → better strikes → higher item worth → more making → more exposure). A smoke cannot rule that feedback in or out.

**What follows.** With the reused 0.04 chance, a study's most likely reading is "no lasting difference", nearly by construction (scout C's point; scout A agrees: "a study may struggle to see any effect").

**The tempting fix is itself a tuning risk.** The fix would be to switch to the radius-1, chance-0.5 rule: seeing a thing put down (`actions.py:312-314`) or a mark made (`marks.py:145-147`). Choosing that rule because it gives a bigger effect would be tuning towards an outcome. The choice must rest on which existing rule is the **closer analogue**, decided and frozen before data:
- seeing an act done at close range (put, mark), or
- working out a recipe from seeing use (`watch`).

This is the first question for the debate.

### 1.6 Study sketch (ACL's usual pattern; to be frozen only after LS2 and sign-off)
- **Arms:** v (v9, `make_watch` 0), a (apprenticeship, 1), x (matched sham, 2). The sham's x − v sits beside a − v as the yardstick for drift.
- **Worlds:** LP (80 founders, 80×80); 32 new paired seeds (a fresh block, not LC1's or LS2's); world bootstrap with 10,000 replicates, resampling seeds once per replicate for all arms (`FS1 questions.md:34`; scout C §3). No seeds added after results (`FS1 questions.md:57`).
- **Length: 200 years, primary window years 100–199.** Reasons:
  - it is past the founder era (founders start at skill 0.2–0.4, `world.py:227`; making is high early, LC1 0.313);
  - it is the window of CU1, the law that passed, and the one Gemini proposed;
  - it keeps cloud chunks within GitHub's job limit (LS2 dropped an arm because LC1's longest chunk reached it, `LS2 questions.md:17-18`).

  A 1,000-year follow-up only if this passes, as CU1 → LC1.
- **Primary candidates:**
  - **FS1/LC1 measure (recommended).** World-born adults' (20–40) mean crafting skill in years 100–199, pooled over yearly censuses (summed skill ÷ summed head count), a − v paired by seed. Margin ±0.012 = one `skill_gain` from zero (`FS1 questions.md:36-39, 48-50`; `LC1 questions.md:16-19`).
    - Why: it is anchored in the code and comparable with CU1 (v 0.232, c − v +0.041 [+0.033, +0.048], `CU1 findings.md:41`) and LC1.
    - It captures both childhood and adult watching.
  - **GPT: skill acquisition among young observers, with against without chances to watch making.** As a within-arm comparison it is observational. Juvenile onlookers are kin or wards in 0.232 of cases (scout A), and children are moved to their carer's tile each week (`world.py:500-505`). Recommend recasting it between arms, as a **key secondary**: crafting skill at 16 (LS1/LS2's measure), a − v; and watched steps per juvenile-year aged 6–15, which also serves as the manipulation check.
  - **Gemini: share of world-born adults 20–40 holding observed recipes with crafting skill > 0.10 in years 100–200.** It needs option (ii), and 0.10 is a new number not taken from the code (`gpt_view_mission_focus:49-51`; scout C §3). It is suitable only as a described secondary if (ii) is ever run.
- **Secondaries (described, not success criteria):**
  - skill at 16 and 30, with practice split into own and watched (tagged by the observer);
  - **intergenerational retention:** LS1's Q5 inheritance rate by birth cohort, and the change in skill from early to late cohorts (LC1-style);
  - making per adult-year: described, with **no expectation** of a rise (skill does not enter make's utility, `mind.py:289-296`; MK1);
  - made things held per adult; the gathering rate; strike quality;
  - exposure: makes with a 6–15-year-old within 4 tiles; onlookers per make;
  - **survival:** extinct worlds; mean population (extinct worlds count 0).
- **Frozen decision rule (the shape, CU1/LC1 style):**
  - **"Apprenticeship raises skill":** the lower 95% bound of a − v is above +0.012 **and** above the upper bound of x − v.
  - **"No lasting difference":** the 95% interval lies inside ±0.012.
  - **"Lowers":** the upper bound is below −0.012.
  - **Otherwise "not shown".**
  - **Flags (block any adoption recommendation):** a has 3 or more extinct worlds beyond v, or mean population in years 100–199 below 0.90 × v (`CU1 questions.md:45-46`).
  - **Manipulation check:** watched gains > 0 in a and exactly 0 in v and x. No threshold may be set from one-event replays (MO1's lesson, `MO1 findings.md:52-60`).
  - **Survivor weighting** in the open: contributing worlds and adult-years beside every skill estimate (`FS1 questions.md:40-42`).
  - **The assistant's prior, frozen before data:** "no lasting difference" is the most likely reading (section 1.5).
- **Main risks:**
  1. Exposure is too rare to pass the margin (section 1.5).
  2. Choosing the exposure rule by its effect would be tuning.
  3. Technique alone may not move making (MK1; `mind.py:289-296`).
  4. Adults are the majority of onlookers (7.01 against 5.11 per make), so the population effect is not purely "young observers".
  5. Existing practice counters get contaminated (section 1.3).
  6. All exposure numbers come from one 50-year smoke world in the early era.

### 1.7 What LS2 could change
- **If LS2 shows (as LS1 did on v7) skill at 16 collapsing with practice weeks** (v7: 0.45 → 0.18 → 0.04, and 39 → 12 → 2.5 weeks, `LS1 findings.md:76-77`): technique is confirmed as the target. Go ahead with (i).
- **If LS2's Q3 shows the loss is mostly at the choice gate** (offered → chosen; on v7, MK1 found 0.0232 → 0.0020 chosen given offered, with the other options carrying 1.03 of the fall, `MK1 findings.md:19-33`): a technique law cannot reach it directly, because skill is not in make's utility. Making should then not be read as an apprenticeship outcome. The better candidate becomes the third capacity in `docs/missing_abilities_audit_2026-10-27.md:93`, "learning worth" (learning by watching that making pays). That would be a different law and a different study.
- **If LS2's Q5 shows recipe inheritance is the main leak while skill holds:** option (ii) gains weight. The PT1 order problem must then be dealt with first, or watched recipes will be evicted.
- **If LS2 shows practice falling mainly in late centuries:** the primary window, or a 1,000-year run, should move to match.
- **LS2 does not count onlookers.** A read-only exposure count on LS2-like worlds (scout C's open question) could replace the one-world smoke before freezing.

---

## Part 2: Autonomy, a read-only audit to define it and measure it early

**Ground truth from the code (scout B; key lines re-read by me).**
- Each person makes one fresh decision a week. `mind.decide` never reads `p.last_action`.
- The only look-ahead is the TD discount of 0.8 (`biology.py:388-396`).
- `thought.steer` adds a bonus from the **top thought only** (`thought.py:187-208`).
- Attention has inertia: +0.12 + 0.3·diligence for last week's focus (`thought.py:169-171`).
- The choice is a softmax at temperature 0.2 (`mind.py:534`; `config.py:172`).
- "Focus" is attention with inertia, not an intention. It has no success condition and no stored plan.
- **The only stored destination that steers later choices is a voyage** (`actions.py:48-51`; `mind.py:360-366, 144-146`).
- `decision.py`'s `prediction_error = |score − 5·reward|` is **not** the person's own expectation (`decision.py:111-119`). Do not use it.

### 2.1 GPT's five signs (`gpt_view_mission_focus:25`) and their best measures
Probe numbers are scout B's scratch counts: 3 LP worlds, 60 years, 9,777 adult-years.

**1. Notices a problem without being assigned it → M1.**
- **Measure:** puzzles from the person's **own** surprise, later acted on, resumed after an interruption, or settled. Sources of own surprise:
  - item use (`knowhow.py:57`);
  - place beliefs (`knowhow.py:180`);
  - sparks (`actions.py:428`);
  - embers (`actions.py:668`).

  These all lead to the `puzzled` event (`inquiry.py:56`). They are split from **told** puzzles (`_wonder`, `information.py:381-384`) and from novel marks (`marks.py:199`).
- **Hooks:** wrap `inquiry.surprised` (for the origin) and `thought.steer`; the `puzzled` and `tested` events.
- **Why not an echo:** counting puzzles alone only re-measures the threshold `|gap| ≥ 0.25` (`inquiry.py:22, 44`). Linking a noticed gap to a **chosen** act weeks later is not a formula.
- **Confound:** the steer bonus 0.35·strength (`thought.py:200-202`) and `_best_put`'s 0.6·pull push exactly this act. The pull scales with curiosity and (1 − 0.8·hunger). So compare with the act's base rate in matched weeks.
- **Observer only.**
- **Probe:** own puzzles 3.16 per adult-year; acted on 9.5% (b: 13.0%, f: 1.9%, **m: 0.0%**); told puzzles acted on 0.0%.
- **Uncertainty:** scout B explains m: 0.0% by "make is closed while they hold the thing" (`mind.py:294`). The line closes make only when the value equals the item's own value. A puzzle term `0.5 × pull` above the item's value would reopen it. The 0.0% is therefore not fully explained and needs checking before M1 is frozen.

**2. Picks a goal from its own experience → the top thought's `about`, tagged by where its value came from (M2/M5).**
- **Measure:** the top thought's target (a craft sig, a puzzle key, a shore), tagged by the source of its value:
  - own use (`judge_item`);
  - a lesson (`information.py:375`);
  - watching (`knowhow.py:244`).
- **Hooks:** wrappers on `judge_item`, `hear_how` and `watch`, as HL1 and CL1 did.
- **Why not an echo:** it asks where the goal came from, not how often goal-kind thoughts win.
- **Confound:** goal-kind strengths are scaled ×(1 − hunger) (`thought.py:142, 145, 149, 154`), so "while calm" is built in. And `q` mixes routes: copying carries 0.93 of the common actions' over-valuation (`CL1 findings.md:18-31`).
- **Observer only.**
- **Probe:** goal kinds on top in 17.5% of adult weeks (puzzle 13.6%, curiosity 3.8%, craft 0.12%, shore 0.04%).

**3. Carries out several actions towards it → M2, sub-goal chains.**
- **Measure:** ordered chains across weeks:
  - gather (a wanted material) → make the part → make the whole (`_wanted_parts`, `mind.py:574-585`; `_material_wants`, `mind.py:613-634`);
  - puzzle → targeted act → test;
  - voyage → crossing.

  Each is compared with a no-want baseline.
- **Why not an echo:** the order across weeks is stored nowhere, and the baseline absorbs completions that would happen anyway.
- **Confound:** having the materials by luck (the `can_make` gate), and the (1 − hunger) scalings.
- **Observer only.**
- **Probe:** a wanted part was made 0.139 times per adult-year, and the whole followed within 52 weeks in 18.0% of cases. Gathers for a wanted material were followed by a matching make within 26 weeks in 8.2% of cases, against 4.6% for other gathers. Voyages: 298 begun, 106 crossings.

**4. Changes plan when evidence contradicts it → M3.**
- **Measure:** after a test with gap ≤ −0.25 on b: or m:, the next act in the same domain within N weeks: the same act, an **alternative means** (another thing, season, place, or recipe for the same use), or none. Compared with what follows a confirming test.
- **Why not an echo:** only "switch to an alternative means" escapes the formula.
- **Confound:** the puzzle loop mandates a re-try. A surprising test keeps the pull at max(pull, |gap|) (`inquiry.py:35-38`). Exclude the hard-coded deletions: dry springs (`mind.py:764-766`), empty last-seen spots (`mind.py:827-829`), tested hearsay (`information.py:106`).
- **Observer only.**
- **Probe:** another test followed 88.4% of surprising tests, against 64.7% of settling ones. That gap is mostly formula.

**5. Holds a goal when immediate reward favours something else → M4 (weakest).**
- **Measure:** weeks where an own-origin goal thought flips the ranking (pre-steer gap ≥ 0.1), followed through to completion; voyage weeks continued while hunger > 0.3.
- **Echo risk is high.** This is `steer` plus inertia (`thought.py:169-171`) plus softmax noise: 32.9% of choices were not the top post-steer option.
- **Observer only; descriptive only.**
- **Probe:** a goal-kind thought flipped the ranking in 0.55% of adult weeks (0.21% with a gap ≥ 0.1).

**Foundation for signs 2 and 5 → M5.** An origin ledger of the deciding term: drive, own-experience value, copied or told value, steer, the curiosity term, or noise. Wrappers on `steer`, `_learn`, `_imitate` and `_upbringing`. Observer only.

### 2.2 What today's nature cannot show at all (honest statement)
- **Sign 2, strict:** a self-made goal outside the 19 fixed thought kinds (`thought.py:41-61`), or a goal held as state with a success condition.
- **Sign 3, strict:** a plan, or a step valued only because it enables a later step, beyond the coded part/material links and the voyage.
- **Sign 4, strict:** revising a plan. There is no plan to revise; only behaviour after contradiction can be measured.
- **Sign 5, strict:** a goal traded against reward. `p.reward` is known only after acting, and no goal state exists. Until an intention state exists, this cannot be told apart from steer + inertia + noise.
- **Sign 1, outside the coded keys:** problems in domains with no expectation key (outside m:, b:, f:, k:, heard). Example: a lost stash is almost never noticed (`found_gone` 1 event in 9,777 adult-years; S1 none, `S1 findings.md:21`), because `take` is offered only while the stash is still there (`mind.py:60-74, 322-325`).

Each of these would need a nature change (a persistent intention, plans, new expectation keys, a prediction the person holds). **Not now.**

### 2.3 A minimal first audit (read-only, v9, the existing observer pattern)
- **Pattern:**
  - wrappers on `thought.steer` and `inquiry.surprised`, which draw no random numbers (the CU1 precedent, `run_cu1.py:123-143`);
  - a weekly observer after the week, when `p.considered`, `p.thoughts`, `q` and `puzzles` are already updated (`world.py:534-541`);
  - checks: the observer is read-only (state and random numbers identical with and without it), all worlds present, one fingerprint, an independent recompute.
- **Three measures:**
  1. **M1 (primary candidate):** own-noticed puzzles → a chosen targeted act, against the matched-week base rate; own against told.
  2. **M2:** sub-goal chain completion against the no-want baseline.
  3. **M3:** after a contradiction, switch / repeat / drop, against a confirming test.

  M4 described only, or left out. M5 later, with a value-route ledger.
- **Design:** LP, v9, a modest number of new seeds and years. Scout B suggests the standard design (32 seeds, 200 years, a discovery set and a holdout). The 3-world probe could serve as the shape of a formal feasibility pilot first.
- **Windows and cut-offs need anchors before freezing.** Code-anchored options:
  - THRESHOLD 0.25 and SETTLED 0.1 for gaps (`inquiry.py:22-23`);
  - a puzzle's fade life, about 41 weeks at pull 1.0 (0.93ⁿ < 0.05; scout B's calculation), for the M1/M3 window;
  - the 12-week life of a voyage (`mind.py:144-146`) and of hearsay (`information.py:468-470`).

  The 26- and 52-week windows and the 0.1 steer gap have no anchor.
- **Cost:** observers only. It could ride on the apprenticeship study's v9 arm, or run as its own study. That is open.

---

## Open questions

**For GPT and Gemini (debate):**
1. **Which existing exposure rule is the true analogue of watching someone make?** `knowhow.watch` (4 tiles, 0.04 × (0.5 + curiosity), age 6+; about 0.025 watched steps per juvenile-year in years 100–200 by my scaling), or seeing an act at close range (1 tile, chance 0.5)? This must be decided on the analogy, before data, not on the expected effect size.
2. Technique only, or technique and recipe? If the recipe too: one notice or two rolls, and what to do about the order problem (`knowhow.py:243-244`; PT1 0.714)?
3. The plain step towards 1.0 (`_gain_skill`), or a move towards the maker's skill at the existing imitation/upbringing rates (0.05 / 0.08; scout A, not re-read by me)? Should the ×1.6 focus factor apply to watchers?
4. Should adults watch? There is no upper age in the existing rules, and adults are the majority of onlookers.
5. The primary: FS1/LC1's world-born adults' skill (±0.012); GPT's young-observer acquisition, recast between arms; or Gemini's > 0.10 share (a new number)?
6. A matched sham (E13R-style, same draws, no write) or the standard `sham_draw`? 200 years or 1,000?
7. Should the on arm emit a `"watched"` event?
8. Is a study worth running when its frozen prior is "no lasting difference"?
9. Autonomy definitions:
   - Do told puzzles count as "assigned"?
   - Does E9's anticipation of a short season count as noticing without being assigned?
   - Do values copied in talk count as "own experience"?
10. Include M4, or declare sign 5 unmeasurable until a nature change?
11. Why are own m: puzzles never acted on (0.0%), when `mind.py:294` does not close make if the puzzle term is the largest?

**For the creator:**
1. Is the general shape right: technique only first, frozen only after LS2's findings and their recompute?
2. Should the correction to `gpt_view_mission_focus:29-31` (hunt-watching is co-hunters only) be appended?
3. Should the autonomy audit be its own read-only study, or observers riding on the apprenticeship study's control arm?
4. Before freezing, should there be a read-only exposure count (how often a 6–15-year-old is within 4 tiles of a make, across eras), on LS2-like worlds instead of the one smoke world?

OPEN QUESTIONS:
- Which existing exposure rule is the right analogue for watching making: knowhow.watch (4 tiles, 0.04 x (0.5 + curiosity), age 6+; about 0.025 watched steps per juvenile-year in years 100-200 by scaling scout A's smoke) or seeing an act at close range (1 tile, chance 0.5)? Must be decided on the analogy, before data, not on the expected effect size.
- Technique only (GPT) or technique + recipe (Gemini)? If recipe: one notice or two rolls, and how to handle the remember-before-value order problem (knowhow.py:243-244; PT1 0.714 evicted)?
- Plain _gain_skill step towards 1.0 (with the x1.6 focus factor) or a move towards the maker's skill at the imitation/upbringing rates (0.05/0.08, scout A, not re-read)?
- Should adults (no upper age in existing rules; 7.01 adult vs 5.11 juvenile onlookers per make) be watchers?
- Primary: FS1/LC1 world-born adults' 20-40 skill with the +/-0.012 margin (recommended), GPT's young-observer acquisition recast between arms, or Gemini's share with skill > 0.10 (a new number)?
- Matched sham (E13R-style, same draws, no write; config.py:169 precedent) or the standard sham_draw? 200 years or 1,000?
- Is a study whose frozen prior is 'no lasting difference' worth running? The era-matched exposure gives about 0.004-0.006 skill, below the 0.012 margin, unless feedback amplifies it.
- If LS2's Q3 shows the loss is mostly at the choice gate, should the next law be 'learning worth' (missing_abilities_audit:93) instead of technique?
- Should the correction to docs/gpt_view_mission_focus_2026-10-30.md:29-31 (hunt-watching is co-hunters only, actions.py:186-189) be appended?
- Autonomy: do told puzzles count as assigned; does E9 anticipation count as unassigned noticing; do talk-copied values count as own experience?
- Why are own m: puzzles acted on 0.0% in the probe, when mind.py:294 does not close make if the 0.5 x puzzle pull is the largest term? Scout B's explanation is incomplete.
- Include M4 (goal held against reward) descriptively, or declare sign 5 unmeasurable until a nature change adds an intention state?
- Anchor the audit windows to code (THRESHOLD 0.25, SETTLED 0.1, puzzle fade about 41 weeks, 12-week voyage/hearsay life) instead of the unanchored 26/52 weeks?
- Should the autonomy audit run as its own read-only study or as observers on the apprenticeship study's v9 arm, and should a formal feasibility pilot come first?
- Before freezing, should a read-only exposure count across eras be taken on LS2-like worlds instead of relying on one 50-year smoke world?